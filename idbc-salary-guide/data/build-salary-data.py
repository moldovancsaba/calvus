# -*- coding: utf-8 -*-
"""Rebuild the salary half of guide-data.json from the client's IDBC_bertabla sheet.

    python3 idbc-salary-guide/data/build-salary-data.py <IDBC_bertabla.xlsx> [<Talent_Insight_riport.xlsx>]

The LinkedIn Talent Insight counts live in the sheet itself since 2026-09-21: column
`linkedin_talent_insight` on WEB_BERTABLA_IMPORT (TOP3 rows) and on EXPERT_POOL_IMPORT, with
`talent_insight_pozicio` naming the report's own label where it differs. The second argument —
the separate Talent Insight workbook — is only needed for a sheet that predates those columns.
The survey half (topics, datasets) is left untouched — that comes from build-guide-data.py.
Sheet: 1aQA6Kw5k1U9LQMiWYgcn__m2YCuGmEhx79QFSzE0hJg (File → Download → xlsx, or the export URL).
"""
import io, json, re, sys, unicodedata
import openpyxl

BERTABLA, TALENT = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else None)
OUT = __file__.rsplit("/", 1)[0] + "/guide-data.json"

# The Bérek page's own area taxonomy and display order (client feedback, 2026-09-22) —
# deliberately different wording from Piaci trendek's separate area list in places (e.g.
# "Pénzügy és számvitel" vs. "Pénzügy, Számvitel", "Office Support" vs. its own Office Support
# wording); do not reconcile the two, they are verified as intentionally separate.
CANONICAL_AREAS = [
    "IT",
    # "IT Contracting" is a verified real data gap, not a bug: the bértábla sheet has no rows for
    # it today (only the separate market-trends survey data carries it as a segment). Kept here so
    # the code is ready for it; with no sheet row mapped to it, it will simply never appear in the
    # rendered <select> (zero matching rows) until the client supplies IT Contracting salary
    # figures, or confirms the segment is already folded into "IT".
    "IT Contracting",
    "SAP", "Pénzügy és számvitel", "Sales", "Marketing", "HR", "Retail", "Office Support",
    "Business Service Center (BSC)", "Logisztika, Szállítás", "Gyártás, Termelés, Mérnökség",
    "Építőipar, Ingatlan", "Pharma, Life Sciences",
]
AREA_ORDER = CANONICAL_AREAS  # display order of the Bérek filter

def _norm(s):
    return " ".join(str(s).split()).casefold()

# The sheet's own `terulet` column held short internal codes (BSC, PENZUGY, GYARTAS, ...) through
# 2026-09-24. On 2026-09-25 the client's sheet was found to hold the site's own full display text
# instead — apparently retyped by hand to match what shipped, not a deliberate format change asked
# for — which broke this converter outright (it asserted on six "unmapped" areas). Every raw value
# a sync might ever see is normalized here rather than assumed to be one format or the other: a
# case/whitespace-insensitive match against the canonical text needs no entry below at all; the
# entries below are for the old short codes and for small spelling drift caught in the wild.
AREA_ALIASES = {
    "BSC": "Business Service Center (BSC)",
    "PENZUGY": "Pénzügy és számvitel",
    "LOGISZTIKA": "Logisztika, Szállítás",
    "GYARTAS": "Gyártás, Termelés, Mérnökség",
    "CP": "Építőipar, Ingatlan",
    "PHARMA": "Pharma, Life Sciences",
    "IT_CONTRACTING": "IT Contracting",
    "Pharma, Life Science": "Pharma, Life Sciences",  # sheet had the singular, 2026-09-25
    "Pénzügy és Számvitel": "Pénzügy és számvitel",  # sheet had this casing, 2026-09-25
}
AREA_LOOKUP = {_norm(a): a for a in CANONICAL_AREAS}
for raw, canon in AREA_ALIASES.items():
    AREA_LOOKUP[_norm(raw)] = canon

def area_name(raw):
    """The sheet's raw `terulet` value -> the canonical display name, or None if genuinely
    unrecognized (a real new area needs a CANONICAL_AREAS/AREA_ALIASES entry, not a guess)."""
    return AREA_LOOKUP.get(_norm(raw))

# Talent Insight area label -> the canonical area name (see CANONICAL_AREAS above).
TI_AREA = {
    "BSC": "Business Service Center (BSC)", "Finance": "Pénzügy és számvitel", "Sales": "Sales",
    "Marketing": "Marketing", "HR": "HR", "Admin / Ügyfélszolgálat": "Office Support",
    "Retail": "Retail", "Gyártás": "Gyártás, Termelés, Mérnökség",
    "Logisztika": "Logisztika, Szállítás", "Építőipar": "Építőipar, Ingatlan",
    "Pharma": "Pharma, Life Sciences", "IT": "IT", "SAP": "SAP",
}
# Talent Insight position label -> sheet TOP3 position, where the two spellings differ.
# Reviewed pair by pair on 2026-09-18; identical labels need no entry.
TI_POSITION = {
    "Medior Technical Support Specialist (Italian / German speaking)": "IT Support / Technical Support Specialist",
    "Junior Supply Chain Specialist (French speaking)": "Supply Chain / Order Management Specialist",
    "Senior Accountant": "Accountant",
    "Senior Transfer Pricing Expert": "Transfer Pricing Expert",
    "Senior Tax Avisor": "Tax Advisor",
    "IT sales": "IT Sales",
    "PPC (senior+)": "PPC",
    "Regional Visual Merchandiser": "Visual Merchandiser",
    "Stategic Buyer": "Strategic Buyer",
    "Generál építésvezető": "Architectural Site Manager",
    "Elektromos előkészítő mérnök": "Electrical Quantity Surveyor",
    "Gépész tervező": "Mechanical Designe Engineer",
    "Medical Sales Representative": "Pharma Medical Sales Representative",
    "Qualified Person/Responsible Person": "Pharma Quality Responsible Person",
    "QC Analyst": "Pharma QC Analyst",
    "Senior AI Engineer": "AI Engineer",
    "Senior Devops/ Cloud Engineer": "Cloud/Devops Engineer",
    "Senior Data Engineer": "Data Engineer",
    "SAP Consultant (MM, SD, FI/CO, EWM)": "SAP Consultant (FI/CO, MM, SD, PP, EWM)",
}

def slug(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9]+", "-", s.upper()).strip("-")

def num(v):
    return None if v is None or v == "" else int(round(float(v)))

wb = openpyxl.load_workbook(BERTABLA, data_only=True)
rows = list(wb["WEB_BERTABLA_IMPORT"].iter_rows(values_only=True))
hi = next(i for i, r in enumerate(rows) if r[0] == "rekord_azonosito")
hdr = [h for h in rows[hi] if h]
raw = [dict(zip(hdr, r)) for r in rows[hi + 1:] if r[1] is not None and r[3] is not None]
IN_SHEET = "linkedin_talent_insight" in hdr
unknown = sorted({r["terulet"] for r in raw if area_name(r["terulet"]) is None})
assert not unknown, f"unmapped area codes/names in the sheet: {unknown}"

web = []
for r in sorted(raw, key=lambda r: AREA_ORDER.index(area_name(r["terulet"]))):
    szint = (r["tapasztalati_szint"] or "").strip() or None
    web.append({
        "id": slug(f"{r['terulet']}-{r['pozicio']}-{szint or 'TOP3'}"),
        "kod": r["terulet"],  # the sheet's raw value, whatever format it was in — provenance only
        "terulet": area_name(r["terulet"]),
        "szint": szint,
        "pozicio": str(r["pozicio"]).strip(),
        "top3": bool(r["top3"]),
        "min": num(r["vallalatok_altal_kinalt_huf"]),
        "idbc": num(r["idbc_javasolt_ber_huf"]),
        "max": num(r["jeloltek_altal_elvart_huf"]),
        "juttatas": (r["juttatasi_megjegyzes"] or "").strip(),
    })
    if IN_SHEET and num(r.get("linkedin_talent_insight")) is not None:
        web[-1]["linkedin"] = num(r["linkedin_talent_insight"])

pool = []
pool_skipped = []
for r in wb["EXPERT_POOL_IMPORT"].iter_rows(min_row=2, values_only=True):
    if not r[0]: continue
    # A row missing its count (darab) is a real, still-open data gap (the client is still
    # sourcing that figure — see 19-implementation-prerequisites.md C-3) not a sync failure:
    # skip it rather than crash the whole import or invent a number for it.
    if r[2] is None:
        pool_skipped.append((r[0], r[1]))
        continue
    pool.append({"iparag": r[0], "pozicio": r[1], "darab": int(r[2])})
    if IN_SHEET and len(r) > 3 and num(r[3]) is not None: pool[-1]["linkedin"] = num(r[3])
readme = "\n".join(str(r[0]) for r in wb["UTMUTATO"].iter_rows(values_only=True) if r[0])

# --- Talent Insight ---------------------------------------------------------------------
top3_by_key = {(w["kod"], w["pozicio"]): w for w in web if w["top3"]}
if IN_SHEET:
    # The sheet is the source: talentInsightTop3 is the TOP3 list as the report names it.
    ti_top3 = []
    for r in raw:
        if not r["top3"]: continue
        ti_area = next(k for k, v in TI_AREA.items() if v == area_name(r["terulet"]))
        ti_top3.append({"terulet": ti_area, "pozicio": (r.get("talent_insight_pozicio") or str(r["pozicio"])).strip(),
                        "linkedin": num(r.get("linkedin_talent_insight"))})
    matched = sum("linkedin" in w for w in top3_by_key.values())
else:
    assert TALENT, "this sheet has no linkedin_talent_insight column — pass the Talent Insight workbook as the second argument"
    tw = openpyxl.load_workbook(TALENT, data_only=True)
    ti_top3 = [{"terulet": r[0], "pozicio": r[1], "linkedin": num(r[2])}
               for r in tw["TOP 3 pozi"].iter_rows(min_row=2, values_only=True) if r[0]]
    ti_pool = {(r[0], r[1]): num(r[3]) for r in tw["Expert pool"].iter_rows(min_row=2, values_only=True) if r[0]}
    matched = 0
    for t in ti_top3:
        key = (TI_AREA[t["terulet"]], TI_POSITION.get(t["pozicio"], t["pozicio"]))
        assert key in top3_by_key, f"Talent Insight position not in the sheet's TOP3: {key}"
        if t["linkedin"] is not None:
            top3_by_key[key]["linkedin"] = t["linkedin"]; matched += 1
    for p in pool:
        n = ti_pool.get((p["iparag"], p["pozicio"]))
        if n is not None: p["linkedin"] = n

d = json.load(io.open(OUT, encoding="utf-8"))
d["salary"] = {"webBertabla": web, "expertPool": pool, "readme": readme, "talentInsightTop3": ti_top3}
io.open(OUT, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, separators=(",", ":")))

areas = {}
for w in web: areas.setdefault(w["terulet"], [0, 0]); areas[w["terulet"]][0] += 1; areas[w["terulet"]][1] += w["top3"]
print(f"webBertabla: {len(web)} rows, {len(areas)} areas, {sum(w['top3'] for w in web)} TOP3 rows, "
      f"{matched} with a Talent Insight count, {sum(1 for w in web if w['top3'] and 'linkedin' not in w)} TOP3 rows without one")
for a, (n, t) in areas.items(): print(f"  {a}: {n} rows, TOP3 {t}")
print(f"expertPool: {len(pool)} rows, {sum('linkedin' in p for p in pool)} with a Talent Insight count")
if pool_skipped:
    print(f"expertPool: {len(pool_skipped)} row(s) skipped, no count (darab) in the sheet yet:")
    for iparag, pozicio in pool_skipped: print(f"  {iparag} / {pozicio}")
