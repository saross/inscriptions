# Roma + Italia analyses — results report

**Run:** `runs/2026-06-21-rome-capital-comparison/` · **Date:** 2026-06-21 ·
**Author:** Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief.
**Status:** complete; descriptive / exploratory (NOT preregistered). Rome remains
excluded from all confirmatory regressions (Decision 36); this run adds reference
units and comparisons only — it changes no confirmatory result.

> **α is the CONVENTION fraction** (1 − α = genuine). The model is
> `p_mix = α·p_conv + (1−α)·p_gen`; higher α = more editorial-convention dating.
> All α below are convention fractions. (See the 2026-06-21 correction in
> `reports/key-findings-summary-2026-06-20.md`.)

## 1. What was done

Five new units were fitted with the **production cross-classified "library"
deconvolution, verbatim** (`refit_lib` + `joint_lib`,
`build_model_cross_classified(pconv_mode="library")`, adopted θ prior θ_conv ≈
0.930 / θ_gen ≈ 0.025, κ = 40) — the same model, the same single universal slab
basis, and the same sampler config (2 000 draws × 4 chains, target-accept 0.95)
as the 29 production units. Because the cc-library uses **one universal basis**,
every unit here is directly comparable to the production aggregates by
construction (driver: `code/run_roma_italia.py`; reuses `run_refit.fit_one`).

## 2. Results (convention fraction α)

| unit | N (rows) | α (convention) | 95 % CI | R̂ | div | conv. pass |
|---|---|---|---|---|---|---|
| **Roma** | 65,457 | **0.799** | [0.790, 0.807] | 1.004 | 0 | yes |
| capitals-empire-62 | 16,123 | 0.561 | [0.515, 0.601] | 1.002 | 3 | yes |
| capitals-latin-41 | 15,557 | 0.561 | [0.519, 0.595] | 1.002 | 8 | yes |
| Italia-incl-Rome | 109,172 | 0.733 | [0.722, 0.743] | 1.009 | 0 | yes |
| provinces-non-Italian-Latin | 65,931 | 0.713 | [0.644, 0.762] | 1.003 | 9 | yes |
| *Italia (excl. Rome)* — production | 43,715 | 0.787 | [0.753, 0.806] | — | — | — |
| *empire-aggregate* — production | 180,609 | 0.680 | [0.665, 0.697] | — | — | — |
| *latin-aggregate* — production | 109,646 | 0.739 | [0.660, 0.789] | — | — | — |

Convergence: all five new fits pass the field-standard gate (R̂ < 1.01, bulk ESS
≥ 400). Three units carry **3–9 benign divergences** out of 8 000 draws
(capitals-latin-41, provinces-non-Italian-Latin, capitals-empire-62) — well within
the field-standard benign-tolerant gate the project adopted (cf. the 2026-06-04
divergence-gate decision); R̂/ESS are clean. Reported honestly; not a concern.

## 3. The capital comparison (§§1–7)

- **Rome is the most convention-dated unit in the corpus (α ≈ 0.80).** Four-fifths
  of the imperial capital's *apparent* dating is editorial round-slab convention —
  the highest of any unit, consistent with its raw aligned fraction (0.79–0.82).
- **Provincial capitals are markedly *less* convention-dated (α ≈ 0.56)** — and the
  empire-62 and Latin-41 composites are identical (0.561 / 0.561), so the result is
  frame-robust. Notably, capitals are *less* convention-dated than the general
  provinces (0.71) and the aggregates (0.68 / 0.74): capital epigraphy carries a
  relatively *higher* genuine-dating share than non-capital epigraphy.
- **Figure F16** (`fig16-capital-comparison`): two genuine-SPD panels (empire /
  Latin) + the convention-fraction strip. **Figure F15** (`fig15-rome-before-after`):
  Rome de-fogged. **Figure F17** (`fig17-why-rome-excluded`): the leverage exhibit.
- *Caveat:* Rome's genuine (de-fogged) SPD shape is weakly constrained — at α ≈
  0.80 the genuine component is a small residual, and the fit shows a late-envelope
  spike (~AD 300–340) that is most likely a high-α edge artefact, not a real
  late-antique surge. Read Rome's genuine *shape* descriptively; the robust result
  is the convention *fraction*, not the residual trajectory.

## 4. The Italia thread (§8)

- **Italian epigraphy — capital AND municipia — is the most convention-dated part
  of the empire.** Rome 0.80 and **Italia-excl-Rome (Italian municipal epigraphy)
  0.79** both sit well above the non-Italian provinces (0.71) and even the Latin
  aggregate (0.74). The dense, early, formulaic Italian epigraphic culture is
  distinctively editorial/round-number in its dating. (**Figure F18**,
  `fig18-italia-exceptionalism`.)
- **Temporal / Severan watershed (Figure F19, `fig19-italia-temporal`).** The
  de-fogged genuine chronologies cross over dramatically: **Italian municipal
  epigraphy dominates early — a sharp genuine peak ~AD 80 — then collapses, while
  the non-Italian provinces rise through the 1st–2nd century to peak at the
  Severan watershed (the AD 212 Antonine Constitution is marked).** This is the
  "Italy leads early, the provinces overtake by the Severan period" pattern, made
  visual and historically legible. *(Method note: full-window de-fogged
  trajectories, not per-period fits — within-period slab identifiability fails;
  spec §8. The sharp AD-80 Italian spike may be partly a deconvolution artefact,
  but the broad early-Italy / late-provinces crossover is robust.)*

## 5. Caveats and scope

- Descriptive / exploratory; not preregistered. Rome stays excluded from all
  confirmatory regressions (Decision 36 unchanged); F17 illustrates *why*.
- All comparisons are model-conditional (the cc-library deconvolution) and on the
  one universal basis (so membership, not basis, drives differences).
- The genuine *shapes* of the highest-α units (Rome 0.80, Italia 0.79) are
  weakly constrained; the convention *fractions* are the robust deliverable.

## 6. Reproduce

```bash
# sapphire
PATH=~/.local/bin:$PATH TMPDIR=$HOME/cc-scratch/tmp PYTENSOR_FLAGS=mode=FAST_RUN \
  taskset -c 0-11 uv run python \
  runs/2026-06-21-rome-capital-comparison/code/run_roma_italia.py
# figures (local)
cd runs/2026-06-20-figures/code && python fig15_rome_before_after.py \
  && python fig16_capital_comparison.py && python fig18_italia_exceptionalism.py \
  && python fig19_italia_temporal.py && python fig17_why_rome_excluded.py
```

Outputs: `outputs/units/*.json`, `outputs/posterior-draws/*-pgen.npz`,
`outputs/roma-italia-summary.json`; figures in
`runs/2026-06-20-figures/outputs/fig15…fig19`.
