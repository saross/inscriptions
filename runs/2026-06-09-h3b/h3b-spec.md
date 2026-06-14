# H3b deviation-detection — build-ready design spec (DRAFT)

> **⚠ SUPERSEDED (2026-06-14) by `h3b-implementation-spec-2026-06-14.md`** in this
> same dir — which folds in OSF Amendment 04 §A5.6 (uncertainty propagation
> replaces the identifiability restriction) and Shawn's 2026-06-14 design
> decisions, and corrects the production source to the cc-library refit. Retained
> as the dated record of the 2026-06-09 design and its open-question framing.

**Status:** DRAFT — FOR REVIEW. Nothing here is confirmatory until a human signs
off the open questions in §10.
**Date:** 2026-06-09.
**Author:** Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief.
**Run dir:** `runs/2026-06-09-h3b/`.
**UK/Australian English; Oxford comma.**

---

## 0. One-paragraph summary

H3b is the project's **pre-specified, exploratory temporal deviation-detection**
analysis. It scans each geographic unit's editorial-convention-CORRECTED genuine
summed-probability analysis (SPA) — the H2.1 hand-off — against a featureless
("null") permutation envelope, and asks whether the corrected curve pokes outside
that envelope at two named historical probe windows: the **Antonine** probe
(AD 165–180) and the **Crisis-of-the-Third-Century** probe (AD 235–284). The null
is a forward-fit exponential (primary) / CPL-3 (secondary) growth–decline model;
significance is the Timpson et al. (2014) global-*p* envelope test. Deviations are
reported descriptively against the project's effect-size brackets, with
multiplicity reported alongside. **Per the lodged preregistration H3b carries NO
confirmatory Holm-corrected family** (Decision 15); the "Holm–Bonferroni" framing
in the project backlog is a *superseded* description — see §2 and OQ-1.

---

## 1. What H3b tests (the question)

> "To decide whether a given wiggle is a real historical event or just noise, we
> build a 'what noise alone looks like' band: we simulate many artificial datasets
> under a deliberately featureless model (smooth growth or decline, no special
> events), measure how much *those* curves wiggle, and check whether the real
> curve pokes outside the resulting band. Poking outside it indicates a deviation
> unlikely to be chance."
> — preregistration-draft.md line 153 (Step 4, plain-language).

A **deviation** = a statistically-flagged departure of the observed (corrected)
SPA from the featureless-null permutation envelope. Operationally there are two
linked quantities (prereg lines 153, 290; §6 below):

1. **Global significance** — the Timpson et al. (2014) global-*p* envelope test:
   the proportion of Monte-Carlo (MC) null replicates whose count of
   out-of-pointwise-envelope bins meets or exceeds the observed count. A unit's
   curve "deviates" globally at *p* < 0.05.
2. **Where** — the bins (and hence calendar windows) at which the observed curve
   lies outside the pointwise 2.5/97.5-percentile envelope. H3b reads these
   against the two pre-specified probe windows.

The envelope **is** the uncertainty representation; no separate credible interval
is computed and **no mixture-posterior uncertainty is propagated** (prereg line 35;
H2.1 launch-spec §8 / Decision 37-D2; prereg-note line 70–72).

---

## 2. Confirmatory status — the central reconciliation (READ THIS)

There is a **direct conflict** between two project sources on whether H3b is
confirmatory and Holm-corrected:

- **The lodged preregistration (authoritative):** H3b is **pre-specified
  EXPLORATORY**, with **no Holm-corrected confirmatory family**.
  - prereg line 91: *"H3b … is not in the confirmatory family — its windows and
    subsets are pre-specified, but no effect-size magnitudes are pre-committed and
    no Holm-corrected confirmatory family is formed."*
  - prereg line 101: *"no Holm-corrected confirmatory family is formed."*
  - prereg line 346: *"Results reported descriptively against the project's
    standard brackets, with multiplicity noted; no Holm-corrected confirmatory
    family."*
  - **Decision 15 (2026-05-14)** recast H3b from confirmatory to pre-specified
    exploratory precisely to dissolve the Holm–Bonferroni family-size researcher
    degree of freedom: *"The Holm-Bonferroni family-size choice (12 vs 6 cells) is
    moot: there is no confirmatory H3b family to correct."* (decision-log.md lines
    1115–1118.)

- **The project backlog / continuity (SUPERSEDED wording):** describes H3b as
  *"deviation detection (forward-fit envelope at H1-reachable cells). Holm-Bonferroni
  across 6 cells … OR 12 cells"* (backlog-2026-05-03.md line 56;
  continuity.md line 153). This phrasing predates / was not updated after Decision
  15 and **Decision 10's** retirement of the `c_20pc_25y` bracket from the H3b
  confirmatory eligibility list. Decision 10 (decision-log.md lines 605–641) still
  speaks of a "Holm–Bonferroni-corrected" H3b family; **Decision 15 then removed
  that family entirely.** The decision-log is internally chronological: 15
  post-dates and overrides 10 on this point.

**This spec follows the preregistration and Decision 15: H3b is exploratory; no
Holm-corrected confirmatory family is formed.** We nonetheless **compute and
report a Holm–Bonferroni-adjusted *p*-value alongside the raw global-*p* as a
descriptive multiplicity diagnostic** (the brief asks for "Holm-Bonferroni-adjusted
significance"; reporting it descriptively satisfies the brief without contradicting
the prereg, which explicitly asks for "multiplicity noted"). The adjusted *p* is
**not** a confirmatory decision rule. **See OQ-1 — the human must confirm which
status governs the paper.**

---

## 3. Inputs (exact)

### 3.1 The corrected genuine SPA (primary observed signal)

- **Source:** `runs/2026-06-07-h2.1-launch-prep/outputs/production/units/unit-NN.json`,
  field **`corrected_genuine_spa`** — an 80-element vector, the posterior-MEDIAN
  corrected genuine SPA, **renormalised to sum to 1** (h2_lib.py line 355, 381:
  `p_gen_med_norm`). It is a probability distribution over the 80 five-year bins,
  NOT integer counts.
- **Envelope / binning:** 50 BC – AD 350, 5-year bins, 80 bins. `BIN_EDGES =
  arange(-50, 351, 5)`; `BIN_CENTRES = -47.5, -42.5, …, 347.5` (h2_lib.py 77–78;
  primitives.py 62–65; prereg line 169). The Antonine probe (AD 165–180) and Crisis
  probe (AD 235–284) both fall cleanly inside the envelope.
- **n_eff:** field `n_eff` per unit — the integer effective corpus size the H2.1
  observation model rounded to. Used to scale the corrected distribution to a count
  vector and to size each MC replicate (so the envelope width matches the unit's N).

### 3.2 The per-unit raw intervals (for the forward-fit null + widths)

The featureless null is **forward-fit in true-date space on the unit's actual
`[not_before, not_after]` intervals**, NOT on the smeared SPA (prereg lines 153,
309; this is the documented false-positive fix). The empirical width distribution
of those intervals is re-applied when generating MC replicates. We therefore need
each unit's member rows.

- **Reconstruction (verbatim from the H2.1 harness, no reimplementation):**
  `h2_lib.load_filtered_lire()` → `h2_lib.classify_family()` → `enumerate_units()`
  → `subset_corpus(df, unit, latin_provinces())`. This yields the identical row
  membership the H2.1 fits used (asserted to the 180,609-row prereg corpus).
- From the subset: `nb = df_unit["nb"]`, `na = df_unit["na"]`, and the width
  distribution `widths = na − nb` (clipped to the envelope by the forward-fit /
  sampler, as `forward_fit.py` already does).

### 3.3 Which units (the identifiable set) — computed explicitly

**Confirmatory-eligible (identifiable) set = units whose H2.1 convention correction
is reliable.** Per the prereg note (`planning/prereg-note-2026-06-09-alpha-
identifiability.md` lines 53, 70–72) and the brief, the **operative flag** is the
gap between the grid-alignment family fraction and the fitted α:

```
gap = f1f3_family_mass_fraction − alpha_median
identifiable  ⇔  gap < 0.20
```

Computed from the **29** unit JSONs (reproducible via
`code/compute_identifiability.py`). *Note:* the production set is 29 units, not 28
— `unit-29.json` is **Italia (excl. Rome)**, the aggregate added post-hoc per the
prereg note §4 (lines 73–79); there is no `unit-28.json`.

**IDENTIFIABLE — 17 units (confirmatory-eligible for the DRAFT pass):**
empire-aggregate, latin-aggregate, **Italia (excl. Rome)**, Latium et Campania /
Regio I, Dalmatia, Hispania citerior, Germania superior, Dacia, Pompeii, Pannonia
superior, Apulia et Calabria / Regio II, Africa proconsularis, Noricum, Baetica,
Etruria / Regio VII, Mogontiacum, Transpadana / Regio XI.

**FLAGGED under-identified — 12 units (EXPLORATORY only):**
Moesia inferior, Samnium / Regio IV, Pannonia inferior, Numidia, Venetia et
Histria / Regio X, Salona, Britannia, Umbria / Regio VI, Ostia, Aquileia, Germania
inferior, Lusitania.

> **⚠ Criterion conflict — OQ-2.** The committed
> `outputs/production/identifiability-table.json` flags identifiability by a
> *different* rule — the **basis swing** `|α_shared − α_per-unit| > 0.2` — which
> marks only **9** units identifiable (and would *exclude* Dalmatia, Hispania
> citerior, Dacia, Africa proconsularis, Baetica, Etruria, and Transpadana from my
> 16). The brief mandates the **gap** rule; the prereg note's own narrative
> example set ("Latium, the aggregates, Noricum, Pompeii, Dalmatia, Etruria, the
> Italia aggregate"; lines 51–52) matches the **gap** rule, not the swing rule. I
> proceed on the gap rule and report both. **The human must confirm which rule is
> canonical for the confirmatory H3b set.** Under the swing rule the
> confirmatory-eligible set is the 7 strict-overlap units
> {empire-aggregate, latin-aggregate, Latium, Hispania citerior, Germania superior,
> Pannonia superior, Mogontiacum, Apulia, Pompeii, Noricum}.

### 3.4 Reachability gate (which units can detect a deviation at all)

Phase 1 (H1, complete) sets the minimum N at which the method detects a
50%-over-≥50-y event at detection ≥ 0.80 — the smallest pre-specified bracket H3b
can reach (prereg line 408; Decision 10 retired the 20%/25y bracket from the H3b
list; the doubling/25y bracket is Gaussian-only-reachable, prereg line 409):

| Level | Binding (cpl-3, Gaussian) min N | exp min N |
|---|---|---|
| empire | reachable at N = 50,000 | reachable at N = 50,000 |
| province | 1,618 | 1,869–1,938 |
| urban-area | 1,549 | 1,854–1,923 |

**All 28 H2.1 units have N_eff ≥ 1,578** (smallest: Lusitania 1,578, Moesia
inferior 1,728). So **every unit clears the province / urban 50%/50y reachability
floor under the exp null at its level** — with two nuances flagged in OQ-3:
(a) Lusitania (1,578) sits just below the province cpl-3-Gaussian 1,618 threshold,
so its *cpl-3 secondary* result should carry a reachability caveat (it is flagged
under-identified anyway); (b) the empire-aggregate level's Phase 1 grid only ran a
single N = 50,000 representative cell, and our empire N_eff = 151,361 ≫ 50,000, so
empire is reachable a fortiori.

---

## 4. The method (derived from the prereg; cite-anchored)

### 4.1 The featureless null

Two null families, both fitted forward in true-date space (prereg lines 153, 309,
317):

- **Exponential (PRIMARY)** — single rate `b`; `f(t) ∝ exp(b·t)` truncated to
  `[−50, 350]`. Fit by closed-form interval-integral maximum likelihood treating
  each `[nb, na]` as an integration range
  (`forward_fit.fit_null_exponential_forward`).
- **CPL-3 (SECONDARY)** — continuous piecewise-linear, 3 interior knots, knot
  positions fitted; flexible enough for rise-and-fall, rigid enough to be a clear
  null (prereg lines 153, 317). Fitted on the SPA via Poisson NLL
  (`primitives.fit_null_cpl(..., k=3)`), then MC-sampled with Poisson noise
  (`primitives.sample_null_spa`).
  - **NOTE — forward-fit asymmetry (OQ-4).** The exponential null has a true
    *forward* sampler (`sample_null_spa_forward_exp`: draws true dates, re-applies
    empirical widths + one aoristic draw — single smearing layer, the documented
    FP fix). The H1 codebase's **CPL path uses the older Poisson-on-fitted-SPA
    sampler**, which does NOT forward-apply the aoristic mechanism. For Phase-1
    threshold-setting this was acceptable (CPL is the secondary null). For H3b on
    real data, mixing a forward-fit exp primary with a smeared-fit CPL secondary is
    a known asymmetry. The DRAFT runs **exp as primary (fully forward)** and CPL-3
    as a **clearly-labelled secondary cross-check**; a forward CPL sampler is a
    pre-confirmatory build item (OQ-4).

### 4.2 The observed signal that is compared to the envelope

This is the load-bearing design choice and the place the prereg is least explicit
for the *corrected* (deconvolved) input (OQ-5):

- The H2.1 hand-off `corrected_genuine_spa` is a **normalised probability
  distribution** (sums to 1). The Timpson envelope test operates on **count-scale**
  SPAs (the MC replicates are integer counts of size N_eff). To put observed and
  null on the same footing we **scale the corrected distribution to counts**:
  `observed_counts = corrected_genuine_spa × n_eff`. This preserves the corrected
  *shape* (what H3b is about) while matching the count scale the envelope is built
  at. (Equivalent to treating the corrected curve as the unit's deconvolved
  per-bin expected counts.)
- **Why the corrected, not the raw, SPA:** the whole point of H2.1 is to remove
  editorial-convention slabs so a *genuine* historical wiggle can be told from a
  convention artefact (prereg line 35; Decision 37-D2). H3b runs on the corrected
  curve. We additionally run a **raw-SPA-vs-corrected-SPA comparison** as the
  pre-specified follow-up (launch-spec §8: "the GRW attenuates sharp peaks, so the
  corrected may be conservative at the Antonine probe").
- **The null is fit to the raw intervals, the envelope compares the corrected
  curve** — this is intentional: the null describes featureless *growth/decline of
  the underlying corpus*; the corrected curve is what we test for departures from
  that featureless baseline. The forward-fit absorbs only the smooth trend, leaving
  genuine events as departures. (OQ-5 records the alternative of fitting the null to
  a deconvolved interval set, which the project has not specified.)

### 4.3 The envelope test (significance)

`primitives.permutation_envelope_test` / `forward_fit.forward_envelope_test`
(hand-rolled Timpson et al. 2014; prereg lines 153, 290):

1. Draw `n_mc` MC null replicate SPAs (count scale, size n_eff).
2. Pointwise envelope = per-bin 2.5 / 97.5 percentiles of the replicates.
3. Observed out-of-envelope bin count vs the per-replicate out-of-envelope counts.
4. **Global *p*** = proportion of replicates with out-count ≥ observed out-count
   (conservative `≥`). Deviation flagged at *p* < 0.05.
- `n_mc = 1000` (prereg line 310, Phase-1 convention). `alpha = 0.05`.

### 4.4 Reading the probe windows

For each unit × null, after the global test, record:

- **Antonine probe** — bins overlapping **AD 165–180** (bin centres 162.5, 167.5,
  172.5, 177.5 — i.e. bin edges [160,165), [165,170), [170,175), [175,180);
  AD 165–180 spans 3 full 5-y bins plus boundaries; we take the 4 bins whose
  centres lie in [162.5, 177.5], inclusive of the window).
- **Crisis probe** — bins overlapping **AD 235–284 inclusive** (50 y under
  inclusive-Roman counting; prereg line 99). Bin centres 237.5 … 282.5 → 10 bins.
- For each probe window we record: (i) whether ANY bin in the window is
  out-of-envelope; (ii) the signed direction (above = surplus, below = deficit);
  (iii) the descriptive effect-size bracket the windowed departure matches
  (project brackets, §4.5). All descriptive — no magnitude is pre-committed (prereg
  line 101, Decision 15).

### 4.5 Effect-size brackets (descriptive reporting only)

From `primitives.BRACKETS` (prereg §6; Decision 5/10):

| bracket | magnitude | duration | role |
|---|---|---|---|
| `a_50pc_50y` | −0.5 (50% dip) | 50 y | primary detectable |
| `b_double_25y` | +1.0 (doubling) | 25 y | detectable (Gaussian) |
| `c_20pc_25y` | −0.2 (20% dip) | 25 y | hard-test boundary; **NOT in H3b family** (Decision 10) |

Observed windowed departures are described against these brackets ("a deficit
consistent with ≥50% over ≥50 y", etc.). No bracket is a decision threshold.

### 4.6 Multiplicity (descriptive)

The family of tests = (identifiable units) × (probe windows) × (null families).
For the DRAFT we report, per global test:

- raw global *p*;
- **Holm–Bonferroni-adjusted *p*** across the family, reported descriptively
  (step-down Holm on the sorted raw *p*-values). This satisfies the brief's
  "Holm-Bonferroni-adjusted significance" *as a multiplicity diagnostic*; it is NOT
  a confirmatory gate (prereg line 101; §2; OQ-1).

---

## 5. The two replication tests (pre-specified probes)

Both are **pre-specified exploratory** (prereg lines 96–101, 346, 350–351, 412–413).

### 5.1 Antonine probe — AD 165–180

- **Windows / subsets (prereg line 98):** empire level + an **Asclepius-cult
  subset** (replicating Glomb, Kaše & Heřmánková 2022 at larger N) + a
  **military-administration subset** (replicating Duncan-Jones 2018), each
  *conditional on per-subset Phase-1 reachability*.
- **Empirical priors conflict (so no magnitude pre-committed; prereg line 101):**
  Glomb et al. 2022 found a NULL at small N; Duncan-Jones 2018 found an abrupt
  cessation of military diplomas after AD 167 (a near-complete halt until AD 177).
  H3b reports what it finds against the brackets, descriptively.
- **DRAFT scope (OQ-6):** the Asclepius and military subsets require their **own
  per-subset deconvolution** (Decision 34/36: empire α is NOT imposed on subsets;
  per-subset mixture fits are unidentified below N≈100–300) and their **own Phase-1
  reachability runs** — neither exists yet, and LIRE has no clean pre-built
  Asclepius / military-diploma flag (only `inscr_type`, `keywords_term`,
  `type_of_inscription_*`). **The DRAFT therefore runs the Antonine probe at
  empire / unit level on the existing corrected SPAs only**, and flags the two
  literature-replication subsets as NOT-YET-BUILT (a pre-confirmatory dependency).

### 5.2 Crisis-of-the-Third-Century probe — AD 235–284 inclusive

- **Windows / subsets (prereg line 99):** empire level + a **Western-Empire
  provincial subset**, operationally `province_language == 'Latin' AND province !=
  'Roma'` (prereg lines 99, 135), conditional on Phase-1 reachability.
- The **latin-aggregate** unit IS exactly the operational Western-Empire-provincial
  subset (h2_lib `latin_all` filter = all Latin provinces; Rome is excluded by
  construction, Decision 36). So the Crisis Western-Empire subset is **directly
  runnable** on the existing `latin-aggregate` corrected SPA — no new fit needed.
- Reported descriptively against the brackets (the Crisis is a diffuse multi-decade
  decline; no magnitude pre-committed).

---

## 6. Outputs

Written to `runs/2026-06-09-h3b/outputs/`:

- `deviations.json` — per (unit × null × probe): raw global *p*, Holm-adjusted *p*,
  global `detected`, per-window out-of-envelope bin lists, signed direction,
  matched descriptive bracket, the pointwise `lo_env`/`hi_env`, the fitted null
  parameters, the seed.
- `deviations-table.csv` — flat tabulation for the report.
- `replication-antonine.json`, `replication-crisis.json` — the two probe results.
- `REPORT.md` — DRAFT-FOR-REVIEW: identifiable-set table, per-unit deviation
  results with Holm-adjusted significance, the two replication outcomes, the
  raw-vs-corrected comparison, and the open questions.
- Optionally per-unit envelope plots (`outputs/figures/`) — deferred unless cheap.

---

## 7. Run plan

- **Compute:** permutation-only, no MCMC. Per unit: 1 exponential ML fit
  (closed-form, milliseconds) + 1 CPL-3 fit (L-BFGS, ×4 restarts, ~1 s) + 2×1000 MC
  replicate SPAs (vectorisable). 16 identifiable units × 2 nulls × 1000 MC ≈ a few
  minutes on a laptop. **Runs locally** (`uv run python`); sapphire not required.
- **Seeds (deterministic, documented):** master seed **`20260609`**; per-unit RNG =
  `default_rng(20260609 + unit_index)`; the MC sampler takes that generator
  explicitly (no global RNG — the project seed-discipline, primitives.py 26–28).
- **Reuse, do not reimplement:** import `forward_fit.py` and `primitives.py` from
  `runs/2026-04-25-h1-simulation/code/`, and the unit/corpus reconstruction from
  `runs/2026-06-07-h2.1-launch-prep/code/h2_lib.py`. The H3b harness is a thin
  driver over these.
- **Order:** (1) compute identifiability split; (2) reconstruct per-unit corpora +
  corrected SPAs; (3) per unit fit null + run envelope test (exp primary, CPL-3
  secondary); (4) read probe windows; (5) Holm-adjust; (6) raw-vs-corrected
  follow-up; (7) write outputs + REPORT.
- **Scope discipline:** identifiable units = the DRAFT confirmatory-eligible set;
  flagged units run too but are tabulated EXPLORATORY-ONLY in a separate block.

---

## 8. Reuse map (no reimplementation)

| Need | Existing artefact | Function |
|---|---|---|
| Forward-fit exp null + forward MC + envelope | `runs/2026-04-25-h1-simulation/code/forward_fit.py` | `fit_null_exponential_forward`, `sample_null_spa_forward_exp`, `forward_envelope_test` |
| CPL-3 null fit + MC + Timpson envelope | `runs/2026-04-25-h1-simulation/code/primitives.py` | `fit_null_cpl`, `sample_null_spa`, `permutation_envelope_test`, `BIN_EDGES`/`BIN_CENTRES`, `BRACKETS` |
| Per-unit corpus + corrected SPA + n_eff | `runs/2026-06-07-h2.1-launch-prep/code/h2_lib.py` + `outputs/production/units/` | `load_filtered_lire`, `classify_family`, `enumerate_units`, `subset_corpus`, `latin_provinces` |

---

## 9. What this DRAFT deliberately does NOT do (pre-confirmatory dependencies)

1. The Antonine **Asclepius-cult** and **military-administration** subsets — need
   per-subset deconvolution + per-subset Phase-1 reachability + a LIRE membership
   rule (OQ-6).
2. A **forward CPL sampler** for real-data symmetry (OQ-4).
3. **baorista** Bayesian-aoristic cross-check (prereg line 378; a separate
   sensitivity appendix).
4. Any **mixture-posterior uncertainty propagation** — deliberately excluded
   (prereg line 35).

---

## 10. OPEN QUESTIONS for the human (load-bearing; confirm before confirmatory)

- **OQ-1 — Confirmatory status / Holm family.** The prereg + Decision 15 say H3b is
  exploratory with NO Holm-corrected confirmatory family; the backlog/continuity
  still say "Holm-Bonferroni across 6/12 cells". This spec follows the prereg
  (exploratory; Holm reported descriptively only). **Confirm** this is the intended
  status, and that the backlog wording is stale.
- **OQ-2 — Identifiability criterion.** Gap rule (`f1f3 − α < 0.20` → 17 units, the
  brief's rule, matches the prereg-note narrative) vs basis-swing rule (`> 0.2` →
  9 units, the committed `identifiability-table.json`). They disagree on 8 units
  (Dalmatia, Hispania citerior, Dacia, Africa proconsularis, Baetica, Etruria,
  Transpadana, and Italia). I used the **gap** rule. **Confirm which is canonical**
  for the confirmatory set.
- **OQ-3 — Reachability edge cases.** Lusitania (N=1,578) is below the province
  cpl-3-Gaussian 1,618 threshold (flag its CPL result); confirm the exp-null
  province threshold (~1,869) vs the cpl-3 (1,618) governs eligibility (the prereg
  §6 binding threshold is the conservative cpl-3-Gaussian — under which several
  smaller units would be borderline). **Confirm the binding threshold.**
- **OQ-4 — CPL forward sampler.** The exp null is forward-fit; the CPL null uses the
  older smeared-fit sampler. Acceptable for a DRAFT secondary? Or build a forward
  CPL sampler before confirmatory?
- **OQ-5 — Observed-signal scaling.** H3b compares the corrected *distribution*
  (×n_eff → counts) against a null fit to the *raw* intervals. Confirm this is the
  intended construction (vs. e.g. deconvolving the interval set itself). The prereg
  does not pin this for the corrected input.
- **OQ-6 — Antonine subsets.** The Asclepius / military subsets are NOT built (no
  per-subset deconvolution, no reachability run, no LIRE membership rule). Confirm
  they are deferred to a follow-up, and provide the intended membership definitions
  (which LIRE columns / keyword sets).
- **OQ-7 — Direction of test at the probes.** Both probes are historically
  *deficits* (Antonine plague mortality; Crisis decline). H3b's envelope test is
  two-sided (out-of-envelope either way). Confirm two-sided reporting with signed
  direction noted (this spec's choice), vs a one-sided deficit test.
- **OQ-8 — Per-unit scope.** The prereg names *empire* and the *Western-Empire
  provincial* subset for the probes explicitly. Running the probes at **every
  identifiable unit** is a natural extension but is broader than the prereg's named
  scope. Confirm whether per-unit probe scanning is in-scope or exploratory-extra.
