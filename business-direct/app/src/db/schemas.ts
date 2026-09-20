import { z } from 'zod';

/** The policy record — one per instance (responsible-data.md Part A §2). */
export const Policy = z.object({
  platform_id: z.string(),
  client: z.string(),
  instance: z.string(),
  postal_address: z.string().min(10).optional(),
  jurisdictions: z.array(z.string()).default([]),
  audienceModel: z.enum(['adults', 'mixed', 'child-directed']).default('adults'),
  childData: z.enum(['none', 'age-band', 'age', 'with-parental-consent']).default('none'),
  minorsMarketing: z.object({ profiling: z.literal(false).default(false), targetedAds: z.literal(false).default(false), pushQuietHours: z.tuple([z.number(), z.number()]).default([21, 7]) }).default({ profiling: false, targetedAds: false, pushQuietHours: [21, 7] }),
  channels: z.object({ email: z.enum(['preference', 'consent']).optional(), push: z.enum(['preference', 'consent']).optional(), sms: z.enum(['consent']).optional() }).default({}),
  consentText: z.object({ sms: z.string().optional(), email: z.string().optional() }).default({}),
  cap: z.object({ providerMessagesPerMonth: z.number().int().positive().default(4), countsPlatformDigest: z.literal(false).default(false) }).default({ providerMessagesPerMonth: 4, countsPlatformDigest: false }),
  optOutSlaHours: z.number().default(24),
  aiDisclosure: z.enum(['none', 'label', 'label+text']).optional(),
  privacyPolicy: z.object({ url: z.string().optional(), lastUpdated: z.string().optional(), clauses: z.object({ emailAlerts: z.boolean().default(false), savesOptIn: z.boolean().default(false), childrenNone: z.boolean().default(false) }).default({ emailAlerts: false, savesOptIn: false, childrenNone: false }) }).default({ clauses: { emailAlerts: false, savesOptIn: false, childrenNone: false } }),
  dpia: z.object({ done: z.boolean().default(false), at: z.string().optional() }).default({ done: false }),
  darkPatterns: z.boolean().optional(),
  accessibility: z.boolean().optional(),
  mediaConsent: z.boolean().optional(),
});
export type Policy = z.infer<typeof Policy>;

/** A visitor's preferences — an age, never a name (R24); every switch off until turned on (R28). */
export const FamilyPrefs = z.object({
  family_id: z.string(),
  platform_id: z.string(),
  prefs: z.object({ picks: z.boolean().default(false), alerts: z.boolean().default(false), nearby: z.boolean().default(false), sms: z.boolean().default(false) }).default({ picks: false, alerts: false, nearby: false, sms: false }),
  kids: z.array(z.object({ age: z.number().int().min(0).max(17) }).strict()).max(6).default([]),
  area: z.string().optional(),
  saved: z.array(z.string()).default([]),
  stopped_at: z.string().nullable().default(null),
  paused_until: z.string().nullable().default(null),
  version: z.number().int().default(0),
}).strict();
export type FamilyPrefs = z.infer<typeof FamilyPrefs>;

export const OutboxKind = z.enum(['sequence', 'answer', 'comment_reply', 'social', 'campaign', 'digest', 'alert', 'sms', 'retain']);
export const Channel = z.enum(['email', 'instagram', 'facebook', 'push', 'sms']);

/** An outbox row — the only way anything leaves (architecture.md Part C §7). */
export const OutboxRow = z.object({
  _id: z.string(),
  platform_id: z.string(),
  kind: OutboxKind,
  channel: Channel,
  to: z.object({ family_id: z.string().optional(), provider_id: z.string().optional(), email: z.string().optional() }),
  copy: z.string(),
  subject: z.string().optional(),
  html: z.string().optional(),
  why: z.string().min(1),
  by: z.string().min(1),
  countsTowardCap: z.boolean().default(true),
  state: z.enum(['queued', 'sending', 'sent', 'refused', 'dead']).default('queued'),
  attempts: z.number().int().default(0),
  next_at: z.number(),
  refused_reason: z.string().optional(),
  policy_basis: z.string().optional(),
  created_at: z.number(),
});
export type OutboxRow = z.infer<typeof OutboxRow>;
export type OutboxInput = Omit<OutboxRow, '_id' | 'state' | 'attempts' | 'next_at' | 'created_at' | 'countsTowardCap'> & { countsTowardCap?: boolean; scheduled_for?: number };
