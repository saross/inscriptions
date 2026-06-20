# Recovery utility-check — spec + results pointer

**Status:** ✅ EXECUTED 2026-06-02 (band calibration) / 2026-06-04 (interpretation).
This spec was reconstructed 2026-06-20 (results-documentation uplift, Tier-2
item 7): the run had genuine results but **no in-directory markdown** — every
finding was externalised to the Observations register (with re-verifiable
artefact paths). This file gives the run a root-level Status banner and points to
where the findings are lodged.

## What this run did

Two post-recovery-grid utility diagnostics for the H2.1 deconvolution:

1. **`code/band-calibration.py`** — does the recovered genuine-SPA (`p_gen`)
   **credible band** have honest coverage? The 2026-05-26 recovery grid validated
   `p_gen` *shape* recovery (Pearson r) but stored only the posterior *median*
   curve, not the per-bin band. This re-fits a representative subset of
   operating-envelope cells (12 cells × 30 reps = 360 fits, `n_jobs=16`),
   extracts the per-bin `p_gen` posterior, and measures pointwise 95 % credible-
   band coverage. Run log: `outputs/band-cal.log`.
2. **`code/real-corpus-convention-fraction.py`** — where does the **real** LIRE
   corpus sit relative to the recovery model's operating envelope (α ≤ 0.70)? A
   descriptive computation of the corpus convention-mass fraction over time.

## Outputs

- `outputs/band-calibration-by-cell.csv`, `outputs/band-calibration-replicates.parquet`
- `outputs/band-cal.log`
- `outputs/convention-fraction-by-bin.csv`, `outputs/convention-fraction-over-time.png`

## Where the findings are lodged (Observations register)

The results live in `docs/notes/working-notes.md`, each with re-verifiable
artefact anchors:

- **Obs 68** — the recovered genuine-SPA credible band: coverage limitation.
- **Obs 69** — the real corpus's convention-fraction trajectory (AD ~142–347 is
  in the degraded-recovery zone); provenance / limitation.
- **Obs 73** — why the band/coverage and corpus-α results are interpreted as they
  are (methodology / interpretation).

(Obs 67 — the Grid A 98.6 % recovery PASS — is the upstream validation this run
follows on from, not a finding generated here.)
