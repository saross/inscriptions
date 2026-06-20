---
title: "Documentation-accuracy certificate — pre-write-up audit"
date: 2026-06-20
provenance: "Workflow doc-accuracy-audit run wf_9892f1e4-9ac (26 agents, 7 clusters; adversarial verify -> independent re-verify -> synthesis with cross-document consistency). Read-only audit; corrections applied separately after review."
confirmed_corrections: 17
---

# Documentation-Accuracy Certificate — Inscriptions / LIRE SPA Paper

Generated 2026-06-19. Scope: seven verifier clusters covering working-notes Obs 46–111, all run-directory REPORT/VERDICT/MEMO/SPEC files, the continuity beacon, decision-log, planning audits, and the paper-facing descriptive/changelog docs.

## 1. Headline verdict

**The documentation is substantially write-up-ready, but a short, well-bounded list of corrections must be applied first — and exactly one of them is high severity.** Across 677 checkable specifics, 660 matched their primary artefacts to stated precision (97.5%), and the two most important clusters for the paper's load-bearing claims — H3a/H3c confirmatory (`runs/2026-06-04-h3a-confirmatory`) and the D13/A01 recent work — are clean or near-clean, with every headline point estimate, CI, count, and verdict reproducing from source. The 17 confirmed errors are dominated by low-severity provenance/labelling slips and post-audit staleness (Obs counts, run-dir counts, seed labels) that do not touch any verdict. The one item that genuinely must be fixed before the Data/Methods section is written is the **65-vs-63 corpus column count still live in `profile-dataset.md`** (high severity, because it is the dataset-shape figure the paper will cite). Two medium-severity issues — the H3b identifiability-criterion bookkeeping (swing-vs-gap conflation, off-by-one counts) and the mislabelled lead α>0 coverage comparator in Obs 89 — are not paper-fatal (H3b is exploratory and flagged OQ-2) but should be corrected so stale criterion attributions do not migrate into the write-up. No headline confirmatory or inferential result is wrong.

## 2. Totals across clusters

| Metric | Count |
|---|---|
| Claims checked | 677 |
| Matches (first-pass) | 660 |
| Mismatches flagged by first verifier | 18 |
| **CONFIRMED mismatches** (re-verify `is_real_mismatch=true`) | **17** |
| **False alarms** (re-verify overturned) | **1** |
| Unresolved (no locatable primary) | 7 |

Per-cluster: h2.1-recovery-cc-theta 118/117/1·0; h3a-h3b-h3c 86/78/5·1 (+3 unresolved); s5-suite 168/163/2·0 (+2 unresolved); sensitivities-suppwave-c10-h9 118/115/3·0; d13-a01-recent 71/71/0·0; research-record 58/57/1·0; paper-facing-and-data 58/44/5·0 (+2 unresolved). (format: checked/matches/confirmed·falsealarm)

## 3. Confirmed corrections (edits the main thread must apply)

Ordered high → low severity.

| # | Doc location | Documented | Correct value | Primary source | Sev |
|---|---|---|---|---|---|
| 1 | `runs/2026-04-23-descriptive-stats/outputs/profile-dataset.md:1` (line 3) | Columns: 65 | **63** (pandas shape (182853, 63); 64th pyarrow field is `__index_level_0__`) | `archive/data-2026-04-22/LIRE_v3-0.parquet`; run.log:2,4; decisions.md:35,41-45 | **high** |
| 2 | `runs/2026-06-09-h3b/REPORT.md:67` | 9 units identifiable under swing rule | **10** identifiable (swing ≤ 0.20); 19 under-identified (the "9" is the SUMMARY-FINAL gap>0.25 count) | `runs/2026-06-07-h2.1-launch-prep/outputs/production/identifiability-table.json` | medium |
| 3 | Obs 80 (`working-notes.md:2266`; table at :2252) | swing > 0.20 → 9 under-identified | swing > 0.20 → **19**; the **9** is gap>0.25 (different criterion) | `…/production/SUMMARY-FINAL.md:14,17` + `identifiability-table.json` | medium |
| 4 | Obs 80 (`working-notes.md:2266`); `runs/2026-06-09-h3b/REPORT.md:69-70`; `h3b-spec.md:419` | 8 units disagree (incl. Hispania citerior) | **7** units disagree; Hispania citerior identifiable under BOTH (gap 0.057, swing 0.156) | `runs/2026-06-09-h3b/outputs/identifiability-split.json` + `identifiability-table.json` | medium |
| 5 | Obs 89 (`working-notes.md:2735`); upstream `cross-classified-signoff.md:270` | lead α>0 coverage (n=168) = 0.456 | **0.467** (full lead grid, n=168); 0.456 is the PILOT n=14 value | `runs/2026-06-09-joint-identifiability/outputs/grid-summary.json`; `cc-PILOT-REPORT.md:22` | medium→low |
| 6 | Obs 75 (`working-notes.md:2089`) | "just 1 of the top-20 N≥2000 provinces is non-Latin" | **0** genuinely non-Latin; the "1" is Roma (Latin, Rome-excluded/unmapped) | `runs/2026-05-21-talk-prep/data/lire-filtered.parquet`; `…/province-language-map.csv` | low |
| 7 | Obs 92 (`working-notes.md:3213`) | CPL-3 null marginal-p ≤ 0.04 for all 29 | max = **0.0405** (Noricum); bound is ≤ 0.0405 / < 0.05 | `runs/2026-06-09-h3b/outputs/drawwise/deviations-table.csv` | low |
| 8 | `runs/2026-06-17-s5-h7-perperiod-h3c/REPORT.md:18` | AD 150-200 Moran's I (k=8) = -0.004 | **-0.005** (-0.004550, rounds to -0.005; Obs 99 has it right) | `…/outputs/h7-summary.json` per_period['150..200'].moran.per_k['8'] | low |
| 9 | `runs/2026-06-17-s5-h7-perperiod-h3c/REPORT.md:17` + Obs 99 (`working-notes.md:4392`) | AD 100-150 Moran's I (k=8) = -0.014 | **-0.013** (-0.013478) | `…/outputs/h7-summary.json` per_period['100..150'] | low |
| 10 | Obs 110 (`working-notes.md:5897,5958`; Findable-later tag :5972) | base_seed 20260618 (both waves) | wave 2 base_seed = **20260619** (wave 1 = 20260618 is correct) | `runs/2026-06-18-c10-validity-test/outputs/{results.json,followup-ii-results.json}` config.base_seed | low |
| 11 | Obs 93 (`working-notes.md:3429-3431`) | "Only 2/29 … de-saturate under either statistic or GP edf20" | two **separate** per-fit 2/29 counts; union = **3** {Pannonia inferior, Noricum, Ostia}; n_eff bound understates Pann. inf. (2812) | `runs/2026-06-09-h3b/outputs/flexnull/flexnull-sweep.json`; ANNEX-REPORT.md:116-119 | low |
| 12 | Obs 110 (`working-notes.md:5896-5897`) | C10 follow-up (ii) ran 2026-06-19 | run/results = **2026-06-18 22:55:39**; only report stamp crosses to 2026-06-19 00:01 | `…/c10-validity-test/outputs/{followup-ii-results.json,followup-ii-report.md}` | low |
| 13 | `planning/prereg-obligations-coverage-sweep-2026-06-20.md:207,241-243` | AM01-d not-covered; covered 54/63 | AM01-d **IS covered** (Obs 108); effective 55/63, not-covered 0 (sweep predates A01 run; continuity inventory already correct) | `runs/2026-06-20-a01-content-residual/outputs/content-residual-results.json`; working-notes.md:5672 | low |
| 14 | `planning/preregistration-changelog.md` (~L485, ~L570) | "[1, 100] is 26% of the corpus" | width-100 *class* = **26.29%** (47,487 rows); exact [1,100] template = **~6.0%** (10,807) | `runs/2026-05-17-interval-width-diagnostic/outputs/REPORT.md:41` + parquet | low |
| 15 | `planning/prereg-obligations-coverage-sweep-2026-06-20.md:234-237` | Total obligations = 63 rows | component groups sum to **76**; row count = 76; by-status tally = 62 — "63" matches none | self-consistency of the doc's own §SUMMARY + table rows | low |
| 16 | `planning/results-documentation-uplift-2026-06-20.md:47-48,300` | 107 numbered observations | **111** (max Obs in working-notes.md) | `docs/notes/working-notes.md` (grep `^## Obs`) | low |
| 17 | `planning/results-documentation-uplift-2026-06-20.md:5` | 58 run directories | **60** | `ls -d runs/*/ \| wc -l` = 60 | low |

**Severity rollup:** 1 high (#1), 3 medium (#2-4), 1 medium-to-low (#5), 12 low. Items #2-4 are the same H3b identifiability-bookkeeping defect repeated across `REPORT.md`, `h3b-spec.md`, and Obs 80 — fix as one coordinated edit. Items #13, #16, #17 are post-audit staleness in 2026-06-20 planning docs; the live continuity inventory already supersedes them, so the safest action is to not cite those audit snapshots as current rather than to re-edit them.

## 4. Cross-document consistency

Scanning `key_quantities` and mismatches across all seven clusters for the same quantity quoted with different values:

| Quantity | Doc A value (location) | Doc B value (location) | Which is correct |
|---|---|---|---|
| H7 AD 150-200 Moran's I (k=8) | -0.004 (`s5-h7…/REPORT.md:18`) | -0.005 (Obs 99 `working-notes.md:4393`) | **Obs 99 (-0.005)**; REPORT is the error (correction #8) |
| H7 AD 100-150 Moran's I (k=8) | -0.014 (`s5-h7…/REPORT.md:17`) | -0.014 (Obs 99 `working-notes.md:4392`) | **Neither**; both wrong, primary = -0.013 (correction #9) — agree with each other but disagree with data |
| H3b under-identified count "9" | swing>0.20 → 9 (Obs 80 :2252,:2266; REPORT:67) | gap>0.25 → 9 (SUMMARY-FINAL.md:14) | **SUMMARY-FINAL (gap-based)**; Obs 80/REPORT mislabel the criterion (corrections #2,#3) |
| lead α>0 coverage, n=168 | 0.456 (Obs 89 :2735; signoff §6c:270) | (cc-VERDICT-library.md correctly omits a lead α>0 figure) | **0.467** (grid-summary.json); 0.456 is the pilot n=14 (correction #5) |
| Empire H3a β_within | 0.587 [0.519,0.657] (h3a REPORT, decision-log:3440, peak-scaling) | 0.5869→0.587 (layerb beta-inversion) / 0.5876→0.588 (layerb residual, re-resampled) | **All consistent**; the 0.5876 differs by documented re-resampling, rounds to 0.588 in its own report — not a contradiction |
| Empire descriptive α (supp-wave) | 0.680 (coverage-sweep C16) | 0.6798 (Obs 111 / supp-wave REPORT) | **Consistent** (0.6798 → 0.680) |
| Decision-38 multi-century share | ~31% (lodged amendment / OSF Amdt 03) | 24.96% full pool / 35.93% F1+F3 (decision-log:3618-3624; Obs 76) | **24.96%/35.93% reproduce**; ~31% genuinely does not — flagged, directive is cite ~36%/24.96% + footnote, leave lodged text unedited (consistent across Decision 38 & Obs 76) |
| C5/C6 max raw \|Δα\| | 0.0156 (continuity inventory:88; Obs 111; model-comparison.md:44) | "0.016" (continuity beacon:8) | **Consistent** (0.0156 → 0.016 rounded) |
| "65 columns" corpus shape | 65 (`profile-dataset.md:1`) | 63 (`summary.md:5`, corrected 2026-06-20) | **63**; profile-dataset.md still wrong (correction #1) — internal contradiction between the two descriptive docs |
| Obs-register size | 107 (uplift audit:47-48,300) | 111 (working-notes.md max Obs) | **111** (correction #16) |
| Run-directory count | 58 (uplift audit:5) | 60 (filesystem) | **60** (correction #17) |
| AM01-d coverage status | not-covered (coverage-sweep:207) | DISCHARGED/covered (continuity.md:71-77; Obs 108) | **covered** (correction #13) — the two planning docs disagree; continuity is current |

The genuinely actionable internal contradictions are: **profile-dataset.md vs summary.md on column count** (#1, the one that matters), **REPORT vs Obs 99 on the AD150-200 Moran's I** (#8, the REPORT cell drifts), and the **H3b "9" criterion** quoted three ways (#2-3). The β_within, α, Decision-38, and |Δα| apparent "two values" are all reconcilable rounding or documented re-resampling, not errors.

## 5. False alarms

One first-verifier flag was overturned on re-check:

| Claim | Doc | Why overturned |
|---|---|---|
| Antonine deficit "centred at AD ~168" | Obs 82 (`working-notes.md:2329`) | Primary `runs/2026-06-09-h3b/outputs/replication-antonine.json` gives peak_year **167.5** (5-year bin centre). The prose uses an explicit "~" approximation marker; 167.5 → ~168 is a faithful rounding, and the exact 167.5 is carried verbatim in the table directly below (lines 2333-2334) and in the tags. `is_real_mismatch=false` — no accuracy discrepancy. |

## 6. Unresolved (need a human / primary look)

Seven claims could not be tied to an in-scope primary artefact and were left unverified rather than guessed:

1. **Obs 46 talk-prep f_within** (unweighted 0.300 / pop-wt 0.496 / insc-wt 0.421), `working-notes.md:1203` — primary is `runs/2026-05-21-talk-prep/outputs/tables/h3a-summary.csv` (different seed 20260521); belongs to the talk-prep cluster verifier. Confirmatory analogues (0.299/0.494/0.419) are close but not the same numbers.
2. **Obs 59 letter-mass f_within shift** +9.89pp (29.94%→39.83%), `working-notes.md:1488-1507` — primary `runs/2026-05-26-letter-count-probe/outputs/tables/h3a-mundlak-three-variants-summary.csv`, out of scope; letter-count-probe verifier owns it.
3. **H3a α_0 R-hat = 1.0100 at superseded starting config**, `runs/2026-06-04-h3a-confirmatory/outputs/REPORT.md:285-292` — a process/history claim about a config that was re-tuned; the 1.0100 value is not persisted (final run records converged 6000/3000/0.97, max_rhat 1.0). Not re-verifiable without re-running the original config.
4. **"34 reliable cities span 19 provinces"**, `runs/2026-06-18-s5-size-vs-dynamics/REPORT.md:35` + Obs 104:5070 — province count not persisted in the summary JSON; needs reconstruction from the InferenceData `.nc` + city-index parquet. Descriptive, non-load-bearing.
5. **q_uv = q_u·q_v nested-identity guard "max abs deviation 1.3×10⁻⁸"**, `runs/2026-06-17-s5-layer-b-residual/REPORT.md:114` + Obs 103 — runtime-guard value asserted only in prose; not persisted (the companion Cirta wiring-guard 5.55×10⁻¹⁶ IS persisted and verified).
6. **Collaborator's "~2,000 mother-daughter inscriptions"**, `paper-significance-and-applications-2026-06-03.md §1` — `data/women.csv` is gzip/binary-encoded, a collaborator's external corpus, not a project primary. Approximate motivating figure only.
7. **Doc-uplift stale-banner claims** (h9 "NOT RUN", h2.1-supp "DRAFT", h3a "PRELIMINARY", recovery-grid supersede banner, summary.md "65 cols"), `results-documentation-uplift-2026-06-20.md` Tier-1/2/3 — these were TRUE at audit time but the recommended fixes have since been applied; the audit's own "is stale/missing" assertions are now outdated. Action: do not re-action already-done items. (Note: the audit pins "65 cols" on summary.md, but the live 65 actually persists in profile-dataset.md — see correction #1.)

## 7. Coverage gaps

What verifiers could not access, per the `coverage_notes`:

- **NetCDF / arviz InferenceData (`.nc`) files are gitignored / on sapphire** (regenerable). Posterior summaries across H3a/H3b/s5 were verified against committed JSON/CSV summaries rather than re-sampled from idata. Per-period NBR betas and Moran permutations were trusted as persisted JSON outputs of converged fits, not recomputed from raw idata.
- **Out-of-scope run dirs not re-read by the assigned clusters:** talk-prep (`runs/2026-05-21-talk-prep/outputs/tables/h3a-summary.csv`, seed 20260521) and letter-count-probe (`runs/2026-05-26-letter-count-probe/…`) — these own Obs 46 and Obs 59 respectively (see Unresolved 1-2).
- **`data/women.csv`** — binary/gzip-encoded collaborator corpus, not readable as a project primary (Unresolved 6).
- **`size-vs-dynamics` `.nc`** would not open with plain `xr.open_dataset` (arviz group file); the "19 provinces" count needs the city-index parquet whose stored provenance path was absolute and absent at the relative location tried (Unresolved 4).
- **Lodged preregistration and amendments** were treated as authoritative per instructions and NOT re-verified in any cluster — including the lodged Decision-38 "~31%" (which is independently known not to reproduce from either CSV and is handled by an explicit write-up directive, not a correction).
- **Figure captions:** confirmed low-risk across all clusters — caption numbers are f-string-computed from data variables (not hand-edited), so no caption-vs-data drift was found; the only literal caption numbers are conceptual axis annotations (AD 79, AD 250, the 0.95 sampler threshold).

---

**Bottom line for the write-up:** apply correction #1 (high) before drafting Data/Methods; apply #2-5 (the H3b identifiability bookkeeping and the Obs 89 lead comparator) before any text touching identifiability or do-no-harm coverage; treat #6-12 and #14 as clean-up edits to working-notes/reports; and for #13/#15/#16/#17, prefer the live continuity inventory over the 2026-06-20 audit snapshots rather than re-editing the snapshots. No confirmatory or inferential headline result requires revision.