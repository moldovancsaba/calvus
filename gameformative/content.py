"""Editorial content for the gameformative prototype — one source, read by build.py.

Every article here is sample editorial copy written for the prototype by the site's data desk (no
named newsroom exists yet — 00-brief.md). No figure is typed: each number is read from
data/stats.json, which data/convert.py computes from openfootball's public-domain (CC0) results.
Where a sentence depends on the data telling a particular story ("City have won all five"), a
`premise` assert states it — so a data refresh that would make the copy untrue stops the build
instead of publishing it (04-decisions.md D7)."""

SITE = dict(
    name="gameformative",
    domain="gameformative.com",
    tagline="Football, explained by the numbers.",
    description="gameformative — football news, analysis and statistics: live tables, form, results and the numbers behind them, across Europe's big five leagues and the World Cup.",
    published="25 September 2026",
    published_iso="2026-09-25",
    byline="gameformative data desk",
)

NAV = [  # label, path from the site root, short label for the phone tab bar
    ("Home", "index.html", "Home"),
    ("Scores", "scores/index.html", "Scores"),
    ("Tables & stats", "stats/index.html", "Stats"),
    ("World Cup 2026", "world-cup-2026/index.html", "World Cup"),
    ("Analysis", "analysis/index.html", "Analysis"),
    ("How we count", "how-we-count/index.html", "Method"),
]
TABBAR = ["Home", "Scores", "Tables & stats", "Analysis"]  # + "More", the fifth tab

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


# ------------------------------------------------------------------ the articles
def articles(S):
    en, es, de, it, fr = (L(S, x) for x in ("en", "es", "de", "it", "fr"))
    p = S["pl2526"]; w = S["wc2026"]
    out = []

    # 1 — the lead: Premier League, five matchdays in
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
        slug="premier-league-five-matchdays-in",
        kind="Analysis", league="en",
        title=f"Five from five: what {lead['name']}’s perfect start does — and doesn’t — tell us",
        dek=f"{lead['pts']} points from {lead['p']} matches is the best start in the league. Last season, the team with {top5[0]} after five finished {ordinal(top5[1])}.",
        keyfacts=[
            f"{lead['name']}: {lead['w']} wins from {lead['p']}, {lead['gf']} scored, {lead['ga']} conceded.",
            f"{most['name']} have the most goals ({most['gf']}) and the biggest win of the season so far.",
            f"2025/26: {top5[2]['name']} had {top5[0]} points after five and finished {ordinal(top5[1])}; {champ5[2]['name']}, the champions, had {champ5[0]}.",
        ],
        body=[
            f"{lead['name']} have won all {lead['p']} of their Premier League matches, scoring {lead['gf']} and conceding {lead['ga']}. That is {lead['pts']} points, the maximum available, and {lead['pts'] - second['pts']} clear of {second['name']} in second.",
            f"The league’s most productive attack belongs to someone else. {most['name']} have scored {most['gf']} — the most of any side — and recorded the biggest win of the season so far, {big['hs']}–{big['as_']} at {big['home'] if most['code'] == big['away'] else big['away']} on {nice_date(big['date'], False)}.",
            ("chart", "race-en"),
            "## Why five matches is not a verdict",
            f"Last season’s table is the warning. After five matchdays of 2025/26, {top5[2]['name']} had {top5[0]} points — more than anyone — and finished {ordinal(top5[1])} on {p['table'][top5[1] - 1]['pts']}. {champ5[2]['name']}, who won the title with {p['table'][0]['pts']}, had {champ5[0]} at the same stage.",
            ("chart", "after5-2526"),
            f"The league as a whole is also running hot on a small sample. {en['agg']['matches']} matches in, it has averaged {en['agg']['gpg']:.2f} goals a game, against {last_full['gpg']:.2f} across all 380 of last season, and {pct(en['agg']['draw_pct'])} of matches have been drawn, against {pct(last_full['draw_pct'])} over the full campaign.",
            f"At the other end, {bottom[0]['name']} and {bottom[1]['name']} have {bottom[0]['pts']} and {bottom[1]['pts']} points and are still looking for a first win. The next round is scheduled for {nice_date(en['upcoming'][0]['date'], False)}.",
        ],
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
        slug="big-five-first-month",
        kind="Analysis", league="all",
        title=f"Europe’s big five after a month: the {by_gpg[0]['name']} scores most, the {by_draw[0]['name']} draws most",
        dek=f"{by_gpg[0]['agg']['gpg']:.2f} goals a game in Germany, {by_gpg[-1]['agg']['gpg']:.2f} in England — and not a single goalless draw yet in {nil0[0]['name']}.",
        keyfacts=[
            "Goals per game: " + ", ".join(f"{l['name']} {l['agg']['gpg']:.2f}" for l in by_gpg) + ".",
            f"Home wins are most common in the {home['name']} ({pct(home['agg']['home_pct'])} of matches).",
            f"{nil0[0]['name']}: 0 goalless draws in {nil0[0]['agg']['matches']} matches.",
        ],
        body=[
            f"A month into the season, Europe’s five biggest leagues have produced {sum(l['agg']['goals'] for l in S['leagues'])} goals in {sum(l['agg']['matches'] for l in S['leagues'])} matches. They have not produced them evenly.",
            ("chart", "gpg-big5"),
            f"The {by_gpg[0]['name']} leads at {by_gpg[0]['agg']['gpg']:.2f} goals a game, helped by results such as {by_gpg[0]['agg']['biggest']['home']} {by_gpg[0]['agg']['biggest']['hs']}–{by_gpg[0]['agg']['biggest']['as_']} {by_gpg[0]['agg']['biggest']['away']}. The {by_gpg[-1]['name']} is lowest at {by_gpg[-1]['agg']['gpg']:.2f}. The gap is real in this sample, but the samples are small and uneven: between {min(l['agg']['matches'] for l in S['leagues'])} and {max(l['agg']['matches'] for l in S['leagues'])} matches per league, because the leagues have played between {min(l['rounds_done'] for l in S['leagues'])} and {max(l['rounds_done'] for l in S['leagues'])} rounds.",
            "## Who wins where",
            ("chart", "outcomes-big5"),
            f"Home advantage looks strongest in the {home['name']}, where the home side has won {pct(home['agg']['home_pct'])} of matches. The {by_draw[0]['name']} has the most draws, {pct(by_draw[0]['agg']['draw_pct'])} — {by_draw[0]['agg']['draws']} of {by_draw[0]['agg']['matches']}.",
            f"Two smaller oddities: {nil0[0]['name']} has not had a single 0–0 in {nil0[0]['agg']['matches']} matches, and both teams have scored in {pct(btts['agg']['btts_pct'])} of {btts['name']} games, the highest share of the five.",
            f"The published schedule resumes on {nice_date(min(l['upcoming'][0]['date'] for l in S['leagues']), False)}; we will re-run these numbers when every league has at least seven rounds behind it.",
        ],
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
    out.append(dict(
        slug="how-spain-won-the-world-cup",
        kind="Analysis", league="wc",
        title=f"How Spain won the 2026 World Cup: {gf} scored, {ga} conceded",
        dek=f"Eight matches, one goal against, and a final settled in extra time by a substitute. The tournament in numbers.",
        keyfacts=[
            f"Spain: {len(sp)} matches, {gf} goals scored, {ga} conceded.",
            f"Final: Spain {fin['row']['hs']}–{fin['row']['as_']} Argentina after extra time; {scorer['name']} {scorer['minute']}′, on as a substitute in the {came_on['minute']}th minute.",
            f"Tournament: {w['goals']:,} goals in {w['matches']} matches ({w['gpg']:.2f} a game); top scorer {ts['name']} ({ts['team']}), {ts['goals']}.",
        ],
        body=[
            f"Spain’s World Cup began with a 0–0 against Cape Verde and ended with a 1–0 against Argentina. In between they scored {gf} goals and conceded {ga}, in eight matches.",
            ("chart", "spain-path"),
            f"The final in New Jersey, in front of {fin['attendance']:,}, was goalless after 90 minutes. {scorer['name']}, who had come on in the {came_on['minute']}th minute, scored in the {scorer['minute']}th.",
            "## The tournament around them",
            f"The first 48-team World Cup produced {w['goals']:,} goals in {w['matches']} matches, {w['gpg']:.2f} a game. {w['extra_time']} matches went to extra time and {w['shootouts']} were settled on penalties.",
            ("chart", "wc-stages"),
            f"The golden boot went to {ts['name']} of {ts['team']} with {ts['goals']}, whose team lost to Spain in the semi-final and then took part in the tournament’s highest-scoring match: {hi['home']} {hi['hs']}–{hi['as_']} {hi['away']} in the match for third place.",
            f"The most productive quarter-hour of the tournament was the last one: {max(w['by_minute'], key=lambda b: b['goals'])['goals']} goals came between the 76th minute and the end of normal time.",
        ],
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
        slug="premier-league-2025-26-goals-by-minute",
        kind="Analysis", league="en",
        title=f"One goal in four came after the 75th minute: the 2025/26 Premier League by the clock",
        dek=f"{late['goals']} of {p['goals']:,} goals arrived in the last quarter-hour of normal time, more than twice as many as in the first fifteen minutes.",
        keyfacts=[
            f"{late['goals']} goals from the 76th minute to the final whistle ({pct(100 * late['goals'] / p['goals'])}).",
            f"{p['stoppage']} goals in added time, at the end of either half.",
            f"{p['pens']} penalties scored, {p['owngoals']} own goals.",
        ],
        body=[
            f"Across the 380 matches of the 2025/26 Premier League, {p['goals']:,} goals were scored. Split into six periods of fifteen minutes, the distribution is anything but flat.",
            ("chart", "minutes-2526"),
            f"The last quarter-hour of normal time, including added time, produced {late['goals']} goals — {pct(100 * late['goals'] / p['goals'])} of the season’s total, against {first['goals']} in the opening fifteen minutes. The period just before half-time, including first-half added time, was second with {bm[2]['goals']}.",
            f"Added time alone accounts for {p['stoppage']} goals across both halves — {pct(100 * p['stoppage'] / p['goals'])} of the season’s total, scored in minutes that are not on the regulation clock.",
            "## Who scored them",
            ("chart", "scorers-2526"),
            f"{p['scorers'][0]['name']} finished as the league’s top scorer with {p['scorers'][0]['goals']}, {p['scorers'][0]['goals'] - p['scorers'][1]['goals']} ahead of {p['scorers'][1]['name']}, whose {p['scorers'][1]['goals']} included {p['scorers'][1]['pens']} penalties. {p['champion']} won the title with {p['table'][0]['pts']} points.",
        ],
        cover=dict(type="minutes"),
    ))

    # 5 — explainer
    ppg_leader = max((r for l in S["leagues"] for r in l["table"]), key=lambda r: (r["ppg"], r["gd"]))
    out.append(dict(
        slug="how-to-read-an-early-season-table",
        kind="Explainer", league="all",
        title="Points per game, goal difference and form: how to read a table in September",
        dek="Leagues that have played different numbers of rounds, teams with a game in hand, a run of five results — three tools for reading a table before it settles.",
        keyfacts=[
            "Points per game (PPG) compares teams and leagues that have played different numbers of matches.",
            "Goal difference separates teams level on points on this site; official tie-breakers vary by league.",
            "Form shows the last five results, most recent on the right, with the letter always printed.",
        ],
        body=[
            f"In late September the tables of Europe’s big five leagues are not comparable at a glance. LaLiga has played {es['rounds_done']} rounds, the Bundesliga {de['rounds_done']}. Three simple measures help.",
            "## Points per game",
            f"Points divided by matches played. It puts a team with a game in hand level with everyone else, and lets you compare across leagues: {ppg_leader['name']} currently lead Europe’s big five on {ppg_leader['ppg']:.2f} points per game. Last season {p['champion']} won the Premier League on {p['table'][0]['ppg']:.2f}.",
            "## Goal difference",
            "Goals scored minus goals conceded. On gameformative, teams level on points are ordered by goal difference, then goals scored, then name. That is the site’s own rule, stated on every table: LaLiga and Serie A use head-to-head results first, so an official table can differ from ours for teams level on points.",
            "## Form",
            "The last five results, oldest on the left, most recent on the right. We print the letter — W, D, L — in every chip and use colour only to repeat it, so the guide reads the same in black and white and for readers with colour-vision deficiency.",
            ("chart", "form-example"),
            "## What the table cannot tell you",
            "Our data carries results, goals, line-ups and attendances. It does not carry shots, possession or expected goals (xG); those need a licensed event-data provider. Where a figure would need that data, the page says so instead of estimating it.",
        ],
        cover=dict(type="explainer"),
    ))
    return out


# ------------------------------------------------------------------ home "numbers of the week"
def numbers(S):
    by_gpg = max(S["leagues"], key=lambda l: l["agg"]["gpg"])
    teams = [(r, l) for l in S["leagues"] for r in l["table"]]
    top_att = max(teams, key=lambda x: (x[0]["gf"] / x[0]["p"], x[0]["gf"]))
    tight = min(teams, key=lambda x: (x[0]["ga"] / x[0]["p"], -x[0]["p"]))
    nil0 = min(S["leagues"], key=lambda l: (l["agg"]["nil_nil"], -l["agg"]["matches"]))
    return [
        dict(n=f"{by_gpg['agg']['gpg']:.2f}", unit="", what=f"goals per game in the {by_gpg['name']}", ctx=f"The most of Europe’s big five, from {by_gpg['agg']['matches']} matches.", href=f"stats/{by_gpg['slug']}.html", accent=True),
        dict(n=str(top_att[0]["gf"]), unit="goals", what=f"{top_att[0]['name']} in {top_att[0]['p']} {top_att[1]['name']} matches", ctx=f"{top_att[0]['gf'] / top_att[0]['p']:.2f} a game — the best rate in the big five.", href=f"stats/{top_att[1]['slug']}.html"),
        dict(n=str(tight[0]["ga"]), unit="conceded", what=f"{tight[0]['name']} in {tight[0]['p']} {tight[1]['name']} matches", ctx="The meanest defence in the big five, per game.", href=f"stats/{tight[1]['slug']}.html"),
        dict(n=str(nil0["agg"]["nil_nil"]), unit="", what=f"goalless draws in {nil0['name']}", ctx=f"In {nil0['agg']['matches']} matches so far this season.", href=f"stats/{nil0['slug']}.html"),
    ]


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
]
