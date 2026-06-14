# Hybrid robustness — pilot findings + recommendation

**Date:** 2026-06-14. **Author:** Claude Code (Opus 4.8). **Status:** pilot complete →
gate = **REVIEW** (not a clean PASS); the next step is a methodological fork for Shawn.
The single-fit posteriors are gitignored; the representative auto-report
(`outputs/HYBRID-PILOT-REPORT.md`, κ=8) and `hybrid-pilot.json` are committed. UK/Aus English.

## What was run

The global-θ cross-classified hybrid (`spec.md`; θ_conv, θ_gen single global scalars,
wider prior, estimated jointly; α per-unit, not pooled; fixed library) fit **once over
the 29 production units**, in **three configurations** to separate sampling from
structure:

| run | draws/tune | target_accept | θ-prior κ | α+θ max R̂ | α+θ min ESS | θ_gen median | cc-in-CI |
|---|---|---|---|---|---|---|---|
| 1 | 1500/1500 | 0.95 | 4 | 1.0185 | 188 | 0.024 | 10/29 |
| 2 | 2000/3000 | 0.97 | 4 | 1.0479 | 69 | 0.023 | 9/29 |
| 3 | 2000/3000 | 0.97 | 8 | 1.0470 | 73 | 0.024 | 9/29 |

0 divergences in every run.

## The three findings (stable across all configurations)

1. **The hybrid is weakly identified / poorly mixing on the real data — structurally,
   not for want of sampling.** Convergence did **not** improve when tuning was doubled
   and target_accept raised (it nudged *worse*: ESS 188 → ~70), and a tighter prior
   (κ 4 → 8) changed nothing. With 0 divergences throughout, this is a **ridge / mild
   between-chain multimodality**, almost certainly the α ↔ θ_gen trade-off (a single
   global θ_gen traded against 29 per-unit α's). More compute will not fix it.

2. **θ_gen robustly wants ≈ 0.02–0.024, far below the calibrated 0.155** — invariant to
   prior width, with a tight posterior CI (~[0.016, 0.030]). The joint cross-classified
   likelihood implies genuine inscriptions are grid-aligned only ~2–3 % of the time, not
   15.5 %. **Likely cause:** the plug-in calibration (`calibrate_theta.py`) fit θ_gen as
   the intercept of `aligned_frac ≈ θ_gen + (θ_conv−θ_gen)·α` over the identifiable units
   **using the under-attributing shared-basis α_shared** — biased-low α's inflate the
   intercept. Re-estimated jointly with free α's, θ_gen falls. (Interpret cautiously: the
   value comes from a poorly-mixed fit, so treat it as a *direction*, not a point.)

3. **The frontier units — the remediation's whole point — are CONCORDANT, and there is
   no systematic shift.** Mean discrepancy (hybrid − cc) is ≈ 0 (−0.002) in every run.
   The diagnostic-flagged frontier units (Britannia, Dacia, Moesia inferior, Numidia,
   Pannonia superior, …) have the cc-library α **inside** the hybrid CI. The discordant
   units are the **broad identifiable** ones (Etruria −0.13, Latium −0.11, Italia −0.10,
   latin-aggregate −0.08), shifted by the lower θ_gen — but with no net direction, and
   within the recovery grid's documented accuracy. The low overall "31 % inside" figure
   is the product of **tight hybrid CIs** (width ~0.04) against small per-unit gaps, not
   a contradiction of the cc result.

**Net:** the cc-library production result is **corroborated where it matters** (frontier
units pinned, no systematic bias), and the pilot surfaced a genuine **θ_gen-calibration
sensitivity** that is worth running down. The fully-global-θ hybrid as specified is **not
a sound vehicle for the lodged robustness number** — it is weakly identified on this data.

## Recommendation (the fork — Shawn's call)

Do **not** advance to the expensive ~24-unit × 10-replicate hierarchical-recovery
validation on the current hybrid: a poorly-mixing model cannot return trustworthy
coverage, so the validation would inherit the pathology. Instead, my recommendation is
**(B) then (C)**, with (A)/(D) as alternatives:

- **(B) Re-derive the θ calibration from the corrected cc-library α's** (cheap; ~minutes).
  Tests finding 2 directly: does θ_gen really sit near 0.02 once the α's are unbiased? And
  re-fit a few units under the re-centred θ to see whether the cc-library α's move at all
  (if the alignment *contrast* dominates, they won't — which would be a strong robustness
  result in itself).
- **(C) Replace the fully-global-θ hybrid with a θ-prior-sensitivity sweep on the
  validated cc-library model** as the robustness check: vary the cc model's θ prior centre
  and κ, re-fit the 29 units (one well-identified fit each, minutes), and report whether the
  per-unit α's are stable. This **directly answers the robustness question** ("are the cc α's
  sensitive to the θ assumption?") with a *better-identified* model than the joint hybrid,
  and sidesteps the ridge entirely. This becomes the preregistered robustness annex.
- **(A) Reparameterise the hybrid for identifiability** (fix θ_conv, which is
  well-identified ~0.933, and free only θ_gen; or a sum-to-zero α scheme) and then
  validate. Real modelling work, uncertain payoff — lower priority than (B)/(C).
- **(D) Accept the frontier-unit corroboration as the robustness result** and document the
  global-θ hybrid's weak identification as an honest limitation. Defensible, minimal.

The amendment (§A5.7) currently flags the hybrid concordance as "pending"; whichever path
is chosen, its result folds in there before lodgement.

## Addendum (2026-06-14) — (B) + (C) done (Shawn-approved)

**(B) θ re-derivation** (`rederive_theta.py`, `outputs/theta-rederivation.json`).
Re-running `calibrate_theta`'s constrained least-squares with the **corrected cc-library
α's** (in place of the under-attributing α_shared) gives **θ_gen ≈ 0.025** (vs the
calibrated 0.155) and fits the aligned-fraction data **2.5× better** (RMSE 0.045 vs
0.117). The reproduction control (α_shared → θ_gen 0.160) confirms the method. So three
independent routes — the hybrid joint fit (0.024), the re-derivation (0.025), and the
wide-κ sweep below — agree θ_gen ≈ 0.02–0.025; the production calibration's 0.155 was
inflated by the circular use of the biased shared-basis α's. (The production refit's
per-unit θ_gen posterior ran at median 0.101 — the data pulled it down, but the tight
κ=40 prior held it above the data-preferred value.)

**(C) θ-prior-sensitivity sweep** (`theta_sweep.py` / `aggregate_sweep.py`,
`outputs/THETA-SWEEP-VERDICT.md`; 4 θ-priors × 29 units = 116 well-identified cc-library
fits, sapphire 18.8 min, 28/29 converge; baseline reproduces the production refit bit-
identically, max |Δα| 0.003). **This is the robustness annex, replacing the poorly-mixing
global-θ hybrid.** Result:

- **27/29 units stable** (α-range < 0.10 across baseline / re-derived / wide-κ /
  re-derived-wide); mean range 0.038; broad units + aggregates rock-stable (range ≤ 0.03).
- **Frontier units 8/10 stable.** The two sensitive ones are the **most
  temporally-confounded** units — Moesia inferior (range 0.159) and Britannia (0.140) —
  where the θ assumption matters most; their α moves **upward** under the corrected lower
  θ_gen and stays **within the H2.1 two-bound range**, so the remediation conclusion is
  unchanged.
- The operative θ_gen 0.155 → 0.025 shift is uniformly small and positive (mean +0.025,
  max +0.072). The alignment **contrast** — not the θ centre — pins the well-identified α's.

**Open decision (Shawn).** Three methods agree θ_gen ≈ 0.025 and it fits markedly better,
so there is a principled case to **adopt the re-derived θ_gen as the production prior and
re-run the 29-unit refit** (~6 min; the α's move little, but it removes a demonstrated
calibration bias rather than disclosing it). Alternatively, keep θ_gen 0.155 as production
and report this sweep as the robustness result. Either way the result folds into amendment
§A5.7 (and, if re-run, §A5.4's per-unit α's update — Moesia/Britannia rise ~0.05–0.07).
