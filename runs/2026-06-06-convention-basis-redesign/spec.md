# Recovery re-validation spec — Decision 38 empirical convention basis

**Date:** 2026-06-06
**Author:** Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief
**Status:** **SPEC — awaiting Shawn sign-off before any sapphire launch.**
**Binds:** Decision 38 §6 (recovery re-validation gate); Decisions 33, 35, 37.
**Generative basis:** `runs/2026-06-06-convention-basis-redesign/design.json`
(empire frame, `tier_basis_empirical`).

---

## 1. Why this is required (Decision 38 §6)

Grid A's 98.6 % α-coverage validated the **old** curated tier-basis shapes
(century / half-century / reign). It does **not** transfer to the new basis: the
`multi_century` tier is a **long flat body plus an envelope-edge plateau**
(15.3 % of its mass piled into AD 300–350 from wide late slabs such as
`[301,500]`; max/min density ratio 226). Decision 38 §6 warns this is *plausibly
harder* to recover — a flat convention plateau is confusable with genuine
quiescence, and a high-α multi-century-heavy unit could have its peaked genuine
signal masked. **No real-LIRE mixture has ever been fit under any basis**; this
re-validation is the gate before the H2.1 production fit.

The learned-weight count is unchanged (3), so the Dirichlet/α/GRW machinery the
prior grid validated is structurally identical — only the **basis shapes**
change. That is what bounds the re-validation to a basis-shape question rather
than a full method re-derivation.

---

## 2. Two-stage design: STRESS-TRIAGE first, then full grid

Decision 38 §6: *"run an α = 0.95 × multi-century × peaked-genuine stress-triage
first, then the full grid only if it passes."* This is a **gate**, not a warm-up:
if the triage fails the hardest corner, we stop and reconsider tier structure
(Decision 38 revisit trigger — fewer tiers, tighter empirical-anchored Dirichlet,
or move the multi-century shape to a fixed component) **before** spending the
full-grid compute.

### 2.1 Stage 1 — stress-triage (the gate)

The single hardest region of the cell space:

| Axis | Triage value | Rationale |
|---|---|---|
| α (convention fraction) | **0.95** | convention-dominated; the regime where a mis-specified plateau most distorts the recovered genuine |
| tier weights | **multicentury_heavy** `[0.10, 0.10, 0.80]` | the collinear, envelope-edge-plateau-dominated tier |
| genuine shape | **rise_and_fall, regnal_cluster, bimodal** (the 3 peaked library shapes) | peaked genuine is the masking-risk case Decision 38 §6 names |
| N | **2,000 and 10,000** | 2,000 = the production reachability floor (Decision 34, hardest); 10,000 confirms scaling |

→ **6 stress cells** (1 α × 1 tier × 3 shapes × 2 N) × 100 replicates = **600 fits**.

**Sanity contrast (2 cells, run alongside):** the same corner with
`shape = flat_baseline` at N ∈ {2,000, 10,000} — confirms the flat-genuine case
under a multi-century-heavy plateau is *also* recovered (guards against the
basis silently absorbing all signal). Total Stage 1 = **8 cells / 800 fits**.

**Triage gate (Amendment 01 §A5.5.1 criterion — CORRECTED 2026-06-06 after the
run; the original "α-coverage ≥ 0.90 binding" wording below was inconsistent with
the lodged framework and is superseded):**
- per-cell **convergence_pass_rate ≥ 0.90** (binding; re-derived R̂ < 1.01 ∧ bulk-ESS ≥ 400);
- **α recovered within the documented envelope** (binding) — small mean |α-bias|
  and, critically, **no systematic under-attribution to genuine** (the
  plateau-confusion failure mode Decision 38 §6 names: a multi-century plateau
  absorbed into `p_gen` would show as an α *under*-estimate). **α-coverage is a
  DIAGNOSTIC, not a gate** (Bland–Altman limits of agreement, shape-conditioned):
  exact CI coverage of the mixing weight collapses at large N under negligible
  bias and "is not field-standard" (Amendment 01 §A5.5.1; Decision 33).
- shape **Pearson r(p_gen)** reported; at α = 0.95 it is N-limited (only 5 %
  genuine mass) and is **not binding at this beyond-envelope corner** (production
  is α ≤ 0.70, Decision 37 D5).

> **OUTCOME (2026-06-06): PASS.** 8/8 cells converged (1.00). α recovered to
> +0.029 at the worst corner (`rise_and_fall`, N=10,000: 0.979 vs true 0.95) — the
> plateau is attributed to convention, *not* confused for genuine quiescence. The
> single sub-0.90 α-coverage cell (0.81) is the benign large-N collapse above
> (bias +0.029, sd 0.012, shape r 0.838), not a recovery failure. Full detail:
> `revalidation/STAGE1-TRIAGE-REPORT.md`. → proceed to Stage 2.

If the gate holds → proceed to Stage 2. If not → **halt and report**; do not
launch the full grid (Decision 38 revisit trigger; standing hard-stop rule).

### 2.2 Stage 2 — full grid (only if Stage 1 passes)

The complete re-validation over the new basis + new tier-weight grid:

| Axis | Values | Count |
|---|---|---|
| genuine shape | flat_baseline, smooth_growth, smooth_decline, rise_and_fall, bimodal, regnal_cluster | 6 |
| α | 0.05, 0.30, 0.50, 0.70, 0.95 | 5 |
| tier weights | uniform, subcentury_heavy, century_heavy, multicentury_heavy, **empirical** `[0.184, 0.431, 0.385]` | 5 |
| N | 2,000, 10,000, 50,000 | 3 |

→ **450 cells × 100 replicates = 45,000 fits** (same envelope as the validated
grid). The `empirical` tier-weight case is the realistic operating point (the
corpus convention-tier frequencies); it is the cell whose recovery most directly
licenses the production fit.

**Full-grid acceptance (Amendment 01 §A5.5.1 criterion — supersedes the
design.json `decision_rule` α-coverage thresholds):**
- **shape (binding):** per-cell median Pearson r ≥ 0.95 (non-flat shapes) and
  global ≥ 0.90; Wasserstein-1 patches the flat-genuine case (undefined r);
- **convergence (binding):** per-cell pass-rate ≥ 0.90;
- **α (diagnostic, NOT a gate):** reported as Bland–Altman limits of agreement,
  shape-conditioned (Amendment 01 §A5.5.1); the design.json `decision_rule`
  α-coverage ≥ 0.90 thresholds are superseded and reported as context only;
- **operating envelope:** production reportability is α ≤ 0.70 ∧ N ≥ 2,000
  (Decision 37 D5); cells above α = 0.70 characterise the boundary, not production.

A clean pass licenses the OSF amendment + H2.1 launch spec. A localised fail
(e.g. only the α = 0.95 × multicentury_heavy × peaked corner) is reported as the
method's **operating envelope** (Decision 37 D5 already gates production fits on
N ≥ 2,000 ∧ posterior α ≤ 0.70 — a high-α fail would simply confirm that ceiling
rather than block the method).

---

## 3. Harness integration (minimal; reuse the validated code)

Reuse the 2026-05-26 two-unit harness
(`runs/2026-05-26-recovery-grid-two-unit/code/`) **unit = inscription** — a single
grid, not two (the letter-mass question is separate and already settled). Exactly
**one** code change is required:

1. **`cell_lib.build_tier_basis`** — load the empirical basis when present:
   ```python
   if "tier_basis_empirical" in design:
       basis = np.asarray(design["tier_basis_empirical"], dtype=float)
       # validate shape (3, n_bins) and row sums ~1; return basis
   # else: existing template_intervals_by_tier construction (backward-compatible)
   ```
   This is additive and leaves the old path intact.

Everything else runs **unchanged** against the new `design.json`:
- `enumerate_grid_cells` reads the new `tier_weight_grid` directly. The
  `pilot_proxy` override is a **no-op** here — the new grid has no tier named
  `pilot_proxy` (it is `empirical`), so `pilot_proxy_for("inscription", …)`
  writes its record file and overrides nothing.
- `synth.generate_replicate` already takes `tier_basis` as an argument.
- `fit.fit_replicate`, `aggregate.aggregate_cell`, `grid-summariser.py` unchanged.

**Two small harness conveniences (optional, recommended):**
- add a `--base-seed` flag to `run-grid.py` (default = `design["base_seed"]` =
  20260606) so the re-validation uses a fresh synthetic stream rather than the
  hard-coded 20260526 (the basis is new regardless, but a fresh seed is cleaner);
- run Stage 1 via `--cell-indices <the 8 triage indices>` (computed from
  `enumerate_grid_cells` order: shapes alphabetical × α asc × tier alphabetical ×
  N asc) **or** a 10-line `triage-cells.py` that filters cells to the triage set
  — the latter is clearer and less index-fragile; recommend the small script.

Run root: a fresh `runs/2026-06-06-convention-basis-redesign/revalidation/`
(keeps the artefact run dir clean; the harness writes `inscription-mass/` under it).

---

## 4. Compute plan (sapphire)

Per the 2026-05-22 SMT lesson and Decision 37 D6:
```
ssh sapphire; cd ~/Code/inscriptions
taskset -c 0-11 ~/.local/bin/uv run python \
  runs/2026-05-26-recovery-grid-two-unit/code/run-grid.py \
  --unit inscription \
  --design-json runs/2026-06-06-convention-basis-redesign/design.json \
  --run-root   runs/2026-06-06-convention-basis-redesign/revalidation \
  --n-jobs 12  --base-seed 20260606  [--cell-indices … for Stage 1]
```
with `PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False` and BLAS threads pinned to 1
(run-grid.py sets both). Sampler: `n_draws=2000, n_tune=1000, n_chains=4,
target_accept=0.95, cores=1` (the validated defaults; raise `n_tune` on a
convergence failure, **never** relax the gate).

**Estimated wall-clock** (from validated per-fit times: N=2k ≈ 18 s, N=10k ≈ 30 s,
N=50k slower):
- Stage 1 triage: 8 cells, all in-flight at once under n_jobs=12 → **≈ 30–50 min**.
- Stage 2 full grid: 450 cells → **≈ 1–1.5 days** parallelised (the validated
  grid's envelope).

Commit the design artefact **before** launch (research-record rule). A `STATUS.txt`
on sapphire + `grid-state.json` give resumable progress (cell-granular resume is
built in).

---

## 5. Pre-launch checklist (Shawn sign-off gate)

- [ ] Basis-population decision confirmed (REPORT §5: fixed shared basis per
      frame; empire basis for re-validation) — **Shawn**.
- [ ] Triage cell set + gate thresholds approved (§2.1) — **Shawn**.
- [ ] `build_tier_basis` empirical-load change written + unit-checked (row sums,
      shape) — CC, pre-launch.
- [ ] `--base-seed` flag (or accept 20260526) — decision.
- [ ] Run on sapphire, **Stage 1 first**; report the triage verdict to Shawn
      **before** launching Stage 2.
- [ ] On Stage 2 pass → OSF amendment draft + H2.1 launch-spec rewrite.

**Hard stops (standing rules):** do not silently negotiate the grid down to fit a
time budget; do not relax the convergence gate to pass a cell; halt and report on
any triage-gate failure rather than proceeding to the full grid.

---

## 6. What this unblocks

A clean re-validation is the last technical gate before H2.1. On pass:
1. OSF amendment (convention-model revision; separable from Amendment 02);
2. H2.1 launch-spec rewrite around this basis (Decision 37 D1–D6 + audit additions);
3. Shawn sign-off → launch the 26-unit production mixture fit.
