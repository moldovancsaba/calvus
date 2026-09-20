# business.direct — product definition

*For everyone who decides on, builds or sells business.direct. What this document holds: what the
product is, for whom, the three jobs it does, how it is operated, what it is not, the vocabulary
every other document uses, and the first customer as the example. It is the root document: the
presentation, the specification, the rules and the plan derive from it.*

## 1. What business.direct is

**business.direct is a standalone product for classified media owners** — the owners of listing
platforms, directories and marketplaces of local businesses — that runs the three jobs their
business never stops needing, every day, from their own data:

| Job | What the product does | Result for the owner |
|---|---|---|
| **Marketing** | reads the listings for what is new — offers, dates, news, photos, footage — and generates the content: posts for every social channel, a weekly digest and alerts for the visitors who opted in, search pages per category and area, clips cut from real footage; delivers each to its medium at the slot after the owner approves; answers comments with a drafted reply; reports what each piece brought | visitors come, and come back |
| **B2B sales** | scores every listed business and works it through a pipeline — identified → contacted → replied → applied → managing → upgraded — with a lawful three-touch sequence, a drafted answer to every reply, a call list for the phone-only, a visitor's enquiry turned into the strongest touch, and the site's placements offered once the product has delivered more than they cost | listings become managing, then paying, advertisers |
| **Retention** | watches every paying advertiser for the signals that precede a cancellation — a renewal due, a stale page, an unanswered enquiry, a listing that stopped surfacing — and drafts a touch from the advertiser's own numbers, never a discount; logs kept and lost | advertisers stay |

Around the three jobs: **the owner's economics as a service** — one screen that computes, on the
owner's own numbers, what a listing sells for, what an advertiser costs to win and is worth, what
a visitor costs to bring in and is worth, what churn costs and retention keeps, all costs and
incomes, the twelve-month plan, and where the next dollar goes; **a Monday recap** of what moved
and what needs a decision; and **a policy record and gate** per site that make the wrong default
impossible to ship.

## 2. How it is operated

- **Departments, not people.** Each job runs as departments that draft, schedule, watch and
  compute on their own. The owner's voice, rules and offers are plain-text files the departments
  read before every draft; edit a file and every department changes.
- **A human gate on everything.** It drafts, it cannot send, it stops and asks. Nothing reaches
  a visitor, an advertiser or a channel without an approval. A department that runs four clean
  weeks earns auto-approval for its routine messages — every one still logged and stoppable.
- **Two interfaces, one product.** *Simple* shows the owner only what needs a person, ranked,
  with the reason and one button, and one press for everything safe; *Advanced* shows every
  screen and input.
- **One loop.** Every touch, reply, post, save, enquiry, renewal and payment is an event; nightly
  the metrics; weekly four levers ranked by expected value per dollar; the owner approves; the
  product measures and adjusts its cadence, its content slots and the moment a placement is offered.
- **The advertiser's own team.** A business that manages its page gets, inside the owner's
  product, its own team: every enquiry answered within the hour from its own files, reminders,
  campaigns to the visitors who saved it, clips from one recording, results on one screen. That is
  why it claims, why it stays and why it upgrades.
- **Visitors never log in to the product.** Their preferences reach it by signed link; every
  channel is off until they turn it on; Stop is one tap; a child is an age, never a name.
- **One site is one instance.** Its policy record (jurisdictions and laws, audience model,
  consent per channel, cap, retention, disclosure), its connector, its sending domain and its
  placements. The second site is a record and a connector, not a rebuild.

## 3. Who it is for

The **classified media owner**: one person or a very small team who gathered the supply, built
the site the visitors use, and is now the whole sales and marketing department for both sides
of it — thousands of listings not yet sold to the businesses on them, visitors who save and hear
nothing, advertisers who leave for reasons visible weeks earlier. The pain and the product are
the same whether the listings are children's activities, sports clubs, jobs, homes or
second-hand goods.

## 4. What it is not

Not a directory or marketplace platform (the owner keeps their site; the product connects to
it). Not a tool sold to the listed businesses one at a time (they get their team inside the
owner's product). Not a generic marketing agent (every department knows what a listing, an
advertiser and a visitor are). Not an autopilot (nothing sends without a person). Not a
discounting engine (retention runs on results, never on price cuts).

## 5. The vocabulary

| Product term | Meaning | The first customer's word |
|---|---|---|
| **Media owner** | the classified media owner who runs the product; the operator is the person who approves | platform |
| **Listing** | a business's page on the site; the inventory the owner sells | card |
| **Advertiser** | a listed business — a prospect until it manages its page, a customer once it pays for a placement | provider |
| **Visitor** | a person using the site; an engaged visitor saves, opens the digest and enquires | family |
| **Placement** | what the owner sells to an advertiser — featured, category, discovery profile | reach product |
| **Instance** | one site with its own policy record, connector, sending domain and placements | Your Field NYC |
| **Department** | a bounded automation with its own approvals and an optional AI switch | — |
| **The human gate** | nothing leaves without an approval or an earned auto-approval | — |

The product shows each site its own words; the prototype, built on the first customer's data,
shows theirs.

## 6. The first customer, as the example

**ClassScout**, operator of **Your Field NYC** (getyourfield.com): a children's-activity
directory in New York — families on one side, activity providers on the other, a catalogue
gathered by a pipeline with thousands of listings still to publish, one founder as the
department. ClassScout is the example every document uses to make the persona concrete, and the
first buyer. Everything specific to their instance — their site measured, what in the prototype
is real and what is sample, their onboarding inputs, the pilot's SWOT — is in
`first-customer-classscout.md`. A second, unrelated directory has been pulled through the same
connector shape to prove that the second instance is a record and a connector.

business.direct is a sibling of DiscountDirect: DiscountDirect retains a web shop's customers;
business.direct sells, fills and keeps a classified media site.

## 7. What exists today

- **The prototype** (`../index.html`): one page, three roles, every screen of the specification,
  every approval moving state, the policy gate, the Economics screen, Simple and Advanced modes —
  on a demo sample of the first customer's public listings, with the activity generated from those
  listings and labelled sample. Nothing sends, publishes or connects; the sample says nothing
  about the size or state of the customer's business.
- **The specification** (`product-specification.md`): how it works and how the customer uses it,
  screen by screen and role by role.
- **The rules** (`business-logic.md`), **the architecture and blueprint** (`architecture.md`),
  **the delivery plan with the operating model and the sign-off sheet** (`delivery-plan.md`),
  **responsible data and the legal position** (`responsible-data.md`), **the market**
  (`market.md`), **the economics** (`economics.md`), **the evidence** (`evidence.md`).

## 8. The decision this document supports

Build business.direct as defined here and run it for the first customer. The sign-off sheet —
who accepts what, by which criterion — is in `delivery-plan.md`.
