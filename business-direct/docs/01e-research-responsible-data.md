# business.direct — research IV: responsible data, children's rights, and the business value of doing it properly

*Fourth research round, 2026-09-19, on the owner's directive: the first client is ClassScout
(the operator of Your Field NYC), but the system must serve any client; the machine must
respect children's rights "in general, whatever clients we work for"; and it must "care about
our customers' data and use it commercially but properly, and deliver benefits and business
value for the clients". This round reads the law by market, the enforcement record, the
design frameworks the regulators themselves publish, and the evidence that responsible data
practice pays. **P** = primary (regulator, statute, the company's own document, the study
itself), **A** = law-firm or trade summary. The framework that comes out of it is
`responsible-data.md`; the policy screen in the prototype is its
reference implementation.*

## 1. The law by market — what any client instance must encode

### 1.1 United States (first client)

- **COPPA, amended rule effective 23 June 2025, full compliance by 22 April 2026**: personal
  information now includes biometrics, government identifiers, phone numbers, audio and
  certain geolocation; separate verifiable parental consent for third-party disclosures;
  prescriptive security; new consent methods (text message, knowledge-based authentication).
  Applies to operators directed to children under 13 or with actual knowledge of a child
  user. **A** [Latham & Watkins](https://www.lw.com/en/insights/ftc-publishes-updates-to-coppa-rule),
  [Hunton](https://www.hunton.com/privacy-and-cybersecurity-law-blog/coppa-rule-amendment-compliance-deadline-approaches),
  [Davis Polk](https://www.davispolk.com/insights/client-update/ftc-prioritizes-coppa-enforcement-new-compliance-obligations-take-effect)
- **New York Child Data Protection Act, effective 20 June 2025**: processing of personal data
  of users under 18 only where strictly necessary or with informed consent (parental under
  13, the teen's own 13–17); covers services accessible in New York. **P** [NY Attorney General guidance](https://ag.ny.gov/child-data-protection-act-guidance)
- **California**: CCPA regulations treat data of known under-16s as sensitive, willful
  disregard of age counts as knowledge; the 2026 session added bans on "addictive features"
  for under-16s (algorithmic feeds, autoplay, push notifications designed to maximise
  engagement). **A** [Paul, Weiss Q1 2026](https://www.paulweiss.com/insights/client-memos/california-privacy-updates-q1-2026),
  [Kelley Drye](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/californias-2026-legislative-session-wraps-a-wave-of-privacy-and-ai-bills-reaches-the-governor-with-key-child-safety-and-ai-measures-signed-into-law)
- **Other states, 2025–2026**: Maryland, Minnesota, Colorado (October 2025), Oregon
  (1 January 2026: no sale or targeted advertising on known under-16 data), Nebraska's
  Age-Appropriate Online Design Code (1 July 2026: high-privacy defaults, no targeted ads
  to minors, restricted push-notification hours). **A** [Venable](https://www.venable.com/insights/publications/2025/11/states-shine-spotlight-on-child-and-teen-privacy),
  [Inside Privacy](https://www.insideprivacy.com/childrens-privacy/state-and-federal-developments-in-minors-privacy-in-2026/)
- **CAN-SPAM** (postal address, opt-out within 10 business days) and **TCPA** (written
  consent for marketing SMS; $500–1,500 per message) — research I §8.

### 1.2 European Union and the United Kingdom (the reference instance and any EU client)

- **GDPR Article 8**: a child's own consent to an information-society service is valid from
  16 (member states may lower to 13); below that, the holder of parental responsibility.
  **P** [Art. 8 GDPR](https://gdpr-info.eu/art-8-gdpr/)
- **DSA Article 28**: platforms accessible to minors must ensure a high level of privacy,
  safety and security for them and **may not show advertising based on profiling when they
  know with reasonable certainty the user is a minor**; in April 2026 the Commission's
  preliminary finding against Meta made self-declared age insufficient. **A** [HLC on the Art. 28 guidelines](https://www.hlc.com/en/publications/the-longawaited-eu-guidelines-on-article-281-dsa-what-online-platforms-must-know),
  [Xident on the Meta finding](https://xident.io/blog/dsa-article-28-minimum-age-enforcement-meta-breach-age-assurance-2026/)
- **UK Age Appropriate Design Code (the Children's Code)**: 15 standards — high-privacy
  defaults, data minimisation, no sharing of children's data by default, geolocation off by
  default, profiling off by default, no nudge techniques, privacy information a child can
  follow; since 5 February 2026 the "higher protection of children" is written into UK GDPR
  Article 25. **P** [ICO: the code](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/),
  [ICO design guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/designing-products-that-protect-privacy/childrens-code-design-guidance/);
  **A** [5Rights](https://5rightsfoundation.com/new-uk-data-law-what-does-it-mean-for-childrens-privacy/)
- **EU AI Act Article 50** (disclosure of AI content, live since 2 August 2026) — research II §4.3.
- **Hungary**: B2B e-mail to corporate addresses without consent; named-person addresses and
  B2C require consent (Act XLVIII of 2008) — research I §8b.

### 1.3 What is common to every market

Read together, the laws converge on eight rules any instance can encode: (1) know whether
the service is for adults, mixed, or child-directed; (2) collect the minimum about a child —
by default nothing, at most an age band; (3) never profile or target advertising on a
minor's data; (4) high-privacy defaults, nothing on by default that shares or locates;
(5) consent that names the channel and the sender, stored verbatim with time and source;
(6) an opt-out honoured in one business day and a physical address on every commercial
e-mail; (7) disclosure when AI wrote or made something; (8) retention with an end date.

## 2. The cost of getting it wrong (the enforcement record)

| Case | What | Cost |
|---|---|---|
| Epic Games (FTC, December 2022) | COPPA violations, default settings that exposed children, dark patterns in billing; internal employee warnings raised the penalty | **$275 M** civil penalty + $245 M refunds = $520 M **A** [Orrick](https://www.orrick.com/en/Insights/2023/02/6-Top-Takeaways-from-FTCs-Landmark-Epic-Games-Settlements), [WilmerHale](https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20221227-settlement-with-epic-games-highlights-continued-focus-by-regulators-on-unfair-privacy-practices-teens-and-user-interface-design) |
| YouTube / Google (FTC, 2019) | data collected from child-directed channels | $170 M **A** [Securiti](https://securiti.ai/blog/ftc-epic-games-settlement/) |
| Disney (FTC, court-approved late 2025) | videos not labelled "made for kids", no parental notice | $10 M **A** [Hunton](https://www.hunton.com/privacy-and-cybersecurity-law-blog/court-approves-disneys-10-million-ftc-settlement-resolving-coppa-enforcement-action) |
| Amazon Alexa, Microsoft Xbox (2023) | children's voice and account data | $25 M, $20 M **A** [Securiti](https://securiti.ai/blog/ftc-epic-games-settlement/) |
| Meta (EU Commission, April 2026, preliminary) | under-13s on Facebook and Instagram — self-declared age not enough | DSA breach finding **A** [Xident](https://xident.io/blog/dsa-article-28-minimum-age-enforcement-meta-breach-age-assurance-2026/) |

**Reading.** Every case is a marketing or engagement design decision, not a data breach: a
default, a label, a nudge, an unverified age. The lesson for a marketing machine is that the
rules must live in the product's defaults and gates, not in a policy document.

## 3. The frameworks the regulators and the best brands publish

- **Privacy by Design (Cavoukian, 2009; adopted by the data-protection commissioners 2010)**:
  proactive not reactive; privacy as the default; embedded in design; full functionality
  (not privacy *or* value); end-to-end security; visibility and transparency; respect for
  the user. **A** [Wikipedia summary](https://en.wikipedia.org/wiki/Privacy_by_design)
- **The ICO Children's Code's 15 standards** (§1.2) are the most concrete design checklist a
  regulator has published; UNICEF's 2025 review treats such codes as the model for other
  jurisdictions. **P** [UNICEF Innocenti case study](https://www.unicef.org/innocenti/media/11096/file/UNICEF-Innocenti-Childrens-Codes-Case-Study-2025.pdf);
  5Rights' **Child Rights by Design** principles (privacy is principle 7). **P** [5Rights](https://childrightsbydesign.5rightsfoundation.com/principles/7-privacy/)
- **ISO/IEC 27701** (a privacy information management system on top of ISO 27001) and the
  **NIST Privacy Framework** (2020; 1.1 in progress) — the two management frameworks a client
  may ask an operator to align with. **A** [IAPP comparison](https://iapp.org/resources/article/web-conference-iso-27701-vs-nist-privacy-framework-choosing-the-right-one-for-you/)
- **The LEGO Group's Responsible Marketing to Children policy** — the best-known brand
  standard: parental permission for under-13s, anonymous usernames, no real photos of
  children, privacy by design and by default named as principles; age-appropriate,
  safe-by-design experiences. **P** [LEGO policy (PDF)](https://education.theiet.org/media/6534/lego-mandatory-polices-responsible-marketing-to-children-policy.pdf),
  [LEGO: responsible engagement with children](https://www.lego.com/en-us/sustainability/children/responsible-enagement-with-children)

**Reading.** The machine's rules R15 (never generate a child), R24 (no child's name), R3
(the cap), R4 (consent per channel per provider), R20 (disclosure) are already these
standards. What is missing is the *instance-level* policy that says which of them apply
where, and a gate that will not run a feature until its policy fields are set.

## 4. The business value of doing it properly

- **Privacy investment returns**: 96 % of organisations say the returns from privacy
  investment outweigh the cost; 86 % say privacy law has a positive effect on their
  business; measurable value named: customer trust, faster sales cycles, reduced risk.
  **P** [Cisco 2025 Data Privacy Benchmark](https://www.cisco.com/c/dam/en_us/about/doing_business/trust-center/docs/cisco-privacy-benchmark-study-2025.pdf),
  [Cisco 2026 study](https://www.cisco.com/c/en/us/about/trust-center/data-privacy-benchmark-study.html)
- **Consumers switch over data practices**: 51 % of "privacy actives" have switched a
  company over its data practices; 49 % of 25–34-year-olds — the parents of young
  children. **P** [Cisco 2024 Consumer Privacy Survey](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2024/m10/how-safe-is-our-data-consumers-want-to-know.html)
- **Volunteered (zero-party) data outperforms inferred data**: campaigns that ask the
  customer what they want report conversion lifts of 31 % to several hundred per cent and
  average collection-campaign conversion around 61 %; 82 % of marketers now collect it.
  **A** [Demand Local statistics](https://www.demandlocal.com/blog/zero-party-data-collection-statistics/),
  [Salesforce](https://www.salesforce.com/marketing/personalization/zero-party-data/)
  *Our family preferences, saves and asks are zero-party data — the family tells the machine
  what to send. That is why the model needs no profiling.*
- **Referrals are the SMB's best channel** (83 %) and parents choose the programme that
  shows up in their world (80 %) — trust is the acquisition channel in this category.
  Research II §2.1, §3.

**Reading.** "Commercially but properly" is not a trade-off in this category: the family who
opts in, saves and asks converts better than any inferred audience, and the parent who
trusts the platform refers the next family. The responsible design *is* the growth design.

## 5. What it means for business.direct — the framework (built as `18-…` and the Policy screen)

1. **A policy per instance** (`platform_id`): jurisdictions, audience model, child-data rule,
   consent model per channel, marketing rules for minors, defaults, retention, AI
   disclosure, postal address, opt-out SLA, the published privacy policy's clauses.
2. **A policy gate**: a feature runs only when the policy fields it depends on are set —
   sequences need the postal address; the digest needs the published e-mail clause;
   campaigns need the audience opt-in; SMS needs the consent text; generation needs the
   disclosure rule.
3. **Client onboarding as a checklist** the policy screen shows: what is set, what is
   missing, what is blocked.
4. **The same for every client**: a job portal (candidates, apprenticeships at 16–18), a
   classifieds site (sellers' addresses, buyers' locations), a sports directory (players'
   ages) — the fields change values, not shape.
5. **The value statement to the client**: lower legal exposure (the enforcement record), a
   higher-converting audience (zero-party), a trusted brand in a category where parents
   switch over data practices, and a machine that can be audited (every send logged with its
   policy basis).

## 6. What was not found

- No published enforcement case yet under New York's Child Data Protection Act.
- The FTC's own amended-rule text was read through law-firm summaries (the Federal Register
  page is long); the dates are consistent across four sources.
- No public benchmark on the conversion effect of *responsible* marketing to parents
  specifically; the zero-party and trust figures are the nearest evidence.
- **Link check** (`curl`, 2026-09-19): four sources refuse scripted fetches (Cisco's two
  study pages, UNICEF's PDF, Demand Local) — each was read through the search tool and is
  kept; open them in a browser. Every other source resolved.
