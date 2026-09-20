# Bízd ránk a zöldet — project documentation

**Bízd ránk a zöldet!** (bizdrankazoldet.hu, @bizdrankazoldet) is the playful office-plant brand
of Gourmet Garden Kft. / Grofie (Budapest): office plant design, rental and care for companies,
with maintenance as part of the service. The owner's brief: research how a silly-but-professional
green service should be presented in 2026 to earn trust, show reliability, own an identity and
sell through its customer journey; then prototype it. Built to the prototyping standard
(`PROTOTYPING.md`); this index is also the process log.

## The set

| Document | What it holds |
|---|---|
| `00-brief.md` | the client, what they sell, the brief, what will be built, what is real |
| `01-research.md` | the research: trust, reliability, identity, the customer journey, the green-claims rules, the competitors; proposals P1–P12 |
| `02-audit.md` | the site, the Instagram account, the parent brand and five competitors, measured |
| `03-sources.md` | what is real and what is sample |

Rendered by `build.py` (`python3 bizdrankazoldet/docs/build.py`); gate `python3 bizdrankazoldet/check.py`
(also run by the root `check.py`).

## Process log

**2026-09-20 — stages 0–2.** The owner named the project and the brief ("the full research on how
a silly but professional green project should be presented in 2026 to give trust, reliability
and a strong identity and a customer journey that sells"). The site was measured with `curl`
(WordPress + Elementor, 292 KB, 51 scripts, 10.5 s cold TTFB, no prices, no reviews, no
impresszum, no guarantee, no link to Instagram, ten of sixteen images without alt); the Instagram
account read behind its login wall (70 followers, three weeks old, four Reels, the brand's voice
already there); the parent brand found (Grofie — 100+ projects, 10+ years, 30+ maintenance
sites, 100 % evergreen guarantee, same phone) and five competitors measured (none publishes a
price, a review or a guarantee). The research read the evidence on B2B trust (rep-free buying,
thought leadership, named people, specificity), on the biophilic effect (honest ranges), on
humour in B2B (works when related to the product; needs rules), on character systems in 2026,
on Hungarian channels (Facebook 6.97 M, Instagram 2.74 M, LinkedIn for the decision) and on the
EU green-claims rules from 27 September 2026 — and wrote the journey step by step and twelve
proposals.

**Next.** The owner reads `01-research.md` and says "direction approved" (or corrects it); then
the design system (gate 1) from the badge, the teal, the voice.
