#!/usr/bin/env python3
"""raw/*.json (openfootball, CC0) → stats.json:  python3 gameformative/data/convert.py
Deterministic: the same raw files always give the same stats.json, byte for byte. Every derived
figure on the site comes from here; nothing is typed by hand. The asserts below are the data gate —
the build stops rather than publishing a table that does not add up."""
import json, hashlib, pathlib, re, sys, unicodedata
from collections import defaultdict, Counter
from teams import CLUBS, PL_FULL_ALIASES, NATIONS, WC_FULL_ALIASES

HERE = pathlib.Path(__file__).parent
RAW = HERE / "raw"

LEAGUES = [  # id, source file, display name, country, slug
    ("en", "2026-27_en.1.json", "Premier League", "England", "premier-league"),
    ("es", "2026-27_es.1.json", "LaLiga", "Spain", "laliga"),
    ("de", "2026-27_de.1.json", "Bundesliga", "Germany", "bundesliga"),
    ("it", "2026-27_it.1.json", "Serie A", "Italy", "serie-a"),
    ("fr", "2026-27_fr.1.json", "Ligue 1", "France", "ligue-1"),
]


def load(name):
    return json.loads((RAW / name).read_text(encoding="utf-8"))


def sha(name):
    return hashlib.sha256((RAW / name).read_bytes()).hexdigest()[:16]


def ft(m):
    """Full-time score as [home, away], or None when the match has no result yet. The 2026/27
    files write some results as a bare [h, a] list instead of {"ft": [h, a]} — both are read."""
    s = m.get("score")
    if isinstance(s, dict) and s.get("ft"):
        return list(s["ft"])
    if isinstance(s, list) and len(s) == 2 and all(isinstance(x, int) for x in s):
        return list(s)
    return None


def final_score(m):
    """Score after extra time where there was extra time (the 'et' figure is cumulative)."""
    s = m["score"]
    return list(s["et"]) if isinstance(s, dict) and "et" in s else ft(m)


def rnum(r):
    m = re.search(r"(\d+)$", r)
    assert m, f"round without a number: {r}"
    return int(m.group(1))


def club(name):
    assert name in CLUBS, f"team missing from teams.py: {name!r}"
    return CLUBS[name]


def blank():
    return dict(p=0, w=0, d=0, l=0, gf=0, ga=0, pts=0)


def add(row, gf, ga):
    row["p"] += 1; row["gf"] += gf; row["ga"] += ga
    if gf > ga: row["w"] += 1; row["pts"] += 3
    elif gf == ga: row["d"] += 1; row["pts"] += 1
    else: row["l"] += 1


def table(matches, names, codes):
    """League table ordered by points, goal difference, goals scored, then name — the site's own
    order, stated on the methodology page; official tie-breakers differ by competition."""
    rows = {t: dict(team=t, name=names[t], code=codes[t], **blank(), home=blank(), away=blank(), cs=0, fts=0, form=[]) for t in names}
    for m in sorted(matches, key=lambda m: (m["date"], m.get("time", ""))):
        s = ft(m)
        if not s: continue
        h, a = m["team1"], m["team2"]
        add(rows[h], s[0], s[1]); add(rows[h]["home"], s[0], s[1])
        add(rows[a], s[1], s[0]); add(rows[a]["away"], s[1], s[0])
        rows[h]["cs"] += s[1] == 0; rows[a]["cs"] += s[0] == 0
        rows[h]["fts"] += s[0] == 0; rows[a]["fts"] += s[1] == 0
        for t, o, gf, ga, ha in ((h, a, s[0], s[1], "H"), (a, h, s[1], s[0], "A")):
            rows[t]["form"].append(dict(r="W" if gf > ga else "D" if gf == ga else "L", opp=codes[o], score=f"{gf}–{ga}", ha=ha, date=m["date"]))
    out = sorted(rows.values(), key=lambda r: (-r["pts"], -(r["gf"] - r["ga"]), -r["gf"], r["name"]))
    for i, r in enumerate(out, 1):
        r["pos"] = i; r["gd"] = r["gf"] - r["ga"]
        r["ppg"] = round(r["pts"] / r["p"], 2) if r["p"] else 0.0
        r["form"] = r["form"][-5:]
    return out


def aggregates(matches, codes):
    played = [m for m in matches if ft(m)]
    n = len(played)
    goals = sum(sum(ft(m)) for m in played)
    hw = sum(ft(m)[0] > ft(m)[1] for m in played)
    dr = sum(ft(m)[0] == ft(m)[1] for m in played)
    aw = n - hw - dr
    btts = sum(min(ft(m)) > 0 for m in played)
    nil = sum(sum(ft(m)) == 0 for m in played)

    def rec(m):
        s = ft(m)
        return dict(date=m["date"], home=codes[m["team1"]], away=codes[m["team2"]], hs=s[0], as_=s[1])
    biggest = max(played, key=lambda m: (abs(ft(m)[0] - ft(m)[1]), sum(ft(m)), m["date"]))
    highest = max(played, key=lambda m: (sum(ft(m)), m["date"]))
    pct = lambda x: round(100 * x / n, 1) if n else 0.0
    return dict(matches=n, goals=goals, gpg=round(goals / n, 2) if n else 0.0,
                home_w=hw, draws=dr, away_w=aw, home_pct=pct(hw), draw_pct=pct(dr), away_pct=pct(aw),
                btts=btts, btts_pct=pct(btts), nil_nil=nil, biggest=rec(biggest), highest=rec(highest))


def race(matches, names, codes, teams_to_show, last_round):
    pts = {t: [0] * last_round for t in names}
    for m in matches:
        s = ft(m)
        if not s: continue
        r = rnum(m["round"])
        if r > last_round: continue
        for t, gf, ga in ((m["team1"], s[0], s[1]), (m["team2"], s[1], s[0])):
            pts[t][r - 1] += 3 if gf > ga else 1 if gf == ga else 0
    series = []
    for t in teams_to_show:
        acc, run = 0, []
        for p in pts[t]:
            acc += p; run.append(acc)
        series.append(dict(code=codes[t], name=names[t], points=run))
    return dict(rounds=last_round, series=series)


def match_row(m, codes):
    s = ft(m)
    return dict(date=m["date"], time=m.get("time", ""), round=m["round"],
                home=m["team1"], away=m["team2"], hcode=codes[m["team1"]], acode=codes[m["team2"]],
                hname=CLUBS[m["team1"]][0], aname=CLUBS[m["team2"]][0],
                hs=s[0] if s else None, as_=s[1] if s else None)


def league(lid, fname, disp, country, slug):
    d = load(fname)
    ms = d["matches"]
    teams = sorted({m[k] for m in ms for k in ("team1", "team2")})
    names = {t: club(t)[0] for t in teams}
    codes = {t: club(t)[1] for t in teams}
    assert len(set(codes.values())) == len(codes), f"{lid}: duplicate team code"
    assert len(ms) == len(teams) * (len(teams) - 1), f"{lid}: fixture count {len(ms)} is not a double round robin"
    played = [m for m in ms if ft(m)]
    tbl = table(ms, names, codes)
    # the data gate: a table that does not add up is never published
    assert sum(r["gf"] for r in tbl) == sum(r["ga"] for r in tbl), f"{lid}: goals for ≠ goals against"
    assert sum(r["p"] for r in tbl) == 2 * len(played), f"{lid}: games played ≠ 2 × results"
    dr = sum(ft(m)[0] == ft(m)[1] for m in played)
    assert sum(r["pts"] for r in tbl) == 3 * (len(played) - dr) + 2 * dr, f"{lid}: points do not reconcile"
    last_date = max(m["date"] for m in played)
    rounds_done = max(rnum(m["round"]) for m in played)
    latest = [match_row(m, codes) for m in ms if rnum(m["round"]) == rounds_done]
    latest.sort(key=lambda r: (r["date"], r["time"], r["hname"]))
    upcoming = sorted((m for m in ms if not ft(m) and m["date"] > last_date), key=lambda m: (m["date"], m.get("time", ""), m["team1"]))
    postponed = sorted((m for m in ms if not ft(m) and m["date"] <= last_date), key=lambda m: m["date"])
    top = [r["team"] for r in tbl[:6]]
    return dict(id=lid, slug=slug, name=disp, country=country, source_name=d["name"], file=fname,
                fixtures=len(ms), played=len(played), last_date=last_date, rounds_done=rounds_done,
                teams=len(teams), table=tbl, latest_round=f"Matchday {rounds_done}", latest=latest,
                upcoming=[match_row(m, codes) for m in upcoming[:10]],
                unplayed_before_cutoff=[match_row(m, codes) for m in postponed],
                agg=aggregates(ms, codes), race=race(ms, names, codes, top, rounds_done))


# ------------------------------------------------------------------ scorer names
def display_name(n):
    """The -full files mix 'Hugo EKITIKE', 'MOHAMED SALAH' and 'Federico Chiesa'. Any all-caps
    word is set in title case; accents the source dropped in caps are not restored."""
    return " ".join(w.capitalize() if w.isupper() and len(w) > 1 else w for w in n.split())


def name_key(n):
    s = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().casefold()
    return re.sub(r"[^a-z ]", "", s).strip()


def minute(mn):
    base, _, extra = str(mn).partition("+")
    return int(base), int(extra or 0)


BUCKETS = [("1–15", 1, 15), ("16–30", 16, 30), ("31–45+", 31, 45), ("46–60", 46, 60), ("61–75", 61, 75), ("76–90+", 76, 90), ("91–120", 91, 120)]


def bucket(mn):
    b, _ = minute(mn)
    for label, lo, hi in BUCKETS:
        if lo <= b <= hi: return label
    raise AssertionError(f"minute out of range: {mn}")


def check_goal_lists(m, where):
    sc = final_score(m)
    g1, g2 = m.get("goals1"), m.get("goals2")
    if g1 is None and g2 is None:
        assert sc == [0, 0], f"{where}: no goal list for {m['team1']}–{m['team2']} {sc}"
        return
    assert [len(g1), len(g2)] == sc, f"{where}: goal list {len(g1)}–{len(g2)} ≠ score {sc} for {m['team1']}–{m['team2']} {m['date']}"


def scorers(ms, team_of, where):
    tally, disp, teamname, pens = Counter(), {}, {}, Counter()
    for m in ms:
        check_goal_lists(m, where)
        for side, t in (("goals1", m["team1"]), ("goals2", m["team2"])):
            for g in m.get(side, []):
                if g.get("owngoal"): continue
                k = (name_key(g["name"]), team_of(t))
                tally[k] += 1; pens[k] += bool(g.get("penalty"))
                disp.setdefault(k, display_name(g["name"])); teamname[k] = team_of(t)
    rows = [dict(name=disp[k], team=teamname[k], goals=v, pens=pens[k]) for k, v in tally.items()]
    rows.sort(key=lambda r: (-r["goals"], r["pens"], r["name"]))
    return rows


def pl_2526():
    base = load("2025-26_en.1.json")["matches"]
    full = load("2025-26_en.1-full.json")["matches"]
    assert len(base) == len(full) == 380
    for m in full:
        for k in ("team1", "team2"):
            assert m[k] in PL_FULL_ALIASES, f"PL 2025/26 full: unmapped team {m[k]!r}"
    # cross-check the two files match by match: same date, same teams, same full-time score
    a = Counter((m["date"], m["team1"], m["team2"], tuple(ft(m))) for m in base)
    b = Counter((m["date"], PL_FULL_ALIASES[m["team1"]], PL_FULL_ALIASES[m["team2"]], tuple(ft(m))) for m in full)
    assert a == b, f"PL 2025/26: the two source files disagree on {sum((a - b).values())} matches"
    teams = sorted({m[k] for m in base for k in ("team1", "team2")})
    names = {t: club(t)[0] for t in teams}; codes = {t: club(t)[1] for t in teams}
    tbl = table(base, names, codes)
    assert all(r["p"] == 38 for r in tbl), "PL 2025/26: not every team has 38 games"
    assert sum(r["gf"] for r in tbl) == sum(r["ga"] for r in tbl)
    team_of = lambda t: CLUBS[PL_FULL_ALIASES[t]][0]
    sc = scorers(full, team_of, "PL 2025/26")
    goals = sum(sum(ft(m)) for m in base)
    evs = [g for m in full for s in ("goals1", "goals2") for g in m.get(s, [])]
    assert len(evs) == goals, f"PL 2025/26: {len(evs)} goal events ≠ {goals} goals"
    by_min = Counter(bucket(g["minute"]) for g in evs)
    att = [(m["attendance"], m) for m in full]
    top_att = max(att, key=lambda x: (x[0], x[1]["date"]))
    champ = tbl[0]["team"]
    rc = race(base, names, codes, [r["team"] for r in tbl], 38)
    return dict(table=tbl, agg=aggregates(base, codes), race=rc, scorers=sc[:15],
                scorers_total=len(sc), goals=goals, pens=sum(bool(g.get("penalty")) for g in evs),
                owngoals=sum(bool(g.get("owngoal")) for g in evs),
                by_minute=[dict(label=l, goals=by_min.get(l, 0)) for l, _, _ in BUCKETS[:6]],
                stoppage=sum(minute(g["minute"])[1] > 0 for g in evs),
                attendance=dict(total=sum(x for x, _ in att), avg=round(sum(x for x, _ in att) / len(att)),
                                top=dict(n=top_att[0], ground=top_att[1]["ground"], date=top_att[1]["date"],
                                         home=names[PL_FULL_ALIASES[top_att[1]["team1"]]], away=names[PL_FULL_ALIASES[top_att[1]["team2"]]])),
                champion=names[champ], champion_after5=rc["series"][0]["points"][4])


# ------------------------------------------------------------------ World Cup 2026
def winner(m):
    s = m["score"]
    for k in ("p", "et", "ft"):
        if k in s and s[k][0] != s[k][1]:
            return m["team1"] if s[k][0] > s[k][1] else m["team2"]
    raise AssertionError(f"knock-out match without a winner: {m['team1']}–{m['team2']}")


def wc_row(m):
    s = m["score"]
    how = "pens" if "p" in s else "aet" if "et" in s else ""
    fs = final_score(m)
    return dict(date=m["date"], round=m["round"], home=m["team1"], away=m["team2"],
                hcode=NATIONS[m["team1"]], acode=NATIONS[m["team2"]], hs=fs[0], as_=fs[1],
                pens=s.get("p"), how=how, ground=m.get("ground", ""), num=m.get("num"),
                group=m.get("group", "").replace("Group ", ""),
                winner=winner(m) if not m.get("group") else None)


def world_cup():
    ms = load("wc2026_worldcup.json")["matches"]
    full = load("wc2026_worldcup-full.json")["matches"]
    assert len(ms) == len(full) == 104
    for m in full:
        for k in ("team1", "team2"):
            m[k] = WC_FULL_ALIASES.get(m[k], m[k])
    for m in ms + full:
        for k in ("team1", "team2"):
            assert m[k] in NATIONS, f"World Cup: nation missing from teams.py: {m[k]!r}"
    a = Counter((m["date"], m["team1"], m["team2"], tuple(final_score(m))) for m in ms)
    b = Counter((m["date"], m["team1"], m["team2"], tuple(final_score(m))) for m in full)
    assert a == b, "World Cup: the two source files disagree"
    groups = defaultdict(list)
    for m in ms:
        if m.get("group"): groups[m["group"]].append(m)
    assert len(groups) == 12 and all(len(v) == 6 for v in groups.values()), "World Cup: expected 12 groups of 6 matches"
    ko = [m for m in ms if not m.get("group")]
    rounds = ["Round of 32", "Round of 16", "Quarter-final", "Semi-final", "Match for third place", "Final"]
    assert Counter(m["round"] for m in ko) == Counter({"Round of 32": 16, "Round of 16": 8, "Quarter-final": 4, "Semi-final": 2, "Match for third place": 1, "Final": 1})
    r32_teams = {m[k] for m in ko if m["round"] == "Round of 32" for k in ("team1", "team2")}
    assert len(r32_teams) == 32
    gtables = {}
    for g in sorted(groups):
        teams = sorted({m[k] for m in groups[g] for k in ("team1", "team2")})
        assert len(teams) == 4
        names = {t: t for t in teams}; codes = {t: NATIONS[t] for t in teams}
        t = table(groups[g], names, codes)
        for r in t: r["through"] = r["team"] in r32_teams; r.pop("home"); r.pop("away"); r.pop("form")
        gtables[g.replace("Group ", "")] = t
    # bracket order: walk back from the final, so each round lists its matches in tree order
    by_round = {r: [m for m in ko if m["round"] == r] for r in rounds}
    def feeders(m, prev):
        out = []
        for t in (m["team1"], m["team2"]):
            src = [p for p in by_round[prev] if winner(p) == t]
            assert len(src) == 1, f"bracket: {t} has {len(src)} feeder matches in {prev}"
            out.append(src[0])
        return out
    order = {"Final": by_round["Final"]}
    chain = ["Final", "Semi-final", "Quarter-final", "Round of 16", "Round of 32"]
    for cur, prev in zip(chain, chain[1:]):
        order[prev] = [f for m in order[cur] for f in feeders(m, prev)]
    bracket = [dict(round=r, matches=[wc_row(m) for m in order[r]]) for r in reversed(chain)]
    goals = sum(sum(final_score(m)) for m in ms)
    stage_goals = []
    for label, sel in (("Group stage", lambda m: bool(m.get("group"))),) + tuple((r, (lambda r: lambda m: m["round"] == r)(r)) for r in rounds):
        sm = [m for m in ms if sel(m)]
        g = sum(sum(final_score(m)) for m in sm)
        stage_goals.append(dict(stage=label, matches=len(sm), goals=g, gpg=round(g / len(sm), 2)))
    sc = scorers(full, lambda t: t, "World Cup")
    evs = [g for m in full for s in ("goals1", "goals2") for g in m.get(s, [])]
    assert len(evs) == goals, f"World Cup: {len(evs)} goal events ≠ {goals} goals"
    fin_full = next(m for m in full if m["round"] == "Final")
    fin = next(m for m in ms if m["round"] == "Final")
    lineups = []
    for side, t in zip(fin_full["lineup"], (fin_full["team1"], fin_full["team2"])):
        lineups.append(dict(team=t, code=NATIONS[t],
                            starters=[dict(name=display_name(p["name"]), captain=bool(p.get("captain"))) for p in side["starter"]],
                            subs=[dict(on=display_name(s["on"]), off=display_name(s["off"]), minute=s["minute"]) for s in side.get("subs", [])]))
    timeline = []
    for side, t in (("goals1", fin_full["team1"]), ("goals2", fin_full["team2"])):
        for g in fin_full.get(side, []):
            timeline.append(dict(minute=g["minute"], team=t, code=NATIONS[t], name=display_name(g["name"]), kind="goal", pen=bool(g.get("penalty")), og=bool(g.get("owngoal"))))
    for s_side, t in zip(fin_full["lineup"], (fin_full["team1"], fin_full["team2"])):
        for s in s_side.get("subs", []):
            timeline.append(dict(minute=s["minute"], team=t, code=NATIONS[t], name=f"{display_name(s['on'])} for {display_name(s['off'])}", kind="sub"))
    timeline.sort(key=lambda e: (minute(e["minute"]), e["kind"] != "goal"))
    att = [m["attendance"] for m in full]
    ex = sum("et" in m["score"] for m in ms); pens = sum("p" in m["score"] for m in ms)
    results = [wc_row(m) for m in sorted(ms, key=lambda m: (m["date"], m.get("time", ""), m["team1"]))]
    highest = max(results, key=lambda r: (r["hs"] + r["as_"], r["date"]))
    return dict(matches=len(ms), goals=goals, results=results, highest=highest, gpg=round(goals / len(ms), 2), groups=gtables,
                bracket=bracket, third=wc_row(by_round["Match for third place"][0]),
                stage_goals=stage_goals, scorers=sc[:12], scorers_total=len(sc),
                pens_scored=sum(bool(g.get("penalty")) for g in evs), owngoals=sum(bool(g.get("owngoal")) for g in evs),
                extra_time=ex, shootouts=pens, attendance=dict(total=sum(att), avg=round(sum(att) / len(att))),
                champion=winner(fin), runner_up=fin["team2"] if winner(fin) == fin["team1"] else fin["team1"],
                final=dict(row=wc_row(fin), ground=fin_full["ground"], attendance=fin_full["attendance"],
                           ht=fin["score"]["ht"], ft=fin["score"]["ft"], et=fin["score"].get("et"),
                           lineups=lineups, timeline=timeline),
                by_minute=[dict(label=l, goals=c) for l, c in ((l, sum(bucket(g["minute"]) == l for g in evs)) for l, _, _ in BUCKETS)])


if __name__ == "__main__":
    files = sorted(p.name for p in RAW.glob("*.json"))
    out = dict(source="openfootball football.json and worldcup.json — CC0 1.0 public domain",
               inputs={f: sha(f) for f in files},
               leagues=[league(*L) for L in LEAGUES], pl2526=pl_2526(), wc2026=world_cup())
    out["data_to"] = max(l["last_date"] for l in out["leagues"])
    text = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    if "--check" in sys.argv:
        same = (HERE / "stats.json").read_text(encoding="utf-8") == text
        print("stats.json reproduces from raw/" if same else "stats.json DIFFERS from a fresh conversion of raw/")
        sys.exit(0 if same else 1)
    (HERE / "stats.json").write_text(text, encoding="utf-8")
    for l in out["leagues"]:
        print(f"{l['name']:15s} {l['played']:3d}/{l['fixtures']} results to {l['last_date']} (matchday {l['rounds_done']}), {l['agg']['goals']} goals, {len(l['unplayed_before_cutoff'])} unplayed before cut-off")
    p = out["pl2526"]; w = out["wc2026"]
    print(f"PL 2025/26      champion {p['champion']}, {p['goals']} goals, top scorer {p['scorers'][0]['name']} {p['scorers'][0]['goals']}")
    print(f"World Cup 2026  champion {w['champion']}, {w['matches']} matches, {w['goals']} goals, top scorer {w['scorers'][0]['name']} {w['scorers'][0]['goals']}")
    print(f"stats.json      {len(text.encode()):,} bytes, data to {out['data_to']}")
