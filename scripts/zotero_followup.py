#!/usr/bin/env python3
"""Follow-up pass to ``zotero_batch_add.py`` (run 2026-04-24).

Addresses three residual gaps:

1. Four Portable Document Format (PDF) downloads failed during the initial
   batch-add — three with HTTP 403 / Cloudflare bot-detection (publisher
   sites) and one because no ``pdf_url`` was supplied in the curated input.
   This script finds Open-Access (OA) URLs via the Unpaywall API, then
   downloads with a browser-like ``User-Agent`` header, verifies the PDF
   magic bytes, and attaches via the Zotero API if valid.

2. Two items lack Digital Object Identifiers (DOIs) altogether — an
   Oxford Handbook chapter (Beltrán Lloris 2015) and a Brill edited
   volume (Benefiel & Keesling 2024). Manual templates are built from
   known metadata.

3. Everything is logged as JSONL for audit.

Idempotency: each PDF retry first checks whether the target item already
has a PDF attachment. Each manual add first checks whether an item with
a distinctive title fragment already exists. Safe to re-run.

Hard safety rails (mirror ``zotero_batch_add.py``):

* Assert ``library_id == '2366083'`` after client instantiation.
* No deletes, no metadata overwrites on existing items.
* Magic-byte verification before any PDF attachment.
"""

from __future__ import annotations

import json
import os
import pathlib
import time
from datetime import datetime, timezone
from typing import Any

import requests
from dotenv import load_dotenv
from pyzotero import zotero

load_dotenv("/home/shawn/Code/inscriptions/.env")
API_KEY = os.environ["ZOTERO_API_KEY"]
GROUP_ID = os.environ["ZOTERO_GROUP_ID"]
SPA_COLLECTION_KEY = "PZN5ATJK"
MAILTO = "shawn@faims.edu.au"
BROWSER_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

LOG_PATH = pathlib.Path(
    "/home/shawn/Code/inscriptions/runs/2026-04-24-zotero-batch-add/followup-log.jsonl"
)

zot = zotero.Zotero(GROUP_ID, "group", API_KEY)
assert str(zot.library_id) == "2366083", (
    f"Safety assertion failed: library_id={zot.library_id} (must be 2366083)"
)


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log(entry: dict[str, Any]) -> None:
    """Append one audit-record line to the JSONL log and echo to stdout."""
    entry.setdefault("timestamp", _ts())
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(json.dumps(entry, ensure_ascii=False))


def unpaywall_pdf_url(doi: str) -> str | None:
    """Query Unpaywall API for the best OA PDF URL for a DOI."""
    try:
        r = requests.get(
            f"https://api.unpaywall.org/v2/{doi}",
            params={"email": MAILTO},
            timeout=30,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        best = data.get("best_oa_location") or {}
        url = best.get("url_for_pdf")
        if url:
            return url
        # Fallback: any OA location's landing URL
        for loc in data.get("oa_locations") or []:
            if loc.get("url_for_pdf"):
                return loc["url_for_pdf"]
        return None
    except requests.RequestException:
        return None


def europepmc_pdf_url(doi: str) -> str | None:
    """Resolve DOI → PubMed Central ID → Europe PMC direct-PDF URL.

    Europe PMC's ``ptpmcrender.fcgi`` endpoint serves PDFs without the
    Cloudflare bot-detection that blocks the publisher-side PMC mirror.
    """
    try:
        r = requests.get(
            "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/",
            params={
                "tool": "inscriptions_project",
                "email": MAILTO,
                "ids": doi,
                "idtype": "doi",
                "format": "json",
            },
            timeout=30,
        )
        if r.status_code != 200:
            return None
        records = r.json().get("records") or []
        if not records:
            return None
        pmcid = records[0].get("pmcid")
        if not pmcid:
            return None
        return (
            f"https://europepmc.org/backend/ptpmcrender.fcgi"
            f"?accid={pmcid}&blobtype=pdf"
        )
    except requests.RequestException:
        return None


def download_pdf_with_ua(url: str) -> bytes | None:
    """GET the URL with a browser UA; return bytes only if magic bytes match."""
    try:
        r = requests.get(
            url,
            headers={
                "User-Agent": BROWSER_UA,
                "Accept": "application/pdf,application/octet-stream,*/*",
            },
            timeout=90,
            allow_redirects=True,
        )
    except requests.RequestException:
        return None
    if r.status_code != 200:
        return None
    if not r.content[:4] == b"%PDF":
        return None
    return r.content


def has_pdf_attachment(item_key: str) -> bool:
    """Return True if the Zotero item already has a PDF attachment."""
    try:
        children = zot.children(item_key, itemType="attachment")
    except Exception:
        return False
    return any(
        c.get("data", {}).get("contentType") == "application/pdf" for c in children
    )


def retry_pdf(item_key: str, short_cite: str, doi: str) -> dict[str, Any]:
    """Attempt to attach a PDF to an existing item via Unpaywall + browser UA."""
    out: dict[str, Any] = {
        "op": "retry_pdf",
        "short_cite": short_cite,
        "item_key": item_key,
        "doi": doi,
    }
    if has_pdf_attachment(item_key):
        out["status"] = "already_has_pdf"
        return out

    # Try Unpaywall first; on miss, fall back to Europe PMC.
    url = unpaywall_pdf_url(doi)
    source = "unpaywall"
    content = download_pdf_with_ua(url) if url else None
    if not content:
        url = europepmc_pdf_url(doi)
        if url:
            source = "europe_pmc"
            content = download_pdf_with_ua(url)

    if not content:
        out["status"] = "no_oa_pdf_available"
        return out

    out["pdf_url"] = url
    out["pdf_source"] = source
    tmp_path = pathlib.Path(f"/tmp/zotero_{short_cite}.pdf")
    tmp_path.write_bytes(content)
    try:
        attach = zot.attachment_simple([str(tmp_path)], item_key)
        out["size_bytes"] = len(content)
        # pyzotero's attachment_simple returns a dict whose ``success`` /
        # ``successful`` entries can be either a dict of {idx: {key: ...}}
        # or a list of item keys — normalise both forms defensively.
        successful = attach.get("success") or attach.get("successful") or {}
        attachment_key: str | None = None
        if isinstance(successful, dict):
            for v in successful.values():
                if isinstance(v, dict) and v.get("key"):
                    attachment_key = v["key"]
                    break
                if isinstance(v, str):
                    attachment_key = v
                    break
        elif isinstance(successful, list):
            for v in successful:
                if isinstance(v, str):
                    attachment_key = v
                    break
                if isinstance(v, dict) and v.get("key"):
                    attachment_key = v["key"]
                    break
        out["status"] = "attached"
        if attachment_key:
            out["attachment_key"] = attachment_key
    except Exception as e:  # noqa: BLE001 — agent-facing report
        out["status"] = "attach_failed"
        out["error"] = f"{type(e).__name__}: {e}"
    finally:
        tmp_path.unlink(missing_ok=True)
    return out


def _find_by_title_and_author(title_fragment: str, author_fragment: str) -> str | None:
    """Return the item key of a matching item, or None."""
    try:
        results = zot.items(q=title_fragment, qmode="titleCreatorYear", limit=25)
    except Exception:
        return None
    for r in results:
        data = r.get("data", {})
        title = data.get("title", "")
        if title_fragment.lower() not in title.lower():
            continue
        creators = data.get("creators", [])
        for c in creators:
            if author_fragment.lower() in c.get("lastName", "").lower():
                return data.get("key")
    return None


def add_beltran_lloris_2015() -> dict[str, Any]:
    """Add the Oxford Handbook of Roman Epigraphy chapter manually."""
    out: dict[str, Any] = {
        "op": "manual_add",
        "short_cite": "beltran_lloris_2015_ohre_chapter",
    }
    existing = _find_by_title_and_author(
        "Epigraphic Habit in the Roman World", "Beltr"
    )
    if existing:
        out["status"] = "already_present"
        out["item_key"] = existing
        return out
    template = zot.item_template("bookSection")
    template["title"] = "The Epigraphic Habit in the Roman World"
    template["bookTitle"] = "The Oxford Handbook of Roman Epigraphy"
    template["creators"] = [
        {
            "creatorType": "author",
            "firstName": "Francisco",
            "lastName": "Beltrán Lloris",
        },
        {"creatorType": "editor", "firstName": "Christer", "lastName": "Bruun"},
        {"creatorType": "editor", "firstName": "Jonathan", "lastName": "Edmondson"},
    ]
    template["date"] = "2015"
    template["pages"] = "131–148"
    template["publisher"] = "Oxford University Press"
    template["place"] = "Oxford"
    template["ISBN"] = "9780195336467"
    template["collections"] = [SPA_COLLECTION_KEY]
    result = zot.create_items([template])
    successful = result.get("successful") or {}
    if successful:
        item = next(iter(successful.values()))
        out["status"] = "created"
        out["item_key"] = item.get("key")
    else:
        out["status"] = "create_failed"
        out["error"] = json.dumps(result, default=str)[:400]
    return out


def add_benefiel_keesling_2024() -> dict[str, Any]:
    """Add the Brill edited volume manually."""
    out: dict[str, Any] = {
        "op": "manual_add",
        "short_cite": "benefiel_keesling_2024_brill_volume",
    }
    existing = _find_by_title_and_author(
        "Inscriptions and the Epigraphic Habit", "Benefiel"
    )
    if existing:
        out["status"] = "already_present"
        out["item_key"] = existing
        return out
    template = zot.item_template("book")
    template["title"] = (
        "Inscriptions and the Epigraphic Habit: "
        "The Epigraphic Cultures of Greece, Rome, and Beyond"
    )
    template["creators"] = [
        {"creatorType": "editor", "firstName": "Rebecca", "lastName": "Benefiel"},
        {
            "creatorType": "editor",
            "firstName": "Catherine M.",
            "lastName": "Keesling",
        },
    ]
    template["date"] = "2024"
    template["publisher"] = "Brill"
    template["place"] = "Leiden"
    template["ISBN"] = "9789004683112"
    template["series"] = "Brill Studies in Greek and Roman Epigraphy"
    template["seriesNumber"] = "20"
    template["collections"] = [SPA_COLLECTION_KEY]
    result = zot.create_items([template])
    successful = result.get("successful") or {}
    if successful:
        item = next(iter(successful.values()))
        out["status"] = "created"
        out["item_key"] = item.get("key")
    else:
        out["status"] = "create_failed"
        out["error"] = json.dumps(result, default=str)[:400]
    return out


# Specific items to retry, from the 2026-04-24 batch-add run.
PDF_RETRIES: list[tuple[str, str, str]] = [
    ("K9NHZPDT", "ortman_lobo_2024_sci_adv", "10.1126/sciadv.adk5517"),
    ("GM82BQQI", "bevan_2017_pnas", "10.1073/pnas.1709190114"),
    ("4QMRBWB6", "carleton_groucutt_2020_holocene", "10.1177/0959683620981700"),
    ("PMVKIVN8", "glomb_kase_hermankova_2022_jasrep", "10.1016/j.jasrep.2022.103466"),
]


def main() -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log({"event": "run_start", "script": "zotero_followup.py"})

    created = 0
    attached = 0
    already = 0
    failed = 0

    for item_key, short_cite, doi in PDF_RETRIES:
        result = retry_pdf(item_key, short_cite, doi)
        log(result)
        status = result.get("status", "")
        if status == "attached":
            attached += 1
        elif status == "already_has_pdf":
            already += 1
        else:
            failed += 1
        time.sleep(1.0)  # Unpaywall etiquette

    for fn in (add_beltran_lloris_2015, add_benefiel_keesling_2024):
        result = fn()
        log(result)
        status = result.get("status", "")
        if status == "created":
            created += 1
        elif status == "already_present":
            already += 1
        else:
            failed += 1

    log(
        {
            "event": "run_end",
            "summary": {
                "created": created,
                "attached": attached,
                "already": already,
                "failed": failed,
            },
        }
    )
    print()
    print(f"created={created} attached={attached} already={already} failed={failed}")


if __name__ == "__main__":
    main()
