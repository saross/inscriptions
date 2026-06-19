# Recovery-grid design artefact (H2.1) — narrative spec

> **➡ FORWARD OUTCOME (what happened after this design pin).** This design bound
> the first recovery validation (`runs/2026-05-22-recovery-grid-validation/`),
> which initially **FAILed** under the lodged zero-tolerance criterion — but that
> FAIL was a metric/gate artefact and was **overturned to PASS** under the
> corrected, field-standard criterion (Obs 67/70; Decision 33 / OSF Amendment 01
> §A5.5.1; the validation REPORT now carries a SUPERSEDE banner). The grid was
> then rebuilt as the **two-unit, empirical-Bayes** grid
> (`runs/2026-05-26-recovery-grid-two-unit/`), the **canonical** recovery result
> (Grid A inscription-mass PASS 98.6 %; Grid B letter-mass FAIL on R̂/ESS). This
> design artefact is the historical pin; the canonical recovery outcome lives in
> those two later dirs.

**Run directory:** `runs/2026-05-22-recovery-grid-design/`
**Status:** pre-Phase-2 design pin; committed before any recovery-simulation
production run.
**Authority:** binds the H2.1 recovery simulation per
`planning/preregistration-draft.md` §4 (Phase 2 — Bayesian mixture validation,
lines 323-338) and `planning/decision-log.md` Decisions 19, 20, and 21.

## 1. Scope and what this artefact pins

The preregistration commits the H2.1 recovery simulation procedurally —
axes are named, minimum cardinalities are stated, and the coverage rule is
binding (≥ 90 % of cells pass; cell passes if ≥ 90 % of replicates produce a
posterior 95 % CI on α that contains the true α; AND posterior-median
Pearson r ≥ 0.95 in ≥ 90 % of cells; prereg §4 lines 325-334). The specific
values along each axis are deferred to this artefact (Decision 21, §4 line
325, §3 line 151). This document is the artefact.

What this pins (Decision 21 axes; all five are prereg-binding minimum
cardinalities):

1. The five-value α grid (with corner cases near 0 and near 1).
2. The six-shape `p_gen` library, each shape specified as an 80-bin
   probability vector with pinned parameters.
3. The five tier-weight vectors over the three template tiers from
   Decision 20.
4. The N grid (three sample sizes drawn from the Phase 1 reachability map).
5. The replicates-per-cell count and the seed policy.

What this artefact does **not** pin: numerical PPC thresholds for H3a
(§3 lines 251-258) and the Wasserstein-1 flagging threshold (§4 line 334)
are scoped to the same `runs/2026-05-XX-recovery-grid-design/` directory in
the prereg but defer to a follow-up pin once the smoke test has produced an
empirical posterior to anchor the threshold. Both are flagged in the
"deferred from this artefact" subsection at the end.

## 2. Grid axes

### 2.1 α grid

**Pinned values:** `α ∈ {0.05, 0.30, 0.50, 0.70, 0.95}` (5 values).

**Justification.** The prereg requires "at least 5 values spanning the
empirical pilot range, with corner cases (α near 0, α near 1) included"
(§4 line 327; Decision 21). The 0.05 / 0.95 endpoints satisfy the
corner-case requirement without forcing the multinomial into a degenerate
α = 0 or α = 1 boundary (where the mixture collapses to a non-mixture
model). The interior values 0.30 / 0.50 / 0.70 span the plausibly-relevant
range. The empirical pilot α posterior on filtered LIRE has not yet been
characterised under the Decision-20 three-tier slab structure — the talk
demo at `runs/2026-05-21-talk-prep/code/04-mixture-recovery-synthetic.py`
used `TRUE_ALPHA = 0.5` for a one-tier illustration and is not an
empirical-α anchor. The five-point grid covers the prereg's required range
without overcommitting to a numeric prior on the empirical posterior;
post-smoke-test refinement is permitted under Decision 21's Revisit
triggers ("the pre-Phase-2 design artefact reveals the empirical pilot
α range is narrow enough that a coarser α grid is sufficient (or wide
enough that a finer α grid is needed)").

### 2.2 Genuine-shape library

**Pinned shapes:** 6 shapes (prereg §4 line 328 / Decision 21 line 1894):
{smooth growth, smooth decline, rise-and-fall (Gaussian), multi-modal
(bimodal), regnal-cluster (mirrors Decision 20's empirical pattern),
flat-baseline}.

Each shape is an 80-bin probability vector over the 50 BC – AD 350 envelope
at 5-year bins (envelope and binning per prereg §3 line 169). Specified
parametrically. All shapes normalise to sum to 1 on the bin grid.

| # | Name | Parameters | Generating function |
|---|---|---|---|
| 1 | `flat_baseline` | — | Uniform 1/80 in every bin. |
| 2 | `smooth_growth` | rate = 0.005 per year | `f(t) ∝ exp(rate · (t − envelope_min))`, normalised. |
| 3 | `smooth_decline` | rate = 0.005 per year | `f(t) ∝ exp(−rate · (t − envelope_min))`, normalised. |
| 4 | `rise_and_fall` | μ = 150, σ = 60 | `f(t) ∝ exp(−0.5 · ((t − μ)/σ)²)`, normalised. |
| 5 | `bimodal` | μ₁ = 50, σ₁ = 40, μ₂ = 250, σ₂ = 40, mix = 0.5 | Equal-weight mixture of two Gaussians, normalised. |
| 6 | `regnal_cluster` | spikes at AD 77.5 (Flavian, weight 0.20), AD 122.5 (Hadrianic, weight 0.30), AD 212.5 (Severan, weight 0.15); each spike a Gaussian with σ = 7.5 years; remaining mass (0.35) distributed as a smooth-growth baseline at rate 0.003 per year | Sum of three Gaussian spikes plus a smooth-growth baseline, normalised. |

**Justification.** The six shapes cover the six prereg-binding categories
verbatim (Decision 21 line 1893-1896). The `regnal_cluster` shape mirrors
the three real narrow-precision spikes identified in the empirical-SPA
shape diagnostic at `runs/2026-05-17-empirical-spa-shape/` and codified in
Decision 20: AD 77.5 Flavian, AD 122.5 Hadrianic, AD 212.5 Severan. The
Gaussian σ = 7.5 years gives a spike that resolves cleanly at the 5-year
bin (matching the §3 line 169 binning rationale: bin width ≤ event width / 3
for Gaussian-tapered recovery; here event ~ 15 y FWHM, bin = 5 y, ratio
3:1). The bimodal shape (peaks at 50 / 250) is distinct from
rise-and-fall and is one of the qualitatively-distinct shapes the prereg
calls for ("multi-modal", line 328).

The "pilot-posterior-drawn" tier-weight vector category referenced in
Decision 21 line 1898 corresponds to a draw from a pilot posterior on the
Decision-20 slab structure that has not yet been fit on real data — see
§2.3 below for how this is operationalised.

### 2.3 Tier-weight vectors

**Three tiers** per Decision 20 line 1755-1759 (template-interval slab
structure): (1) century-slab tier, (2) half-century-slab tier, (3)
reign-interval-slab tier. (The prereg flags a fourth "BC-AD-boundary" tier
as a known limitation in §9 / Decision 20 line 1804-1807; it is not in the
recovery grid.)

**Pinned vectors (5 vectors over (century, half-century, reign) weights):**

| # | Name | Vector | Rationale |
|---|---|---|---|
| 1 | `uniform` | (1/3, 1/3, 1/3) | Equal weights across tiers — null-hypothesis weighting (Decision 21 line 1898). |
| 2 | `century_heavy` | (0.70, 0.20, 0.10) | Reflects the empirical dominance of century templates (`[1, 100]` alone = 26 % of corpus per Decision 20 line 1671). |
| 3 | `half_century_heavy` | (0.20, 0.70, 0.10) | Counter-factual — what if editorial practice were dominated by half-century templates (`[1, 50]`, `[125, 175]`, etc.). |
| 4 | `reign_heavy` | (0.20, 0.10, 0.70) | Counter-factual — what if reign-interval tagging dominated. |
| 5 | `pilot_proxy` | (0.55, 0.30, 0.15) | Proxy for the not-yet-fit empirical pilot posterior. Anchored on the empirical endpoint-frequency evidence (Decision 17 lines 1314-1316: 54.5 % `not_before` endings in `01`, 53.0 % `not_after` endings in `00`) suggesting century > half-century > reign in the corpus. |

**Justification.** The five vectors cover the five prereg-binding
categories verbatim (Decision 21 line 1897-1899): uniform, century-heavy,
half-century-heavy, reign-heavy, pilot-posterior-drawn. The
`pilot_proxy` substitutes for a true pilot-posterior draw — no pilot fit
has yet been run on real LIRE data under the Decision-20 three-tier
structure (the only mixture fit to date is the one-tier talk demo). The
proxy's (0.55, 0.30, 0.15) vector is anchored on the
endpoint-frequency descriptive evidence rather than a posterior draw, and
this substitution is flagged transparently in the run report. If a pilot
fit becomes available before the production grid runs, this vector should
be replaced by an actual posterior draw — but this artefact is committed
now so the simulation can proceed.

### 2.4 Sample sizes N

**Pinned values:** `N ∈ {2000, 10000, 50000}` (3 values).

**Justification.** The prereg requires "representative N values from
empire, province, and urban-area levels (specific N's pinned from the
Phase 1 simulation's reachability map)" (Decision 21 line 1900-1902;
prereg §4 line 330: "from Phase 1's reachability map"). Reference to the
Phase 1 reachability map at
`runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md`:

- **Empire-level:** bracket A (50 % effect, ≥ 50 y) reachable only at
  N = 50,000 (REPORT-v2-final.md table, empire / a_50pc_50y row). The
  empire-wide corpus post-filter is 115,174 (prereg §2 / line 121),
  comfortably above; N = 50,000 is the **representative empire-level
  value**.
- **Urban-area boundary:** bracket A binding-Gaussian threshold = 1,549
  inscriptions (REPORT-v2-final.md, urban-area / a_50pc_50y / cpl /
  gaussian). N = 2,000 represents the **urban-area boundary** — a
  conservative round-up that resolves the boundary cleanly.
- **Province / mid-range:** province bracket A reaches at ~ 1,400-2,500
  (REPORT-v2-final.md province rows); N = 10,000 represents a typical
  province (Hispaniae, Pannoniae) and a high-coverage urban area
  (Aquileia, Tarragona; cf. §2.3 city-population list).

Three N values across two orders of magnitude cover the empirical range
without proliferating cells unnecessarily. (The prereg's wording
"representative N values from empire, province, and urban-area levels"
naturally maps to one N per level — three.)

### 2.5 Replicates per cell

**Pinned value:** 100 replicates per cell.

**Justification.** Prereg §4 line 331 states "Design-artefact default is
100" and §3 line 210 says "≥ 100 replicates per cell". The 100-replicate
default is binding under this artefact. The "two-stage variant running 50
across the full grid to identify failure regions and 200 at boundary
cells" (Decision 21 line 1903 / prereg §4 line 331) is **not** invoked here
— this artefact uses the simpler one-stage default. Two-stage is reserved
as a Revisit-trigger response if the grid uncovers boundary failures.

### 2.6 Seed policy

`seed = base_seed + cell_index`, where `base_seed = 20260522` and
`cell_index` runs over the deterministic grid enumeration (alphabetical
on shape × ascending α × ascending tier-vector index × ascending N).
Within a cell, replicate `r` uses `cell_seed * 1000 + r` to keep
intra-cell seeds easily decomposable. Reproducibility is the binding
property (Decision 21 line 1904-1905).

## 3. Total simulation cost estimate

Total cells: 5 (α) × 6 (shapes) × 5 (tier-weights) × 3 (N) = **450 cells**.
Total fits: 450 × 100 = **45,000 fits**.

Per-fit cost on sapphire — to be measured by the smoke test. Anticipated
range: 5-15 s for the three-tier multinomial model with NUTS (4 chains ×
2 000 draws × 1 000 tune, target_accept = 0.95), based on the talk
demo's one-tier ~ 3-5 s/fit timing scaled by parameter count (the
three-tier model adds two Dirichlet-shaped tier weights and replaces the
parametric Gaussian p_gen with a Gaussian-random-walk smoothness prior on
80 latent bin-log-density values — meaningfully more state, but the
likelihood remains a single multinomial). The smoke test pins the
empirical per-fit time before the grid launches.

**Sapphire wall-clock estimate (24 physical cores; n_jobs = 20):**

- At 5 s/fit: 45,000 × 5 s ÷ 20 ≈ **11,250 s ≈ 3.1 h**
- At 10 s/fit: 45,000 × 10 s ÷ 20 ≈ **22,500 s ≈ 6.3 h**
- At 15 s/fit: 45,000 × 15 s ÷ 20 ≈ **33,750 s ≈ 9.4 h**

Bottleneck: NUTS sampling per fit (single-threaded inside one fit; pymc's
4-chain parallelism is captured inside the per-fit budget — n_jobs in the
outer joblib loop fans out across cells, not chains). If pymc's default
multiprocessing chain parallelism conflicts with joblib's outer
parallelism (chain workers × n_jobs > 24), the outer n_jobs is capped at
6 (= 24 / 4) — to be checked at smoke-test time.

## 4. Expected outputs

Production run (after smoke test passes; per
`runs/2026-05-22-recovery-grid-validation/`):

- `data/synthetic-cells/<cell_id>/replicate_<i>.parquet` — synthetic
  multinomial draws (80 bins each), one per replicate per cell. 45,000
  files total.
- `outputs/cell-fits/<cell_id>/replicate_<i>-posterior.parquet` —
  per-replicate posterior summaries (α 95 % CI, posterior-median p_gen
  vector, Pearson r vs truth, Wasserstein-1 vs truth, R-hat, ESS_bulk).
- `outputs/cell-summaries/<cell_id>-summary.json` — per-cell aggregates:
  α-coverage rate, median Pearson r, median W-1, replicate count, any
  flagged non-convergence.
- `outputs/REPORT.md` — final grid-level report: global pass rates against
  the 90 % / 90 % thresholds, cell-wise table of pass / fail with failure
  mode characterisation, recommendations on whether to declare the model
  validated.
- `outputs/grid-state.json` — checkpoint after each cell; lets the run
  resume.

## 5. Decision rule

Per prereg §4 lines 333-334 (binding):

1. **Cell passes coverage** if ≥ 90 % of its replicates produce a posterior
   95 % CI on α that contains the true α.
2. **Cell passes shape recovery** if the posterior-median Pearson r between
   recovered and true `p_gen` is ≥ 0.95. (The wording at prereg §3 line 210
   uses "in ≥ 90 % of cells" — the cell-level criterion is on a per-replicate
   median; the global criterion below is the ≥ 90 %-of-cells aggregation.)
3. **The mixture is validated** if (a) ≥ 90 % of cells pass coverage AND
   (b) the posterior-median Pearson r is ≥ 0.95 in ≥ 90 % of cells.

Failure of either binding criterion triggers an OSF amendment and model
revision per prereg §4 line 334. Wasserstein-1 is reported as
supplementary distribution-sensitive shape evidence (prereg §3 line 210,
§4 line 334) but is not part of the binding rule.

## 6. Deferred from this artefact

Two threshold categories scoped to the `runs/2026-05-XX-recovery-grid-design/`
directory in the prereg (§4 lines 337-338) are **deferred to a follow-up
pin** under this artefact:

1. **Wasserstein-1 flagging threshold** — pinned post-smoke-test, once an
   empirical W-1 distribution is available to anchor the threshold. Until
   pinned, W-1 is reported per cell without a binding flag rule.
2. **Numerical PPC thresholds for H3a** (prereg §3 line 251-258) — pinned
   pre-Phase-3 once the H3a pilot fit produces posterior-predictive
   distributions. Out of scope for the recovery simulation.

Both deferrals are flagged in the artefact's commit message.

## 7. Cross-references

- Prereg §3 lines 165-210 (analysis pipeline; Bayesian mixture model spec).
- Prereg §4 lines 323-338 (Phase 2 / H2.1 procedural commitments).
- Decision 17 (superseded by Decision 20; retained context only).
- Decision 19 (multinomial primary observation model).
- Decision 20 (template-interval slab structure; three-tier convention).
- Decision 21 (recovery-grid procedural pre-commitment).
- Phase 1 reachability map: `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2-final.md`.
- Talk-demo simplified one-tier recovery:
  `runs/2026-05-21-talk-prep/code/04-mixture-recovery-synthetic.py`.
