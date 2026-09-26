# gameformative.com — FIND pass: DATA + DRIVE desks
Prepared 2026-09-26. All sources below were accessed 2026-09-25/26.

## How to read the source labels
- **OPENED (full)**: I read the full text or full page.
- **OPENED (abstract)**: I read the official abstract or record, but not the full text. The reason is given.
- **OPENED (rendered)**: I read the page through a fetch-and-summarise tool, not the raw HTML. The figures are reliable, but check the exact wording before quoting it.
- **BLOCKED**: 403, paywall, CAPTCHA or JS/bot challenge. I did not attempt any bypass.
- **SNIPPET ONLY**: seen only in a search-result snippet. Not opened, and not usable as a seed or as a fact.

Existing site football pieces (PL form, big-five goals per game, WC 2026 review, goals by minute) are not duplicated. The only football candidate below (D-DRIVE-3) is about leadership decisions, not scoring or form.

---

# DATA desk — "Analytics: models, tracking, measurement, decision support"

## DATA-1 · Baseball — "Two Seconds to Overrule the Umpire: What Baseball's First Robot-Zone Season Taught Us"
**Reader promise:** You'll understand what baseball's new ball-strike challenge data really measures, why catchers win more challenges than hitters, and why "54% overturned" does not mean umpires are wrong half the time.

**Seed source: OPENED (full)**
- *ABS Challenge Dashboard*, Baseball Savant (MLB / Statcast). Live 2026 regular-season page, accessed 2026-09-26. The page states no data cut-off date. https://baseballsavant.mlb.com/abs
- Figures read:
  - Overall: **54% overturns**, with **5,598 overturned / 4,771 confirmed / 10,369 attempts**.
  - Batters: **49%** (2,295 overturned of 4,687 attempts).
  - "Fielders" (pitchers and catchers): **58%** (3,303 of 5,682).
- Rules as stated on the page:
  - Only batters and pitchers/catchers may challenge. Each team starts with **two challenges** and loses the ability after two incorrect ones. Each team gets one challenge per extra inning.
  - No challenges are allowed when a position player is pitching.
  - The ABS zone is **17 inches wide**. Its **top is 53.5%** and its **bottom 27%** of the player's measured height without cleats. It is measured as the ball passes **the middle of the plate**.
- Companion page, OPENED (rendered): *ABS Metrics Documentation* (https://baseballsavant.mlb.com/abs-metrics-documentation).
  - A "challenge opportunity" is roughly **50% of pitches** in 2026.
  - A "reasonable pitch" to challenge is roughly **5%**. The page uses RE288 run expectancy to define a break-even confidence level.
  - Recheck wording before quoting.

**Supporting sources (would be "sources used")**
1. **OPENED (full).** Travis Sawchik, *"ABS Challenge System results, what we have learned"*, MLB.com, published 2026-04-03. https://www.mlb.com/news/abs-challenge-system-results-what-we-have-learned
   - A full count carries a **.730** swing in run expectancy. A first-pitch ball/strike is worth "a mere **.07**".
   - Through week one, 2-2 counts drew the most challenges (**27**).
   - **54%** of challenges came in the 6th inning or later, which covers **44%** of game time.
   - In MLB's 288-game ABS test (2025 spring), challenge success was **pitchers 41%, hitters 50%, catchers 56%**.
   - In Minor League play, **1.6%** of first pitches were challenged, against **8%** of full-count calls.
2. **OPENED (rendered).** Bradford Doolittle, *"MLB 2026: What we've learned so far about ABS"*, ESPN, 2026-05-19. https://www.espn.com/mlb/story/_/id/48807610/mlb-2026-abs-automated-balls-strikes-system-early-numbers-lessons-analytics
   - The top-30 pitch framers averaged **0.704** framing runs per 100 innings in 2025, against **0.565** so far in 2026 ("nearly a 20% drop").
   - The in-zone pitch rate of **47.3%** is the lowest since 2008 tracking began.
   - A raw curl returned an empty body, so recheck the exact wording.
3. **OPENED (abstract; PREPRINT, not peer-reviewed).** M. Shinya & M. Tomomura, *"Bayesian sensory integration explains ball-count bias in Major League Baseball umpires"*, Research Square, posted 2026-06-10. DOI 10.21203/rs.3.rs-9598750/v1
   - Uses **450,460** called pitches from 2015–2024 and **88** umpires.
   - A count-based Bayesian prior model predicts the shifts in the effective zone boundary: high R² = **0.940**, outer 0.690, inner 0.515.
   - Umpires with more perceptual uncertainty lean more on count priors (r = 0.235, p = 0.029).

**Investigated, not used**
- ESPN *"2026 MLB ABS challenge system tracker"* (updated through 2026-09-24, OPENED rendered). It ranks individual umpires by overturn rate on samples as small as **9 challenges**. That invites unfair judgements of named officials, so I use aggregates only.
- Baseball-Reference *"2026 MLB ABS Challenge Analysis"*: **BLOCKED** (HTTP 403).
- TSN, "54 per cent overturn rate after opening weekend" (175 challenges): **SNIPPET ONLY**, and superseded by full-season data.
- MLB.com, "There's loads of ABS data from last season" (2025): **SNIPPET ONLY**, older, and pre-MLB (spring/minors).

**Segment outline**
1. **Tap the helmet** — the two-second window and the two-challenge budget.
2. **What the robot zone actually is** — 17 in wide, 27%–53.5% of height, judged at mid-plate.
3. **The season scoreboard** — 10,369 challenges, 54% overturned. Catchers and pitchers are at 58%, hitters at 49%.
4. **Why the catcher wins** — vantage point and volume. The 2025 test split was 56/50/41.
5. **Spend your challenge wisely** — count leverage (.730 vs .07), late innings, keep one in reserve.
6. **What "overturned" does NOT mean** — selection bias: only doubtful pitches get challenged. Umpire count bias is explained by the Bayesian preprint.
7. **Ripple effects** — framing value down about 20% and zone rate at a record low. These are associations, not proven effects.

**Risks and must-nots**
- The overturn rate is **not** the umpire error rate. It covers only pitches players chose to challenge.
- The dashboard is live, so state "as of 26 Sept 2026".
- "Fielders" combines pitchers and catchers. The dashboard does not split them.
- Do not attribute the 2026 walk-rate or zone-rate changes solely to ABS. ESPN reports the numbers but not the cause.
- The preprint is not peer-reviewed and must be labelled that way.
- Do not name or rank individual umpires.
- I saw no source quantifying Hawk-Eye's own measurement error, so do not claim the robot zone is "perfect".

---

## DATA-2 · Rugby union — "Three Points or the Corner? The Maths Behind Rugby's Biggest Penalty Decision"
**Reader promise:** You'll learn how an "expected points" map turns rugby's kick-or-lineout dilemma into a decision you can read off the pitch, and why even Test captains' "wrong" calls cost surprisingly little.

**Seed source: OPENED (abstract of record + full author preprint); publisher full text BLOCKED**
- K. Watts & J. Pipping-Gamón, *"Kicking for goal or touch? An expected points framework for penalty decisions in rugby union"*, *Journal of Quantitative Analysis in Sports*, published **2026-09-02**, CC BY 4.0. DOI 10.1515/jqas-2025-0183
- How I read it:
  - I read the official abstract via Crossref.
  - The De Gruyter HTML returned an AWS WAF JavaScript challenge, which I did not bypass.
  - I read the full text of the author preprint, **arXiv 2512.00312v2 (26 Jan 2026)**, "submitted to JQAS": https://arxiv.org/abs/2512.00312v2. The writer should check figures against the version of record.
- Findings (preprint):
  - The data are **35,199 phases / 132 matches** from the 2018/19 Premiership, plus **3,802** international penalty kicks on a 5 m grid. The model uses **2,046** lineout observations.
  - Lineout expected points fall **0.0586** per metre from the try line (intercept 3.2545).
  - Card advantage adds **+0.88**. The team-strength term is **+0.65** (p = 0.058).
  - A missed kick's continuation value is modelled with a 22 m drop-out assumption. The average restart value is **0.76** points.
  - **Case study.** A South Africa penalty in the 22nd minute, 15 m from touch and 30 m out: the lineout becomes preferable once the kick gains more than **~16 m**. Assuming a 20 m gain, the lineout is worth **2.67** points against **2.42** for the kick, a gap of ΔEP 0.25.
  - Across that NZ–SA match, the model-optimal choice was made **46%** of the time, with a total "regret" of **1.39 points**. The game ended **24–17** to NZ.
  - A yellow card against the attacking team favours kicking. An opposition yellow favours the lineout.

**Supporting sources**
1. **OPENED (abstract via Crossref).** G. Martinez-Arastey et al., *"Foundations of expected points in rugby union: A methodological approach"*, *Journal of Sports Analytics*, online 2025-07-31, CC BY. DOI 10.1177/22150218251365220
   - Uses the **same** 132-match / 35,199-phase dataset.
   - The best model predicting scoring outcomes reached **39.7%** accuracy, below a **44.3%** usability baseline.
   - Use this as the humility counterweight. It is older than the seed window, but it is supporting, not seed.
2. **OPENED (arXiv abstract).** R. Brill, R. Yurko, A. Wyner, *"Analytics, have some humility: a statistical view of fourth-down decision making"*, *The American Statistician* (published 2025-04-22; arXiv 2311.03490). They find uncertainty in the optimal fourth-down call "far greater than that currently expressed by sports analysts". This is the cross-sport parallel.
3. **OPENED (rendered).** rugby.com.au match report, *"All Blacks edge Springboks in tense Eden Park battle"*: NZ 24–17 SA at Eden Park, dated **6 Sept 2025**. I used it only to fact-check the case-study match.

**Investigated, not used**
- RugbyReferee.net, *"Laws updated from 1 July"* (2026-07-03, OPENED rendered). It is a secondary referee blog.
  - It says 60-second conversions remain global law trials for another year.
  - It also says some in-goal restarts moved from 22 m drop-outs to try-line drop-outs. That could affect the paper's missed-kick assumption.
  - Confirm with World Rugby's own law text before mentioning it.
- C. Claassen, *"Dynamic team attack and defense strength in international rugby union"*, JQAS 2026-09-25 (OPENED abstract). It is sound but tangential: team ratings, not penalty choices.
- World Rugby law-trial ball-in-play claims ("33 minutes per match"): **SNIPPET ONLY**.

**Segment outline**
1. **The captain's 20-second dilemma** — posts or corner.
2. **Expected points, minus the jargon** — the average points a situation usually leads to.
3. **Two maps of the pitch** — lineout value by metre, and kick success by distance and angle. A miss isn't worth zero.
4. **Where the line falls** — the 16 m tipping point and the 2.67 v 2.42 example.
5. **Cards and class move the line** — yellow cards and team strength.
6. **Did the Test sides get it right?** — 46% "optimal", but only 1.39 points of regret. Most calls sit near the boundary.
7. **Read the small print** — one club season, mixed club and international data, EP versus win probability.

**Risks and must-nots**
- The model rests on **one 2018/19 club season** plus international kick data, and laws have changed since.
- The authors flag selection bias: strong teams generate more advanced lineouts.
- The model maximises points, not win probability. Near-boundary calls are not "mistakes".
- **Discrepancy:** the preprint dates the NZ–SA case-study match "September 16th, 2025", but the rugby.com.au report dates NZ 24–17 SA at Eden Park to 6 Sept 2025. Use the verified date and check the version of record.
- Do not criticise named kickers or captains.

---

## DATA-3 · Multi-sport — "Can a Machine Call the Result? What 118 Studies Say About AI Sports Prediction"
**Reader promise:** A plain-English guide to what AI prediction models in sport can and can't do, and a five-question checklist for the next "AI predicted the winner" headline.

**Seed source: OPENED (full, open access)**
- A. Gregori, I. Reyes-Pedroza, A.Y. Barrera-Animas, J. Noguez, D. Escobar-Castillejos, *"Forecasting sports outcomes through machine learning"* (systematic review), *Frontiers in Computer Science* 8:1883327, published **2026-09-18**. DOI 10.3389/fcomp.2026.1883327. https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2026.1883327/full
- What the review covers: **118** English-language journal articles published 2020–2025.
- Prediction tasks:
  - Match outcome: **50 (42%)**
  - Player performance: **34 (29%)**
  - Injury: **25 (21%)**
  - In-game events: **9 (8%)**
- Sports:
  - Soccer: **28 (24%)**
  - Basketball: **21 (18%)**
  - Cricket: **14 (12%)**
  - Esports: **10 (8%)**
  - Tennis: 7 (6%)
  - Baseball: 2
  - Rugby: 1
- Verified quotes:
  - External validation "was reported far less often than internal validation".
  - Performance "appeared to depend less on algorithmic novelty alone than on data scale, signal complexity, validation design, and task definition".
  - The authors recommend "rolling-origin validation for temporal data" and "models that report uncertainty alongside a point prediction".
  - They name likely "publication bias toward studies reporting favorable accuracy".
  - The review did **not** pool accuracy figures.

**Supporting sources**
1. **OPENED (abstract via Crossref).** H. Choi, *"Event-specific versus stable predictors of medal outcomes…Asian Games and Olympic Games"*, *J. Sports Analytics*, online 2026-08-26. DOI 10.1177/22150218261483305
   - Covers **1,011** athletes at Hangzhou and Paris.
   - Gradient-boosting models showed "substantial transfer declines" across events.
   - Simple L2-logistic regression transferred partially, matching or beating them for bronze and overall medals.
   - This is the ideal "when the season changes" example.
2. **OPENED (abstract via Crossref).** C. Claassen, *"Dynamic team attack and defense strength in international rugby union"*, JQAS, 2026-09-25. DOI 10.1515/jqas-2026-0073. The Bayesian models, tested **out-of-sample on 2025**, outperformed the official World Rugby rankings algorithm. This shows validation done right.
3. **OPENED (abstract via Crossref).** L. Szczecinski, *"New insights into elo algorithm for practitioners and statisticians"*, *J. Sports Analytics*, 2026-07-15. DOI 10.1177/22150218261467512. Convergence analysis suggests FIFA men's national-team ratings "had not converged for the vast majority of teams".

**Investigated, not used**
- A sports-analytics market report ("$3.05bn in 2025 → $9.64bn in 2030"): **SNIPPET ONLY**. It is commercial market-sizing, unverifiable and off-topic.
- Medium post, "How AI & Sports Analytics Are Transforming Every Sport in 2026": **SNIPPET ONLY**. Not a credible source.
- Martinez-Arastey et al. 2025 (rugby EP accuracy 39.7%): relevant, but it duplicates DATA-2's use, so keep it there.

**Segment outline**
1. **"The AI picked the winner"** — why these headlines multiply.
2. **What researchers actually try to predict** — the four task types, and which sports dominate. Baseball: 2 studies. Rugby: 1.
3. **The toolbox** — random forests and boosting. Data beats algorithm novelty.
4. **The blind spot: testing on the future** — external validation is rare, and publication bias is likely.
5. **When the context shifts** — the Olympics/Asian Games transfer drop versus the rugby out-of-sample win.
6. **Your five-question checklist** — out-of-sample? baseline? calibrated? uncertainty shown? new season or league?

**Risks and must-nots**
- Never state an "AI accuracy %" for sport. The review deliberately gives none.
- The scope is English-language journal papers from 2020–2025, and there was no risk-of-bias scoring.
- Don't imply ML "doesn't work". The point is that the claims are often under-tested.
- The medal study covers two events and one athlete sample, so avoid generalising it.

---

# DRIVE desk — "What moves results: incentives, culture, leadership, audience levers"

## DRIVE-1 · Basketball (WNBA) — "Is Home Court Disappearing? What Jet Lag and Charter Flights Did to the WNBA"
**Reader promise:** You'll learn how much home advantage the WNBA has lost since 2009, why travelling east seems to hurt more than travelling west, and what that means for a bigger, more spread-out league.

**Seed source: OPENED (full, open access via Europe PMC PMC13350567)**
- J. Leota, D.J. Miller, M.É. Czeisler, J. Cook, L. Mascaro, T.D. Smithies, A. Nelthropp, E.R. Facer-Childs, *"Home-Court Advantage and the Associations of Travel and Jet Lag with Team Performance in the WNBA"*, *Sports Medicine – Open* 12, published **2026-07-09**. DOI 10.1186/s40798-026-01067-0
- Data and method: **3,489** regular-season games over 18 seasons (2007–2024), analysed with mixed models.
- Home-court trend:
  - Home advantage declined: β = −0.67, p = .002.
  - It fell from **64.3% (2009) to 52.3% (2024)**.
  - Full text: from 2021 to 2024 it "averaged **53.0%**".
- Travel and jet lag:
  - More travel distance in the prior 7 days was associated with worse **away** performance (β = −0.04, p = .020). This was driven by **points conceded** (β = 0.04, p = .018).
  - **Eastward** jet lag was associated with worse **home**-team performance (β = −0.15, **p = .049**).
  - There were no associations for westward jet lag or for away teams (all p ≥ .399).
- Context from the full text:
  - Upgraded travel under the 2020 CBA, and full-time charters for all teams from **2024**.
  - In a 2023 survey, most players named travel the league's biggest issue.
  - The 2020 "Wubble" season was excluded from the travel analysis.
  - Odd/even-year swings are possibly linked to Olympic and FIBA years.
- Limitations stated: team-level jet-lag estimates with a uniform 1 h/day resync, itineraries not public, and points-based outcomes only.

**Supporting sources**
1. **OPENED (rendered).** WNBA.com, *"Portland Fire, Toronto Tempo Select 22 Players in WNBA Expansion Draft 2026"*, 2026-04-03. https://www.wnba.com/news/wnba-expansion-draft-2026-results
   - The two teams picked from players "determined by each of the other 13 WNBA franchises". That makes 15 teams, by arithmetic.
   - Toronto opened on May 8 at home to the Mystics, and Portland on May 9 at home to the Sky.
2. **OPENED (abstract via Crossref).** P. Smith et al., *"Preliminary evidence of a circadian rhythm effect on English Premier League match outcome"*, *J. Sports Analytics*, 2026-09-08. DOI 10.1177/22150218261470130
   - Across kick-off times from 12:00 to 20:15, predicted home win probability rose **1.8%** and away win probability fell **3.2%**.
   - This is a cross-sport body-clock parallel. The authors call it "preliminary".

**Investigated, not used**
- Marquina Nieto et al., *"The women's side of home advantage: … top seven handball leagues"*, *Front. Sports Act. Living*, 2026-04-24 (OPENED abstract). It confirms home advantage across 4,744 women's handball matches. The abstract gives no headline percentage, and short domestic European trips don't test time zones, so it adds little.
- Jaguszewski et al. (Jan 2026), home advantage and crowds in the big-four football leagues: **SNIPPET ONLY**. Football-centred.
- APA PsycNet record on home advantage and crowding in women's leagues (2025): **SNIPPET ONLY**. Older.

**Segment outline**
1. **The shrinking edge** — from 64.3% to 52.3%.
2. **How you measure a jet-lagged team** — 3,489 games, 7-day mileage, direction of travel.
3. **Miles cost the visitors on defence** — more points conceded.
4. **The eastward puzzle** — home teams back from an eastward trip perform worse. Why direction matters for body clocks.
5. **Charters, contracts and a flatter league** — travel upgrades coincide with the decline. This is an association, not proof.
6. **A bigger map in 2026** — Portland and Toronto join, and schedules get busier.
7. **What the numbers can't see** — individual sleep, menstrual-cycle and circadian data, and points-only outcomes.

**Risks and must-nots**
- Say "coincided with", never "charter flights caused the decline".
- The eastward result is borderline (p = .049). Present it as suggestive.
- The paper says 2021–24 home advantage was "only one-third of what it was from 2007 to 2019". That phrasing is ambiguous (it likely means the margin above 50%), so do not repeat it without clarification.
- The data end in 2024. Make no claims about the 2025 or 2026 seasons.
- Name no players.

---

## DRIVE-2 · American football (NFL) — "Five Yards That Rewired a Play: How the NFL Used Incentives to Bring Back the Kickoff"
**Reader promise:** A case study in incentive design: how moving one touchback spot changed what 32 teams chose to do, what it cost, and how the league keeps closing loopholes.

**Seed source: OPENED (full)**
- NFL Player Health & Safety, *"2025 Season Key Takeaways"*, NFL.com, published **2026-02-02** (data shared 2026-01-30). https://www.nfl.com/playerhealthandsafety/health-and-wellness/injury-data/2025-season-key-takeaways
- Verbatim: "Concussions on the kickoffs increased year-over-year (from **8 to 35**) due to the higher number of plays – but the rate remains below the old kickoff format, as the kickoff return rate **more than doubled** in the second season under the Dynamic Kickoff, resulting in **1,157 more returned kickoffs**. There was also a **35% decrease** in the lower-extremity injury rate on the play compared to the prior format."
- Also on the page: "Injury rates remained stable in 2025".

**Supporting sources**
1. **OPENED (full).** Daire Carragher, *"NFL kickoffs are evolving as returns surged in 2025"*, PFF, 2026-03-03. https://www.pff.com/news/nfl-kickoffs-are-evolving-as-returns-surged-in-2025
   - Kickoff return rate: **22.9% (2023), 34.7% (2024), 75.9% (2025)**.
   - Hang time on kicks landing between the 10 and the goal line fell from **3.98 s (2023) to 3.48 s** as low "dirty" kicks spread.
   - Double teams on returns rose from **42.8% to 56.4%**.
   - There was a **33% rise** in 40+ yard returns.
2. **OPENED (full, primary).** *2026 Official Playing Rules of the NFL* (PDF). https://media.nfl.com/content/dam/communications/Official%20Playing%20Rules/2026%20Official%20Playing%20Rules.pdf
   - 2026 changes: 6-1-3 (setup-zone alignment), 6-1-5 and 6-1-6.
   - Rule text: "if the kickoff is from the 50-yard line and the play results in a touchback, then the dead ball spot is the **20-yard line**".
   - Onside rule text: "**At any time during the game**, the kicking team may declare an onside kick".
   - A touchback is the 35 or the 20 depending on whether the ball first touched the landing zone.
3. **OPENED (rendered).** Josh Alper, *"2026 season has seen the most kickoff return yards ever through two weeks"*, ProFootballTalk/NBC Sports, 2026-09-23. It reports **256 returns for 6,773 yards** through two weeks, attributed to NFL EVP Troy Vincent.

**Investigated, not used**
- AP via NFL.com, *"NFL sees surge in returns with new dynamic kickoff; onside kicks remain concern"* (Oct 2025, OPENED rendered). It gives 79.3% returns through Week 7 and under 5% onside recovery. It is older and mid-season, superseded by the full-season data.
- Mike Florio, PFT, *"The latest tweak to the kickoff has dramatically increased the concussion rate"* (2025-11-14, OPENED rendered). It gives **1.48 v 0.29** concussions per 100 kickoffs over the first 7 weeks. The data are second-hand (via The Athletic), partial-season and older. Mention only as the contested counterpoint, if at all.
- Buccaneers.com, *"Kickoffs Tweaked Again…"* (2026-03-31, OPENED). It says an out-of-bounds kick from the 50 "would come out to the 40", which conflicts with Rams.com and the rulebook's touchback-at-20 wording. Rams.com (2026-03-31, OPENED) is accurate but duplicates the rulebook; its Rich McKay quote is usable if needed.
- A search-engine summary claimed onside kicks still require the team to be trailing in 2026. The 2026 rulebook contradicts this, so the rulebook wins.

**Segment outline**
1. **The play the NFL nearly killed** — returns at 22.9% in 2023.
2. **The five-yard nudge** — the touchback moved to the 35 for 2025.
3. **Behaviour flips** — 34.7% to 75.9%, and 1,157 more returns.
4. **Everyone adapts** — knuckling "dirty" kicks, shorter hang time, double-team blocking.
5. **The price tag** — concussions 8 to 35 on more plays, and the NFL's rate claim. Lower-extremity injuries down 35%.
6. **Patching the loopholes** — the 2026 rules: touchback from the 50 goes to the 20, and onside kicks can be declared any time.
7. **The lesson for any rule-maker** — incentives work fast, and side effects follow.

**Risks and must-nots**
- The NFL page asserts the per-play concussion rate is "below the old kickoff format" but publishes no rate. Do not compute or invent one, and attribute the claim to the NFL.
- Health framing must stay factual. Name no injured players.
- Two weeks of 2026 data are a tiny sample.
- Quote rule wording from the 2026 rulebook, not from club sites (Bucs vs Rams conflict).
- Distinguish PFF's 75.9% from mid-season figures (79.3%).

---

## DRIVE-3 · Football (leadership angle) — "The Sacking Illusion: Why Firing the Coach Rarely Fixes the Team"
**Reader promise:** Why the "new-manager bounce" is mostly a statistical mirage, what expected points reveal about whether a team is really in decline, and why coaches still matter even though sacking them doesn't help.

**Seed source: OPENED (abstract only); full text BLOCKED (paywall/403)**
- E. Lundkvist, S. Holmström, A. Pérez-Ferreirós, A. Kalén, *"The sacking illusion: A counterfactual analysis of mid-season coaching changes using points and expected points in European football"*, *Journal of Sports Sciences*, online **2026-07-09**. DOI 10.1080/02640414.2026.2698238, PMID 42421473.
- How I read it:
  - Abstract read via the Europe PMC API.
  - tandfonline returned 403.
  - PubMed showed a reCAPTCHA, which I did not bypass.
- Abstract figures:
  - **331** mid-season changes in the top two men's divisions of the five highest-ranked European countries, 2017/18–2021/22.
  - Treated teams were matched to controls with **identical five-match trajectories**.
  - Before the dismissal, points per match fell from **1.28 to 0.34**, while expected points stayed **1.26–1.38**.
  - Effect on points afterwards: ATT **−0.18 to +0.13**.
  - Effect on expected points: ATT **−0.06 to +0.05**.
  - All confidence intervals include zero.
  - Quote: "clubs react to outcome variance rather than genuine decline".
- **The writer must obtain the full text before adding anything beyond the abstract.**

**Supporting sources**
1. **OPENED (full summary).** A. Heuer et al., *"Usefulness of Dismissing and Changing the Coach in Professional Soccer"*, PLOS ONE, 2011-03-22. It covers 46 Bundesliga seasons and 154 in-season dismissals. Dismissal has "basically no effect", and the apparent bounce is regression to the mean. It is older but classic corroboration.
2. **OPENED (abstract via Crossref).** D.M. Kahan, *"mWAR: A Bayesian estimator of manager value"*, *J. Sports Analytics*, 2026-05-19. It studies 500+ MLB managers since 1901. A substantial fraction shifted win% by **≥ ±0.012 (≈ ±2 wins per 162 games)**. Managers can matter even if sacking doesn't help.
3. **OPENED (abstract via Crossref).** F. Angelini et al., *"Strategic play and home advantage: coaches' tactical impact in Serie A"*, JQAS, 2026-07-29 (Serie A 2011/12–2013/14). Coaching decisions are "systematically associated with match performance conditional on pre-match strength and market expectations".

**Investigated, not used**
- PubMed record 42421473: **BLOCKED** (reCAPTCHA).
- tandfonline full text: **BLOCKED** (403).
- "The performance effects of wise and unwise managerial dismissals" (ResearchGate): **SNIPPET ONLY**. Older and not opened.

**Segment outline**
1. **The Monday-morning sacking** — the ritual, and why boards feel they must act.
2. **The bounce that isn't** — regression to the mean in plain words.
3. **Building a fair test** — 331 changes, each matched with a "twin" team that kept its coach.
4. **Results collapsed, performance didn't** — 1.28 to 0.34 points against steady expected points.
5. **After the axe** — no detectable improvement.
6. **So do coaches matter?** — MLB manager value of about ±2 wins, and Serie A tactics. Firing is not the same as coaching.
7. **A better boardroom dashboard** — expected-points trajectories before the trigger is pulled.

**Risks and must-nots**
- Abstract-only reading means any method detail beyond it (COVID-affected seasons 2019/20–2020/21 are inside the window) must be checked in the full text.
- "No detectable effect" is not the same as "zero effect".
- These are averages, so individual cases differ.
- Name no coaches or clubs as "bad sackings".
- Keep it distinct from the site's four football scoring and form pieces. This one is about leadership decisions.

---

# Reserves (verified seeds, not fully developed)
- **Snooker (DRIVE or DATA).** X. Chen, *"The evolution of maximum breaks in professional snooker"*, JQAS 2026-09-02, CC BY (OPENED abstract via Crossref; publisher page behind a JS challenge).
  - **217** 147s over 44 seasons. The 147 rate is rising **6.8%/season** (IRR 1.068), faster than centuries (4.8%).
  - Bonuses ranging from £0 to £147,000 show **no significant association** (all p > 0.5).
  - A great "incentives don't always move results" piece.
- **Basketball, incentives (DRIVE).** J. Zytnick, *"Trade the pick: Ending tanking in professional sports"*, *J. Sports Analytics* 2026-08-19 (OPENED abstract). It proposes that teams trade away their own next first-round pick before the season. It is theoretical plus NBA data, so present it as a proposal, not evidence.
- **Youth football, culture (DRIVE).** S. Wagnsson & E. Lundkvist, *"Scoreless but still scoring…"*, *J. Sports Sci.* 2026-08-05 (OPENED abstract; paywalled). Covers 30,000+ Swedish children aged 7–12. Removing league tables and playoffs in 2017 brought no significant change in participation.
- **NFL decision (DATA).** D. Goings, *"Game-theoretic analysis of the NFL playoff overtime coin toss"*, *J. Sports Analytics* 2026-07-21 (OPENED abstract). Receiving wins **53.14%** of simulated games, yet most toss winners kick.
- **NBA tracking (DATA).** A. Kondur & W. Shen, *"Statistical analysis of NBA defensive responses to hot-hand streaks"*, *J. Sports Analytics* 2026-06-05 (OPENED abstract). Defenders tighten more after makes than they relax after misses, over roughly a 3–5-shot memory window.

---

# Ranked shortlist: write these first

**DATA → DATA-1, the MLB ABS challenge ("Two Seconds to Overrule the Umpire").**
- It is the first MLB regular season with ball-strike challenges, and it is ending now.
- The seed is primary league data, fully opened, with three supporting sources.
- It is non-football and teaches a key analytics idea: selection bias, "overturn rate ≠ error rate".
- It gives the reader a practical decision rule based on count leverage.
- Next: DATA-3 (ML review; fully opened, 18 Sept) and then DATA-2 (rugby EP; its version of record is behind a bot challenge, so write from the preprint only after checking).

**DRIVE → DRIVE-1, WNBA home advantage and jet lag ("Is Home Court Disappearing?").**
- The seed is a July 2026 peer-reviewed, open-access paper read in full.
- It covers women's sport with a surprising, well-quantified result (64.3% to 52.3%, and the eastward effect).
- It is timely with the 2026 expansion season, and it names no individuals.
- Next: DRIVE-2 (NFL kickoff incentives; all official sources opened, although the seed dates from Feb 2026) and then DRIVE-3 (sacking illusion; the seed is abstract-only and it is football, so it goes last).
