# Recovery-grid re-simulation under two unit choices — narrative spec

**Run directory:** `runs/2026-05-26-recovery-grid-two-unit/` (parent), with per-grid children `inscription-mass/` and `letter-mass/` plus a sibling `comparison/` for the cross-grid artefacts.
**Status:** spec — locked 2026-05-26; explicit go for sapphire launch authorised, triggered by completion of the 2026-05-26 Bayesian Mundlak three-variant fit (in flight, agent on sapphire).
**Authority:** binds the Stage 3 launch readiness check under the two-measure framework adopted 2026-05-26 (Obs 58; `runs/2026-05-26-letter-count-probe/spec.md`).
**Run-dir naming**: Obs 58 (commit `dd326dc`) referenced `runs/2026-05-26-recovery-grid-letter-mass/` as the anticipated path. The locked layout puts each grid's outputs under its own subdir (`inscription-mass/`, `letter-mass/`) inside the parent `recovery-grid-two-unit/`, with cross-grid artefacts under `comparison/`. The Obs's findable-later path resolves to `runs/2026-05-26-recovery-grid-two-unit/letter-mass/`.

## 1. Scope and motivation

The 2026-05-22 recovery-grid run (`runs/2026-05-22-recovery-grid-validation/`) FAILed the prereg binding criteria at 40.9 % cell pass-rate — well below the 90 % threshold. The 2026-05-24 diagnostic chain (Experiments A + B; F0 / F1 / F3 follow-ups, `runs/2026-05-24-*`) traced the failure to a structural likelihood ridge between α and shape complexity, biasing α toward the middle of its range. Two structural fixes emerged:

- **F1** sharper α prior — `Beta(1, 1)` (uniform, but tighter than the original loose prior) → Δα +0.025; not a prior-pull artefact.
- **F3** non-centred Gaussian-random-walk reparameterisation of `log p_gen` → Δα +0.001 *but* ESS gain of 45–50× on the slowest-mixing parameter; adopted unconditionally.

The 2026-05-26 letter-count probe (`runs/2026-05-26-letter-count-probe/`) then surfaced that inscription-count and letter-count are not rival operationalisations but complementary measures (Obs 58); both must be validated as recoverable for the two-measure Stage 3 framework to launch.

**This artefact pins two head-to-head grids:**

1. **Grid A — inscription-mass:** matches the 2026-05-22 cell design with the F1 + F3 structural fixes folded in. Each inscription deposits unit mass (weight = 1.0).
2. **Grid B — letter-mass conservative:** identical cell design with F1 + F3, but each inscription deposits letter-mass drawn from the empirical post-filter LIRE distribution of `letter_count_conservative`.

The head-to-head verdict (both pass / only A passes / only B passes / both fail) determines the Stage 3 launch path per §5 below.

## 2. What this artefact pins

Carries forward from `runs/2026-05-22-recovery-grid-design/spec.md` unless flagged. **The cell design (axes, shapes, tier vectors, sample sizes, replicate count, seed policy) is identical between Grid A and Grid B** so that any verdict difference is attributable to the unit-of-analysis swap, not to design drift.

Deltas from 2026-05-22:

- **Two grids instead of one** — added.
- **F1 + F3 structural fixes** — baked into the harness for both grids.
- **Letter-count weight distribution** (Grid B only) — new pin; §3.4 below.
- **Tier-vector `pilot_proxy` for Grid B** — re-anchored to letter-mass endpoint frequencies (must be re-derived pre-launch; §3.3).
- **Per-grid `base_seed`** values to keep stochastic streams disjoint; §3.5.
- **Cross-grid comparison artefacts** — new; §4.
- **Outcome branching** that informs Stage 3 launch — new; §5.

Unchanged from 2026-05-22:

- α grid: `{0.05, 0.30, 0.50, 0.70, 0.95}` (5 values).
- Genuine-shape library: 6 shapes (`flat_baseline`, `smooth_growth`, `smooth_decline`, `rise_and_fall` µ=150 σ=60, `bimodal` µ₁=50 σ₁=40 µ₂=250 σ₂=40 mix=0.5, `regnal_cluster` with spikes at AD 77.5 / 122.5 / 212.5).
- Sample sizes (N inscriptions per replicate): `{2000, 10000, 50000}`.
- Replicates per cell: 100.
- Five tier vectors per grid: `uniform`, `century_heavy`, `half_century_heavy`, `reign_heavy`, `pilot_proxy`.
- Binding criteria: ≥ 90 % of cells pass coverage AND posterior-median Pearson r ≥ 0.95 in ≥ 90 % of cells (prereg §4 lines 333–334).
- Envelope: 50 BC – AD 350; 80 bins at 5 y width.
- Total cells per grid: 5 × 6 × 5 × 3 = **450 cells**, **45,000 fits per grid**, **900 cells / 90,000 fits across both grids**.

## 3. Design specifics

### 3.1 Structural fixes baked into the harness (both grids)

The 2026-05-22 harness has been refactored in-session-but-not-yet-committed at `runs/2026-05-24-followup-experiments/`. For this run:

- **F1** — `alpha ~ Beta(1, 1)` prior (replaces the looser 2026-05-22 prior).
- **F3** — non-centred GRW reparameterisation on `log p_gen[1:80]`:
  ```
  innovations ~ Normal(0, 1)  # shape (79,)
  log_p_gen_raw[0] ~ Normal(0, 1)
  log_p_gen_raw[1:] = log_p_gen_raw[0] + cumsum(sigma_grw * innovations)
  p_gen = softmax(log_p_gen_raw)
  ```
  versus the 2026-05-22 centred form. ESS gain 45–50× on the slowest-mixing parameter.

These are the only model-spec changes from 2026-05-22. **No other priors, sampling settings, or likelihood structures change.** NUTS settings: 4 chains × 2,000 draws × 1,000 tune, `target_accept = 0.95`.

### 3.2 Synthetic data generation under each unit

**Grid A (inscription-mass):** identical to 2026-05-22. Each replicate draws N samples from the mixture `α × p_conv + (1 − α) × p_gen`; bin-count vector is the multinomial histogram. Each sample contributes 1 count to its bin.

**Grid B (letter-mass conservative):** each replicate draws N samples from the mixture. Each sample i is independently assigned a `letter_count_i` drawn iid from the empirical letter-count distribution (§3.4). The bin-count vector is:
```
count[b] = Σ_{i assigned to bin b} letter_count_i
```
counts are integer-valued; the NegativeBinomial likelihood handles the heavier per-bin variance via its dispersion parameter (α_disp, NOT the mixture α).

### 3.3 Tier vectors

Four of five vectors are unit-independent (the corpus-level claim about template structure does not require a unit choice): `uniform` (1/3, 1/3, 1/3), `century_heavy` (0.70, 0.20, 0.10), `half_century_heavy` (0.20, 0.70, 0.10), `reign_heavy` (0.20, 0.10, 0.70).

**`pilot_proxy` differs between grids:**

- Grid A (inscription-mass): `(0.55, 0.30, 0.15)` — the 2026-05-22 value, anchored on inscription-endpoint frequencies (54.5 % `not_before` `01`, 53.0 % `not_after` `00`, Decision 17 lines 1314–1316). Recorded in `inscription-mass/data/pilot-proxy.json` at launch for record-preservation symmetry with Grid B.
- Grid B (letter-mass conservative): **TBD — must be re-derived pre-launch.** A short pre-launch script (~ 30 min) reweights the endpoint-frequency descriptive by `letter_count_conservative` and emits the corresponding three-tier vector. Locked at launch; recorded in `letter-mass/data/pilot-proxy.json`.

Flagged caveat (carried from 2026-05-22): both `pilot_proxy` vectors are descriptive-frequency proxies, not draws from a posterior. Replace with actual posterior draws when a pilot fit becomes available.

### 3.4 Letter-count distribution (Grid B only)

**Empirical source:** `runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet`, column `letter_count_conservative`. 180,609 rows; summary: median 25, mean 45.4, max 35,537; 2.2 % zero-count rows.

**Pin:** for each inscription i in a Grid B replicate, draw `letter_count_i` iid from the empirical distribution **with no cap** (the long tail is real epigraphic-cultural signal — monumental dedications, civic decrees — and capping would systematically remove the very inscriptions that drive the letter-mass story).

**Critical-friend note flagged for surfacing in the report:** the 99th-percentile letter-count is ~ 450; the maximum is ~ 35,000. A handful of mega-inscriptions per replicate (at N=50,000) will dominate a few bins. If identifiability is meaningfully affected by this heavy tail (per-cell variance blowup observable in the smoke test), a sensitivity run with 99th-percentile capping should be considered — but is **not** baked into this artefact.

**Pre-launch sanity check** (§5 below): the synthesised bin-count vector under letter-mass should show a Pearson r ≥ 0.85 with the corresponding inscription-mass bin-count vector on a one-cell smoke test. If not, the data-generation logic has a bug.

### 3.5 Seed policy

`base_seed_A = 20260526` (Grid A inscription-mass; today's date).
`base_seed_B = 20260527` (Grid B letter-mass; offset by 1 day for stream disjointness).
Within each grid: `cell_seed = base_seed + cell_index`, where `cell_index` enumerates deterministically over (shape × ascending α × ascending tier-vector index × ascending N).
Within each cell, replicate r uses `cell_seed * 1000 + r` for the multinomial draw.
For Grid B's letter-count draws: `cell_seed * 1000 + r + 999_000_000` (large additive offset to keep the multinomial-draw and letter-count-draw streams disjoint).

## 4. Expected outputs

Directory layout (locked 2026-05-26):

```
runs/2026-05-26-recovery-grid-two-unit/
├── spec.md                                          # this file
├── code/                                            # shared harness; parametrised by --unit {inscription,letter}
├── inscription-mass/
│   ├── data/pilot-proxy.json                        # tier vector at launch
│   ├── data/synthetic-cells/<cell_id>/replicate_<i>.parquet
│   └── outputs/
│       ├── cell-fits/<cell_id>/replicate_<i>-posterior.parquet
│       ├── cell-summaries/<cell_id>-summary.json
│       ├── tables/grid-summary.parquet              # cell-level pass / fail flags + headlines
│       ├── figures/
│       └── REPORT.md                                # binding-criterion verdict + alpha-bias systematics
├── letter-mass/
│   ├── data/pilot-proxy.json                        # re-derived for letter-mass at launch (§3.3)
│   ├── data/synthetic-cells/<cell_id>/replicate_<i>.parquet
│   └── outputs/  (same shape as inscription-mass/outputs/)
└── comparison/
    ├── cell-pass-comparison.parquet                 # per-cell pass-or-fail pairs across grids
    ├── figures/
    │   ├── fig-pass-rate-heatmap.png                # side-by-side (α × shape) heatmaps; same colour scale
    │   └── fig-alpha-bias-by-tier.png               # F0 systematics extended to two units
    └── COMPARISON-REPORT.md                         # head-to-head writeup driving §5 outcome branching
```

`cell-pass-comparison.parquet` filter views: **both-pass** (the good case), **A-passes-B-fails** (letter-mass identifiability problem), **B-passes-A-fails** (inscription-mass identifiability problem), **both-fail** (still need structural rethink).

## 5. Decision rule and outcome branching

**Per-grid binding criterion (unchanged from 2026-05-22):** the mixture is validated for that unit choice if (a) ≥ 90 % of cells pass coverage AND (b) the posterior-median Pearson r is ≥ 0.95 in ≥ 90 % of cells.

**Cross-grid outcome branching:**

| Grid A (inscription) | Grid B (letter) | Stage 3 launch path |
|----------------------|-----------------|---------------------|
| PASS | PASS | **Launch Stage 3 under both units in parallel** (the planned two-measure framework). The delta becomes a third output. |
| PASS | FAIL | Letter-mass calibration cohort lacks identifiability. Investigate: (i) is the heavy-tail letter-count distribution the cause? Try a 99th-pct cap as sensitivity. (ii) Is the calibration cohort itself too small under letter-mass? Stage 3 launches under inscription-mass only; letter-mass reported as limitation. |
| FAIL | PASS | Inscription-mass identifiability problem persists despite F1 + F3 fixes; the 2026-05-22 finding generalises. Stage 3 launches under letter-mass only; inscription-mass reported as limitation. (A structural-pivot-ii diagnostic chain is triggered if both H3a and H3b need inscription-mass.) |
| FAIL | FAIL | Both unit choices fail. **Stage 3 cannot launch under the current methodology.** Trigger a second diagnostic chain analogous to 2026-05-24's, applied to the two-grid failure pattern. Likely need: structural model revision (the F1 + F3 fixes proved insufficient under both units), prior re-derivation, or a methodological pivot beyond the calibration-cohort empirical-Bayes design. |

**Reporting requirement under any FAIL outcome:** the COMPARISON-REPORT must localise the failure to specific cells (which α / shape / tier combinations) and propose at least one diagnostic experiment that would discriminate among candidate explanations. No silent "good enough" verdicts.

**Wasserstein-1 reporting:** supplementary distribution-sensitive shape evidence (prereg §3 line 210). Reported per cell; not part of the binding rule (still deferred per the 2026-05-22 spec's §6).

## 6. Cost estimate

**Per grid (matching 2026-05-22 post-SMT-aware-config benchmark):** 450 cells × 100 replicates = 45,000 fits; ~ 30 h sapphire wall-clock under SMT-pinned `n_jobs=12 + taskset -c 0-11`.

**Two grids sequential:** ~ 60 h wall-clock. No API spend.

**TMPDIR redirect mandatory** per 2026-05-23 learned-lesson: set `TMPDIR=~/cc-scratch/inscriptions-recovery-grid-two-unit/pytensor-tmp/` (mkdir -p before launch). Tmpfs `/tmp` has a 1,048,576-inode ceiling that pytensor recompiles can blow through; disk-backed scratch is mandatory.

**Resumability:** per-cell checkpointing (matches 2026-05-22 design). If sapphire is rebooted mid-grid (note: standing rule forbids actively rebooting sapphire, but power events are not under our control), the grid resumes from the last completed cell.

**Outcome wall-clock — for prioritisation:**

- Both PASS or one PASS: Stage 3 launch decision in ~ 60 h.
- Both FAIL: ~ 60 h + diagnostic chain (likely 2–5 days analogous to 2026-05-24 chain) = 1–2 weeks before Stage 3 launch.

## 7. Pre-launch checks (critical-friend gates)

Before launching the production grids on sapphire, the harness MUST pass these checks:

1. **Smoke test per grid** — one cell each (cell_id = `shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000`); 5 replicates; full pipeline including fit + posterior summary. Both grids' smoke tests must converge (R-hat < 1.01, no divergences).
2. **Bin-count-vector sanity** (Grid B) — one synthetic replicate at N=10,000; check that the letter-mass bin-count vector has Pearson r ≥ 0.85 with the inscription-mass bin-count vector on the same mixture (modulo letter-count weighting). If r < 0.85, the data-generation logic has a bug.
3. **Empirical letter-count distribution sanity** — re-confirm post-filter median ~ 25, mean ~ 45, max ~ 35K; this matches Block 1 of the 2026-05-26 letter-count probe.
4. **`pilot_proxy` re-derivation for Grid B** — script emits `data/pilot-proxy-letter-mass.json`; vector sums to 1.0; entries in [0, 1].
5. **SMT-pinning verified** — `nproc` shows 24; `taskset -c 0-11` confirmed on launch; `n_jobs=12` set; `PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False` set.
6. **TMPDIR redirect verified** — `~/cc-scratch/inscriptions-recovery-grid-two-unit/pytensor-tmp/` exists, is writable, on disk-backed mount with ≥ 5 GB free.
7. **F1 + F3 fixes verified in harness** — code inspection or unit test confirming the Beta(1,1) prior and the non-centred GRW are active.

If any gate fails, HALT and report. Do not silently relax.

## 8. Authority and amendment status

**OSF-amendment status:** this re-simulation is methodological development / identifiability diagnostic. **No OSF amendment is required before launch** per the standing rule (2026-05-26 memory `2026-05-26-40ce5927fddc`). The eventual two-measure-framework amendment (to be batched with the post-Martin reframe of D19/D21/D23/D25) will reference this artefact as supporting empirical record.

**Authority over Stage 3 launch:** the COMPARISON-REPORT's verdict (per §5) is binding on the Stage 3 launch path. Shawn must explicitly sign off on the launch path before Stage 3 implementation begins. The amendment-gate rule (memory `2026-05-26-40ce5927fddc`) applies between recovery-grid completion and Stage 3 confirmatory-claim-producing work.

## 9. Cross-references

- `runs/2026-05-22-recovery-grid-design/spec.md` — predecessor; this spec inherits its design discipline.
- `runs/2026-05-22-recovery-grid-validation/` — the FAIL run that motivated the diagnostic chain.
- `runs/2026-05-24-followup-experiments/` — F1 + F3 derivation; structural fixes baked in here.
- `runs/2026-05-26-letter-count-probe/` — the probe that surfaced the two-measure framework.
- `runs/2026-05-26-letter-count-probe/spec.md` — the binary-verdict spec being reframed.
- `planning/h2.1-stage-3-implementation-plan-2026-05-25.md` — downstream consumer; updated to reflect two-unit parallel after this run completes.
- `docs/notes/reflections/working-notes.md` Obs 58 — the "acts vs content" reframe (commit `dd326dc`).
- `docs/notes/reflections/continuity.md` §"Martin Eftimoski consultation outcome — recalibration (2026-05-26)" — the Martin nudge.
- Memory `2026-05-26-40ce5927fddc` — amendment-gate standing rule.
- Decision 21 (recovery-grid procedural pre-commitment) — the prereg authority over recovery-grid design.

## 10. Locked decisions (2026-05-26)

All sign-off items below were resolved with Shawn on 2026-05-26:

1. **Directory layout** — `runs/2026-05-26-recovery-grid-two-unit/` is the parent; per-grid children `inscription-mass/` and `letter-mass/`; cross-grid artefacts under `comparison/`. (See §4 for the full layout.)
2. **Letter-count distribution** — uncapped. The heavy tail is real epigraphic-cultural signal (monumental dedications, civic decrees); capping would systematically remove the inscriptions that drive the letter-mass story. A capped sensitivity run is a follow-up if the uncapped run reveals identifiability problems traceable to the tail.
3. **Smoke-test cell** — `shape=rise_and_fall_alpha=0.50_tier=uniform_N=2000`, same as the 2026-05-22 smoke-test cell.
4. **Sapphire launch authorisation** — granted, with the explicit trigger **"as soon as the currently-running Bayesian Mundlak three-variant fit completes"** (the agent in flight on sapphire as of spec-locking). Wall-clock estimate ~ 60 h sequential under the SMT-pinned config.
5. **Paper-figure status of comparison artefacts** — yes; the cross-grid `fig-pass-rate-heatmap.png` and `fig-alpha-bias-by-tier.png` are paper-figure candidates. The two-measure validation IS the methodological contribution and warrants direct visual presentation in the paper.
