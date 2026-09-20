import type { Listing } from '../catalogue/index.js';
import type { ProviderState } from '../pipeline/index.js';
import { templateDrafter, patternGuard } from '../drafting/index.js';

export type Signal = 'renewal' | 'stale' | 'unanswered' | 'no_saves';
export type RetentionInput = { listing: Listing; state: ProviderState; entitlementRenewsAt?: number; enquiryWaitingSince?: number; savesLast30d: number; numbers: { saves: number; enquiries: number; enrolled: number } };
const DAY = 86_400_000;
/** The four signals that precede a cancellation (R37). */
export function signals(i: RetentionInput, now = Date.now()): Signal[] {
  if (!['managing', 'upgraded'].includes(i.state.stage)) return [];
  const s: Signal[] = [];
  if (i.entitlementRenewsAt && i.entitlementRenewsAt - now <= 14 * DAY) s.push('renewal');
  if (i.listing.updatedAt && now - new Date(i.listing.updatedAt).getTime() >= 30 * DAY) s.push('stale');
  if (i.enquiryWaitingSince && now - i.enquiryWaitingSince >= 2 * DAY) s.push('unanswered');
  if (i.savesLast30d === 0) s.push('no_saves');
  return s;
}
export type RetainDraft = { provider_id: string; signal: Signal; renewal: boolean; copy: string; why: string; ai: false };
/** One drafted touch per signal, from the advertiser's own numbers, never a discount; an existing waiting draft for the signal is not duplicated. */
export function drafts(i: RetentionInput, existing: RetainDraft[], vars: { link: string; postal_address: string }, now = Date.now()): RetainDraft[] {
  const out: RetainDraft[] = [];
  for (const sig of signals(i, now)) {
    if (existing.some(e => e.provider_id === i.listing.id && e.signal === sig)) continue;
    const d = templateDrafter.retain(sig, i.listing, i.numbers, vars);
    if (patternGuard(d.copy).length) continue; // a retention draft with a banned pattern is never produced
    out.push({ provider_id: i.listing.id, signal: sig, renewal: sig === 'renewal', copy: d.copy, why: d.why, ai: false });
  }
  return out;
}
