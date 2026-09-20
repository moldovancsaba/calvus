import { Policy } from '../../db/schemas.js';

/** The features the gate knows (responsible-data.md Part A §3, ten rows). */
export type Feature = 'provider_email' | 'digest' | 'alerts' | 'audience_saves' | 'sms' | 'ai_draft' | 'generated_media' | 'minor_field' | 'push' | 'clips_children' | 'safeguarding_claim' | 'any_draft';
export type GateCtx = { at?: Date; field?: string; consentRef?: string | null };

const miss = (p: Policy, fields: string[]) => fields.filter(f => {
  const v = f.split('.').reduce<any>((o, k) => (o == null ? o : o[k]), p);
  return v === undefined || v === null || v === '' || (Array.isArray(v) && v.length === 0);
});
const inQuietHours = (at: Date, [from, to]: [number, number]) => { const h = at.getHours(); return from > to ? (h >= from || h < to) : (h >= from && h < to); };

/** Returns the policy fields a feature needs and does not have — empty means the feature may run. */
export const NEEDS: Record<Feature, (p: Policy, ctx: GateCtx) => string[]> = {
  provider_email: p => miss(p, ['postal_address', 'jurisdictions']),
  digest: p => miss(p, ['channels.email']).concat(p.privacyPolicy.clauses.emailAlerts ? [] : ['privacyPolicy.clauses.emailAlerts']),
  alerts: (p, c) => NEEDS.digest(p, c),
  audience_saves: p => (p.privacyPolicy.clauses.savesOptIn ? [] : ['privacyPolicy.clauses.savesOptIn']),
  sms: p => (p.channels.sms === 'consent' && p.consentText.sms ? [] : ['channels.sms', 'consentText.sms']),
  ai_draft: p => (p.aiDisclosure ? [] : ['aiDisclosure']),
  generated_media: (p, c) => NEEDS.ai_draft(p, c),
  minor_field: (p, c) => (p.audienceModel !== 'adults' && !p.dpia.done ? ['dpia'] : c.field !== 'age' && p.childData === 'none' ? ['childData'] : []),
  push: (p, c) => (p.audienceModel !== 'adults' && inQuietHours(c.at ?? new Date(), p.minorsMarketing.pushQuietHours) ? ['quietHours'] : []),
  clips_children: (_p, c) => (c.consentRef ? [] : ['mediaConsent']),
  safeguarding_claim: () => ['never'], // R31: never claimed, only displayed as verified
  any_draft: p => miss(p, ['darkPatterns', 'accessibility']),
};

export type GateResult = { ok: true } | { ok: false; missing: string[] };
export function gate(policy: Policy, feature: Feature, ctx: GateCtx = {}): GateResult {
  const missing = NEEDS[feature](policy, ctx);
  return missing.length ? { ok: false, missing } : { ok: true };
}
/** What the Policy screen shows: per field, the features it blocks (the inversion of NEEDS). */
export function blockedBy(policy: Policy): Record<string, Feature[]> {
  const out: Record<string, Feature[]> = {};
  for (const f of Object.keys(NEEDS) as Feature[]) for (const m of NEEDS[f](policy, {})) (out[m] ??= []).push(f);
  return out;
}
/** The policy basis written on every message (R26). */
export const basis = (feature: Feature, p: Policy) => `${feature}: ${p.jurisdictions.join('+') || 'no-jurisdiction'}; cap ${p.cap.providerMessagesPerMonth}/month`;
