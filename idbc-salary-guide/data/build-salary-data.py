# -*- coding: utf-8 -*-
"""Rebuild the salary half of guide-data.json from the client's IDBC_bertabla sheet and the
LinkedIn Talent Insight workbook.

    python3 idbc-salary-guide/data/build-salary-data.py <IDBC_bertabla.xlsx> <Talent_Insight_riport.xlsx>

The survey half (topics, datasets) is left untouched — that comes from build-guide-data.py.
Sheet: 1aQA6Kw5k1U9LQMiWYgcn__m2YCuGmEhx79QFSzE0hJg (File → Download → xlsx, or the export URL).
"""
import io, json, re, sys, unicodedata
import openpyxl

BERTABLA, TALENT = sys.argv[1], sys.argv[2]
OUT = __file__.rsplit("/", 1)[0] + "/guide-data.json"

# Area codes in the sheet -> the names the site uses. Where the trends pages already name the
# area (areas.json), that name is reused so one area reads the same everywhere; the sheet splits
# Sales and Marketing, which the trends survey pools — kept split here, it is the client's table.
AREA_NAME = {
    "BSC": "BSC",
    "PENZUGY": "Pénzügy és számvitel",
    "Sales": "Sales",
    "Marketing": "Marketing",
    "HR": "HR",
    "Office Support": "Office Support & Ügyfélszolgálat",
    "Retail": "Retail",
    "GYARTAS": "Gyártás, termelés, mérnökség",
    "LOGISZTIKA": "Logisztika és szállítás",
    "CP": "Építőipar, ingatlan",
    "PHARMA": "Pharma & Life Sciences",
    "IT": "IT",
    "SAP": "SAP",
}
AREA_ORDER = list(AREA_NAME)  # display order of the Bérek filter

# Talent Insight area label -> sheet area code.
TI_AREA = {
    "BSC": "BSC", "Finance": "PENZUGY", "Sales": "Sales", "Marketing": "Marketing", "HR": "HR",
    "Admin / Ügyfélszolgálat": "Office Support", "Retail": "Retail", "Gyártás": "GYARTAS",
    "Logisztika": "LOGISZTIKA", "Építőipar": "CP", "Pharma": "PHARMA", "IT": "IT", "SAP": "SAP",
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
hdr = rows[hi][:9]
raw = [dict(zip(hdr, r[:9])) for r in rows[hi + 1:] if r[1] is not None and r[3] is not None]
unknown = sorted({r["terulet"] for r in raw} - set(AREA_NAME))
assert not unknown, f"unmapped area codes in the sheet: {unknown}"

web = []
for r in sorted(raw, key=lambda r: AREA_ORDER.index(r["terulet"])):
    szint = (r["tapasztalati_szint"] or "").strip() or None
    web.append({
        "id": slug(f"{r['terulet']}-{r['pozicio']}-{szint or 'TOP3'}"),
        "kod": r["terulet"],
        "terulet": AREA_NAME[r["terulet"]],
        "szint": szint,
        "pozicio": str(r["pozicio"]).strip(),
        "top3": bool(r["top3"]),
        "min": num(r["vallalatok_altal_kinalt_huf"]),
        "idbc": num(r["idbc_javasolt_ber_huf"]),
        "max": num(r["jeloltek_altal_elvart_huf"]),
        "juttatas": (r["juttatasi_megjegyzes"] or "").strip(),
    })

pool = [{"iparag": r[0], "pozicio": r[1], "darab": int(r[2])}
        for r in wb["EXPERT_POOL_IMPORT"].iter_rows(min_row=2, values_only=True) if r[0]]
readme = "\n".join(str(r[0]) for r in wb["UTMUTATO"].iter_rows(values_only=True) if r[0])

# --- Talent Insight ---------------------------------------------------------------------
tw = openpyxl.load_workbook(TALENT, data_only=True)
ti_top3 = [{"terulet": r[0], "pozicio": r[1], "linkedin": num(r[2])}
           for r in tw["TOP 3 pozi"].iter_rows(min_row=2, values_only=True) if r[0]]
ti_pool = {(r[0], r[1]): num(r[3]) for r in tw["Expert pool"].iter_rows(min_row=2, values_only=True) if r[0]}

top3_by_key = {(w["kod"], w["pozicio"]): w for w in web if w["top3"]}
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
