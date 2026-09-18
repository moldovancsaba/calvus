#!/usr/bin/env python3
"""Render every project's documentation:  python3 build-docs.py
Runs the four per-project renderers in place (each keeps its own page list, tokens and
template — projects do not share a look on purpose). Needs the `markdown` package.
Follow with `python3 check.py`.
"""
import subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
for r in ["holdvolgy/docs/build.py", "idbc-salary-guide/docs/build.py", "discountdirect/build-docs.py", "lexodont.hu/docs/build.py"]:
    print(f"== {r}")
    subprocess.run([sys.executable, str(ROOT / r)], check=True)
