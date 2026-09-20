import type { Store } from '../../lib/store.js';
import type { EventLog } from '../../lib/events.js';

/** A listing as the first instance's API returns it (the fields the modules read). */
export type Listing = {
  id: string; name: string; category?: string; borough?: string; neighborhood?: string;
  email?: string | null; phone?: string | null; website?: string | null; image?: string | null;
  primaryActivityType?: string | null; nextOccurrence?: unknown; announcement?: unknown; trial?: { available?: boolean; free?: boolean } | null;
  claimStatus?: string | null; verifiedFields?: unknown[]; updatedAt?: string; sessions?: unknown[]; price?: unknown; contactKind?: 'role' | 'person';
};
export type Cached = Listing & { _id: string; platform_id: string; synced_at: number };

/** The connector interface (architecture.md Part B §6): reads are public, writes need a key. */
export interface PlatformConnector {
  listProviders(): Promise<Listing[]>;
  createClaimRequest?(providerId: string, contact: string): Promise<void>; // keyed
  setCardFlag?(providerId: string, flag: 'featured' | 'camp' | 'profile', on: boolean): Promise<void>; // keyed
}
export class NotKeyed extends Error { constructor(op: string) { super(`connector: ${op} needs the site's key`); } }

/** A connector over a fixture (the demo sample) — the contract test's double and the reference for `YourFieldConnector`. */
export class FixtureConnector implements PlatformConnector {
  constructor(private rows: Listing[]) {}
  async listProviders() { return this.rows.map(r => ({ ...r })); }
  set(rows: Listing[]) { this.rows = rows; }
}

const WATCHED: (keyof Listing)[] = ['sessions', 'trial', 'announcement', 'nextOccurrence', 'email', 'phone', 'claimStatus'];
const changed = (a: Cached, b: Listing) => WATCHED.filter(k => JSON.stringify(a[k] ?? null) !== JSON.stringify(b[k] ?? null));

/** Pull the catalogue, diff against the cache, emit events; never edits the cache by hand. */
export async function sync(platformId: string, c: PlatformConnector, cache: Store<Cached>, events: EventLog, ensure: (id: string) => Promise<void>) {
  const remote = await c.listProviders();
  for (const r of remote) {
    const prev = await cache.get(r.id);
    const doc: Cached = { ...r, _id: r.id, platform_id: platformId, synced_at: Date.now() };
    if (!prev) { await cache.put(doc); await events.emit(platformId, 'provider.new', { provider_id: r.id }); await ensure(r.id); continue; }
    if (prev.updatedAt === r.updatedAt) continue;
    const diff = changed(prev, r);
    await cache.put(doc);
    if (diff.length) await events.emit(platformId, 'provider.changed', { provider_id: r.id, changes: diff });
    if (diff.includes('sessions') || diff.includes('nextOccurrence')) await events.emit(platformId, 'provider.new_session', { provider_id: r.id });
  }
  return remote.length;
}
