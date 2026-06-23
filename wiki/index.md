---
title: "Inscriptions wiki — index"
tags: [index, infrastructure]
created: 2026-06-23
updated: 2026-06-23
status: active
---

# Inscriptions project wiki

The per-project memory for the inscriptions / LIRE deconvolution paper, on the
canonical four-artefact `wiki/` layout (reference:
`~/personal-assistant/wiki/index.md`). Migrated from the legacy `docs/notes/` +
root `planning/` layout on **2026-06-23** (`chore/repo-reorg`); the path
concordance below resolves any stale reference in the historical run records under
`runs/` (which are deliberately *not* rewritten).

## Project layer

| Artefact | Path | Job |
|---|---|---|
| Continuity | [continuity.md](continuity.md) | Cross-session state — the load-bearing handoff doc (read at session start) |
| Working notes | [working-notes.md](working-notes.md) | Research record — the empirical, chronological lab notebook (Observations) |
| Reflections | [`reflections/`](reflections/) | Meta-research — session reflection, abductive reasoning, reasoning + session logs |
| User observations | [user-observations.md](user-observations.md) | Curated meta-observations about how we work together |
| Claude observations | [claude-observations.md](claude-observations.md) | Claude-owned register of how-we-work observations |
| Decision log | [decision-log.md](decision-log.md) | The numbered design-decisions register |
| Research intent | [research-intent.md](research-intent.md) | Project framing / charter |
| AI contributions | [ai-contributions.md](ai-contributions.md) | Living log of substantive AI intellectual contributions (RDA AI-disclosure practice) |
| Preregistration record | [`prereg/`](prereg/) | The lodged OSF prereg, four amendments, and the obligations/compliance audits |
| Planning | [`planning/`](planning/) | **Active** plans only (incl. [`future-papers/`](planning/future-papers/)) |

`working-notes.md` (research record) and `reflections/` (meta-research) are
separate layers — never write Observations into reflection docs, or vice versa.

## The rest of the repo (outside `wiki/`)

- `sources/` — bibliographic inputs (BibTeX + `annotated-bibliographies/`); living.
- `data/` — datasets (Hanson 2016, processed, `women.csv`).
- `runs/` — per-run artefacts (spec, code, outputs, REPORT.md) per analysis stage.
- `scripts/` — long-lived helper scripts.
- `reports/` — curated output reports (key-findings summary; LLM-use inventory).
- `archive/` — completed history (archive-don't-delete; categorical subdirs below).

## Path concordance (old → new, 2026-06-23 reorg)

References in `runs/` and other history-of-record docs use the **old** paths; they
are resolved here rather than rewritten.

| Old path | New path |
|---|---|
| `docs/notes/reflections/continuity.md` | `wiki/continuity.md` |
| `docs/notes/working-notes.md` | `wiki/working-notes.md` |
| `docs/notes/user-observations.md` | `wiki/user-observations.md` |
| `docs/notes/claude-observations.md` | `wiki/claude-observations.md` |
| `docs/notes/reflections/{abductive-reasoning,reasoning-log,session-log,session-reflection}.md` | `wiki/reflections/` |
| `docs/notes/reflections/continuity-2026-04-23.md` | `archive/beacons/` |
| `planning/decision-log.md` | `wiki/decision-log.md` |
| `planning/research-intent.md` | `wiki/research-intent.md` |
| `planning/ai-contributions.md` | `wiki/ai-contributions.md` |
| `planning/{preregistration-draft,preregistration-changelog}.md` | `wiki/prereg/` |
| `planning/{prereg-note-*,prereg-obligations-*}.md` | `wiki/prereg/` |
| `planning/osf-*.{md,pdf,txt}`, `planning/cross-model-adversarial-review-preregistration.md` | `wiki/prereg/` |
| `planning/{jamt-paper-outline,paper-writing-brief,paper-significance-and-applications-2026-06-03,paper-subsection-reachability,archive-search-crash-diagnosis-2026-06-21,baorista-install-plan,future-studies}.md` | `wiki/planning/` |
| `planning/hmm-paper-stub/README.md` | `wiki/planning/future-papers/hmm-followup.md` |
| `planning/paper-outlines/aeneas-partition.md` | `wiki/planning/future-papers/aeneas-partition.md` |
| `planning/{inscriptions-spa,inscriptions-aeneas}.bib` | `sources/` |
| `planning/bibliography-*.md` | `sources/annotated-bibliographies/` |
| `planning/{next-session-prompt-*,backlog-*,archive-2024-summary}.md` | `archive/beacons/` |
| `planning/{h2.1-*,h3a-*,spec-decision-33-harness-update-2026-06-03}.md` | `archive/specs/` |
| `planning/{prior-art-scout-*,lit-scout-*,scout-2026-06-09-*}` | `archive/scouts/` |
| `planning/gemini-statistical-review.md`, `planning/chatgpt-*.md`, `planning/saturation-check-prompt-2026-05-17.md`, `planning/prereg-saturation-check-gemini.md` | `archive/cross-model-review/` |
| `planning/GPT55-statistical-review.md` | `archive/cross-model-review/gpt55-statistical-review.md` *(renamed)* |
| `planning/prereg-saturation-check-GPT55.md` | `archive/cross-model-review/prereg-saturation-check-gpt55.md` *(renamed)* |
| `planning/{doc-accuracy-audit-2026-06-20,recovery-grid-utility-review-2026-06-02,results-documentation-uplift-2026-06-20}.md` | `archive/audits/` |
| `planning/martin*.md`, `planning/cc-briefing-2026-04-22.md`, `planning/memos/*` | `archive/consultation/` |
| `planning/conference-talk-rac-trac-2026/` | `archive/planning/conference-talk-rac-trac-2026/` |

**Tags:** git tags `osf-lodgement-2026-05-20` and `osf-amendment-01..04` resolve by
commit, so they are unaffected by these path moves.

**Note on living-doc cross-references:** `wiki/continuity.md` and the active
`wiki/planning/` docs still carry some old-path references in their bodies; these
resolve via this concordance and refresh naturally as the docs are edited. Only the
README and the key-findings summary had their paths updated at reorg time.

## Provenance

Reorg proposal + decisions: [`planning/repo-reorg-proposal-2026-06-22.md`](planning/repo-reorg-proposal-2026-06-22.md).
Executed on branch `chore/repo-reorg`, batched logical commits, 2026-06-23.
