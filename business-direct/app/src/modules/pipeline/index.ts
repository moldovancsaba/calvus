import type { Store } from '../../lib/store.js';
import type { EventLog } from '../../lib/events.js';
import type { Listing } from '../catalogue/index.js';

export const STAGES = ['identified', 'contacted', 'replied', 'applied', 'managing', 'upgraded'] as const;
export type Stage = typeof STAGES[number];
const FORWARD: Record<Stage, Stage[]> = { identified: ['contacted'], contacted: ['replied'], replied: ['applied'], applied: ['managing'], managing: ['upgraded'], upgraded: [] };

export type ProviderState = { _id: string; platform_id: string; stage: Stage; stage_changed_at: number; stage_changed_by: string; score: number; version: number; history: { from: Stage; to: Stage; by: string; override: boolean; at: number }[] };
export class IllegalMove extends Error { constructor(from: Stage, to: Stage) { super(`stage ${from} → ${to} is not an event-driven move; use override with a reason`); } }

export async function ensure(id: string, platformId: string, states: Store<ProviderState>) {
  if (!(await states.get(id))) await states.put({ _id: id, platform_id: platformId, stage: 'identified', stage_changed_at: Date.now(), stage_changed_by: 'sync', score: 0, version: 0, history: [] });
}
/** Forward on events only; a person may move any stage with override, logged with who and why (R9). */
export async function setStage(id: string, to: Stage, by: string, states: Store<ProviderState>, events: EventLog, opts: { override?: boolean; reason?: string } = {}) {
  const s = await states.get(id); if (!s) throw new Error(`no state for ${id}`);
  if (s.stage === to) return s;
  if (!FORWARD[s.stage].includes(to) && !opts.override) throw new IllegalMove(s.stage, to);
  const next = await states.update(id, { stage: to, stage_changed_at: Date.now(), stage_changed_by: by, version: s.version + 1, history: [...s.history, { from: s.stage, to, by, override: !!opts.override, at: Date.now() }] }, { version: s.version });
  if (!next) throw new Error('conflict'); // optimistic concurrency
  await events.emit(s.platform_id, 'stage.changed', { provider_id: id, from: s.stage, to, by, override: !!opts.override, reason: opts.reason });
  return next;
}
/** The propensity score (ADR-13; the prototype's score() with the audit's signals A8). */
export function score(p: Listing, st?: ProviderState, signals: { saved?: boolean; asked?: boolean; optOut?: 'not_mine' | 'bounced' | 'unsubscribed' | null; thread?: boolean } = {}): number {
  if (signals.optOut === 'unsubscribed') return 0;
  let n = 0;
  if (p.email) n += 30; if (p.phone) n += 15; if (p.trial?.available) n += 15; if (p.nextOccurrence) n += 15; if (p.announcement) n += 10; if (p.image) n += 5;
  n += Math.min(10, (p.verifiedFields?.length ?? 0) * 2); if (p.claimStatus === 'unclaimed') n += 10;
  if (st?.stage === 'replied') n += 20; if (st?.stage === 'applied') n += 30; if (signals.thread) n += 10; if (signals.saved || signals.asked) n += 15;
  if (signals.optOut === 'not_mine') n -= 40; if (signals.optOut === 'bounced') n -= 20;
  return Math.max(0, Math.min(100, n));
}
