# gameformative.com — FIND pass: DEFEND + DEAL desks

Prepared 2026-09-26. Six candidates (3 per desk), each on a seed opened and read. I checked the site files read-only: both desks show "No … articles published yet". The existing articles are `gps-injury-risk-which-math` (ACWR/GPS) and `how-spain-won-the-world-cup` (results). None of the candidates below repeats either angle.

## How to read the source labels

- **OPENED (verbatim)**: I read the raw text (HTML scraped with curl, PDF text via pdftotext, or the abstract via the Europe PMC API) and checked the figures against it.
- **OPENED (fetch tool)**: I read the page through the WebFetch tool, which returns a model-written summary. The figures are as reported by the tool. **Re-check them verbatim at the writing stage.**
- **SNIPPET ONLY**: seen only in a search-result snippet. Never a seed, never a figure source.
- **BLOCKED**: 403, JavaScript challenge, paywall or redirect. Not used.
- The key documents (Deloitte ARFF 2026, USTA audited accounts, Wimbledon 2026 prize money, WADA 2027 List, explanatory note and Monitoring Program) are linked in each entry below; open them at source — third-party PDFs are not copied into this repository.

---

# DEFEND — Risk and integrity: injury systems, load practice, governance

## D1. The 2027 banned list is out. Weight-loss jabs still aren't on it — here's what is new

**Reader promise:** in five minutes, know what changes for athletes on 1 January 2027, what stays the same, and why WADA has not banned GLP-1 drugs.

**Seed: OPENED (verbatim).** WADA, "WADA publishes 2027 Prohibited List", 21 Sep 2026. https://www.wada-ama.org/en/news/wada-publishes-2027-prohibited-list
- The Executive Committee approved the list on 10 Sep 2026. It enters into force on 1 Jan 2027.
- Major modifications:
  - Substances of Abuse: metabolites are to be considered in results management.
  - S4.2 title expanded.
  - S8: changed "to reflect current scientific knowledge on the Δ9-THC like-effects of commonly encountered cannabinoids".
  - S9: vaginal glucocorticoid administration added as a permitted route.
  - P1 beta-blockers: sport disciplines harmonised.
  - Extra examples added in S0, S4, S5 and S8.
- GLP-1 receptor agonists, including semaglutide and tirzepatide, "will remain unchanged for 2027 pending further data". Olivier Rabin (WADA Senior Director, Science and Medicine) said "there is not enough evidence available for us to conclude with confidence that the substances meet the criteria". WADA has started a second study.
- To be added to the List, a substance must meet 2 of 3 criteria: performance, health risk, spirit of sport.
- The List is published three months before it takes effect.

**Supporting sources (all OPENED)**

1. **WADA, "2027 Summary of Major Modifications and Explanatory Notes"** (PDF dated 17 Aug 2026, published 21 Sep 2026). OPENED (verbatim). https://www.wada-ama.org/sites/default/files/2026-09/2027_list_explanatory_note_en_final_17_august_2026_1.pdf
   - S0: "peptides are now named as examples".
   - S4: imlunestrant, seladelpar, SLU-PP-332 and SLU-PP-915 added as examples.
   - S5: eplerenone and finerenone added.
   - S8: "Cannabidiol is not prohibited", but CBD from cannabis plants may contain THC.
   - Monitoring Program: codeine, dermorphin and analogues, and hydrocodone removed; fentanyl and tramadol removed from out-of-competition monitoring.
   - **Clean 2027 List** (`2027list_en_final_clean_26_august_2026_2.pdf`), OPENED (verbatim): S8 now names "Δ8-THC and Δ10-THC" and "Hexahydrocannabinols (HHC)". S0 text names "peptides" and BPC-157. Tramadol remains in S7 (in-competition).
2. **WADA, "2027 Monitoring Program"** (PDF dated 21 Aug 2026). OPENED (verbatim). https://www.wada-ama.org/sites/default/files/2026-09/2027_list_monitoring_program_en_final_clean_21_august_2026.pdf
   - "GLP-1 Agonists: In and Out-of-Competition: Semaglutide and tirzepatide" are still monitored.
   - Also monitored: caffeine, nicotine and bupropion (in-competition), and ecdysterone.
3. **La Vignera S, Condorelli RA.** "Incretin-Based Therapies in Sports… A Narrative Review." *Int J Mol Sci* 27(14):6116, first published 8 Jul 2026, doi:10.3390/ijms27146116. **Abstract** OPENED (verbatim, Europe PMC); the MDPI full text was BLOCKED (403).
   - GLP-1 RAs "reduce lean mass by 20-30% of total weight loss".
   - "clinical trials show no consistent improvement in physical performance in humans".
   - "current evidence does not support classification as doping agents".

**Investigated, not used**
- **USADA**, "Weight Loss Drugs: What athletes need to know about GLP-1s". OPENED (fetch tool). The page is **undated** and repeats WADA's position. Use it only as a "where to ask" pointer if at all.
- **Sport Resolutions**, "WADA publishes 2027 Prohibited List" (23 Sep 2026). OPENED (fetch tool). Secondary and duplicates the WADA primary.
- **Gran Fondo Daily** (12 Sep 2026) and **worldbandy.com** (22 Sep 2026): secondary re-reports, SNIPPET ONLY.
- **BPC-157 "status" pages** (highpeptides, realpeptides, undergroundbiohacking and others): commercial sellers or biohacking blogs. Unreliable and SNIPPET ONLY. Never cite.
- **LawInSport** on the 2027 Code: about Code sanctions, not the List. Off-scope and not opened.

**Segment outline (target 2,400–3,000 characters)**
1. *The list that lands every autumn*: what the Prohibited List is, the 2-of-3 criteria, and why it comes out three months early.
2. *What actually changed*: the peptide wording in S0; new named THC-like cannabinoids (Δ8, Δ10, HHC); CBD still allowed but with a contamination caveat; vaginal glucocorticoids permitted.
3. *The GLP-1 question*: still permitted and still monitored. What the 2026 review evidence says about lean-mass loss and the lack of performance proof.
4. *Monitoring vs banning*: what the Monitoring Program is for, and what dropped off (codeine, hydrocodone, and others).
5. *What it means for an athlete on 1 January*: strict liability, and asking your anti-doping organisation when in doubt.

**Risks**
- Do not imply that any athlete uses GLP-1s or peptides. No names and no cases.
- Do not say GLP-1s are "safe" or "performance-enhancing". Both are unproven.
- Do not state the full S8 wording change beyond what the clean List and the explanatory note show.
- The 2027 World Anti-Doping **Code** also takes effect in 2027 (SNIPPET ONLY here). Do not blend Code sanction changes into a List article.
- Not medical advice. Point readers to their anti-doping organisation.

---

## D2. What a smart mouthguard can — and can't — tell a doctor about a head knock

**Reader promise:** understand how instrumented mouthguards flag head impacts, why one peak number isn't enough, and why a 45 kg teenager shouldn't be scored like an adult man.

**Seed: OPENED (verbatim abstract via Europe PMC; full text read on PMC via fetch tool).** Ward J, Tooby J, Bonnet D, et al. "Biomechanical Profiles of Diagnosed Concussions in Rugby Union: A Case Study Using Instrumented Mouthguards." *Sports Medicine – Open* 12, first published 13 Jul 2026, doi:10.1186/s40798-026-01068-z. https://pmc.ncbi.nlm.nih.gov/articles/PMC13365273/
- Study population: a French professional U21 academy across 34 matches (254 player-matches, 241 h). Mouthguards captured 4,414 head acceleration events (HAEs). Three concussions were clinically diagnosed.
- Across the three concussions, peak linear acceleration was 27.6–48.4 g, peak angular acceleration 3,234–4,089 rad/s², and ΔPAV 17.7–28.5 rad/s.
- Player #3 lost consciousness after a head-on-head collision and had the highest ΔPAV (28.5 rad/s).
- Player #2 was diagnosed after the match. He showed the highest *cumulative* angular load (ΔPAV 144.3 rad/s; PAA 17,340 rad/s²) "despite no clear concussive impact".
- Conclusion: concussions "can result from both single high magnitude impacts and cumulative impacts". The authors call for multi-metric monitoring "rather than reliance on isolated thresholds".

**Supporting sources (all OPENED)**

1. **Bussey MD, McGeown JP, Dempsey S.** "Sensitivity of brain injury criteria to anthropometric scaling assumptions in instrumented mouthguard data." *Journal of Biomechanics* 204 (online 17 May 2026; print July 2026), doi:10.1016/j.jbiomech.2026.113378. **Abstract** OPENED (verbatim, Europe PMC). The ScienceDirect page was BLOCKED (JavaScript).
   - Data: 15,237 video-verified HAEs from 572 community rugby players aged 10–38 and weighing 34–142 kg.
   - Most commercial systems assume a 50th-percentile male head.
   - Female players modelled with male parameters showed "up to 54% higher PRHIC and 18-27% higher HIP and kinetic energy".
   - For players under 55 kg, the multiple-reference model cut predicted rotational power "by more than 60%".
   - Misclassification occurred near thresholds such as "PLA ≥ 65 g".
2. **World Rugby**, "Instrumented Mouthguard (iMG) update", 8 Mar 2024. OPENED (fetch tool). https://www.world.rugby/news/912305/instrumented-mouthguard-img-update
   - Process: an alert leads to an on-field doctor check. A player the doctor clears stays on but still completes HIA1 at half-time or full-time, plus HIA2 and HIA3.
   - No numeric thresholds are published there. **Older, used for process context only.**
3. **World Rugby**, "World Rugby integrates smart mouthguard technology to the HIA", 9 Oct 2023. OPENED (fetch tool). Covers the €2m initial support, supplier Prevent Biometrics, and HIA integration from January 2024. **Background only.**

**Investigated, not used**
- **MedicalXpress**, "One-size-fits-all smart mouthguard data may overlook serious rugby head injuries" (29 Jun 2026). OPENED (fetch tool). A press summary of the J Biomech paper; the primary abstract is used instead.
- **arXiv 2502.15405**, "Concussion and head acceleration exposure in elite rugby union and American football". SNIPPET ONLY. A 2025 preprint that is not peer-reviewed and too old.
- **Sports Medicine 2023** (Tooby et al., elite iMG incidence): older than 2026, context only. Not opened.
- **March 2026 community-rugby HAE study** (259 players, U13 to senior): SNIPPET ONLY. Not opened, so not used.

**Segment outline (target 2,200–2,800 characters)**
1. *A sensor between your teeth*: what an iMG measures (linear vs rotational acceleration) and why rugby adopted it.
2. *Alert ≠ diagnosis*: how an alert feeds into the Head Injury Assessment (World Rugby process).
3. *Three concussions, three signatures*: the 2026 U21 case study, including the cumulative-load finding.
4. *Your head is not the crash-test dummy's*: the scaling problem in the 54% and >60% figures, and what it means for women and youth players.
5. *What good monitoring looks like*: multiple metrics, cumulative load, and clinical judgement first.

**Risks**
- The case study has **n = 3 concussions**. It is hypothesis-generating and must not be presented as a rule.
- Do not publish numbers as "the concussion threshold". None is published, and the papers argue against single thresholds.
- Do not suggest named products are faulty. The J Biomech paper criticises a modelling assumption, not a brand.
- Community-rugby data do not transfer automatically to elite play (the authors say so).
- No medical advice.

---

## D3. Too hot to play? Why sport still can't agree on the thermometer

**Reader promise:** understand what WBGT is, why FIFA and the players' union draw the danger line at different numbers, and what 2026 science says about whether those lines work.

**Seed: OPENED (verbatim abstract, Europe PMC).** Blackman C, Bellenger C, Périard J, Wakim D, Chalmers S. "Thermophysiological response of adults to long-distance running in different ACSM environmental risk conditions: A systematic review and meta-analysis." *Journal of Sport and Health Science*, first published 20 Jul 2026, doi:10.1016/j.jshs.2026.101158.
- Data: 43 studies (48 participant groups) of self-paced runs of at least 5 km, grouped by ACSM WBGT categories (low ≤22.2 °C; moderate 22.3–25.6; high 25.7–27.8; very high ≥27.9).
- The high-risk group reached the highest end core temperature (39.50 °C). Only the low and high groups differed significantly (p = 0.026).
- Heart rate was 185 vs 181 bpm (high vs moderate).
- Conclusion: strain was "typically greater in the higher risk categories". However, "risk thresholds were not consistently distinct".
- Full text not opened; abstract only.

**Supporting sources (all OPENED)**

1. **Bandiera D, Garrandes F, … Racinais S, … Bermon S.** "What do thermal indices lack to help predict heat-related risk in elite Athletics?" *BJSM* 60(7), first published 23 Mar 2026, doi:10.1136/bjsports-2025-110822. **Abstract** OPENED (verbatim, Europe PMC).
   - Data: 4,938 athletes in 80 World Athletics races, 2019–2024.
   - Exertional heat stroke occurred at "8/1000 on average and 16/1000 when the WBGT was above 28.0°C".
   - Mean radiant temperature was a stronger predictor (R² = 0.11) than WBGT (R² = 0.04).
   - Neither index "provided sufficient predictive accuracy".
2. **FIFPRO**, "Players in Korea Republic call for stronger heat protections after alarming survey", 17 Aug 2026. OPENED (verbatim). https://www.fifpro.org/en/articles/2026/08/players-in-korea-republic-call-for-stronger-heat-protections-after-alarming-survey
   - The survey was run by the Korea Pro-Footballers Association (KPFA): 536 K League and WK League players.
   - 86.2% reported significant strain, 64.7% dizziness and 56.6% severe dehydration.
   - "13 percent – 70 players – said they had experienced temporary lapses in consciousness".
   - FIFPRO guidance: cooling breaks above 26 °C WBGT; delay or postpone above 28 °C.
3. **ESPN (Mark Ogden)**, "FIFA, FIFPRO discussing heat protocols after World Cup concerns – sources", 12 Jul 2026. OPENED (fetch tool; raw HTML returned empty). https://www.espn.com/soccer/story/_/id/49343877/fifa-world-cup-fifpro-temperature-heat-protocol-talks-sources
   - England v Norway QF in Miami: WBGT reported at 31.1 °C (88 °F) at kickoff.
   - FIFA's mandatory cooling-break threshold is 32 °C WBGT; FIFPRO's delay/postpone line is 28 °C.
   - "no accepted or agreed cut-off point between FIFA and FIFPRO."
   - Also FIFA (inside.fifa.com), "Players to benefit from hydration breaks at FIFA World Cup 2026", OPENED (fetch tool; page date not captured). Three-minute breaks 22 minutes into each half of every match, with "no weather or temperature condition".

**Investigated, not used**
- **Reuters satellite-WBGT analysis** (about 11 Jul 2026: 35 of 94 matches above FIFPRO's 26 °C, 27 above 28 °C, none at 32 °C). SNIPPET ONLY. The mirror (barlamantoday) was BLOCKED (403) and I found no readable Reuters copy. **Do not use these counts.**
- **Guardian analysis** (16 Jul 2026, "nearly one in five matches"). SNIPPET ONLY; the domain is inaccessible to my tools. VitalLaw's re-report (21 Jul 2026) was OPENED (fetch tool), but it is secondary and gives no match counts.
- **World Weather Attribution**, "Climate Change Big Player at FIFA World Cup 2026" (14 May 2026). OPENED (fetch tool). A pre-tournament projection (for example, about 5 games expected at ≥28 °C WBGT) that observed conditions now supersede. Not stated as peer-reviewed.
- **arXiv 2607.19783** (Dey, Jul 2026), hydration breaks and match momentum. OPENED (fetch tool). A preprint that is not peer-reviewed and about tactics, not health.
- **ESPN (Tom Chambers)**, 19 Jul 2026, on criticism that the breaks carried adverts. OPENED (fetch tool). Commercial angle and off-desk; a possible DEAL spin-off.
- **Scientific Reports 2024** heat-risk forecast: older than 2026.

**Segment outline (target 2,400–3,000 characters)**
1. *One number for heat*: what WBGT combines (temperature, humidity, sun, wind).
2. *Two red lines*: FIFA's 32 °C vs FIFPRO's 26 °C and 28 °C, the World Cup quarter-final at 31.1 °C, and the blanket hydration breaks.
3. *What the lab says*: the July 2026 meta-analysis, where strain rises with category but the category boundaries are not cleanly distinct.
4. *What the racecourse says*: the BJSM athletics data, where the heat-stroke rate above 28 °C WBGT is twice the average (16 vs 8 per 1,000) yet WBGT predicts poorly.
5. *What players say*: the Korean survey (self-reported).
6. *So what should a rule do?* Why an index plus acclimatisation, kick-off times and medical cover beats any single number.

**Risks**
- The meta-analysis covers running time trials and the BJSM study covers elite endurance athletics, **not football**. Say so explicitly.
- The Korean figures are self-reported survey answers, not clinical diagnoses.
- WBGT values vary by measurement method (on-site vs satellite, open-air vs air-conditioned venues). Do not compare numbers from different methods.
- Do not claim any World Cup player was harmed, and do not allege negligence. The FIFA–FIFPRO talks are reported via unnamed "sources", so attribute them.
- Stick to published thresholds.

---

# DEAL — Money and rights: sponsorship, media rights, commercial structures

## M1. $108 million and still arguing: how much of a Grand Slam's money reaches the players?

**Reader promise:** see where the "15% vs 22%" numbers in tennis's pay dispute come from, and how to check them yourself in a tournament's accounts.

**Seed: OPENED (verbatim).** Reuters (Frank Pingue), "U.S. Open announces record $108-million prize purse", 21 Aug 2026 (syndicated copy, Fulton Sun). https://www.fultonsun.com/news/2026/aug/21/us-open-announces-record-108-million-prize-purse/
- $108m purse, "the largest purse in tennis history".
- Singles champions get $5.5m each (+10%). First-round payouts are $140,000 (+27%).
- The Player Support Program starts with $2m in 2026.
- The top players' statement: "While this is not yet tied to an agreed revenue-sharing formula, players remain committed to that principle."
- The 15-minute media limits at the French Open and Wimbledon symbolised "the roughly 15 percent of tournament revenue" going to prize money.

**Supporting sources (all OPENED)**

1. **USTA and Affiliates, Consolidated Financial Statements, years ended 31 Dec 2024 and 2023** (audited; published 2025). OPENED (verbatim PDF). https://www.usta.com/content/dam/usta/2025-pdfs/2025-usta-and-affiliates-consolidated-financial-statements.pdf
   - US Open operating revenue: $559.658m (2024) and $514.105m (2023).
   - US Open expenses, including depreciation, pledge and interest: $282.239m (2024).
   - Player compensation: $76.349m (2024) and $65.739m (2023).
   - Ticket revenues: $208.475m. Broadcasting cash: $140.077m. Sponsorship cash: $124.978m.
   - *Own calculation:* player compensation ÷ US Open revenue ≈ 13.6% (2024) and 12.8% (2023).
2. **AELTC**, "The Championships, Wimbledon 2026 – Prize Money" (PDF created 10 Jun 2026). OPENED (verbatim). https://content.wimbledon.com/is/content/AELTC/aeltc/wimbledon/live-site/guest/pdfs/The%20Championships%202026_Prize%20Money.pdf
   - Total £64.2m (+20%). Singles winners get £3.6m. First round is £80,000 (+21%).
3. **ESPN/AP**, "French Open players plan media protest over prize money share", 20 May 2026. OPENED (fetch tool). https://www.espn.com/tennis/story/_/id/48825737/french-open-players-plan-media-protest-prize-money-share
   - The players' own calculation: 15.5% (2024) falling to 14.9% (2026 projected).
   - Roland-Garros revenue was €395m in 2025 and is estimated at over €400m for 2026.
   - Prize pool €61.7m. The 22% demand matches the ATP/WTA combined 1000 events.
   - Also ATP Tour, "2026 US Open prize money" (20 Aug 2026), OPENED (fetch tool; curl hit a Cloudflare challenge): the round-by-round table and the 20% rise.

**Investigated, not used**
- **usopen.org official release** (20 Aug 2026). BLOCKED (JavaScript-rendered; fetch timed out).
- **Sportico** "2026 US Open Prize Money of $108M…". BLOCKED (tollbit paywall redirect).
- **Sportico 2025**, "USTA Enters U.S. Open With $624M in Revenue". Secondary and duplicates the primary audited statements.
- **CBS Sports, EssentiallySports, Bleacher Report** prize-money explainers: duplicative secondary coverage.

**Segment outline (target 2,400–3,000 characters)**
1. *A record cheque*: the $108m US Open, and why players welcomed it but didn't declare victory.
2. *Where the 15% comes from*: prize money ÷ tournament revenue, and why the players' Roland-Garros figures are their own calculation.
3. *Reading the US Open's own accounts*: $559.7m revenue vs $76.3m player compensation in 2024 (≈13.6%), including the ticket, TV and sponsor lines.
4. *Why 22%?* The ATP/WTA 1000 benchmark.
5. *Same sport, four landlords*: the Slams set their own prize money (Wimbledon £64.2m, Roland-Garros €61.7m).
6. *What to watch*: revenue-share formula talks, and the 2025 accounts when they are published.

**Risks**
- The 15%, 14.9% and 22% figures are **players' calculations or demands**. Attribute them. The Slams have not endorsed them; the FFT only offered talks on "evolving the distribution of value".
- The USTA "player compensation" line is organisation-wide and may include more than US Open prize money. Label the 13.6% as an approximation and our own calculation.
- The fiscal years don't match: 2024 accounts vs the 2026 purse. Never divide the 2026 purse by 2024 revenue.
- Separate litigation involving the player association and the tours exists (not investigated). Do not reference allegations.
- No named-player claims beyond published statements.

---

## M2. Four fewer races, 38% less money: how Formula 1 actually books its revenue

**Reader promise:** understand F1's three main income streams and why a postponed Grand Prix knocks a hole in one quarter's numbers.

**Seed: OPENED (verbatim).** Liberty Media, "Liberty Media Corporation Reports Second Quarter 2026 Financial and Operating Results", 6 Aug 2026. https://www.libertymedia.com/investors/news-events/press-releases/detail/587/liberty-media-corporation-reports-second-quarter-2026

**Q2 2026 vs Q2 2025** (unaudited, $ millions)

| Line | Q2 2025 | Q2 2026 | Change |
|---|---|---|---|
| Races in period | 9 | 5 | – |
| Primary F1 revenue | 1,032 | 622 | −40% |
| Other F1 revenue | 194 | 142 | −27% |
| Total F1 revenue | 1,226 | 764 | −38% |
| Team payments | 513 | 316 | – |
| Adjusted OIBDA | 361 | 139 | – |
| Operating income | 293 | 73 | – |

- Year to date: $1,381m revenue (−15%), from 8 races vs 11.
- Primary revenue is defined as "(i) race promotion fees, (ii) media rights fees and (iii) sponsorship fees".
- Season-based revenue is recognised per race: "5/22nds during the quarter compared to 9/24ths" a year earlier.
- The fall was "partially offset by underlying contractual fee increases". Q2 2025 also included one-time media revenue from the F1 movie.
- The Saudi Arabian GP was not held in April. The Bahrain GP was moved to Malaysia in October, and the calendar is now assumed at 23 races.
- The Las Vegas GP was extended through 2037.
- Apple partnership: "total hours watched up 13%".
- MotoGP Q2 revenue: $170m.

**Supporting sources**

1. **Sportcal (Euan Cunningham)**, "F1 race postponements lead to Liberty Media revenue drop in Q2", 6 Aug 2026. OPENED (fetch tool). https://www.sportcal.com/news/f1-race-postponements-lead-to-liberty-media-revenue-drop-in-q2/
   - Reports (paraphrased by the fetch tool) that the Bahrain and Saudi races were postponed because of a regional conflict in the Middle East. The primary release gives no reason, so attribute this to Sportcal and re-check the wording verbatim.
2. **ESPN (Nate Saunders)**, "Formula 1 announces new Apple TV US broadcast deal", 17 Oct 2025. OPENED (fetch tool). A five-year exclusive US deal from 2026. **Older, background only.**

**Investigated, not used**
- **Apple deal value**: reported figures differ (about $140m/yr in a CNBC snippet, about $160m/yr per the fetch-tool read of ESPN, about $750m total in a Variety snippet). The value is not officially disclosed and I could not verify it in raw text. **Do not print a number.**
- **GPFans**, "F1 teams suffer $127m shock…": the figure is not in the primary release and the framing is sensational.
- **TradingView and GuruFocus** summaries: derivative of the primary release.
- **CNBC 2025 Apple article**: BLOCKED (403). **Hollywood Reporter**: BLOCKED (tollbit).

**Segment outline (target 2,000–2,800 characters)**
1. *The headline that isn't a crisis*: −38% in a quarter, explained.
2. *F1's three taps*: race promotion, media rights and sponsorship (plus "other", such as hospitality and freight).
3. *Revenue by the race*: the 5/22 vs 9/24 recognition, where a season's money is booked race by race.
4. *Who else feels it*: team payments move with revenue ($316m vs $513m).
5. *Calendar as a financial instrument*: the Malaysia replacement, the Las Vegas extension, and why hosting fees matter.
6. *The streaming bet*: Apple in the US (viewing metrics only, no price).

**Risks**
- The quarter is unaudited. The drop is mostly a timing effect, so do not frame it as F1 "losing money" or demand collapsing.
- Attribute the reason for the postponements (regional conflict) to Sportcal and do not speculate further.
- No Apple deal value.
- Figures cover F1 as a Liberty segment, not the teams' finances.

---

## M3. The £1bn turnstile: why football's matchday is suddenly the growth story

**Reader promise:** see why ticket and hospitality money is now growing faster than TV money, what "premiumisation" means, and who pays for it.

**Seed: OPENED (verbatim, full PDF).** Deloitte Sports Business Group, *Annual Review of Football Finance 2026: "Defending from the front"* (35th edition), cover dated **July 2026**. The foreword says the World Cup was "about to enter its Quarter Finals" at launch. https://www.deloitte.com/uk/en/services/consulting/research/annual-review-of-football-finance-europe.html (PDF: `…/2026/deloitte-annual-review-of-football-finance-2026.pdf`)

**Europe and the big five**
- The European market "surpassed €40 billion for the first time" (+6%). The big five account for 54% (€22bn).
- "Matchday revenue was therefore the only source of income that grew across all five leagues", up €0.4bn (16%) to €3.4bn.

**Premier League**
- Matchday revenue "rose by £133m (15%)… to surpass £1 billion for the first time". It is anticipated at "almost £1.1 billion" in 2025/26.
- Total revenue was £6.8bn (+8%). Broadcast revenue rose only 2% to £3.4bn.
- The new domestic deal is a reported £6.7bn over four years, "an estimated 2% increase" per season.
- Aggregate operating profit fell £274m to £263m; pre-tax losses were £948m.

**Deloitte's framing**
- It flags "premiumisation and hyper-commercialisation" seen at the World Cup.
- It says 2026 World Cup ticket pricing "raised questions about the accessibility of the game".

**Supporting sources**

1. **FIFA Annual Report 2024**, "Revised 2023–2026 budget". OPENED (verbatim JSON text). https://inside.fifa.com/official-documents/annual-report/2024/financials/revised-2023-2026-budget
   - 2026 revenue budget: USD 8,911m, including "Hospitality rights and ticket sales… a record high of USD 3,017 million".
   - The cycle target is USD 13,000m.
   - Also **FIFA Annual Report 2025**, "2025 revenue", OPENED (verbatim). The publication date of 16 Mar 2026 comes from a search snippet only; the page did not show it. 2025 revenue USD 2,661m, with 93% of the cycle budget contracted by the end of 2025.
2. **FIFA**, "Gianni Infantino aims to 'unleash the commercial potential'…", 18 Jul 2026. OPENED (verbatim). https://inside.fifa.com/news/gianni-infantino-world-cup-usd-15-billion-revenue-members
   - "Expects FIFA's revenues to top USD 15 billion… for the 2023-2026 cycle". This is a **projection, not audited**.
   - Forward funding: USD 2.7bn for 2027–2030.
3. **Fortune (Marco Quiroz-Gutierrez)**, 21 Jul 2026. OPENED (fetch tool). https://fortune.com/2026/07/21/fifa-15-billion-dollar-pay-day-world-cup-usa-spain-argentina-final-2030/
   - First use of dynamic pricing at a World Cup; group-stage tickets up to $575 (vs $220 max in Qatar).
   - FIFA took a 15% cut from both buyer and seller on its resale platform.
   - $15bn refers to the cycle, not the tournament. Re-check these figures verbatim before use.

**Investigated, not used**
- **Inside World Football**, 20 Jul 2026. OPENED (fetch tool). It presents $15bn as "World Cup revenue", which conflicts with FIFA's own "2023-2026 cycle" wording. It also mentions state attorney-general inquiries into ticketing; that is legally sensitive and not needed.
- **CNBC**, "FIFA emerges as the $9 billion winner…" (20 Jul 2026). BLOCKED (403).
- **Deloitte Football Money League 2026** (January 2026): a club-ranking scope that duplicates ARFF. Not opened.
- **Yahoo** syndication of Fortune: duplicate.

**Segment outline (target 2,400–3,000 characters)**
1. *A £1bn milestone*: Premier League matchday money crosses £1bn.
2. *Why the gate is outgrowing the TV*: broadcast +2%, a flat-ish new domestic deal, and more European home games.
3. *Premiumisation, defined*: hospitality tiers, "enhanced fan experiences", and yearly price rises.
4. *The World Cup as a showroom*: FIFA's USD 3,017m ticket and hospitality budget, dynamic pricing, and the resale cut.
5. *Revenue up, profit down*: the £263m operating profit and £948m pre-tax loss.
6. *The fan question*: Deloitte's own warning that match-goers may "vote with their feet".

**Risks**
- FIFA's USD 15bn is a spoken projection for the whole cycle. The audited figure comes with FIFA's 2026 annual report. Never call it "World Cup revenue".
- Keep Deloitte's estimates ("anticipated", "reported") hedged as Deloitte hedges them.
- Do not repeat attorney-general inquiry claims.
- Two sports business contexts (clubs vs FIFA) must not be merged into one number.
- This is football-only, so pair it with M1 and M2 for spread.

---

# Reserve bench (checked, weaker; not full candidates)

- **NFL may repackage its TV deals.** SportsPro, 11 Sep 2026, OPENED (fetch tool). Goodell's quotes; the $110bn over 11 years deals with a 2029 opt-out. Forward-looking and interview-based; the "50% increase sought" figure is report-only.
- **Betting-integrity alerts Q2 2026.** Covers.com, 23 Jul 2026, OPENED (fetch tool). 76 alerts across 9 sports (football 25, esports 16), +10.1% YoY. The IBIA primary (ibia.bet) is BLOCKED (403), so there is no primary seed yet.
- **IOC TOP sponsorship at $560m in 2025, after five sponsors exited.** SNIPPET ONLY (SportsPro, IOC Annual Report 2025, published June 2026). Worth opening next if DEAL needs an Olympic angle.
- **IOC female-category policy (SRY screening, EB 26 Mar 2026).** SNIPPET ONLY. High legal and editorial sensitivity; would need the IOC text opened first.

# Ranked shortlist — write first

1. **DEFEND → D1 (WADA 2027 Prohibited List).**
   - Freshest seed (published 21 Sep 2026, five days ago) with a real deadline for readers (in force 1 Jan 2027).
   - Every claim rests on primary WADA documents I read verbatim: the release, the explanatory note, the clean List and the Monitoring Program. A July 2026 peer-reviewed review supports the GLP-1 angle.
   - No named individuals, so the lowest legal risk on the desk.
   - Runner-up: D2 (mouthguards), which is excellent science but rests on n = 3.
2. **DEAL → M1 (Grand Slam revenue share).**
   - The US Open ended 13 Sep and the $108m purse was announced 21 Aug. The story has a genuine, answerable reader question.
   - Primary documents give the maths: the USTA audited accounts and the AELTC prize-money sheet.
   - It covers a non-football sport.
   - The contested numbers are clearly attributable (players' figures vs audited accounts).
   - Runner-up: M2 (F1), which is fully primary-sourced and lower-risk but less topical for a general reader.
