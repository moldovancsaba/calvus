# business.direct — executive summary for ClassScout

*One page for the decision-maker. What it supports: the decision to build. Every figure is
measured on the platform's public API, sourced in the research, or marked as an assumption to
be replaced by the platform's own numbers; the full case is `22-business-case.md`, the plan
`13-implementation-plan.md`. Written 2026-09-20 (D38).*

## The situation

Your Field NYC has gathered 253 children's-activity providers and built the tools families use
to save and plan. **None of the 253 manages its page**; the cards carry 0 reviews and 28 prices;
83 next sessions, 72 trial policies and 26 announcements sit on them unpublished; families who
save a provider are told nothing when something starts near them. The platform has the supply
and the demand and no team working either side.

## The complication

Small providers lose the enquiries the platform sends them — 62 % of calls to small businesses
go unanswered, and the customer buys from whoever answers first. Discovery is moving to social
and to AI answers that cite reviewed, structured sources — which a catalogue without reviews or
prices is not. The category's money ($1 016 per child per sport, up 46 % in five years) flows
past a platform whose providers are unmanaged. And the incumbents already sell the fix: Yelp
bought Hatch for $270 M and charges $99 a month for "answer, follow up, convert".

## The question

How does a platform with no sales team and no content team turn 253 listings into managed
pages, paying providers and families who come back — without breaking the law, a parent's
trust or its own privacy policy?

## The answer

**business.direct**: a marketing and sales machine the platform runs on its own data. Two
flows at the front door — real content that brings families to the listing page, and a lawful,
capped invitation sequence that brings providers to manage their page — and behind them the
provider's own one-person team (conversations answered within the hour, campaigns to the
families who saved it, clips from one recording, results on one screen) and the platform's
reach products offered once the machine has delivered more than they cost. One loop decides
where the next dollar goes; **a person approves everything**; every message says why it was
sent; a child is an age, never a name.

## The three numbers

1. **Today's honest finding: LTV : CAC 0.7.** Outbound e-mail alone, on 253 providers at $49,
   does not pay for itself. The machine pays as the platform's growth engine from day one
   (a new family for ≈ $4 against ≈ $6 of expected value; ≈ $610 k a year of provider revenue
   through the platform's introductions at 5 000 families), and as a profit centre at 1 000
   providers (LTV : CAC ≈ 2) or priced for the category (≈ 6).
2. **Seventeen weeks, two developers**, nine sprints with an acceptance test each; Meta's
   review submitted in the first week.
3. **≈ $50–75 a month to run at pilot**, ≈ $280–400 at 1 000 providers — every vendor's price
   read on the day; covered by two upgraded providers at pilot.

## What is different

Responsible by design for every client — one policy record and a gate in the code, no
profiling of minors, no dark patterns, disclosure when a machine made something; two
interfaces — Simple shows what needs you with one button, Advanced shows everything; honest
data — 253 real providers, every figure labelled real, sample or assumption, an audit that
found and fixed its own contradictions.

## The decision

Go ahead. Nothing is needed from ClassScout before it; what the build needs after it — the
postal address, one privacy-policy paragraph, the policy record confirmed, counsel's wording,
later the platform's events and a pilot provider — is a checklist with owners and dates
(`19-implementation-prerequisites.md`). The first measured numbers replace the assumptions at
the end of sprint 2.
