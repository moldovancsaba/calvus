"""Editorial content for the gameformative prototype — one source, read by build.py.

gameformative is a sport analytical and educational infotainment site: news, tactics, techniques
and the science of sport. Its sections are the eight desks in DESKS — each article sits on one, by
what it does for the reader — and each article carries a subject from TOPICS (owner, 2026-09-25). The launch is articles
only (04-decisions.md D17). Every article obeys the house rules in RULES — 800 to 3,200 characters
of body text, always segmented under headings, and closed by two source lists: the sources used and
the sources investigated but not used. build.py and check.py both enforce them.

Two kinds of article live here:
- the owner's own drafts, shipped as written (the first: the GPS / injury-risk piece, from the
  owner's draft of 2026-09-25 — its internal status block was removed, nothing else changed);
- data articles written for the prototype by the data desk (no named newsroom exists yet), whose
  every number is read from data/stats.json (openfootball, CC0). Where a sentence depends on the
  data telling a particular story, a `premise` assert states it, so a data refresh that would make
  the copy untrue stops the build instead of publishing it (D7)."""

SITE = dict(
    name="gameformative",
    domain="gameformative.com",
    # Absolute base for canonical, Open Graph, sitemap and feed URLs. The prototype is served from
    # GitHub Pages; production sets "https://gameformative.com/" (docs/15-discoverability.md).
    url="https://moldovancsaba.github.io/calvus/gameformative/",
    production_url="https://gameformative.com/",
    tagline="Sport, explained.",
    description="gameformative — sport analysis and education: news, tactics, techniques and the science of sport, every article with its sources listed, used and investigated.",
    published="25 September 2026",
    published_iso="2026-09-25",
)

# The house rules for every article (owner, 2026-09-25). "Characters" are the characters of the
# body text a reader reads — the standfirst and every paragraph of every segment, spaces included;
# the headline, segment headings, charts and the source lists are not counted (10-ssot.md).
RULES = dict(min_chars=800, max_chars=3200, min_segments=3)

# The desks (owner, 2026-09-25): the site's sections. Each article sits on exactly one desk, chosen by
# what the article does for the reader — the owner's wording, verbatim.
DESKS = [  # slug, name, what the article does for the reader
    ("discover", "Discover", "Something new: tech, method, science finding, financing model"),
    ("define", "Define", "Literacy: what a term/metric/rule means, and how not to get fooled"),
    ("design", "Design", "How to build: team, tactic, training system, experience"),
    ("develop", "Develop", "Pathways: athletes and coaches getting better over time"),
    ("data", "Data", "Analytics: models, tracking, measurement, decision support"),
    ("drive", "Drive", "What moves results: incentives, culture, leadership, audience levers"),
    ("defend", "Defend", "Risk and integrity: injury systems, load practice, governance"),
    ("deal", "Deal", "Money and rights: sponsorship, media rights, commercial structures"),
]
DESK = {s: dict(slug=s, name=n, does=d) for s, n, d in DESKS}

# The subjects (owner's topic list, round 2) — kept as each article's subject tag, not as sections.
TOPICS = [  # slug, name, what the subject covers
    ("international-news", "International news", "What happened across world sport, and why it matters."),
    ("sport-science", "Sport science", "Research on performance, injury, recovery and health — read, weighed and explained."),
    ("tactics-technique", "Tactics & technique", "How teams and athletes solve problems on the field, broken down."),
    ("sport-analytics", "Sport analytics", "What the numbers say, how they are made, and where they mislead."),
    ("data-intelligence", "Data intelligence", "How clubs, leagues and brands turn data into decisions."),
    ("sport-tech", "Sport tech", "Wearables, tracking, broadcast and the tools changing how sport is played and watched."),
    ("athlete-development", "Athlete development", "Talent, training and the long road from academy to elite."),
    ("fan-engagement", "Fan engagement", "How fans follow, pay, play and belong — and what keeps them."),
    ("sponsorship", "Sponsorship", "The deals, the money and what partners actually get back."),
    ("training-goods", "Training goods", "Equipment for training and recovery, tested against the evidence."),
    ("sport-goods", "Sport goods", "Kit, boots, balls and the business behind them."),
]
TOPIC = {s: dict(slug=s, name=n, blurb=b) for s, n, b in TOPICS}

NAV = [  # label, path from the site root, short label for the phone tab bar
    ("Home", "index.html", "Home"),
    ("Latest", "articles/index.html", "Latest"),
    ("Desks", "desks/index.html", "Desks"),
    ("Sources", "sources/index.html", "Sources"),
    ("How we work", "how-we-count/index.html", "Standards"),
]
TABBAR = ["Home", "Latest", "Desks", "How we work"]  # + "More", the fifth tab

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def nice_date(iso, year=True):
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]}" + (f" {y}" if year else "")


def short_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[int(m) - 1][:3]}"


def premise(cond, what):
    assert cond, f"content premise no longer true after a data refresh: {what} — rewrite the copy"


def ordinal(n):
    return {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth"}.get(n, f"{n}th")


def pct(x):
    return f"{x:.1f}".rstrip("0").rstrip(".") + "%"


def L(S, lid):
    return next(l for l in S["leagues"] if l["id"] == lid)


def src(title, publisher, url, note, date=None):
    return dict(title=title, publisher=publisher, url=url, note=note, date=date)


OF = "https://github.com/openfootball/football.json/blob/master/"
WC = "https://github.com/openfootball/worldcup.json/blob/master/2026/"
OFP = "openfootball / football.json — public domain (CC0 1.0)"
WCP = "openfootball / worldcup.json — public domain (CC0 1.0)"
# Sources investigated for the data articles and not used — each was opened or requested on
# 2026-09-25 during the research (docs/01a-source-register.md), and the reason is the real one.
NOT_STATSBOMB = src("StatsBomb open data and its user agreement", "StatsBomb", "https://github.com/statsbomb/open-data", "Investigated as an event-data source; its agreement forbids commercial use and redistribution.")
NOT_FBREF = src("Premier League stats", "FBref", "https://fbref.com/en/comps/9/Premier-League-Stats", "Refused our request (HTTP 403, a bot challenge), so its figures could not be checked.")
NOT_UNDERSTAT = src("EPL expected goals table", "Understat", "https://understat.com/league/EPL", "Opened for its xG data; the licence for reuse is not established, and xG is outside what public-domain data carries.")
NOT_OPTA = src("Premier League stats", "Opta Analyst", "https://theanalyst.com/competition/premier-league/stats", "Opened; proprietary Opta data — not used, so every figure here can be rebuilt from public-domain files.")
NOT_SOFASCORE = src("Premier League tournament page", "Sofascore", "https://www.sofascore.com/tournament/football/england/premier-league/17", "Refused our request (HTTP 403), so it could not be compared.")
NOT_WHOSCORED = src("Premier League tournament page", "WhoScored", "https://www.whoscored.com/", "Blocked our request (HTTP 403), so it could not be compared.")
NOT_FIFA = src("FIFA World Cup 26 coverage", "FIFA", "https://www.fifa.com/en", "The page is built in the browser and returned no readable content to our request.")
NOT_OPTADEF = src("Opta football stats definitions", "Opta Analyst, 23 Jul 2024", "https://theanalyst.com/articles/opta-football-stats-definitions", "Opened for the xG definition; not needed, because this piece uses no xG.")


# ------------------------------------------------------------------ the articles
def articles(S):
    en, es, de, it, fr = (L(S, x) for x in ("en", "es", "de", "it", "fr"))
    p = S["pl2526"]; w = S["wc2026"]
    out = []

    # 0 — the owner's draft (2026-09-25), shipped as written: the lead
    out.append(dict(
        slug="gps-injury-risk-which-math", desk="define", topic="sport-science", kind="Explainer", byline="gameformative editorial desk",
        origin="owner",
        title="Your GPS says “injury risk.” The new football evidence says: which math are we using?",
        standfirst=None,
        segments=[
            ("Why this matters now", ["Your GPS watch says the team is “overcooked.” The medical staff hears “injury risk.” But a 2026 football review found something awkward: depending on how researchers cut the same idea of “high load,” the danger either disappears—or more than doubles. So is the dashboard lying, or are we asking it the wrong question?"]),
            ("The landscape", ["Clubs already live inside GPS and IMU numbers—distance, high-speed running, sprints, accelerations, and the famous acute:chronic workload ratio. Those labels sound shared. They aren’t. Speed zones and ACWR formulas differ by vendor and study. A separate 2026 team-sport meta-analysis of ACWR only found a modest injury link and warned against treating the ratio as a stand-alone crystal ball. Machine-learning models can look sharper on paper while still training on those messy labels."]),
            ("What you can do with this", ["Recognise the trap: a red “spike” tile is not a diagnosis. Avoid treating one universal HSR or ACWR threshold as an on/off injury switch across players. What to do instead—ask three questions before you change a session: (1) Is this spike versus this athlete’s own recent base, not a squad average? (2) Which exact metric and speed band fired? (3) What else changed—minutes, travel, sleep, pitch? If you can’t answer those, deload curiosity beats deload panic."]),
            ("What we would keep", ["Keep measuring with validated devices and clear injury clocks (time-loss / medical attention). Keep multi-marker context beside the pretty ratio: how hard it felt, calendar congestion, and each player’s baseline. That combination is how load monitoring earns its keep."]),
            ("What we would question", ["Question any vendor story that ports Club A’s sprint band onto Club B’s risk model without recalibration. Question reviews that pool incompatible definitions quietly. And question the comfort of a single number when the underlying cut-points still disagree."]),
            ("How the field is arguing it", ["Believers say high-speed and sprint spikes, read against a player’s chronic base, are practical red flags. Sceptics say small single-club samples and non-equivalent formulas make “risk doubling” look more scientific than it is. ML papers chase better AUC; sports-medicine voices answer that a prettier model cannot fix unclear injury labels."]),
            ("Closing note", ["Use GPS as a shared language for “what we did,” not as a verdict on “who will get hurt.” The open question worth caring about: which features stay useful once clubs finally agree on the same speed zones and the same injury clock?"]),
        ],
        sources_used=[
            src("Wearable-Monitored External Workload (GPS/GNSS/IMU) and Lower-Limb Muscle Injuries in Football: A Systematic Review and Exploratory Data Synthesis", "Sport Mont 2026, 24(1), 169–178", "https://doi.org/10.26773/smj.260219", "Seed — OR vs RR split on “high load” is the curiosity gap"),
            src("Acute:chronic workload ratio and load management for team sports: a multilevel meta-analysis", "Frontiers in Public Health, 13 Aug 2026", "https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2026.1896651/full", "Independent ACWR meta-analysis — modest link; rejects stand-alone causal use"),
        ],
        sources_investigated=[
            src("Enhancing Sports Injury Risk Assessment in Soccer Through Machine Learning and Training Load Analysis", "PMC / Sensors (Basel)", "https://pmc.ncbi.nlm.nih.gov/articles/PMC11366842/", "Strong ML angle; deferred so the piece stays on definition literacy + actionable load questions"),
            src("A Frequency-Aware Dual-Stream Deep Learning Framework for Athlete Workload Monitoring and Injury Risk Assessment", "Sensors (MDPI)", "https://doi.org/10.3390/s26134228", "Methods-heavy; would pull the wider audience into a model bake-off"),
            src("Athletes' training load prediction using transformers through data analytics and feature projection", "Discover Artificial Intelligence (Springer)", "https://link.springer.com/article/10.1007/s44163-026-01021-9", "Student-athlete multisport sample — wrong population for pro football muscle-injury decisions"),
        ],
        cover=dict(type="evidence"),
    ))

    # 1 — Premier League, five matchdays in
    t = en["table"]; lead, second = t[0], t[1]
    premise(lead["w"] == lead["p"], "Premier League leader has won every match")
    most = max(t, key=lambda r: (r["gf"], -r["pos"]))
    big = en["agg"]["biggest"]
    premise(most["code"] in (big["home"], big["away"]), "the top scorers also have the biggest win")
    after5 = [(s["points"][4], i + 1, s) for i, s in enumerate(p["race"]["series"])]
    top5 = max(after5, key=lambda x: (x[0], -x[1]))
    premise(top5[1] != 1, "last season's leader after five did not win the title")
    champ5 = after5[0]
    last_full = p["agg"]
    bottom = t[-2:]
    out.append(dict(
        slug="premier-league-five-matchdays-in", desk="data", topic="sport-analytics", kind="Analysis", byline="gameformative data desk", origin="data",
        title=f"Five from five: what {lead['name']}’s perfect start does — and doesn’t — tell us",
        standfirst=f"{lead['pts']} points from {lead['p']} matches is the best start in the league. Last season, the team with {top5[0]} after five finished {ordinal(top5[1])}.",
        segments=[
            ("The start", [
                f"{lead['name']} have won all {lead['p']} of their Premier League matches, scoring {lead['gf']} and conceding {lead['ga']}. That is {lead['pts']} points, the maximum available, and {lead['pts'] - second['pts']} clear of {second['name']} in second.",
                f"The league’s most productive attack belongs to someone else. {most['name']} have scored {most['gf']} — the most of any side — and recorded the biggest win of the season so far, {big['hs']}–{big['as_']} at {big['home'] if most['code'] == big['away'] else big['away']} on {nice_date(big['date'], False)}.",
                ("chart", "race-en")]),
            ("Why five matches is not a verdict", [
                f"Last season’s table is the warning. After five matchdays of 2025/26, {top5[2]['name']} had {top5[0]} points — more than anyone — and finished {ordinal(top5[1])} on {p['table'][top5[1] - 1]['pts']}. {champ5[2]['name']}, who won the title with {p['table'][0]['pts']}, had {champ5[0]} at the same stage.",
                ("chart", "after5-2526"),
                f"The league as a whole is also running hot on a small sample. {en['agg']['matches']} matches in, it has averaged {en['agg']['gpg']:.2f} goals a game, against {last_full['gpg']:.2f} across all 380 of last season, and {pct(en['agg']['draw_pct'])} of matches have been drawn, against {pct(last_full['draw_pct'])} over the full campaign."]),
            ("What to watch", [
                f"At the other end, {bottom[0]['name']} and {bottom[1]['name']} have {bottom[0]['pts']} and {bottom[1]['pts']} points and are still looking for a first win. The next round is scheduled for {nice_date(en['upcoming'][0]['date'], False)}."]),
        ],
        sources_used=[
            src("English Premier League 2026/27 — results (2026-27/en.1.json)", OFP, OF + "2026-27/en.1.json", "Every 2026/27 result, table figure and the next fixture date."),
            src("English Premier League 2025/26 — results (2025-26/en.1.json)", OFP, OF + "2025-26/en.1.json", "Last season’s points after five matchdays and the final table."),
        ],
        sources_investigated=[NOT_FBREF, NOT_OPTA, NOT_UNDERSTAT],
        cover=dict(type="race", league="en"),
    ))

    # 2 — the big five compared
    by_gpg = sorted(S["leagues"], key=lambda l: -l["agg"]["gpg"])
    by_draw = sorted(S["leagues"], key=lambda l: -l["agg"]["draw_pct"])
    premise(by_gpg[0]["id"] == "de" and by_draw[0]["id"] == "en", "Bundesliga scores most, Premier League draws most")
    nil0 = [l for l in S["leagues"] if l["agg"]["nil_nil"] == 0]
    premise(len(nil0) == 1, "exactly one league without a goalless draw")
    btts = max(S["leagues"], key=lambda l: l["agg"]["btts_pct"])
    home = max(S["leagues"], key=lambda l: l["agg"]["home_pct"])
    out.append(dict(
        slug="big-five-first-month", desk="data", topic="sport-analytics", kind="Analysis", byline="gameformative data desk", origin="data",
        title=f"Europe’s big five after a month: the {by_gpg[0]['name']} scores most, the {by_draw[0]['name']} draws most",
        standfirst=f"{by_gpg[0]['agg']['gpg']:.2f} goals a game in Germany, {by_gpg[-1]['agg']['gpg']:.2f} in England — and not a single goalless draw yet in {nil0[0]['name']}.",
        segments=[
            ("Where the goals are", [
                f"A month into the season, Europe’s five biggest leagues have produced {sum(l['agg']['goals'] for l in S['leagues'])} goals in {sum(l['agg']['matches'] for l in S['leagues'])} matches. They have not produced them evenly.",
                ("chart", "gpg-big5"),
                f"The {by_gpg[0]['name']} leads at {by_gpg[0]['agg']['gpg']:.2f} goals a game, helped by results such as {by_gpg[0]['agg']['biggest']['home']} {by_gpg[0]['agg']['biggest']['hs']}–{by_gpg[0]['agg']['biggest']['as_']} {by_gpg[0]['agg']['biggest']['away']}. The {by_gpg[-1]['name']} is lowest at {by_gpg[-1]['agg']['gpg']:.2f}. The samples are small and uneven: between {min(l['agg']['matches'] for l in S['leagues'])} and {max(l['agg']['matches'] for l in S['leagues'])} matches per league, after {min(l['rounds_done'] for l in S['leagues'])} to {max(l['rounds_done'] for l in S['leagues'])} rounds."]),
            ("Who wins where", [
                ("chart", "outcomes-big5"),
                f"Home advantage looks strongest in the {home['name']}, where the home side has won {pct(home['agg']['home_pct'])} of matches. The {by_draw[0]['name']} has the most draws, {pct(by_draw[0]['agg']['draw_pct'])} — {by_draw[0]['agg']['draws']} of {by_draw[0]['agg']['matches']}."]),
            ("Two oddities", [
                f"{nil0[0]['name']} has not had a single 0–0 in {nil0[0]['agg']['matches']} matches, and both teams have scored in {pct(btts['agg']['btts_pct'])} of {btts['name']} games, the highest share of the five.",
                f"The published schedule resumes on {nice_date(min(l['upcoming'][0]['date'] for l in S['leagues']), False)}; we will re-run these numbers when every league has at least seven rounds behind it."]),
        ],
        sources_used=[src(f"{l['source_name']} — results (2026-27/{l['id']}.1.json)", OFP, OF + f"2026-27/{l['id']}.1.json", f"Every {l['name']} result to {nice_date(l['last_date'], False)}.") for l in S["leagues"]],
        sources_investigated=[NOT_OPTA, NOT_SOFASCORE, NOT_STATSBOMB],
        cover=dict(type="bars"),
    ))

    # 3 — World Cup: how Spain won
    premise(w["champion"] == "Spain", "Spain won the World Cup")
    sp = [r for r in w["results"] if "Spain" in (r["home"], r["away"])]
    gf = sum(r["hs"] if r["home"] == "Spain" else r["as_"] for r in sp)
    ga = sum(r["as_"] if r["home"] == "Spain" else r["hs"] for r in sp)
    premise(ga == 1, "Spain conceded once")
    fin = w["final"]
    scorer = next(e for e in fin["timeline"] if e["kind"] == "goal")
    came_on = next((e for e in fin["timeline"] if e["kind"] == "sub" and e["name"].startswith(scorer["name"] + " for")), None)
    premise(came_on is not None, "the final's scorer came off the bench")
    ts = w["scorers"][0]
    hi = w["highest"]
    sf = next(r for r in w["results"] if r["round"] == "Semi-final" and "Spain" in (r["home"], r["away"]))
    premise(ts["team"] in (sf["home"], sf["away"]) and ts["team"] in (hi["home"], hi["away"]) and hi["round"] == "Match for third place",
            "the top scorer's team lost the semi-final to Spain and played the highest-scoring match, the third-place match")
    premise(max(w["by_minute"], key=lambda b: b["goals"])["label"] == "76–90+", "the World Cup's busiest quarter-hour is the last")
    premise(sum(len(g) for g in w["groups"].values()) == 48, "48 teams took part")
    out.append(dict(
        slug="how-spain-won-the-world-cup", desk="data", topic="international-news", kind="Analysis", byline="gameformative data desk", origin="data",
        title=f"How Spain won the 2026 World Cup: {gf} scored, {ga} conceded",
        standfirst="Eight matches, one goal against, and a final settled in extra time by a substitute. The tournament in numbers.",
        segments=[
            ("The path", [
                f"Spain’s World Cup began with a 0–0 against Cape Verde and ended with a 1–0 against Argentina. In between they scored {gf} goals and conceded {ga}, in eight matches.",
                ("chart", "spain-path")]),
            ("The final", [
                f"The final in New Jersey, in front of {fin['attendance']:,}, was goalless after 90 minutes. {scorer['name']}, who had come on in the {came_on['minute']}th minute, scored in the {scorer['minute']}th."]),
            ("The tournament around them", [
                f"The 48-team World Cup produced {w['goals']:,} goals in {w['matches']} matches, {w['gpg']:.2f} a game. {w['extra_time']} matches went to extra time and {w['shootouts']} were settled on penalties.",
                ("chart", "wc-stages"),
                f"The golden boot went to {ts['name']} of {ts['team']} with {ts['goals']}, whose team lost to Spain in the semi-final and then took part in the tournament’s highest-scoring match: {hi['home']} {hi['hs']}–{hi['as_']} {hi['away']} in the match for third place.",
                f"The most productive quarter-hour of the tournament was the last one: {max(w['by_minute'], key=lambda b: b['goals'])['goals']} goals came between the 76th minute and the end of normal time."]),
        ],
        sources_used=[
            src("World Cup 2026 — all matches (2026/worldcup.json)", WCP, WC + "worldcup.json", "Every result, the bracket and the stage totals."),
            src("World Cup 2026 — scorers, line-ups, attendances (2026/worldcup-full.json)", WCP, WC + "worldcup-full.json", "The final’s scorer, substitution and crowd; the scoring chart."),
        ],
        sources_investigated=[NOT_FIFA, NOT_STATSBOMB, NOT_WHOSCORED],
        cover=dict(type="final"),
    ))

    # 4 — PL 2025/26: goals by the clock
    bm = p["by_minute"]
    late = next(b for b in bm if b["label"] == "76–90+")
    premise(late["goals"] == max(b["goals"] for b in bm), "the last quarter-hour has the most goals")
    first = bm[0]
    premise(late["goals"] > 2 * first["goals"], "more than twice as many late goals as early ones")
    premise(sorted(bm, key=lambda b: -b["goals"])[1]["label"] == "31–45+", "the period before half-time is second")
    out.append(dict(
        slug="premier-league-2025-26-goals-by-minute", desk="data", topic="sport-analytics", kind="Analysis", byline="gameformative data desk", origin="data",
        title="One goal in four came after the 75th minute: the 2025/26 Premier League by the clock",
        standfirst=f"{late['goals']} of {p['goals']:,} goals arrived in the last quarter-hour of normal time, more than twice as many as in the first fifteen minutes.",
        segments=[
            ("By the clock", [
                f"Across the 380 matches of the 2025/26 Premier League, {p['goals']:,} goals were scored. Split into six periods of fifteen minutes, the distribution is anything but flat.",
                ("chart", "minutes-2526"),
                f"The last quarter-hour of normal time, including added time, produced {late['goals']} goals — {pct(100 * late['goals'] / p['goals'])} of the season’s total, against {first['goals']} in the opening fifteen minutes. The period just before half-time, including first-half added time, was second with {bm[2]['goals']}."]),
            ("Added time", [
                f"Added time alone accounts for {p['stoppage']} goals across both halves — {pct(100 * p['stoppage'] / p['goals'])} of the season’s total, scored in minutes that are not on the regulation clock. {p['pens']} goals were penalties and {p['owngoals']} were own goals."]),
            ("Who scored them", [
                ("chart", "scorers-2526"),
                f"{p['scorers'][0]['name']} finished as the league’s top scorer with {p['scorers'][0]['goals']}, {p['scorers'][0]['goals'] - p['scorers'][1]['goals']} ahead of {p['scorers'][1]['name']}, whose {p['scorers'][1]['goals']} included {p['scorers'][1]['pens']} penalties. {p['champion']} won the title with {p['table'][0]['pts']} points."]),
        ],
        sources_used=[
            src("England Premier League 2025/26 — goals and line-ups (2025-26/en.1-full.json)", OFP, OF + "2025-26/en.1-full.json", "Every goal with its minute, penalty and own-goal flags; the scorers."),
            src("English Premier League 2025/26 — results (2025-26/en.1.json)", OFP, OF + "2025-26/en.1.json", "The final table; cross-checked match by match against the full file."),
        ],
        sources_investigated=[NOT_WHOSCORED, NOT_FBREF, NOT_OPTA],
        cover=dict(type="minutes"),
    ))

    # 5 — explainer
    ppg_leader = max((r for l in S["leagues"] for r in l["table"]), key=lambda r: (r["ppg"], r["gd"]))
    out.append(dict(
        slug="how-to-read-an-early-season-table", desk="define", topic="sport-analytics", kind="Explainer", byline="gameformative data desk", origin="data",
        title="Points per game, goal difference and form: how to read a table in September",
        standfirst="Leagues that have played different numbers of rounds, teams with a game in hand, a run of five results — three tools for reading a table before it settles.",
        segments=[
            ("The problem", [
                f"In late September the tables of Europe’s big five leagues are not comparable at a glance. LaLiga has played {es['rounds_done']} rounds, the Bundesliga {de['rounds_done']}. Three simple measures help."]),
            ("Points per game", [
                f"Points divided by matches played. It puts a team with a game in hand level with everyone else, and lets you compare across leagues: {ppg_leader['name']} currently lead Europe’s big five on {ppg_leader['ppg']:.2f} points per game. Last season {p['champion']} won the Premier League on {p['table'][0]['ppg']:.2f}."]),
            ("Goal difference and tie-breakers", [
                "Goals scored minus goals conceded. On gameformative, teams level on points are ordered by goal difference, then goals scored, then name — the site’s own rule, stated on every table. Official rules differ: LaLiga and Serie A look first at the matches between the teams level on points, and Serie A settles a tie for the title or for relegation with a play-off. For teams level on points, an official table can differ from ours."]),
            ("Form", [
                "The last five results, oldest on the left, most recent on the right. We print the letter — W, D, L — in every chip and use colour only to repeat it, so the guide reads the same in black and white and for readers with colour-vision deficiency.",
                ("chart", "form-example")]),
            ("What the table cannot tell you", [
                "Our data carries results, goals, line-ups and attendances. It does not carry shots, possession or expected goals (xG); those need a licensed event-data provider. Where a figure would need that data, the page says so instead of estimating it."]),
        ],
        sources_used=[
            src("Big-five league results 2026/27 and the 2025/26 Premier League (football.json)", OFP, "https://github.com/openfootball/football.json", "Rounds played, points per game and last season’s champion; the README states what the files carry."),
            src("Criterios de desempate en LaLiga", "Flashscore España", "https://www.flashscore.es/noticias/futbol-laliga-ea-sports-como-se-decidira-el-descenso-en-caso-de-que-dos-o-mas-equipos-empaten/6aYxHRoD/", "LaLiga’s order for teams level on points: the matches between them first."),
            src("Serie A: chi vince a pari punti e in caso di classifica avulsa", "DAZN Italia", "https://www.dazn.com/it-IT/news/altro/serie-a-chi-vince-a-pari-punti-e-in-caso-di-classifica-avulsa/8pfs8lp79uto166dnjta9653g", "Serie A’s head-to-head criteria and the play-off (spareggio)."),
        ],
        sources_investigated=[
            src("La Liga: criterio de desempate en caso de igualdad de puntos", "365Scores", "https://www.365scores.com/es/news/la-liga-desempate-puntos-igualdad/", "Opened for the LaLiga rule; the page returned a server error (HTTP 500), so the Flashscore report was used instead."),
            NOT_OPTADEF,
        ],
        cover=dict(type="explainer"),
    ))
    return out


def body_chars(a):
    """The house-rule count: standfirst + every paragraph, spaces included (RULES)."""
    n = len(a["standfirst"] or "")
    for _, items in a["segments"]:
        n += sum(len(x) for x in items if isinstance(x, str))
    return n


GLOSSARY = [
    ("P", "Played — matches with a recorded result."),
    ("W · D · L", "Won, drawn, lost."),
    ("GF · GA", "Goals for (scored), goals against (conceded)."),
    ("GD", "Goal difference: GF minus GA."),
    ("Pts", "Points: three for a win, one for a draw."),
    ("PPG", "Points per game: Pts divided by P, to two decimals. Compares teams and leagues with different numbers of matches played."),
    ("Form", "The last five results, oldest on the left. The letter is always printed; colour repeats it (blue W, grey D, orange L)."),
    ("Goals per game", "All goals in a competition divided by the matches with a result. After extra time where a match had extra time; shoot-out penalties are never goals."),
    ("Home win % · Draw % · Away win %", "Share of matches with a result that ended in each outcome."),
    ("Both teams scored (BTTS)", "Share of matches in which each side scored at least once."),
    ("Clean sheet", "A match in which the team conceded no goals."),
    ("aet · pens", "After extra time; decided on penalties (shoot-out score in brackets)."),
    ("Minute buckets", "Goals grouped by the minute recorded in the source: 1–15, 16–30, 31–45 plus first-half added time, 46–60, 61–75, 76–90 plus added time, and 91–120 for extra time."),
    ("xG (expected goals)", "The probability that a shot becomes a goal, from a model trained on past shots. Not shown on gameformative yet: it needs licensed shot-level event data, which the prototype does not have."),
    ("ACWR (acute:chronic workload ratio)", "A recent training load divided by a longer-term average load, used to flag spikes. The load metric, the formula and the time windows differ between studies and vendors (Frontiers in Public Health, 2026)."),
]
