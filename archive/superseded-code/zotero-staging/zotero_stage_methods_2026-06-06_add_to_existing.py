#!/usr/bin/env python3
"""Add more sources to an EXISTING 2026-06-06 staging subcollection.

Variant of ``scripts/zotero_stage_methods_2026-06-06.py`` (commit
``5c6cddd``). The difference is deliberate and narrow: instead of
*creating* a new dated-topic subfolder under ``staging``, this targets an
**already-existing** subcollection by key
(``7RVI3KB7`` = ``My Library > staging > 2026-06-06-epigraphic-dating-methodology``)
and appends further DOI'd refs verified this session.

Why a separate script rather than an edit to the committed one: the
original is a record of a completed one-off run; re-running it would
create a duplicate subfolder. This variant preserves that record and adds
the explicit "append to existing collection" behaviour the follow-up task
needs.

History of refs appended by this script (each run dedups, so re-running
is idempotent):

First run (2 refs, CrossRef-only):

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

Second run (3 more refs, mixed registry — REQUIRED a DataCite branch):

* ``10.5281/zenodo.3575154`` — Cowey et al. 2019, "Epigraphic Database
  Heidelberg EpiDoc files" (Zenodo concept/all-versions DOI). This is a
  **DataCite**, not CrossRef, DOI, so CrossRef has no record of it. The
  ``datacite_item`` branch below fetches it from the DataCite REST API
  and maps the citeproc/resourceTypeGeneral ``dataset`` to Zotero
  ``dataset``. Primary EDH data-dump cite for the dating-criteria field.
* ``10.5281/zenodo.3575155`` — same authors/title/year, the Zenodo **v1
  version DOI** (also DataCite, also ``dataset``). Carries an Extra note
  recording it as the v1 snapshot and pointing at the concept DOI.
* ``10.1515/9783112519684-024`` — Krummrey 1987, a De Gruyter **book
  review** of Schillinger-Häfele's consular/titulature-dating handbook.
  This one IS a CrossRef DOI, typed ``book-chapter`` upstream, but its
  ``container-title`` is junk (just ``"1987"``). To avoid a misleading
  ``bookTitle`` we force it to Zotero ``document`` via ``TYPE_OVERRIDE``
  and rely on its Extra note to explain what it is and that the reviewed
  handbook itself has no DOI (needs a manual catalogue entry).

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

# DOIs to append. Each is tagged with the registry it lives in so the
# right fetcher is used: CrossRef DOIs go through ``crossref_item``;
# DataCite DOIs (Zenodo, here) go through ``datacite_item``. The first
# two CrossRef entries were the original run and are kept so re-runs stay
# idempotent (they dedup out as already-present).
DOIS = [
    # --- first run (CrossRef) ---
    ("10.5334/jcaa.220", "crossref"),            # Tobalina-Pulido & Martín-Rodilla 2026
    ("10.46771/978-3-96769-729-2", "crossref"),  # Hartmann 2025 — German monograph
    # --- second run (mixed) ---
    ("10.5281/zenodo.3575154", "datacite"),      # EDH EpiDoc files — concept DOI
    ("10.5281/zenodo.3575155", "datacite"),      # EDH EpiDoc files — v1 version DOI
    ("10.1515/9783112519684-024", "crossref"),   # Krummrey 1987 — book review (De Gruyter)
]

# Per-DOI forced Zotero item type, overriding the registry type maps
# below. Used where the upstream type would produce a misleading record.
# The Krummrey review is typed ``book-chapter`` by CrossRef but its
# container-title is junk (``"1987"``), so we make it a plain
# ``document`` and lean on the Extra note for context.
TYPE_OVERRIDE = {
    "10.1515/9783112519684-024": "document",
}

# Per-DOI text appended to the Zotero "Extra" field. Used for provenance
# notes that do not fit a structured field.
EXTRA_NOTES = {
    "10.5281/zenodo.3575155":
        "v1 snapshot (2019-12-13) of the EDH EpiDoc dump; "
        "concept DOI 10.5281/zenodo.3575154",
    "10.1515/9783112519684-024":
        "Book review of Schillinger-Häfele 1986 "
        "(Consules–Augusti–Caesares), the standard consular/titulature-"
        "dating handbook, which itself has no DOI and needs a manual "
        "catalogue entry.",
}

# CrossRef uses several "book-ish" types for single-volume scholarly
# books. Map all of them to Zotero ``book`` so the item does not silently
# fall back to ``journalArticle``. (Hartmann 2025 comes back as
# ``edited-book``; Cooley 2012 in the parent script came back as
# ``monograph``.)
CR_TYPE = {"journal-article": "journalArticle", "posted-content": "preprint",
           "book-chapter": "bookSection", "book": "book",
           "monograph": "book", "edited-book": "book"}

# DataCite ``resourceTypeGeneral`` -> Zotero item type. Zenodo data
# dumps come back as ``Dataset``; map to Zotero ``dataset``.
DC_TYPE = {"dataset": "dataset", "software": "computerProgram",
           "text": "document", "report": "report"}


def crossref_item(zot, doi, coll):
    """Fetch CrossRef metadata for a DOI and build a Zotero item.

    Respects ``TYPE_OVERRIDE`` (force a Zotero type for awkward records)
    and ``EXTRA_NOTES`` (per-DOI provenance text for the Extra field).
    """
    r = requests.get(f"https://api.crossref.org/works/{doi}",
                     params={"mailto": MAILTO}, timeout=30)
    r.raise_for_status()
    m = r.json()["message"]
    ztype = TYPE_OVERRIDE.get(doi) or CR_TYPE.get(
        (m.get("type") or "").lower(), "journalArticle")
    it = zot.item_template(ztype)
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
    if doi in EXTRA_NOTES and "extra" in it:
        it["extra"] = EXTRA_NOTES[doi]
    it["collections"] = [coll]
    return it


def datacite_item(zot, doi, coll):
    """Fetch DataCite metadata for a DOI and build a Zotero item.

    DataCite is the registry behind Zenodo (and most data/software DOIs);
    CrossRef has no record of these DOIs, so they MUST be resolved here.
    The ``resourceTypeGeneral`` (e.g. ``Dataset``) is mapped to a Zotero
    type via ``DC_TYPE``, with ``TYPE_OVERRIDE`` winning if set. Honours
    ``EXTRA_NOTES`` for per-DOI provenance text, and records the Zenodo
    version (when present) in ``versionNumber``.
    """
    r = requests.get(f"https://api.datacite.org/dois/{doi}", timeout=30)
    r.raise_for_status()
    a = r.json()["data"]["attributes"]
    general = ((a.get("types") or {}).get("resourceTypeGeneral") or "").lower()
    ztype = TYPE_OVERRIDE.get(doi) or DC_TYPE.get(general, "document")
    it = zot.item_template(ztype)
    it["title"] = (a.get("titles") or [{}])[0].get("title", "")
    it["DOI"] = a.get("doi", "") or doi
    # Prefer a stable DOI URL over the (version-specific) landing page.
    it["url"] = f"https://doi.org/{a.get('doi') or doi}"
    # Issued date if present, else fall back to the publication year.
    issued = next((d.get("date") for d in (a.get("dates") or [])
                   if (d.get("dateType") or "").lower() == "issued"), "")
    it["date"] = issued or str(a.get("publicationYear") or "")
    # ``repository`` is the natural home for the publisher of a dataset
    # (Zotero ``dataset`` has no ``publisher`` field; it has both
    # ``repository`` and ``publisher`` only for some types).
    pub = a.get("publisher", "") or ""
    if "repository" in it:
        it["repository"] = pub
    elif "publisher" in it:
        it["publisher"] = pub
    ver = a.get("version")
    if ver and "versionNumber" in it:
        it["versionNumber"] = str(ver)
    # DataCite ``creators`` carry givenName/familyName for Personal names
    # and a bare ``name`` for organisations.
    it["creators"] = [
        ({"creatorType": "author", "firstName": c.get("givenName", ""),
          "lastName": c.get("familyName", "")}
         if (c.get("nameType") or "").lower() == "personal"
            and c.get("familyName")
         else {"creatorType": "author", "name": c.get("name", "")})
        for c in (a.get("creators") or []) if c.get("name") or c.get("familyName")
    ]
    if doi in EXTRA_NOTES and "extra" in it:
        it["extra"] = EXTRA_NOTES[doi]
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
    for doi, registry in DOIS:
        if doi.strip().lower() in existing_dois:
            print(f"skip (already present): {doi}", file=sys.stderr)
        else:
            to_add.append((doi, registry))
    if not to_add:
        print("nothing to add — all DOIs already present.")
        return 0

    # 3. Build items, dispatching to the registry-specific fetcher.
    fetchers = {"crossref": crossref_item, "datacite": datacite_item}
    items = []
    for doi, registry in to_add:
        fetch = fetchers[registry]
        print(f"fetch ({registry}): {doi}", file=sys.stderr)
        items.append(fetch(zot, doi, TARGET_KEY))
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

    # 4. Verify each new item landed in the target collection, and that
    #    any expected Extra note / version was persisted.
    print("\n=== post-write verification (collection membership) ===")
    for k, v in ok.items():
        key = v.get("data", {}).get("key")
        item = zot.item(key)["data"]
        in_coll = TARGET_KEY in item.get("collections", [])
        print(f"  {key}  type={item.get('itemType'):14s} "
              f"in {TARGET_KEY}={in_coll}  DOI={item.get('DOI','')}")
        print(f"        title={item.get('title','')}")
        if item.get("versionNumber"):
            print(f"        versionNumber={item.get('versionNumber')}")
        if item.get("extra"):
            print(f"        extra={item.get('extra')}")

    print(f"\ntarget: My Library > {EXPECTED_PARENT_NAME} > {EXPECTED_NAME} "
          f"(key {TARGET_KEY})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
