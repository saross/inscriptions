#!/usr/bin/env python3
"""Batch-add scout-cited papers to the SDAM Zotero group library.

This script adds ~23 curated papers (from three scout reports) to the
"SPA" collection (key ``PZN5ATJK``) in the SDAM Zotero group
(group ID ``2366083``). It is designed to be strictly idempotent, safe,
and auditable:

* Items already in SDAM (matched by normalised Digital Object Identifier
  (DOI)) are not recreated; they are merely linked to the SPA collection
  if missing.
* New items are created via CrossRef metadata, with item-type inferred
  from CrossRef ``type`` (``journal-article`` → ``journalArticle`` etc.).
* For open-access (OA) papers with a direct ``pdf_url``, the Portable
  Document Format (PDF) is downloaded and attached --- but only if the
  first four bytes are the literal ``%PDF`` magic bytes. Landing pages
  and paywall decoys are never attached.
* Every write is guarded by ``assert library_id == '2366083'`` and a
  hard cap of ``MAX_NEW_ITEMS = 30`` new creations. Three consecutive
  errors abort the run.
* A JSON-Lines (JSONL) log is appended one record at a time, so partial
  progress survives interruption.

Usage::

    /home/shawn/Code/inscriptions/.venv/bin/python3 \
        scripts/zotero_batch_add.py            # full batch
    /home/shawn/Code/inscriptions/.venv/bin/python3 \
        scripts/zotero_batch_add.py --test     # single test paper only

See ``runs/2026-04-24-zotero-batch-add/log.jsonl`` for the authoritative
audit trail.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import requests
from dotenv import load_dotenv
from pyzotero import zotero

# ----------------------------------------------------------------------
# Constants --- safety rails and project-specific identifiers.
# ----------------------------------------------------------------------

#: The SDAM group identifier --- the ONLY library this script writes to.
SDAM_GROUP_ID: str = "2366083"

#: The SPA collection key within the SDAM group. Every created item is
#: linked to this collection.
SPA_COLLECTION_KEY: str = "PZN5ATJK"

#: Polite mailto header for CrossRef Application Programming Interface
#: (API) etiquette (see https://api.crossref.org).
CROSSREF_MAILTO: str = "shawn@faims.edu.au"

#: Maximum number of new items the script may create in a single run.
#: Idempotency checks still run for remaining papers once hit.
MAX_NEW_ITEMS: int = 30

#: Abort threshold for consecutive errors (CrossRef or Zotero).
MAX_CONSECUTIVE_ERRORS: int = 3

#: Seconds to sleep between CrossRef requests --- etiquette, not a hard
#: requirement. Zotero calls are not throttled here (pyzotero handles
#: its own rate-limiting).
CROSSREF_DELAY_S: float = 0.5

#: Mapping from CrossRef ``type`` strings to pyzotero item-type keys.
CROSSREF_TYPE_MAP: dict[str, str] = {
    "journal-article": "journalArticle",
    "book-chapter": "bookSection",
    "book": "book",
    "monograph": "book",
    "edited-book": "book",
    "posted-content": "preprint",
    "proceedings-article": "conferencePaper",
}

#: Project root (the directory containing the ``.env`` file).
PROJECT_ROOT: Path = Path("/home/shawn/Code/inscriptions")

#: Path to the JSONL log for this run.
LOG_PATH: Path = (
    PROJECT_ROOT / "runs" / "2026-04-24-zotero-batch-add" / "log.jsonl"
)

# ----------------------------------------------------------------------
# Curated input --- 23 scout-cited papers (see task brief).
# ----------------------------------------------------------------------

PAPERS: list[dict[str, Any]] = [
    {"tier": 1, "short_cite": "carleton_2025_nature_cities", "doi": "10.1038/s44284-025-00213-1", "title": "Parallel scaling of elite wealth in ancient Roman and modern cities with implications for understanding urban inequality", "venue": "Nature Cities", "year": 2025, "oa_status": "OA", "pdf_url": "https://www.nature.com/articles/s44284-025-00213-1.pdf", "item_type_override": None},
    {"tier": 1, "short_cite": "carleton_campbell_collard_2018_plos_one", "doi": "10.1371/journal.pone.0191055", "title": "Radiocarbon dating uncertainty and the reliability of the PEWMA method of time-series analysis for research on long-term human-environment interaction", "venue": "PLOS ONE", "year": 2018, "oa_status": "OA", "pdf_url": "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0191055&type=printable", "item_type_override": None},
    {"tier": 1, "short_cite": "glomb_kase_hermankova_2022_jasrep", "doi": "10.1016/j.jasrep.2022.103466", "title": "Popularity of the cult of Asclepius in the times of the Antonine Plague: Temporal modeling of epigraphic evidence", "venue": "Journal of Archaeological Science: Reports", "year": 2022, "oa_status": "OA", "pdf_url": None, "item_type_override": None},
    {"tier": 1, "short_cite": "ortman_lobo_2024_sci_adv", "doi": "10.1126/sciadv.adk5517", "title": "Identification and measurement of intensive economic growth in a Roman imperial province", "venue": "Science Advances", "year": 2024, "oa_status": "OA", "pdf_url": "https://www.science.org/doi/pdf/10.1126/sciadv.adk5517", "item_type_override": None},
    {"tier": 1, "short_cite": "shennan_2013_nat_comm", "doi": "10.1038/ncomms3486", "title": "Regional population collapse followed initial agriculture booms in mid-Holocene Europe", "venue": "Nature Communications", "year": 2013, "oa_status": "OA", "pdf_url": "https://www.nature.com/articles/ncomms3486.pdf", "item_type_override": None},
    {"tier": 1, "short_cite": "bevan_2017_pnas", "doi": "10.1073/pnas.1709190114", "title": "Holocene fluctuations in human population demonstrate repeated links to food production and climate", "venue": "Proceedings of the National Academy of Sciences", "year": 2017, "oa_status": "OA", "pdf_url": "https://www.pnas.org/doi/pdf/10.1073/pnas.1709190114", "item_type_override": None},
    {"tier": 1, "short_cite": "kase_hermankova_sobotkova_2022_plos_one", "doi": "10.1371/journal.pone.0269869", "title": "Division of labor, specialization and diversity in the ancient Roman cities: A quantitative approach to Latin epigraphy", "venue": "PLOS ONE", "year": 2022, "oa_status": "OA", "pdf_url": "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0269869&type=printable", "item_type_override": None},
    {"tier": 1, "short_cite": "grossmann_weinelt_muller_2023_plos_one", "doi": "10.1371/journal.pone.0291956", "title": "Demographic dynamics between 5500 and 3500 calBP (3550-1550 BCE) in selected study regions of Central Europe and the role of regional climate influences", "venue": "PLOS ONE", "year": 2023, "oa_status": "OA", "pdf_url": "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0291956&type=printable", "item_type_override": None},
    {"tier": 1, "short_cite": "collard_carleton_campbell_2021_plos_one", "doi": "10.1371/journal.pone.0253043", "title": "Rainfall, temperature, and Classic Maya conflict: A comparison of hypotheses using Bayesian time-series analysis", "venue": "PLOS ONE", "year": 2021, "oa_status": "OA", "pdf_url": "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0253043&type=printable", "item_type_override": None},
    {"tier": 2, "short_cite": "carleton_groucutt_2020_holocene", "doi": "10.1177/0959683620981700", "title": "Sum things are not what they seem: Problems with point-wise interpretations and quantitative analyses of proxies based on aggregated radiocarbon dates", "venue": "The Holocene", "year": 2020, "oa_status": "OA", "pdf_url": "https://journals.sagepub.com/doi/pdf/10.1177/0959683620981700", "item_type_override": None},
    {"tier": 3, "short_cite": "palmisano_2021_italy_j_world_prehistory", "doi": "10.1007/s10963-021-09159-3", "title": "Long-Term Demographic Trends in Prehistoric Italy: Climate Impacts and Regionalised Socio-Ecological Trajectories", "venue": "Journal of World Prehistory", "year": 2021, "oa_status": "paywalled", "pdf_url": None, "item_type_override": None},
    {"tier": 3, "short_cite": "palmisano_2021_neareast_qsr", "doi": "10.1016/j.quascirev.2020.106739", "title": "Holocene regional population dynamics and climatic trends in the Near East: A first comparison using archaeo-demographic proxies", "venue": "Quaternary Science Reviews", "year": 2021, "oa_status": "paywalled", "pdf_url": None, "item_type_override": None},
    {"tier": 3, "short_cite": "timpson_2014_jas", "doi": "10.1016/j.jas.2014.08.011", "title": "Reconstructing regional population fluctuations in the European Neolithic using radiocarbon dates: a new case-study using an improved method", "venue": "Journal of Archaeological Science", "year": 2014, "oa_status": "paywalled", "pdf_url": None, "item_type_override": None},
    {"tier": 3, "short_cite": "meyer_1990_jrs", "doi": "10.2307/300281", "title": "Explaining the Epigraphic Habit in the Roman Empire: The Evidence of Epitaphs", "venue": "Journal of Roman Studies", "year": 1990, "oa_status": "paywalled", "pdf_url": None, "item_type_override": None},
    {"tier": 3, "short_cite": "beltran_lloris_2015_ohre_chapter", "doi": None, "title": "The Epigraphic Habit in the Roman World", "venue": "The Oxford Handbook of Roman Epigraphy", "year": 2015, "oa_status": "paywalled", "pdf_url": None, "item_type_override": "bookSection"},
    {"tier": 3, "short_cite": "woolf_1996_jrs", "doi": "10.2307/300421", "title": "Monumental Writing and the Expansion of Roman Society in the Early Empire", "venue": "Journal of Roman Studies", "year": 1996, "oa_status": "paywalled", "pdf_url": None, "item_type_override": None},
    {"tier": 3, "short_cite": "gelman_goodrich_gabry_vehtari_2019_amstat", "doi": "10.1080/00031305.2018.1549100", "title": "R-squared for Bayesian Regression Models", "venue": "The American Statistician", "year": 2019, "oa_status": "paywalled", "pdf_url": None, "item_type_override": None},
    {"tier": 3, "short_cite": "hanson_2022_jua_scalograms", "doi": "10.1484/j.jua.5.129843", "title": "Urban Scalograms: An Experiment in Scaling, Emergence, and Greek and Roman Urban Form", "venue": "Journal of Urban Archaeology", "year": 2022, "oa_status": "unknown", "pdf_url": None, "item_type_override": None},
    {"tier": 3, "short_cite": "hanson_2023_jamt_pompeii", "doi": "10.1007/s10816-023-09604-x", "title": "Scaling in Pompeii: Preliminary Evidence for the Occurrence of Scaling Phenomena Within an Ancient Built Environment", "venue": "Journal of Archaeological Method and Theory", "year": 2023, "oa_status": "unknown", "pdf_url": None, "item_type_override": None},
    {"tier": 3, "short_cite": "smith_2023_cup_monograph", "doi": "10.1017/9781009249027", "title": "Urban Life in the Distant Past: The Prehistory of Energized Crowding", "venue": "Cambridge University Press", "year": 2023, "oa_status": "paywalled", "pdf_url": None, "item_type_override": "book"},
    {"tier": 3, "short_cite": "altaweel_palmisano_2018_jamt", "doi": "10.1007/s10816-018-9400-4", "title": "Urban and Transport Scaling: Northern Mesopotamia in the Late Chalcolithic and Bronze Age", "venue": "Journal of Archaeological Method and Theory", "year": 2018, "oa_status": "paywalled", "pdf_url": None, "item_type_override": None},
    {"tier": 3, "short_cite": "lobo_bettencourt_ortman_2024_epb", "doi": "10.1177/23998083241308418", "title": "Urban scaling theory: Answers to frequent questions", "venue": "Environment and Planning B", "year": 2024, "oa_status": "paywalled", "pdf_url": None, "item_type_override": None},
    {"tier": 3, "short_cite": "benefiel_keesling_2024_brill_volume", "doi": None, "title": "Inscriptions and the Epigraphic Habit: The Epigraphic Cultures of Greece, Rome, and Beyond", "venue": "Brill Studies in Greek and Roman Epigraphy", "year": 2024, "oa_status": "paywalled", "pdf_url": None, "item_type_override": "book"},
]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------


def now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""

    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalise_doi(raw: str | None) -> str | None:
    """Return a lowercased DOI with common URL/``doi:`` prefixes stripped.

    Args:
        raw: A raw DOI string (or ``None``).

    Returns:
        The normalised DOI, or ``None`` if ``raw`` is falsy.
    """

    if not raw:
        return None
    doi = raw.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi = doi[len(prefix):]
    return doi.strip()


def log_event(record: dict[str, Any]) -> None:
    """Append a single JSON record to the run log.

    The log is flushed immediately so that partial progress survives
    an interruption (e.g., ``KeyboardInterrupt``).

    Args:
        record: A JSON-serialisable dict. A ``timestamp`` key is added
            automatically if not already present.
    """

    record.setdefault("timestamp", now_iso())
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


#: Lazy cache of ``normalised_DOI -> item dict`` for the whole SDAM group.
#: Populated on first call to :func:`search_by_doi`. Zotero's ``q=`` search
#: does NOT index the DOI field, so we build our own index by paging the
#: full group and reading the DOI from each item's ``data`` (plus any
#: ``extra`` field containing ``DOI: ...``). This is O(N) on first call
#: and O(1) thereafter.
_DOI_INDEX: dict[str, dict[str, Any]] | None = None


def _build_doi_index(zot: zotero.Zotero) -> dict[str, dict[str, Any]]:
    """Page the full SDAM group and return a DOI → item-dict index.

    Includes both top-level items and child items so that a DOI found
    only in a note or attachment (rare) would still be detected. Items
    without a DOI are skipped. If duplicate DOIs exist, the first one
    encountered wins (the caller should be alerted separately).
    """

    index: dict[str, dict[str, Any]] = {}
    start = 0
    page_size = 100
    while True:
        batch = zot.items(start=start, limit=page_size)
        if not batch:
            break
        for item in batch:
            data = item.get("data", {})
            candidates: list[str | None] = [data.get("DOI")]
            extra = data.get("extra", "") or ""
            for line in extra.splitlines():
                if line.lower().startswith("doi:"):
                    candidates.append(line.split(":", 1)[1])
            for raw in candidates:
                key = normalise_doi(raw)
                if key:
                    index.setdefault(key, item)
        if len(batch) < page_size:
            break
        start += page_size
    return index


def search_by_doi(zot: zotero.Zotero, doi: str) -> dict[str, Any] | None:
    """Return the SDAM item whose DOI matches ``doi`` (normalised).

    Uses a lazily-built DOI index over the whole group because Zotero's
    ``q=`` parameter does NOT search the DOI field (it searches titles,
    creators, notes, tags, and attachment filenames only).

    Args:
        zot: An authenticated :class:`pyzotero.zotero.Zotero` client.
        doi: A normalised DOI (lowercase, no URL/``doi:`` prefix).

    Returns:
        The matching item dict, or ``None`` if no match is found.
    """

    global _DOI_INDEX
    target = normalise_doi(doi)
    if not target:
        return None
    if _DOI_INDEX is None:
        _DOI_INDEX = _build_doi_index(zot)
    return _DOI_INDEX.get(target)


def fetch_crossref(doi: str) -> dict[str, Any] | None:
    """Fetch CrossRef metadata for a DOI.

    Args:
        doi: A normalised DOI.

    Returns:
        The ``message`` sub-dict of the CrossRef response, or ``None``
        on failure.
    """

    try:
        resp = requests.get(
            f"https://api.crossref.org/works/{doi}",
            params={"mailto": CROSSREF_MAILTO},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("message")
    except Exception as exc:  # noqa: BLE001 --- broad catch is intentional
        log_event(
            {
                "event": "crossref_error",
                "doi": doi,
                "error": f"{type(exc).__name__}: {exc}",
            }
        )
        return None


def _issued_date(message: dict[str, Any]) -> str:
    """Return an ISO-8601 date string from CrossRef ``issued.date-parts``."""

    parts = (
        message.get("issued", {}).get("date-parts", [[]]) or [[]]
    )[0]
    if not parts:
        return ""
    if len(parts) == 1:
        return f"{parts[0]:04d}"
    if len(parts) == 2:
        return f"{parts[0]:04d}-{parts[1]:02d}"
    return f"{parts[0]:04d}-{parts[1]:02d}-{parts[2]:02d}"


def _creators_from_crossref(
    message: dict[str, Any], creator_type: str = "author"
) -> list[dict[str, str]]:
    """Convert CrossRef ``author``/``editor`` lists to Zotero creators."""

    key = "author" if creator_type == "author" else "editor"
    out: list[dict[str, str]] = []
    for person in message.get(key, []) or []:
        entry: dict[str, str] = {"creatorType": creator_type}
        given = person.get("given")
        family = person.get("family")
        if given or family:
            entry["firstName"] = given or ""
            entry["lastName"] = family or ""
        elif person.get("name"):
            # Corporate author --- use single-field form.
            entry = {"creatorType": creator_type, "name": person["name"]}
        else:
            continue
        out.append(entry)
    return out


def build_item_from_crossref(
    zot: zotero.Zotero,
    message: dict[str, Any],
    item_type_override: str | None = None,
) -> dict[str, Any]:
    """Populate a Zotero item template from CrossRef metadata.

    Args:
        zot: Authenticated pyzotero client (used for ``item_template``).
        message: CrossRef ``message`` sub-dict.
        item_type_override: If given, forces this pyzotero item type
            instead of mapping from CrossRef ``type``.

    Returns:
        A fully populated item dict ready for ``zot.create_items([...])``.
    """

    cr_type = (message.get("type") or "").lower()
    item_type = item_type_override or CROSSREF_TYPE_MAP.get(
        cr_type, "journalArticle"
    )
    template: dict[str, Any] = zot.item_template(item_type)

    # Title: CrossRef returns a list (sometimes with subtitle merged in).
    titles = message.get("title") or []
    subtitles = message.get("subtitle") or []
    full_title = titles[0] if titles else ""
    if subtitles:
        full_title = f"{full_title}: {subtitles[0]}" if full_title else subtitles[0]
    template["title"] = full_title

    template["DOI"] = message.get("DOI", "")
    template["url"] = message.get("URL", "")
    template["abstractNote"] = message.get("abstract", "") or ""

    # Publication venue --- field name depends on item type.
    container = (message.get("container-title") or [""])[0]
    if item_type == "journalArticle":
        template["publicationTitle"] = container
        template["volume"] = message.get("volume", "") or ""
        template["issue"] = message.get("issue", "") or ""
        template["pages"] = message.get("page", "") or ""
    elif item_type == "bookSection":
        template["bookTitle"] = container
        template["pages"] = message.get("page", "") or ""
    elif item_type == "book":
        # For ``book``, ``publisher`` is the relevant field; keep the
        # container (series) in ``series`` if present.
        if "series" in template:
            template["series"] = container
    elif item_type == "preprint":
        template["repository"] = container
    elif item_type == "conferencePaper":
        template["proceedingsTitle"] = container

    if "publisher" in template:
        template["publisher"] = message.get("publisher", "") or ""

    template["date"] = _issued_date(message)

    # Creators: authors always; editors for books/chapters.
    creators = _creators_from_crossref(message, "author")
    if item_type in {"book", "bookSection"}:
        creators += _creators_from_crossref(message, "editor")
    template["creators"] = creators

    # ISBN (books only).
    if item_type == "book" and "ISBN" in template:
        isbns = message.get("ISBN") or []
        if isbns:
            template["ISBN"] = isbns[0]

    template["collections"] = [SPA_COLLECTION_KEY]
    return template


def download_and_verify_pdf(
    url: str, dest: Path
) -> tuple[bool, str]:
    """Download a PDF and verify its first four bytes are ``%PDF``.

    Args:
        url: Direct download URL.
        dest: Destination file path.

    Returns:
        A tuple ``(ok, status)`` where ``status`` is one of
        ``"downloaded"``, ``"invalid_magic_bytes"``, or
        ``"download_failed"``.
    """

    try:
        resp = requests.get(url, timeout=60, allow_redirects=True)
        resp.raise_for_status()
    except Exception:  # noqa: BLE001
        return False, "download_failed"
    data = resp.content
    if not data.startswith(b"%PDF"):
        return False, "invalid_magic_bytes"
    dest.write_bytes(data)
    return True, "downloaded"


# ----------------------------------------------------------------------
# Per-paper processing
# ----------------------------------------------------------------------


def process_paper(
    zot: zotero.Zotero,
    paper: dict[str, Any],
    new_items_created: int,
) -> tuple[str, int]:
    """Process a single paper: idempotency check, create, attach PDF.

    Args:
        zot: Authenticated pyzotero client.
        paper: One entry from :data:`PAPERS`.
        new_items_created: How many items have already been created in
            this run (for enforcing :data:`MAX_NEW_ITEMS`).

    Returns:
        A tuple ``(action, new_items_created_after)``.
    """

    short_cite = paper["short_cite"]
    raw_doi = paper.get("doi")
    doi = normalise_doi(raw_doi)

    # No DOI --- we can't deduplicate or fetch CrossRef. Skip with flag.
    if not doi:
        log_event(
            {
                "short_cite": short_cite,
                "action": "skipped_no_doi",
                "key": None,
                "pdf_status": None,
                "note": "No DOI; add manually via Zotero web UI.",
            }
        )
        return "skipped_no_doi", new_items_created

    # --- 1. Idempotency: search by DOI. ---
    existing = search_by_doi(zot, doi)
    if existing is not None:
        item_key = existing["key"]
        collections = existing.get("data", {}).get("collections", []) or []
        if SPA_COLLECTION_KEY in collections:
            log_event(
                {
                    "short_cite": short_cite,
                    "action": "already_complete",
                    "key": item_key,
                    "pdf_status": None,
                }
            )
            return "already_complete", new_items_created
        # Exists in SDAM but not in SPA --- link it.
        assert str(zot.library_id) == SDAM_GROUP_ID  # belt-and-braces
        try:
            zot.addto_collection(SPA_COLLECTION_KEY, existing)
            log_event(
                {
                    "short_cite": short_cite,
                    "action": "added_to_spa",
                    "key": item_key,
                    "pdf_status": None,
                }
            )
            return "added_to_spa", new_items_created
        except Exception as exc:  # noqa: BLE001
            log_event(
                {
                    "short_cite": short_cite,
                    "action": "failed",
                    "key": item_key,
                    "pdf_status": None,
                    "error": f"addto_collection: {type(exc).__name__}: {exc}",
                }
            )
            return "failed", new_items_created

    # --- 2. Guard against exceeding creation cap. ---
    if new_items_created >= MAX_NEW_ITEMS:
        log_event(
            {
                "short_cite": short_cite,
                "action": "failed",
                "key": None,
                "pdf_status": None,
                "error": f"MAX_NEW_ITEMS ({MAX_NEW_ITEMS}) reached; not creating.",
            }
        )
        return "failed", new_items_created

    # --- 3. Fetch CrossRef metadata. ---
    time.sleep(CROSSREF_DELAY_S)
    message = fetch_crossref(doi)
    if message is None:
        log_event(
            {
                "short_cite": short_cite,
                "action": "skipped_doi_not_found",
                "key": None,
                "pdf_status": None,
                "error": "CrossRef lookup returned no metadata.",
            }
        )
        return "skipped_doi_not_found", new_items_created

    # --- 4. Build item and create. ---
    template = build_item_from_crossref(
        zot, message, item_type_override=paper.get("item_type_override")
    )
    assert str(zot.library_id) == SDAM_GROUP_ID  # belt-and-braces
    try:
        result = zot.create_items([template])
    except Exception as exc:  # noqa: BLE001
        log_event(
            {
                "short_cite": short_cite,
                "action": "failed",
                "key": None,
                "pdf_status": None,
                "error": f"create_items: {type(exc).__name__}: {exc}",
            }
        )
        return "failed", new_items_created

    successful = result.get("successful", {}) or {}
    if not successful:
        log_event(
            {
                "short_cite": short_cite,
                "action": "failed",
                "key": None,
                "pdf_status": None,
                "error": f"create_items returned no successes: {result}",
            }
        )
        return "failed", new_items_created

    # pyzotero keys ``successful`` by stringified index, typically "0".
    first_key = next(iter(successful))
    new_item = successful[first_key]
    new_key = new_item.get("key") or new_item.get("data", {}).get("key")
    new_items_created += 1

    # --- 5. PDF attachment (OA only). ---
    pdf_status: str | None
    pdf_url = paper.get("pdf_url")
    oa_status = paper.get("oa_status")
    if not pdf_url:
        pdf_status = "not_oa" if oa_status == "paywalled" else "skipped_paywalled"
    else:
        pdf_path = Path(f"/tmp/zotero_pdf_{short_cite}.pdf")
        ok, dl_status = download_and_verify_pdf(pdf_url, pdf_path)
        if not ok:
            pdf_status = dl_status
        else:
            try:
                zot.attachment_simple([str(pdf_path)], new_key)
                pdf_status = "attached"
            except Exception as exc:  # noqa: BLE001
                pdf_status = f"attach_failed: {type(exc).__name__}: {exc}"

    log_event(
        {
            "short_cite": short_cite,
            "action": "created",
            "key": new_key,
            "pdf_status": pdf_status,
        }
    )
    return "created", new_items_created


# ----------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------


def build_client() -> zotero.Zotero:
    """Instantiate and sanity-check the Zotero client."""

    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.environ["ZOTERO_API_KEY"]
    group_id = os.environ.get("ZOTERO_GROUP_ID", SDAM_GROUP_ID)
    assert str(group_id) == SDAM_GROUP_ID, (
        f"Refusing to run: ZOTERO_GROUP_ID={group_id!r} != {SDAM_GROUP_ID!r}"
    )
    zot = zotero.Zotero(group_id, "group", api_key)
    assert str(zot.library_id) == SDAM_GROUP_ID
    return zot


def run(papers: Iterable[dict[str, Any]]) -> dict[str, int]:
    """Run the batch-add procedure over ``papers``.

    Args:
        papers: Iterable of paper dicts (see :data:`PAPERS`).

    Returns:
        Counts keyed by action name.
    """

    zot = build_client()
    # Print key scope for the caller's confirmation.
    try:
        info = zot.key_info()
        print(
            "Key access:",
            json.dumps(info.get("access", {}), sort_keys=True),
            file=sys.stderr,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: key_info() failed: {exc}", file=sys.stderr)

    counts: dict[str, int] = {
        "created": 0,
        "already_complete": 0,
        "added_to_spa": 0,
        "failed": 0,
        "skipped_no_doi": 0,
        "skipped_doi_not_found": 0,
    }
    new_items_created = 0
    consec_errors = 0

    for paper in papers:
        try:
            action, new_items_created = process_paper(
                zot, paper, new_items_created
            )
        except Exception as exc:  # noqa: BLE001
            action = "failed"
            log_event(
                {
                    "short_cite": paper.get("short_cite"),
                    "action": "failed",
                    "key": None,
                    "pdf_status": None,
                    "error": f"uncaught: {type(exc).__name__}: {exc}",
                }
            )

        counts[action] = counts.get(action, 0) + 1
        if action == "failed":
            consec_errors += 1
            if consec_errors >= MAX_CONSECUTIVE_ERRORS:
                log_event(
                    {
                        "event": "aborted",
                        "reason": (
                            f"{MAX_CONSECUTIVE_ERRORS} consecutive errors"
                        ),
                    }
                )
                print(
                    "ABORTED: hit MAX_CONSECUTIVE_ERRORS", file=sys.stderr
                )
                break
        else:
            consec_errors = 0

    return counts


def main() -> int:
    """Command-line entry point."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--test",
        action="store_true",
        help=(
            "Run the single test paper (Carleton, Campbell & Collard "
            "2018 PLOS ONE) only."
        ),
    )
    args = parser.parse_args()

    if args.test:
        papers = [
            p
            for p in PAPERS
            if p["short_cite"] == "carleton_campbell_collard_2018_plos_one"
        ]
    else:
        papers = PAPERS

    counts = run(papers)

    print("\n=== Summary ===")
    for k, v in counts.items():
        print(f"  {k:25s}: {v}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
