import { describe, it, expect } from 'vitest';
import { patternGuard, templateDrafter } from '../src/modules/drafting/index.js';
import { listings } from './helpers.js';

describe('R32/R36 the pattern guard', () => {
  for (const [text, pattern] of [['Only 3 spots left — book now', 'false urgency or scarcity'], ['Limited time offer', 'false urgency'], ['No thanks, I don\'t want to save money', 'confirmshaming'], ['20% off if you renew today', 'a discount (R13, R37)'], ['We know you can\'t afford it, but…', 'pressure on a stated vulnerability'], ['See [link]', 'unresolved link']] as const)
    it(`refuses "${text}"`, () => { expect(patternGuard(text).map(v => v.pattern)).toContain(pattern); });
  it('passes plain copy', () => { expect(patternGuard('Hi Sam — your page is yours to manage, free. Sessions go on it in minutes: https://example.com/p/1')).toEqual([]); });
});
describe('R10 the template drafter (AI off)', () => {
  const p = listings.find(l => l.email)!;
  it('every sequence step carries the postal address and the unsubscribe footer and passes the guard', () => {
    for (const step of [1, 2, 3] as const) {
      const d = templateDrafter.sequence(step, p, { link: 'https://example.com/p/' + p.id, postal_address: '123 Test Street, New York, NY 10001' });
      expect(d.copy).toContain('123 Test Street'); expect(d.copy).toMatch(/unsubscribe/); expect(d.ai).toBe(false); expect(patternGuard(d.copy)).toEqual([]);
    }
  });
});
