# cc-library production refit — spec

**Status:** design decisions settled empirically (this doc); implement → audit → run.
**Date:** 2026-06-13. **Author:** Claude Code (Opus 4.8), on Shawn's adoption sign-off
(2026-06-13) of the cross-classified `library` model (`runs/2026-06-09-joint-identifiability/
cross-classified-signoff.md` §6c). UK/Aus English.

## 0. What this does

Re-fit the H2.1 production units under the **recovery-validated cross-classified `library`
model** (`joint_lib.build_model_cross_classified`, `pconv_mode="library"`), replacing the
shared-3-tier temporal-only fit (`build_model_f1_f3`) that under-attributed convention for
temporally-concentrated frontier units (the diagnostic, `runs/2026-06-07-h2.1-launch-prep/
outputs/production/DIAGNOSTIC-alpha-identifiability-REPORT.md`). Output: per-unit α with CI +
convergence + the corrected genuine SPA, reconciled against the H2.1 two-bound diagnostic.

Units: the **28** from `h2_lib.enumerate_units()` (empire-aggregate, latin-aggregate, 19
Latin provinces, 5 cities, 2 grey-band provinces). *Note:* the continuity's "28 + Italia =
29" does not match the canonical `enumerate_units()` (28); the code is the authority — refit
covers those 28, and the fitted set is cross-checked against `summary-final.json` at aggregation.

## 1. Design decision 1 — k / n_rows on real data (SETTLED)

The cc factorisation requires `k = y_aligned.sum()` and `n_rows = y_aligned.sum() +
y_nonaligned.sum()` (the exact lumping/thinning identity — the property that makes the model
the *exact* concomitant-variable likelihood). On real data the natural alternative would be
*row* counts (k = # aligned inscriptions, n_rows = # inscriptions), which is what θ was
calibrated on (`calibrate_theta.py`, row aligned-fractions). These differ because (a) aoristic
spreading and (b) envelope clipping hit wide aligned intervals hardest.

**Decision: aoristic-effective counts** — `y_aligned`/`y_nonaligned` = largest-remainder of
each subset's aoristic SPA; `k = y_aligned.sum()`; `n_rows = y_aligned.sum() +
y_nonaligned.sum()`. This preserves the exact factorisation (and so the validated model
structure) rather than inventing an un-validated decoupled-N variant.

**Why it is safe (measured, `outputs/unit-measurements.json`):** the aoristic-mass aligned
fraction differs from the row aligned fraction by **mean 0.021, max 0.058** (Ostia) across the
28 units — so θ (calibrated on row fractions) transfers to the mass-fraction binomial with
≤0.06 error, far inside the model's tolerance. The reinterpretation of θ from "P(aligned row |
type)" to "P(aligned mass | type)" is immaterial at this magnitude.

## 2. Design decision 2 — the convention basis (SETTLED): a FIXED corpus-wide slab library

Signoff §2 sketched a *per-unit* slab catalogue. The empirical measurement changed the call
to its cleaner limit (signoff §2's "optionally plus corpus-wide common slabs", taken all the
way): **a single FIXED, a-priori, round-endpoint slab library, identical for every unit**
(`outputs/production-slab-library.json`, built + validated by `library_design.py`).

**Why fixed-corpus-wide beats per-unit (three reasons, the first two evidence-driven):**

1. **It is the direct production analogue of what the grid validated.** The recovery grid
   validated a *fixed* deterministic-box library (`grid_lib.slab_library_basis`, 19 rows), not
   a per-unit catalogue. A fixed corpus-wide library is that exact design, sized to the real
   corpus. (The grid's *specific* 19 rows cover only 62 % of real aligned mass — built for the
   synthetic AD 100–300 recipes — so the rows are re-derived, but the *design* is identical.)
2. **No per-unit contamination channel.** A per-unit catalogue's membership is data-derived
   *from the unit being fit*, so a genuine-but-aligned inscription (≈15 % of genuine, per
   θ_gen) injects a near-genuine-shaped candidate row into that unit's basis (signoff §2's
   acknowledged "contamination by membership"). A fixed library is identical for every unit and
   independent of the unit's data — it cannot tailor to any unit's genuine signal. Strictly
   cleaner.
3. **It avoids the per-unit truncation/collinearity tuning** (real units have 33–362 distinct
   aligned interval types — far too many to use per-unit; a fixed library sidesteps the
   top-K-per-unit choice entirely).

**Construction (`library_design.py`):** all a-priori round-endpoint slabs `(lo, hi)` with
`lo ∈ {−50,1,51,101,151,201,251,301}`, `hi ∈ {50,100,150,200,250,300,350}`, `lo<hi`,
envelope-clipped width ≥ 49 (sub-50 intervals are genuine-like and excluded so p_conv cannot
cheaply mimic a genuine spike), deduped after clipping (35 candidates), pruned to the rows
that carry ≥0.02 normalised NNLS weight in ≥1 unit → **27 rows** (locked in
`production-slab-library.json`). Each row is the deterministic aoristic box of one slab; no
data enters a row's shape (no mass-contamination channel).

**Validation (measured):**
- **Spanning:** NNLS reconstruction of every unit's aligned-subset SPA onto the library has L1
  residual **mean 0.056, ≤0.083 for all real-convention units** (cosine ≥0.993). The sole
  outlier is **Pompeii** (L1 0.632) — expected and *correct*: Pompeii is genuine-precision-
  dated (α≈0.001, the diagnostic's validation case), its 227 aligned rows are *narrow* non-
  convention intervals a wide-slab library rightly cannot represent, and its convention
  component is negligible so p_conv is barely weighted.
- **Collinearity is not a convergence risk.** The library's Gram condition number is
  **3.0×10¹⁷ — *lower* than the grid's validated 19-row library (6.9×10¹⁷)**, which converged
  at 96 %. α is identified by the two-subset alignment *contrast*, not by `tier_weights`
  uniqueness; the Dirichlet prior keeps the posterior proper; the grid proved the convergence
  gate passes at this collinearity level. The convergence gate will still flag any unit where
  `tier_weights` fails to mix, and those are reported caveated.

This keeps the **adopted `library` arm's character** (overlapping wide-bracket slabs — the
constraint that beat the `free` arm on confounded bias, +0.010 vs −0.031), rather than
degenerating to disjoint tiles (≈ the `free` arm).

## 3. The fit (per unit)

```
y_aligned, y_nonaligned, k, n_rows  ← split the unit's corpus by aligned_indicator(rule C),
                                       aoristic-SPA + largest-remainder each subset (§1)
model = build_model_cross_classified(y_aligned, y_nonaligned, k, n_rows,
            tier_basis=FIXED_LIBRARY, theta_conv_ab, theta_gen_ab, pconv_mode="library")
```

- θ priors: rule C, κ=40 → `beta_from_mean_concentration(0.945, 40)` / `(0.155, 40)` (identical
  to the grid; `theta-calibration.json`).
- Sampler: DRAWS 2000, TUNE 1000, CHAINS 4, target_accept 0.95, cores=1 (the validated config,
  `grid_lib`/`h2_lib` agree). Per-unit seed = `BASE_SEED + unit_index`.
- Convergence gate: `convergence_pass(max_rhat, min_ess_bulk)` over {alpha, tier_weights,
  sigma_smooth, z_pgen, theta_conv, theta_gen} — the grid's monitored set for the library arm.
- Extract: α median + 95 % CI; corrected genuine SPA (p_gen posterior-median, renormalised —
  the H3b hand-off); p_conv median; tier_weights median; PPC adequacy (per-subset MAE frac);
  convergence diagnostics.

29 fits total at ~30–130 s each ⇒ **well under an hour** on sapphire (this is NOT grid-scale).
Run on sapphire (the box has the PyTensor C backend; the local box lacks python3-dev).

## 4. Acceptance + reconciliation (the verdict)

1. **Convergence:** per-unit `convergence_pass`; report any failures caveated (do not drop).
2. **Frontier-unit recovery — the point of the exercise.** For the ~10 diagnostic-flagged
   under-attributed units (Moesia inferior, Britannia, Pannonia inferior, Samnium, Salona,
   Ostia, Venetia et Histria, Numidia, Dacia, Umbria), the cc-library α should sit **between**
   the H2.1 two bounds [α_shared (wrong-low), α_perunit (wrong-high)] and near the
   classification-implied α (`theta-calibration.json` `implied_alpha[C]`) — i.e. the contrast
   pins the value the shared-basis fit could not. Tabulate cc-α vs [α_shared, α_perunit,
   implied_α].
3. **Controls unchanged:** identifiable units (Pompeii≈0, Noricum, latin-aggregate, Latium et
   Campania, etc.) should keep their H2.1 α within the recovery grid's accuracy (±~0.02–0.03);
   a large move on a control is a red flag.
4. **Coverage caveat carried forward:** per signoff §6c, reported CIs are ~1σ-optimistic by the
   grid's residual bias; flag any unit in a high-residual corner (high %win × high α) and pair
   with the two-bound sensitivity as the disclosure.

## 5. Outputs + retention

- `outputs/units/<name>.json` (per-unit fit) — gitignored (regenerable, deterministic seeds).
- `outputs/refit-summary.json` + `REFIT-VERDICT.md` (per-unit α table + reconciliation) —
  committed. `unit-measurements.json` + `production-slab-library.json` — committed (the locked
  design inputs).

## 6. What this unblocks / what stays gated

Clean refit ⇒ the **OSF amendment** (reverses Amendment 03's shared basis; adopts cc-library;
records the recovery grid + this refit as the gate) — drafted next, **for Shawn's review before
lodging**. The H3b identifiable-set reconciliation folds in. Then the hybrid robustness pilot
(`hybrid-robustness-spec.md`), one fit first. None of these auto-launch.
