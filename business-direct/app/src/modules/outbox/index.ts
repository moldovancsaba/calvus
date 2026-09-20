import { OutboxRow, type OutboxInput, type Policy, type FamilyPrefs } from '../../db/schemas.js';
import type { Store, Counter } from '../../lib/store.js';
import type { EventLog } from '../../lib/events.js';
import { gate, basis, type Feature } from '../policy/index.js';

export type Sending = { platform_id: string; postal_address: string; daily_cap: number; warm_day: number; bounce_rate: number };
export type ChannelAdapter = { publish(row: OutboxRow): Promise<{ providerMessageId: string }> };
export type Message = { _id: string; platform_id: string; row_id: string; kind: OutboxRow['kind']; channel: OutboxRow['channel']; to: OutboxRow['to']; sent_at: number; provider_message_id: string; why: string; by: string; policy_basis: string };
export type Deps = {
  platformId: string; policy: Policy; sending: Sending;
  outbox: Store<OutboxRow>; messages: Store<Message>; families: Store<FamilyPrefs & { _id: string }>;
  consents: Store<{ _id: string; family_id: string; channel: string; revoked_at: number | null }>;
  optOuts: Store<{ _id: string; provider_id: string }>;
  counter: Counter; events: EventLog; adapters: Partial<Record<OutboxRow['channel'], ChannelAdapter>>; now?: () => number;
};
const FEATURE_OF: Record<OutboxRow['kind'], Feature> = { sequence: 'provider_email', answer: 'provider_email', comment_reply: 'any_draft', social: 'any_draft', campaign: 'audience_saves', digest: 'digest', alert: 'alerts', sms: 'sms', retain: 'provider_email' };
const PREF_OF: Partial<Record<OutboxRow['channel'], keyof FamilyPrefs['prefs']>> = { email: 'picks', push: 'alerts', sms: 'sms' };
const month = (t: number) => new Date(t).toISOString().slice(0, 7);
const warmupCap = (day: number) => Math.min(60, 5 + day * 2); // ponytail: linear warm-up, the research's 4–6 weeks
let seq = 0; const id = () => `ob-${Date.now()}-${++seq}`;

/** The same checks at enqueue (a forecast) and at send (the truth; the cap INCR is atomic) — ADR-3, R3, R4, R23, R26. */
export async function checks(row: OutboxRow, phase: 'enqueue' | 'send', d: Deps): Promise<string | null> {
  const now = d.now?.() ?? Date.now();
  const g = gate(d.policy, FEATURE_OF[row.kind], { at: new Date(now) });
  if (!g.ok) return `policy: ${g.missing.join(', ')}`;
  if (row.to.family_id) {
    const f = (await d.families.find(x => x.family_id === row.to.family_id))[0];
    if (!f || f.stopped_at) return 'stopped';
    if (f.paused_until && new Date(f.paused_until).getTime() > now) return 'paused (stated vulnerability)';
    const pref = PREF_OF[row.channel]; if (pref && !f.prefs[pref] && row.countsTowardCap) return `preference off: ${row.channel}`;
    if (row.channel === 'sms' && !(await d.consents.find(c => c.family_id === f.family_id && c.channel === 'sms' && c.revoked_at === null)).length) return 'no sms consent';
    if (row.countsTowardCap) {
      const key = `cap:${d.platformId}:${f.family_id}:${month(now)}`;
      const n = phase === 'send' ? await d.counter.incr(key) : (await d.counter.get(key)) + 1;
      if (n > d.policy.cap.providerMessagesPerMonth) { if (phase === 'send') await d.counter.decr(key); return `cap ${d.policy.cap.providerMessagesPerMonth}/month reached`; }
    }
  }
  if (row.to.provider_id) {
    if ((await d.optOuts.find(o => o.provider_id === row.to.provider_id)).length) return 'opted out / not my program';
    if (row.channel === 'email') {
      const body = row.html ?? row.copy;
      if (!body.includes(d.sending.postal_address) || !/unsubscribe/i.test(body)) return 'footer: postal address or unsubscribe missing';
      if (d.sending.bounce_rate >= 0.02) return 'paused: bounce rate ≥ 2 %';
      const key = `sent:${d.platformId}:${new Date(now).toISOString().slice(0, 10)}`;
      const sent = phase === 'send' ? await d.counter.incr(key) : (await d.counter.get(key)) + 1;
      if (sent > Math.min(d.sending.daily_cap, warmupCap(d.sending.warm_day))) { if (phase === 'send') await d.counter.decr(key); return 'daily send cap reached (warm-up)'; }
    }
  }
  return null;
}

export async function enqueue(m: OutboxInput, d: Deps): Promise<{ queued: string } | { refused: string }> {
  const now = d.now?.() ?? Date.now();
  const row = OutboxRow.parse({ ...m, _id: id(), state: 'queued', attempts: 0, next_at: m.scheduled_for ?? now, created_at: now });
  const refusal = await checks(row, 'enqueue', d);
  if (refusal) { await d.outbox.put({ ...row, state: 'refused', refused_reason: refusal }); await d.events.emit(d.platformId, 'outbox.refused', { reason: refusal, kind: row.kind }); return { refused: refusal }; }
  await d.outbox.put(row); return { queued: row._id };
}

/** One tick: the lock, a batch, the checks again, the only call into a channel, the message log, backoff, dead-letter. */
export async function send(d: Deps, batch = 100) {
  const now = d.now?.() ?? Date.now();
  if (!(await d.counter.setnx(`lock:send:${d.platformId}`))) return { sent: 0, refused: 0, locked: true };
  try {
    const rows = (await d.outbox.find(r => r.state === 'queued' && r.next_at <= now)).sort((a, b) => a.next_at - b.next_at).slice(0, batch);
    let sent = 0, refused = 0;
    for (const row of rows) {
      const claimed = await d.outbox.update(row._id, { state: 'sending' }, { state: 'queued' }); if (!claimed) continue;
      const refusal = await checks(row, 'send', d);
      if (refusal) { await d.outbox.update(row._id, { state: 'refused', refused_reason: refusal }); refused++; continue; }
      try {
        const adapter = d.adapters[row.channel]; if (!adapter) throw new Error(`no adapter for ${row.channel}`);
        const { providerMessageId } = await adapter.publish(row);
        await d.messages.put({ _id: `m-${row._id}`, platform_id: d.platformId, row_id: row._id, kind: row.kind, channel: row.channel, to: row.to, sent_at: now, provider_message_id: providerMessageId, why: row.why, by: row.by, policy_basis: basis(FEATURE_OF[row.kind], d.policy) });
        await d.outbox.update(row._id, { state: 'sent' }); await d.events.emit(d.platformId, `${row.kind}.sent`, { row_id: row._id, provider_id: row.to.provider_id, family_id: row.to.family_id }); sent++;
      } catch (e) {
        const attempts = row.attempts + 1;
        if (attempts >= 5) await d.outbox.update(row._id, { state: 'dead', refused_reason: String(e) });
        else await d.outbox.update(row._id, { state: 'queued', attempts, next_at: now + 60_000 * 2 ** attempts });
      }
    }
    return { sent, refused, locked: false };
  } finally { await d.counter.del(`lock:send:${d.platformId}`); }
}
/** Stop: every queued row for the visitor is refused, in the same step as the preference change (R28's Stop). */
export async function cancelFor(familyId: string, outbox: Store<OutboxRow>, channel?: OutboxRow['channel']) {
  for (const r of await outbox.find(r => r.to.family_id === familyId && r.state === 'queued' && (!channel || r.channel === channel))) await outbox.update(r._id, { state: 'refused', refused_reason: 'stopped' });
}
