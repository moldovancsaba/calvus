# Responsible data

*The policy record for gameformative, and the gate that holds a feature until its fields are set.
Written 2026-09-25. The prototype collects nothing: the newsletter form is disabled, sign-in is
inert, and the only thing stored is the reader's theme choice, on their own device. This record
applies from the first feature that stores or contacts people. Legal wording is the team's reading,
to be confirmed by counsel.*

## What the prototype stores

| Item | Where | Personal data | Purpose |
|---|---|---|---|
| Theme choice (`gf-theme`: light or dark) | the reader's browser `localStorage` | no | remember the reader's choice; never sent anywhere |

No cookies, no analytics, no advertising, no third-party scripts. The one third-party request is
the font (Google Fonts), which production removes by self-hosting (ADR-05).

## The policy record (to fill before the feature ships)

| Field | Value | Blocks |
|---|---|---|
| Jurisdictions and laws | EU/EEA (GDPR, ePrivacy, AI Act Art. 50), UK (UK GDPR, PECR), others per market (A6) | every feature below |
| Audience | general adult audience; the site is not directed at children | accounts, newsletter |
| Child-data rule | a child is an age, never a name; no profiling or targeting on a minor's data, with or without consent | accounts |
| Consent per channel | newsletter: double opt-in naming the sender and the channel; no pre-ticked boxes | newsletter (A5) |
| High-privacy defaults | analytics without personal data and without cross-site tracking; ads only with consent (ADR-06) | analytics, ads (A4) |
| Frequency cap | newsletter weekly ("The Monday brief"), nothing more without a new opt-in | newsletter |
| Opt-out | one-click unsubscribe in every mail, honoured immediately; postal address in every commercial mail | newsletter |
| AI disclosure | automated text labelled; AI-generated text labelled unless human-reviewed under named editorial responsibility; AI imagery always labelled | publishing |
| Retention | subscriber data until unsubscribe + 30 days; server logs 30 days | newsletter, hosting |
| Published policy | a privacy page and the automation policy (How we work) | launch |

**The gate:** no feature that stores or contacts a person goes live while its row above says
"to fill". The prototype's disabled newsletter form says so on the page ("nothing is collected;
consent and sender are set before launch").
