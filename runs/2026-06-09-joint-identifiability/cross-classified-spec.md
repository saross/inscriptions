# Cross-classified time × alignment model — spec (D-B contamination fix)

**Status:** ✅ EXECUTED / ADOPTED — signed off (`cross-classified-signoff.md`),
implemented, run, and **adopted as the production lead** (the cross-classified
`library` model is the A04 governing temporal deconvolution; `outputs/cc-VERDICT-library.md`
passes all four adoption criteria; Obs 88/89; production refit
`runs/2026-06-13-cc-production-refit/`). The original "PROPOSED — needs sign-off"
stamp is superseded. **Date drafted:** 2026-06-11. **Author:** Claude Code (Opus
4.8), at the close of the session that ran the 300-cell lead grid. UK/Aus English.

## 0. Why (the motivating result — now measured, not just predicted)

The full 300-cell grid (`outputs/grid-VERDICT.md`, commit `18dac46`) showed the **lead**
model (fixed *estimated* per-unit basis + classification binomial) carries a **systematic,
near-uniform +0.06…+0.08 over-attribution bias** across the entire %win × α surface. The
bias is small in magnitude (mean |median bias| 0.075) but its consequences are real:

- **C1 (do-no-harm, identifiable) FAILS: 37/210 (18%)** — driven entirely by **coverage**
  (mean 0.374, not bias), because the +0.07 shift plus tight CIs miss the truth.
- C2 (confounded) passes 64/90 and beats the baseline ~5× (|bias| 0.066 vs 0.362) — so the
  model *does* resolve the under-attribution it was built for.
- C4 (convergence) marginal: 252/300 cells (84%) at ≥0.95; mean rate 0.950.

**Root cause:** the lead feeds the fit a per-unit convention basis built from the unit's
**grid-aligned-subset SPA**, which is *contaminated* — it is `∝ α·θ_conv·p_conv +
(1−α)·θ_gen·p_gen`, i.e. it carries a faint copy of the genuine peak. The fit inherits that
copy and over-attributes to convention. The κ-sweep already ruled out fixing it via the θ
prior; §1 of `full-grid-spec.md` proposed the cross-classified model as the principled fix.

## 1. The design — separate the contamination instead of inheriting it

Split each unit's inscriptions by alignment into two temporal multinomials that **share**
the latents (α, p_conv, p_gen, θ_conv, θ_gen), rather than feeding one multinomial a
contaminated basis. Per unit with `N` inscriptions, `k` grid-aligned:

```
α            ~ Beta(1, 1)
p_conv       = tier_weights · TIER_BASIS         # see §2 — parameterisation is the key decision
tier_weights ~ Dirichlet(ones(n_tiers))
p_gen        = softmax(cumsum(σ·z))              # non-centred GRW (unchanged from lead)
θ_conv ~ Beta(μ,κ); θ_gen ~ Beta(μ,κ)            # calibrated (rule C: 0.945 / 0.155, κ=40)

# alignment-conditional temporal mixtures (both are proper SPAs; see derivation below)
w_a       = α·θ_conv + (1−α)·θ_gen               # = P(aligned)
p_aligned   = (α·θ_conv·p_conv     + (1−α)·θ_gen·p_gen)     / w_a
p_nonalign  = (α·(1−θ_conv)·p_conv + (1−α)·(1−θ_gen)·p_gen) / (1 − w_a)

k          ~ Binomial(N, w_a)                    observed = k_aligned
y_aligned  ~ Multinomial(k,   p_aligned)         observed = SPA of the aligned subset
y_nonalign ~ Multinomial(N−k, p_nonalign)        observed = SPA of the non-aligned subset
```

`p_aligned` and `p_nonalign` each sum to 1 (the numerator sums to the denominator). The
contamination is gone because **we no longer use the aligned-subset SPA as a basis** — we
*model* it as a mixture. p_conv and p_gen are identified by the **contrast** between the two
subsets: the aligned subset is convention-enriched (weight `α·θ_conv` on p_conv), the
non-aligned subset is genuine-enriched (weight `(1−α)·(1−θ_gen)` on p_gen). That contrast is
the new information the single-multinomial lead never had.

## 2. The key design decision (needs sign-off / second opinion)

**How is `p_conv` parameterised?** This is the crux and the main risk.

- **Option A (recommended start): slab `TIER_BASIS`** — the *clean* editorial-slab dictionary
  (the Amendment-03/H2.1 slab tiers), NOT the contaminated estimated SPA. p_conv =
  tier_weights · TIER_BASIS gives shape-freedom within the slab structure; the two-subset
  likelihood weights the tiers. **Risk:** the 2026-06-09 POC (Exp 1) found that a *shared
  slab basis* failed on confounded cells in the *single-multinomial lead* ("the confidently-
  wrong temporal term overpowers the classification"). The cross-classified likelihood has
  strictly more information (two subsets + their contrast), so a slab basis *may* now be
  identified where it wasn't before — **but this must be proven on the confounded cells, not
  assumed.** If it re-fails, fall back to B.
- **Option B (fallback): free p_conv** — its own GRW or Dirichlet over bins, like p_gen.
  More flexible, but risk of under-identification when α is extreme (α≈0 ⇒ almost no
  convention inscriptions ⇒ p_conv barely informed). Would likely need a weak shape prior.

**Recommendation:** implement A first; if the recovery grid shows confounded-cell failure
(C2 regression or non-convergence), try B. Report whichever is adopted.

## 3. Generator change (`grid_lib`)

The current generator returns `(y, k)` for a cell. The cross-classified arm needs the
alignment-split SPAs. Per inscription draw: type ∈ {conv, gen} by α; aligned ∈ {0,1} by
θ_type (θ_conv_true=0.95 / θ_gen_true=0.15); bin by p_type. Then:

- `y_aligned`     = histogram of aligned inscriptions' bins   (sums to k)
- `y_nonaligned`  = histogram of non-aligned inscriptions' bins (sums to N−k)
- invariants to assert: `y_aligned + y_nonaligned == y` (the lead's y) and `sum(y_aligned)
  == k`. This keeps the cross-classified data **comparable to the lead's** on the same seed,
  so the head-to-head is apples-to-apples.

Keep the existing seed policy (`BASE_SEED + cell_index`, per-rep offset) so a cell's draw is
identical to the lead's; only the *summary* (split vs pooled) differs.

## 4. Implementation notes (do NOT repeat the leak)

- New `build_model_cross_classified(...)` in `joint_lib.py`. **Wrap `y_aligned`,
  `y_nonaligned`, `k` in mutable `pm.Data`** from the start (the lead's `set_data` lesson —
  build once per cell, swap per rep; never bake data as constants). zero external dependents.
- Reuse the validated GRW/Dirichlet/θ blocks verbatim from `build_model_joint`.
- Same sampler config (DRAWS/TUNE/CHAINS/TACC), `cores=1`, spawn + `max_tasks_per_child=1`,
  `TMPDIR` on root fs, cgroup `MemoryMax` cap. The memory + /tmp infrastructure is solved;
  inherit it.
- **Watch convergence:** the cross-classified model has two multinomials + a binomial + the
  same GRW/Dirichlet; geometry may be harder. If C4 regresses, consider reparameterisation
  (e.g. softmax/stick-breaking on tier_weights, or tighter σ prior) before widening compute.

## 5. Scope + acceptance (head-to-head vs the lead)

Reduced arm (per `full-grid-spec.md` §2 robustness): run the cross-classified model on the
**confounded + identifiable cells head-to-head with the fixed-estimated-basis lead** — the
lead's 300-cell results already exist (`outputs/grid/`), so the arm only needs to fit the
**cross-classified** model on the same cells (or a representative subset). Spec budget
~600 fits; at the new n_jobs=12 + set_data speed this is a short run (~1–2 h), so consider
the **full 300 cells** for a clean like-for-like rather than a subset.

**Adopt the cross-classified model as the production lead IFF, vs the fixed-basis lead:**

1. **Bias surface flattens** — the uniform +0.07 drops to ≈0 (or at least materially below
   the lead's), especially on identifiable cells.
2. **C1 recovers** — identifiable coverage rises toward ≥0.90 (the lead's 0.374 is the bar to
   beat); |median bias| stays <0.12.
3. **C2 not sacrificed** — confounded |bias| stays well below baseline (the lead's 0.066 vs
   0.362 advantage is preserved, not traded away).
4. **C4 not materially worse** — convergence stays ≥ the lead's 84%/0.950.

If it improves C1/coverage without sacrificing C2, it is the better production model and the
OSF amendment adopts it (and the §0 contamination finding becomes the *motivation* narrative
rather than a disclosed limitation). If it does **not** clearly beat the lead, fall back to
the lead's "accept-and-report +0.07 + two-bound α sensitivity" path.

## 6. What this unblocks downstream

- Clean pass ⇒ **production refit of the 28 units (+ Italia)** under the chosen model →
  **OSF amendment** (sweep ALL changes since the last lodged amendment; it REVERSES
  Amendment 03's shared basis; the prereg-note "Planned remediation" § is stale-flagged).
- THEN Option 3 (hybrid, `hybrid-robustness-spec.md`): pilot ONE hybrid fit first.
- Open D-A (single vs 3-row per-unit basis) is moot for the cross-classified model if p_conv
  uses the slab TIER_BASIS (Option A) — note in whichever direction is chosen.
