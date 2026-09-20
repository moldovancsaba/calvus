import { describe, it, expect } from 'vitest';
import { gate, blockedBy } from '../src/modules/policy/index.js';
import { completePolicy, emptyPolicy } from './helpers.js';
import { Policy } from '../src/db/schemas.js';

describe('R26 the policy gate — every row of the framework', () => {
  const empty = emptyPolicy(), full = completePolicy();
  it('provider e-mail needs the postal address and the jurisdictions', () => {
    expect(gate(empty, 'provider_email')).toEqual({ ok: false, missing: ['postal_address', 'jurisdictions'] });
    expect(gate(full, 'provider_email')).toEqual({ ok: true });
  });
  it('the digest and alerts need the e-mail channel and the privacy-policy clause', () => {
    expect(gate(empty, 'digest').ok).toBe(false);
    expect((gate(empty, 'digest') as any).missing).toContain('privacyPolicy.clauses.emailAlerts');
    expect(gate(full, 'alerts')).toEqual({ ok: true });
  });
  it('campaign audiences need the saves opt-in clause', () => { expect(gate(empty, 'audience_saves')).toEqual({ ok: false, missing: ['privacyPolicy.clauses.savesOptIn'] }); expect(gate(full, 'audience_saves').ok).toBe(true); });
  it('SMS needs the consent basis and the consent text', () => { expect(gate(empty, 'sms').ok).toBe(false); expect(gate(full, 'sms').ok).toBe(true); });
  it('AI drafts and generated media need the disclosure rule', () => { expect(gate(empty, 'ai_draft')).toEqual({ ok: false, missing: ['aiDisclosure'] }); expect(gate(empty, 'generated_media').ok).toBe(false); expect(gate(full, 'generated_media').ok).toBe(true); });
  it("a minor's field: an age is allowed on an adults instance; anything else needs childData; a mixed instance needs a DPIA", () => {
    expect(gate(full, 'minor_field', { field: 'age' }).ok).toBe(true);
    expect(gate(full, 'minor_field', { field: 'name' })).toEqual({ ok: false, missing: ['childData'] });
    const mixed = Policy.parse({ ...full, audienceModel: 'mixed' });
    expect(gate(mixed, 'minor_field', { field: 'age' })).toEqual({ ok: false, missing: ['dpia'] });
  });
  it('push respects quiet hours on a mixed instance only', () => {
    const mixed = Policy.parse({ ...full, audienceModel: 'mixed' });
    const night = new Date(); night.setHours(23, 0, 0, 0); const day = new Date(); day.setHours(12, 0, 0, 0);
    expect(gate(mixed, 'push', { at: night }).ok).toBe(false); expect(gate(mixed, 'push', { at: day }).ok).toBe(true); expect(gate(full, 'push', { at: night }).ok).toBe(true);
  });
  it('R30 clips from a recording that shows children need the consent reference', () => { expect(gate(full, 'clips_children', { consentRef: null }).ok).toBe(false); expect(gate(full, 'clips_children', { consentRef: 'c-1' }).ok).toBe(true); });
  it('R31 safeguarding is never claimed', () => { expect(gate(full, 'safeguarding_claim').ok).toBe(false); });
  it('R34/R36 any draft needs the dark-pattern and accessibility rules', () => { expect(gate(empty, 'any_draft')).toEqual({ ok: false, missing: ['darkPatterns', 'accessibility'] }); expect(gate(full, 'any_draft').ok).toBe(true); });
  it('the Policy screen inverts NEEDS: a missing field lists the features it blocks', () => {
    const b = blockedBy(empty);
    expect(b['postal_address']).toEqual(['provider_email']); expect(b['aiDisclosure']).toEqual(['ai_draft', 'generated_media']);
    expect(Object.keys(blockedBy(full)).sort()).toEqual(['childData', 'mediaConsent', 'never']); // a complete adults instance still blocks any child field but an age, footage without consent, and any safeguarding claim
  });
});
