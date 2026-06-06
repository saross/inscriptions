# Inscriptions project — CLAUDE.md

Project-specific instructions for the inscriptions / LIRE SPA paper. Supplements
`~/Code/CLAUDE.md` (coding-mentor defaults) and `~/.claude/CLAUDE.md` (global).
Add genuinely inscriptions-specific guidance here; do not duplicate the parents.

## Shared tooling — use it; do not reimplement

Literature discovery, citation metadata, and Zotero import are handled by
**canonical, cross-project tooling in `~/personal-assistant/scripts/`**. Before
writing *any* bespoke utility for literature / citation / Zotero / lit-scout
work, check there first. Reimplementing this locally is a recurring mistake — on
2026-06-06 three bespoke per-batch staging scripts were written before noticing
the shared importer already existed (now archived; see below).

- **`~/personal-assistant/scripts/lit-search.py`** — metadata fetch
  (CrossRef → DataCite → OpenAlex, plus Semantic Scholar), with HTTP-429
  retry/backoff and per-host pacing. Backs `/lit-scout`, `/cite`, etc.
  Subcommands include `metadata <doi>` and `bibtex <doi> [...]`.
- **`~/personal-assistant/scripts/lit-scout-zotero-import.py`** — imports a
  `/lit-scout-iterate` workspace into a Zotero **user-library** staging
  subcollection. Handles CrossRef → DataCite → OpenAlex metadata, item-type
  mapping, SQLite dedup (across the whole library, including group libraries),
  and provenance notes.
  **Interface:** `python lit-scout-zotero-import.py <workspace> [--query "…"]
  [--live] [--limit N]` — **dry-run by default; pass `--live` to write.**
- Reference: `~/personal-assistant/global-claude-md/zotero-reference.md`.

### Canonical pattern for staging lit-scout finds

Run **`/lit-scout-iterate`** (it produces the workspace, with
`iter-N/claims.jsonl` + `report.md`), then import that workspace:
`python ~/personal-assistant/scripts/lit-scout-zotero-import.py <workspace> --live`.
**Do not write per-batch bespoke staging scripts.**

### Known gaps in the shared importer → extend it, don't reimplement

The importer is **workspace-driven** (it needs a lit-scout-iterate workspace; it
does **not** take an ad-hoc DOI list), writes to the **user-library** staging
collection (not arbitrary group libraries), and does **not** attach PDFs. If you
need any of those — ad-hoc DOI staging, a group-library target, or Unpaywall
PDF-attach — **extend the shared tool on a branch**; do not add a new bespoke
local script. Reference implementations for the group-library + PDF-attach
features are archived at `archive/superseded-code/zotero-staging/`
(`zotero_batch_add.py`, `zotero_followup.py`).

### Archived bespoke staging code

`archive/superseded-code/zotero-staging/` holds the superseded bespoke Zotero
staging one-offs (`zotero_stage_methods_2026-06-*.py`, `zotero_batch_add.py`,
`zotero_followup.py`) — reference only; superseded by the shared tooling above.

## General principle

Before building a new utility for a cross-cutting concern (literature, citation,
Zotero, memory, scheduling, etc.), survey `~/personal-assistant/scripts/` and
`~/personal-assistant/global-claude-md/` for existing shared tooling first, and
prefer extending it over a project-local reimplementation.
