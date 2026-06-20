---
title: "LLM-Use Inventory — inscriptions"
purpose: "Supporting record for a Methods disclosure of large-language-model use"
generated: 2026-06-20
source: "~/cc-archives/inscriptions/ (session.meta.json across 30 archived sessions)"
status: draft
---

# LLM-Use Inventory — inscriptions

**Generated 2026-06-20** by `scripts/llm-use-inventory.py` from the local
Claude Code session archive. This is the **supporting (quantitative) half** of a
Methods disclosure; the **governance section below leads** and must be completed
by the author — see `notes/llm-use-disclosure-standard.md` for the full standard.
This is a **draft working record** — verify and adapt before submission.

## 1. Governance and author control (author to complete — this leads the disclosure)

> The control claim rests here, not on the interaction counts in §3. A reviewer
> reads prompt and subagent counts as evidence of *interaction*, not *oversight*.
> Fill the apparatus that actually evidences author control, for example:

- [ ] **Preregistration** lodged (OSF link / DOI) + amendment history.
- [ ] **Decisions register** — the numbered analytical decisions and who made them.
- [ ] **Pre-launch sign-off gates** — review before committing compute/API spend.
- [ ] **Adversarial / independent verification** — verifier passes, accuracy audits.
- [ ] **Author review** — what the author read, checked, and signed off.
- [ ] **What remained strictly under author control** — design, interpretation, claims.

*(Cross-reference the project's paper-writing brief / governance section so the
qualitative frame and this quantitative inventory are one disclosure, two halves.)*

## 2. Tools and models

| Field | Value |
|---|---|
| Tool | Claude Code (Anthropic agentic command-line interface) |
| Access method | `claude-code-cli` |
| Models used (exact IDs) | Opus 4.8 (`claude-opus-4-8`, 18 sessions), Opus 4.7 (`claude-opus-4-7`, 11 sessions), Fable 5 (`claude-fable-5`, 1 session) |
| Archived sessions | 30 |
| Period | 2026-04-22 – 2026-06-19 |

**Model progression.** 2026-04-22: Opus 4.7 (`claude-opus-4-7`) → 2026-05-29: Opus 4.8 (`claude-opus-4-8`) → 2026-06-11: Fable 5 (`claude-fable-5`) → 2026-06-14: Opus 4.8 (`claude-opus-4-8`).

## 3. Interaction summary (supporting texture — read the caveats)

| Field | Value |
|---|---|
| Sessions by type *(all auto-proposed — confirm before use)* | 21 analysis, 4 prereg-admin, 2 dissemination, 3 infra |
| Human turns (prompts) | 1,016 |
| Tool calls (code / file / search actions) | 6,097 |
| Delegated subagent runs | 263 |
| LLM output volume | ≈35.8 M tokens |

**Subagent runs by recorded type** (the metadata's `subagent_type`; `unspecified`
means the type was not captured, not that no role existed):

| Subagent type | Runs |
|---|---|
| general-purpose | 121 |
| unspecified | 49 |
| obs-writer | 33 |
| Explore | 25 |
| prior-art-scout | 13 |
| lit-scout | 9 |
| lit-scout-verifier | 7 |
| prior-art-scout-verifier | 4 |
| Plan | 2 |

**Caveats — read before quoting any figure.**

- *Session type* is auto-proposed by keyword heuristic (rows marked `*` in §4);
  **confirm or override** (`--types-map`) before relying on the split.
- *Output tokens* are generated output as recorded; **reasoning/"thinking"
  traces are tracked separately** (4,339 thinking blocks across the
  run, flagged research-only) and are **not** included in this figure.
- *Wall-clock duration* across the run is ≈1,283 hours, but this is
  elapsed open-to-close time **dominated by overnight/long-running agent windows
  — not human effort.** Actual human time lives in the personal time-log.
- *Cost* — the archive's notional list-price token cost is **not actual
  expenditure** (flat-rate subscription) and is omitted here by design.

## 4. Draft Methods paragraph (example — adapt to the venue's policy)

> Statistical analysis and analysis-code development for this study were carried
> out with the assistance of Claude Code (Anthropic), an agentic
> large-language-model coding environment, across 21 analysis sessions
> (plus 4 prereg-admin; 2 dissemination; 3 infra) between 2026-04-22 and
> 2026-06-19. The models used are listed in §2 by exact identifier. The
> analytical apparatus that governed this work — preregistration and amendments,
> a numbered decisions register, pre-launch sign-off gates, and independent
> verification (see §1) — kept design, analytical choices, and interpretation
> under author control; the model executed code, edited project files, and ran
> delegated sub-tasks under that governance (263 subagent runs;
> 6,097 tool invocations; ≈1,016 author prompts). Complete
> session transcripts are retained and available on request.

## 5. Per-session inventory (appendix)

Rows marked `*` in the *Type* column are auto-proposed and unconfirmed.

| # | Date | Session focus | Type | Model | Turns | Tool calls | Subagents |
|---|------|---------------|------|-------|-------|------------|-----------|
| 1 | 2026-04-22 | establish inscriptions spa pipeline | analysis* | Opus 4.7 | 60 | 185 | 14 |
| 2 | 2026-04-23 | establish research intent and osf | prereg-admin* | Opus 4.7 | 44 | 169 | 11 |
| 3 | 2026-04-24 | build forward fit cpl null models | analysis* | Opus 4.7 | 68 | 246 | 19 |
| 4 | 2026-05-14 | preregistration review and documentation | prereg-admin* | Opus 4.7 | 61 | 201 | 11 |
| 5 | 2026-05-16 | preregistration revision cycle with cross | prereg-admin* | Opus 4.7 | 23 | 182 | 4 |
| 6 | 2026-05-17 | incorporate stand in statistical review | analysis* | Opus 4.7 | 19 | 219 | 0 |
| 7 | 2026-05-17 | evaluate martin s hmm pivot and prepare | analysis* | Opus 4.7 | 16 | 27 | 2 |
| 8 | 2026-05-21 | complete rac trac 2026 conference talk slide | dissemination* | Opus 4.7 | 42 | 521 | 1 |
| 9 | 2026-05-22 | complete rac trac deck rewrite speaker | dissemination* | Opus 4.7 | 46 | 273 | 4 |
| 10 | 2026-05-23 | validate h2 1 deconvolution mixture model | analysis* | Opus 4.7 | 61 | 345 | 16 |
| 11 | 2026-05-25 | establish acts vs content two measure | analysis* | Opus 4.7 | 33 | 149 | 7 |
| 12 | 2026-05-29 | complete section 5 layer a city trajectory | analysis* | Opus 4.8 | 49 | 202 | 17 |
| 13 | 2026-06-02 | standardise dependency stack on pymc 6 | infra* | Opus 4.8 | 17 | 148 | 3 |
| 14 | 2026-06-02 | adjudicate grid a formulate corrected | analysis* | Opus 4.8 | 26 | 227 | 2 |
| 15 | 2026-06-03 | finalise two unit recovery adjudication | analysis* | Opus 4.8 | 21 | 264 | 2 |
| 16 | 2026-06-04 | finalise cross sectional track with h3c i | analysis* | Opus 4.8 | 36 | 245 | 5 |
| 17 | 2026-06-04 | finalise and lodge osf preregistration | prereg-admin* | Opus 4.8 | 11 | 63 | 0 |
| 18 | 2026-06-05 | establish empirical calendar slab basis | analysis* | Opus 4.8 | 34 | 110 | 15 |
| 19 | 2026-06-06 | build decision 38 empirical convention basis | analysis* | Opus 4.8 | 12 | 209 | 0 |
| 20 | 2026-06-07 | evaluate re validation grid finalize h2 1 | analysis* | Opus 4.8 | 32 | 213 | 6 |
| 21 | 2026-06-09 | design and build joint identifiability | analysis* | Opus 4.8 | 16 | 168 | 5 |
| 22 | 2026-06-09 | resolve sapphire resource exhaustions | infra* | Opus 4.8 | 27 | 206 | 1 |
| 23 | 2026-06-11 | adopt and validate cross classified temporal | analysis* | Fable 5 | 58 | 417 | 10 |
| 24 | 2026-06-14 | clean sapphire tempfiles and run draw wise | infra* | Opus 4.8 | 16 | 152 | 1 |
| 25 | 2026-06-15 | execute h3b flexible null robustness annex | analysis* | Opus 4.8 | 24 | 158 | 3 |
| 26 | 2026-06-15 | execute h3b flexible null robustness annex | analysis* | Opus 4.8 | 27 | 158 | 3 |
| 27 | 2026-06-16 | (untitled session — see transcript) | analysis* | Opus 4.8 | 22 | 177 | 4 |
| 28 | 2026-06-17 | clear residual layer b inversion and latin | analysis* | Opus 4.8 | 24 | 180 | 7 |
| 29 | 2026-06-18 | deconvolve temporal epigraphic patterns | analysis* | Opus 4.8 | 47 | 153 | 29 |
| 30 | 2026-06-19 | complete final preregistered analyses | analysis* | Opus 4.8 | 44 | 130 | 61 |

## 6. Provenance and regeneration

- **Source:** `~/cc-archives/inscriptions/<session>/session.meta.json`; full
  transcripts (`session.jsonl.gz`, SHA-256-hashed) + nested subagent transcripts
  are retained per session.
- **Regenerate:** `python ~/personal-assistant/scripts/llm-use-inventory.py
  --project inscriptions --out <repo>/reports/llm-use-inventory.md`
  (add `--types-map` once session types are confirmed). Re-run after any new
  session is archived (archives are written at session close).
