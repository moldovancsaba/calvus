import { describe, it, expect } from 'vitest';
import { enqueue, send } from '../src/modules/outbox/index.js';
import { stop } from '../src/modules/families/index.js';
import { deps, family, footer, emptyPolicy, PLATFORM } from './helpers.js';

const seqRow = (d: ReturnType<typeof deps>, pid = 'p1') => ({ platform_id: PLATFORM, kind: 'sequence' as const, channel: 'email' as const, to: { provider_id: pid, email: 'coach@example.com' }, copy: 'Hi' + footer(d.sending.postal_address), why: 'step 1', by: 'sequence:invite' });
const famRow = (fid: string, extra: Partial<Parameters<typeof enqueue>[0]> = {}) => ({ platform_id: PLATFORM, kind: 'campaign' as const, channel: 'email' as const, to: { family_id: fid }, copy: 'A trial class near you', why: 'you saved this provider', by: 'campaign:c1', ...extra });

describe('ADR-4 the outbox is the only sender; R26 the gate runs at enqueue and at send', () => {
  it('refuses a provider e-mail when the policy record lacks the postal address', async () => {
    const d = deps(emptyPolicy());
    const r = await enqueue(seqRow(d), d); expect(r).toEqual({ refused: 'policy: postal_address, jurisdictions' });
  });
  it('R23 refuses a provider e-mail without the postal address in the body, and pauses at bounce ≥ 2 %', async () => {
    const d = deps();
    expect(await enqueue({ ...seqRow(d), copy: 'Hi — unsubscribe' }, d)).toEqual({ refused: 'footer: postal address or unsubscribe missing' });
    const d2 = deps(); d2.sending.bounce_rate = 0.021;
    expect(await enqueue(seqRow(d2), d2)).toEqual({ refused: 'paused: bounce rate ≥ 2 %' });
  });
  it('sends a valid row once: a message row with why, by and the policy basis; an event; the lock released', async () => {
    const d = deps(); const q = await enqueue(seqRow(d), d); expect('queued' in q).toBe(true);
    const r = await send(d); expect(r).toEqual({ sent: 1, refused: 0, locked: false });
    const m = (await d.messages.find(() => true))[0]; expect(m.why).toBe('step 1'); expect(m.policy_basis).toMatch(/provider_email/); expect(d.events.count('sequence.sent')).toBe(1);
    expect(await send(d)).toEqual({ sent: 0, refused: 0, locked: false });
  });
  it('excludes an opted-out advertiser (not my program)', async () => {
    const d = deps(); await d.optOuts.put({ _id: 'o1', provider_id: 'p1' });
    expect(await enqueue(seqRow(d), d)).toEqual({ refused: 'opted out / not my program' });
  });
});
describe('R3 the cap — checked at enqueue, counted atomically at send', () => {
  it('a race of two sends against one remaining slot delivers exactly one', async () => {
    const d = deps(); d.policy.cap.providerMessagesPerMonth = 1; await d.families.put(family('f1'));
    await enqueue(famRow('f1'), d); await enqueue(famRow('f1'), d); // both forecasts pass: the cap is not consumed at enqueue
    expect((await d.outbox.find(r => r.state === 'queued')).length).toBe(2);
    const r = await send(d); expect(r.sent).toBe(1); expect(r.refused).toBe(1);
    expect((await d.outbox.find(r => r.refused_reason === 'cap 1/month reached')).length).toBe(1);
  });
  it("the site's own digest and alerts do not count toward the cap", async () => {
    const d = deps(); d.policy.cap.providerMessagesPerMonth = 1; await d.families.put(family('f1'));
    await enqueue(famRow('f1'), d); await enqueue({ ...famRow('f1'), kind: 'digest', why: 'your Sunday picks', by: 'digest', countsTowardCap: false }, d);
    const r = await send(d); expect(r).toMatchObject({ sent: 2, refused: 0 });
  });
  it('R4 SMS is impossible without a consent row; a preference off refuses the channel', async () => {
    const d = deps(); await d.families.put(family('f1', { sms: true }));
    expect(await enqueue({ ...famRow('f1'), kind: 'sms', channel: 'sms' }, d)).toEqual({ refused: 'no sms consent' });
    await d.families.put(family('f2', { picks: false }));
    expect(await enqueue(famRow('f2'), d)).toEqual({ refused: 'preference off: email' });
  });
});
describe('R28 Stop', () => {
  it('turns every channel off and cancels what is queued in one operation', async () => {
    const d = deps(); await d.families.put(family('f1', { sms: true })); await enqueue(famRow('f1'), d); await enqueue({ ...famRow('f1'), channel: 'push' }, d);
    await stop('f1', PLATFORM, d.families, d.outbox, d.consents as any, d.events);
    const f = (await d.families.find(x => x.family_id === 'f1'))[0]; expect(f.prefs).toEqual({ picks: false, alerts: false, nearby: false, sms: false }); expect(f.stopped_at).toBeTruthy();
    expect((await d.outbox.find(r => r.state === 'refused' && r.refused_reason === 'stopped')).length).toBe(2);
    expect(await enqueue(famRow('f1'), d)).toEqual({ refused: 'stopped' });
  });
});
describe('R24 a child is an age, never a name', () => {
  it('the visitor schema has no name field for a child', async () => {
    const { FamilyPrefs } = await import('../src/db/schemas.js');
    expect(() => FamilyPrefs.parse({ family_id: 'f', platform_id: PLATFORM, kids: [{ age: 5, name: 'Leo' }] })).toThrow();
    expect(FamilyPrefs.parse({ family_id: 'f', platform_id: PLATFORM }).prefs).toEqual({ picks: false, alerts: false, nearby: false, sms: false });
  });
});
