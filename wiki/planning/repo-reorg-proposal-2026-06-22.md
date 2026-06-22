---
title: "Inscriptions repo reorganisation — proposal"
tags: [infrastructure, coding-practices]
created: 2026-06-22
updated: 2026-06-22
status: PROPOSAL — awaiting Shawn; NO MOVES EXECUTED (read-only survey only)
---

# Inscriptions repo reorganisation — proposal

**Purpose:** bring this repo to the canonical four-artefact wiki layout and clear the
`planning/` accretion, separating active plans from completed history, research outputs,
and the registered (OSF) record. Creating this document **seeds `wiki/`** (additive; the
only change made so far).

**Authoritative layout reference:** `~/personal-assistant/wiki/index.md` ("PA project layer").
**Skill spec this executes by hand:** `~/personal-assistant/wiki/planning/repo-standardise-skill-spec.md`
(v2, not yet implemented; inscriptions is its #1 Full-tier target — §6).
**Worked-example precedent:** `~/Code/2026-mq-llm-dh-judgement-paper-b/wiki/planning/repo-reorg-proposal-2026-06-10.md`.

> **⚠ STATUS — this is a Phase-3 proposal. The spec mandates a STOP here.** Phases 0–2
> (preflight, survey, classify) were run **read-only** on 2026-06-22 (HEAD `7fbb578`,
> clean tree, `0 behind`). **No files have been moved, renamed, or deleted.** Execution
> (Phase 4) waits for Shawn to resolve the decision points in §4 and is done on a branch
> with a PR (Full-tier rule + the global branch-for-migrations rule). Safe to leave as-is
> indefinitely.

---

## 0. Tier & preflight (Phase 0)

- **Tier: Full** (active, solo-led research repo with layout debt). Authors:
  Shawn 721 commits; Brian Ballsun-Stanton 1 commit → effectively solo (renames allowed,
  concorded; direct authorship). `git shortlog -sne`.
- **Clean tree, `0 ahead/0 behind`** origin/main at survey time.
- **No submodules** (`.gitmodules` absent).
- **Remote:** `git@github.com:saross/inscriptions.git` (personal, not org).
- **Protected paths:** the **OSF / preregistration cluster** (registered research record —
  §4 D1) and per-repo `CLAUDE.md` (shared-tooling constraints; unaffected).

## 1. Diagnosis (Phase 1, verified 2026-06-22, HEAD `7fbb578`)

The repo is **already half-canonical**: `data/`, `scripts/`, `reports/`, `runs/`, and
`archive/` are role-true and stay put. The debt is concentrated in exactly two places.

**F-codes** reference the failure-mode catalogue in the skill spec §1.

1. **Legacy `docs/notes/` wiki layout (F3).** The four-artefact set lives under the old
   path: `docs/notes/{working-notes,user-observations,claude-observations}.md`,
   `docs/notes/reflections/{continuity,continuity-2026-04-23,abductive-reasoning,reasoning-log,session-log,session-reflection}.md`.
   `docs/` holds nothing else. `/handoff`, `/observe`, `/reflect`, `/obs-writer` are already
   layout-aware and will target `wiki/` once it exists.
2. **`planning/` as universal attractor (F1)** — 121 tracked files / 19 MB / 7 subdirs,
   holding **nine** distinct kinds of thing (active plans, governance docs, the OSF record,
   completed specs, scout/review/audit outputs, consultation packs, dated beacons, a
   delivered conference talk, bibliography). The classification in §3 untangles them.
3. **Continuity-beacon sprawl (F2).** Live beacon at `docs/notes/reflections/continuity.md`
   (the session-start protocol reads `wiki/continuity.md`, falling back to legacy — so a
   move *improves* discovery); plus 6 superseded beacon-ish docs in `planning/`
   (4 × `next-session-prompt-2026-05-*.md`, 2 × `backlog-2026-0*.md`) + a dated continuity
   snapshot (`continuity-2026-04-23.md`).
4. **Partial archive already exists (F3/F7).** `archive/planning/conference-talk-rac-trac-2026/`
   exists alongside the *live* `planning/conference-talk-rac-trac-2026/` (32 files, ~12 MB,
   talk delivered 2026-05-22) — finish the migration, don't duplicate.
5. **README drift (F5).** README last touched 2026-06-06 vs repo 2026-06-21; its structure
   section predates the figures, the women work, and the JAMT outline, and still points at
   `docs/notes/reflections/`.
6. **Minor naming (F6).** `GPT55-statistical-review.md` / `prereg-saturation-check-GPT55.md`
   use uppercase where the parallel `gemini-*` files are lowercase — low-priority concorded
   rename. (The ~hundreds of capitalised `*.json` files under `runs/` are **place-name data
   keys** — Aquileia, Beneventum, … — *not* violations; left alone.)

**Not problems here:** loose root is all-conventional (no junk); `runs/` heft is mostly
gitignored (2.4 GB on disk, only 1,953 tracked files across 62 run-dirs); only **5** tracked
files exceed 5 MB (4 in `archive/`, 1 an `h1-simulation` parquet) — a heft *note*, not a
reorg target.

## 2. Target layout

```text
inscriptions/
├── README.md                  # rewritten (Phase 6)
├── CLAUDE.md  LICENSE  PROVISIONING.md  pyproject.toml  uv.lock  .gitignore  .env.example   # unchanged
├── wiki/                      # NEW — canonical four-artefact layout
│   ├── index.md               # NEW — orientation + path concordance (old → new)
│   ├── continuity.md          # ← docs/notes/reflections/continuity.md (the live beacon)
│   ├── working-notes.md       # ← docs/notes/working-notes.md
│   ├── user-observations.md   # ← docs/notes/user-observations.md
│   ├── claude-observations.md # ← docs/notes/claude-observations.md
│   ├── decision-log.md        # ← planning/decision-log.md     (governance → wiki)
│   ├── research-intent.md     # ← planning/research-intent.md  (governance → wiki)
│   ├── reflections/           # ← docs/notes/reflections/ (4 meta-research logs)
│   └── planning/              # ACTIVE plans only (see §3-C)
├── data/                      # unchanged (inputs: hanson2016/, processed/, women.csv)
├── scripts/                   # unchanged (7 analysis/build scripts)
├── reports/                   # unchanged (key-findings-summary, llm-use-inventory)
├── runs/                      # unchanged (62 analysis run-dirs — the research record)
└── archive/                   # expanded, archive-don't-delete, categorical subdirs (§3-D)
```

`docs/` ceases to exist (held only `notes/`). Top level becomes eight role-true entries:
`wiki/` = project memory, `data/` = inputs, `scripts/` = code, `reports/` = curated outputs,
`runs/` = run record/workspace, `archive/` = completed history, plus README + config.

## 3. Classification — every current item → target

### A. wiki migration (`docs/notes/` → `wiki/`)

| Current | Target | Action |
|---|---|---|
| `docs/notes/reflections/continuity.md` | `wiki/continuity.md` | `git mv` (live beacon) |
| `docs/notes/working-notes.md` | `wiki/working-notes.md` | `git mv` |
| `docs/notes/user-observations.md` | `wiki/user-observations.md` | `git mv` |
| `docs/notes/claude-observations.md` | `wiki/claude-observations.md` | `git mv` |
| `docs/notes/reflections/{abductive-reasoning,reasoning-log,session-log,session-reflection}.md` | `wiki/reflections/` | `git mv` |
| `docs/notes/reflections/continuity-2026-04-23.md` | `archive/beacons/` *(D4)* | `git mv` (dated snapshot, superseded) |
| — | `wiki/index.md` | **new** (orientation + concordance) |
| `docs/` (now empty) | — | removed |

### B. governance docs (`planning/` → `wiki/`)

| Current | Target |
|---|---|
| `planning/decision-log.md` | `wiki/decision-log.md` |
| `planning/research-intent.md` | `wiki/research-intent.md` |
| `planning/ai-contributions.md` | **D3** — `reports/` (beside `llm-use-inventory.md`) or `wiki/` or archive |

### C. active plans (`planning/` → `wiki/planning/`)

`jamt-paper-outline.md`, `paper-writing-brief.md`,
`paper-significance-and-applications-2026-06-03.md`, `paper-subsection-reachability.md`,
`archive-search-crash-diagnosis-2026-06-21.md`, `baorista-install-plan.md`,
`future-studies.md`, and **this document** (already there). Bibliography
(`inscriptions-spa.bib`, `bibliography-2026-04-22.md`) → `wiki/planning/` for now, or a new
`sources/` (**D5**, low priority).

### D. completed history (`planning/` → `archive/<category>/`)

| Category (new archive subdir) | Members |
|---|---|
| `archive/beacons/` | 4 × `next-session-prompt-2026-05-{17,18,21,22}.md`; `backlog-2026-04-22.md`; `backlog-2026-05-03.md`; `archive-2024-summary.md` |
| `archive/specs/` | 5 × `h2.1-*.md`; `h3a-confirmatory-launch-spec-2026-06-04.md`; `h3a-design-artefact-2026-06-04.md`; `spec-decision-33-harness-update-2026-06-03.md` |
| `archive/scouts/` | `lit-scout-2026-05-25-pottery-aoristic-roman/`; `lit-scout-2026-06-19-aoristic-mc-misclassification-bias/`; `prior-art-scout-2026-04-25-aoristic-envelope.md`; `prior-art-scout-2026-05-19-hmm-aoristic.md`; `prior-art-scout-2026-05-25-ceramics-aoristic-techniques/`; `prior-art-scout-2026-06-02-recovery-validation-metrics.md`; `scout-2026-06-09-identifiability-remediation-SYNTHESIS.md` |
| `archive/cross-model-review/` | `gemini-statistical-review.md`; `GPT55-statistical-review.md`; `chatgpt-review-triage.md`; `chatgpt-cross-model-review-prompt.md`; `prereg-saturation-check-gemini.md`; `prereg-saturation-check-GPT55.md`; `saturation-check-prompt-2026-05-17.md` |
| `archive/audits/` | `doc-accuracy-audit-2026-06-20.md`; `prereg-obligations-audit-2026-06-05.md`; `prereg-obligations-audit-2026-06-18.md`; `prereg-obligations-coverage-sweep-2026-06-20.md`; `results-documentation-uplift-2026-06-20.md`; `recovery-grid-utility-review-2026-06-02.md` |
| `archive/consultation/` | `martin.md`; `martin-consultation-pack-2026-05-17.md`; `martin-consultation-2026-05-25-followup.md`; `martin-review-statistical-grounds-2026-06-04.md`; `cc-briefing-2026-04-22.md`; `memos/2026-04-23-reflect-multi-invocation.md` |
| `archive/conference-talk-rac-trac-2026/` | merge live `planning/conference-talk-rac-trac-2026/` (32 files) into the existing `archive/planning/conference-talk-rac-trac-2026/` (delivered 2026-05-22) |

*Liveness flag:* a handful above are inferred-complete from filename + date + project
knowledge. Phase 4 re-greps each for live references before moving (rule below); any that
turns out live drops back to §3-C.

### E. OSF / preregistration cluster — **DECISION D1 (see §4)**

The 27 `osf-*` / `prereg*` / `preregistration*` / `cross-model-adversarial-review-preregistration.md`
files. **Not auto-moved.** Proposed: consolidate into `wiki/planning/prereg/` (keeps the record
together and discoverable), *conditional on* confirming nothing external links the in-repo
paths (§4 D1). `preregistration-changelog.md` is live and travels with the cluster.

### F. future companion paper (aeneas / HMM) — **DECISION D2**

`hmm-paper-stub/README.md`, `paper-outlines/aeneas-partition.md`,
`bibliography-aeneas-2026-04-23.md`, `inscriptions-aeneas.bib` — material for a *separate*
future paper. Proposed: group under `wiki/planning/future-papers/` (or leave; low urgency).

## 4. Decision points (resolve before Phase 4)

- **D1 — OSF/prereg cluster (the important one).** Move-with-care per spec rule 15. Git tags
  (`osf-lodgement-2026-05-20`, `osf-amendment-01..04`) point to *commits*, not paths, so a
  move is git-safe and tags still resolve. The risk is an **external link to an in-repo
  path** (the OSF registration page or the lodged supplementary). OSF hosts its own uploaded
  copies, so this is *likely* safe — but it needs your confirm. Options: **(a)** consolidate
  into `wiki/planning/prereg/` after you confirm no external pointer; **(b)** leave the
  cluster in a `planning/prereg/` subdir under the *old* path (minimal touch); **(c)** leave
  entirely in place. *Recommend (a) if you can confirm; (b) as the safe default.*
- **D2 — aeneas/HMM companion grouping** (§3-F): `wiki/planning/future-papers/` vs leave.
- **D3 — `ai-contributions.md` home**: `reports/` (beside `llm-use-inventory.md`) vs `wiki/`
  vs archive (if superseded by the inventory). *Recommend `reports/`.*
- **D4 — `continuity-2026-04-23.md`**: `archive/beacons/` (proposed) vs keep as historical in
  `wiki/reflections/`.
- **D5 — bibliography files**: `wiki/planning/` (proposed, minimal) vs a new `sources/` dir.
- **D6 — `GPT55-*` rename** to lowercase (`gpt55-*`) to match `gemini-*`: yes/no (concorded).
- **D7 — branch/PR**: `chore/repo-reorg` + PR (proposed, per Full-tier + global rule).

## 5. Reference integrity

- **Cross-repo (F8b): clean.** `git grep` of paper-b, map-reader, and LLM-History-Paper for
  inscriptions paths → **0 hits**. No sibling protocol depends on this repo's paths. (The 9
  hits in `~/personal-assistant` are doc/script *mentions* — `infrastructure-reference.md`,
  `llm-use-inventory.py --project inscriptions` [archive-subdir name, not a path],
  `search-archives-safe.sh`, wiki notes — none break on a move.)
- **Internal: 78 tracked files reference `planning/`/`docs/notes/` paths — but ~76 are inside
  `runs/`** (immutable spec/plan/code/REPORT records). Per the spec's live-vs-historical rule
  these are **history-of-record: NOT rewritten**; the concordance table in `wiki/index.md`
  resolves their stale paths. Rewriting them would falsify the research record.
- **Live docs that DO get path updates (the short list):**
  - `README.md` — full rewrite (Phase 6); currently points at `docs/notes/reflections/` and
    `planning/` (lines 11, 30, 34).
  - `reports/key-findings-summary-2026-06-20.md` — two references
    (`docs/notes/working-notes.md` L22; `planning/doc-accuracy-audit-2026-06-20.md` L590).
    Near-final deliverable: update the two paths (or let the concordance carry them — your
    call at execution).

## 6. Execution plan (Phase 4 — only after §4 is resolved)

Branch `chore/repo-reorg`, commits batched by logical area, then PR (D7). Each commit leaves
the tree internally consistent.

1. **wiki migration** — `git mv` the `docs/notes/` artefacts; create `wiki/index.md` (with
   the old→new concordance); remove the empty `docs/`.
2. **governance → wiki** — `git mv` `decision-log.md`, `research-intent.md`.
3. **archive sweep** — create `archive/<category>/` subdirs (§3-D) + `git mv`; add/extend
   `archive/README.md` noting categories and that pre-reorg paths inside refer to the old
   layout; merge the split conference-talk dir.
4. **active plans → wiki/planning** — `git mv` the §3-C set.
5. **OSF cluster** — per D1 resolution (may be a no-op).
6. **documentation** — README rewrite; concordance finalised.

## 7. Verification checklist (gate before PR/push)

- [ ] `git grep -nE 'docs/notes|planning/(decision-log|research-intent|martin|h2\.1|next-session)'`
      hits only `archive/`, `runs/` (history), and `wiki/` concordance/continuity.
- [ ] `git log --follow` spot-check on 3 moved files shows continuous history.
- [ ] Git tags `osf-lodgement-2026-05-20`, `osf-amendment-01..04` still resolve.
- [ ] `git status` clean; ignored paths still ignored at any new location.
- [ ] Session-start picks up `wiki/continuity.md` (next session confirms).
- [ ] No build/test breakage (scripts reference `data/`, `runs/`, not `planning/`).

## 8. Out of scope

- `runs/` internals, `data/`, `scripts/` — untouched (already role-true).
- Heft/data management beyond the note in §1 (no LFS, no `runs/` pruning).
- Content edits to moved documents (continuity stays the live doc; the only sanctioned
  live-doc edits are the README rewrite and the two key-findings-summary path fixes).
- History-of-record rewrites in `runs/` (concordance resolves them).
- Implementing the `repo-standardise` skill itself (separate infra task; this is the manual
  worked example that would inform it — like paper-b informed the spec).
