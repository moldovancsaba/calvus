#!/usr/bin/env python3
"""Download the openfootball source files into data/raw/:  python3 gameformative/data/fetch.py
openfootball (football.json, worldcup.json) is dedicated to the public domain under CC0 1.0 —
"Use as you please with no restrictions whatsoever" (README, read 2026-09-25). Run this only to
refresh the inputs; then run convert.py, then build.py. The committed raw files are the inputs the
committed stats.json was built from, so a rebuild without a fetch reproduces it byte for byte."""
import pathlib, urllib.request

RAW = pathlib.Path(__file__).parent / "raw"
BASE = "https://raw.githubusercontent.com/openfootball"
FILES = {
    "2026-27_en.1.json": "football.json/master/2026-27/en.1.json",
    "2026-27_de.1.json": "football.json/master/2026-27/de.1.json",
    "2026-27_es.1.json": "football.json/master/2026-27/es.1.json",
    "2026-27_it.1.json": "football.json/master/2026-27/it.1.json",
    "2026-27_fr.1.json": "football.json/master/2026-27/fr.1.json",
    "2025-26_en.1.json": "football.json/master/2025-26/en.1.json",
    "2025-26_en.1-full.json": "football.json/master/2025-26/en.1-full.json",
    "wc2026_worldcup.json": "worldcup.json/master/2026/worldcup.json",
    "wc2026_worldcup-full.json": "worldcup.json/master/2026/worldcup-full.json",
}

if __name__ == "__main__":
    RAW.mkdir(exist_ok=True)
    for name, path in FILES.items():
        with urllib.request.urlopen(f"{BASE}/{path}", timeout=60) as r:
            body = r.read()
        (RAW / name).write_bytes(body)
        print(f"{name:28s} {len(body):9d} bytes  ← {BASE}/{path}")
