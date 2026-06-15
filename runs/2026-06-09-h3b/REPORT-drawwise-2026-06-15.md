# H3b deviation-detection — draw-wise DRAFT results (2026-06-15)

> **DRAFT — exploratory.** H3b carries no Holm-corrected confirmatory family (prereg; Decision 15); all readings are descriptive. Supersedes the 2026-06-09 median-based draft `REPORT.md` and is the deliverable of `h3b-implementation-spec-2026-06-14.md` under OSF Amendment 04 §A5.6 (reliability by uncertainty propagation).

**Construction (Shawn-confirmed 2026-06-15):** the genuine-SPA **posterior** (8,000 cc-library draws/unit) is propagated draw-wise through a featureless-null envelope built once per unit. The informative null is **CPL-3 fit to the observed corrected curve** (D1; standard SPD self-referential null); the **exponential** null is retained as a **labelled saturated cross-check** (D3). The global Timpson test is reported as a saturated gate and the **probe-window P(deficit)** is the deliverable (D2); the large-N correction + baorista null are a **deferred robustness annex** (D2, see end).

## 1. The global test is saturated (a methodological finding)

Under **both** nulls the global marginal-*p* < 0.05 for **29/29** (CPL) and **29/29** (exp) units. This is the documented large-N over-power of the basic SPD/Timpson test: at n_eff = 1,577–151,361 the pointwise envelope is Poisson-tight, and the real Roman epigraphic curve is jagged and humped — far richer than a monotone exponential or a 3-knot CPL — so essentially the whole curve reads as 'deviation'. The exponential null is degenerate (empire: 77/80 bins out-of-envelope); see `figures/fig-exp-saturation-empire.png`. The global *p* is therefore an uninformative gate here; the probe windows carry the signal. (The jaggedness of the corrected curve — e.g. a sharp feature near AD 77 — is itself a candidate for the deferred annex: real round-year structure vs deconvolution residual.)

## 2. Probe-window deficit posteriors — the deliverable (CPL null, λ=1.0)

Two complementary readings per window: **net dep.** = posterior-median signed windowed relative departure from the smooth trend (negative = net deficit; the magnitude), and **P(def)** = posterior probability that ≥ 1 window bin lies below the envelope (the probabilistic flag; one-sided). They can diverge — a window can be net-surplus yet carry a probable single-bin dip. By net departure, **20/29** units show a net Antonine deficit and **14/29** a net Crisis deficit; by P(def) ≥ 0.5, **17/29** (Antonine) and **18/29** (Crisis). `λ1.2` = §A5.5 coverage-inflation sensitivity on P(def).

Flags: `*` θ-sensitive soft-annotated (Amendment 04 §A5.6); `‡` below the cpl-3 reachability floor (n_eff < 1,618); `◆` prereg-named probe scope.

| unit | n_eff | Ant net dep. | Ant P(def) | Ant λ1.2 | Cri net dep. | Cri P(def) | Cri λ1.2 | flags |
|---|---|---|---|---|---|---|---|---|
| empire-aggregate | 151,361 | -23% | 1.00 | 1.00 | -27% | 1.00 | 1.00 | ◆ |
| latin-aggregate | 101,066 | -43% | 1.00 | 1.00 | -13% | 1.00 | 1.00 | ◆ |
| Latium et Campania / Regio I | 17,037 | -46% | 0.90 | 0.88 | -72% | 1.00 | 1.00 |  |
| Dalmatia | 6,325 | +6% | 0.41 | 0.45 | +18% | 0.84 | 0.84 |  |
| Hispania citerior | 6,011 | -57% | 0.99 | 0.98 | +55% | 0.32 | 0.45 |  |
| Germania superior | 5,570 | +2% | 0.59 | 0.59 | -25% | 0.99 | 0.98 |  |
| Venetia et Histria / Regio X | 5,560 | +3% | 0.17 | 0.26 | -26% | 0.92 | 0.92 |  |
| Dacia | 4,718 | -29% | 1.00 | 1.00 | +26% | 1.00 | 1.00 |  |
| Britannia | 4,407 | -32% | 1.00 | 1.00 | +39% | 0.03 | 0.08 | * |
| Pannonia superior | 4,174 | -27% | 0.97 | 0.95 | -9% | 0.77 | 0.83 |  |
| Samnium / Regio IV | 3,952 | -34% | 0.66 | 0.66 | +1% | 0.43 | 0.52 |  |
| Africa proconsularis | 2,967 | +19% | 0.13 | 0.21 | +20% | 1.00 | 1.00 |  |
| Germania inferior | 3,261 | -38% | 0.92 | 0.90 | -54% | 0.99 | 0.99 |  |
| Apulia et Calabria / Regio II | 3,012 | -20% | 0.54 | 0.56 | -54% | 0.96 | 0.96 |  |
| Pannonia inferior | 2,812 | -6% | 0.49 | 0.55 | +15% | 0.47 | 0.59 |  |
| Numidia | 2,727 | +34% | 0.98 | 0.97 | +5% | 0.99 | 0.98 |  |
| Etruria / Regio VII | 2,426 | -29% | 0.48 | 0.56 | +16% | 0.50 | 0.63 |  |
| Umbria / Regio VI | 2,573 | -9% | 0.26 | 0.34 | +9% | 0.41 | 0.52 |  |
| Noricum | 2,600 | +1% | 0.21 | 0.30 | +18% | 0.32 | 0.41 |  |
| Baetica | 2,449 | -13% | 0.95 | 0.92 | +30% | 0.06 | 0.15 |  |
| Transpadana / Regio XI | 2,201 | -25% | 0.49 | 0.52 | +25% | 0.29 | 0.40 |  |
| Pompeii | 4,247 | n/a | 0.00 | 0.00 | n/a | 0.00 | 0.00 |  |
| Salona | 2,890 | -15% | 0.61 | 0.64 | +32% | 0.61 | 0.68 |  |
| Ostia | 2,316 | -28% | 0.91 | 0.89 | -38% | 0.84 | 0.84 |  |
| Mogontiacum | 2,325 | +25% | 0.02 | 0.06 | -47% | 0.00 | 0.00 |  |
| Aquileia | 1,885 | +1% | 0.22 | 0.28 | -0% | 0.39 | 0.51 |  |
| Moesia inferior | 1,728 | -31% | 0.88 | 0.86 | -13% | 0.99 | 0.98 | * |
| Lusitania | 1,577 | -4% | 0.34 | 0.41 | -41% | 0.85 | 0.87 | ‡ |
| Italia (excl. Rome) | 40,499 | -70% | 0.99 | 0.98 | -42% | 1.00 | 1.00 |  |

## 3. Prereg-named scopes

- **empire-aggregate** — Antonine net dep. **-23%**, P(deficit) **1.000**; Crisis net dep. **-27%**, P(deficit) **1.000**.
- **latin-aggregate** — Antonine net dep. **-43%**, P(deficit) **1.000**; Crisis net dep. **-13%**, P(deficit) **1.000**.

empire is the named Antonine scope; latin-aggregate is the operational Western-Empire-provincial Crisis scope (Decision 36). Both show high-probability deficits at their named windows, consistent with the Antonine-plague and Third-Century-Crisis decline narratives. All other per-unit rows are **exploratory-extra** (broader than the prereg's named scope; scope confirmed 2026-06-14).

## 4. Coverage sensitivity (λ=1.2)

The §A5.5 inflation sensitivity (widen each draw about its posterior mean by 1.2, counteracting the cc posterior's ~1σ optimism) moves only borderline units and leaves saturated/near-zero ones flat — see the `λ1.2` columns above. It is a sensitivity, not the headline; the primary reading is λ=1.0.

## 5. Raw-vs-corrected follow-up

Per launch-spec §8, the raw (uncorrected) SPA was tested against the same null. Both raw and corrected global tests saturate at these N, so the comparison is uninformative at the global level here; the per-unit raw global *p* is in `outputs/drawwise/raw-vs-corrected.json`.

## 6. Caveats

- **Global saturation** (above): the deliverable is the probe-window P(deficit), not the global *p*.
- **Coverage** (§A5.5): cc CIs are ~1σ-optimistic; propagated deviations carry the caveat, with λ=1.2 as the sensitivity.
- **Soft-annotated units** (Moesia inferior, Britannia): θ-sensitive; flagged not excluded; read with extra caution.
- **Reachability** (`‡`): units below the cpl-3 province floor (n_eff < 1,618; Lusitania 1,577) carry a power caveat.
- **Jaggedness of the corrected curve** drives the saturation and may inflate probe P(deviation); whether it is real structure or deconvolution residual is a question for the annex.

## 7. Deferred robustness annex (D2 — to run after this base)

- **Large-N correction** — a reduced-significance / mark-permutation variant or effective-N thinning so the global test is not over-powered.
- **baorista Bayesian-aoristic null** (prereg line 378) — a better-specified flexible null that may also sharpen the probe readings.
Both are independent post-hoc sensitivities; neither changes the base deliverable. Logged in `planning/backlog` / the decision note.

## 8. Reproduce
```bash
uv run python runs/2026-06-09-h3b/code/run_h3b_drawwise.py   # Stage B
uv run python runs/2026-06-09-h3b/code/make_h3b_report.py    # this report
uv run python runs/2026-06-09-h3b/code/plot_h3b_drawwise.py  # figures
```

Figures: `outputs/drawwise/figures/{fig-cpl-smallmultiples,fig-named-scopes,fig-exp-saturation-empire}.png`. Per-test detail: `outputs/drawwise/deviations-table.csv`.
