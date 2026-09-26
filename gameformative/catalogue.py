"""The source catalogue — one entry per source any article cites or consulted, keyed by its URL.
Articles keep their own one-line note on each source (what it contributed, or why it was set aside);
this file owns what a source *is*: its canonical title, publisher, date, type, identifiers, and how
we checked it. build.py stops if an article cites a URL that has no entry here, so every source on
the site has a catalogue page anchor (docs/16-source-catalogue.md).

"checked" records what we actually did, on which day — never more. A source we could not read is
catalogued as such; it can only ever appear under "investigated but not used"."""

TYPES = {  # key: (label, what it means for trust — shown on the catalogue page)
    "research": ("Peer-reviewed research", "A study in a peer-reviewed journal. We read at least the abstract and say when we read only that."),
    "official": ("Official body", "A governing body, league, federation, regulator or court speaking for itself."),
    "dataset": ("Open dataset", "Primary data we download and recompute ourselves; the licence is stated."),
    "stats": ("Statistics provider", "A commercial or community statistics site. Consulted; used only where its terms allow."),
    "reporting": ("Reporting", "Journalism from an identified outlet; used for what it reports, attributed."),
    "reference": ("Reference", "A glossary, definition page or method note from a named publisher."),
}

OF = "https://github.com/openfootball/football.json/blob/master/"
WC = "https://github.com/openfootball/worldcup.json/blob/master/2026/"
_OF_CHECK = ("2026-09-25", "Downloaded and converted by the site's converter, which checks every table reconciles.")
_OF = dict(publisher="openfootball (football.json)", type="dataset", licence="CC0 1.0 (public domain)", checked=_OF_CHECK)


def _of(path, title):
    return dict(_OF, id="openfootball-" + path.replace("/", "-").replace(".json", "").replace(".", "-"), title=title)


CATALOGUE = {
    # --- peer-reviewed research ------------------------------------------------------------
    "https://doi.org/10.26773/smj.260219": dict(
        id="sportmont-2026-gps-muscle-injuries", type="research",
        title="Wearable-Monitored External Workload (GPS/GNSS/IMU) and Lower-Limb Muscle Injuries in Football: A Systematic Review and Exploratory Data Synthesis",
        publisher="Sport Mont", date="2026", issue="24(1), 169–178", doi="10.26773/smj.260219",
        checked=("2026-09-25", "Abstract read on the publisher's page; the pooled estimates quoted are in the abstract.")),
    "https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2026.1896651/full": dict(
        id="frontiers-2026-acwr-meta-analysis", type="research",
        title="Acute:chronic workload ratio and load management for team sports: a multilevel meta-analysis",
        publisher="Frontiers in Public Health", date="2026-08-13", doi="10.3389/fpubh.2026.1896651",
        checked=("2026-09-25", "Abstract and results read on the publisher's page.")),
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC11366842/": dict(
        id="sensors-ml-soccer-injury-risk", type="research",
        title="Enhancing Sports Injury Risk Assessment in Soccer Through Machine Learning and Training Load Analysis",
        publisher="Sensors (Basel), via PubMed Central",
        checked=("2026-09-25", "Abstract read on PubMed Central.")),
    "https://doi.org/10.3390/s26134228": dict(
        id="sensors-dual-stream-workload", type="research",
        title="A Frequency-Aware Dual-Stream Deep Learning Framework for Athlete Workload Monitoring and Injury Risk Assessment",
        publisher="Sensors (MDPI)", doi="10.3390/s26134228",
        checked=("2026-09-25", "Not read: the DOI resolves, but the publisher refused our request (HTTP 403).")),
    "https://link.springer.com/article/10.1007/s44163-026-01021-9": dict(
        id="discover-ai-transformers-training-load", type="research",
        title="Athletes' training load prediction using transformers through data analytics and feature projection",
        publisher="Discover Artificial Intelligence (Springer)", doi="10.1007/s44163-026-01021-9",
        checked=("2026-09-25", "Not read: the page resolves, but the publisher served a browser challenge.")),
    # --- open datasets --------------------------------------------------------------------
    OF + "2026-27/en.1.json": _of("2026-27/en.1.json", "English Premier League 2026/27 — results"),
    OF + "2026-27/es.1.json": _of("2026-27/es.1.json", "Spain Primera División 2026/27 — results"),
    OF + "2026-27/de.1.json": _of("2026-27/de.1.json", "Deutsche Bundesliga 2026/27 — results"),
    OF + "2026-27/it.1.json": _of("2026-27/it.1.json", "Italian Serie A 2026/27 — results"),
    OF + "2026-27/fr.1.json": _of("2026-27/fr.1.json", "French Ligue 1 2026/27 — results"),
    OF + "2025-26/en.1.json": _of("2025-26/en.1.json", "English Premier League 2025/26 — results"),
    OF + "2025-26/en.1-full.json": _of("2025-26/en.1-full.json", "England Premier League 2025/26 — goals, line-ups, attendances"),
    WC + "worldcup.json": dict(_OF, id="openfootball-worldcup-2026", publisher="openfootball (worldcup.json)", title="World Cup 2026 — all matches"),
    WC + "worldcup-full.json": dict(_OF, id="openfootball-worldcup-2026-full", publisher="openfootball (worldcup.json)", title="World Cup 2026 — scorers, line-ups, attendances"),
    "https://github.com/openfootball/football.json": dict(_OF, id="openfootball-football-json", title="football.json — free open public-domain football data (repository and README)",
        checked=("2026-09-25", "Repository, README and licence read; the files used are downloaded and converted.")),
    "https://github.com/statsbomb/open-data": dict(
        id="statsbomb-open-data", type="dataset", title="StatsBomb open data and the StatsBomb Public Data User Agreement",
        publisher="StatsBomb", licence="User agreement: no redistribution, no commercial use",
        checked=("2026-09-25", "Repository and user agreement (PDF) read.")),
    # --- statistics providers -------------------------------------------------------------
    "https://fbref.com/en/comps/9/Premier-League-Stats": dict(
        id="fbref-premier-league", type="stats", title="Premier League stats", publisher="FBref",
        checked=("2026-09-25", "Not read: the site refused our request (HTTP 403, a bot challenge).")),
    "https://theanalyst.com/competition/premier-league/stats": dict(
        id="opta-analyst-premier-league", type="stats", title="Premier League stats", publisher="Opta Analyst",
        checked=("2026-09-25", "Page read; its tables are built in the browser.")),
    "https://understat.com/league/EPL": dict(
        id="understat-epl", type="stats", title="EPL expected goals table", publisher="Understat",
        checked=("2026-09-25", "Page read; its data loads in the browser.")),
    "https://www.sofascore.com/tournament/football/england/premier-league/17": dict(
        id="sofascore-premier-league", type="stats", title="Premier League tournament page", publisher="Sofascore",
        checked=("2026-09-25", "Not read: the site refused our request (HTTP 403).")),
    "https://www.whoscored.com/": dict(
        id="whoscored", type="stats", title="Tournament pages", publisher="WhoScored",
        checked=("2026-09-25", "Not read: the site blocked our request (HTTP 403).")),
    # --- official bodies ------------------------------------------------------------------
    "https://www.fifa.com/en": dict(
        id="fifa-com", type="official", title="FIFA — World Cup 26 coverage", publisher="FIFA",
        checked=("2026-09-25", "Not read: the page is built in the browser and returned no readable content.")),
    # --- reporting ------------------------------------------------------------------------
    "https://www.flashscore.es/noticias/futbol-laliga-ea-sports-como-se-decidira-el-descenso-en-caso-de-que-dos-o-mas-equipos-empaten/6aYxHRoD/": dict(
        id="flashscore-es-laliga-tie-breakers", type="reporting", title="Criterios de desempate en LaLiga (how relegation is decided when teams are level)",
        publisher="Flashscore España",
        checked=("2026-09-25", "Page read; the criteria are quoted from it.")),
    "https://www.dazn.com/it-IT/news/altro/serie-a-chi-vince-a-pari-punti-e-in-caso-di-classifica-avulsa/8pfs8lp79uto166dnjta9653g": dict(
        id="dazn-it-serie-a-tie-breakers", type="reporting", title="Serie A: chi vince a pari punti e in caso di classifica avulsa",
        publisher="DAZN Italia",
        checked=("2026-09-25", "Page read; the criteria are quoted from it.")),
    "https://www.365scores.com/es/news/la-liga-desempate-puntos-igualdad/": dict(
        id="365scores-laliga-tie-breakers", type="reporting", title="La Liga: criterio de desempate en caso de igualdad de puntos",
        publisher="365Scores",
        checked=("2026-09-25", "Not read: the page returned a server error (HTTP 500).")),
    # --- reference ------------------------------------------------------------------------
    "https://theanalyst.com/articles/opta-football-stats-definitions": dict(
        id="opta-football-stats-definitions", type="reference", title="Opta football stats definitions",
        publisher="Opta Analyst", date="2024-07-23",
        checked=("2026-09-25", "Page read.")),
}
