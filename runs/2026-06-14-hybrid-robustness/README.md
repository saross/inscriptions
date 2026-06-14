# θ robustness for the cross-classified production model (2026-06-14)

**Directory-name note.** This directory is called `hybrid-robustness` because the planned
robustness check was a global-θ **hybrid** model (`hybrid-robustness-spec.md`, written when
the lead was still the single-multinomial model). The hybrid turned out to be **weakly
identified on the real data** (an α↔θ_gen ridge — see below), so it is **not** the lodged
robustness vehicle. The actual robustness annex is the **θ-prior sensitivity sweep**, which
lives in the same directory. So the folder holds *two* things: the hybrid (a diagnostic that
surfaced a calibration bias) and the sweep (the delivered robustness result). The full
narrative is `HYBRID-PILOT-FINDINGS.md`; the OSF amendment §A5.7 summarises it.

## What's here

### The delivered robustness result — θ-prior sensitivity sweep
- `code/theta_sweep.py` — re-fits the 29 production units under 4 θ priors (original centre
  × re-derived centre × κ ∈ {40, 12}) with the **validated cc-library model** (well
  identified). `code/aggregate_sweep.py` → `outputs/THETA-SWEEP-VERDICT.md` +
  `theta-sweep-summary.json`. **Result: cc α's stable for 27/29 units; only the two
  most-confounded frontier units (Moesia inferior, Britannia) are θ-sensitive, within
  bounds.** This is the lodged robustness annex.

### The cause it traced — θ re-derivation
- `code/rederive_theta.py` → `outputs/theta-rederivation.json`. Re-fitting the calibration
  regression with the **corrected** cc α's gives θ_gen ≈ 0.025 (vs the calibration's 0.155,
  which was inflated by the under-attributing shared-basis α's), fitting 2.5× better. This
  drove the decision to **adopt θ_gen 0.025 as the production prior** (the 2026-06-13 refit
  was re-run; `refit_lib.adopted_theta_priors`).

### The diagnostic that started it — global-θ hybrid (NOT the lodged check)
- `code/hybrid_lib.py` (`build_model_hybrid`, batched-over-units, θ global) + `code/run_pilot.py`
  → `outputs/HYBRID-PILOT-REPORT.md` + `hybrid-pilot.json`. One joint fit over all 29 units
  estimating θ globally. **Weakly identified** (convergence does not improve with more
  compute; invariant to prior width; an α↔θ_gen ridge), so its intervals are not trustworthy
  and the planned hierarchical-recovery validation was **not** pursued. It is retained
  because it independently surfaced θ_gen ≈ 0.024 and corroborated the frontier-unit α's.

## Outputs (committed vs regenerable)
Committed: `HYBRID-PILOT-FINDINGS.md`, `HYBRID-PILOT-REPORT.md`, `hybrid-pilot.json`,
`theta-rederivation.json`, `THETA-SWEEP-VERDICT.md`, `theta-sweep-summary.json`, this README.
Gitignored (regenerable; `.gitignore`): the per-unit sweep fits (`outputs/sweep-*/`), run
logs, and the hybrid posterior.

## Provenance
Reuses the production refit's data prep + fixed library + cc model verbatim
(`runs/2026-06-13-cc-production-refit/code/refit_lib.py`;
`runs/2026-06-09-joint-identifiability/code/joint_lib.py`). Original hybrid spec:
`runs/2026-06-09-joint-identifiability/hybrid-robustness-spec.md` (model block superseded by
`spec.md` here). Folds into OSF Amendment 04 §A5.7.
