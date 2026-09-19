# -*- coding: utf-8 -*-
"""Pull Your Field NYC's public data into business-direct/data/ — the first client (D11).

    python3 business-direct/data/fetch-yourfield.py [https://getyourfield.com] [city=nyc]

Reads only public endpoints the site's own front end calls (found in its JS bundles, 2026-09-19):
  /api/public/browse-facets       boroughs, neighbourhoods, activity counts
  /api/public/site                site copy (hero, how it works, trust, newsletter, "List your program")
  /api/public/providers           every provider card (252 on 2026-09-19)
  /api/public/providers/{id}      the full record: sessions, announcement, booking, trial policy, geo
Writes platform.json and providers.json. Read-only; no key; deterministic for a platform state.
"""
import io, json, sys, time, datetime, concurrent.futures
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://getyourfield.com").rstrip("/")
CITY = sys.argv[2] if len(sys.argv) > 2 else "nyc"
OUT = __file__.rsplit("/", 1)[0]
UA = {"User-Agent": "Mozilla/5.0 (business.direct prototype; public data only)"}

def get(path, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(BASE + path, headers=UA), timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if i == tries - 1: raise
            time.sleep(1.5 * (i + 1))

facets = get("/api/public/browse-facets")
site = get("/api/public/site")
cards = get("/api/public/providers")
print(f"{BASE}: {len(cards)} providers; boroughs {facets['boroughCounts']}; {len(facets['activities'])} activities")

KEEP_SITE = ["homeHeroTitle", "homeHeroTagline", "homeHeroSubtitle", "homeHeroPrimaryCta", "homeHeroSecondaryCta",
             "howItWorksSectionTitle", "howItWorksSteps", "trustLines", "trustPillars", "newsletterTitle",
             "newsletterSubtitle", "newsletterCta", "newsletterFinePrint", "popularPicksSectionTitle",
             "neighborhoodSectionTitle", "sidebarTitle", "sidebarBody", "sidebarCtaLabel", "logoUrl"]

def full(card):
    d = get(f"/api/public/providers/{card['id']}")["provider"]
    price = d.get("price") or {}
    geo = d.get("geo") or {}
    return {
        "id": d["id"], "name": d["name"], "category": d.get("category", ""),
        "borough": d.get("borough", ""), "neighborhood": d.get("neighborhood", ""), "address": d.get("address", ""),
        "lat": geo.get("lat"), "lng": geo.get("lng"),
        "activityTypes": d.get("activityTypes", []), "primaryActivityType": d.get("primaryActivityType", ""),
        "ageRanges": d.get("ageRanges", []), "ageMinMonths": d.get("ageMinMonths"), "ageMaxMonths": d.get("ageMaxMonths"),
        "shortDescription": d.get("shortDescription", ""), "longDescription": d.get("longDescription", ""),
        "price": {"amount": price.get("amount"), "currency": price.get("currency"), "unit": price.get("unit"), "evidence": price.get("evidence")} if price else None,
        "website": d.get("website", ""), "phone": d.get("phone", ""), "email": d.get("email", ""),
        "image": d.get("image", ""), "dayTimeTags": d.get("dayTimeTags", []), "venueModel": d.get("venueModel", ""),
        "sessions": [{"id": s.get("id"), "title": s.get("title"), "registration": s.get("registrationStatus")} for s in (d.get("sessions") or [])],
        "nextOccurrence": d.get("nextOccurrence"),
        "announcement": {"title": d.get("announcementTitle"), "description": d.get("announcementDescription"), "badge": d.get("announcementBadge")} if d.get("announcementTitle") else None,
        "bookingEnabled": bool(d.get("bookingEnabled")),
        "trial": {"available": bool((d.get("trialPolicy") or {}).get("trialAvailable")), "free": bool((d.get("trialPolicy") or {}).get("trialIsFree")),
                  "text": (d.get("trialPolicy") or {}).get("sourceText")} if d.get("trialPolicy") else None,
        "rating": d.get("rating", 0), "reviewCount": d.get("reviewCount", 0), "badges": d.get("badges", []),
        # the list endpoint carries claimStatus ("unclaimed" on 15 of 252 today); the single record does not
        "claimStatus": d.get("claimStatus") or card.get("claimStatus") or "unset",
        "verifiedFields": sorted({v["field"] for v in (d.get("fieldVerifications") or []) if v.get("field")}),
        "updatedAt": d.get("updatedAt"), "publishedAt": d.get("publishedAt"), "sourceCount": d.get("sourceCount"),
    }

rows = []
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    for i, row in enumerate(ex.map(full, cards), 1):
        rows.append(row)
        if i % 50 == 0: print(f"  {i}/{len(cards)}")
rows.sort(key=lambda r: r["id"])
today = datetime.date.today().isoformat()
io.open(f"{OUT}/platform.json", "w", encoding="utf-8").write(json.dumps({
    "source": BASE, "city": CITY, "fetched": today, "facets": facets,
    "siteCopy": {k: site.get(k) for k in KEEP_SITE if site.get(k) not in (None, "", [], {})},
}, ensure_ascii=False, indent=1))
io.open(f"{OUT}/providers.json", "w", encoding="utf-8").write(json.dumps({"source": BASE, "city": CITY, "fetched": today, "providers": rows}, ensure_ascii=False, separators=(",", ":")))
n = len(rows)
print(f"providers.json: {n} rows; website {sum(1 for r in rows if r['website'])}, phone {sum(1 for r in rows if r['phone'])}, "
      f"email {sum(1 for r in rows if r['email'])}, price {sum(1 for r in rows if r['price'] and r['price']['amount'])}, "
      f"sessions {sum(1 for r in rows if r['sessions'])}, nextOccurrence {sum(1 for r in rows if r['nextOccurrence'])}, "
      f"geo {sum(1 for r in rows if r['lat'])}, announcement {sum(1 for r in rows if r['announcement'])}, "
      f"booking {sum(1 for r in rows if r['bookingEnabled'])}, trial {sum(1 for r in rows if r['trial'] and r['trial']['available'])}, claimStatus {dict((s, sum(1 for r in rows if r['claimStatus']==s)) for s in set(r['claimStatus'] for r in rows))}")
