#!/usr/bin/env python3
"""Add 2 more sources to an EXISTING 2026-06-06 staging subcollection.

Variant of ``scripts/zotero_stage_methods_2026-06-06.py`` (commit
``5c6cddd``). The difference is deliberate and narrow: instead of
*creating* a new dated-topic subfolder under ``staging``, this targets an
**already-existing** subcollection by key
(``7RVI3KB7`` = ``My Library > staging > 2026-06-06-epigraphic-dating-methodology``)
and appends 2 further DOI'd refs verified this session.

Why a separate script rather than an edit to the committed one: the
original is a record of a completed one-off run; re-running it would
create a duplicate subfolder. This variant preserves that record and adds
the explicit "append to existing collection" behaviour the follow-up task
needs.

The 2 refs:

* ``10.5334/jcaa.220`` — Tobalina-Pulido & Martín-Rodilla 2026,
  "Quantifying Inherited Uncertainty in Archaeological Legacy Data Using
  Fuzzy Logic Metrics" (JCAA; ``journalArticle``). Nearest-competitor
  paper for the project's novelty claim.
* ``10.46771/978-3-96769-729-2`` — Hartmann 2025, "Die frühlateinischen
  Inschriften und ihre Datierung" (German monograph). CrossRef returns
  type ``edited-book`` for this record, so the type map below maps both
  ``monograph`` AND ``edited-book`` to Zotero ``book`` — otherwise the
  item silently falls back to ``journalArticle``. The task requires it to
  land as ``book``.

Safety rails (carried over, plus tightened for the append case):

* writes ONLY to the user library (asserts library type ``users``);
* asserts the target collection's name + parent ``staging`` BEFORE any
  write — aborts on mismatch;
* dedups each DOI against the target collection's current contents —
  skips any already present;
* every new item is created with ``collections=[TARGET_KEY]`` so nothing
  leaks to the top-level library;
* a hard cap of 5 new items.

Usage::

    /home/shawn/Code/inscriptions/.venv/bin/python3 \
        scripts/zotero_stage_methods_2026-06-06_add_to_existing.py
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
TARGET_KEY = "7RVI3KB7"  # My Library > staging > 2026-06-06-epigraphic-dating-methodology
EXPECTED_NAME = "2026-06-06-epigraphic-dating-methodology"
EXPECTED_PARENT_NAME = "staging"
MAILTO = "shawn@faims.edu.au"
MAX_NEW = 5

# 2 DOI'd refs — full metadata fetched from CrossRef.
DOIS = [
    "10.5334/jcaa.220",              # Tobalina-Pulido & Martín-Rodilla 2026 (PRIORITY)
    "10.46771/978-3-96769-729-2",    # Hartmann 2025 — German monograph (PRIORITY)
]

# CrossRef uses several "book-ish" types for single-volume scholarly
# books. Map all of them to Zotero ``book`` so the item does not silently
# fall back to ``journalArticle``. (Hartmann 2025 comes back as
# ``edited-book``; Cooley 2012 in the parent script came back as
# ``monograph``.)
CR_TYPE = {"journal-article": "journalArticle", "posted-content": "preprint",
           "book-chapter": "bookSection", "book": "book",
           "monograph": "book", "edited-book": "book"}


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
    print(f"User library {uid}; appending to {TARGET_KEY}", file=sys.stderr)

    # 1. Verify the target collection identity BEFORE any write.
    coll_obj = zot.collection(TARGET_KEY)
    cdata = coll_obj["data"]
    assert cdata["name"] == EXPECTED_NAME, \
        f"ABORT: target name {cdata['name']!r} != {EXPECTED_NAME!r}"
    parent_key = cdata.get("parentCollection")
    assert parent_key, "ABORT: target has no parent collection"
    pname = zot.collection(parent_key)["data"]["name"]
    assert pname == EXPECTED_PARENT_NAME, \
        f"ABORT: parent {pname!r} != {EXPECTED_PARENT_NAME!r}"
    print(f"verified: {EXPECTED_PARENT_NAME} > {EXPECTED_NAME} "
          f"({TARGET_KEY})", file=sys.stderr)

    # 2. Dedup against the target collection's current DOIs.
    existing = zot.collection_items(TARGET_KEY)
    existing_dois = {(it["data"].get("DOI") or "").strip().lower()
                     for it in existing}
    existing_dois.discard("")
    to_add = []
    for doi in DOIS:
        if doi.strip().lower() in existing_dois:
            print(f"skip (already present): {doi}", file=sys.stderr)
        else:
            to_add.append(doi)
    if not to_add:
        print("nothing to add — all DOIs already present.")
        return 0

    # 3. Build items.
    items = []
    for doi in to_add:
        items.append(crossref_item(zot, doi, TARGET_KEY))
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

    # 4. Verify each new item landed in the target collection.
    print("\n=== post-write verification (collection membership) ===")
    for k, v in ok.items():
        key = v.get("data", {}).get("key")
        item = zot.item(key)["data"]
        in_coll = TARGET_KEY in item.get("collections", [])
        print(f"  {key}  type={item.get('itemType'):14s} "
              f"in {TARGET_KEY}={in_coll}  DOI={item.get('DOI','')}")
        print(f"        title={item.get('title','')}")

    print(f"\ntarget: My Library > {EXPECTED_PARENT_NAME} > {EXPECTED_NAME} "
          f"(key {TARGET_KEY})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
