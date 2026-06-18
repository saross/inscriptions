# C10 follow-up "(ii)" — realism-graded ground-truth recovery (BUILD-NOTES, pre-audit)

Status: **BUILT, NOT RUN.** No fit, MCMC, diagnostic, or SSH was executed. Only
`py_compile`, the non-MCMC generator / count-builder / decision-rule logic, and
graph-build-only model construction were exercised. This note is for the standing
pre-run audit; the realism-graded generator's faithfulness to the mechanism (below)
is the key audit target.

Author: Claude (Opus 4.8, 1M context) on Shawn's brief, 2026-06-19. UK/Aus English.

## The puzzle (ii) resolves

The first validity test (`run_c10.py` / `outputs/VALIDITY-REPORT.md`) found a
contradiction:

- **1b (synthetic, idealised §2 generator):** the point-date aoristic-MC RECOVERS
  the planted α as well as the mass arm (max |Δα| 0.046) — verdict **(a)**.
- **1c (real empire):** point-collapse α = **0.100** vs mass-preserving α = **0.615**
  — a large divergence the synthetic did **NOT** reproduce.

So the idealised §2 synthetic generator is missing whatever real-data feature drives
the collapse. (ii) GRADES the realism of the generator and asks, per variant: *does
the point-date arm now DIVERGE from the mass arm (and/or collapse toward the ~0.1
floor), reproducing the 1c real-empire gap?*

## The mechanism (the design crux — please audit this first)

Point-date sampling draws `t ~ Uniform(RECORDED interval)`. It **never uses the
latent true date.** Therefore — for a convention inscription whose recorded interval
IS the slab — BOTH arms see a flat-over-slab shape *regardless* of the true-date
distribution. The idealisations that can drive the collapse must live in the
**RECORDED-interval / observed dimensions**, NOT in the latent true date. The
first-wave (R0) generator idealises the recorded dimension two ways:

1. **Interval widths.** R0: convention = exact (wide, round) library slabs;
   genuine = tight ±2.5 y (one 5-year bin). Real data (profiled from the empire
   subset; see below): the real **non-aligned** subset carries a BROAD spread of
   widths — many WIDE non-round intervals (median 41 y; modes at 59, 78, 129 y), not
   just tight ones. A point-date sample of a wide non-aligned interval spreads as
   broadly as a wide aligned one, so the TEMPORAL CONTRAST between the two alignment
   subsets — which is what the cross-classified α reads — is washed out.
   → **R1, the PRIMARY hypothesis.**
2. **θ separation.** R0 yields P(aligned|convention) = 1.000, P(aligned|genuine) =
   0.000 — a PERFECTLY separable alignment signal. Production θ is θ_conv ≈ 0.93,
   θ_gen ≈ 0.025 (`refit_lib.adopted_theta_priors`): ~7 % of convention inscriptions
   are recorded non-aligned, ~2.5 % of genuine ARE aligned. That cross-contamination
   puts convention mass into the non-aligned subset and vice versa, again eroding the
   contrast. → **R2.**
3. **In-slab true-date shape** (the originally-named variant). R0 draws the
   convention true date Uniform(slab). A non-uniform in-slab shape is the obvious
   "realism" knob — but by the mechanism above it should make **no difference** to
   recovery, because neither arm uses the true date. → **R3, a confirmatory NULL.**

The real driver may be joint, so we also run **R1+R2**.

## The variants built (`code/c10_ii_lib.py`)

`generate_inscriptions_variant(variant, alpha_true, n, seed, slabs, p_gen, …)`. The
planted-α machinery is IDENTICAL across variants: `type_i ~ Bernoulli(alpha_true)`
(1 = convention, 0 = genuine). Variants change ONLY the recorded-interval emission
and (R3) the in-slab true-date shape.

| variant | what is relaxed vs R0 | expected outcome |
|---|---|---|
| **R0** | nothing — delegates VERBATIM to `c10_lib.generate_inscriptions` | negative control; must NOT reproduce ((a)-verdict baseline) |
| **R1** | recorded WIDTHS drawn from the real empire per-subset width distribution | **PRIMARY**: predicted to reproduce |
| **R2** | alignment a realistic θ mix (θ_conv ≈ 0.93, θ_gen ≈ 0.025) | may reproduce / partially |
| **R3** | convention in-slab true date U-shaped (Beta(0.5, 0.5)) not Uniform | confirmatory NULL; predicted NOT to reproduce |
| **R1+R2** | R1 widths AND R2 θ contamination | the joint effect |

Alignment is ALWAYS assigned at the end by the REAL
`joint_lib.aligned_indicator(rule="C")` on the recorded `[nb, na]` — never hand-set.
The variant logic controls only how the recorded interval is BUILT; the indicator
re-derives the label, and the two agree by construction (verified: `recorded_as` vs
the indicator agree ≥ 98.5 % across variants).

### R0 == the existing idealised generator (parameterisation invariant)

`variant="R0"` delegates verbatim to `c10_lib.generate_inscriptions` with the same
seed and arguments. **Verified byte-identical** on the `[type, t_true, nb, na,
date_range, aligned]` columns. The realism knobs are strictly additive; R0
reproduces the (a)-verdict baseline.

### How R1 samples the real width distribution

`real_empire_width_dist("empire-aggregate")` follows the SPEC path exactly:
`h2_lib.load_filtered_lire` → `refit_lib.subset_for` (empire-aggregate) →
`joint_lib.aligned_indicator(rule="C")` → the per-subset histogram of
`date_range = na − nb`. It stores the observed `(width, count)` histogram for each
subset and draws widths by exact inverse-CDF (categorical) sampling — no smoothing,
because the widths ARE discrete integer years. (Profiled values: aligned median
99 y, dominated by the round F1/F3 widths {99, 199, 49, 149, 299, 29, 39}; non-
aligned median 41 y, a broad spread.) A synthetic **convention** inscription draws
its width from the **aligned-subset** histogram; a **genuine** inscription from the
**non-aligned-subset** histogram. (Under R2 the width is keyed to the *intended*
recorded alignment, so a θ-contaminated convention recorded non-aligned gets a non-
aligned-style width, and vice versa.)

## Design choices / ambiguities — FLAG FOR AUDIT

1. **R1 convention "slab centre" placement given a sampled width
   (`_place_aligned_interval`).** A convention inscription must be RECORDED aligned
   (rule C). The sampled aligned width is first SNAPPED to the nearest rule-C family
   width ({F1} ∪ {F3} = {19, 24, 29, 39, 49, 99, 149, 199, 299}) so it is alignable
   with round endpoints (the real aligned subset is itself dominated by exactly these
   widths, so the snap is small and rarely binds). The lower endpoint is then placed
   on the 25-year grid, chosen so the convention true date `t_true` falls INSIDE
   `[nb, nb + width]` (the slab the editor chose contains the inscription's date —
   the R0 semantics where `t_true ~ Uniform(slab) ⊂ slab`). The anchor offset is
   drawn Uniform(0, width). **Audit: confirm the snap-to-family-width + 25-grid
   placement is an acceptable "centred on a slab/round position", or specify an
   alternative (e.g. round the endpoints to the nearest 50 and accept the resulting
   width).**

2. **R1/R2 non-aligned interval placement (`_place_nonaligned_interval`).** A
   genuine (or θ-contaminated convention recorded non-aligned) inscription gets a
   recorded interval of the sampled non-aligned width, bracketing `t_true` at a
   uniform position, with the lower endpoint nudged OFF the 25-y grid by a shift in
   {3, …, 22} so rule C fails on at least one endpoint (genuinely non-round). Tight
   widths (≤ `TIGHT_MAX` = 4) are left as-is (they are `Tight` → non-aligned
   regardless). **Audit: confirm the off-grid forcing is the intended way to make a
   non-aligned interval of a real non-aligned width.**

3. **R2 alignment-consistent recorded intervals (the contamination mechanism).** R2
   assigns each inscription an INTENDED recorded alignment: a convention is recorded
   ALIGNED with prob `theta_conv` (≈ 0.93, read from the artefact) — else non-aligned
   (a wide non-round bracket); a genuine is recorded ALIGNED with prob `theta_gen`
   (≈ 0.025) — else non-aligned (tight, idealised case) / its real width (R1+R2). The
   recorded interval is then BUILT with the aligned vs non-aligned placement helper
   per that intent, so the REAL indicator re-derives the intended label. **Verified:
   realised θ_conv = 0.927, θ_gen = 0.024 under R2 — on target.** θ_conv / θ_gen
   MEANS are read from `refit_lib.adopted_theta_priors`'s `theta_fit`, not hardcoded.
   **Audit: confirm "assign alignment as the realistic mix consistent with those θ"
   is correctly operationalised as a per-inscription Bernoulli on the recorded-
   alignment intent.**

4. **R3 non-uniform in-slab true-date shape.** Beta(0.5, 0.5) (U-shaped, mass piled
   at the slab edges) scaled to `[lo, hi]` — the most adversarial departure from
   Uniform(slab). The recorded interval is otherwise as R0 (the slab). **Audit:
   confirm an edge-weighted U is the intended "non-uniform"; recovery is predicted
   UNCHANGED (the confirmatory null) because neither arm uses the true date.**

5. **θ PRIOR fed to the model is the production `adopted_theta_priors`** (θ_conv ≈
   0.93, θ_gen ≈ 0.025) for ALL variants — including R0 (whose realised separation is
   1.0 / 0.0). This is intentional: the model is told the production prior, not the
   synthetic truth, exactly as in the first wave. Under R0 there is a mild prior–data
   tension (the binomial likelihood pulls θ_conv up / θ_gen down from the prior); the
   first wave already ran this way and recovered α cleanly, so it is not a confound.
   **Audit: confirm we keep the production θ prior for all variants (so the only
   thing changing across variants is the DATA, not the prior).**

6. **`N_SEEDS = 2`** (SPEC (ii): "≥ 2 generator seeds"), 5 variants × 4 α × 2 seeds =
   **40 cells**, each a mass fit + a 10-realisation point-date arm. At synthetic
   N = 3000 (each fit ~seconds–minutes), this is a few core-hours — same footing as
   the first wave's 1b, scaled by the variant count. **Audit: confirm 2 seeds and
   N_synth = 3000 are adequate; the first wave used 3 seeds at N_synth = 3000.**

## Decision rule (pre-registered here)

Per variant, over its α-sweep:

- the **mass arm recovers** planted α if `max |mass α − planted| ≤ RECOVERY_TOL`
  (= 0.1);
- the **arms diverge** if `mean |mass α − point-date α| ≥ DIVERGENCE_TOL` (= 0.15;
  the real 1c gap is ≈ 0.52);
- the point-date arm is **near the floor** if `median point-date α ≤ PILOT_FLOOR +
  RECOVERY_TOL` (= 0.20; pilot/1c floor ≈ 0.10).

A variant **REPRODUCES the 1c collapse** if `mass_recovers AND (arms_diverge OR
near_floor)`. The overall verdict NAMES the reproducing variant(s) (R1 → realistic
interval widths; R2 → θ contamination; R1+R2 → the joint effect) and flags whether
the controls are clean (R0 and R3 must NOT reproduce). **Verified on stubs:**
(a)-shape → not reproduced; collapse-to-floor → reproduced; divergence-without-floor
→ reproduced; overall verdict names the reproducer and reports control cleanliness.

## Files built

| File | Role |
|---|---|
| `code/c10_ii_lib.py` | The **new** realism-graded generator (R0 delegates to `c10_lib`; R1/R2/R3/R1+R2 new), the real-empire width-distribution profiler, the recorded-interval placement helpers, and the realised-θ diagnostic. Imports `c10_lib` / `h2_lib` / `joint_lib` / `refit_lib`; performs NO MCMC. |
| `code/run_c10_ii.py` | The per-variant recovery sweep + per-variant and overall verdicts + report writer. REUSES `run_c10`'s validated arm-fitters (`_fit_mass_arm`, `_fit_pointdate_arm`, `_alpha_stats`) and `c10_lib`'s count builders + `joint_lib.build_model_cross_classified`. Performs MCMC — runs only **after** audit sign-off. |

Both pass `py_compile`. `idata` `.nc` are gitignored
(`runs/2026-06-18-c10-validity-test/outputs/*.nc`, root `.gitignore` line 148); this
wave writes only `outputs/followup-ii-results.json` + `outputs/followup-ii-report.md`
(no `.nc` is persisted — α draws are pooled in-memory, as in the first wave).

### Post-audit run command (sapphire/zbook — do NOT run during build)

```bash
cd /home/shawn/Code/inscriptions
.venv/bin/python runs/2026-06-18-c10-validity-test/code/run_c10_ii.py \
    --variants R0 R1 R2 R3 R1+R2
```

(`--variants R0 R1` runs just the negative control + primary hypothesis if a quick
cut is wanted first.) Writes `outputs/followup-ii-results.json` +
`outputs/followup-ii-report.md`. Uses the production sampler config (no
negotiate-down): `h2_lib.N_DRAWS=2000`, `N_TUNE=1000`, `N_CHAINS=4`,
`TARGET_ACCEPT=0.95`, cores = 1 (via the reused `run_c10._sample_alpha`).

## Confirmations

- **Nothing was run** (no fit/MCMC/diagnostic/SSH). Only `py_compile`, the non-MCMC
  generator / count-builder / decision-rule logic, the real-empire width profiling
  (pure data load + numpy), and graph-build-only model construction were executed.
- **No lodged/shared module was modified** — `joint_lib`, `refit_lib`, `h2_lib`,
  `cell_lib`, and the slab library are imported/read only.
- **The existing `c10_lib.py` / `run_c10.py` were NOT modified** — they are imported
  and extended in the NEW files `c10_ii_lib.py` / `run_c10_ii.py`.
- Commit uses explicit pathspecs confined to `runs/2026-06-18-c10-validity-test/`.
