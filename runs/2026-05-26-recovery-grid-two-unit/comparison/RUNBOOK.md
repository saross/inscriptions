# Completion runbook — two-unit recovery grid → Stage-3 decision

**Owner:** next CC instance (or Shawn) at Grid B completion (~3 June 2026).
**Status (2026-06-02):** Grid A (inscription-mass) COMPLETE and adjudicated —
**FAIL** (see `../inscription-mass/outputs/REPORT.md`). Grid B (letter-mass)
RUNNING on sapphire (PID 931910), ~3 June ETA. The comparison harness is
BUILT and smoke-tested (A-vs-A) against Grid A's real 450-cell outputs, so it
is one-command-ready.

---

## When Grid B finishes (`GRID-B-END rc=0` in `STATUS.txt`)

1. **Confirm a clean finish on sapphire:**
   `tail STATUS.txt` → expect `GRID-B-END rc=0`; confirm `failed=0` in the last
   `letter progress` line of `nohup.out`.

2. **`git pull` on sapphire** — now safe (grid done; *never* mid-run). Brings
   `grid-summariser.py`, `compare-grids.py`, `finalise-comparison.sh`
   (`collect-alpha-bias.py` was shipped 2026-06-02). If the pull is blocked by
   untracked Grid A cell-summary JSONs (byte-identical to what is being
   adopted), they are safe to remove first:
   `git -C ~/Code/inscriptions clean -n runs/2026-05-26-recovery-grid-two-unit/inscription-mass/outputs/cell-summaries`
   to preview, then drop the `-n`. (Their content is already preserved in the
   committed `grid-summary.parquet`.)

3. **Run the finaliser on sapphire** (data-local; `.venv` python, no `uv` sync):
   ```bash
   bash runs/2026-05-26-recovery-grid-two-unit/code/finalise-comparison.sh
   ```
   Writes each grid's `outputs/REPORT.md` + `tables/{grid-summary,alpha-bias}.parquet`,
   and `comparison/` (`cell-pass-comparison.parquet`, two figures,
   `COMPARISON-REPORT.md`).

4. **Pull `comparison/` + the letter-mass tables back** to a local host for the
   record, and commit.

5. **Read `comparison/COMPARISON-REPORT.md`:** §1 per-grid verdicts, §1b
   flat-excluded diagnostic, §2 four-way classification, §3 failure
   localisation, §6 methodology note. The report names the spec §5 outcome
   branch and the **recommended** Stage-3 path.

6. **Only then — the deliberate sapphire pymc-6 upgrade** (`uv sync --frozen`;
   see `PROVISIONING.md`). Verify `arviz >= 1.x` can read the §5 arviz-1.1 `.nc`
   before any Layer B work on sapphire.

---

## HARD GATES (do not skip)

- **OSF Amendment 01 must be lodged before ANY Stage-3 confirmatory work.**
  Even a both-PASS verdict yields only a *recommended* launch path, not a
  launch (standing rule; memory `2026-05-26-40ce5927fddc`). **As of
  2026-06-02, Amendment 01 is NOT lodged.**
- **Grid A already FAILs as-written** (coverage 69.8%, shape-r 70.2%, both
  42.7%). The realistic outcome space is FAIL/FAIL or letter-only-PASS.
- **flat_baseline Pearson-r artefact:** criterion (b) is undefined for the
  constant-truth shape (zero variance), so it caps shape-pass at 83.3% for
  *both* units, independent of model quality (documented in
  `runs/2026-05-24-followup-systematics/`). A criterion clarification —
  exclude undefined-r cells, or substitute Wasserstein-1 for the flat case —
  belongs in Amendment 01, with Shawn + statistician sign-off. The harness
  applies the criterion **as currently written** and also reports the
  flat-excluded diagnostic view.

---

## ⚠ Criterion superseded (2026-06-02) — read before adjudicating

The harness (`grid-summariser.py`, `compare-grids.py`) currently computes the
**lodged** binding criterion (exact 95%-CI α-coverage + Pearson *r* ≥ 0.95).
That criterion has been **superseded** by the metric correction in **OSF
Amendment 01 §A5.5.1** (drafted 2026-06-02; see
`planning/osf-amendment-2026-05-29-two-measure-framework.md` and the evidence at
`planning/prior-art-scout-2026-06-02-recovery-validation-metrics.md`):

- **Shape gate (hybrid):** Pearson *r* ≥ 0.95 for non-flat shapes (unchanged);
  Wasserstein-1 ≤ T_flat = 10 y for the flat shape (Pearson undefined there).
- **Convergence precondition** made explicit (≥90% replicates, R̂ < 1.01).
- **α demoted** from binding gate to a quantified diagnostic (90th-pct |bias|
  ≈ 0.18).
- **Operating-envelope reframe:** gate evaluated for α ≤ 0.70; α ≥ 0.95 reported
  as stress sensitivity. Grid A preview under the corrected criterion: **91.9%
  PASS** in the operating envelope (vs 42.7% under the lodged criterion).

**Therefore:** the harness output is the *old-criterion reference*. Before the
headline two-grid adjudication, **update the harness to the §A5.5.1 criterion**
(the next coding step; W1 and α intervals are already stored, so no re-fit) —
and only after the amendment's α-diagnostic operationalisation has Martin's
draft-stage sign-off. Run both old and corrected for transparency.

## What was done 2026-06-02 (already committed)

- **Grid A verdict:** FAIL. `REPORT.md` + `grid-summary.parquet` +
  `alpha-bias.parquet` committed. Genuine identifiability problem localised:
  36 cells with α-coverage = 0.00 (CI never covers true α), concentrated in
  regnal_cluster (24) + bimodal (12) at large N — the α/shape-complexity
  likelihood ridge; F1+F3 reduced but did not eliminate it.
- **Harness** (smoke-tested A-vs-A): `grid-summariser.py`,
  `collect-alpha-bias.py`, `compare-grids.py`, `finalise-comparison.sh`.
