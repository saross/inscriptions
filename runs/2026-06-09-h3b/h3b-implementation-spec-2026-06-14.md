# H3b deviation-detection — build-ready implementation + run spec (2026-06-14)

**Status:** EXECUTED (2026-06-15) — base run complete, see `REPORT-drawwise-2026-06-15.md`.
Supersedes the 2026-06-09 draft (`h3b-spec.md`). **Post-run resolutions:** the §1
table's **OQ-5 ("null fit to raw")** was corrected at run time — for the CPL null,
fit-to-raw saturates the probe windows; the informative null fits the **observed
corrected** curve (D1, standard SPD), per
`DECISION-NEEDED-null-construction-2026-06-14.md`. The global test is reported as a
saturated gate (D2; large-N over-power) with the probe-window P(deficit) as the
deliverable; exp is a labelled saturated cross-check (D3); the large-N correction +
baorista null are a deferred robustness annex.
**Date:** 2026-06-14.
**Author:** Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief.
**Run dir:** `runs/2026-06-09-h3b/`.
**UK/Australian English; Oxford comma.**

---

## 0. What this document is

The 2026-06-09 draft (`h3b-spec.md`) was written **before** the cc-library
remediation and **OSF Amendment 04** (lodged 2026-06-14, tag
`osf-amendment-04-2026-06-14` → commit `61c954c`). Amendment 04 §A5.6 changed the
H3b design in one decisive way — it **replaced the post-hoc α-identifiability
*restriction* with propagation of the deconvolution uncertainty into the
(exploratory) H3b deviation test** — and it corrected the production source. This
spec folds that pivot and Shawn's 2026-06-14 design decisions into a build-ready
plan. The draft's method skeleton (forward-fit null, Timpson envelope, probe
windows, reuse map) is retained; the *observed signal* and the *reporting* change.

---

## 1. Decisions locked (2026-06-14 session) and their authority

| Topic | Locked decision | Authority |
|---|---|---|
| Confirmatory status (OQ-1) | **Exploratory**; no Holm-corrected confirmatory family. Holm reported **descriptively** as a multiplicity diagnostic only. | Prereg; Decision 15; Amdt 04 §A5.6 |
| Identifiability restriction (OQ-2) | **Moot.** No identifiable-set / threshold. Reliability is carried by **uncertainty propagation** + a soft annotation. | Amdt 04 §A5.6 |
| **Production source** | The **cc-library refit** (`runs/2026-06-13-cc-production-refit/`), **not** the stale `2026-06-07-h2.1-launch-prep` pointer in the draft §3.1. | Amdt 04 (reverses A03 shared basis) |
| **Observed signal** | The genuine-SPA **posterior** (8,000 draws/unit), not the posterior-median. The refit currently emits only the median → must be re-run to persist draws (§4, Stage A). | Amdt 04 §A5.6; this session |
| **Aggregation** | **Marginal global-*p* = headline** (mean over draws of the per-draw Timpson global-*p*); **P(deviation) = `P(global-p<0.05)` companion**; **per-draw *p* spread** as the uncertainty diagnostic. | This session |
| Scan scope (OQ-8) | **All 29 units** + the prereg-named probe scopes (empire; Western-Empire-provincial = `latin-aggregate`). Per-unit results beyond the named scopes labelled **exploratory-extra**. | This session |
| Test direction (OQ-7) | Global test **two-sided** (excursions either way); at the named probes also report **signed direction + one-sided deficit posterior probability**. | This session |
| CPL null (OQ-4) | **Exp primary** (fully forward); **CPL-3 labelled secondary cross-check** on the existing smeared-fit sampler. Forward-CPL sampler **deferred**. | This session |
| Null construction (OQ-5) | Null fit to raw `[nb,na]` **intervals** (fixed across draws); envelope compares each posterior draw × **fixed** `n_eff`. | This session |
| Antonine subsets (OQ-6) | **Deferred** (Asclepius / military not built). Antonine runs at empire + per-unit on existing corrected SPAs. | This session; Amdt 04 |
| Reachability (OQ-3) | **Per-unit annotation, not exclusion.** Flag units below the cpl-3-Gaussian province floor 1,618 (e.g. Lusitania N≈1,578) on their CPL result. | This session |
| Coverage caveat (§A5.5) | **Carry the caveat** (cc CIs ~1σ-optimistic); optional small posterior-spread **inflation as a documented sensitivity** (default OFF). | Amdt 04 §A5.5/§A5.6 |
| Soft annotation | **Moesia inferior, Britannia** flagged (θ-sensitive), not excluded. | Amdt 04 §A5.6 |

---

## 2. The statistic (precise)

For unit *u* and null family *f* ∈ {exp (primary), cpl-3 (secondary)}:

1. **Fixed null + envelope (computed once per *u* × *f*).** Fit *f* forward to the
   unit's raw `[nb, na]` intervals; draw `n_mc = 1000` MC null replicate count-SPAs
   of size `n_eff`; pointwise envelope = per-bin 2.5/97.5 percentiles; record the
   per-replicate out-of-envelope counts `{O^null_m}` (m = 1…1000).
2. **Observed signal = the posterior** `{g_d}` (d = 1…8000), each draw the
   **per-draw-normalised** corrected genuine SPA; scaled to counts
   `c_d = g_d · n_eff`.
3. **Per draw:** `O^obs_d` = #bins of `c_d` outside the fixed envelope;
   `p_d = (1 + #{m : O^null_m ≥ O^obs_d}) / (1 + n_mc)` (add-one, conservative).
4. **Headline — marginal global-*p*:** `p̄_u,f = mean_d p_d`. Equivalently the
   probability that featureless noise yields ≥ as many excursions as a
   posterior-random corrected curve (integrates both the MC-null and the
   deconvolution posterior). Reduces exactly to the single-curve Timpson test if
   the posterior is a point mass.
5. **Companion — P(deviation):** `π_u,f = mean_d 1[p_d < 0.05]`.
6. **Uncertainty diagnostic:** the 2.5/50/97.5 percentiles of `{p_d}`.

Deviation is **described** at `p̄ < 0.05` (not a confirmatory gate). The MC null is
built with a fixed seed so the envelope is shared across all 8,000 draws — draw-wise
propagation is then just 8,000 cheap out-count comparisons (vectorised), not 8,000
re-samples.

**Probe windows** (Antonine AD 165–180 → 4 bins, centres 162.5–177.5; Crisis
AD 235–284 → 10 bins, centres 237.5–282.5): per draw record whether any window bin
is out-of-envelope and its **signed** direction; aggregate to **P(window deviation)**,
**P(window deficit)** (one-sided companion), and the **posterior distribution of the
windowed departure magnitude** against the descriptive brackets (`primitives.BRACKETS`).
No magnitude pre-committed.

**Multiplicity (descriptive only).** Family = (29 units) × (2 probe windows) × (2
nulls). Holm–Bonferroni step-down on the sorted headline `p̄` values, reported
alongside the raw `p̄` as a diagnostic — **not** a decision rule (prereg; Decision 15).

---

## 3. Inputs (corrected)

| Input | Source | Note |
|---|---|---|
| Corrected genuine SPA **posterior** | NEW artefact from Stage A: `runs/2026-06-13-cc-production-refit/outputs/posterior-draws/` | per-draw `p_gen` (8,000×80) per unit; normalised per draw in H3b |
| `n_eff`, α median/CI, medians | `runs/2026-06-13-cc-production-refit/outputs/refit-summary.json` | the committed canonical refit; **not overwritten** |
| Per-unit raw intervals (`nb`, `na`) | `h2_lib.load_filtered_lire` → `classify_family` → `enumerate_units` → `subset_corpus` | identical row membership to the refit; for the forward-fit null + widths |
| Unit list (29) | refit `enumerate_refit_units()` | 28 + Italia (excl. Rome); empire & latin aggregates are the named-probe scopes |

---

## 4. Architecture — two stages

### Stage A — refit emits the genuine-SPA posterior (sapphire; the only compute)

The deconvolution posterior does not exist on disk (the refit samples in memory,
extracts medians, discards `idata`). Re-run the **same seeded refit** with a new
draws-persistence path:

- **Code change** (`runs/2026-06-13-cc-production-refit/code/run_refit.py`): add a
  `--emit-draws DIR` flag. When set, after sampling each unit, save the full
  per-draw `p_gen` posterior (`idata.posterior["p_gen"].reshape(-1, n_bins)`,
  8,000×80, `float32`) to `DIR/unit-NN-pgen.npz` with the seed and unit metadata.
- **Provenance gate (free reproducibility check):** the re-run recomputes the
  median; **assert** it matches the committed `refit-summary.json`
  `p_gen_median_raw` within `1e-9` per unit. A mismatch halts the run (it would mean
  the environment or seed drifted). **`refit-summary.json` is NOT overwritten** —
  the draws are a purely additive artefact.
- **Determinism:** unchanged seeds (`REFIT_BASE_SEED = 20260613 + unit_index`),
  adopted θ priors (θ_conv 0.930 / θ_gen 0.025), `n_jobs` per the original.
- **Cost:** ~5.5 min on sapphire (the measured refit time); ~150 MB of draws.
- **Hygiene:** runs under the Layer-1 `TMPDIR` default now in place (Item [1]).

### Stage B — H3b draw-wise harness (local; `uv run python`)

`runs/2026-06-09-h3b/code/` — a thin driver over the verified reused primitives
(§7). **No reimplementation** of the fit, sampler, or envelope; Stage B adds only
(a) the per-draw loop and (b) the aggregation/reporting.

Order:
1. Load the 29 posterior-draw artefacts (Stage A) + `refit-summary.json` (`n_eff`).
2. Reconstruct each unit's raw intervals (`h2_lib` chain above).
3. Per unit × null: fit null forward (exp) / smeared (cpl-3); build the MC envelope
   + `{O^null_m}` **once** (fixed seed `20260609 + unit_index`).
4. Evaluate all 8,000 draws → `{p_d}` → `p̄`, `π`, per-draw spread (§2).
5. Probe windows → P(deviation), P(deficit), windowed-magnitude posterior, brackets.
6. Holm-adjust the `p̄` family (descriptive).
7. Reachability annotation; soft annotation (Moesia inf., Britannia); coverage caveat.
8. Raw-SPA-vs-corrected-SPA follow-up (launch-spec §8: GRW may attenuate the
   Antonine peak → corrected may be conservative there). Run the same test on the
   raw observed SPA for comparison; report both.
9. Write outputs + DRAFT REPORT (§5).

**Compute:** permutation-only, no MCMC; a few minutes on a laptop. Sapphire not
needed for Stage B.

---

## 5. Outputs (`runs/2026-06-09-h3b/outputs/`)

- `deviations.json` — per (unit × null): `p̄`, `π`, `{p_d}` percentiles, per-window
  P(dev)/P(deficit)/magnitude-posterior/bracket, the fixed `lo_env`/`hi_env`, fitted
  null params, seed, reachability + soft-annotation flags, Holm-adjusted `p̄`.
- `deviations-table.csv` — flat tabulation for the report.
- `replication-antonine.json`, `replication-crisis.json` — the two named probes
  (empire + per-unit; Crisis also `latin-aggregate`).
- `raw-vs-corrected.json` — the §8 follow-up.
- `REPORT.md` — DRAFT-FOR-REVIEW: scope + reliability table, per-unit headline `p̄`
  with P(deviation) and spread, the two replication outcomes, raw-vs-corrected, the
  coverage caveat, soft annotations, Holm diagnostic, and a deferred-items list.
- (optional) per-unit envelope plots with the posterior band overlaid — deferred
  unless cheap.

---

## 6. Reliability handling (Amendment 04 §§A5.5–A5.6)

- **Propagation, not exclusion.** Weakly-identified units get a wider `{p_d}` → `p̄`
  pulled toward non-significance automatically. No unit is dropped.
- **Soft annotation.** Moesia inferior and Britannia (θ-sensitive in the θ-sweep)
  carry a reliability flag in every table.
- **Coverage caveat.** The cc posterior CIs are ~1σ-optimistic (§A5.5), so the
  propagated `{p_d}` is mildly too narrow. Carried as an explicit report caveat.
  **Sensitivity (default OFF):** an optional posterior-spread inflation factor
  (e.g. ×1.0–1.3 on the centred draws) is exposed as a flag; if Shawn wants it ON
  for the DRAFT, set one value and report both.
- **High-residual-corner fallback.** For any unit flagged in the refit's
  high-convention-%×high-α corner, the report notes the two-bound [shared, per-unit]
  α range as the §A5.5 fallback sensitivity.

---

## 7. Reuse map (verified 2026-06-14 — functions exist at these lines)

| Need | Artefact | Function (line) |
|---|---|---|
| Forward exp null + forward MC + envelope | `runs/2026-04-25-h1-simulation/code/forward_fit.py` | `fit_null_exponential_forward` (196), `sample_null_spa_forward_exp` (316), `forward_envelope_test` (391) |
| CPL-3 null + MC + Timpson envelope; bins; brackets | `runs/2026-04-25-h1-simulation/code/primitives.py` | `fit_null_cpl` (316), `sample_null_spa` (423), `permutation_envelope_test` (543), `BIN_EDGES` (62), `BIN_CENTRES` (63), `BRACKETS` (656) |
| Corpus + intervals + unit enumeration | `runs/2026-06-07-h2.1-launch-prep/code/h2_lib.py` | `load_filtered_lire` (106), `classify_family` (129), `latin_provinces` (147), `enumerate_units` (256), `subset_corpus` (288) |

The existing envelope tests return a single global-*p*; Stage B adds a thin wrapper
that **exposes the envelope + `{O^null_m}` once** and loops the 8,000 draws against
them — reusing the sampler/fit unchanged.

---

## 8. Run plan + PRE-LAUNCH GATE (what Shawn is approving)

1. **Stage A (sapphire compute):** the `--emit-draws` change to `run_refit.py` +
   re-run the 29-unit refit (~5.5 min, seeded, median-match provenance gate, no
   overwrite of `refit-summary.json`). **← the only compute; needs Shawn's go.**
2. **Stage B (local):** build + run the draw-wise harness; produce the DRAFT REPORT.
3. **Review:** DRAFT REPORT returns to Shawn; nothing is lodged or paper-bound
   without his read (H3b is exploratory and stays draft until then).

Standing rules honoured: spec-before-launch; no silent parameter negotiation; commit
before the pipeline stage; sapphire workdir `~/Code/inscriptions`.

---

## 9. Deferred (explicitly out of scope here; pre-confirmatory or follow-up)

1. Forward-CPL sampler (OQ-4) — CPL stays a labelled smeared-fit secondary.
2. Antonine Asclepius / military subsets (OQ-6) — need per-subset deconvolution,
   per-subset reachability, and a LIRE membership rule; define when built.
3. `baorista` Bayesian-aoristic cross-check (prereg line 378) — separate appendix.
4. Per-unit envelope plots — unless cheap.

---

## 10. Cross-references

- Supersedes: `runs/2026-06-09-h3b/h3b-spec.md` (2026-06-09 draft).
- Authority: `planning/osf-amendment-2026-06-14-cross-classified-remediation.md`
  §§A5.5–A5.6; tag `osf-amendment-04-2026-06-14` → `61c954c`.
- Decision 15 (exploratory recast): `planning/decision-log.md`.
- Production deconvolution: `runs/2026-06-13-cc-production-refit/`.
