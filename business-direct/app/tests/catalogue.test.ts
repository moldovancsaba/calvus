import { describe, it, expect } from 'vitest';
import { FixtureConnector, sync, type Cached } from '../src/modules/catalogue/index.js';
import { MemoryStore } from '../src/lib/store.js';
import { EventLog } from '../src/lib/events.js';
import { ensure, type ProviderState } from '../src/modules/pipeline/index.js';
import { listings, PLATFORM } from './helpers.js';

describe('P2 the connector and sync — contract against the demo sample', () => {
  it('caches every listing of the sample and starts each at identified', async () => {
    const cache = new MemoryStore<Cached>(), states = new MemoryStore<ProviderState>(), events = new EventLog();
    const n = await sync(PLATFORM, new FixtureConnector(listings), cache, events, id => ensure(id, PLATFORM, states));
    expect(n).toBe(listings.length);
    expect((await cache.find(() => true)).length).toBe(listings.length);
    expect((await states.find(s => s.stage === 'identified')).length).toBe(listings.length);
    expect(events.count('provider.new')).toBe(listings.length);
  });
  it('a changed updatedAt with a new session produces exactly one diff event and one new-session event', async () => {
    const cache = new MemoryStore<Cached>(), states = new MemoryStore<ProviderState>(), events = new EventLog();
    const c = new FixtureConnector(listings);
    await sync(PLATFORM, c, cache, events, id => ensure(id, PLATFORM, states));
    const changed = listings.map((l, i) => i === 0 ? { ...l, updatedAt: '2099-01-01T00:00:00Z', nextOccurrence: { weekday: 'Saturday', startTime: '10:00' } } : l);
    c.set(changed);
    await sync(PLATFORM, c, cache, events, id => ensure(id, PLATFORM, states));
    expect(events.count('provider.changed')).toBe(1); expect(events.count('provider.new_session')).toBe(1);
    expect(events.count('provider.new')).toBe(listings.length);
  });
  it('schema drift: every listing in the sample carries id, name and a borough', () => {
    for (const l of listings) { expect(l.id).toBeTruthy(); expect(l.name).toBeTruthy(); expect(l.borough).toBeTruthy(); }
  });
});
