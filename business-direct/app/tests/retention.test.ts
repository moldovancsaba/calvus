import { describe, it, expect } from 'vitest';
import { signals, drafts } from '../src/modules/retention/index.js';
import { patternGuard } from '../src/modules/drafting/index.js';
import { listings } from './helpers.js';
import type { ProviderState } from '../src/modules/pipeline/index.js';

const DAY = 86_400_000, now = Date.now();
const state = (stage: ProviderState['stage']): ProviderState => ({ _id: 'p', platform_id: 'x', stage, stage_changed_at: now, stage_changed_by: 't', score: 50, version: 0, history: [] });
const vars = { link: 'https://example.com/p/1', postal_address: '123 Test Street, New York, NY 10001' };

describe('R37 retention', () => {
  const l = { ...listings.find(x => x.email)!, updatedAt: new Date(now - 40 * DAY).toISOString() };
  it('a stale page, a renewal within 14 days and an unanswered enquiry each produce exactly one waiting draft', () => {
    const i = { listing: l, state: state('upgraded'), entitlementRenewsAt: now + 10 * DAY, enquiryWaitingSince: now - 3 * DAY, savesLast30d: 4, numbers: { saves: 12, enquiries: 3, enrolled: 1 } };
    expect(signals(i, now)).toEqual(['renewal', 'stale', 'unanswered']);
    const d = drafts(i, [], vars, now); expect(d.map(x => x.signal)).toEqual(['renewal', 'stale', 'unanswered']);
    expect(drafts(i, d, vars, now)).toEqual([]); // no duplicate while a draft waits
  });
  it('no draft contains a discount or a banned pattern; every draft carries the footer and the advertiser\'s numbers', () => {
    const i = { listing: l, state: state('upgraded'), entitlementRenewsAt: now + 3 * DAY, savesLast30d: 0, numbers: { saves: 12, enquiries: 3, enrolled: 1 } };
    for (const d of drafts(i, [], vars, now)) { expect(patternGuard(d.copy)).toEqual([]); expect(d.copy).toContain(vars.postal_address); expect(d.ai).toBe(false); }
    expect(drafts(i, [], vars, now).find(d => d.signal === 'renewal')!.copy).toContain('12 families saved');
  });
  it('a listing that is not managing has no signals', () => { expect(signals({ listing: l, state: state('contacted'), savesLast30d: 0, numbers: { saves: 0, enquiries: 0, enrolled: 0 } }, now)).toEqual([]); });
});
