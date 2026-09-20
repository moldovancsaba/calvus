import { Policy, FamilyPrefs, type OutboxRow } from '../src/db/schemas.js';
import { MemoryStore, MemoryCounter } from '../src/lib/store.js';
import { EventLog } from '../src/lib/events.js';
import type { Deps, Message } from '../src/modules/outbox/index.js';
import fixture from '../fixtures/providers.json' with { type: 'json' };
import type { Listing } from '../src/modules/catalogue/index.js';

export const listings = (fixture as { providers: Listing[] }).providers;
export const PLATFORM = 'yourfield-nyc';

/** A policy record with every field the gate needs — the test's "complete" instance. */
export const completePolicy = (): Policy => Policy.parse({
  platform_id: PLATFORM, client: 'ClassScout', instance: 'Your Field NYC', postal_address: '123 Test Street, New York, NY 10001',
  jurisdictions: ['US-NY', 'US'], channels: { email: 'preference', push: 'preference', sms: 'consent' }, consentText: { sms: 'Reply YES to receive texts from {provider} via Your Field. Msg&data rates may apply. Reply STOP to end.' },
  aiDisclosure: 'label', privacyPolicy: { clauses: { emailAlerts: true, savesOptIn: true, childrenNone: true } }, darkPatterns: true, accessibility: true, mediaConsent: true,
});
export const emptyPolicy = (): Policy => Policy.parse({ platform_id: PLATFORM, client: 'ClassScout', instance: 'Your Field NYC' });

export function deps(policy = completePolicy(), overrides: Partial<Deps> = {}): Deps {
  const adapters = { email: { publish: async () => ({ providerMessageId: 'r-' + Math.random().toString(36).slice(2) }) }, push: { publish: async () => ({ providerMessageId: 'p1' }) }, sms: { publish: async () => ({ providerMessageId: 's1' }) } };
  return {
    platformId: PLATFORM, policy, sending: { platform_id: PLATFORM, postal_address: policy.postal_address ?? '', daily_cap: 60, warm_day: 42, bounce_rate: 0.008 },
    outbox: new MemoryStore<OutboxRow>(), messages: new MemoryStore<Message>(), families: new MemoryStore<FamilyPrefs & { _id: string }>(),
    consents: new MemoryStore(), optOuts: new MemoryStore(), counter: new MemoryCounter(), events: new EventLog(), adapters, ...overrides,
  };
}
export const family = (id: string, prefs: Partial<FamilyPrefs['prefs']> = {}) => ({ ...FamilyPrefs.parse({ family_id: id, platform_id: PLATFORM, prefs: { picks: true, alerts: true, ...prefs }, kids: [{ age: 5 }] }), _id: id });
export const footer = (postal: string) => `\n\n${postal} · unsubscribe`;
