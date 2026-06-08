# Full-grid recovery re-validation — REPORT

**Status:** COMPLETE — verdict **PASS** (Amendment-01 §A5.5.1 binding criterion).
Scored 2026-06-08 over the clean 450-cell grid (after the 12-cell disk-failure
re-run; see §0.1). Numbers below are read from the summariser output
(`inscription-mass/outputs/REPORT.md`, `tables/grid-summary.parquet`) and the
α-LoA artefact (`tables/alpha-loa-summary.json`), all committed alongside.

**Author:** Claude Code (Opus 4.8) on Shawn Ross's brief.
**Design:** `runs/2026-06-06-convention-basis-redesign/design.json`
(`tier_basis_empirical`, Option 2; Decision 38).
**Predecessor:** `STAGE1-TRIAGE-REPORT.md` (Stage-1 stress-triage, PASS, 2026-06-06).

---

## 0. Provenance

### 0.1 Run history (the grid ran in two passes)

- **Full grid, pass 1** (PID 1681813): launched 2026-06-06 13:45 UTC, finished
  2026-06-08 00:26 UTC, wall 34.7 h. **438 ok / 12 failed.** All 12 failures were
  `smooth_decline` cells that hit `OSError [Errno 28] No space left` during a
  transient ~1h40m window (2026-06-07 15:53–17:34 UTC) when PyTensor's numba
  compile temp files filled the 31 GB RAM-backed `tmpfs` `/tmp`. An
  **infrastructure failure, independent of the model**; integrity check confirmed
  the 438 good cells each carry exactly 100 replicates (no silent truncation).
- **Re-run, pass 2** (PID 1810768): the 12 failed cells re-run 2026-06-08 with
  `TMPDIR` redirected to the 264 GB root disk (the fix). **450 ok / 0 failed**,
  wall 1.05 h. Deterministic seeds (`cell_seed = base_seed + cell_index`) ⇒ the
  re-run reproduces the synthetics that would have run — not a retry-until-pass.
  Original failure state preserved at `grid-state.before-rerun-2026-06-08.json`.

### 0.2 Scoring

Scored with `code/grid-summariser.py` (the opt-in-regression fix, commit
`5494347`; `--assert-grid-a-regression` left **off** — this basis's headline is a
measurement, not a Grid-A regression target). Binding criterion = Amendment 01
§A5.5.1: convergence precondition (≥ 90 % replicates pass R̂ < 1.01 ∧ bulk-ESS
≥ 400) + hybrid shape gate (median Pearson r ≥ 0.95 non-flat; Wasserstein-1
≤ 10 y for `flat_baseline`), α-coverage demoted to a shape-conditioned
**diagnostic**, evaluated within the operating envelope (α ≤ 0.70); ≥ 90 % of
in-envelope cells must clean-pass.

---

## 1. Headline verdict — **PASS**

| Figure | Value | Bar |
|---|---|---|
| **Headline B** (clean-pass ÷ in-envelope) | **96.4 %** (347/360) | ≥ 90 % → **PASS** |
| Diagnostic A (shape-pass ÷ convergence-eligible in-envelope) | 97.2 % (347/357) | — |
| Convergence-excluded in-envelope | 3 cells, all `regnal_cluster` | — |
| Stress row (α = 0.95, never gated) | shape-pass 17.8 % (90 cells) | reported only |
| Basis-shift vs Grid A | 96.4 % vs 98.6 % (Δ **−2.2 %**) | informational |

The 13 in-envelope non-clean-passes are **3 non-converged + 10 shape-misses**,
concentrated in `regnal_cluster` (the sharp-spike shape) and a few large-N
`bimodal` cells — the expected hard corners, comfortably inside the 10 %
tolerance. The lodged-reference criterion "FAILs" (coverage 71.8 %, shape-r
65.8 %) exactly as Amendment 01 anticipated — that's the demoted exact-α-coverage
+ strict-Pearson rule (large-N coverage collapse; `flat_baseline` Pearson
undefined), not binding.

## 2. Shape-recovery map (per-axis pattern)

Per-axis pass rates (lodged-criterion descriptive columns, from the auto-REPORT
§2; the binding clean-pass is the §1 headline). Reads that matter:

- **By α** — shape recovery is strong across the envelope (shape-pass 76–83 % at
  α ∈ {0.05, 0.3, 0.5, 0.7}) and **collapses only at the α = 0.95 stress row**
  (7 %), which is out of the operating envelope by design (5 % genuine mass).
- **By tier_weights** — `multicentury_heavy` shape-pass **64 %**, statistically
  indistinguishable from every other tier (64–69 %). **The multi-century tier is
  NOT a systematic failure** — see §4.
- **By shape** — `rise_and_fall`/`smooth_*` strong (76–84 %); `regnal_cluster`
  and `bimodal` are the weaker peaked shapes. `flat_baseline` reads 0 % here
  *only* because Pearson r is undefined for a flat signal; under the binding gate
  it is scored on Wasserstein-1 (≤ 10 y), which it passes (W1 mostly < 2 y).
- **By N** — the large-N α-coverage decline (91 % → 57 % from N=2 000 → 50 000)
  is the benign, documented coverage collapse under negligible bias (demoted to
  diagnostic), not a recovery failure.

## 3. Operating envelope (α ≤ 0.70) — CONFIRMED

The α ≤ 0.70 ceiling holds: clean-pass is 96.4 % within it, and shape recovery
degrades sharply only at α = 0.95 (outside). No basis to tighten or loosen the
launch-spec's envelope (N ≥ 2 000 ∧ posterior α ≤ 0.70).

## 4. α recovery (Bland–Altman LoA) — within Decision 33's ±0.18 envelope

In-envelope (α ≤ 0.70), posterior-median estimator, per-cell signed bias
(`tables/alpha-loa-summary.json`, via `code/compute-alpha-loa.py`):

| | New basis | Decision 33 / Grid A |
|---|---|---|
| Mean signed bias | **+0.005** (essentially unbiased) | −0.02 |
| 95 % LoA (pooled) | **[−0.12, +0.13]** (±0.123) | [−0.22, +0.17] (±0.18) |
| 90th-pct \|bias\| smooth/flat | **0.073** (LoA ±0.09) | 0.07–0.11 |
| 90th-pct \|bias\| multimodal (bimodal, regnal_cluster) | **0.130** (LoA ±0.18) | 0.18–0.27 |

The new basis recovers α **slightly better than** the validated Grid A and sits
**inside the ±0.18 envelope**. The shape-conditioned hedge carries over: ±0.09 in
smooth/flat regimes, ±0.18 in peaked regimes. α-derived claims stay coarse and
directional — not a tight dial.

## 5. Interpretation — the Decision-38 §6 fear is resolved at scale

The §6 fear was that the new multi-century tier (a long flat body + an AD 300–350
envelope-edge plateau) would be mistaken for genuine quiescence, under-attributing
to convention. The full grid corroborates the triage's negative finding **at
scale and across all shapes**: `multicentury_heavy` clean-passes at the same rate
as every other tier within the envelope, and α is recovered essentially unbiased
(+0.005). The plateau is attributed to convention, not confused for genuine
signal. Convergence is ≥ 0.90 in 357/360 in-envelope cells (the 3 exceptions are
`regnal_cluster`, the known-hard peaked shape, not the multi-century tier).

## 6. Recommendation

**PASS — proceed.** Fill Amendment 03 §A5.5 + launch-spec §7 from this verdict
(done, this session); generate + lodge Amendment 03; sign off the launch spec;
build + launch the H2.1 26-unit fit. The weak corners (peaked shapes at large N;
the α = 0.95 stress row) are out-of-envelope or within tolerance and are already
hedged by the operating envelope + the shape-conditioned α LoA.

## 7. Artefacts (committed)

- Auto-tables: `inscription-mass/outputs/REPORT.md`,
  `tables/grid-summary.parquet`.
- α bias / LoA: `tables/alpha-bias.parquet`, `tables/alpha-loa-summary.json`
  (`code/compute-alpha-loa.py`).
- Grid state (final, 450/0): `inscription-mass/outputs/grid-state.json`;
  pre-rerun snapshot `grid-state.before-rerun-2026-06-08.json` (on sapphire).
- Per-cell summaries (450) + per-replicate posteriors: on sapphire (gitignored bulk).
- Stage-1 triage: `STAGE1-TRIAGE-REPORT.md`.
