---
title: "LLM-Use Inventory — Inscriptions"
purpose: "Supporting record for the JAMT Methods disclosure of LLM use"
generated: 2026-06-20
source: "~/cc-archives/inscriptions/ (session.meta.json across 30 archived sessions)"
status: draft
---

# LLM-Use Inventory — Inscriptions

**Generated 2026-06-20** from the local Claude Code session archive
(`~/cc-archives/inscriptions/`). This document supports the **Methods**
disclosure of large-language-model (LLM) use for the *Journal of Archaeological
Method and Theory* (JAMT) submission. It is a **draft working record** — verify
and adapt the wording before submission.

## Provenance

- **Source:** `~/cc-archives/inscriptions/<session>/session.meta.json` — the
  enriched metadata sidecar written for each archived Claude Code session. All
  figures below are extracted programmatically from that metadata, not
  hand-transcribed.
- **Full transcripts retained:** each session directory also holds the complete
  raw transcript (`session.jsonl.gz`) plus nested subagent transcripts
  (`subagents/agent-*.jsonl.gz`), available if reviewers request the record.
- **Coverage:** 30 sessions, 2026-04-22 – 2026-06-19. **The final session (2026-06-20 — analysis
  completion and co-author handover) is not yet archived** (archives are written
  at session close); add it once captured.

## Summary

| Field | Value |
|---|---|
| Tool | Claude Code (Anthropic agentic command-line interface) |
| Access method | `claude-code-cli` |
| Models used | Claude Opus 4.8 (18 sessions), Claude Opus 4.7 (11 sessions), Claude Fable 5 (1 session) |
| Archived sessions | 30 |
| Period | 2026-04-22 – 2026-06-19 |
| Human turns (prompts) | 1,016 |
| Tool calls (code / file / search actions) | 6,097 |
| Delegated subagent runs | 263 |
| LLM output volume | ≈35.8 M tokens |

**Model progression.** 2026-04-22: Opus 4.7 → 2026-05-29: Opus 4.8 → 2026-06-11: Fable 5 → 2026-06-14: Opus 4.8. All access
was through the Claude Code CLI under a Claude Code Max subscription.

**On effort and cost — read before quoting any duration or dollar figure.**
Cumulative session wall-clock is ≈1,283 hours, but this measures
elapsed time between session open and close and is **dominated by long-running
and overnight agent windows — it is not a measure of human effort.** Actual
human time is recorded separately in the personal time-log. The archive also
reports a notional list-price token cost; this is **not actual expenditure**
(the work ran under a flat-rate Claude Code Max subscription) and is
deliberately omitted here to avoid a misleading figure.

## Draft Methods paragraph (example — adapt for JAMT's policy)

> Statistical analysis, analysis-code development, and parts of the literature
> review for this study were carried out with the assistance of Claude Code
> (Anthropic), an agentic large-language-model coding environment, across 30
> recorded working sessions between 2026-04-22 and 2026-06-19.
> The models used were Claude Opus 4.7 and Claude Opus 4.8, with one session
> using Claude Fable 5, all accessed via the Claude Code command-line interface.
> The first author directed and reviewed all work, issuing approximately
> 1,016 prompts across the sessions; the model executed analysis
> code, edited project files, and ran delegated sub-tasks (263
> subagent runs; 6,097 tool invocations in total). Preregistration, all
> analytical decisions, and the interpretation of results remained under author
> control. Complete session transcripts are retained and available on request.

*(Tailor the claims to JAMT's specific disclosure requirements and to exactly
what you wish to assert about author control and reproducibility.)*

## Per-session inventory

| # | Date | Session focus | Model | Turns | Tool calls | Subagents |
|---|------|---------------|-------|-------|------------|-----------|
| 1 | 2026-04-22 | establish inscriptions spa pipeline | Opus 4.7 | 60 | 185 | 14 |
| 2 | 2026-04-23 | establish research intent and osf | Opus 4.7 | 44 | 169 | 11 |
| 3 | 2026-04-24 | build forward fit cpl null models | Opus 4.7 | 68 | 246 | 19 |
| 4 | 2026-05-14 | preregistration review and documentation | Opus 4.7 | 61 | 201 | 11 |
| 5 | 2026-05-16 | preregistration revision cycle with cross | Opus 4.7 | 23 | 182 | 4 |
| 6 | 2026-05-17 | incorporate stand in statistical review | Opus 4.7 | 19 | 219 | 0 |
| 7 | 2026-05-17 | evaluate martin s hmm pivot and prepare | Opus 4.7 | 16 | 27 | 2 |
| 8 | 2026-05-21 | complete rac trac 2026 conference talk slide | Opus 4.7 | 42 | 521 | 1 |
| 9 | 2026-05-22 | complete rac trac deck rewrite speaker | Opus 4.7 | 46 | 273 | 4 |
| 10 | 2026-05-23 | validate h2 1 deconvolution mixture model | Opus 4.7 | 61 | 345 | 16 |
| 11 | 2026-05-25 | establish acts vs content two measure | Opus 4.7 | 33 | 149 | 7 |
| 12 | 2026-05-29 | complete section 5 layer a city trajectory | Opus 4.8 | 49 | 202 | 17 |
| 13 | 2026-06-02 | standardise dependency stack on pymc 6 | Opus 4.8 | 17 | 148 | 3 |
| 14 | 2026-06-02 | adjudicate grid a formulate corrected | Opus 4.8 | 26 | 227 | 2 |
| 15 | 2026-06-03 | finalise two unit recovery adjudication | Opus 4.8 | 21 | 264 | 2 |
| 16 | 2026-06-04 | finalise cross sectional track with h3c i | Opus 4.8 | 36 | 245 | 5 |
| 17 | 2026-06-04 | finalise and lodge osf preregistration | Opus 4.8 | 11 | 63 | 0 |
| 18 | 2026-06-05 | establish empirical calendar slab basis | Opus 4.8 | 34 | 110 | 15 |
| 19 | 2026-06-06 | build decision 38 empirical convention basis | Opus 4.8 | 12 | 209 | 0 |
| 20 | 2026-06-07 | evaluate re validation grid finalize h2 1 | Opus 4.8 | 32 | 213 | 6 |
| 21 | 2026-06-09 | design and build joint identifiability | Opus 4.8 | 16 | 168 | 5 |
| 22 | 2026-06-09 | resolve sapphire resource exhaustions | Opus 4.8 | 27 | 206 | 1 |
| 23 | 2026-06-11 | adopt and validate cross classified temporal | Fable 5 | 58 | 417 | 10 |
| 24 | 2026-06-14 | clean sapphire tempfiles and run draw wise | Opus 4.8 | 16 | 152 | 1 |
| 25 | 2026-06-15 | execute h3b flexible null robustness annex | Opus 4.8 | 24 | 158 | 3 |
| 26 | 2026-06-15 | execute h3b flexible null robustness annex_2dc7fc5b | Opus 4.8 | 27 | 158 | 3 |
| 27 | 2026-06-16 | c0b6bf25 | Opus 4.8 | 22 | 177 | 4 |
| 28 | 2026-06-17 | clear residual layer b inversion and latin | Opus 4.8 | 24 | 180 | 7 |
| 29 | 2026-06-18 | deconvolve temporal epigraphic patterns | Opus 4.8 | 47 | 153 | 29 |
| 30 | 2026-06-19 | complete final preregistered analyses | Opus 4.8 | 44 | 130 | 61 |

## Caveats and regeneration

- "Session focus" is the auto-generated session label — consult the transcript
  for detail.
- "Turns" = human prompts; "Tool calls" = analysis / file / search actions the
  model took; "Subagents" = delegated sub-tasks spawned within the session.
- Per-session wall-clock duration is omitted from the table for the reason given
  under *On effort and cost*.
- **Regenerate** after the final 2026-06-20 session is archived: re-run the
  extraction over `~/cc-archives/inscriptions/*/session.meta.json`.
