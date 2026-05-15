# Decision Log — inscriptions SPA

**Convention.** Record methodology and scope decisions here as an
ADR-style log. One decision per entry; numbered; dated; `status` is
`proposed` → `committed` → optionally `superseded-by-NNN`. The
point of this log is that the journal reviewer's "why did you do
X?" has an auditable answer; the secondary point is that we can
revisit decisions deliberately rather than silently drifting.

**When to add an entry.** Any methodology choice, scope boundary,
or infrastructural commitment that would be defensible in writing
but not obvious from the code alone. Data-cleaning parameter
choices, statistical-method picks, dataset-scope boundaries,
tooling selections, interpretation stances. Skip: anything that's
just "standard practice" with no live alternative.

**Template** (copy for new decisions):

```markdown
## Decision N — YYYY-MM-DD: [Short imperative title]

**Status:** proposed | committed | superseded-by-NNN
**Decided by:** Shawn (+ CC, + other collaborators)

### Context

What problem or choice-point this decision addresses. What changed
to make this a decision we had to make now rather than later.

### Options considered

- **A** — description. Pros / cons.
- **B** — description. Pros / cons.
- **C** — description. Pros / cons.

### Decision

Chosen option, one-paragraph justification.

### Consequences

What this makes easier, what this makes harder, what it commits us to
downstream. Costs we accept, alternatives we've closed off.

### Revisit triggers

Conditions under which we'd reopen this decision. If none, say so.
```

---

## Decision 1 — 2026-04-22: Target LIRE v3.0 for the Friday / Saturday deliverable; swap to LIST v1.2 in paper-sprint Week 1

**Status:** committed
**Decided by:** Shawn (CC raised the option; Shawn endorsed 2026-04-22)

### Context

The archived project used LIRE (182,852 rows, 50 BC – AD 350). The
rebuilt project's original motivation was to extend chronological
coverage via LIST (525,870 rows, wider envelope). The Friday /
Saturday deliverable deadline is tight (3 days from decision), and
LIST requires additional filtering and cleaning decisions we have
not yet made. The LIST reconnaissance agent confirmed on 2026-04-22
that **LIST and LIRE share an identical 65-attribute schema** — LIRE
is a row-filter of LIST, not a column transform — so the dataset
swap is structurally cheap.

### Options considered

- **A — LIST from the start.** Pros: final-form analysis earlier,
  no later-stage migration. Cons: more cleaning choices on the
  critical path (is_within_RE? is_geotemporal? date-interval cutoff?
  — LIST needs these decided before it's a usable frame), more risk
  for Friday / Saturday.
- **B — LIRE throughout; no LIST work at all.** Pros: lowest-risk
  execution; LIRE is what the 2024 seminar demonstrated on. Cons:
  surrenders a primary motivation of the rewrite (extended temporal
  coverage into Late Antiquity).
- **C — LIRE for Friday / Saturday; swap to LIST in paper-sprint
  Week 1.** Pros: de-risks the co-author-facing deliverable; the
  schema-identity finding makes the swap a data-loader change
  rather than a rewrite. Cons: two data-framing passes rather than
  one; the Friday / Saturday min-thresholds calculation's absolute
  numbers will change when applied to LIST (though the method
  applies unchanged).

### Decision

**Option C.** LIRE v3.0 as the Friday / Saturday working dataset;
schedule the LIST v1.2 swap for paper-sprint Week 1 (week of
2026-04-27). The swap is a `read_parquet` source change plus
application of the three LIRE filter predicates (`is_within_RE`,
`is_geotemporal`, 50 BC – AD 350 interval) up-front.

Rationale: the min-threshold simulation method is dataset-agnostic,
so the Friday deliverable's methodological content holds under the
swap. LIRE gives Shawn immediate access to a vetted on-disk copy
with derived columns. LIST's additional rows are mostly outside the
50 BC – AD 350 Roman-Empire envelope (LIST covers ~700 BC – AD 950
more sparsely); the temporal-extension motivation specifically needs
LIST's Late-Antique subset, which can be the Week-1 focus without
blocking Friday / Saturday.

### Consequences

- The Friday draft uses LIRE as its worked-example corpus.
- The Saturday feasibility doc names the swap as the Week-1 gate.
- Adela sees numbers computed against a corpus she knows; she can
  assess the method without needing to simultaneously assess a
  new dataset.
- All simulation / significance / power code must be written to
  accept any aoristically-dated inscription frame, not LIRE-specific
  conventions, so the Week-1 swap is mechanical.
- The feasibility doc's *data artefacts* section lists the EDH/EDCS
  upstream issues (see `docs/notes/reflections/working-notes.md`
  Obs 7) that apply equally to both datasets.

### Revisit triggers

- LIRE reveals a blocker the method can't handle (unlikely but
  possible — e.g., an unforeseen numerical issue in `date_range`
  calculation).
- LIST swap in Week 1 surfaces data-quality issues in the newly-
  included rows that make the swap ill-advised. In that case,
  ship the paper on LIRE and flag LIST as a follow-up.

---

## Decision 2 — 2026-04-22: Minimum-count method — simulation-based power analysis using tempun + scipy primitives; port rcarbon-style permutation logic to Python (~200 LOC)

**Status:** committed
**Decided by:** Shawn (CC proposed the approach; prior-art-scout confirmed the build surface; Shawn endorsed 2026-04-22)

### Context

The historic blocker from the archived notebook was a rigorous
minimum-count method and a formal significance test on SPAs. The
radiocarbon SPD community has well-developed machinery for both
(Crema & Bevan 2021; Timpson 2014; Crema 2022 review). No existing
Python package exposes this machinery for calendar-date aoristic
inscription data.

### Options considered

- **A — rpy2-wrapped rcarbon.** Pros: uses the reference
  implementation verbatim. Cons: introduces an R dependency that
  makes open-science packaging harder; rcarbon's permutation/model
  functions assume binned radiocarbon dates and their calendar-data
  adaptation is non-trivial even in R.
- **B — Adopt baorista (Crema 2025, Bayesian aoristic).** Pros:
  methodologically the most relevant package for calendar-dated
  inscription data; Crema 2025 calls for exactly this application.
  Cons: R + NIMBLE + C++ compilation; heavier-weight than needed
  for a 2-day sprint; Shawn prefers Python.
- **C — Port rcarbon-style permutation logic to Python (~200 LOC)
  using tempun for aoristic sampling and scipy primitives
  (`scipy.stats.permutation_test`, `numpy.quantile`) for the
  significance / permutation layer.** Pros: Python-native;
  publishable as open-science reproducibility contribution; uses
  SDAM's own tempun for the date-sampling layer (aligns with
  collaborators' toolchain and Adela is co-author on the
  `tempun_demo` notebook). Cons: build cost of ~1 focused day of
  work; we own the code rather than inherit a community-maintained
  reference.

### Decision

**Option C.** Port rcarbon-style permutation machinery to Python,
using `tempun` for criterion (i) aoristic date sampling and scipy
primitives for criteria (ii) pointwise Monte Carlo significance
envelopes, (iii) permutation test for SPA group comparison, and
(iv) power / minimum-sample-size simulation. Target: ~200 LOC of
Python, tested, documented, packageable.

Rationale: eliminates the R dependency; uses SDAM's own tempun as the
sampling foundation (collaborator alignment + licence-clean at MIT);
rcarbon's `tests.R` (~350 LOC in R) is the algorithmic reference to
port. The ~200 LOC Python build is well within reach before Friday.
Baorista (Bayesian) remains interesting as a sensitivity / benchmark
comparison — see Decision 3.

### Consequences

- Dependency: `tempun` (PyPI, MIT) added to the project environment.
- Ownership: the project must maintain the permutation-envelope
  implementation. Tests must be comprehensive (the reference is
  rcarbon's R implementation — document behavioural parity).
- Packaging: the implementation should be clean enough to be useful
  to the next research group applying SPD machinery to any
  calendar-dated corpus, per the RDA open-science framing.
- Friday deliverable can ship with the significance-envelope + power
  simulation running; Adela will see real numbers, not method-only
  prose.

### Revisit triggers

- Build cost balloons past 2 days — fall back to rpy2-wrapped
  rcarbon for Friday, return to the Python port later.
- baorista (Decision 3) turns out to produce materially different
  results on real data; consider elevating baorista to primary and
  the permutation port to sensitivity analysis.

---

## Decision 3 — 2026-04-22: Bayesian aoristic benchmark (Crema 2025 baorista) — parallel sensitivity analysis if viable; candidate for a follow-up paper

**Status:** committed
**Decided by:** Shawn 2026-04-22

### Context

Crema's 2025 *baorista* paper is the methodological pivot for
calendar-dated aoristic archaeological data — the first published
Bayesian alternative to frequentist aoristic analysis, explicitly
calling for the kind of application this project undertakes. Shawn
has flagged two concerns: (a) Crema 2025 uses simulated data and the
real-world translation is untested; (b) Crema is a serious
methodologist whose framework deserves treatment, not dismissal.

### Options considered

- **A — Ignore baorista; frequentist SPA only.** Dismisses a
  methodologically relevant recent development.
- **B — Switch primary method to baorista.** Would require R +
  NIMBLE dependency; violates the Python preference; too heavy for
  3-week paper timeline.
- **C — Frequentist SPA (permutation-envelope) as primary; baorista
  as sensitivity analysis in parallel, if viable within the
  timeline.** If baorista runs cleanly, report both; if results
  diverge substantively, that's itself a finding.
- **D — Frequentist SPA as primary; baorista as an explicitly-
  planned follow-up paper.** Defers the Bayesian comparison to
  dedicated treatment.

### Decision

**Option C as primary intent, with D as the fallback.** Attempt a
baorista run on a representative LIRE subset during paper-sprint
Week 2. If the results are ready by Week 3 of the paper sprint,
include as sensitivity analysis. If not (R/NIMBLE install, run-time,
or interpretation complexity blocks us), push to follow-up paper per
Option D.

Rationale: running both at a subset scale costs relatively little
once the frequentist pipeline is working and answers Shawn's
curiosity about real-world translation of Crema 2025; a clean
frequentist-vs-Bayesian convergence or divergence is a useful result;
the fallback to follow-up paper preserves scope control on the
conference paper.

### Consequences

- Time budget in Week 2 of the paper sprint reserved for baorista
  install + small-subset test run.
- If Option D fallback: frame the baorista comparison as the headline
  of a follow-up paper; this is explicitly welcomed by Crema 2025's
  call for applications.
- R + NIMBLE + C++ compilation tooling installed on sapphire if
  Option C path is pursued; install cost likely ~1 hour.

### Revisit triggers

- baorista's documentation reveals a deal-breaker for inscription
  data (e.g., can't handle our date-interval structure).
- Paper-sprint timeline compresses further.

---

## Decision 4 — 2026-04-22: Distribution over inscription date intervals — uniform primary; trapezoidal as sensitivity analysis

**Status:** committed
**Decided by:** Shawn 2026-04-22

### Context

Aoristic date treatment requires a distribution choice over
`[not_before, not_after]`. Uniform is the default and matches the
2024 seminar prior work. Shawn raised the argument for trapezoidal
(mid-interval more likely than edges) citing Crema's earlier work
(Crema 2012 or similar). `tempun` supports both via the `b`
parameter in `model_date()` (`b=0` uniform, `b>0` trapezoidal).

### Options considered

- **A — Uniform only.** Simple; matches 2024 precedent; may
  over-weight interval extremes.
- **B — Trapezoidal only.** Uses prior information about typical
  inscription-production dynamics; requires choosing trapezoid
  shape parameters.
- **C — Uniform primary, trapezoidal as sensitivity analysis.**
  Reports both; detects whether conclusions are robust to
  distributional choice.

### Decision

**Option C.** Uniform for the primary Friday / Saturday analyses and
the conference paper's headline figures; a trapezoidal sensitivity
run for selected subsets (likely the full-empire SPA and 2–3
representative province / city SPAs) to be reported in the paper's
robustness section.

### Consequences

- Simulation code must parameterise the `b` input from tempun, not
  hard-code uniform.
- Paper includes a short robustness-check section.
- The trapezoid shape parameters themselves become a sensitivity
  consideration (Week 2 of paper sprint).

### Revisit triggers

- Trapezoidal produces materially different results at uniform's
  power — may need to elevate trapezoidal to primary, uniform to
  sensitivity.

---

## Decision 5 — 2026-04-22: Effect-size targets for the Friday min-thresholds simulation — run (a), (b), (c) for bracketing; (a) as Adela's headline

**Status:** committed
**Decided by:** Shawn 2026-04-22

### Context

The Friday draft promises Adela a first-pass minimum-threshold
calculation: how many inscriptions / letters per subset are needed
to distinguish a meaningful signal from noise. This requires
specifying an effect size — the deviation magnitude the test must
have power to detect.

### Options considered

- **A — Conservative**: detect a 50% sustained deviation from the
  whole-empire SPA over a ≥50-year window.
- **B — Middle**: detect a doubling/halving event over a ≥25-year
  window.
- **C — Ambitious**: detect a ≥20% deviation over a ≥25-year
  window.
- **Antonine-anchored**: detect the Antonine Plague signature
  specifically (shape and magnitude roughly from Glomb et al. 2022
  Asclepius temporal model).

### Decision

**Run (a), (b), and (c) in exploration; report (a) as the baseline in
Adela's Friday draft; bracket with (b) and (c) in the appendix or
companion figure.** This gives Adela a defensible headline number
plus a sense of the sensitivity of the threshold to effect-size
assumption.

Rationale: bracketing with three effect sizes costs little once the
simulation engine runs (loop over three conditions); the bracket
itself is informative because it tells the reader how much effort
goes into resolving finer deviations.

### Consequences

- Simulation output includes a 3-curve power-vs-n plot for each
  subset level (city, province, decade).
- The Friday draft highlights (a) in tables and headline prose;
  (b) and (c) appear as supplementary curves.

### Revisit triggers

- Adela's feedback requests a different anchor (e.g., Antonine-
  specific, or a historical event she considers more tractable).

---

## Decision 7 — 2026-04-23: Main-paper deconvolution architecture + scope-commitment path

**Status:** committed
**Decided by:** Shawn (after Claude's critical-friend push-back on an earlier four-co-equal-approaches plan)

### Context

The 2026-04-23 comprehensive rerun of the descriptive profile quantified substantial editorial-convention artefacts in LIRE v3.0 (midpoint-inflation observed/expected ratios of 22.8× / 41.5× / 18.8× / 39.7× at century midpoints AD 50/150/250/350; Westfall-Young adjusted p ≈ 0 on all four). The main paper's SPA methodology needs to address this artefact credibly. Multiple deconvolution approaches were discussed; the architecture and the scope commitment needed to be settled.

### Options considered

- **A — Four co-equal primary approaches** (thresholded / stratified / baorista Bayesian / explicit mixture): comprehensive but risks redundancy, scope creep, and reviewer confusion about which is the headline method.
- **B — One primary correction + robustness checks** (single headline method, related approaches as supporting evidence): cleaner narrative, clearer contribution claim.
- **C — Split into methods paper (JAMT) + results paper (JAS) upfront**: highest-commitment path; generates two papers but doubles submission effort and requires the methodology to stand alone as a publication.

### Decision

**Option B, with this architecture:**

- **Primary correction — explicit editorial-convention deconvolution mixture model.** Observed SPA decomposed as `observed = α · convention_SPA + (1 − α) · genuine_SPA`; α estimated from data; `genuine_SPA` recovered by deconvolution. Novel methodology + clean counterfactual + better narrative than the stratification alternative.
- **Robustness in body — thresholded SPAs** (Shawn's 2024 practice). Runs SPA at `date_range ≤ 25 / 50 / 100 / 200 / 300 / all`; agreement across thresholds rules out wide-range-row dominance. Established method, reviewer-familiar.
- **Robustness in appendix — stratified SPAs by convention-vs-precision classification.** Hard classification of each row; per-stratum SPAs. Cross-check that agrees with the mixture's deconvolved SPA validates the mixture without demanding its own in-body narrative space.
- **Bayesian comparison — baorista** (Crema 2025). Install properly on sapphire; run on a representative LIRE subset (provinces with n ≥ 1000 — likely ~7–10 provinces); appendix figure + paragraph-to-page integration. Not "a throwaway paragraph"; run and report properly.
- **Aeneas-partition** remains a separate follow-up paper (FS-1).

### Scope commitment path

Default: **single combined paper targeting JAMT** (methods-heavy) or JAS (balanced). Commit to single-vs-split **by end of Week 1 of the paper sprint** (no later). Trigger conditions that would favour splitting per FS-0:

- Methodology content exceeds ~3,000–4,000 words of novel material during drafting.
- Deconvolution + baorista produce substantively different results (methodology story becomes interesting enough to publish on its own).
- Aeneas-partition outline suggests a natural companion submission with a dedicated methods paper.

If none of the above trigger by end-of-Week-1, single paper.

### Consequences

- Sunday / Monday: baorista install on sapphire. Pilot run.
- Thursday (this week): run the deconvolution mixture on LIRE pilot (one province) alongside the descriptive-profile-rerun outputs.
- Friday OSF preregistration covers the deconvolution-mixture approach as preregistered primary methodology.
- Week-1 checkpoint (Sunday 2026-05-03): methodology word-count + baorista-comparison results reviewed; scope committed.

### Preliminaries to watch for

These would surface scope signal earlier and reduce risk of late-cycle indecision:

- **Literature prior art for single-vs-split structure**: how did Timpson/Crema structure their Neolithic Europe SPA work — methods-first, results-first, combined? Quick lit-scout could reveal the field's convention.
- **Deconvolution-mixture pilot quality**: if the pilot run produces clean interpretable results at first attempt, methodology section stays compact; if substantial tuning is needed, it expands toward the split threshold.
- **baorista install cost**: if installing on sapphire is non-trivial (C++ compilation fails, NIMBLE setup issues), the baorista-run-properly plan may need to become citation-with-rationale.

### Revisit triggers

- Week-1 checkpoint (Sunday 2026-05-03).
- Any of the three preliminary signals above tipping clearly.
- Methodology content growing unexpectedly during drafting — flag for re-evaluation.

---

## Decision 6 — 2026-04-22: Tooling-routinisation triggers — commit-to-run defaults

**Status:** committed
**Decided by:** Shawn 2026-04-22

### Context

Shawn has developed a set of standing tools (`/audit`,
`/review-implementation`, `/improve-prompt`, `prior-art-scout`,
`/lit-scout` with verifier, `/phase-gate`) and asked to routinise
their invocation. The aim is defence-in-depth at known inflection
points rather than ad-hoc triggering.

### Options considered

- **A — All triggers opt-in.** Low overhead; high miss rate.
- **B — All triggers commit-to-run, waivable.** Higher overhead;
  low miss rate; Shawn can waive per-invocation.
- **C — Tiered.** High-leverage triggers commit-to-run; lower-
  leverage ones opt-in.

### Decision

**Option B with one scope clarification.** Commit-to-run:

- `/audit` after any code written or modified (already in Shawn's
  scratchpad as non-negotiable).
- `/review-implementation` at methodology-choice boundaries, phase
  boundaries, and before any agent run costing ≥30 min compute.
- `prior-art-scout` before building anything we might not need to
  build; default-on when starting to write >~50 LOC of methodology
  from scratch.
- `/improve-prompt` on any agent brief driving a long-running or
  expensive-to-re-run agent.
- `/lit-scout` (with verifier) any time methodology citations will
  appear in published text.

**Scoped:**

- `/phase-gate` — **only on paid external-API spend** (not Claude
  Max credit, which is pre-paid and un-gated). If we move to, e.g.,
  per-row LLM classification calls on the dataset, `/phase-gate`
  fires before launch. Everyday work in the Max plan does not
  require it.

### Consequences

- Session-start and phase-boundary routine becomes: check whether
  trigger conditions are met; if yes, run the trigger; waive
  explicitly in conversation if overriding.
- The candidate new tools (`/decide` convention, agent-session
  capture, rigour-review agent) from the earlier discussion remain
  deferred; build on first concrete need, not speculatively.

### Revisit triggers

- A trigger fires repeatedly without catching anything — may be
  the wrong trigger or wrong condition. Tune.
- A failure occurs that a trigger should have caught but didn't —
  tighten the trigger condition.

---

## Decision 8 — 2026-04-26: Forward-fit nulls in true-date space (supersedes Decision 2's Poisson-on-fit MC)

**Status:** committed
**Decided by:** Shawn 2026-04-26 (after CC pilot validation)
**Supersedes:** Decision 2's MC mechanism (the rest of Decision 2 — Python port, ~200 LOC, scipy backbone — stands).

### Context

The H1 v1 simulation ran on 2026-04-25 and discovered catastrophic false-positive-rate inflation in the parametric-null Monte Carlo envelope: exponential null FP=1.000 at empire n=50 000, ≥ 0.95 at province n ≥ 500; CPL-3 well-controlled at small n but degrading to ≥ 0.50 at province / urban-area n ≥ 2 500. 88 of zero-bracket cells exceeded the preregistered 0.05 FP target. Investigation surfaced two compounding root causes:

1. **Variance-structure mismatch.** The MC sampler drew `Poisson(fitted_mean)` per bin, giving variance ≈ `fitted_mean`. The observed SPA carried bootstrap-and-aoristic-resample variance, which is roughly `n × p_eb (1 − p_eb)` summed over events e — typically 5–10× larger than `Poisson(mean)` for inscription widths around 50 y. MC envelopes were too tight; observed routinely fell outside.
2. **Null fitted in already-smeared SPA space.** `fit_null_exponential` and `fit_null_cpl` in `primitives.py` fit the null to `observed_spa`, which is itself a single aoristic-smeared realisation. Drawing synthetic events from this fit and re-applying empirical widths via aoristic resampling double-smears the MC. Even after attempting an Option A "aoristic-resample-from-fit" port of rcarbon's `calsample` mechanism (`experiment_aoristic_mc.py::sample_null_spa_aoristic`), FP went from 0.535 to 1.000 — worse, not better.

A non-parametric row-bootstrap MC (Option C; `sample_mc_nonparametric`) controlled FP empirically (0.033 mean across 80-cell sapphire validation grid) but failed a deeper test: under the bootstrap principle, observed and MC are exchangeable when both are drawn from the same corpus, so Option C cannot detect features that exist in the corpus (e.g. real Antonine Plague dip, real growth-decline shape). It is the wrong null for H3b's deviation-detection question.

### Options considered

- **A — Status quo (Poisson-on-fit, smeared-space null).** Reject. Confirmed broken at all but the smallest n.
- **B — rcarbon-port "Option A" (aoristic-resample-from-fit) with fit on smeared-space SPA.** Reject. Double-smear failure mode confirmed empirically.
- **C — Non-parametric row-bootstrap envelope.** Reject for H3b. Cannot detect features that live in the corpus. Acceptable as H1-only power calibration but not as a unified pipeline.
- **D — Forward-fit in true-date space (this decision).** Fit `f(t; θ)` by maximum likelihood treating each row's `[nb_i, na_i]` as the observation and integrating density over the interval (no smearing absorbed into the fit). Generate MC by sampling synthetic true dates from the fitted true-date density, drawing widths from the empirical width distribution, applying aoristic resampling once. Variance structures match between observed and MC; null is in true-date space; detection power against real events is preserved.
- **E — baorista (Crema 2025) Bayesian posterior predictive.** Defer. Decision 3 already keeps baorista as appendix sensitivity. Promoting to primary requires R + NIMBLE + C++ install on sapphire and significant additional integration; not justified when forward-fit works.
- **F — ADMUR / CPL likelihood ratio test (Timpson 2021).** Defer. A principled alternative to envelope tests; not the same statistical question (likelihood ratio between two specified models, vs envelope deviation from a single null). Worth flagging as a follow-up sensitivity.

### Decision

**Option D — Forward-fit nulls in true-date space.** The fitted density `f(t; θ)` describes the underlying date density; aoristic smearing is forward-applied to MC replicates via `t_synthetic ~ f(t; θ̂)` → empirical width assignment → aoristic-resample → bin. Implementation: `runs/2026-04-25-h1-simulation/code/forward_fit.py` (exponential, pilot-validated 2026-04-26 commit `0974fa3`); `runs/2026-04-25-h1-simulation/code/forward_fit_cpl.py` (CPL k ∈ {2, 3, 4}, in progress).

**Coupled change:** the H1 simulation framework moves from the v1 "bootstrap n rows from real LIRE → aoristic-resample → observed_spa → fit null on observed → MC" loop to a "synthetic data drawn from a specified ground-truth null → aoristic-resample → observed_spa → fit null forward → MC" loop. This matches the prereg's intent ("Simulate a synthetic SPA under the null") which the v1 implementation did not honour, and is required for proper power calibration: under H0, observed must come from the null, otherwise the test asks the wrong question.

### Consequences

- **What this makes easier.** FP control is recoverable in principle (pilot demonstrated mean FP = 0.040 across synthetic Part A grid, 0/9 cells > 0.10). The methodology is documented as a clean port of rcarbon's `calsample` design once the smearing / fitting space is sorted. H3b deviation detection retains power against real events because the null is parametric, not bootstrap-of-self.
- **What this makes harder.** Implementation is more substantial than v1 (closed-form integral likelihood for exponential is clean; CPL requires per-segment trapezoidal integration and L-BFGS-B with random restarts to handle multimodality). The prereg's H1 framework requires substantive amendment (bootstrap-from-LIRE → synthetic-from-null), and §3 / §4 / §6 / §8 need updating for the v2 numerical thresholds.
- **What this commits us to downstream.** Forward-fit primitives are now the canonical null-fit machinery for the project. H2 mixture validation and H3 substantive analyses will use them. The original `primitives.py::fit_null_exponential` and `fit_null_cpl` remain in the repo as the v1 record but are no longer in the pipeline.
- **What we accept.** Slightly more implementation complexity; one additional methodological caveat (the position-uniform-within-interval assumption for synthetic interval construction); a reduced-but-real risk that CPL forward-fit will hit multimodality that random restarts can't tame (mitigated by the L-BFGS-B-with-restarts pattern; differential evolution as fall-back).

### Revisit triggers

- CPL forward-fit validation fails (Part A FP > 0.20). Fall back to exponential-only as primary null with CPL as "future work" sensitivity.
- baorista becomes practically deployable on sapphire and gives substantively different results from forward-fit. Promote baorista from sensitivity to alternative-primary.
- Reviewers push hard on the position-uniform-within-interval assumption. Consider adopting a shape-aware position prior (e.g., trapezoidal per FS-3) as a sensitivity.
- Real LIRE has structure beyond what CPL k = 4 captures (Part C behaviour suggests this is plausible). Consider higher-k CPL or kernel-density nulls as exploratory.

### References

- `runs/2026-04-25-h1-simulation/decisions.md` (Decisions 1–7 of the H1 design; this Decision 8 supersedes the MC mechanism in Decision 2).
- `runs/2026-04-25-h1-simulation/outputs/REPORT.md` (v1 broken FP table — the empirical motivation).
- `runs/2026-04-25-h1-simulation/outputs/option-c-validation/SUMMARY.md` (Option C validation; demonstrates non-parametric path is FP-clean but wrong-null for H3b).
- `runs/2026-04-25-h1-simulation/outputs/forward-fit-pilot/SUMMARY.md` (exp forward-fit pilot — the gate-passing evidence).
- `planning/prior-art-scout-2026-04-25-aoristic-envelope.md` (literature scan; §8 empirical addendum on why scout-recommended Option A failed).

---

## Decision 9 — 2026-04-26: H1 v2 precision and compute envelope (drop CPL k=2; optimise forward-fit; rerun at full preregistered precision)

**Status:** committed
**Decided by:** Shawn 2026-04-26 (after critical-friend review of agent-shipped preliminary v2)
**Supersedes:** Decision 6's H1 wall-time estimate (~20 min on sapphire). Forward-fit CPL is ~8 × slower per iteration than v1's smeared-space CPL because per-row interval-likelihood scales with `n_obs` rather than `n_bins`.

### Context

The CPL forward-fit + H1 v2 agent (commits `9b37e1b`–`1ded896`, 2026-04-26) shipped a preliminary v2 at **n_iter = 100, n_mc = 200** — silently reduced from the preregistered 1000/1000 to fit a 60-min hard cap. Wilson 95 % CI on a 0.80 detection rate at n_iter = 100 is [0.715, 0.866] (width 0.151) — too wide for confident threshold-setting at the 0.80 boundary. The shipped v2 is preliminary, not prereg-ready.

Three cost lines compound: (i) forward-fit CPL is ~8 × slower than the smeared-space v1 baseline; (ii) k ∈ {2, 3, 4} sweep triples the CPL-side compute; (iii) preregistered 1000/1000 precision multiplies vs the agent's 100/200 by 100 ×. Naive full 1000/1000 at current speed: ≈ 94 hours sapphire.

Separately, Stage 3 / Stage 5 evidence shows **CPL k = 2 systematically biases to FP = 1.0 at high n** (province ≥ 10 000, all empire) on a 3-knot ground truth. k = 2 is structurally underfit; cannot represent LIRE's empirical shape. Carrying k = 2 into the primary cell grid wastes ~33 % of CPL compute on cells that the validation has already shown are misspecified.

### Options considered

- **A — Accept the preliminary 100/200 v2 with documented deviation.** Reject. CI width 0.151 makes threshold determination at 0.80 statistically meaningless for binding cells.
- **B — Run full 1000/1000 with k ∈ {2, 3, 4} at current code speed.** Reject. ~94 h sapphire; not feasible in any reasonable timeframe; wastes compute on known-broken k = 2.
- **C — Reduce parameters to a documented-deviation level (e.g. n_iter = 500, n_mc = 500) and ship.** Reject. Still a deviation; statistical precision (CI width 0.071) is borderline; sets a precedent of soft-shipping.
- **D — Drop k = 2 from the primary grid + optimise CPL fit + rerun at full 1000/1000.** Accept. Drops ~33 % of CPL compute outright. Optimisation (group-by-interval, vectorise, JIT) targets ≥ 5 × speedup. Combined: ~12 × reduction → ~7 h sapphire at full precision. Aggressive parallelisation (target 80 % machine utilisation) closes any remaining gap.

### Decision

**Option D.** Three coupled changes:

1. **Drop CPL k = 2 from the primary cell grid.** k = 3 primary, k = 4 exploratory upper bound, k = 2 referenced in the prereg as "documented underfit; tested in pilot, excluded from primary because it cannot represent the LIRE 3-knot AIC-best truth." H1 v2's k-sensitivity narrows to k ∈ {3, 4}.
2. **Engineer the CPL forward-fit code for performance.** Profile first, then apply targeted optimisations:
   - Group rows by `(nb, na)` intervals — many inscriptions share dating bands; compute integral once per unique interval, multiply by row count.
   - Vectorise per-row integration across all rows in a single numpy operation (broadcast over segments × rows).
   - Pre-compute segment-overlap masks given fixed knot positions; reuse across L-BFGS-B evaluations within a single fit.
   - Numba `@njit` on the inner integration loop if numpy alone doesn't reach the speedup target.
   - Aggressive joblib parallelisation; saturate sapphire's 24 cores at ≥ 80 % utilisation.
   Target: ≥ 5 × speedup vs the agent-shipped implementation. Re-validate via Stage 1 unit tests + a re-run of the 30-cell Stage 3 grid; results must match the pilot's PASS verdict within MC noise.
3. **Rerun H1 v2 at full preregistered precision.** n_iter = 1000, n_mc = 1000 per cell. **No wall-time cap.** Cells: 3 levels × 4 brackets × 2 shapes × n-sweep × 2 nulls (exp + CPL k = 3) plus CPL k = 4 stored per iteration for k-sensitivity. Total ≈ 192 cells. Estimated wall: ~6–10 h on sapphire post-optimisation.

### Consequences

- **What this makes easier.** Prereg-ready threshold determination with CI width ~0.025 at the 0.80 boundary. Prereg amendment language can use precise numerical thresholds rather than "preliminary" qualifiers. CPL k-sensitivity narrows but is honestly characterised.
- **What this makes harder.** Engineering time for optimisation (~4–8 h focused). Slightly longer overall sprint. Drops the lowest-flexibility null model (k = 2) from primary, which a reviewer might query — answered by referencing the validation-grid evidence that k = 2 is structurally underfit on a 3-knot truth.
- **What this commits us to downstream.** Optimised forward-fit primitives become the canonical H2 / H3 fit machinery. H2 mixture and H3a NBR will use these.
- **What we accept.** Larger compute investment up front; one less k-sensitivity data point (k ∈ {3, 4} instead of {2, 3, 4}); possible engineering-side risk if optimisation hits unexpected pathologies.

### Revisit triggers

- Optimisation fails to deliver ≥ 5 × speedup → escalate to numba JIT + cython if needed; or accept a documented n_iter / n_mc reduction (e.g. 500/500) with widened CIs flagged in REPORT.md.
- CPL k = 4 also shows underfit issues at high n on revalidated grid → reduce to k = 3-only primary; document.
- Re-run reveals materially different threshold structure from the preliminary 100/200 (beyond expected CI narrowing) → triggers diagnostic review.
- Memory pressure during full 1000/1000 run on sapphire → chunk by cell or reduce parallel workers.

### References

- `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2.md` — preliminary v2; relabel as `h1-v2-preliminary/` and tag `PRELIMINARY — NOT PREREG-READY` in the header.
- `runs/2026-04-25-h1-simulation/outputs/forward-fit-pilot/SUMMARY-CPL.md` — Stage 3 PASS validation; basis for trusting the methodology.
- `runs/2026-04-25-h1-simulation/code/forward_fit_cpl.py` — current implementation; target of optimisation.
- Decision 6 — superseded on H1 wall-time estimate; the rest stands.
- Decision 8 — the methodological pivot to forward-fit; this Decision 9 is the precision-and-compute companion.

---

## Decision 10 — 2026-04-26: c_20pc_25y bracket — preregistered hard-test boundary; retired from H3b confirmatory eligibility list

**Status:** committed
**Decided by:** Shawn 2026-04-26

### Context

The H1 v2 preliminary results show **all `c_20pc_25y / step` cells unreachable across all (level × null × k)** combinations and `c_20pc_25y / gaussian` unreachable across all province cells and most urban-area cells. Detection at n = 10 000 / 20 % / 25 y (the smallest effect-size bracket per Decision 5) sits at 0.24–0.40 across CPL truths in the synthetic-data grid. The pattern is robust at low statistical precision and consistent with the underlying difficulty: a 20 % multiplicative deviation over a 25 y window is at the noise floor of permutation-envelope methods on aoristic SPA at any feasible inscription corpus size.

Two distinct uses of this bracket in the prereg:
1. **H1 power-calibration boundary.** "What is the smallest detectable effect at preregistered n?" — anchors the bottom of the power curve.
2. **H3b confirmatory eligibility.** "Which (level × bracket) cells enter confirmatory testing?" — gated on H1 detection ≥ 0.80 at the cell's n.

The two roles are separable: a bracket can be *preregistered as a hard test* without being *preregistered as confirmatory-eligible*.

### Decision

**Keep `c_20pc_25y` in H1 v2 as a preregistered hard-test boundary; remove from H3b confirmatory eligibility list.**

The H1 framework continues to test detection at this magnitude × duration; cells where detection < 0.80 at n_max are tagged `min_n_unreachable: True` in the v2 schema rather than imputing a fictitious extrapolated threshold. The bracket appears in the prereg's effect-size table (§6) with explicit "preregistered as hard-test boundary; not in H3b confirmatory family" annotation. The H3b confirmatory family (Holm–Bonferroni corrected) reduces to `a_50pc_50y` and `b_double_25y` at preregistered (level × shape) cells where H1 yields a finite min-n threshold.

### Consequences

- **What this makes easier.** Honest power-curve reporting with the lower boundary preserved. Reviewer-facing answer to "could you have detected smaller effects?" is preregistered: "no, here's the 20 %-25 y validation showing detection rate caps at 0.40 at n = 10 000, even with optimised methodology." H3b confirmatory family is statistically tractable (smaller, well-powered, Holm–Bonferroni manageable).
- **What this makes harder.** None substantively. The bracket's compute is already in the H1 grid; running it costs nothing extra.
- **What we accept.** Honest narrowing of H3b confirmatory scope to brackets that the methodology can detect.

### Revisit triggers

- Optimised H1 v2 changes the unreachable-cell map materially (e.g. some province `c_20pc_25y / gaussian` cells become reachable at high n). Reconsider including specific reachable cells in the H3b confirmatory family.
- A future methodological development (e.g. baorista posterior predictive, ADMUR likelihood ratio) gives a different power profile for small-magnitude effects. Re-evaluate the bracket's confirmatory eligibility under the new methodology.

### References

- `runs/2026-04-25-h1-simulation/outputs/h1-v2/REPORT-v2.md` — preliminary unreachable-cell map (to be confirmed by full-precision rerun per Decision 9).
- Decision 5 — original effect-size bracket selection (a/b/c).
- Prereg §4 H3b — confirmatory family definition; will be amended to limit family to `a_50pc_50y` and `b_double_25y` at H1-reachable cells.

---

## Decision 11 — 2026-05-14: Submission venue — commit to JAMT (resolves Decision 7's open scope-commitment item)

**Status:** committed
**Decided by:** Shawn 2026-05-14
**Resolves:** the open submission-venue item carried in Decision 7's
"scope commitment path" (single combined paper; JAMT methods-heavy
vs JAS balanced; commit by end of Week 1 of the paper sprint).

### Context

Decision 7 set a single combined paper as the default and named two
candidate venues — JAMT (*Journal of Archaeological Method and
Theory*, methods-heavy) and JAS (*Journal of Archaeological Science*,
balanced) — with the venue commitment due by end of Week 1 of the
paper sprint. That checkpoint has now arrived. The preregistration is
being brought to a clean lodgement-ready state and carried an "open
design decision" placeholder for the venue; that placeholder needs to
resolve so the preregistration can drop its open-decisions list.

### Options considered

- **A — JAMT** (methods-heavy). The paper's primary contribution is
  methodological — the deconvolution-mixture correction for
  editorial-convention artefacts, the forward-fit permutation-envelope
  machinery, and the small-N trajectory-estimation diagnostic. JAMT's
  readership and scope match a paper whose headline is a method, with
  an illustrative substantive finding.
- **B — JAS** (balanced). Broader archaeological-science readership;
  would suit a paper weighted more evenly between method and
  substantive result.

### Decision

**Option A — JAMT.** The paper's centre of gravity is methodological:
the substantive population-variance decomposition is framed throughout
as the *illustrative* application, not the headline. JAMT is the
correct readership for that balance.

This decision is recorded here as the auditable venue commitment. The
preregistration itself does **not** name a target venue — naming a
journal in a preregistration is unnecessary and premature, and the
preregistration is a method-and-hypothesis record, not a submission
plan. The venue lives in this log.

### Consequences

- The preregistration's "Open design decisions" list can be removed in
  full (this was its last unresolved item).
- Drafting can target JAMT's length conventions and methods-forward
  structure from the outset.
- If the methodology content grows past the Decision 7 split-trigger
  thresholds during drafting, the single-vs-split question reopens —
  but the venue for the methods component would remain JAMT.

### Revisit triggers

- Decision 7's split-trigger conditions fire during drafting (methods
  content exceeds ~3,000–4,000 words; deconvolution and baorista
  diverge substantively; the Aeneas-partition outline suggests a
  natural companion submission).
- JAMT scope or submission guidelines turn out to be a poor fit on
  closer reading of recent issues.

---

## Decision 12 — 2026-05-14: Rescope the primary research question; promote the variance partition to confirmatory via a within–between H3a specification

**Status:** committed
**Decided by:** Shawn 2026-05-14 (arising from the adversarial
pre-lodgement review of the preregistration; CC laid out the options,
Shawn chose Option B + Fix B; external sanity-check with Adela
Sobotková and a statistician pending before lodgement).

### Context

The adversarial pre-lodgement review of `preregistration-draft.md`
(two independent fresh-context agents, 2026-05-14) flagged, as a
consensus BLOCKING finding, that the primary research question —
"what fraction of the temporal and spatial variation … is accounted
for by urban population" — was answered only by an analysis filed as
*exploratory* (the §5 variance partition, "no pre-committed numerical
target"). The confirmatory hypothesis H3a tested only whether Bayesian
R² cleared 0.25 / 0.50 thresholds — a "does population correlate at
all" question, not a "what fraction" question.

Two further problems were bundled in:

- The variance partition as written decomposed `Var(log E[insc])` into
  `Var(β·log_pop) + Var(α_province) + residual` as if additive, but
  `log_pop` and `α_province` are correlated (provinces differ
  systematically in their city-size distributions), so the cross-
  covariance term `2·Cov(β·log_pop, α_province)` was silently dropped
  and the three "proportions" do not sum to one.
- The primary RQ asked about "temporal and spatial" variation, but the
  variance partition is purely cross-sectional (city-level
  `log(E[inscriptions_city])`) — the temporal half was decomposed by
  nothing.

### Options considered

**For the confirmatory-status problem:**

- **A — Narrow the RQ to match the existing confirmatory analyses.**
  Rewrite the primary RQ to ask only whether population correlates
  above a threshold. Pro: near-zero new work; honest. Con: a retreat
  from the more interesting, project-defining "what fraction"
  question.
- **B — Promote the variance partition to confirmatory, fix its
  specification, and pre-commit a falsifiable rule.** Pro: the primary
  RQ is genuinely answered; stronger paper. Con: requires a model-
  specification change and a pre-committed decision rule.

**For the variance-partition mis-specification:**

- **Fix A — Report the covariance term explicitly** as a fourth
  bucket so the components sum to the total. Pro: trivial; fully
  honest; no model change. Con: a covariance term is not
  interpretively clean; population's share would have to be reported
  as a range (unique part, to unique + shared), weakening the
  confirmatory claim.
- **Fix B — Within–between ("Mundlak") specification.** Split
  `log(population)` into a province-mean component and a within-
  province deviation, with separate coefficients. The within-province
  deviation is orthogonal to province membership by construction, so
  its variance component is unambiguous; the between-province
  component remains entangled with `α_province`, but that entanglement
  is a named, genuine identification limit rather than a dropped
  covariance. Standard and citable (Mundlak 1978; Bell & Jones 2015).

### Decision

**Option B, with Fix B.**

- The variance partition is promoted from exploratory to the
  confirmatory primary quantitative result, replacing the R²-threshold
  framing of H3a.
- H3a is respecified as a within–between (Mundlak) negative-binomial
  regression: `log(population)` split into province-mean and
  within-province-deviation components with separate coefficients
  (`β_between`, `β_within`).
- The confirmatory estimand is the **within-province
  population-attributable variance fraction** — orthogonal to province
  membership, hence unambiguous.
- The decision rule is a **well-defined estimand plus a falsifiable
  rule**, not a pre-committed point target: the posterior
  population-attributable variance fraction is reported with its 95 %
  credible interval, and H3a is "supported" if the CI excludes a low
  value (to be pinned and justified, e.g. 0.10) — the claim is
  "population explains a non-trivial share," with the fraction itself
  as the estimate.
- The between-province population gradient is reported but explicitly
  flagged as not fully separable from province-level "everything
  else," connecting to the existing identifiability limitation in the
  prereg's Known Limitations section.
- "Temporal" is dropped from the primary RQ; the primary RQ becomes
  spatial and within-province. Temporal structure is addressed by a
  separate, explicitly exploratory analysis (see Decision 13).
- The estimand *scale* — variance decomposed on the latent/log scale
  vs the response scale — is to be stated explicitly in the prereg.

### Consequences

- The H3a model specification in the prereg's Analysis Pipeline
  section must be rewritten (province-mean predictor added; β split
  into `β_within` and `β_between`).
- The primary RQ, the H3a hypothesis statement, and the effect-size
  table all change together; the exploratory variance-partition item
  is removed and folded up into confirmatory H3a.
- The confirmatory claim is narrower than the original sweeping
  "fraction of temporal and spatial variation" — but it is one the
  analysis can actually defend.
- A pre-committed low-value threshold for the falsifiable rule still
  needs to be chosen and justified.

### Revisit triggers

- Adela Sobotková or the external statistician consultation
  identifies a problem with the within–between specification or
  recommends a different estimand (e.g. ICC, commonality analysis).
- Prior-predictive or model-fit checks show the within–between NBR is
  not well-identified on the data.

---

## Decision 13 — 2026-05-14: Temporal structure addressed by a bounded, exploratory "habit-removed residual trajectory" analysis

**Status:** committed
**Decided by:** Shawn 2026-05-14 (arising from the adversarial
pre-lodgement review; follows Decision 12's removal of "temporal"
from the primary RQ).

### Context

Decision 12 dropped "temporal" from the primary research question
because the confirmatory variance partition is purely cross-sectional.
But the temporal dimension is a genuine strength of inscription SPA —
it yields a time series per city, where Hanson (2016) gives only a
single maximum-population estimate per city — and the project wants an
exploratory analysis that uses it.

The naive design (compare a city's raw SPA peak to an independently
known demographic-peak date) is confounded: the epigraphic habit has
its own empire-wide temporal shape (the MacMullen / Meyer "rise and
fall of the epigraphic habit"), so a raw peak-to-peak comparison
largely measures the habit, not the city.

### Options considered

**Analysis design:**

- **Raw peak-to-peak** — compare each city's raw SPA peak to an
  independent demographic-peak date. Rejected: confounded by the
  empire-wide epigraphic-habit curve.
- **Habit-removed residual trajectory** — decompose each city's SPA
  trajectory into an empire-wide habit component plus a city-specific
  residual trajectory, and validate the *residual* against
  independent temporal evidence. Mirrors the spatial residual logic
  of H3c; controls for the habit confound.

**Scope of independent temporal anchors:**

- **Comprehensive assembly** — assemble independent dates for as many
  cities as possible. Rejected: a multi-month deep-research project,
  beyond this paper's scope.
- **Foundation dates only** — cheap, abundant, well-attested; a
  colony founded in AD X should show ~zero SPA mass before AD X.
- **Bounded case-study set** — foundation dates corpus-wide, plus a
  deliberately time-boxed set of cities for which richer independent
  dates can be assembled without open-ended research.

### Decision

A **bounded, exploratory "habit-removed residual trajectory"
analysis**:

- Each city's SPA trajectory is decomposed into an empire-wide habit
  component and a city-specific residual trajectory; the residual is
  what is compared to independent evidence.
- **Anchor types, by priority:**
  - **Foundation dates** — applied corpus-wide; weighted most heavily
    (cheap, abundant, sharp: ~zero SPA mass expected before
    foundation).
  - **Independent peak-population dates** — assembled for a bounded
    case-study set of cities only; compared as posterior-CI
    calibration (does the independent date fall within the posterior
    peak-time credible interval), not point-to-point matching.
  - **Multi-point independent trajectories** — for the few
    well-studied cities where they exist; full-shape comparison
    (overlaps and extends the existing Layer B validation gate in the
    prereg's exploratory section).
  - **Ordinal flourishing-era rankings** — where absolute dates are
    unavailable; rank-correlation of SPA-peak order against
    independent ordinal knowledge.
- A *systematic* offset between city-specific inscription peaks and
  independent demographic peaks is reported as a **quantitative
  estimate of the epigraphic-habit lag** — a methodological finding,
  not a failure.
- The analysis is **exploratory throughout** — no pre-committed
  thresholds; the independent-anchor evidence is too sparse and
  uncertain to bind.
- Scope is **explicitly bounded**: foundation dates corpus-wide plus a
  time-boxed case-study set for richer anchors; comprehensive
  independent-date assembly is out of scope and deferred.

### Consequences

- Extends and partly absorbs the existing Layer B validation gate in
  the prereg's exploratory section, which already proposes comparing
  trajectories to independent estimates for specific cities.
- Adds an exploratory analysis to the prereg; no confirmatory
  hypotheses, no effect-size-table rows.
- Requires a bounded literature task (assembling the case-study
  anchors) — to be time-boxed, not open-ended.
- The empire-wide habit-component estimate becomes a reusable
  intermediate, also relevant to the H3b deviation-detection work.

### Revisit triggers

- The bounded case-study anchor assembly yields too few usable cities
  to support even an exploratory analysis.
- The habit-component decomposition proves unstable or ill-defined in
  practice.

---

## Decision 14 — 2026-05-14: Validate the deconvolution-mixture model with a recovery simulation; respecify it as a Bayesian mixture

**Status:** committed
**Decided by:** Shawn 2026-05-14 (arising from the adversarial
pre-lodgement review; external sanity-check with the statistician
consultation pending before lodgement — this is a primary item for
that consultation).

### Context

The adversarial pre-lodgement review flagged, as a BLOCKING finding,
that Phase 2 — described as "H2 mixture-model validation" — does not
actually validate the deconvolution-mixture model, which is the
paper's central methodological contribution:

- There is no independent ground truth for what the "genuine" SPA is,
  so none of H2.1–H2.4 tests whether the deconvolution recovers the
  *correct* answer.
- H2.1 ("α > 0") is already known true from the measured 22–41×
  century-midpoint spikes — a non-hypothesis.
- H2.2 ("corrected spikes shrink toward the neighbourhood mean") is
  guaranteed by construction; the deconvolution is built to do
  exactly that.
- H2.4 checks the mixture's genuine_SPA against a
  stratified-by-convention-class SPA — but both use the same
  convention-vs-precise row classification, so their agreement is
  internal consistency, not validation. If the classification is
  wrong, both are wrong together.
- The Phase 1 simulation validated the permutation envelope, not the
  mixture model.

The review separately flagged that the deconvolution is
under-specified and likely ill-posed: linear deconvolution with
non-negativity constraints is an ill-conditioned inverse problem when
the convention basis is broad (uniform century slabs overlap heavily
with any smooth genuine signal); no regulariser or smoothness prior is
stated; the estimator is left as "ML or mixture-model fit"; and
α-versus-convention-shape identifiability is not addressed.

### Options considered

**Validation:**

- **1 — Recovery simulation.** Construct synthetic observed_SPA from a
  known genuine_SPA + known α + known convention_SPA, run the mixture
  model, check it recovers α and the genuine shape within tolerance
  across a pre-specified grid. Genuine ground-truth validation;
  mirrors the Phase 1 structure; forces full specification of the
  model. Cost: a bounded new build, reusing Phase 1 infrastructure.
- **2 — Honest relabelling.** Keep H2.2–H2.4 but stop calling them
  "validation"; relabel as internal-consistency / robustness checks;
  fix the abstract. Zero new work, but leaves the central
  contribution with no validation at all — unacceptable for a
  methods-journal submission.
- **3 — Hybrid.** Recovery simulation as the actual validation (a new
  confirmatory hypothesis with a real decision rule, which also
  dissolves the H2.1 non-hypothesis problem) plus honest relabelling
  of H2.2–H2.4 as the supporting consistency / robustness layer on
  real data.

**Model specification:**

- **Linear deconvolution + explicit regulariser** — keep the current
  approach, add a stated smoothness constraint to stabilise the
  inverse problem.
- **Bayesian mixture model** — respecify the deconvolution as a
  Bayesian mixture with explicit priors on the convention and genuine
  components. Coherent with the rest of the pipeline (the H3a NBR and
  baorista are Bayesian); priors regularise the ill-posed inverse
  problem naturally; yields a proper posterior on α instead of a
  bootstrap interval.

### Decision

**Option 3, with a Bayesian mixture model.**

- The deconvolution-mixture model is respecified as a **Bayesian
  mixture** with explicit priors on the convention and genuine
  components. This pins the estimator (no "ML or mixture-fit"
  ambiguity), regularises the ill-posed inverse problem via the priors
  rather than an ad-hoc constraint, and reports α with a posterior
  credible interval (replacing the bootstrap interval in the
  uncertainty-quantification table).
- A **recovery simulation** is added as the genuine validation:
  synthetic observed_SPA built from known genuine_SPA + known
  α + known convention_SPA, across a pre-specified grid; the model
  must recover α and the genuine-SPA shape within a pre-specified
  tolerance. This becomes a confirmatory hypothesis with a real,
  falsifiable decision rule, and replaces the H2.1 non-hypothesis.
- H2.2–H2.4 are retained but **honestly relabelled** as the supporting
  internal-consistency and robustness layer on real data — not
  "validation." The abstract is corrected accordingly.

### Consequences

- New bounded work: building the recovery simulation (reuses Phase 1
  simulation infrastructure) and respecifying the mixture model in a
  Bayesian framework.
- The Analysis Pipeline, the H2 hypothesis statements, the abstract,
  the effect-size table, and the uncertainty-quantification table all
  change together.
- The Bayesian mixture is a larger modelling commitment than the
  within–between tweak of Decision 12; it is a primary item for the
  statistician consultation.
- If the recovery simulation shows the deconvolution does not recover
  known answers well, that is a genuine finding — a characterised
  limit of the method, like the Phase 1 reachability map — not scope
  creep, and is reported as such.

### Revisit triggers

- The statistician consultation recommends a different validation
  design or a different mixture specification.
- The recovery simulation proves unexpectedly hard to specify, or the
  Bayesian mixture does not fit stably — in which case the
  linear-deconvolution-plus-regulariser fallback is reconsidered.

---

## Decision 15 — 2026-05-14: Recast H3b as pre-specified exploratory deviation-detection

**Status:** committed
**Decided by:** Shawn 2026-05-14 (arising from the adversarial
pre-lodgement review).

### Context

The adversarial pre-lodgement review flagged, as a consensus BLOCKING
finding, that H3b's confirmatory decision rule — a departure
"matching at least one preregistered effect-size bracket … at one or
more preregistered (subset × temporal-window) combinations" across a
12-cell grid — is near-unfalsifiable: a 300-year corpus contains some
real historical structure, so something deviates somewhere. The
(subset × temporal-window) combinations were also never actually
enumerated, only described by a generative rule.

Two further consensus blockers were tangled into H3b:

- The Antonine test was listed as "H3b primary" and confirmatory
  (≥ 50 % dip ≥ 50 y at AD 165–180) in the effect-size table, but as
  "exploratory … not pre-committed to a specific effect-size
  expectation" in the hypothesis statement and the confirmatory-
  analysis section — a direct internal contradiction.
- The Holm-Bonferroni correction family size (12 cells vs 6) was
  explicitly deferred to "lock time," an unverifiable later choice —
  a researcher degree of freedom.

The underlying question: does the project have a genuinely
pre-committed, specific deviation prediction? The only candidate is
the Antonine test, and the empirical priors genuinely conflict —
Glomb, Kaše & Heřmánková (2022) found a null (KS *p* = 0.20,
N = 210), while Duncan-Jones (2018) found an ~85 % step-down in
military diplomas. Pre-committing a magnitude would be a coin flip
between contradictory secondary sources.

### Options considered

- **A — Treat the Antonine test as confirmatory.** Fully enumerate its
  subsets, window, magnitude, and decision rule; small specified
  family, so the Holm-Bonferroni family-size problem dissolves.
  Rejected: it would require pre-committing an effect size the
  contradictory secondary literature cannot justify.
- **B — Recast H3b as pre-specified exploratory deviation-detection.**
  The temporal windows and subsets to be scanned are enumerated in
  advance (so the analysis is pre-specified, not post-hoc fishing),
  but no effect sizes are pre-committed. The Antonine and
  Crisis-of-the-Third-Century tests become the two named
  pre-specified exploratory probes.

### Decision

**Option B.**

- H3b is recast from confirmatory to **pre-specified exploratory
  deviation-detection**. The temporal windows and subsets to be
  scanned are enumerated in advance; no effect-size brackets are
  pre-committed.
- The Antonine test (AD 165–180) and the Crisis-of-the-Third-Century
  test (AD 235–284) are the two named pre-specified exploratory
  probes; both are reported against the effect-size brackets
  descriptively, neither pre-commits a magnitude.
- The "H3b primary | Antonine signature | ≥ 50 % dip" row is removed
  from the effect-size table; the Antonine confirmatory-versus-
  exploratory contradiction is resolved by H3b being uniformly
  exploratory.
- The Holm-Bonferroni family-size choice (12 vs 6 cells) is moot:
  there is no confirmatory H3b family to correct. Exploratory
  deviation results are reported with their multiplicity noted
  descriptively.
- Phase 1 (H1) still gates H3b — it determines which subset levels
  can detect deviations at all, and H3b is run only where H1
  establishes detection is feasible.

### Consequences

- The paper's confirmatory backbone is now H3a (the variance
  partition, per Decision 12) and H3c (which has genuine pre-committed
  predictions replicating Hanson 2021). H3b is exploratory.
- Field 3, the Phase 3 confirmatory-analysis section, and the
  effect-size table all change: H3b moves out of the confirmatory
  hypotheses; the H3b effect-size rows are removed or relabelled
  exploratory; the multiple-comparison rule is simplified (no H3b
  confirmatory family).
- The deviation-detection work loses nothing in substance — it still
  demonstrates the corrected SPA can detect known historical events —
  but it is honestly framed as discovery, not confirmation.
- This single decision resolves three of the review's consensus
  blockers at once: the H3b unfalsifiability, the Antonine
  confirmatory/exploratory contradiction, and the deferred
  Holm-Bonferroni degree of freedom.

### Revisit triggers

- The statistician consultation argues a defensible confirmatory
  deviation test can be constructed after all.
- New evidence resolves the Glomb / Duncan-Jones conflict enough to
  justify a pre-committed Antonine magnitude.

---

## Decision 16 — 2026-05-15: Drop the regional-pattern clause from H3c-spatial; reduce H3c-spatial to Moran's I clustering only

**Status:** committed
**Decided by:** Shawn 2026-05-15 (arising from the consolidated
Hanson 2021 re-verification and the SDAM-AU library scan; surfaced a
confabulated attribution in the original draft).

### Context

The adversarial pre-lodgement review flagged the H3c-spatial
decision rule's "qualitative pattern matches Hanson's map" clause as
an unoperationalised researcher degree of freedom. The clause stated:
"over-production concentrated in Italy and along the Rhine / Danube
frontier; under-production scattered in Britannia, Gaul peripheries,
and other western edges of the Empire," attributed to Hanson (2021).

Two independent Explore agents reading the full Hanson 2021 PDF
found, with page-anchored verbatim quotes, that this attribution is
**not supported by the paper**. Hanson explicitly states "there does
not seem to be any obvious pattern in the distribution of residuals"
(p. 147) and that sites from different regions are "evenly
scattered" (p. 148). The only spatial-structural claim Hanson does
make is the Moran's I = 0.046 clustering on residuals (Table 7.4,
p. 148), without naming regions. The prereg's specific regional
geography appears to be a confabulation produced in an earlier
drafting session, attributed to Hanson 2021 with high conviction,
and never verified against the source until now.

A subsequent library scan — covering all 8 Hanson items in the
SDAM-AU group and the 22-item `roman_demography` collection, with
PDF abstracts read for items lacking Zotero `abstractNote` entries
— also found no Hanson-corpus paper that makes an explicit
inscription-residual regional claim. Adjacent material exists:
Hanson 2016 has per-province urban-hierarchy analyses; Wilson 2012
contrasts empire-wide vs North African temporal patterns of building
inscriptions; Hanson & Ortman 2020 finds civic-status patterning of
residuals (entertainment structures, not inscriptions). None of
these is an inscription-residual regional-spatial prior of the form
the dropped clause asserted.

### Options considered

- **A — Drop the regional-pattern clause from H3c-spatial.**
  H3c-spatial reduces to Moran's I clustering in ≥ 2 of
  {k = 5, 8, 10}, which is a verified Hanson 2021 replication. Any
  regional pattern observed in the data is treated as descriptive,
  not confirmatory.
- **B — Construct a regional contrast from the patched-together
  Hanson 2016 / Wilson 2012 / Hanson & Ortman 2020 material.**
  Rejected: this would be interpretive scaffolding rather than a
  published prior — exactly the kind of post-hoc construction the
  prereg discipline exists to prevent.
- **C — Read Hanson 2016 chapters 7–8 to confirm there is no
  regional inscription-residual claim in the underlying monograph.**
  Not pursued (Shawn's judgement: not in the book).

### Decision

**Option A.** The H3c-spatial decision rule reduces to:

> Moran's I > 0 at *p* < 0.05 in ≥ 2 of {k = 5, k = 8, k = 10} k-NN
> weights.

The qualitative-pattern clause is removed entirely from the
confirmatory rule and from all three locations where it appeared
(Field 3, §3, §6). Any regional pattern observed in the H3c
residuals is reported descriptively, not as part of H3c-spatial
pass/fail.

The literature identified during the search is folded into adjacent
decisions, not (c)-2:

- **Wilson 2012's** empire-wide vs North African temporal-pattern
  contrast is recorded as an independent anchor candidate for
  Decision 13's bounded temporal case-study set.
- **Hanson 2016's** per-province urban hierarchies inform Decision 13's
  province scoping.
- **Hanson & Ortman 2020's** civic-status residual patterning is
  noted as an additional supporting reference for H3c(i)'s
  provincial-capitals contrast.

### Consequences

- H3c-spatial's decision rule is unambiguously specified across
  Field 3, §3, and §6; the existing §6-vs-Field-3 drift on Moran's I
  is also fixed.
- The H3c confirmatory family remains two tests (capitals contrast,
  clustering) — no expansion, simplifying multiple-comparison
  handling.
- The dropped clause's history is recorded here as part of the
  project's research record.
- A separate concern is raised: this clause's presence in the
  original draft is a confirmed confabulation. The Hanson 2021
  re-verification also caught a second mischaracterisation (the SR1
  "polity × century resolution" wording, which misdescribes
  Hanson's design — Hanson works at site level with cumulative
  inscription counts). Two confirmed confabulations in one source
  warrant a systematic pre-lodgement citation audit of the full
  preregistration (see task #21).

### Revisit triggers

- A direct published inscription-residual regional-spatial prior
  surfaces during further reading and is robust enough to ground a
  pre-specified contrast.
