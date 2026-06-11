# Cross-classified arm (D-B) — sign-off review and second opinions

**Status:** SIGNED OFF with three corrections (§2–§4 below) and a staged execution plan (§5).
**Date:** 2026-06-11. **Reviewer:** Claude Code (Fable 5), fresh-eyes pass requested in the
2026-06-11 resume brief. **Reviews:** `cross-classified-spec.md` (commit `37a94c5`).
UK/Aus English.

## 1. Overall verdict on the design

The cross-classified time × alignment model is the right fix, and the case for it is stronger
than the spec claims. The spec frames it as "separate the contamination instead of inheriting
it". The sharper statement: **the cross-classified model is the *exact* likelihood of the
assumed per-inscription generative process, whereas the lead is a composite likelihood with a
contaminated plug-in.** Under the generative model (per inscription: type ~ Bernoulli(α),
bin ~ p_type, aligned ~ Bernoulli(θ_type)), the joint law of the cross-classified counts
factorises exactly as

```text
k          ~ Binomial(N, w_a),                w_a = α·θ_conv + (1−α)·θ_gen
y_aligned  ~ Multinomial(k,   p_aligned)      (independent of y_nonalign given k)
y_nonalign ~ Multinomial(N−k, p_nonalign)
```

with `p_aligned`, `p_nonalign` as in spec §1 — the standard lumping/thinning factorisation of
an i.i.d. categorical process. The lead, by contrast, (a) treats `y` (pooled) and `k` as
independent given parameters, which they are not under the generative process, and (b) plugs
in a convention basis built from data the model should be explaining. D-B removes both
defects at once, not just the contamination. This is worth saying in the OSF amendment: the
cross-classified model is not a patch but the *completion* of the concomitant-variable design
the scout synthesis identified as canonical (Dayton & Macready 1988; Huang & Bandeen-Roche
2004; OxCal archetype Bronk Ramsey 2009).

## 2. §2 decision — p_conv parameterisation (the requested sign-off)

**Decision: do not pick A or B blind — run a cheap three-arm pilot, then commit the full grid
to the winner.** The three arms:

- **Arm `tiers3` (Option A as written):** `p_conv = tier_weights · LATIN_BASIS` (the shared
  Amendment-03/H2.1 3-tier empirical basis, `design.json::tier_basis_empirical_latin`).
- **Arm `library` (Option A′ — my recommended candidate):** `p_conv = tier_weights ·
  SLAB_LIBRARY`, where the library rows are the **deterministic aoristic boxes of individual
  round-endpoint slabs** (19 rows: lo ∈ {1, 51, 76, 101, 151} × hi ∈ {150, 200, 250, 300},
  lo < hi), fixed across all cells.
- **Arm `free` (Option B):** `p_conv` gets its own non-centred GRW, mirroring `p_gen`.

**Why I expect Option A as written to fail confounded cells (the spec's own flagged risk,
now made quantitative).** In a confounded cell the aligned subset's true shape is
≈ 0.80·p_conv + 0.20·p_gen (at α = 0.4, θ at truth) — concentrated in AD 100–300. The shared
3-tier basis cannot produce a concentrated shape (POC: ~36 % of its mass sits before AD 100).
The model's escape route is α → 0 with θ_gen drifting up to match k/N: that costs roughly
10 nats against the κ = 40 θ_gen prior plus a small two-subset shape-compromise cost, whereas
holding α at truth with a broad-forced p_conv costs hundreds of nats of multinomial mismatch
on the aligned subset (≈ k × KL, with k ≈ 1,300 at N = 2,800). The α → 0 route wins, and now
*two* multinomials are confidently wrong instead of one — POC Experiment 1's failure mode
should reproduce or worsen. This is a prediction, and the pilot measures it rather than
assuming it; but it is why `tiers3` is not the recommended candidate despite being "Option A
as written".

**Why `library`, not the estimated basis, and not only `free`.** The contamination in the
lead entered because the basis *mass* was estimated from the aligned-subset SPA. A slab
*library* keeps the slab structure (the true convention is, by construction here and
plausibly in production, a weighting of round-endpoint slabs) while every row's shape is
**deterministic arithmetic from its endpoints — no data, no contamination channel**. The
Dirichlet weights are then identified by the two-subset contrast. `free` (Option B) is the
safety net: maximally flexible, but weakly informed at extreme α and structurally able to
absorb genuine shape; if `library` passes, `library` is the more constrained, more
interpretable choice.

**Production analogue of `library` (record this in the amendment if adopted):** per-unit
slab *catalogue* — rows are the deterministic aoristic boxes of the distinct grid-aligned
interval types observed in the unit (optionally plus the corpus-wide common slabs).
Catalogue *membership* is data-derived, but a misclassified genuine inscription contributes
only a candidate row with a free weight the Dirichlet can zero — contamination by membership,
not by mass. This is qualitatively weaker leakage than the lead's fixed estimated basis.

**Grid-vs-truth representability note:** the recipes' (50, ·) slabs are represented in the
library by (51, ·) rows — a sub-bin (≤ 1-year-in-5-year-bin) difference, negligible against
the 0.12 bias gate, and deliberately retained so the library does not exactly contain the
truth (production catalogues never do). The 50/51 near-duplicate rows were *not* both
included, to avoid near-collinear Dirichlet components degrading the tier_weights R̂ that the
convergence gate (unchanged from the lead, for comparability) includes.

**D-A is moot** under `library` and `free` (no estimated basis, no bracket question), as the
spec §6 anticipated. It remains moot under `tiers3` (shared basis has no per-unit bracket).

## 3. Correction 1 — the §3 generator invariants are unsatisfiable as written

Spec §3 asks for a fresh per-inscription draw *and* the invariant `y_aligned + y_nonaligned
== y (the lead's y)` under the same seed. These are incompatible: the lead drew `y ~
Multinomial(N, p_mix)` and then `k ~ Binomial(N, π)` **independently** from one RNG stream; a
per-inscription simulation consumes the stream differently and cannot reproduce the lead's
`y` bit-for-bit (nor its `k`, which under the true process is *dependent* on `y` anyway).

**Fix (implemented): the conditional-split construction, which is exactly equivalent to the
per-inscription draw.** Draw `y` with the identical first RNG call (bit-identical to the
lead's `y` by construction), then split each bin's count with an independent RNG:

```text
m_j | y_j ~ Binomial(y_j, q_j),   q_j = [α·θ_conv·p_conv_j + (1−α)·θ_gen·p_gen_j] / p_mix_j
y_aligned = m;  y_nonaligned = y − m;  k_cc = Σ_j m_j
```

`q_j` = P(aligned | bin j) under the generative process, so `(y, m)` has exactly the
per-inscription joint law (marginally `k_cc ~ Binomial(N, π)` — same law as the lead's `k`,
a different realisation). Invariants that hold and are asserted: `y_aligned + y_nonaligned ==
y` (lead's `y`, bit-identical), `sum(y_aligned) == k_cc`, `0 ≤ m_j ≤ y_j`. The lead's `k`
is irrelevant to the cc fit; the head-to-head pairs cells on identical `y` draws and
aggregates over 100 replicates, so the `k` realisation difference is immaterial at cell level.

Seed policy: split RNG = `data_seed + 1_000_000`, cc-fit sampler seed = `data_seed +
1_300_000`, where `data_seed = (BASE_SEED + cell_index) · 1000 + rep`. Offsets chosen so no
(cell, rep, purpose) seed collides with the lead's data (+0), joint-fit (+500 000), or
baseline-fit (+700 000) seeds across the 300-cell × 100-rep range.

## 4. Correction 2 — the §5 compute estimate is ~15× low

Spec §5 says a full 300-cell like-for-like is "a short run (~1–2 h)". Measured lead-grid
throughput (25.1 h, n_jobs = 12, 39,000 fits) is **27.8 core-seconds per fit**. The cc model
adds a second 80-bin multinomial, so per-fit cost will be ≥ the lead's. Aggregates:

| stage | fits | wall-clock @ n_jobs = 12 |
|---|---|---|
| smoke (1 cell × 2 reps × 3 arms) | 6 | minutes |
| pilot (20 cells × 20 reps × 3 arms) | 1,200 | ~ 1–1.5 h |
| full grid, chosen arm (300 × 100) | 30,000 | **~ 21–28 h** (overnight-plus) |

No baseline re-fit is needed (the lead grid's per-cell baseline results are reused for C2),
saving 9,000 fits. **Hard-stop rule honoured:** if the pilot-measured per-fit time projects
the full run past ~30 h, halt and report to Shawn before launching — do not trim reps or
cells to fit.

## 5. Execution plan (staged, phase-gated)

1. Sign-off (this document) → commit.
2. Implement: `grid_lib.generate_cc` + `SLAB_LIBRARY`; `joint_lib.build_model_cross_classified`
   (modes `tiers3` / `library` / `free`; `y_aligned`, `y_nonaligned`, `k` all mutable
   `pm.Data` — build once per cell, `set_data` per rep, per spec §4); `run_cc_grid.py`
   (spawn + `max_tasks_per_child`, atomic writes, validity-gated resume, per-arm output dirs,
   `--pilot`); `aggregate_cc_grid.py` (head-to-head vs `outputs/grid/`). `/audit` before launch.
3. Sapphire: SHA-verify-then-remove the four untracked files, pull, smoke test (invariants +
   timing).
4. **Pilot** (the §2 decision gate): 20 cells — recipes {broad, conc, stress} × α {0.0, 0.4,
   0.8} × genuine {gauss_early, gauss_inwin} × N 2800, plus `conc_a0.4_regnal_N2800` and
   `stress_a0.8_regnal_N2800` (8 confounded, 12 identifiable) — × 20 reps × 3 arms. Arm
   choice criteria, in order: (i) confounded bias profile (C2 proxy — does the arm hold α
   near truth where `tiers3` is predicted to collapse?), (ii) identifiable bias flatness
   (does the +0.07 vanish?), (iii) coverage, (iv) convergence. Ties break towards `library`
   (more constrained than `free`).
5. Phase-gate skill at the pilot → production boundary, then the full 300 × 100 run of the
   chosen arm, detached on sapphire under the solved infra (root-fs `TMPDIR`, 50 G cgroup
   cap via `systemd-run --user`, spawn + recycle, n_jobs 12), resumable at cell granularity.
6. `aggregate_cc_grid.py` → `cc-VERDICT.md` head-to-head against spec §5's four adoption
   criteria. Only verdict + summary artefacts committed (grid-state retention rule).

## 6. Second opinions (the four items from the resume brief)

### 6.1 Is the alignment split the right contamination fix? Does a slab TIER_BASIS risk re-introducing POC-Exp-1?

Yes to the first — and it is stronger than "a fix": it is the exact likelihood of the
generative process (§1), with α now identified through two channels at once (the binomial
count *and* the compositional contrast between the two subsets), where the lead had only the
count. On the second: **Option A as *written* (shared 3-tier basis) does risk exactly the
POC-Exp-1 re-failure, and §2 gives the quantitative argument why it should be expected** —
the escape route to α = 0 is ~ 10 prior-nats cheap while truthful α with a broad-forced
p_conv costs hundreds of multinomial nats. The extra information in the two-subset likelihood
raises the cost of the escape (the subsets' *shape contrast* must also be explained away),
but with both component shapes in-window (confounded regime) that contrast is weak. The slab
**library** variant keeps Option A's structure while removing its failure mode: shape freedom
within the slab family, zero contamination channel through the basis mass. The pilot decides
on measurement, not on this argument.

### 6.2 Coverage 0.374 with bias 0.075 — pure shift, or under-propagated uncertainty?

**Pure shift, with the data to show it.** From the 300 per-cell replicate records on sapphire
(converged reps only): identifiable-cell mean 95 % CI half-width 0.0659 → implied posterior
σ ≈ 0.034; mean |median bias| 0.075 → **bias ≈ 2.2 σ**, and a pure-shift normal
approximation predicts coverage 0.405 against the observed 0.374 — the shift explains ~ 93 %
of the failure. The residual is second-order (replicate-level bias scatter around the cell
median). Crucially, the posterior is **not** under-dispersed: the CI-implied posterior σ is
**1.6–2.0× the actual sampling sd of the point estimate** across every regime × N stratum
(e.g. identifiable N = 2,800: 0.035 vs 0.018), because the θ-prior uncertainty contributes
interval width but no replicate-to-replicate scatter. The model propagates *more* than the
sampling uncertainty; it is simply aimed 2 σ off-target. Consequence: if D-B removes the
bias, coverage should return to ≥ 0.95 (likely conservative) with no structural change to
uncertainty handling — and "fix the bias, not the intervals" is the right order of operations.

### 6.3 C4 marginal (84 %, mean R̂-pass 0.950) — reparameterise before scaling D-B?

**No — measure first.** Two reasons. (a) The cc likelihood is *more* informative (the
aligned subset is ≈ 80 % pure convention at moderate α; the non-aligned ≈ 96 % pure genuine),
which shortens the weakly-identified α–GRW ridge that is the likely cause of the lead's
marginal convergence — geometry should improve, not worsen, despite the extra multinomial.
(b) The lead's C4 was itself only marginal, not failing, and any reparameterisation applied
to the cc arm but not the lead contaminates the head-to-head. The pilot reports per-arm
convergence rates; if an arm regresses, the cheap ladder is target_accept 0.95 → 0.97, then
tier_weights stick-breaking / tighter σ_smooth — *before* widening compute (spec §4 already
says this; endorsed). One design choice in §2 already serves convergence: the 19-row library
deliberately excludes near-duplicate (50, ·)/(51, ·) row pairs that would create
near-collinear Dirichlet components and degrade tier_weights R̂.

### 6.4 Is "classification-as-likelihood + estimated basis" the best design vs the concomitant-variable / OxCal alternatives?

The question dissolves under D-B: **the cross-classified model *is* the concomitant-variable
latent-class model, in collapsed exact form** — per-inscription latent type with two manifest
indicators (temporal bin, alignment), aggregated to sufficient counts. The lead's
"classification-as-likelihood + estimated basis" was an approximation to it (composite
likelihood + plug-in); D-B closes the gap, so we are no longer choosing *between* our design
and the literature's remedy — we are implementing the literature's remedy properly (Huang &
Bandeen-Roche identification-by-covariate; OxCal's two-component mixture as the
archaeological archetype). The one genuine alternative family left — upstream filtering or
external-proxy subtraction — was already rejected for principled reasons (it discards the
quantity of interest). Framing for the amendment: the lead grid's +0.07 surface is the
measured cost of the composite-likelihood approximation; the cc model is the exact-likelihood
completion. Gustafson's partial-identification lens: under the lead, α was identified only
through the θ-instrumented binomial; under D-B it is identified through that *and* the
subset-shape contrast — strictly more identifying information, which is also why 6.3 expects
better geometry.

## 7. Risks accepted

- The pilot adds ~ 1–1.5 h sapphire compute and one decision gate before the full run —
  chosen deliberately over burning a 21–28 h full grid on a predicted-to-fail arm.
- `library` hands the fit a slab family that (approximately) spans the truth; a
  dictionary-misspecification arm (truth outside the library) is Tier-2 interval-level
  territory (`full-grid-spec.md` §2) and out of scope for D-B.
- The cc arm's `k` realisations differ from the lead's (same law); cell-level head-to-head
  is unaffected.
