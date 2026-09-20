import { describe, it, expect } from 'vitest';
import { MemoryStore } from '../src/lib/store.js';
import { EventLog } from '../src/lib/events.js';
import { ensure, setStage, score, IllegalMove, type ProviderState } from '../src/modules/pipeline/index.js';
import { listings, PLATFORM } from './helpers.js';

describe('R9 the stage machine', () => {
  it('moves forward on events and refuses a skip', async () => {
    const states = new MemoryStore<ProviderState>(), events = new EventLog(); await ensure('p1', PLATFORM, states);
    await setStage('p1', 'contacted', 'sequence step 1', states, events);
    await expect(setStage('p1', 'managing', 'reply', states, events)).rejects.toBeInstanceOf(IllegalMove);
    expect((await states.get('p1'))!.stage).toBe('contacted');
  });
  it('a person may move any stage with override, logged with who and why', async () => {
    const states = new MemoryStore<ProviderState>(), events = new EventLog(); await ensure('p1', PLATFORM, states);
    const s = await setStage('p1', 'managing', 'operator:anna', states, events, { override: true, reason: 'claimed by phone' });
    expect(s.stage).toBe('managing'); expect(s.history.at(-1)).toMatchObject({ by: 'operator:anna', override: true });
    expect(events.rows.at(-1)!.props).toMatchObject({ override: true, reason: 'claimed by phone' });
  });
});
describe('R22 the propensity score', () => {
  it('orders the sample: e-mail and a next session score above a website-only listing; an unsubscribed address scores 0', () => {
    const withEmail = listings.find(l => l.email && l.nextOccurrence)!, webOnly = listings.find(l => !l.email && !l.phone)!;
    expect(score(withEmail)).toBeGreaterThan(score(webOnly));
    expect(score(withEmail, undefined, { optOut: 'unsubscribed' })).toBe(0);
    expect(score(withEmail, undefined, { optOut: 'not_mine' })).toBe(Math.max(0, score(withEmail) - 40));
    expect(score(withEmail, undefined, { saved: true })).toBe(Math.min(100, score(withEmail) + 15));
  });
});
