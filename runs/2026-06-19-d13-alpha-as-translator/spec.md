# D13 α-as-translator — implementation spec (Option A)

**Status:** ✅ EXECUTED 2026-06-19 — signed off and run; results in
`outputs/D13-REPORT.md` and lodged as **Obs 107** (β_within +0.431 → +0.422, clean
null; H3a NOT confounded by per-city convention intensity). The original "DRAFT …
Do NOT launch compute until signed off" stamp is superseded.
**Author:** Claude Code (Opus 4.8) on Shawn's brief, 2026-06-19. UK/Australian English.
**Route chosen by Shawn (2026-06-19):** Option A (prereg-literal, standalone per-city α at
N ≥ 100, with uncertainty propagation). Option B (hierarchical partial-pooling) to be
discussed separately *after* A is launched.

---

## 1. What this delivers (the lodged obligation)

The lodged exploratory/sensitivity analysis, verbatim
(`planning/osf-supplementary-2026-05-20.md:349`,
`planning/preregistration-draft.md:382`):

> **α-as-translator sensitivity analysis for H3a:** include per-city posterior mixture α as
> an additional covariate in the NBR; test whether the within-province β estimate shifts
> meaningfully. Informs whether the Hanson correlation is confounded by epigraphic-habit
> intensity. (Caveat: per-city α is unidentified for low-N cities; this sensitivity is
> restricted to cities with N ≥ 100, ~ 200 cities.)

This is an **exploratory/sensitivity** analysis (prereg §5 block), **not confirmatory** — no
confirmatory decision rule rides on it. It is nonetheless an outstanding preregistered
obligation to report.

**Substantive question:** is the H3a within-province population–epigraphy scaling (β_within /
`f_within`) confounded by per-city editorial-convention intensity (α_c)? Adding α_c as a
covariate and watching β_within answers it. The province-level proxy (Obs 94, the
deconvolution-leverage diagnostic) already found α uncorrelated with population
(Spearman −0.11; implied Δβ ≈ 0); D13 is the **city-level** version of the same test. The
*expected* result is therefore a null (no meaningful β_within shift), but the city-level test
is the lodged deliverable.

---

## 2. The identifiability tension (must be reported, not hidden)

The prereg's "N ≥ 100 identifies α_c, ~200 cities" assumption **predates** the project's own
measured reachability map (Decision 34; `runs/2026-06-03-small-n-reachability/outputs/REPORT.md`),
which found standalone subset-specific α recovery is only **16 % reliable at N = 100**
(|α-bias| ≈ 0.135), with the reliable floor at **N ≈ 500–2000**. So per-city α at the sizes
where we have cities is largely prior-dominated / biased.

**Verified feasibility census** (Latin frame `data/processed/city_level_for_h3a_latin.parquet`,
817 cities / 39 provinces; re-run by the implementing agent and reproduced in the report):

| Threshold | Cities | Provinces | Provinces with ≥2 such cities |
|---|---|---|---|
| N ≥ 100 | 163 | 36 | 26  (regression-feasible) |
| N ≥ 500 | 18 | 11 | 2 |
| N ≥ 1000 | 8 | 6 | 1 |
| N ≥ 2000 | 5 | 4 | 1 |

The irreducible tension: where the within-province regression is feasible (N ≥ 100), α_c is
unreliable; where α_c is reliable (N ≥ 500), within-province leverage is gone (only 2
provinces have ≥2 cities). **Option A handles this honestly by (a) propagating the per-city α
posterior uncertainty into the NBR so unreliability surfaces as wide coefficient uncertainty
rather than false precision, (b) annotating every city by whether it clears the floor, and
(c) cross-checking against the province-level proxy.** This is the design limitation the
report must foreground.

---

## 3. Stage 1 — per-city α (the new per-city mixture build)

**No per-city α exists yet** (only the 29 production units, 5 of which are single cities).
Stage 1 produces it.

**City set:** the **163 Latin-frame cities with `inscription_count` ≥ 100**
(`city_level_for_h3a_latin.parquet`). Latin frame, not all-provinces (consistent with the
lodged primary frame, Decision 36 / Amendment 02).

**Model:** the **current production deconvolution** — the recovery-validated cross-classified
`library` model under the adopted re-derived θ prior (θ_conv ≈ 0.930, θ_gen ≈ 0.025, κ = 40),
fit **standalone per city**. This is exactly the production refit
(`runs/2026-06-13-cc-production-refit/code/run_refit.py`) pointed at cities instead of the 29
units. Reuse verbatim: `fit_one`, `build_unit_cc_data`, `subset_for`, `load_library_basis`,
`adopted_theta_priors`, and `h2_lib`'s corpus loader / aoristic SPA / family classifier /
largest-remainder. Sampling settings inherited unchanged (`H.N_DRAWS`/`N_TUNE`/`N_CHAINS`/
`TARGET_ACCEPT`).

**Implementation:** a thin new driver `code/run_city_alpha.py` + helper `code/city_lib.py`
that:
- enumerates the 163 cities as units `{"name": city, "kind": "city", "frame": "latin",
  "filter": ("urban_context_city", city), "unit_index": i}`;
- extends `subset_for` (or adds a local branch) to handle the `("urban_context_city", name)`
  filter: `df.loc[df["urban_context_city"] == name]`;
- **reconciliation gate (REQUIRED, pre-fit):** for each city, assert the mixture subset row
  count reconciles with the H3a `inscription_count` for that city (same 50 BC – AD 350 window,
  same Latin frame). If `H.load_filtered_lire()` applies a different window/filter than the
  H3a frame builder, halt and report — do NOT silently fit on a mismatched corpus. Record the
  per-city (H3a-count, mixture-subset-N, aoristic-effective n_rows) triple.
- reuses the refit's ProcessPoolExecutor (spawn + `max_tasks_per_child`), `--n-jobs`, atomic
  per-city JSON writes, unit-granular resume, STATUS file;
- **persists the full per-city α posterior draws** (`outputs/alpha-draws/<city>-alpha.npz`,
  α vector shape (n_draws_total,)), analogous to the refit's `--emit-draws` p_gen hand-off —
  required for Stage 2 propagation.

**Per-city outputs (JSON):** `alpha_median`, `alpha_ci_lo/hi`, `alpha_post_sd`, convergence
(`max_rhat`, `min_ess_bulk`, `n_divergences`, `convergence_pass`), `n_rows_eff`, the
H3a `inscription_count`, and a **reachability flag** (`reliable` iff N ≥ 500; `caveated`
otherwise — N is the H3a count). PPC adequacy as in the refit.

**Seed:** new base `D13_BASE_SEED = 20260619`; per-city seed = base + city_index
(collision-free).

**Compute:** ~163 fits, ~30–130 s each, N-independent (NUTS over the fixed bin grid).
Parallelised n_jobs ≈ 12 on sapphire ⇒ **~15–30 min**. Sapphire, `~/Code/inscriptions`,
`uv run`, root-fs `TMPDIR`, cgroup `MemoryMax` via the launch wrapper (reuse the refit's
launch pattern verbatim).

---

## 4. Stage 2 — augmented H3a NBR + propagation

Reuse the H3a confirmatory machinery: `runs/2026-06-04-h3a-confirmatory/code/02-h3a-fit.py`
(`build_model`, `f_within`, `summarise_f`) and `h3a_common.py` (Latin frame builder,
`standardise_predictors`). The implementing agent **must read these files** and reuse them;
do not re-derive the NBR. Base comparison = the existing Latin-frame H3a fit (β_within,
`f_within`, unweighted primary).

Augment `log_mu` with a per-city α covariate:
`log_mu = α0 + α_prov[prov] + β_within·within + β_between·between + γ·α_c_std`
where `α_c_std` is the standardised per-city α.

- **S2a — prereg-literal primary.** `α_c_std` = standardised **posterior-median** α_c (the
  literal "include per-city posterior mixture α as a covariate"). One NBR fit on the 163-city
  Latin frame. Report β_within, `f_within` (unweighted), and γ, each vs the **base** H3a Latin
  fit on the same 163 cities (re-fit the base on the identical 163-city subset so the only
  difference is the α_c term — not the full-frame base). **Pre-specified "meaningful shift"
  yardstick:** the D11 precedent — a `f_within` posterior-median/CI shift ≥ **0.063** is
  "material" (continuity 2026-06-16: D11 max CI shift 0.047 < 0.063 → no material divergence);
  additionally report the β_within shift against its posterior SD and CI overlap. State the
  yardstick *before* seeing the result.

- **S2b — uncertainty-propagation (the honesty layer for §2).** Multiple imputation: draw
  M = 50 per-city α-vectors from the Stage-1 posteriors, fit the augmented NBR on each, pool
  β_within / `f_within` / γ via Rubin's rules. This respects the full, bounded, often
  prior-piled per-city α posteriors and propagates the reachability-driven unreliability into
  the coefficient uncertainty. (Considered and rejected as primary: a single measurement-error
  NBR with logit-α_c ~ Normal(post-mean, post-sd) — cleaner but mis-states the non-Gaussian
  low-N posteriors.)

- **S2c — reachability robustness.** (i) Re-run S2a on the N ≥ 500 subset (18 cities) as a
  "reliable-α" cross-check, explicitly flagged as within-province-leverage-thin (descriptive,
  not a within-province regression). (ii) Report the city-level α_c-vs-population scatter +
  robust slope (Theil-Sen) — the city-level extension of the Obs 94 province-level proxy.

**Covariate form note:** the prereg says "an additional covariate"; primary keeps α_c as a
single city-level predictor. A Mundlak within/between split of α_c is reported as a secondary
only if S2a shows any movement (otherwise it adds nothing to a null).

---

## 5. Hard-stops (agent brief — standing rule)

- Do **NOT** silently reduce draws/tune/chains, M, or city count to fit a time budget. Halt
  and report.
- If the Stage-1 per-city N reconciliation gate fails (mixture corpus ≠ H3a frame), **halt** —
  do not fit on a mismatched corpus.
- If > ~10 % of cities fail convergence (`convergence_pass` False), halt and report before
  Stage 2 — broad non-convergence changes the interpretation.
- `/audit` (or a code-review agent) each new script **before** running it on sapphire; fix
  criticals first. Commit before each stage (research-record preservation).
- Sapphire only for the fits; workdir `~/Code/inscriptions` (NOT `~/inscriptions`); `uv` at
  `~/.local/bin/uv`.

---

## 6. Outputs

`runs/2026-06-19-d13-alpha-as-translator/`:
- `code/city_lib.py`, `code/run_city_alpha.py`, `code/h3a_alpha_translator.py` (Stage 2)
- `outputs/units/<city>.json` (163), `outputs/alpha-draws/<city>-alpha.npz`
- `outputs/city-alpha-summary.json` (census + per-city α + reachability flags)
- `outputs/D13-REPORT.md` — census (reproduced), per-city α distribution, S2a/S2b/S2c results,
  the explicit identifiability caveat (§2), the proxy cross-check, and the verdict on whether
  β_within shifts meaningfully.
- One figure: α_c-vs-population scatter with the robust slope.

**On completion:** `/observe` a new Obs (D13 result, cross-referencing Obs 94), update the
continuity "Remaining work" inventory, commit + push.

---

## 7. Open design decisions for Shawn (confirm before launch)

1. **Frame** = Latin (163 cities), not all-provinces (169). [Recommended: Latin — the lodged
   primary frame.]
2. **Model** = the current cross-classified `library` production deconvolution under adopted
   θ, standalone per city. [vs the older single-stream `build_model_f1_f3`.]
3. **Propagation** = S2a point-median primary + S2b multiple-imputation (M=50) robustness.
4. **"Meaningful shift" yardstick** = `f_within` shift ≥ 0.063 (D11 precedent) + β_within
   shift vs posterior SD.
5. **Reachability handling** = annotate all; S2c N≥500 cross-check + proxy scatter.
