---
title: "H3a confirmatory launch spec — cross-sectional within-between NBR (+ H3c), run blind"
scope: "The cross-sectional track of Decision 35: bring the talk-prep H3a up to preregistered confirmatory standard, run by an agent blind to the preliminary exploration. Covers H3a (primary confirmatory result) + H3c (Hanson residual replication). Does NOT cover the H2.1 mixture (temporal track)."
status: "DRAFT for Shawn's sign-off. No fits run until approved. After sign-off: dispatch the blind run."
date: 2026-06-04
author: "Claude Code (analyst/RSE) on Shawn's brief"
sequencing: "Decision 35 + addendum (2026-06-04): cross-sectional track FIRST; mixture (H3b/§5) follows."
related:
  - planning/preregistration-draft.md (§3 H3a lines 212–269; H3c lines 269–280)
  - planning/decision-log.md (Decision 12 Mundlak; 22 date-window counts; 32 f_within weightings; 35 model+scope; 35 addendum)
  - planning/h3a-design-artefact-2026-06-04.md (the pinned PPC / prior-predictive thresholds — a prerequisite)
  - runs/2026-05-21-talk-prep/code/05-h3a-bayesian-mundlak.py (reference model code; clean of result values)
  - runs/2026-05-21-talk-prep/code/01-filter-and-prep.py (reference data prep; CITY_COUNT_NOTE)
  - scripts/h3a_brms_shadow.R (the cross-language shadow; audited 2026-04-25)
---

# H3a confirmatory launch spec (cross-sectional track)

## 1. Objective

Produce the paper's **primary confirmatory quantitative result** — the
within-province population-attributable variance fraction `f_within` and its
three-way verdict — to full preregistered standard, plus the **H3c** Hanson
residual replication. The talk-prep code already implements the model faithfully
(audit 2026-06-04); this spec adds the confirmatory scaffolding the talk omitted
and runs the whole thing **blind to the preliminary exploration** to neutralise
anchoring.

## 2. What already exists vs what this spec adds

**Exists (faithful to prereg, reused as the reference implementation):** the
within-between NBR model + all six priors; the `f_within` estimand (unweighted,
per-draw); the three-way verdict at 0.10; the probability ladder; convergence
gating; date-window-filtered Rome-excluded sample; the brms shadow script.

**This spec adds:** canonical data artefact; prior-predictive checks + committed
thresholds (design artefact); the full PPC suite + two-tier severity; Bayesian R²;
the OLS log-log comparator (SR1 / Hanson); the two weighted `f_within` variants
(Decision 32); the standardisation sensitivity; H3c (residuals + Moran's I); and
the brms-shadow execution + cross-language agreement check.

## 3. Sample and scope (decided)

- **Unit:** inscription-mass only (letter-mass FAILed recovery, Obs 72; the
  cross-sectional letter-mass H3a is a *separate* co-registered confirmatory under
  the two-measure framework and is **out of scope here** — this spec is the
  inscription-mass primary).
- **Sample (Decision 35A):** **1,044 Hanson-matched cities, Rome-excluded** — the
  prereg-text-faithful "all cities with Hanson population estimates, Rome excluded".
  The prereg's parenthetical "~815" was a stale 2024-notebook Latin-province filter
  (a hand-curated province→language dict, not a data column;
  `01-filter-and-prep.py` CITY_COUNT_NOTE). **Document the discrepancy** in the
  REPORT; the ~815 Latin-only sample is an **optional sensitivity** (report if
  cheap; not the primary).
- **Counts:** per-city date-window-filtered (50 BC – AD 350) inscription counts. The
  mixture is NOT applied (Decision 22 / 35 addendum).

### 3a. OPEN SUB-QUESTION for Shawn (must resolve before data prep is finalised)

**Zero-inscription Hanson cities.** The talk frame is built by grouping LIRE rows,
so it contains only Hanson cities with **≥ 1** inscription (→ 1,044). The prereg
text "all cities with Hanson population estimates" *could* additionally intend
Hanson cities with **zero** LIRE inscriptions as structural zeros (an NBR handles
zeros; Carleton et al. 2025 explicitly report an "epigraphy-no-zeros variant",
prereg SR1 line 49, so zeros are a known axis). Options:

- **(i)** Primary = LIRE-present cities only (1,044), as the talk did; report the
  count of zero-inscription Hanson cities and a with-zeros sensitivity. *(My lean —
  matches the talk and the realised 1,044; keeps the primary on observed cities.)*
- **(ii)** Primary = all Hanson cities incl. zeros; no-zeros as the sensitivity
  (closer to a strict reading of "all cities with Hanson estimates").

I recommend **(i)** but flag it because it changes the sample definition and should
be a conscious, documented choice (and possibly a one-line amendment note since the
prereg text is ambiguous). *Please confirm (i) or (ii).*

## 4. Pipeline (blind run)

All steps run on **sapphire** unless trivial. New run dir:
`runs/2026-06-04-h3a-confirmatory/`.

0. **Prior-predictive + threshold commit** (`prior-predictive.py`). Draw 1,000
   parameter sets from the priors; simulate per-city counts from the predictor
   matrix only (no observed `y`); compute and **commit** the data-shaped thresholds
   (`count_cap_p99`, `tail_count_bound`) into the design artefact (or a committed
   sidecar `prior-predictive-thresholds.json`) **before the confirmatory fit**.
   Run the prior-sanity gate (design artefact §2).
1. **Data prep** (`01-data-prep.py`) → **`data/processed/city_level_for_h3a.parquet`**
   (canonical path). One row per city; columns:
   `city, province, urban_context_pop_est, log_pop, log_pop_prov_mean,
   log_pop_within, province_idx, inscription_count` (+ provenance: filter window,
   LIRE version, Rome-exclusion flag, sample = 1,044). This *productionises* the
   talk's inline `build_city_frame`.
2. **Confirmatory H3a fit** (`02-h3a-fit.py`, pymc): the model as built (non-centred
   `α_prov`; `tune ≥ 3,000` — the talk hit R̂ = 1.0100 at tune = 1,000, so tune is
   raised to clear the < 1.01 gate unambiguously; 4 chains; `target_accept = 0.95`).
   Outputs the posterior + `f_within` (unweighted **primary**) + the two **weighted
   variants** (population-weighted, inscription-weighted; Decision 32) + the
   three-way verdict + probability ladder + **Bayesian R²** (Gelman et al. 2019) +
   the **OLS log-log coefficient** (Hanson/SR1 comparator) + the **standardisation
   sensitivity** (re-fit with standardised predictors; report β stability).
3. **PPC suite** (`03-ppc.py`) — all ten checks in the design artefact (prior- and
   posterior-predictive), with the two-tier severity adjudication. A **critical**
   trigger halts and reports (model revision + amendment before final results); a
   **minor** trigger is a logged caveat.
4. **brms shadow** (`scripts/h3a_brms_shadow.R`) — run against the canonical parquet;
   check pymc vs brms posteriors agree within Monte-Carlo noise on `β_within`,
   `β_between`, `f_within`. Disagreement beyond MC noise → investigate; if it
   materially affects the verdict → amendment before final. (brms needs the R/Stan
   env; confirm availability on sapphire, else run on a host that has it.)
5. **H3c** (`04-h3c.py`) — Pearson residuals from the H3a posterior; Moran's I with
   k-NN weights at **k = 8 primary, k = 5 / 10 sensitivity**; conditional permutation
   inference (999 perms) on the **posterior-mean residual vector** per k; plus the
   **posterior distribution of Moran's I** across draws (2.5/50/97.5 pct per k).
   Confirmatory rule: Moran's I > 0 at p < 0.05 in ≥ 2 of {5, 8, 10}.
6. **REPORT** (`outputs/REPORT.md`) — headline `f_within` verdict + ladder; weighted
   variants; R²; OLS comparator vs Hanson 2021 β = 0.672 / Carleton 2025; PPC table
   with severities; H3c verdict; the 1,044-vs-815 note; the zero-cities decision;
   convergence diagnostics; and the contamination/blind-run disclosure.

## 5. Blind-run protocol (per Shawn's 2026-06-04 instruction)

The confirmatory pipeline is executed by a **fresh agent blind to the preliminary
exploration**, so that no preliminary `f_within` value anchors the confirmatory
numbers.

- **May read:** the prereg (`preregistration-draft.md`); this spec; the design
  artefact; the *model code* `runs/2026-05-21-talk-prep/code/05-h3a-bayesian-mundlak.py`
  and `01-filter-and-prep.py` **as implementation references** (these contain no
  result values — verified: `f_within` is computed, not hard-coded); the data
  (LIRE filtered parquet; Hanson population fields).
- **Must NOT read:** any talk-prep **output** (`runs/2026-05-21-talk-prep/outputs/`
  tables/figures, the talk REPORT, the deck, `qa-report-*`), the letter-probe H3a
  outputs, or any continuity/working-notes passage quoting a preliminary `f_within`.
  It must not be told the preliminary value.
- **Self-check:** the agent states, in its REPORT, that it derived every reported
  number from the prereg + data + design artefact and read no preliminary result.
- **Honesty floor:** because *this* (non-blind) thread has seen the preliminary
  estimand, the REPORT discloses that the estimand was previously seen at
  exploratory talk-prep (design artefact §0); the blind run is a mitigation, not a
  claim of zero prior exposure.

## 6. Compute, convergence, reproducibility

- Sapphire; tracked launch wrapper; `TMPDIR` redirect to disk-backed scratch
  (2026-05-23 lesson).
- Convergence gates (prereg §4): R̂ < 1.01 all params; ESS-bulk ≥ 400; 0
  divergences. If R̂ marginal at tune = 3,000, raise tune / investigate before
  accepting (do not relax the gate).
- Commit before each step (research-record preservation). All outputs under the new
  run dir; the canonical parquet under `data/processed/`.

## 7. Open items to confirm at sign-off

1. **Zero-inscription Hanson cities** — §3a, options (i)/(ii). *(My lean: (i).)*
2. **~815 Latin-only sensitivity** — report it, or omit? *(My lean: report if cheap.)*
3. **brms env on sapphire** — confirm R/Stan present, or nominate a host.
4. **Standardisation sensitivity** — confirmatory-adjacent exploratory; keep in
   scope here (cheap) or defer? *(My lean: keep.)*

## 8. Sign-off gate

Shawn approves this spec (and the four open items) → the design artefact + this spec
are committed → the **blind agent** runs the pipeline → REPORT returned → **Shawn
signs off before any result is labelled "final"** (and before any confirmatory claim
leaves the repo). No fits run before approval.
