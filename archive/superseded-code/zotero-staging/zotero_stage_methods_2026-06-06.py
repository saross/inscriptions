#!/usr/bin/env python3
"""Stage the 2026-06-06 epigraphic dating-methodology bibliography.

Adds 4 newly-discovered sources (verified via CrossRef this session) to
**My Library** (the personal user library) → ``staging`` collection (key
``IX8XR97K``) → a new dated-topic subfolder
``2026-06-06-epigraphic-dating-methodology``.

This is a direct reuse of the established one-off staging method first
committed as ``scripts/zotero_stage_methods_2026-06-04.py`` (commit
524ea32). All 4 items here are DOI'd, so only the CrossRef path applies;
the arXiv-preprint and no-DOI-web branches of the original are omitted as
they have no items to stage.

Safety rails (carried over unchanged): writes ONLY to the user library
(asserts library type ``users``); a hard cap of 15 new items; CrossRef
for DOI'd refs.

Usage::

    /home/shawn/Code/inscriptions/.venv/bin/python3 \
        scripts/zotero_stage_methods_2026-06-06.py
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
SUBFOLDER = "2026-06-06-epigraphic-dating-methodology"
MAILTO = "shawn@faims.edu.au"
MAX_NEW = 15

# 4 DOI'd refs — full metadata fetched from CrossRef.
DOIS = [
    "10.1163/9789004748613_012",  # Feraudi-Gruénais & Grieshaber 2025 — Brill chapter
    "10.1017/cbo9781139020442",   # Cooley 2012 — Cambridge Manual of Latin Epigraphy (PRIORITY)
    "10.5334/johd.428",           # Heřmánková et al. 2025 — FAIR Epigraphic Vocabularies (JOHD)
    "10.5334/jcaa.191",           # Roe et al. 2025 — XRONOS (JCAA)
]

# CrossRef returns ``monograph`` for some single-author scholarly books
# (e.g. Cooley 2012), so map it to ``book`` alongside the plain ``book``
# type — otherwise the item silently falls back to ``journalArticle``.
CR_TYPE = {"journal-article": "journalArticle", "posted-content": "preprint",
           "book-chapter": "bookSection", "book": "book",
           "monograph": "book"}


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
    # bookSection uses bookTitle for the container; everything else
    # uses publicationTitle. Fall back gracefully if a key is absent.
    container = (m.get("container-title") or [""])[0]
    if it.get("itemType") == "bookSection" or "bookTitle" in it:
        it["bookTitle"] = container
        if "publisher" in it:
            it["publisher"] = m.get("publisher", "") or ""
    else:
        if "publicationTitle" in it:
            it["publicationTitle"] = container
        if "publisher" in it:
            it["publisher"] = m.get("publisher", "") or ""
    for key in ("volume", "issue", "pages"):
        src = "page" if key == "pages" else key
        if key in it:
            it[key] = m.get(src, "") or ""
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

    # 2. Build all items.
    items = []
    for doi in DOIS:
        items.append(crossref_item(zot, doi, coll))
        time.sleep(0.4)

    assert len(items) <= MAX_NEW, f"too many items ({len(items)})"
    print(f"creating {len(items)} items…", file=sys.stderr)
    out = zot.create_items(items)
    ok = out.get("successful", {})
    fail = out.get("failed", {})
    print(f"\n=== created {len(ok)} / {len(items)}  (failed {len(fail)}) ===")
    for k, v in ok.items():
        d = v.get("data", {})
        print(f"  + {d.get('key')}  {d.get('itemType'):14s} "
              f"{d.get('title','')[:60]}")
    if fail:
        print("FAILURES:", json.dumps(fail, indent=2))
    print(f"\nsubfolder: My Library > staging > {SUBFOLDER}  (key {coll})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
