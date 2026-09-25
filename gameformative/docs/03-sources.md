# Inputs and gaps

*Every input the prototype was built from, what it contributed, and every gap between the ask and
what the inputs can support. Written 2026-09-25. The research sources are listed separately in
`01a-source-register.md`; this page covers what went into the build.*

## Inputs

| # | Input | What it contributed |
|---|---|---|
| 1 | The owner's message of 2026-09-25 (quoted in `00-brief.md`) | the product, the scope of the research, the sites to study |
| 2 | The owner's follow-up: list every source with what we learned | `01a-source-register.md` |
| 3 | The Népszabadság prototype (`../../nepszabadsag/`) | the generator pattern, prototype banner, gate and documentation structure |
| 4 | openfootball `football.json` — `2026-27/{en,es,de,it,fr}.1.json`, `2025-26/en.1.json`, `2025-26/en.1-full.json` | every league result, table and derived figure; 2025/26 scorers, minutes, attendances. CC0 1.0 |
| 5 | openfootball `worldcup.json` — `2026/worldcup.json`, `2026/worldcup-full.json` | all 104 World Cup matches, scorers, line-ups, substitutions, attendance. CC0 1.0 |
| 6 | The research of 2026-09-25 (`01-research.md`) | the palette, type, layout, navigation, table, chart, trust and automation decisions |

The raw files are committed in `data/raw/`; `data/fetch.py` re-downloads them and
`data/convert.py` turns them into `data/stats.json`. The SHA-256 prefix of every input is written
into `stats.json` and listed on the How we count page.

## Gaps

1. **No licensed event data.** The open source carries results, goals, line-ups, substitutions and
   attendances — not shots, possession, xG, passes or player ratings, which fans of a stats site
   expect (`01-research.md` §3.3). Those panels are shown in place, marked not available, and never
   estimated. Filling them needs a data licence (`08-client-asks.md` A1).
2. **No live data.** Results are recorded by hand upstream and arrive after the match; the
   prototype shows final results to 20 September 2026 and the next fixtures as published. The live
   match centre is specified (`12-technical-design.md` §5), not built.
3. **No newsroom.** There are no journalists, so the byline is "gameformative data desk" and the
   copy is sample. Inventing named reporters would put fictional people on a news site; we did not.
4. **Official tie-breakers not applied.** Tables are ordered by points, goal difference, goals
   scored, then name. LaLiga and Serie A use head-to-head first; FIFA's group rules add more steps.
   For teams level on points an official table can differ. Said on every table and on How we count.
5. **Names as the source spells them.** The "-full" files set many names in capitals without
   accents ("MBAPPE"). The converter sets all-caps words in title case; accents the source dropped
   are not restored (Kylian Mbappe, Joao Pedro), because restoring them would mean hand-editing data.
6. **Team short names and codes are ours.** No open standard exists for club abbreviations;
   `data/teams.py` is the reviewed table (every source name must be in it, or the build stops).
   National teams use FIFA trigrams.
7. **One sport, men's competitions.** Women's football, cricket (India's first sport), NBA and CBA
   (China) are proposed expansions (`01-research.md` P12). No open, commercially usable data for
   them was verified: StatsBomb and NBA.com terms forbid it (register O3, O4).
8. **No photography.** No licensed photo source, and AI imagery is ruled out. The prototype uses
   data graphics generated from the numbers as its covers — a deliberate identity choice (D9) —
   and a photo agency licence is an ask for the real build.
9. **The data's own record is taken as given.** Where the dataset records the 2026 World Cup final
   or a 2026/27 score, the prototype shows it as the source records it; it was not independently
   verified against a second source. Two files for the same competition are cross-checked match by
   match by the converter.
10. **Blocked research sites.** Nine sites refused automated fetches (`01-research.md` §0); their
    designs are not part of the benchmark.
