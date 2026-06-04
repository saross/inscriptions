#!/usr/bin/env python3
"""Stage the 2026-06-04 Bayesian-workflow methodology bibliography.

Adds the 12 sources grounding the recovery-grid criterion decisions (OSF
Amendment 01 §A5.5.1, 2026-06-04) to **My Library** (the personal user
library) → ``staging`` collection (key ``IX8XR97K``) → a new dated-topic
subfolder. Verified bibliography: ``planning/martin-review-statistical-
grounds-2026-06-04.md``.

Safety rails: writes ONLY to the user library (asserts library type
``user``); a hard cap of 15 new items; CrossRef for DOI'd refs; manual
templates for arXiv preprints and no-DOI web case studies/docs.

Usage::

    /home/shawn/Code/inscriptions/.venv/bin/python3 \
        scripts/zotero_stage_methods_2026-06-04.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from pyzotero import zotero

PROJECT_ROOT = Path("/home/shawn/Code/inscriptions")
STAGING_KEY = "IX8XR97K"  # My Library > staging
SUBFOLDER = "2026-06-04-bayesian-workflow-conventions-divergences-recovery"
MAILTO = "shawn@faims.edu.au"
MAX_NEW = 15

# 6 DOI'd journal articles — full metadata fetched from CrossRef.
DOIS = [
    "10.1016/S0140-6736(86)90837-8",  # Bland & Altman 1986 (Lancet) — LoA
    "10.1177/2515245918771304",       # Kruschke 2018 (AMPPS) — ROPE
    "10.1214/20-BA1221",              # Vehtari et al. 2021 — R-hat/ESS
    "10.1037/met0000275",             # Schad et al. 2021 — principled workflow
    "10.1214/23-BA1404",              # Modrak et al. 2025 — SBC checking
    "10.1017/RDC.2020.95",            # Crema & Bevan 2020/21 — rcarbon
]

# 2 arXiv-only preprints (canonical IDs; arXiv API was rate-limiting).
ARXIV = [
    {"title": "Validating Bayesian Inference Algorithms with "
              "Simulation-Based Calibration",
     "creators": [("Sean", "Talts"), ("Michael", "Betancourt"),
                  ("Daniel", "Simpson"), ("Aki", "Vehtari"),
                  ("Andrew", "Gelman")],
     "date": "2018", "id": "1804.06788"},
    {"title": "Bayesian Workflow",
     "creators": [("Andrew", "Gelman"), ("Aki", "Vehtari"),
                  ("Daniel", "Simpson"), ("Charles C.", "Margossian"),
                  ("Bob", "Carpenter"), ("Yuling", "Yao"),
                  ("Lauren", "Kennedy"), ("Jonah", "Gabry"),
                  ("Paul-Christian", "Bürkner"), ("Martin", "Modrák")],
     "date": "2020", "id": "2011.01808"},
]

# 4 no-DOI web case studies / docs.
WEB = [
    {"type": "blogPost", "title": "Diagnosing Biased Inference with Divergences",
     "creators": [("Michael", "Betancourt")], "date": "2017",
     "blogTitle": "Betancourt — Writing (case studies)",
     "url": "https://betanalpha.github.io/assets/case_studies/"
            "divergences_and_bias.html"},
    {"type": "blogPost", "title": "Identifying Bayesian Mixture Models",
     "creators": [("Michael", "Betancourt")], "date": "",
     "blogTitle": "Stan case studies",
     "url": "https://mc-stan.org/learn-stan/case-studies/"
            "identifying_mixture_models.html"},
    {"type": "webpage",
     "title": "Runtime warnings and convergence problems (diagnostics)",
     "creators": [("Stan Development Team", None)], "date": "",
     "websiteTitle": "Stan Documentation",
     "url": "https://mc-stan.org/learn-stan/diagnostics-warnings.html"},
    {"type": "blogPost", "title": "Taming Divergences in Stan Models",
     "creators": [("Martin", "Modrák")], "date": "2018",
     "blogTitle": "Martin Modrák — blog",
     "url": "https://www.martinmodrak.cz/2018/02/19/"
            "taming-divergences-in-stan-models/"},
]

CR_TYPE = {"journal-article": "journalArticle", "posted-content": "preprint",
           "book-chapter": "bookSection", "book": "book"}


def creators(persons):
    """Build a Zotero creators list from (first, last) tuples.

    A ``None`` last name marks a single-field (corporate) creator.
    """
    out = []
    for first, last in persons:
        if last is None:
            out.append({"creatorType": "author", "name": first})
        else:
            out.append({"creatorType": "author", "firstName": first,
                        "lastName": last})
    return out


def crossref_item(zot, doi, coll):
    """Fetch CrossRef metadata for a DOI and build a Zotero item."""
    r = requests.get(f"https://api.crossref.org/works/{doi}",
                     params={"mailto": MAILTO}, timeout=30)
    r.raise_for_status()
    m = r.json()["message"]
    it = zot.item_template(CR_TYPE.get((m.get("type") or "").lower(),
                                       "journalArticle"))
    title = (m.get("title") or [""])[0]
    sub = (m.get("subtitle") or [""])
    if sub and sub[0]:
        title = f"{title}: {sub[0]}"
    it["title"] = title
    it["DOI"] = m.get("DOI", "")
    it["url"] = m.get("URL", "")
    it["publicationTitle"] = (m.get("container-title") or [""])[0]
    it["volume"] = m.get("volume", "") or ""
    it["issue"] = m.get("issue", "") or ""
    it["pages"] = m.get("page", "") or ""
    parts = (m.get("issued", {}).get("date-parts", [[]]) or [[]])[0]
    it["date"] = "-".join(f"{p:02d}" if i else f"{p:04d}"
                          for i, p in enumerate(parts)) if parts else ""
    it["creators"] = [
        ({"creatorType": "author", "firstName": p.get("given", ""),
          "lastName": p.get("family", "")} if p.get("family")
         else {"creatorType": "author", "name": p.get("name", "")})
        for p in (m.get("author") or []) if p.get("family") or p.get("name")
    ]
    it["collections"] = [coll]
    return it


def main():
    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.environ["ZOTERO_API_KEY"]
    uid = requests.get("https://api.zotero.org/keys/current",
                       headers={"Zotero-API-Key": api_key},
                       timeout=30).json()["userID"]
    zot = zotero.Zotero(uid, "user", api_key)
    # pyzotero stores library_type pluralised ("users"/"groups") for URLs.
    assert zot.library_type == "users", "refusing: not the user library"
    assert str(zot.library_id) == str(uid)
    print(f"User library {uid}; staging under {SUBFOLDER!r}", file=sys.stderr)

    # 1. Create the dated-topic subfolder under staging.
    res = zot.create_collections([{"name": SUBFOLDER,
                                   "parentCollection": STAGING_KEY}])
    coll = res["successful"]["0"]["key"]
    print(f"created subfolder key={coll}", file=sys.stderr)

    # 2. Build all 12 items.
    items = []
    for doi in DOIS:
        items.append(crossref_item(zot, doi, coll))
        time.sleep(0.4)
    for a in ARXIV:
        it = zot.item_template("preprint")
        it.update({"title": a["title"], "creators": creators(a["creators"]),
                   "date": a["date"], "repository": "arXiv",
                   "archiveID": f"arXiv:{a['id']}",
                   "url": f"https://arxiv.org/abs/{a['id']}",
                   "collections": [coll]})
        items.append(it)
    for w in WEB:
        it = zot.item_template(w["type"])
        it.update({"title": w["title"], "creators": creators(w["creators"]),
                   "date": w["date"], "url": w["url"], "collections": [coll]})
        if w["type"] == "blogPost":
            it["blogTitle"] = w.get("blogTitle", "")
        else:
            it["websiteTitle"] = w.get("websiteTitle", "")
        items.append(it)

    assert len(items) <= MAX_NEW, f"too many items ({len(items)})"
    print(f"creating {len(items)} items…", file=sys.stderr)
    out = zot.create_items(items)
    ok = out.get("successful", {})
    fail = out.get("failed", {})
    print(f"\n=== created {len(ok)} / {len(items)}  (failed {len(fail)}) ===")
    for k, v in ok.items():
        d = v.get("data", {})
        print(f"  + {d.get('itemType'):14s} {d.get('title','')[:60]}")
    if fail:
        print("FAILURES:", json.dumps(fail, indent=2))
    print(f"\nsubfolder: My Library > staging > {SUBFOLDER}  (key {coll})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
