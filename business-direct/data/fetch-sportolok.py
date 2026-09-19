# -*- coding: utf-8 -*-
"""Pull the public data of one listing platform instance into business-direct/data/.

    python3 business-direct/data/fetch-sportolok.py [https://sport.doneisbetter.com]

Reads only public endpoints (documented at /api-reference) and the public listing pages'
schema.org JSON-LD. Writes:
  platform.json   facets, territory levels, age bands, site copy, fetch date
  listings.json   one row per listing: id, name, category, locality, county, address, geo,
                  website, description, verified, checkedAt, when, hours, nextSession
Deterministic for a given platform state; re-run to refresh. No key, no writes to the platform.
"""
import io, json, re, sys, time, html, datetime, concurrent.futures
import urllib.request

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://sport.doneisbetter.com"
OUT = __file__.rsplit("/", 1)[0]
UA = {"User-Agent": "Mozilla/5.0 (business.direct prototype; public data only)"}

def get(path, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(BASE + path, headers=UA), timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(1.5 * (i + 1))

facets = json.loads(get("/api/public/browse-facets"))
site = json.loads(get("/api/public/site"))
pins = json.loads(get("/api/public/map-pins"))
FACET_LABEL = {f["slug"]: f["label"] for f in facets["facets"]}
print(f"{BASE}: {len(facets['facets'])} facets, {len(pins['pins'])} pins (capped={pins['capped']}, unmapped={pins['unmappedCount']})")

def text(s):
    s = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", "", s, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

def listing(pin):
    page = get(f"/listing/{pin['id']}")
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', page, flags=re.S)
    ld = json.loads(m.group(1)) if m else {}
    if isinstance(ld, list): ld = next((x for x in ld if x.get("@type") == "LocalBusiness"), ld[0] if ld else {})
    body = text(page[page.lower().find("<body"):])
    cat = re.search(r"← Vissza: ([^ ]+(?: [^ ]+)?) ", body)
    when = re.search(r"Mikor ([^\n]*?) Utoljára ellenőrizve", body)
    checked = re.search(r"Utoljára ellenőrizve (\d{4}\. [a-záéíóöőúüű]+\.? \d{1,2}\.)", body)
    hours = re.search(r"((?:Hétfő|H-|Hétköznap|Minden nap)[^.]{0,160}\.)", body)
    nxt = re.search(r"Következő: ([^·]{3,30}· ?\d{1,2}:\d{2})", body)
    county = re.search(r"([A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű-]+(?:-[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]+)? vármegye)", body)
    addr = ld.get("address", {}) if isinstance(ld.get("address"), dict) else {}
    geo = ld.get("geo", {}) if isinstance(ld.get("geo"), dict) else {}
    locality = addr.get("addressLocality", "")
    slug = pin["spriteKey"].replace("pin-", "")
    return {
        "id": pin["id"], "name": ld.get("name") or pin["name"],
        "category": slug,
        # the facet label by slug; the page's breadcrumb repeats the badge ("Edzőtermek Edzőtermek")
        "categoryLabel": FACET_LABEL.get(slug, {"multi": "Többféle lehetőség", "default": "Egyéb"}.get(slug, slug)),
        "locality": locality,
        # Budapest is a capital, not a vármegye: the page prints no county for it
        "county": "Budapest" if locality.startswith("Budapest") else (county.group(1) if county else ""),
        "address": addr.get("streetAddress", ""), "lat": pin["lat"], "lng": pin["lng"],
        "website": ld.get("sameAs", ""), "description": ld.get("description", ""),
        "verified": "Ellenőrzött" in body[:2000] or "Checked recently" in body,
        "checkedAt": checked.group(1) if checked else "",
        "when": when.group(1).strip() if when else "",
        "hours": hours.group(1).strip() if hours else "",
        "nextSession": nxt.group(1).strip() if nxt else "",
        "claimed": False,  # the platform shows "Az enyém ez a sportolási lehetőség" on every card: none is claimed yet
    }

rows, errors = [], []
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    for i, res in enumerate(ex.map(lambda p: (p, listing(p)), pins["pins"]), 1):
        p, row = res
        rows.append(row)
        if i % 50 == 0: print(f"  {i}/{len(pins['pins'])}")
rows.sort(key=lambda r: r["id"])
today = datetime.date.today().isoformat()
io.open(f"{OUT}/platform.json", "w", encoding="utf-8").write(json.dumps({
    "source": BASE, "fetched": today, "facets": facets["facets"], "territory": facets["territory"],
    "ages": facets["ages"], "siteCopy": {k: v for k, v in site["siteCopy"].items() if k not in ("source", "account")},
}, ensure_ascii=False, indent=1))
io.open(f"{OUT}/listings.json", "w", encoding="utf-8").write(json.dumps({"source": BASE, "fetched": today, "listings": rows}, ensure_ascii=False, separators=(",", ":")))
cats = {}
for r in rows: cats[r["category"]] = cats.get(r["category"], 0) + 1
print(f"listings.json: {len(rows)} rows; categories {cats}; with website {sum(1 for r in rows if r['website'])}, "
      f"with description {sum(1 for r in rows if r['description'])}, with next session {sum(1 for r in rows if r['nextSession'])}, "
      f"counties {len({r['county'] for r in rows if r['county']})}")
