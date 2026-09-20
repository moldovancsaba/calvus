# business.direct — research V: beyond children — the other people, data and practices a responsible marketing machine must cover

> **Status — evidence.** Written while the project was framed around the first customer's site; the vocabulary of that time (client, platform, provider, family) is kept, the product's terms are in `product-definition.md` §5. Every figure the stakeholder documents use from this round was re-verified on 2026-09-20 in `evidence.md`, which is the authority where the two differ.


*Fifth research round, 2026-09-19, on the owner's question: "Is there any other use case like
kids that we need to cover, or could we cover, as a responsible business entity?" The
answer is yes — eleven of them, in three groups: **people** the law or good practice treats as
needing more care, **data categories** that may never drive marketing, and **practices**
that are banned whoever the audience is. Each is anchored in a primary source where one
exists (**P**), otherwise a law-firm or trade summary (**A**), and each ends with the rule
it becomes in the framework (`responsible-data.md`, rules R30–R36) and
what the prototype does about it. Two of the eleven are already live in our first client's
own category and were gaps: real footage of children (§1.2) and the adults who work with
them (§1.3).*

## 1. People who need more care

### 1.1 Children — covered (research IV)
A child is an age, never a name; no profiling or targeting; the platform's own policy
(adults only, no children's data) binds the machine. Rules R15, R24, R27.

### 1.2 Children in real footage — a gap we had
The clip engine (D28) cuts a provider's session recording into the week's Reels. A session
recording of a kids' soccer class is a video of children. Every safeguarding body's guidance
is the same: **written parental consent before a child under 16 is photographed or filmed,
the child's own wishes honoured, no identifying detail (name, club, location) with the
image**, and consent that can be withdrawn. **P** [NSPCC: photographing and filming children](https://learning.nspcc.org.uk/online-safety/photographing-filming-children),
[CPSU: photography and filming in sport](https://thecpsu.org.uk/help-advice/topics/photography-and-filming-in-sports-and-activities/),
[The FA guidance note 8.3](https://www.thefa.com/-/media/thefacom-new/files/rules-and-regulations/safeguarding/section-8/8-3-photographing-and-filming-children-colour-version.ashx)
The 2025 COPPA rule also counts audio and images of a child as personal information
(research IV §1.1).
**Rule R30 (media consent):** a recording that shows a child is cut only when the provider
confirms it holds written parental consent for every child shown, the clip carries no
child's name or identifying detail, and the consent record is kept with the clip; without
it the clip engine refuses and offers the coach-only or place-only cut.

### 1.3 The adults who work with children — safeguarding
US youth sports run on background checks and SafeSport training for every adult in regular
contact with minors (thirteen states now require checks by statute; national bodies
require them every two years), and in the UK the club or activity provider owes a **duty of
care** to keep children safe. **A** [Sports Management Resources](https://sportsmanagementresources.com/library/background-and-reference-checks-and-required-safesport-training-covered-individuals),
[Secure Search Pro: state requirements](https://securesearchpro.com/youth-sports-background-check-requirements-by-state/);
**P** [CPSU: duty of care](https://thecpsu.org.uk/resource-library/best-practice/duty-of-care/),
[U.S. Soccer Safe Soccer Clearance](https://www.ussoccer.com/soccer-forward/resource-hub/safe-soccer-clearance-program)
The machine markets providers to families. It must never imply a safeguarding standard it
has not verified, and it can make the verified standard a visible, honest signal.
**Rule R31 (safeguarding signal):** a provider's safeguarding status (background checks,
safeguarding training, a named welfare contact) is shown only as the platform verified it
— "not verified" is a valid, displayed state; marketing copy never claims safety; a family's
enquiry template can ask.

### 1.4 People in vulnerable circumstances
UK financial regulation (the Consumer Duty, FG21/1 and the 2025 review) expects firms to
identify customers in vulnerable circumstances — health, life events such as bereavement,
low resilience, low capability — and to design communications and support around them;
the EU's Unfair Commercial Practices Directive judges a practice by its effect on the
vulnerable group it reaches ("mental or physical infirmity, age or credulity"). **P**
[FCA: fair treatment of vulnerable customers](https://www.fca.org.uk/publications/finalised-guidance/guidance-firms-fair-treatment-vulnerable-customers),
[EU UCPD](https://commission.europa.eu/law/law-topic/consumer-protection-law/unfair-commercial-practices-and-price-indication/unfair-commercial-practices-directive_en);
**A** [Covington on the 2025 FCA review](https://www.cov.com/en/news-and-insights/insights/2025/04/fca-publishes-findings-on-firms-treatment-of-consumers-in-vulnerable-circumstances)
For a marketing machine this means: no urgency or scarcity pressure ("today only", "3 spots
left" unless literally true), a cooling-off on any purchase, plain language, a human
pathway on request, and a pause when a person signals a life event.
**Rule R32 (no pressure, plain language, a pause):** no false urgency or scarcity in any
draft (the voice file already bans it; the gate enforces it); a person who says "not now",
"bereavement", "can't afford" or asks for a human gets a pause on all marketing and a
human reply; every purchase has a cooling-off.

### 1.5 Protected characteristics in targeting and ad delivery
The US Department of Justice settled with Meta in 2022 over housing ads whose delivery
relied on race, national origin and sex — a Fair Housing Act case about the *algorithm*,
not the advertiser's intent; employment and credit advertising carry the same rules (ADEA,
ECOA). **P** [DOJ settlement, June 2022](https://www.justice.gov/archives/opa/pr/justice-department-secures-groundbreaking-settlement-agreement-meta-platforms-formerly-known)
Our audiences are saves, asks and neighbourhood — and neighbourhood correlates with
protected characteristics. The rule must be explicit.
**Rule R33 (no protected characteristic, directly or by proxy):** audiences and content
slots are never built or optimised on race, ethnicity, religion, sex, disability, family
status or national origin — nor on a proxy for them; the neighbourhood holdout and the
content-slot rule (R18) are audited for disparate delivery, and a job-portal or housing
instance adds the market's specific ad rules to its policy record.

### 1.6 People with disabilities — accessibility of every message
The European Accessibility Act applies since 28 June 2025 to electronic communications and
digital services, including e-mail and web content aimed at EU consumers; about 101 million
people in the EU live with a disability. **A** [WFA on the EAA](https://wfanet.org/knowledge/item/2025/06/13/european-accessibility-act-what-it-means-for-marketers),
[Level Access: EAA requirements](https://www.levelaccess.com/compliance-overview/european-accessibility-act-eaa/)
In the US the ADA's web-accessibility standard is WCAG in practice. The prototype already
holds 44 px targets, one `h1`, alt text and contrast ≥ 4.5 : 1; the messages the machine
sends must hold the same.
**Rule R34 (accessible by default):** every e-mail, page and post the machine produces
meets WCAG 2.2 AA (structure, alt text on real media, captions on every clip, contrast,
plain language); captions are part of the clip engine's output, not an option.

## 2. Data categories that never drive marketing

| Category | Law / case | What it means for the machine |
|---|---|---|
| **Health, reproductive, mental health** | FTC v. GoodRx ($1.5 M, Feb 2023) and BetterHelp ($7.8 M, 2023): sharing health data with ad platforms, banned from using it for advertising. **P** [FTC: GoodRx](https://www.ftc.gov/news-events/news/press-releases/2023/02/ftc-enforcement-action-bar-goodrx-sharing-consumers-sensitive-health-info-advertising), [FTC: BetterHelp](https://www.ftc.gov/news-events/news/press-releases/2023/07/ftc-gives-final-approval-order-banning-betterhelp-sharing-sensitive-health-data-advertising) | a family's note that a child has a condition (an enquiry: "my son has ADHD, is the class suitable?") is an answer to give, never a field to store or a segment to build |
| **Precise location and sensitive places** | FTC v. Kochava (2022–2026): selling location that reveals visits to clinics, places of worship, schools, shelters; the order bars it without opt-in consent. **P** [FTC complaint, Aug 2022](https://www.ftc.gov/news-events/news/press-releases/2022/08/ftc-sues-kochava-selling-data-tracks-people-reproductive-health-clinics-places-worship-other); **A** [White & Case](https://www.whitecase.com/insight-alert/ftc-settles-data-broker-kochava-over-sale-sensitive-location-data-key-takeaways) | the machine uses a neighbourhood the family chose, never a device location; "nearby" is a preference, not a track |
| **Biometrics, voice, face** | Illinois BIPA: written notice and consent before any face or voice template; private right of action, $1,000+ per person. **A** [ACLU of Illinois](https://www.aclu-il.org/campaigns-initiatives/biometric-information-privacy-act-bipa/); COPPA 2025 adds biometrics for children | no face recognition in the clip engine; voice cloning only with the coach's written consent, never a child's voice |
| **GDPR Article 9 special categories** (ethnicity, religion, politics, union, genetics, biometrics, health, sex life or orientation) | processing prohibited unless an exception applies; explicit consent for marketing is practically never obtained. **P** [Art. 9 GDPR](https://gdpr-info.eu/art-9-gdpr/) | on any EU instance these fields do not exist in the machine; a job portal instance must not infer them from a CV |
| **Financial hardship, debt** | UCPD and the FCA's vulnerability guidance (§1.4) | "can't afford" pauses marketing; discounts are not the machine's tool (R13) |
| **Immigration status, family status** | protected under fair-housing and employment rules in the US; special or sensitive in the EU | never stored, never inferred |

**Rule R35 (sensitive categories):** the machine stores no health, location-track,
biometric, Article 9 or financial-hardship data about a person; when one arrives in a
message it is answered and not recorded as a field; no audience, slot or score uses one.

## 3. Practices banned whoever the audience is

- **Dark patterns.** The FTC's 2022 report *Bringing Dark Patterns to Light* (false urgency,
  hidden costs, obstruction of cancellation, pre-ticked boxes, confirmshaming) and the EU
  DSA Article 25 (interfaces that "deceive or manipulate … or otherwise materially distort
  or impair" free decisions). **P** [FTC report (PDF)](https://www.ftc.gov/system/files/ftc_gov/pdf/P214800+Dark+Patterns+Report+9.14.2022+-+FINAL.pdf),
  [DSA Art. 25](https://dsa-library.com/article/25/)
- **AI manipulation.** EU AI Act Article 5, applicable since 2 February 2025, prohibits AI
  systems that use manipulative or deceptive techniques to distort behaviour, and systems
  that exploit vulnerabilities of age, disability or socio-economic situation. **A** [Future of Privacy Forum](https://fpf.org/blog/red-lines-under-the-eu-ai-act-understanding-manipulative-techniques-and-the-exploitation-of-vulnerabilities/),
  [WilmerHale](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20240408-prohibited-ai-practices-a-deep-dive-into-article-5-of-the-european-unions-ai-act)
- **Frequency and timing.** Push notification hours for minors (Nebraska, California —
  research IV); the cap and quiet hours already exist.

**Rule R36 (no dark pattern, no manipulation):** a banned-pattern list is enforced on every
draft and every screen — no false urgency or scarcity, no pre-ticked consent, no
confirmshaming, no obstruction of Stop or unsubscribe (one tap, always), no hidden cost;
an AI draft that scores a person's vulnerability or pressures on it is refused.

## 4. What it means for other clients (the framework generalises)

| Client type | The case that matters most | Policy fields |
|---|---|---|
| Kids' activities (Your Field) | children in footage; the adults who coach them; parents in vulnerable circumstances | `mediaConsent`, `safeguarding`, `vulnerability` |
| Sports directory (athletes may be minors) | the same, plus the athlete's own health data (injuries) | + `sensitiveCategories: health` |
| Job portal | protected characteristics in job ads and matching (ADEA, EEOC, EU equal treatment); candidates' CVs as Article 9 sources; apprentices 16–18 | `protectedCharacteristics`, `sensitiveCategories`, `audienceModel: mixed` |
| Classifieds | sellers' home addresses and phone numbers; buyers' locations; vulnerable sellers (bereavement sales, debt) | `sensitiveCategories: location`, `vulnerability` |
| Housing or credit adjacent (any) | Fair Housing / ECOA ad-delivery rules | `protectedCharacteristics` with the market's specific rules |

## 5. What was not found

- No published enforcement yet under the EAA for marketing e-mail specifically; the
  obligation is clear, the case law is not.
- No US federal rule on filming children at private activities — the standard is the
  safeguarding bodies' guidance and COPPA's definition of personal information.
- The AI Act's Article 5 guidance from the Commission was read through summaries; the
  prohibition's wording is quoted from them.
