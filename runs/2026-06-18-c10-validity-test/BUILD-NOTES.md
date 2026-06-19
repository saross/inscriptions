# C10 validity test — BUILD-NOTES (pre-audit)

Status: **✅ EXECUTED 2026-06-18 (first wave) + 2026-06-19 (follow-up ii).** The
original "BUILT, NOT RUN" banner is superseded — both result waves ran. See
`REPORT.md` (top-level), `outputs/VALIDITY-REPORT.md` ("(a) SUPPORTED — C10
stands"), `outputs/followup-ii-report.md`, and `outputs/run-c10-full.log`. This
file is retained as the build-decision / pre-run-audit record.

Author: Claude (Opus 4.8, 1M context) on Shawn's brief, 2026-06-18. UK/Aus English.

## Files built

| File | Role |
|---|---|
| `code/c10_lib.py` | The **new** synthetic per-inscription generator (SPEC §2/§3b), the two count representations, and the 1a diagnostics. Imports `h2_lib` / `joint_lib` / `refit_lib` (never modifies them). Performs NO MCMC. |
| `code/run_c10.py` | The 1a/1b/1c driver + SPEC §3b decision rule + report writers. Performs MCMC — runs only **after** audit sign-off. |

Both pass `py_compile`. All non-MCMC paths (generator, count builders, 1a metrics,
1c data prep, the decision rule, and the `build_model_cross_classified` call
signature via a graph-build-only check) were exercised and behave as specified;
nothing was sampled.

## How the generator implements SPEC §2 (the crux)

`c10_lib.generate_inscriptions(alpha_true, n, seed, slabs, p_gen, ...)`:

```
type_i ~ Bernoulli(alpha_true)            # 1 = convention, 0 = genuine
```

**CONVENTION** (verbatim logic) — recorded AS a round-number slab; true date
uniform over the slab:

```python
slab_idx = rng.choice(len(slabs), size=n_conv, p=slab_w)   # draw slab from library weights
lo = slab_lo[slab_idx]; hi = slab_hi[slab_idx]
nb[is_conv] = lo;  na[is_conv] = hi          # recorded interval = the slab [lo, hi]
t_true[is_conv] = rng.uniform(lo, hi)        # TRUE date ~ Uniform(slab)
```

**GENUINE** (verbatim logic) — tight bracket around a smooth-shape true date:

```python
bin_choice = rng.choice(N_BINS, size=n_gen, p=pgen_norm)   # true date ~ p_gen
within = rng.uniform(0.0, BIN_SIZE, size=n_gen)            # continuous within the bin
tg = BIN_EDGES[bin_choice] + within
t_true[~is_conv] = tg
nb[~is_conv] = tg - genuine_half_width        # TIGHT recorded bracket (±half y)
na[~is_conv] = tg + genuine_half_width
```

Alignment is then assigned by the **real** production indicator on the recorded
intervals (NOT hand-set):

```python
df["aligned"] = J.aligned_indicator(df, rule=R.ALIGN_RULE)   # rule "C"
```

The two count representations come from the SAME synthetic frame:

- **(i) aoristic-mass** — `c10_lib.mass_cc_counts` → `refit_lib.build_unit_cc_data`
  (each inscription's mass spread over its recorded interval; convention mass stays
  on the slab). Largest-remainder integers; `k == y_aligned.sum()`,
  `n_rows == y_aligned.sum() + y_nonaligned.sum()` asserted.
- **(ii) point-date** — `c10_lib.point_date_cc_counts` (`t_i ~ Uniform(recorded
  interval)`, one bin each, within FIXED alignment subsets). This is the lodged C10
  method reproduced from `run_supp.aoristic_mc_realisation` (reproduced, not
  imported, so we do not couple to the concurrent supp-wave dir). For convention
  inscriptions the sampled date is Uniform(slab) → reconstructs the true date and
  erases the slab concentration (the reading-(b) destruction mechanism).

## How 1a / 1b / 1c are wired

- **1a** (`run_1a`, NO MCMC): real empire-aggregate subset
  (`h2_lib.load_filtered_lire` → `refit_lib.subset_for` → rule-C
  `aligned_indicator`). Builds the aoristic-mass aligned SPA and `N_DIAG_SPA = 10`
  point-date aligned SPAs; computes the three §3a metrics for both — (i) L1 to
  nearest `production-slab-library.json` row, (ii) round-boundary (50 BC/AD0/50/…)
  mass fraction + ratio to uniform, (iii) best-fit non-negative slab-mixture weight
  (`scipy.optimize.nnls`).
- **1b** (`run_1b`, MCMC, decisive): sweeps planted α ∈ {0.3, 0.5, 0.68, 0.8} × 3
  seeds. Per cell: generate a frame, fit the **mass arm**
  (`build_model_cross_classified(pconv_mode="library")` once on the mass counts) and
  the **point-date arm** (the C10 build-once-then-`set_data` loop over `N_MC = 10`
  point-date realisations, pooling α draws). Records recovered α median + 95 % CI
  for both vs planted. `decide()` applies the SPEC §3b rule (verified on stub
  sweeps: (b)-shaped → "(b) CONFIRMED"; (a)-shaped → "(a) SUPPORTED").
- **1c** (`run_1c`, MCMC): real empire, aoristic-MC two ways — **point-collapse**
  (current C10) and **mass-preserving** (jitter recorded bounds ±1 bin, keep mass
  spread over the perturbed interval). N_MC = 10 each; compare pooled α.

### Post-audit run command (sapphire/zbook — do NOT run during build)

```bash
cd /home/shawn/Code/inscriptions
.venv/bin/python runs/2026-06-18-c10-validity-test/code/run_c10.py --stage all
```

(`--stage 1a` is the cheap deterministic-only stage and runs anywhere.) Writes
`outputs/results.json` + `outputs/VALIDITY-REPORT.md`.

## Design choices / ambiguities — FLAG FOR AUDIT

1. **Slab mixture weights → UNIFORM default.** The locked slab library stores no
   per-slab weights. `slab_mixture_weights` defaults to uniform over the 27 slabs;
   a vector can be supplied. The recovery logic does not depend on the exact weights
   (only on convention being recorded AS slabs with Uniform(slab) true dates), but
   uniform is a modelling choice, not data. **Audit: confirm uniform is acceptable,
   or supply an empirical slab-frequency profile.**

2. **`p_gen` for genuine → empire posterior median** (`GENUINE_PGEN = "empire"`,
   from `empire-aggregate-pgen.npz`, `p_gen_median_raw`, renormalised). Fallback
   `"gauss"` = `gaussian_pgen(200, 60)`. **Audit: confirm the empire posterior is
   the right smooth shape (it is the corpus's recovered genuine activity), or pin
   the Gaussian control.**

3. **Tight-interval width → ±2.5 y** (`GENUINE_HALF_WIDTH = 2.5`, recorded width
   5 y = one 5-year bin). `half = 0` gives the `[t, t]` year-precise case. **Audit:
   confirm one-bin width is the intended "tight".**

4. **DEGENERATE synthetic θ (the most important flag).** Because all 27 library
   slabs pass rule C (round endpoints, width ≥ 49) and all ±2.5 y genuine brackets
   fail it, the generator yields a **perfectly separable** alignment signal:
   **P(aligned|convention) = 1.000, P(aligned|genuine) = 0.000** at every planted α
   (verified). So `row_aligned_frac` ≈ planted α exactly. This is FAITHFUL to SPEC
   §2 as written, but cleaner than production (θ_conv ≈ 0.93, θ_gen ≈ 0.025 —
   `refit_lib.adopted_theta_priors`). It is favourable to the mass arm's recovery
   and gives the alignment binomial near-perfect information. **Audit decision:
   accept the idealised separation (the test is about whether point-date *destroys*
   a signal the mass arm *can* recover — a clean signal makes that contrast
   sharpest), OR add contamination (a fraction of genuine recorded with wide
   brackets, or convention with sub-round endpoints) to match the production θ.**
   This is a parameter-level extension to `generate_inscriptions`, not a §2
   violation. The θ **prior** fed to the model is still the production
   `adopted_theta_priors` (θ_conv ≈ 0.93, θ_gen ≈ 0.025), so the model is NOT told
   the synthetic separation is perfect — a mild prior-data tension the audit should
   note (the binomial likelihood will pull θ_conv up / θ_gen down from the prior).

5. **Mass-preserving jitter scheme (1c).** Each recorded bound shifted by an
   independent uniform integer in {−1, 0, +1} bins (±5 y); re-ordered so `na ≥ nb`;
   minimum width `BIN_SIZE` enforced so `aoristic_spa` (width > 0) keeps every
   inscription. Mass then spread over the perturbed interval (aoristic-mass build,
   largest-remainder). Alignment is on the ORIGINAL recorded interval (held
   constant). **Audit: confirm ±1 bin and the min-width floor are the intended
   "small jitter, keep the mass spread".** Note the mass-preserving counts are
   aoristic-effective (k ≈ 100 k) vs point-collapse raw (k ≈ 121 k) on empire — each
   arm internally consistent; the comparison is recovered α, not raw counts.

6. **Point-date arm `set_data` reuse; mass-preserving rebuild.** The point-date arm
   holds k/n_rows constant (one count per inscription), so the model is built once
   and swapped via `set_data` (the lodged pattern). The mass-preserving arm's
   aoristic-effective k/n_rows vary per realisation (largest-remainder of the
   jittered SPA), so its model is rebuilt each realisation (N_MC = 10, cheap).

## Confirmations

- Nothing was run (no fit/MCMC/diagnostic/SSH). Only `py_compile` and
  data-prep/decision-rule logic checks were executed.
- No lodged/shared module was modified — `h2_lib`, `joint_lib`, `refit_lib`,
  `cell_lib`, and the slab library are imported/read only. `git status` shows
  changes confined to `runs/2026-06-18-c10-validity-test/code/`.
- The concurrent supp-wave dir was read (for the C10 method) but NOT modified; its
  untracked files are excluded by explicit pathspecs at commit.
