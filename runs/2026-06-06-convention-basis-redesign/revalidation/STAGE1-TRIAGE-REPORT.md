# Stage-1 stress-triage — recovery re-validation (Decision 38 empirical basis)

**Date:** 2026-06-06 · **Author:** Claude Code (Opus 4.8) on Shawn Ross's brief
**Status:** triage complete; **substantive verdict PASS**, pending Shawn's decision on the full grid and on reconciling the spec gate with Amendment 01.
**Run:** sapphire, PID 1652634; 8 cells × 100 replicates = 800 fits; production sampler (2000 draws, 1000 tune, 4 chains, target_accept 0.95); wall 2,310 s (~38 min); 0 failed; base seed 20260606.
**Basis:** `runs/2026-06-06-convention-basis-redesign/design.json` `tier_basis_empirical` (empire, Option 2).

## Results (the α=0.95 × multi-century-heavy × peaked-genuine stress corner)

| shape | N | α-coverage | convergence | shape r(p_gen) | role |
|---|---|---|---|---|---|
| bimodal | 2,000 | 1.00 | 1.00 | 0.283 | peaked (gate) |
| bimodal | 10,000 | 0.99 | 1.00 | 0.561 | peaked (gate) |
| regnal_cluster | 2,000 | 1.00 | 1.00 | 0.336 | peaked (gate) |
| regnal_cluster | 10,000 | 0.97 | 1.00 | 0.816 | peaked (gate) |
| rise_and_fall | 2,000 | 1.00 | 1.00 | 0.566 | peaked (gate) |
| **rise_and_fall** | **10,000** | **0.81** | 1.00 | 0.838 | peaked (gate) |
| flat_baseline | 2,000 | 0.99 | 1.00 | n/a (flat) | contrast |
| flat_baseline | 10,000 | 0.99 | 1.00 | n/a (flat) | contrast |

## Interpretation

**The Decision-38 §6 concern is resolved.** The fear was that the new multi-century
tier — a long flat body with an AD 300–350 envelope-edge plateau — would be
confused for genuine quiescence, i.e. the model would *under*-attribute to
convention (α under-estimate, plateau absorbed into `p_gen`). The opposite, and
negligible, is observed: at the hardest corner (`rise_and_fall`, N=10,000) the
model recovers **α = 0.979 (sd 0.012) against a true 0.95 — a +0.029 over-estimate**
(90th-pct |bias| 0.042). The plateau is correctly attributed to convention;
shape recovery there is the best of the set (r = 0.838). Convergence is 1.00 in
every cell.

**The single sub-threshold cell is the benign large-N α-coverage collapse.**
`rise_and_fall` N=10,000 has α-coverage 0.81 not because recovery fails but because
at N=10,000 the per-replicate CI tightens (sd 0.012) faster than the tiny +0.029
bias shrinks, so the interval misses 0.95 ~19 % of the time. The same shape at
N=2,000 (looser CI) covers 1.00. **This is exactly the phenomenon Amendment 01
§A5.5.1 documented and acted on** — exact CI coverage of the mixing weight "is not
field-standard and collapses at large N under negligible bias" — which is why
Amendment 01 **demoted α-coverage from a binding gate to a shape-conditioned
diagnostic** (reported as Bland–Altman limits of agreement).

**Spec-gate inconsistency (a correction to this re-validation's own spec).** The
`spec.md` §2.1 triage gate ("per-cell α-coverage ≥ 0.90, binding") is stricter than,
and inconsistent with, the lodged Amendment 01 framework. Under the Amendment 01
criterion — α-coverage = diagnostic; shape (Pearson r / Wasserstein-1) = binding;
operating envelope α ≤ 0.70 — the triage passes: every cell converges, α is
recovered to within 0.03 at the worst corner, and the plateau-confusion failure
mode is absent.

**Shape recovery at α=0.95 is N-limited, and beyond the operating envelope.** At
α=0.95 only 5 % of the mass is genuine, so recovering the genuine *shape* is hard
at small N (r 0.28 at N=2,000 → 0.84 at N=10,000). But **α=0.95 is outside the
production operating envelope** (Decision 37 D5 gates production fits at posterior
α ≤ 0.70). The full grid will characterise the α ≤ 0.70 envelope, where the genuine
component is ≥ 30 % of the mass and shape recovery is production-relevant.

## Recommendation

**Proceed to the full 450-cell grid, scored under the Amendment-01 criterion**
(α-coverage → diagnostic; shape binding; large-N α-coverage collapse reported as
benign). Correct `spec.md` §2.1 accordingly. Pending Shawn's sign-off (the full
grid is ~1–1.5 days of compute and this reverses the literal "FAIL → halt" gate).

## Artefacts

- Summaries: `inscription-mass/outputs/cell-summaries/` (8 cells); `grid-state.json`.
- Full per-replicate posteriors remain on sapphire (as with the validated grid).
