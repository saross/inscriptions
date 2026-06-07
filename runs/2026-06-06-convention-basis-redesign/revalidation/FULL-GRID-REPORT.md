# Full-grid recovery re-validation — REPORT (DRAFT SKELETON)

**Status:** DRAFT SKELETON written 2026-06-07 while the full grid runs
(sapphire PID 1681813, ~150/450 at scaffold time, 0 failed). Every
verdict-dependent value below is an explicit `[PENDING]` placeholder — **do not
quote any number from this file until the grid has finished and the summariser
has been run.** This scaffold exists so the post-grid scoring + amendment/spec
fill is mechanical (fill-in-the-numbers), not so the verdict can be pre-judged.

**Author:** Claude Code (Opus 4.8) on Shawn Ross's brief.
**Design:** `runs/2026-06-06-convention-basis-redesign/design.json`
(`tier_basis_empirical`, Option 2; Decision 38).
**Predecessor:** `STAGE1-TRIAGE-REPORT.md` (Stage-1 stress-triage, PASS, 2026-06-06).

---

## 0. Scoring runbook (run these, in order, once the grid EXITS)

The grid is finished when `grid-state.json` has `finished_at != null` **and**
`len(completed_cells) == 450` **and** `failed_cells == []`. Verify first:

```bash
ssh sapphire 'cd ~/Code/inscriptions/runs/2026-06-06-convention-basis-redesign; \
  python3 -c "import json; d=json.load(open(\"revalidation/inscription-mass/outputs/grid-state.json\")); \
  print(\"finished:\", d[\"finished_at\"], \"completed:\", len(d[\"completed_cells\"]), \"failed:\", len(d[\"failed_cells\"]))"'
```

Then score (note: `--assert-grid-a-regression` is **OFF** by default and must
STAY off — this is a *new* basis, so the Grid-A 98.6 % figure is a reference
delta, not a pass target; the regression hard-abort was scoped to opt-in on
2026-06-07 precisely for this run):

```bash
ssh sapphire 'cd ~/Code/inscriptions/runs/2026-06-06-convention-basis-redesign/revalidation; \
  ~/.local/bin/uv run python code/grid-summariser.py \
    --grid-dir inscription-mass'
```

This writes `inscription-mass/outputs/REPORT.md` (the auto-tables) and
`inscription-mass/outputs/tables/grid-summary.parquet`, and prints the headline.
**The auto-`REPORT.md` is the source of every number below.** This
hand-written file wraps it with interpretation, the envelope read, the
recommendation, and the amendment/spec field-mapping.

**Extra step the summariser does NOT do — the α ±precision (Bland–Altman LoA).**
Launch-spec §7 line 147 wants the α limits-of-agreement (cf. Decision 33's
±0.18). The cell-summary JSON stores `alpha_coverage`, not the recovered-α draws,
so the LoA must be computed from the in-envelope per-replicate posteriors
(α ≤ 0.70 cells) on sapphire. Either (a) compute the in-envelope mean α-bias ±
1.96·SD of (α̂ − α_true) across replicates, or (b) if that analysis is deferred,
quote Decision 33's ±0.18 as the reference LoA and state that the new-basis LoA
is reported in a follow-up. Decide at fill time; flag which was used.

---

## 1. Headline verdict — `[PENDING]`

Binding criterion = Amendment 01 §A5.5.1 (corrected): convergence precondition
(≥ 90 % replicates pass R̂ < 1.01 ∧ bulk-ESS ≥ 400) + hybrid shape gate
(median Pearson r ≥ 0.95 non-flat; Wasserstein-1 ≤ 10 y for `flat_baseline`),
α-coverage demoted to a shape-conditioned **diagnostic**, evaluated within the
operating envelope (α ≤ 0.70); ≥ 90 % of in-envelope cells must clean-pass.

- **Verdict: `[PENDING — PASS / FAIL]`.**
- **Headline B (binding):** `[PENDING]` % of in-envelope cells clean-pass
  (`[PENDING n_clean]/[PENDING n_envelope]`), against the ≥ 90 % bar.
- **Diagnostic A:** `[PENDING]` % shape-pass among convergence-eligible
  in-envelope cells.
- **Basis-shift vs Grid A:** Grid-A headline was 98.6 %; this basis is
  `[PENDING]` % (Δ `[PENDING]`). Informational — *not* a regression target.
- **Convergence-excluded in-envelope cells:** `[PENDING]` (by shape: `[PENDING]`).
- **Stress row (α ≥ 0.95, never gated):** shape-pass `[PENDING]` %.

> If FAIL: **halt** — do not lodge Amendment 03 or launch H2.1. Diagnose which
> axis fails (see §2) and report to Shawn. A FAIL most plausibly localises to the
> multi-century-heavy tier or the peaked-genuine shapes at small N (the
> Decision-38 §6 fear); characterise it, do not negotiate the criterion.

## 2. Shape-recovery map (the per-axis pattern) — `[PENDING]`

Lift the four per-axis tables verbatim from the auto-`REPORT.md` §2 (pass rates
by **alpha**, **shape**, **tier_weights**, **N**). This is the "shape-recovery
map" Amendment 03 §A5.5 Stage-2 asks for. Key reads to extract:

- **By α:** confirm clean-pass is high across α ≤ 0.70 and degrades only at α ∈
  {0.95} (expected — outside envelope). `[PENDING table]`
- **By tier_weights:** confirm `multicentury_heavy` is not a systematic failure
  (the §6 fear) within the envelope. `[PENDING table]`
- **By shape:** confirm peaked shapes (`bimodal`, `regnal_cluster`) recover
  within the envelope; note any small-N caveat. `[PENDING table]`
- **By N:** note the large-N α-coverage collapse is benign (diagnostic only).
  `[PENDING table]`

## 3. Operating envelope (α ≤ 0.70) — `[PENDING]`

State the demonstrated reportable envelope. The spec sets N ≥ 2 000 ∧ posterior
α ≤ 0.70. Confirm from the map whether α ≤ 0.70 is the right ceiling or whether
the data support tightening/loosening it. `[PENDING — confirm or adjust; this is
the value launch-spec §7 line 133–135 consumes]`

## 4. Interpretation — `[PENDING]`

Does the full grid corroborate the triage's resolution of the Decision-38 §6
fear (multi-century plateau attributed to convention, not confused for genuine
quiescence) at scale and across shapes? `[PENDING prose, grounded in §2]`

## 5. Recommendation — `[PENDING]`

`[PENDING — on PASS: proceed to fill Amendment 03 §A5.5 + launch-spec §7, lodge,
sign off, launch. On FAIL: halt + diagnose.]`

## 6. Artefacts

- Auto-tables + parquet: `inscription-mass/outputs/REPORT.md`,
  `inscription-mass/outputs/tables/grid-summary.parquet`.
- Per-cell summaries: `inscription-mass/outputs/cell-summaries/` (450 cells).
- Grid state: `inscription-mass/outputs/grid-state.json`.
- Per-replicate posteriors: on sapphire (for the α LoA step).
- Stage-1 triage: `STAGE1-TRIAGE-REPORT.md`.

---

## 7. Downstream field-mapping (post-PASS fill templates)

Copy these into the two target files once §1–§5 are filled. Placeholders map 1:1
onto §1–§3 above.

### 7a. → Amendment 03 §A5.5 Stage-2 bullet
File: `planning/osf-amendment-2026-06-07-convention-basis.md` (line ~174).
Replace the `[PENDING — PID 1681813; …]` bullet with:

> - **Stage-2 full grid: `[PASS/FAIL]`** (450 cells, 0 failed; sapphire). Headline
>   B `[X]` % of in-envelope (α ≤ 0.70) cells clean-pass (convergence AND shape),
>   against the ≥ 90 % bar; diagnostic A `[Y]` %. The multi-century-heavy tier
>   `[does not / does]` systematically fail within the envelope — the §6
>   plateau-confusion failure mode is `[absent / present]` at scale. Shape recovery
>   holds for peaked genuine signals within the envelope `[caveat at small N if
>   any]`. Basis-shift vs Grid A: `[Δ]`. REPORT:
>   `runs/2026-06-06-convention-basis-redesign/revalidation/FULL-GRID-REPORT.md`
>   (+ auto-tables `inscription-mass/outputs/REPORT.md`).

Then flip the YAML `status:` and the `skeleton-note:` to reflect §A5.5 filled.

### 7b. → Launch-spec §7
File: `runs/2026-06-07-h2.1-launch-prep/launch-spec.md`.

- **Line ~134–135 (envelope):** replace `[CONFIRM from the full-grid REPORT…]`
  with the demonstrated envelope from §3 (e.g. "confirmed: N ≥ 2 000 ∧ posterior
  α ≤ 0.70; clean-pass `[X]` % within it").
- **Line ~147 (α ±precision):** replace `[CONFIRM from REPORT; cf. Decision 33's
  ±0.18]` with the new-basis α LoA from the runbook §0 extra step, OR retain
  Decision 33's ±0.18 as the cited reference with a note that the new-basis LoA
  follows. State which.
- Tick §10 pre-launch boxes: re-validation PASS (line 178); §7 filled (line 181).

### 7c. → Continuity + Decision log
- Continuity frontmatter + a new session-history entry: verdict, REPORT path,
  amendment lodged, sign-off, launch.
- Decision 38 in `planning/decision-log.md`: append the re-validation outcome.
