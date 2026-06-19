# Finer-α operating-envelope confirmation (α 0.70–0.90 at N = 2000) — REPORT

- **Status:** ✅ COMPLETE (run 2026-06-04 on sapphire). This report + provenance
  note was added 2026-06-20 (pre-write-up uplift); the dir previously held only
  the two output files with no code/spec/report/Obs (HIGH-severity gap in
  `planning/results-documentation-uplift-2026-06-20.md`, Tier-1 item 4). **No
  code is fabricated here** — the generating script was intentionally not
  committed (see provenance below); this report documents what produced the
  files, the result, and the traceable lineage.
- **What it is.** A finer-α recovery sweep that confirms the **α ≤ 0.70
  operating envelope** adopted in OSF Amendment 01 §A5.5.1 / §A5.7. It extends
  the recovery grid above the cut (α ∈ {0.70, 0.75, 0.80, 0.85, 0.90}) at the
  worst-case reachability N = 2000, to show *how* recovery degrades past 0.70.

---

## Result (re-read from `outputs/reachability-by-cell.csv`)

15 cells = **3 shapes** (`regnal_cluster`, `rise_and_fall`, `smooth_growth`) ×
**5 α** (0.70–0.90) × **N = 2000**, **30 replicates** per cell. Mean shape-recovery
rate by α:

| α_true | mean shape-recovery rate |
|---|---|
| 0.70 | 0.833 |
| 0.75 | 0.667 |
| 0.80 | 0.444 |
| 0.85 | 0.344 |
| 0.90 | 0.167 |

**Recovery declines gradually and shape-dependently above the cut** — mean 83 %
at α = 0.70 falling to 17 % at α = 0.90; `smooth_growth` holds to ~0.80,
`regnal_cluster` collapses by ~0.75–0.80. Only 1 of the 15 cells clears the full
binding `cell_pass` (rise_and_fall at α = 0.70). This is the evidence behind the
amendment's statement that **α ≤ 0.70 is the last broadly-reliable region**, with
a *gradual, shape-dependent* decline above it (not a cliff).

This result is lodged in **OSF Amendment 01 §A5.5.1** (operating-envelope bullet)
and underpins the "α ≤ 0.70" envelope cited in `continuity.md`.

---

## Provenance (anchored; NO code fabricated)

- **Generating commit:** `006a655` — *"feat(criterion): encode envelope
  finer-alpha + benign-divergence gate"* (Shawn Ross, 2026-06-04). Its body
  states verbatim: "fold in the 2026-06-04 finer-alpha run (alpha 0.70-0.90 at
  N=2000). Recovery declines gradually and shape-dependently above the cut (mean
  83% at 0.70 -> 17% at 0.90; smooth holds to ~0.80, regnal_cluster collapses by
  ~0.75-0.80)" and "**Commit the finer-alpha by-cell result; gitignore its
  logs/jsonl/scratch.**" — i.e. the by-cell CSV was committed deliberately and
  the generating script + logs + per-replicate JSONL were intentionally
  gitignored, not lost.
- **Code lineage:** the run used the recovery-grid two-unit fit harness
  (`runs/2026-05-26-recovery-grid-two-unit/code/fit.py`) under the
  **corrected convergence gate** introduced in the same commit `006a655`
  (`convergence_pass` = R̂ + bulk-ESS only; per-replicate `n_divergences == 0`
  auto-fail dropped, divergences assessed benign at grid level per
  Stan/Betancourt). The per-cell schema in the CSV (`shape_name, alpha_true, n,
  conv_rate, shape_rate, mean_abs_alpha_bias, band_cov95, n_reps, cell_pass`) and
  the per-replicate schema in the (untracked) JSONL (`cell_id, shape_name,
  alpha_true, n, replicate, pearson_r, abs_alpha_bias, max_rhat, n_divergences,
  band_cov95, w1, converged, shape_pass`) are the recovery-grid harness's own
  output schemas.
- **Compute:** sapphire, 2026-06-04 (per `continuity.md` 2026-06-04 marathon
  entry: "A finer-α run (sapphire, `runs/2026-06-04-envelope-finer-alpha/`)
  confirmed α ≤ 0.70 (gradual, shape-dependent decline above)"). n_jobs ≈ 14 was
  the host's settled parallelism for the recovery harness at that date.
- **Seed:** not separately recorded in the committed CSV; the recovery harness
  seeds per-replicate from the cell id (the `replicate` index in the JSONL). The
  by-cell CSV is the aggregate over 30 replicates per cell; the per-replicate
  R̂/r/bias are in the working-tree JSONL.
- **Reproduce:** re-run the recovery-grid two-unit harness
  (`runs/2026-05-26-recovery-grid-two-unit/code/fit.py` + the aggregation step)
  restricted to shapes {regnal_cluster, rise_and_fall, smooth_growth}, α ∈
  {0.70, 0.75, 0.80, 0.85, 0.90}, N = 2000, 30 replicates, under the corrected
  benign-divergence convergence gate (commit `006a655` onward). The committed
  CSV is the canonical result; the harness reproduces the same cell schema.

**Honest gap statement.** The *exact* generating driver script and the
per-replicate JSONL/logs for this specific sweep were intentionally not committed
(commit `006a655`), so this sweep is **not bit-reproducible from this dir alone**;
it is, however, fully **traceable** to the recovery-grid harness + the corrected
gate + the committed by-cell result, and its headline (the 83 % → 17 % gradual
decline) is re-derivable from the committed CSV and is quoted verbatim in the
generating commit and the lodged amendment.

---

## Outputs

`outputs/reachability-by-cell.csv` (the committed by-cell result — 15 cells; the
source for every number above); `outputs/reachability-records.jsonl` (per-replicate
records; present in the working tree, untracked per commit `006a655`).
Cross-refs: OSF Amendment 01 §A5.5.1/§A5.7 (the operating-envelope cut this
confirms); `runs/2026-05-26-recovery-grid-two-unit/` (the recovery-grid harness +
the corrected gate); commit `006a655` (generating + encoding commit);
`docs/notes/reflections/continuity.md` (2026-06-04 marathon entry).
