# Joint identifiability-remediation — local recovery proof-of-concept REPORT

**Date:** 2026-06-09 · **Author:** Claude Code (Opus 4.8, 1M context) on Shawn's brief.
**Run host:** sapphire (`taskset -c 0-11`, `PYTENSOR_FLAGS=FAST_RUN`); amd-tower lacks
`python3-dev` for the PyTensor C backend. **Spec:** `../spec.md`. UK/Aus English.

## Headline

A small, fast proof-of-concept (6 realistic synthetic cells, well-specified
generative model) **pivots the design** and gives a clear, sign-off-ready answer:

1. **The continuity's lead design — shared broad basis + classification term — FAILS**
   for temporally-concentrated (confounded) units. The classification binomial is
   overpowered by a *confidently-wrong* temporal multinomial, and α stays ≈ 0.
2. **The design the POC points to — a FLEXIBLE (per-unit) convention shape +
   classification term — RECOVERS α** across identifiable and confounded cells,
   including with a realistic, observable, contaminated shape estimate.

The lever is the convention **shape AND the count, jointly** — neither alone suffices.
This is a coherent, well-precedented model (a concomitant-variable mixture: a flexible
mixture whose mixing weight is identified by a covariate) and a more defensible position
than either the shared-basis-only or per-unit-basis-only fits.

## Setup

Cells (N = 2,000 per cell; one well-specified replicate each; draws 1,500, tune 1,000,
4 chains, target-accept 0.95). `%win` = fraction of the component's mass in AD 100–300.
θ generation truth (0.95, 0.15); θ priors from `theta-calibration.json` rule C
(θ_conv μ 0.945, θ_gen μ 0.155, κ 40). Generative model (spec §5 Tier 1):
`y ~ Multinomial(N, α·p_conv + (1−α)·p_gen)`, `k ~ Binomial(N, α·θ_conv + (1−α)·θ_gen)`.

- **identifiable** cells: broad convention (`%win` 0.63, like the Latin aggregate) +
  genuine peaked early (`%win` 0.33) — temporally separable.
- **confounded** cells: convention concentrated in AD 100–300 (`%win` 1.00 — the
  *stress corner*; real frontier units sit ~0.88–0.90) + genuine peaked *in the same
  window* (`%win` 0.99) — the frontier-province failure mode.

## Experiment 1 — lead design (shared basis + classification): FAILS confounded

`code/poc_recovery.py` → `poc-recovery.json`. α posterior median [95 % CI]:

| cell | α_true | shared-only | per-unit-only | **shared + classification (LEAD)** |
|---|---|---|---|---|
| ident_a0.3 | 0.3 | 0.08 [0.01,0.21] | 0.37 [0.27,0.45] | **0.16 [0.04,0.29]** |
| ident_a0.6 | 0.6 | 0.09 [0.01,0.22] | 0.63 [0.53,0.71] | **0.28 [0.11,0.44]** |
| conf_a0.2 | 0.2 | 0.00 | 0.38 [0.26,0.47] | **0.00** |
| conf_a0.4 | 0.4 | 0.00 | 0.52 [0.41,0.62] | **0.00** |
| conf_a0.6 | 0.6 | 0.00 | 0.74 [0.65,0.83] | **0.00** |
| conf_regnal_a0.5 | 0.5 | 0.04 | 0.53 [0.44,0.60] | **0.06** |

**Why it fails (the mechanism).** With the shared basis too broad for a concentrated
unit, α > 0 forces convention mass *outside* the data window (the basis has ~36 % of its
mass before AD 100, where the confounded unit has almost none). The temporal multinomial
— 80 bins × 2,000 counts — penalises that mismatch *enormously*, so it is not merely flat
in α (the under-identification picture) but **confidently wrong** (Feller et al. 2016): it
prefers α = 0. A single binomial over 2,000 trials cannot overpower it. This independently
reproduces the informed-α note's conclusion — *"the prior must be paired with a per-unit
or period-aware convention shape to be effective"* — now shown for the joint *likelihood*,
not just the prior.

## Experiment 2 — flexible shape + classification (TRUE shape): RECOVERS

`code/poc_perunit_joint.py` → `poc-perunit-joint.json`. Per-unit basis = the cell's true
convention shape (idealised). The classification term reins in the per-unit basis's
over-attribution:

| cell | α_true | per-unit-only (over) | **per-unit + classification** | bias |
|---|---|---|---|---|
| ident_a0.3 | 0.3 | 0.37 (+0.07) | **0.32 [0.25,0.38]** | +0.02 |
| ident_a0.6 | 0.6 | 0.63 (+0.03) | **0.61 [0.55,0.68]** | +0.01 |
| conf_a0.2 | 0.2 | 0.38 (+0.18) | **0.26 [0.19,0.33]** | +0.06 |
| conf_a0.4 | 0.4 | 0.52 (+0.12) | **0.45 [0.38,0.52]** | +0.05 |
| conf_a0.6 | 0.6 | 0.74 (+0.14) | **0.67 [0.60,0.76]** | +0.07 |
| conf_regnal_a0.5 | 0.5 | 0.53 (+0.03) | **0.51 [0.45,0.57]** | +0.01 |

**6/6 PASS** (|bias| < 0.18); **6/6 cover α_true at 95 %**. The flexible shape lets the
temporal term *accept* the true α (it is now genuinely under-identified, not confidently
wrong), and the classification term selects the right point — exactly the
concomitant-variable identifiability restoration (Huang & Bandeen-Roche 2004).

## Experiment 3 — flexible shape + classification (ESTIMATED, observable shape): RECOVERS

`code/poc_estimated_basis.py` → `poc-estimated-basis.json`. The true convention shape is
not observable; the production analogue is the aoristic SPA of the **grid-aligned
inscription subset**, which is contaminated (in expectation `∝ α·θ_conv·p_conv +
(1−α)·θ_gen·p_gen`). Re-fitting with that realistic estimate:

| cell | α_true | **per-unit(est) + classification** | bias | cover95 |
|---|---|---|---|---|
| ident_a0.3 | 0.3 | 0.35 [0.27,0.43] | +0.05 | ✓ |
| ident_a0.6 | 0.6 | 0.65 [0.57,0.73] | +0.05 | ✓ |
| conf_a0.2 | 0.2 | 0.27 [0.19,0.35] | +0.07 | ✓ |
| conf_a0.4 | 0.4 | 0.49 [0.41,0.59] | +0.09 | ✗ (CI [0.41,0.59]) |
| conf_a0.6 | 0.6 | 0.72 [0.62,0.83] | +0.12 | ✗ (CI [0.62,0.83]) |
| conf_regnal_a0.5 | 0.5 | 0.55 [0.49,0.63] | +0.05 | ✓ |

**6/6 PASS** the |bias| < 0.18 gate; coverage clean for 4/6, **marginal for the two
high-α confounded cells** (a +0.10–0.12 residual positive bias from the contaminated
estimate pushes the tight CI just off truth). Still a decisive improvement on
shared-basis under-attribution (−0.20 to −0.60) and per-unit-only over-attribution
(+0.12 to +0.18).

## Conclusions

- **Adopt:** the joint model with a **flexible per-unit convention basis (estimated from
  the unit's grid-aligned-subset SPA) + the grid-alignment classification binomial.**
- **Reject:** the shared-basis + classification design (the continuity's lead) — it
  cannot overcome the convention-shape mismatch for concentrated units.
- The classification term is **necessary but not sufficient**: it identifies the *weight*
  but only once the convention *shape* is free enough for the temporal term to be
  genuinely under-identified rather than confidently wrong.
- **Open quantities for the full grid:** (i) the small positive residual bias under the
  estimated shape (+0.05 to +0.12) — characterise and consider a θ_gen-aware correction;
  (ii) coverage at high α — the marginal cases need replicate-level coverage rates;
  (iii) θ-transferability and κ-sensitivity (spec §7).

## Caveats (honest framing)

- One replicate per cell; convergence not yet audited per cell (point estimates only).
  The full grid supplies replicate-level bias/coverage and the convergence gate.
- Confounded convention `%win` = 1.00 is the **stress corner**; realistic units (~0.88)
  are easier. The full grid sweeps `%win ∈ {0.85, 0.95, 1.0}`.
- Experiments 1–2 use the *true* convention shape for the per-unit basis; only
  Experiment 3 uses the observable estimate. The interval-level synthetic (Tier 2)
  remains the cleanest test of the estimate and is deferred to the full grid.
- **This is a design change relative to Amendment 03** (which adopted the shared basis
  specifically to avoid per-unit over-attribution). The POC shows the classification term
  supplies the missing over-attribution control — so a per-unit basis becomes safe — but
  this reverses a lodged design decision and needs Shawn's sign-off + an OSF amendment.

## Postscript — θ-prior κ sweep (2026-06-09): widening the prior is COUNTERPRODUCTIVE

`code/poc_kappa_check.py` → `poc-kappa-check.json`. We tested widening the θ prior
(κ 40 → 20 → 12) on the estimated basis, expecting it to widen the α CI and fix the
marginal high-α coverage. **It does the opposite** — it amplifies the positive bias:

| cell | α_true | κ=40 | κ=20 | κ=12 |
|---|---|---|---|---|
| conf_a0.2 | 0.2 | 0.27 [0.19,0.34] ✓ | 0.33 ✗ | 0.50 ✗ |
| conf_a0.4 | 0.4 | 0.49 [0.41,0.59] (+0.09) | 0.54 | 0.59 |
| conf_a0.6 | 0.6 | 0.72 [0.62,0.83] (+0.12) | 0.76 | 0.78 |
| ident_a0.6 | 0.6 | 0.65 ✓ | 0.66 ✓ | 0.67 ✓ |

**Diagnosis.** The marginal coverage is a small *positive bias*, not CI under-dispersion.
Its source is the **estimated-basis contamination**: the grid-aligned-subset SPA ≈
`α·θ_conv·p_conv + (1−α)·θ_gen·p_gen`, so the convention basis carries a faint copy of the
genuine peak, letting the convention component over-reach. A *tighter* θ prior anchors α
to the classification signal and limits the over-attribution; a *looser* prior lets it
float up. **Keep κ = 40** (do not widen). The +0.09/+0.12 residual is a *characterised
limitation* at the stress corner (`%win` 1.00; real units ~0.88 are milder), within the
|bias| < 0.18 gate, to be mapped on the full grid.

**Principled fix (candidate for the full grid / refined lead):** a fully cross-classified
**time × alignment** model — observe the aligned-subset and non-aligned-subset temporal
SPAs separately, both as multinomials sharing (α, p_conv, p_gen, θ), so the model
*separates* the contamination instead of inheriting it via a fixed basis. Likely removes
the residual bias; needs its own validation. Logged for the full-grid decision.
