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
  upstream issues (see `docs/notes/working-notes.md`
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

---

## Decision 17 — 2026-05-15: Editorial-convention hierarchy is real and structured; fold it into the Bayesian mixture as a flexible convention-shape prior

**Status:** **SUPERSEDED by Decision 20 (2026-05-17).** The empirical
grounding for Decision 17's three-tier anchor-year structure
(century-start / end / midpoint, half-century-start, reign-related)
was the 2026-05-15 editorial-convention-hierarchy diagnostic, which
used the integer-truncated-midpoint test statistic `int((nb + na) / 2)`.
Three further diagnostics on 2026-05-17 (interval-width diagnostic;
empirical-SPA shape; date-range-filtered SPAs) established that
(i) the test statistic conflated wide-century-template slabs with
narrow midpoint-anchored intervals, (ii) the actual SPA shows no
anchor-year structure at AD 50/150/250 (local excess −77/−79/+22),
(iii) the dominant artefact is wide-century-template slab loading
(plateau over [1, 100], [101, 200], etc.) and the dominant real
narrow-precision clustering is at reign intervals (AD 77.5 Flavian,
122.5 Hadrianic, 212.5 Severan). Decision 20 replaces the three-tier
anchor-year structure with a template-interval slab structure.
Retained from Decision 17: the principle that the convention-shape
is empirically structured (not a single uniform), the inclusive-Roman
century-counting framing of the artefact, and the use of a
flexible-prior Bayesian-mixture component to estimate tier weights.
**Decided by:** Shawn 2026-05-15 (overnight diagnostic run conclusive;
runs/2026-05-15-editorial-convention-hierarchy/).

### Context

The preregistration's deconvolution-mixture model (now Bayesian per
Decision 14) specifies a `convention_SPA` shape that defaults to
"uniform century slabs," with a contingent shift to a weighted
hierarchical shape gated by an undefined editorial-convention-hierarchy
test on an unspecified 14-boundary sample. The adversarial review
flagged this as a researcher degree of freedom and (c)-3 of the
triage was to either define the gate, drop the hierarchical option,
or fold the choice into the Bayesian mixture itself.

The 2026-04-23 descriptive-stats run had quantified century-midpoint
inflation at AD 50/150/250/350 (observed/expected ratios 22.8 / 41.5 /
18.8 / 39.7) but had not looked at any sub-century structure. An
audit of the 2023-09 and 2026-04 exploratory notebooks plus the
descriptive-stats outputs (2026-05-15) confirmed no systematic
sub-century analysis had been done — but surfaced incidental evidence
in the existing data (mc_ratio 19.7 at AD 100, 8.1 at AD 125, etc.)
that strongly suggested a hierarchy was present.

A targeted five-test diagnostic (top-N endpoint frequencies,
hierarchical O/E by tier, trailing-two-digit histogram, reign-boundary
specific test, and convention-text labelled-subset analysis) was run
on the filtered corpus (180,609 rows). The diagnostic produced a
decisive — and unexpected — answer.

### Empirical findings

The hierarchy is real, large, and structured. Key results (see
`runs/2026-05-15-editorial-convention-hierarchy/outputs/REPORT.md`
for the full report):

- 54.5 % of all `not_before` values end in `01`; 53.0 % of all
  `not_after` values end in `00`. Two-thirds of `not_after` values are
  `00` or `50`; two-thirds of `not_before` values are `01` or `51`.
- The dominant editorial convention is **inclusive-Roman century
  counting**: "Xth century AD" maps to `not_before = (X-1)*100 + 1`
  and `not_after = X*100`. The convention is *explicit* in the
  `raw_dating` field (top values are literally "1 to 100",
  "101 to 200", "301 to 400", with 96–100 % modal endpoint match).
- Tier-by-tier geometric-mean observed/expected ratios (combined
  endpoints, σ = 20 baseline):
  - century-incl-start (year ≡ 1 mod 100): **20.28**
  - century-incl-end (year ≡ 0 mod 100): **18.34**
  - century-midpoint (year ≡ 50 mod 100): **10.16**
  - half-century-incl-start (year ≡ 51 mod 100): **2.44**
  - reign-related (curated 39-year set): 0.75 overall, with 13 years
    Holm-significant; strongest signals at AD 79 (Vesuvius / Titus,
    O/E 4.37), AD 251 (Crisis-era, O/E 3.78), AD 270 (Aurelian,
    O/E 2.78), 27 BC (Augustus, O/E 2.61), AD 138/14/161
    (dynastic transitions, O/E ~2.3).
  - sub-century tiers (quarter-century, decade, lustrum):
    *below baseline* (O/E < 0.51) — depleted, not enhanced.

The preregistration's prior framing of the artefact as
"century-midpoint inflation" is **partial**: midpoint inflation is a
derivative effect of endpoint rounding. An interval like `[1, 100]`
or `[101, 200]` places aoristic mass at midpoint years AD 50 or 150;
the underlying editorial action is rounding the endpoints to
inclusive-Roman century boundaries.

### Options considered

- **A — Commit to uniform century slabs as the convention shape; no
  hierarchical option.** Rejected: would model the data against
  visible, strong evidence (half-century layer has O/E 2.44; reign
  layer has Holm-significant clustering at 13 dynastic/Crisis years).
- **B — Define a pre-test that gates between uniform-century and
  weighted-hierarchical shapes.** Rejected: an undefined pre-test
  was the original problem; replacing it with a defined pre-test
  adds a binary choice the Bayesian mixture can handle directly.
- **C — Fold the convention-shape choice into the Bayesian mixture
  as a flexible prior with explicit tier components.** Accepted:
  empirically grounded, structurally consistent with Decision 14's
  Bayesian respecification, and dissolves the contingent-shape pre-test
  entirely.

### Decision

**Option C.** The `convention_SPA` shape in the Bayesian mixture
takes a flexible prior with explicit tier components, structured by
the diagnostic's empirical findings:

- **Century layer (primary).** Mass at inclusive-Roman starts
  (year ≡ 1 mod 100: AD 1, 101, 201, 301) and inclusive-Roman ends
  (year ≡ 0 mod 100: AD 0, 100, 200, 300), plus the original
  "century-midpoint" set (year ≡ 50 mod 100: AD 50, 150, 250, 350)
  which captures intervals like `[1, 100]` and `[101, 200]` that
  place mass on midpoint years.
- **Half-century layer (secondary).** Mass at year ≡ 51 mod 100
  (AD 51, 151, 251) — half-century inclusive starts. Half-century
  inclusive ends are already captured in the century-midpoint layer.
- **Reign-related layer (tertiary).** Mass at a curated set of
  dynastic-transition and Crisis-era reign years where the
  diagnostic showed Holm-significant clustering: 27 BC, AD 14, 41,
  69, 79, 117, 138, 161, 217, 222, 235, 251, 270. (AD 79 in particular
  is anchored by Vesuvius, not solely by Titus's accession.)
- **No sub-century tiers** — quarter-century, decade, and lustrum
  tiers showed below-baseline O/E and do not need a model component.

The relative tier weights are estimated by the Bayesian mixture; the
prior allows the data to set them within a weakly-informative
half-Normal range.

### Consequences

- The preregistration's §3 deconvolution-mixture spec rewrites to
  reflect endpoint-rounding (not midpoint-inflation) as the artefact
  mechanism, and lists the three tier components above as the
  convention-shape's structure.
- The §2 Description should reference endpoint rounding (and quote
  the trailing-digit statistic — 54.5 % of `not_before` values end
  in `01`) as the artefact's primary manifestation; the original
  century-midpoint ratios are kept as the derivative aoristic-mass
  signal.
- The §7 contingency on the "editorial-convention-hierarchy test"
  is removed — the test is now superseded by the diagnostic findings
  and the model itself.
- The recovery-simulation grid (Decision 14) must include synthetic
  observed_SPAs built from the three-tier convention structure
  identified here, not just uniform century slabs.
- The diagnostic run record is committed to
  `runs/2026-05-15-editorial-convention-hierarchy/` per the project's
  research-record convention.

### Revisit triggers

- The Bayesian mixture's recovery simulation reveals the chosen
  three-tier convention structure is misspecified (e.g. a tier is
  redundant or another tier is missing).
- The statistician consultation (Martin) recommends a different
  decomposition of the convention shape.
- A broader anchor-year list (beyond the curated 39 reign-boundary
  years) reveals additional dating-anchor years not yet in the
  reign-related layer.

---

## Decision 18 — 2026-05-17: H3a confirmatory rule is directional (three-way verdict, with posterior-probability ladder as supplementary reporting)

**Status:** committed
**Decided by:** Shawn 2026-05-17 (arising from the ChatGPT 5.5
cross-model adversarial review of the preregistration; ChatGPT
finding #1, BLOCKING).

### Context

The post-rewrite preregistration (2026-05-16) specifies H3a's
confirmatory decision rule as: "the posterior 95 % credible interval
for the within-province population-attributable variance fraction
`f_within` excludes 0.10." This wording is **symmetric**: a posterior
interval `[0.01, 0.08]` would count as support under the literal
reading, despite being evidence *against* the claim "population
explains a non-trivial share." The wording slipped during the
comprehensive rewrite implementing Decision 12 — Decision 12's stated
intent ("population explains a non-trivial share") is clearly
directional, but the rewrite encoded the symmetric version.

This is a direct hypothesis → decision-rule failure: under the
current rule, an analysis returning a posterior that is *actually
evidence against H3a* would be reported as *supporting* H3a.

### Options considered

- **A — Two-way, directional.** Replace "excludes 0.10" with
  "P(f_within > 0.10) ≥ 0.95" (equivalently, "the posterior 95 % CI
  lies wholly above 0.10"). Simplest fix; restores Decision 12's
  intent. A posterior interval wholly below 0.10 is "not supported"
  but is not formally named as "evidence against."
- **B — Three-way verdict.** Wholly above 0.10 = supported;
  wholly below 0.10 = evidence against; straddling 0.10 =
  inconclusive. Adds a named "evidence against" verdict, forcing the
  paper to report negative findings as informative rather than as a
  soft null.
- **C — Two-way + posterior-probability ladder.** Same as A, plus
  pre-commit to reporting P(f_within > 0.05), P(f_within > 0.10), and
  P(f_within > 0.20) as a posterior-probability ladder regardless of
  the verdict.

### Decision

**B + C's reporting layer.** The H3a decision rule is three-way; the
posterior-probability ladder of C is added as supplementary reporting
alongside the verdict.

- **Decision rule (binding):**
  - **Supported:** posterior 95 % credible interval for `f_within`
    lies wholly above 0.10.
  - **Evidence against:** posterior 95 % credible interval lies
    wholly below 0.10.
  - **Inconclusive:** posterior 95 % credible interval straddles
    0.10.
- **Reporting (supplementary):** the paper reports the full posterior
  of `f_within`, plus P(f_within > 0.05), P(f_within > 0.10), and
  P(f_within > 0.20), regardless of the verdict outcome.

Rationale for B over A: a three-way verdict pre-commits to
falsifiable named outcomes including the negative case. A binary
verdict with the same ladder still tends to read the negative as a
soft null; the three-way wording forces the stronger reading "evidence
against the non-trivial-share claim." The probability ladder is
reporting only — it neither defines nor influences the verdict.

### Consequences

- §3 H3a "Confirmatory estimand and decision rule" rewritten:
  three-way verdict replaces the symmetric "excludes 0.10" wording;
  probability-ladder reporting added.
- Field 3 H3a hypothesis statement updated to the three-way wording.
- §6 effect-size table H3a row updated; the probability-ladder
  reporting added to the same row.
- §6 / Field 3 confirmatory claim hierarchy (which lands as ChatGPT
  triage item C3) needs one additional sentence: what happens to the
  H3 family if H3a returns "evidence against." The natural answer is
  that H3c is still run (it tests Hanson-replication, which is a
  separate question), but the paper's headline result is then
  "H3a evidence against the non-trivial-share claim; H3c results
  reported as Hanson-replication." This is folded into the C3
  resolution.
- The plain-English walkthrough's H3a description (Step 6) needs
  parallel rewording: the rule is now three-way; the negative case
  has a name.

### Revisit triggers

- The statistician consultation (Martin) recommends a different
  threshold than 0.10, or argues that the variance-fraction
  decomposition on the latent (log) scale is the wrong scale for
  this rule.
- Prior-predictive checks suggest the 0.10 threshold is implausible
  *a priori* under the prior (e.g. the prior predictive places > 50 %
  mass above 0.10, making the rule near-vacuous).

---

## Decision 19 — 2026-05-17: Bayesian mixture observation model — multinomial primary; Dirichlet-multinomial and rescaled negative-binomial as supplementary

**Status:** committed; primary item for Martin's consultation
**Decided by:** Shawn 2026-05-17 (arising from ChatGPT 5.5
cross-model review finding #2, BLOCKING — "the Bayesian mixture is
not yet a complete statistical model").

### Context

The Bayesian deconvolution-mixture model (Decision 14) specifies the
deterministic equation `observed_SPA(t) = α · convention_SPA(t) +
(1 − α) · genuine_SPA(t)` and priors on α (Beta(2, 2)), tier weights
(Dirichlet), and genuine-component smoothness (Gaussian random walk
with HalfNormal bandwidth), but the **observation model** is not
specified. Without a likelihood, the posterior is undefined — the
priors alone do not pin down the inferential machinery.

Three sub-questions are tangled in the same gap:

1. The likelihood family itself (multinomial, NegBin, etc.).
2. Whether `convention_SPA` and `genuine_SPA` are normalised densities
   (compositional shape), count intensities (absolute scale), or
   posterior latent curves.
3. Where aoristic uncertainty enters — upstream in the SPA
   construction or carried explicitly into the likelihood (e.g. via
   per-inscription latent-date sampling).

This is the central methodological contribution. The gap is real and
must be closed before lodgement.

### Options considered

- **A — Multinomial on binned aoristic mass.** `y_t ~ Multinomial(N,
  p_t)` with `p_t = α p_conv,t + (1 − α) p_gen,t` and both component
  vectors normalised to sum to 1. Compositional shape inference;
  standard for this problem class; α identifiable as the compositional
  weight; aoristic uncertainty handled upstream.
- **B — Negative-binomial on per-bin counts.** `y_t ~ NegBin(λ_t, φ)`
  with `λ_t = α λ_conv,t + (1 − α) λ_gen,t` on the absolute count
  scale. As initially specified this has a scale-degeneracy problem
  (λ_conv, λ_gen, and α cannot be jointly identified without further
  constraint). **Rescaled form:** `λ_t = N · (α p_conv,t + (1 − α)
  p_gen,t)` with `p` normalised — this is a NegBin reformulation of
  the multinomial that adds per-bin overdispersion without breaking
  identifiability.
- **C — Dirichlet-multinomial.** As A, plus a concentration parameter
  κ to handle bin-level overdispersion. Reduces to multinomial as
  κ → ∞.

### Decision

**Primary (binding confirmatory likelihood): Option A, multinomial.**
**Supplementary (exploratory model-comparison, both reported alongside
the primary):**

- **Option C, Dirichlet-multinomial.** Reports the posterior on κ
  alongside α as a diagnostic of mixture-noise structure. Failure of
  multinomial posterior-predictive dispersion checks (κ posterior
  concentrated on small values) is interpreted as motivation for the
  Dirichlet-multinomial fit being preferred — but the multinomial
  remains the binding H2.1 result and the abstract's stated
  contribution.
- **Option B (rescaled form only), NegBin.** Reports an alternative
  per-bin overdispersion treatment as a cross-check on Option C.
  Reported descriptively; not a confirmatory comparator.

The supplementary analyses are not fishing for a preferred answer: the
H2.1 recovery simulation and the H3 substantive analyses all attach
to the primary multinomial; the supplementary fits are reported as
model-comparison evidence informing whether the multinomial choice was
correct, with revisions (if any) handled via the post-lodgement OSF
amendment mechanism. Shawn's stated rationale: "in other projects
we've sometimes found that we didn't always choose the correct
approach first try; Martin's review should help, but some exploratory
work is still warranted." This is defensible model-checking, not
post-hoc selection.

**Resolving sub-questions 2 and 3:**

- **What `convention_SPA` and `genuine_SPA` are:** normalised densities
  summing to 1 (compositional). Same answer under all three
  likelihoods (Option B uses N · p_t to recover an intensity).
- **Where aoristic uncertainty enters:** upstream in the SPA
  construction. Each mixture fit uses a single per-subset SPA
  computed under the standard pipeline (per-inscription uniform
  aoristic mass, summed to 5-year bins). Propagation of aoristic
  uncertainty through multiple SPA draws into the mixture posterior
  is **not** preregistered as part of the primary or supplementary
  analyses; it is a candidate exploratory extension and a
  statistician question for Martin (whether the loss of upstream
  aoristic-uncertainty propagation is material for α identifiability).

### Consequences

- §3 "Bayesian deconvolution-mixture model" rewritten to state the
  multinomial likelihood explicitly; the supplementary Dirichlet-
  multinomial and rescaled NegBin fits added as named alternative
  parameterisations.
- §4 Phase 2 / H2.1 rewritten to specify which fit is the recovery-
  simulation target (the multinomial); the supplementary fits are
  also recovered (the recovery simulation is run under all three
  likelihoods, with the primary verdict attached to the multinomial).
- §6 effect-size table: H2.1 row updated to clarify the recovery
  rule applies to the multinomial; supplementary-fit results reported
  alongside without separate decision rules.
- Plain-English walkthrough's Step 2 needs a single sentence stating
  that the model treats the SPA as compositional shape data
  (proportions in each 5-year bin) and uses the multinomial as the
  binding likelihood.
- Listed as **primary item for Martin's consultation pack** — the
  multinomial-vs-Dirichlet-multinomial-vs-NegBin choice has
  identifiability and overdispersion consequences that warrant
  statistician review.

### Revisit triggers

- Martin's consultation recommends a different likelihood family
  (e.g. a hierarchical multinomial accounting for tier structure
  explicitly).
- The recovery simulation (H2.1) under the multinomial fails coverage
  or shape-recovery while Dirichlet-multinomial or NegBin passes —
  triggers an OSF amendment promoting the alternative to primary.
- Posterior predictive dispersion checks on real data show the
  multinomial is materially under-dispersed (a known failure mode
  when bin counts have structure the multinomial cannot capture).
- Propagating aoristic uncertainty into the likelihood is judged
  necessary for α identifiability after the recovery simulation runs.

---

## Decision 20 — 2026-05-17: Convention component is a template-interval slab structure (supersedes Decision 17)

**Status:** committed; supersedes Decision 17
**Decided by:** Shawn 2026-05-17 (arising from the ChatGPT 5.5
cross-model review finding #3 BLOCKING; three diagnostics on
2026-05-17 driving the supersession).

### Context

ChatGPT 5.5's review finding #3 noted that under Uniform aoristic, a
wide-century-template interval like `[1, 100]` deposits mass
*uniformly* across all 100 years rather than preferentially on the
midpoint year. So the preregistration's claim that "intervals such as
`[1, 100]` and `[101, 200]` place aoristic mass on midpoint years by
construction" cannot be right under the project's stated aoristic
method — yet the descriptive profiling showed clear 22.8× / 41.5× /
18.8× O/E ratios at AD 50 / 150 / 250. Something is wrong with
either the mechanism explanation, the test statistic, or both.

Three diagnostics were run to resolve this:

1. **Interval-width diagnostic**
   (`runs/2026-05-17-interval-width-diagnostic/`). Established that:
   (i) the corpus is dominated by exact-century-template intervals
   (`[1, 100]` 26.3% of corpus; `[101, 200]` and `[201, 300]` adding
   roughly the same magnitude again); (ii) the headline 22.8 ×
   ratios were generated by `int((nb + na) / 2)` as the observed
   statistic, which makes wide century-template midpoints (50.5,
   150.5, 250.5) truncate to round years — conflating wide-slab
   loading with midpoint-anchored mass; (iii) removing all narrow
   intervals (width ≤ 25) does *not* collapse the spikes — they
   intensify to 25.1 × / 48.3 × / 25.2 × (109 % / 117 % / 132 %
   retention). The dominant artefact is wide-template-slab loading,
   not midpoint anchors.

2. **Empirical-SPA shape diagnostic**
   (`runs/2026-05-17-empirical-spa-shape/`). Constructed the actual
   5-year per-year-uniform-aoristic SPA over 50 BC – AD 350 and
   visualised the shape directly. Found: (i) no local anchor-year
   excess at AD 50 / 150 / 250 (excess −77 / −79 / +22 relative to
   the local plateau); (ii) the largest narrow spikes are at
   AD 122.5 (Hadrian, [117, 138] = 552 inscriptions plus [123, 123]
   = 1,304 inscriptions) and AD 77.5 (Flavian, [78, 79] etc.); (iii)
   the 1 BC / AD 1 boundary is the largest single discontinuity
   (+1,159); (iv) mid-envelope century-boundary steps are modest
   (AD 100 / 101: +96; AD 200 / 201: −547; AD 300 / 301: +180); (v)
   trapezoidal vs uniform aoristic differ quantitatively (per-bin
   Pearson r = 0.94, max relative diff 47.6%) but not qualitatively.

3. **Date-range-filtered SPA diagnostic**
   (`runs/2026-05-17-date-range-filtered-spas/`). Recomputed the
   SPAs under progressive `date_range` thresholds {0, ≤1, ≤10, ≤25,
   ≤50, ≤75, ≤100, ≤200, all}. The decisive findings: (i) regnal
   spikes *amplify* under narrow-precision filtering — AD 122.5
   spike-to-plateau ratio goes 1.61 × → 4.96 × → 13.83 × as we
   tighten from full → ≤ 25 → == 0; (ii) the century-boundary
   plateau-step pattern weakens decisively under narrow filtering
   (Pearson r between SPA( ≤ 25) and SPA( > 100) = 0.34); (iii) a
   third regnal spike at AD 212.5 (Severan, [212, 217] = 728
   inscriptions) emerges. The regnal spikes are *real ancient
   clustering*; the plateau-step pattern is *editorial-encoding
   artefact*.

The implication: Decision 17's three-tier anchor-year structure is
targeting a phenomenon that isn't there (no anchor-year structure at
AD 50 / 150 / 250) while missing the dominant artefact
(wide-template slabs). The structure must be replaced.

### Conceptual clarification — what the convention component models

The convention component should model only the *editorial-encoding
artefact*, not real ancient clustering. Two distinct populations
coexist at AD 122.5:

- **Reign-interval inscriptions** dated `[117, 138]` because the
  editor knows "Hadrianic" but not the exact year. These deposit
  *uniform mass over the reign interval*. **This is editorial
  convention; goes in the convention component.**
- **Year-precise inscriptions** dated `[123, 123]` because the
  inscription carries a consular date or regnal-year stamp. These
  deposit *real point mass at AD 123*. **This is genuine ancient
  anchoring; stays in the genuine component.**

Same logic for centuries: `[101, 200]` dated by an editor unable to
pin the date more tightly is convention; `[123, 123]` is real
history. The two populations are separated by interval width.

### Decision

**Convention component = template-interval slab structure.** A
dictionary of empirically-supported template intervals; mass uniform
over each interval; tier-level weight estimated jointly with α.

- **Dictionary scope:** century templates ([1, 100], [101, 200],
  [201, 300], [301, 400] and BC equivalents), half-century templates
  ([1, 50], [51, 100], [101, 150], [151, 200], etc., where
  empirically supported), reign-interval templates (Augustan
  [27 BC, 14 AD], Tiberian, Flavian, Trajanic, Hadrianic [117, 138],
  Antonine [161, 180], Severan [212, 217], etc.), and any other
  empirically-supported template intervals revealed by the scan.
- **Dictionary-build procedure (pre-Phase-2 implementation step,
  not preregistration substance):** scan the filtered corpus for
  exact-match interval templates; include any template with
  N ≥ a stated threshold (threshold pinned in the implementation
  scan's run report). The committed empirical scan replaces Decision
  17's curated 13-year anchor-year list. The procedural commitment
  is the prereg-binding part; the actual dictionary contents are
  implementation artefacts.
- **Tier structure within the slab component:** template intervals
  are grouped into tiers by template type (century / half-century /
  reign / BC-AD-boundary) for interpretive reporting; the model
  estimates a single weight per tier (each tier's individual
  intervals share weight by total interval-width-normalised mass).
- **Year-precise inscriptions** ([123, 123], single-year encodings)
  are *not* in the convention component — they stay in genuine_SPA.
- **No anchor-year tier.** Mass at AD 50 / 150 / 250 / 350, 51 / 151
  / 251 (Decision 17's century-midpoint and half-century-start
  tiers) is *not* in the model. The empirical diagnostic falsified
  these.

**Aoristic distribution:** uniform aoristic remains primary;
trapezoidal aoristic remains the existing sensitivity (per H3
confirmatory-eligible subset). Trapezoidal is not promoted; the
slab-tier component is a more direct correction for the
"epigraphers anchor on mid-century" intuition than a reshaping of
aoristic mass within wide intervals.

**Observation model:** unchanged — multinomial primary (Decision 19),
Dirichlet-multinomial and rescaled NegBin as supplementary.

### Consequences

- §2 (Description) rewritten: the artefact framing shifts from
  "century-midpoint inflation" to "wide-template-slab editorial
  encoding plus real ancient regnal clustering." The "intervals
  like [1, 100] place aoristic mass on midpoint years" claim is
  removed entirely; replaced with the slab-loading description.
  The 22.8 × / 41.5 × / 18.8 × O/E ratios — which were generated by
  the int-truncated-midpoint test statistic — are reframed as
  diagnostic outputs of one particular test, not as the artefact's
  primary signature in the SPA. The 54.5 % / 53.0 % endpoint-
  rounding statistic remains the primary descriptive evidence.
- §3 (Analysis pipeline / "Convention component") rewritten:
  three-tier anchor-year structure replaced with the template-
  interval slab structure. Dictionary-build procedure named; tier
  structure described.
- Plain-English walkthrough Step 2 rewritten: the "convention
  component" is now described as a wrapper of editorial-template
  intervals (centuries, half-centuries, reign intervals); the model
  removes uniform mass deposited by these wrappers, leaving the
  genuine signal.
- H2.1 recovery-simulation grid (Decision 14; ChatGPT review B4 /
  the in-flight Decision 21) must include synthetic SPAs built
  from the template-interval slab structure, not anchor-year mass.
  The supersession is consequential for the recovery design.
- §6 effect-size table — H2.1 row updated as part of the recovery-
  grid respec.
- §9 known limitations: add a sentence on the BC / AD boundary
  step (+1,159 at the 1 BC / AD 1 boundary in the empirical SPA),
  the single largest discontinuity and not currently modelled as a
  tier — flagged as a known limitation the genuine_SPA will inherit.

### Revisit triggers

- Martin's consultation recommends a different decomposition (e.g.
  a single combined "all-templates" tier rather than typed
  sub-tiers; a hierarchical prior over template types).
- The pre-Phase-2 dictionary-build scan finds templates that don't
  fit any of the existing categories (centuries, half-centuries,
  reigns, BC-AD boundary) — would force a model-structure revision.
- The recovery simulation (H2.1) shows the slab structure cannot
  recover known α from synthetic data with this structure —
  triggers reconsideration of identifiability and possible
  reintroduction of an anchor-year residual tier.
- A bounded follow-up empirical analysis surfaces a real
  anchor-year mass signal previously missed (the existing three
  diagnostics tested AD 50 / 150 / 250 / 350 specifically; other
  anchor years remain plausible candidates).

---

## Decision 21 — 2026-05-17: H2.1 recovery-simulation grid pinned procedurally in-prereg; specific values committed to a pre-Phase-2 design artefact

**Status:** committed; primary item for Martin's consultation
**Decided by:** Shawn 2026-05-17 (arising from ChatGPT 5.5
cross-model review finding #4, BLOCKING — "H2.1's recovery
simulation is still under-specified and its 'coverage' criterion is
statistically muddled").

### Context

The Bayesian deconvolution-mixture model's validation rests on a
recovery simulation (Decision 14, H2.1): synthetic observed SPAs
built from a known genuine SPA + known α + known convention
component, run through the model, with the model judged validated
if it recovers known parameters within tolerance. ChatGPT's review
identified two coupled defects in how the simulation is currently
specified:

1. **Grid not enumerated.** The prereg describes the grid
   qualitatively (a "pre-specified parametric grid spanning the
   empirical α range", a "library of plausible shapes", tier weights
   "from a pilot fit") but pins no values: no α list, no shape
   library, no tier-weight vectors, no sample sizes, no replicates
   per cell, no seed policy.
2. **"Coverage" criterion is statistically muddled.** "≥ 90 % of
   grid cells have the true α inside the posterior 95 % CI"
   requires repeated synthetic datasets per cell to be a coverage
   statement (coverage is a repeated-sampling property). The
   current spec runs one synthetic dataset per cell, so the
   criterion tests whether each cell's *single* posterior interval
   happened to include the truth — not whether the model has
   nominal coverage.

The grid is now further constrained by Decision 20 (template-interval
slab convention component): the synthetic convention components in
the recovery grid must be built from the slab structure, not the
anchor-year structure of Decision 17.

### Options considered

- **A — Procedural in-prereg + deferred values.** Pre-commit the
  grid *axes* in the prereg (α coverage range, shape library
  categories, tier-weight categories, sample-size categories,
  minimum replicates per cell, seed policy), the coverage rule
  (≥ 90 % of cells pass; cell passes if ≥ 90 % of replicates per
  cell produce a 95 % CI on α containing the true α), the cell-wise
  reporting requirement, and the commitment to a pre-Phase-2 design
  artefact at a named `runs/...` directory where the specific
  values are pinned before any recovery simulation runs.
- **B — Full enumeration in-prereg.** Lock specific α values,
  specific shape parameters, specific tier-weight vectors, specific
  sample sizes, and specific replicate counts in the prereg body.
  Maximally pre-committed; bulky text; locks values without the
  empirical pilot fit that should inform them.
- **C — Defer entirely to Martin.** Pre-register only the existence
  of the grid and the principle of repeated-replicates coverage;
  pin specifics post-Martin. Honest about the gap; punts resolution.

### Decision

**Option A, procedural pre-commitment + design-artefact deferral.**

- **Prereg-binding grid axes:**
  - **α grid:** at least 5 values spanning the empirical pilot
    range; corner cases (α near 0, α near 1) included.
  - **Genuine-shape library:** at least 6 shapes covering
    {smooth growth, smooth decline, rise-and-fall, multi-modal,
    regnal-cluster (mirrors the empirical pattern Decision 20
    identified), flat-baseline}.
  - **Tier-weight vectors:** at least 5 vectors covering
    {uniform across tiers, century-heavy, reign-heavy, half-century-
    heavy, pilot-posterior-drawn}.
  - **Sample sizes:** representative N values from empire,
    province, and urban-area levels (specific N's pinned from the
    Phase 1 simulation's reachability map).
  - **Replicates per cell:** ≥ 50.
  - **Seed policy:** cell-deterministic (seed = base_seed +
    cell_index) for reproducibility.
- **Prereg-binding coverage rule:**
  - A *cell passes* if ≥ 90 % of its replicates produce a posterior
    95 % CI on α that contains the true α (proper repeated-sampling
    coverage at the cell level).
  - The mixture is *validated* if ≥ 90 % of cells pass, AND the
    posterior-median Pearson r against the true genuine shape is
    ≥ 0.95 in ≥ 90 % of cells.
  - **Cell-wise reporting required** (not just the global mean) —
    the report identifies any cells that fail and characterises the
    failure mode.
- **Design artefact:** a pre-Phase-2 `runs/2026-05-XX-recovery-
  grid-design/` directory committed before any recovery simulation
  runs, pinning the specific α values, shape parameters, tier-
  weight vectors, sample sizes, and replicate counts. The prereg
  names this artefact and binds the grid to its commit hash.
- The H2.1 confirmatory wording "the posterior α̂ falls within the
  95 % CI of the true α" is corrected to "the posterior 95 %
  credible interval for α contains the known true α" (ChatGPT
  finding #15, bucket (c) item C7 — folded in here because it's the
  same decision rule).

**Listed as primary item for Martin's consultation:** the 90 %
coverage threshold, the 50-replicates-per-cell minimum, the shape-
library completeness, and whether the variance-fraction validation
should attach to the multinomial likelihood only or also to the
Dirichlet-multinomial supplementary (Decision 19).

### Consequences

- §4 Phase 2 "Bayesian mixture validation" rewritten: grid-axes
  procedural spec replaces the qualitative description; coverage
  rule corrected to use repeated replicates; cell-wise reporting
  added; design-artefact reference added.
- §3 "Bayesian deconvolution-mixture model" "Validation" subsection
  updated to point at the procedural recovery-simulation spec.
- §6 effect-size table H2.1 rows rewritten: coverage criterion
  states "per-cell coverage ≥ 90 % across replicates; ≥ 90 % of
  cells pass"; shape-recovery criterion states "posterior-median
  Pearson r ≥ 0.95 in ≥ 90 % of cells" (not just the global mean
  r ≥ 0.95).
- Field 3 H2.1 hypothesis statement updated to match.
- The plain-English walkthrough Step 3 needs one extra sentence
  stating that the recovery simulation runs multiple synthetic
  datasets per grid cell so the coverage rule is a proper repeated-
  sampling statement.
- The recovery-grid design artefact is created as a pre-Phase-2
  step (not now); the prereg's mention of its `runs/...` location
  is the cross-reference.

### Revisit triggers

- Martin's consultation recommends a different coverage threshold,
  a different replicate count, or a different shape library.
- The pre-Phase-2 design artefact reveals the empirical pilot α
  range is narrow enough that a coarser α grid is sufficient (or
  wide enough that a finer α grid is needed).
- The mixture's identifiability profile (revealed by an early
  diagnostic on a single cell) shows the planned grid undersamples
  a key parameter axis.

---

## Decision 22 — 2026-05-17: H3a uses date-window-filtered counts; mixture model corrects temporal analyses only

**Status:** committed
**Decided by:** Shawn 2026-05-17 (arising from ChatGPT 5.5
cross-model review finding #5, BLOCKING — "H3a may not actually use
mixture-corrected data").

### Context

The preregistration's primary research question (Decision 12) reads:
"After controlling for editorial-convention dating artefacts via a
Bayesian deconvolution-mixture model, what fraction of the within-
province spatial variation in Latin inscription production during
the Roman Empire is accounted for by urban population dynamics?"

But the H3a model as specified is `y_c ~ NegativeBinomial(mu_c, φ)`
where `y_c` is the per-city inscription count under the 50 BC – AD
350 date-window filter — *not* a mixture-corrected count. The
Bayesian deconvolution-mixture model produces a posterior on a
temporal genuine-SPA shape, not on a per-city corrected count. As
written, the analysis answers a does-it-answer-the-question failure:
it tests how raw date-filtered inscription counts scale with
population, not how mixture-corrected counts scale with population.

The mismatch arises from a real structural distinction:

- **The mixture corrects a temporal aggregate.** Posterior α and
  posterior `genuine_SPA(t)` are well-identified at corpus / large-
  subset level where N is in the thousands. The mixture removes
  editorial-encoding artefacts from the temporal SPA shape — useful
  for H2.1 validation and H3b deviation-detection.
- **H3a is cross-sectional.** The estimand is a *spatial* variance
  fraction across ~ 815 cities at urban-area scale. Roughly 600 of
  these cities have N < 100 inscriptions, where a within-city
  mixture fit would be unidentified (the posterior on α_c would
  collapse to the prior). A city-level mixture correction is not
  empirically feasible for the bulk of the sample.

ChatGPT flagged two paths through: (i) narrow the claim — H3a uses
date-window-filtered counts; the mixture corrects temporal analyses
only; (ii) specify a per-city mixture-corrected response with
explicit uncertainty propagation. Option (ii) is methodologically
purer but infeasible for the bulk of the sample.

### Options considered

- **A — Narrow the claim** (ChatGPT's suggestion 1). Primary RQ
  rephrased so the artefact-protection mechanism for H3a is named
  honestly: the 50 BC – AD 350 date-window filter constrains the
  date-attribution artefact at city level; the Bayesian mixture
  corrects the temporal analyses (H2.1, H3b) but not the cross-
  sectional H3a regression. Mixture-α is reported as descriptive
  context.
- **B — Specify the corrected response** (ChatGPT's suggestion 2).
  Define `y_c` as a posterior-weighted count from a within-city
  mixture fit. Identifiability collapse for low-N cities; effectively
  excludes 75 % of the Hanson-matched sample.
- **C — Hybrid.** Primary H3a uses date-filtered counts (option A
  wording); a preregistered exploratory sensitivity re-runs H3a on
  the ~ 200 cities with N ≥ 100 under the within-city mixture-
  weighted response (option B). Reports both; disagreement flagged
  as a limitation, not a confirmatory amendment.

### Decision

**Option A, narrow the claim.**

- **Primary RQ revised:** "After applying a 50 BC – AD 350 date-
  window filter to constrain the date-attribution artefact, what
  fraction of the within-province spatial variation in Latin
  inscription production is accounted for by urban population
  dynamics?" The mixture-model phrase ("controlling for editorial-
  convention dating artefacts via a Bayesian deconvolution-mixture
  model") is removed from the RQ. The cross-sectional artefact
  protection is the date-window filter, named explicitly.
- **H3a model:** unchanged in structure — `y_c ~ NegBin(mu_c, φ)`
  with the within-between (Mundlak) `log(population)` decomposition.
  `y_c` is the city-level inscription count under the 50 BC – AD 350
  date-window filter. The mixture is *not* applied to `y_c`.
- **Mixture's role in the paper:** the mixture corrects the
  temporal SPA analyses (H2.1 recovery validation; H3b deviation-
  detection at the Antonine and Crisis-of-the-Third-Century probes).
  It does *not* correct H3a's cross-sectional count, and (clarified
  2026-05-17 in response to round-3 cross-model review) it does not
  correct H3c either: H3c's Pearson residuals are derived from H3a's
  posterior and therefore inherit H3a's date-filtered-count scope.
  Both H3a and H3c live in cross-sectional space; the artefact
  protection for both is the 50 BC – AD 350 date-window filter.
- **Reporting:** the empire-level posterior α from the mixture fit
  is reported as descriptive context — "the mixture fit estimates
  that α % of the corpus-level SPA is editorial-encoding artefact"
  — but H3a's confirmatory decision rule is not gated on α.
- The hybrid sensitivity (option C) is *not* preregistered — adding
  a second H3a fit on a different sample would muddle the
  confirmatory claim. If a posterior-weighted H3a is desired post-
  lodgement, it is a follow-up analysis, not a sensitivity on the
  confirmatory.

### Consequences

- §2 (Description) primary RQ rewritten as above.
- §3 (Analysis pipeline / "Bayesian NBR for H3a") rewritten to
  state explicitly that the response variable is date-window-
  filtered counts, not mixture-corrected counts; the mixture's
  role in H3a is descriptive context only.
- §3 ("Bayesian deconvolution-mixture model") scoped explicitly to
  the temporal SPA analyses (H2.1 validation; H3b deviation-
  detection); the scope-of-application sentence is added. H3c
  (cross-sectional, derived from H3a's posterior) is *not* in the
  mixture-corrects list (round-3 clarification 2026-05-17).
- Plain-English walkthrough Step 6 (the population question)
  rewritten to drop the mixture-correction framing for H3a; Step 2
  (the mixture model) gains a sentence stating it applies to
  temporal analyses only.
- Field 3 H3a hypothesis statement: keep the within-between
  specification and the variance-fraction estimand (Decision 12);
  remove any implicit claim that `y_c` is mixture-corrected.
- §9 known limitations: add a sentence clarifying that the
  cross-sectional H3a regression operates on date-window-filtered
  counts and does not propagate mixture-posterior uncertainty into
  the variance-fraction posterior; this is a real scope limit.
- Decision 12's "what fraction of within-province variance" framing
  is preserved; only the artefact-protection mechanism wording
  changes.

### Revisit triggers

- Martin's consultation argues a per-city mixture correction is
  feasible after all (e.g. via a hierarchical mixture pooling
  information across cities within a province), in which case
  option C or B is reconsidered.
- An exploratory post-lodgement analysis on the ~ 200 highest-N
  cities under option C's posterior-weighted response shows the
  variance-fraction estimate shifts materially.
- The mixture posterior α is so close to 0 (or 1) at corpus level
  that the artefact protection in H3a via the date-window filter
  alone looks empirically inadequate or unnecessary.

---

## Decision 23 — 2026-05-17: H3c residuals are Pearson residuals; capitals contrast is draw-wise; Moran's I uses posterior-mean residuals with field-standard permutation inference

**Status:** committed; primary item for Martin's consultation
**Decided by:** Shawn 2026-05-17 (arising from ChatGPT 5.5
cross-model review finding #6, BLOCKING — "H3c residuals not
operationally defined").

### Context

H3c has two confirmatory tests on the H3a posterior: (i) a capitals
contrast (provincial capitals over-produce inscriptions relative to
non-capitals; replicating Hanson 2021); (ii) Moran's I clustering on
the residual surface (replicating Hanson 2021's spatial-
autocorrelation finding). The current prereg specifies "continuous
posterior residuals" for both — under-specified in two ways:

- **Which residual.** For a Bayesian negative-binomial regression,
  plausible residual definitions include raw `y_c − μ_c`, log
  `log(y_c + 0.5) − log(μ_c)`, Pearson `(y_c − μ_c) /
  sqrt(μ_c + μ_c²/φ)`, deviance, and posterior-predictive
  residuals. Each has different distributional properties under the
  NBR; the choice is a researcher degree of freedom.
- **How Moran's I treats posterior uncertainty.** Options: (i)
  compute Moran's I on posterior-mean residuals (one I per k-NN
  structure; field-standard for spatial tests; uses conditional
  permutation inference for p-values); (ii) compute Moran's I per
  posterior draw (yields a posterior distribution of I per k;
  cleaner Bayesian; loses the standard permutation-based test);
  (iii) propagate posterior uncertainty into the permutation p-value
  via a more elaborate scheme. The capitals contrast already
  implies draw-wise residuals (the existing "posterior contrast"
  wording) — but the residual *definition* is the underspecified
  bit.

### Options considered

- **A — Pearson, draw-wise capitals + posterior-mean Moran's I.**
  Pearson residuals throughout (NBR field-standard; normalises out
  the mean-variance relationship). Capitals contrast: per posterior
  draw, compute the capital-vs-non-capital mean residual difference;
  P(contrast > 0) ≥ 0.95 is the rule. Moran's I: on posterior-mean
  Pearson residuals per k ∈ {5, 8, 10}; conditional permutation
  inference per k; rule I > 0 at p < 0.05 in ≥ 2 of 3 k. Supplementary:
  posterior distribution of Moran's I across draws (per k) reported.
- **B — Log residuals throughout.** Replace Pearson with log.
  Closer to Hanson 2021's implicit log-log OLS residual scale; loses
  the Pearson normalisation for NBR's mean-variance relationship.
- **C — Posterior distribution of Moran's I as the confirmatory
  rule.** Compute Moran's I per posterior draw; rule P(I > 0) ≥ 0.95
  in ≥ 2 of 3 k. More Bayesian; loses the standard permutation
  inference (field-non-standard for spatial tests).
- **D — Defer to Martin.** Pre-register Pearson-or-log + frequentist
  Moran's I; pin specifics post-Martin.

### Decision

**Option A: Pearson residuals throughout; draw-wise capitals contrast;
posterior-mean residuals for Moran's I with field-standard
conditional permutation inference; posterior distribution of Moran's
I across draws reported as supplementary.**

**Residual definition (binding):**

```text
For posterior draw s and city c:
  r_c,s = (y_c − μ_c,s) / sqrt(μ_c,s + μ_c,s² / φ_s)
```

where μ_c,s is the full posterior mean for city c on draw s,
*including* the province random intercept α_province[c] (so the
residual is relative to the Mundlak NBR's full city-level mean, not
the population-only fixed effect). φ_s is the posterior overdispersion
parameter draw.

**H3c(i) capitals contrast (binding):**

```text
For posterior draw s:
  contrast_s = mean(r_c,s | c ∈ provincial_capitals)
             − mean(r_c,s | c ∉ provincial_capitals)
Decision rule:
  P(contrast > 0) ≥ 0.95
  (posterior probability over draws)
```

**H3c(ii) Moran's I (binding):**

```text
r_c = posterior mean residual
    = (1/S) · Σ_s r_c,s
For each k ∈ {5, 8, 10}:
  Compute Moran's I on r_c with k-NN row-
    standardised spatial weights
  Conditional permutation inference (999
    permutations of r_c over fixed weights)
Decision rule:
  Moran's I > 0 at p < 0.05 in ≥ 2 of {k = 5, 8, 10}
```

**Supplementary reporting (binding):**

The posterior distribution of Moran's I across draws (per k) is
reported alongside — for each posterior draw s, Moran's I_s
computed on r_·,s with the same k-NN weights. Reported as the 2.5th
/ median / 97.5th percentiles of I_s per k. This makes the posterior
uncertainty on the spatial test visible without replacing the
field-standard permutation rule.

**Rationale for the asymmetric draw-wise / posterior-mean split:**

- Capitals contrast: the question naturally lives in posterior
  space ("does the contrast exceed 0 with high posterior
  probability?"); draw-wise computation directly answers this.
- Moran's I: the field-standard test for spatial autocorrelation
  is permutation-based. Running it on posterior-mean residuals
  preserves the field-standard inference for the confirmatory rule
  while reporting the posterior distribution of I supplementarily.
- The two tests answer different questions (a categorical contrast
  vs a spatial-structure test); using the natural inferential
  framework for each is more defensible than forcing both into the
  same scheme.

Listed as a Martin-consultation item: whether the asymmetric framing
is acceptable, whether Pearson is the right residual for an NBR with
random intercepts (a deviance residual variant may be considered),
and whether the posterior-mean vs draw-wise choice for Moran's I is
defensible to spatial statisticians.

### Consequences

- §3 ("Residual analysis (H3c)" and "Spatial clustering (H3c)")
  rewritten: residual definition pinned; capitals contrast and
  Moran's I procedural specs added; supplementary draw-wise Moran's
  I reporting added.
- Field 3 H3c(i) and H3c(ii) wording updated to match the formal
  residual definition.
- §6 effect-size table H3c rows updated.
- The plain-English walkthrough Step 7 needs a sentence stating
  that residuals are the Pearson kind (the NBR field standard) and
  that the spatial test uses posterior-mean residuals with the
  standard permutation procedure.

### Revisit triggers

- Martin's consultation recommends a different residual (e.g.
  deviance, log) or a different inferential procedure for Moran's I.
- The H3a posterior overdispersion parameter φ is so close to 0 (or
  so close to "Poisson") that the Pearson normalisation is
  empirically vacuous.
- The supplementary posterior distribution of Moran's I across
  draws shows the posterior-mean result is far from the posterior
  median — suggesting the confirmatory rule's residual averaging
  is hiding important uncertainty.

---

## Decision 24 — 2026-05-17: Freeze LIRE v3.0 for this OSF lodgement; LIST v1.2 reserved for post-lodgement amendment or follow-up

**Status:** committed
**Decided by:** Shawn 2026-05-17 (arising from ChatGPT 5.5
cross-model review finding #7, BLOCKING — "the LIST swap contingency
leaves a live data / envelope choice").

### Context

The preregistration's §1 (Dataset) and §7 (Planned deviations and
contingencies) currently allow the analytical envelope to extend
from AD 350 to AD 600 "if the LIST swap completes during the
fortnightly paper sprint (11–24 May 2026)." ChatGPT flagged
"completes" as operationally undefined, and the consequences as
large: dataset identity, temporal envelope, subset composition,
mixture model, Phase 3 counts, and Late Antique additions could all
change.

The contingency is also empirically near-resolved by the calendar:
today is 2026-05-17; the fortnightly sprint ends 2026-05-24; the
LIST swap is not done; the swap is not currently expected to land
within the remaining seven days.

### Options considered

- **A — Freeze LIRE v3.0; LIST is a post-lodgement amendment or
  follow-up.** Cleanest. Removes the live RDF entirely. The LIST
  envelope extension (50 BC – AD 600) becomes a candidate for
  either an OSF amendment after lodgement (if the swap lands soon)
  or a follow-up paper.
- **B — Keep the contingency with hard objective criteria + calendar
  cutoff.** Define "swap completes" operationally (schema check,
  row-count reconciliation, envelope validation, all by a hard
  calendar cutoff before any model output is inspected). Honest if
  the swap is genuinely in flight, but adds prereg complexity for
  little gain when the calendar is forcing the answer anyway.
- **C — Delay lodgement; pre-commit to LIST.** Hold OSF lodgement
  until LIST is ready. Honest about target dataset; indeterminate
  delay; risks scope creep.

### Decision

**Option A, freeze LIRE v3.0.**

- **§1 Dataset** reads: LIRE v3.0 (Zenodo DOI
  10.5281/zenodo.8147298, 11 October 2023) is the dataset for this
  preregistration. No envelope extension is permitted without an
  OSF amendment.
- **§7 Contingencies:** the LIST swap contingency clause is
  removed. Replaced with: "LIST v1.2 (Zenodo DOI
  10.5281/zenodo.10473706; same released schema as LIRE; extends
  the temporal envelope to AD 600) is a candidate for either a
  post-lodgement OSF amendment or a follow-up paper. If the LIST
  swap is pursued post-lodgement, an OSF amendment is filed before
  any LIST analysis is run, specifying the revised envelope,
  subset composition, and any Late Antique additions."

### Consequences

- §1 (Dataset) rewritten to drop the "Possible extension" LIST
  paragraph; the LIST DOI moved to §7 as a future-amendment marker.
- §7 (Planned deviations and contingencies) rewritten as above; the
  "If the LIST swap completes during the fortnightly paper sprint"
  bullet is removed entirely.
- §6 effect-size table: Phase 1 thresholds remain pinned to LIRE
  v3.0 reachability (no change).
- §9 known limitations: Late Antique and post-AD-350 phenomena
  remain out of scope (sentence already present; no change).
- The H1 (Phase 1 completed groundwork) is unaffected — Phase 1 ran
  on LIRE v3.0.

### Revisit triggers

- The LIST swap completes within weeks of lodgement, making a
  promptly-filed OSF amendment worthwhile.
- LIRE v3.0's known limitations (e.g. its envelope cap at AD 350)
  prevent a co-author or reviewer-requested analysis the LIST
  envelope would enable.

---

## Decision 25 — 2026-05-17: Prior- and posterior-predictive check failure triggers are numerical; specifics pinned in the pre-Phase-2 design artefact

**Status:** committed; specifics pinned in the pre-Phase-2 design
artefact (same artefact as Decision 21's recovery-grid spec)
**Decided by:** Shawn 2026-05-17 (arising from ChatGPT 5.5
cross-model review finding #8, SHOULD-FIX — "prior and posterior
predictive failure triggers are too vague").

### Context

The preregistration's PPC section uses narrative triggers — "most
counts in `[0, 10⁴]`", "no implausibly large counts", "divergent",
"remaining structure", "beyond Monte Carlo noise" — that are not
binding criteria. Yet failed checks trigger model revision. ChatGPT
flagged this as a researcher degree of freedom: workflow-driven
model revision after seeing diagnostics is reasonable Bayesian
practice, but preregistration discipline needs to constrain *when*
that happens and *how* confirmatory status is preserved.

Same structural pattern as the recovery-simulation grid (Decision
21): the right level of pre-commitment is procedural (categories
and reporting rule) with specific numerical values pinned in a
named pre-Phase-2 design artefact.

### Decision

**PPC failure triggers are numerical, not narrative.** Specifics are
pinned in the same pre-Phase-2 design artefact as the recovery-grid
spec (Decision 21).

**Prereg-binding (procedural):**

- PPC trigger *categories* (each gets a specific numerical bound
  pinned in the design artefact):
  - Prior predictive 99th-percentile count cap.
  - Posterior-predictive mean: within X % of observed.
  - Posterior-predictive standard deviation: within Y % of observed.
  - Posterior-predictive tail-count (95th percentile): within
    specified bounds of observed.
  - Posterior-predictive proportion-of-zeros: within specified
    bounds of observed (NBR sanity check for zero-inflation).
  - Residual-vs-fitted slope (standardised Pearson residuals over
    fitted values): absolute slope < threshold.
  - Province-level residual dispersion: ratio of within-province
    residual variance to grand residual variance within specified
    bounds.
- **Failure response:**
  - Any tripped trigger initiates model revision (revising priors,
    link function, or model structure).
  - The originally-preregistered model result is **reported
    alongside** the revised model's result in the paper — confirmatory
    status is preserved for the original; the revised model is
    reported as a transparent post-hoc revision.
  - An OSF amendment is filed before the final results are lodged
    (per the §7 amendment rule).
- **No PPC trigger is used to test a hypothesis** — these are
  diagnostic checks on model fit, not confirmatory tests.

**Listed as Martin-consultation item:** the specific numerical
thresholds in each category. Martin will likely have opinions on:
the X / Y / tail-count percentages; the residual-slope cutoff; the
province-level dispersion bounds; whether to add additional checks
(e.g. autocorrelation in standardised residuals if residuals are
ordered by population or province).

### Consequences

- §3 ("Posterior predictive checks" and "Prior predictive checks")
  rewritten: narrative triggers replaced with procedural commitment
  to numerical thresholds; design-artefact reference added.
- §7 contingencies: the "if posterior or prior predictive checks
  fail for H3a" bullet rewritten to specify "any of the numerical
  PPC triggers tripped" rather than narrative.
- The H2.1 recovery-simulation design artefact (Decision 21)
  acquires a second pinning role: it pins both the recovery-grid
  values and the PPC numerical thresholds. One artefact, two
  spec-tables.
- §6 / Field 3: unchanged for confirmatory rules (PPCs are not
  confirmatory).

### Revisit triggers

- Martin's consultation recommends additional PPC categories (e.g.
  posterior-predictive spatial-autocorrelation check for the H3a
  residuals before H3c is run).
- A specific numerical threshold pinned in the design artefact
  proves unsupportable at the pilot fit (the pilot fit's posterior
  systematically violates the proposed threshold) — triggers an
  amendment to the design artefact before lodgement.

---

## Decision 26 — 2026-05-17: Smaller-substantive ChatGPT-pass adjustments (Hanson-population sensitivity; Western-Empire subset operationalisation)

**Status:** committed
**Decided by:** Shawn 2026-05-17 (arising from ChatGPT 5.5
cross-model review findings #9 (partial) and #10 (partial),
SHOULD-FIX).

### Context

Two smaller adjustments from the ChatGPT-pass triage:

- **B9 — Hanson-population uncertainty sensitivity.** Hanson (2016)
  urban population estimates are treated as exact in the H3a
  regression. The estimates are themselves uncertain; treating them
  as exact understates the posterior on `β_within` and on the
  within-province population-attributable variance fraction.
  ChatGPT recommended a lognormal measurement-error sensitivity.
- **B10 — Western-Empire provincial subset operationalisation.**
  H3b's "Western-Empire provincial subset" was named but not
  defined. Shawn's earlier exploratory work
  (`archive/2026-04-22-inscriptions-spa.ipynb` cell 54) classified
  60 LIRE province values as Latin / Greek; the operational
  definition for the Western-Empire subset is "province_language ==
  'Latin' AND province != 'Roma'", using that classification.

### Decisions

**B9 — Add as a preregistered exploratory sensitivity.** Add to
§5 a single exploratory sensitivity analysis:

- Re-run H3a with a lognormal measurement-error model on the
  Hanson population predictor: `log_pop_c ~ Normal(log_pop_observed_c,
  σ_pop)` for σ_pop ∈ {0.1, 0.2, 0.3} (low / moderate / high
  measurement uncertainty).
- Report the posterior on the within-province population-
  attributable variance fraction `f_within` under each σ_pop.
- Material divergence from the primary H3a result (posterior 95 %
  CI on `f_within` shifts by more than 50 % of its primary-result
  width) is flagged as a limitation in the paper; does *not*
  trigger an OSF amendment (this is a preregistered exploratory
  sensitivity, not a confirmatory test).

**B10 — Western-Empire subset defined operationally from
Shawn's existing province_language classification.** Specifically:

- The Western-Empire provincial subset comprises all LIRE v3.0
  provinces where the project's `province_language` classification
  equals `'Latin'`, **excluding** the province `'Roma'`.
- The classification is taken from
  `archive/2026-04-22-inscriptions-spa.ipynb` cell 54
  (`province_language_map`), with one correction: the dictionary
  entry `'Aquitani(c)a': 'Latin'` is a likely typo — the actual
  LIRE province field uses either `'Aquitania'` or `'Aquitanica'`.
  The corrected key will be applied at the data-cleaning stage of
  the analysis pipeline (not a preregistration commitment).
- The 41 Latin-classified provinces (Roma excluded) include the
  Italian core ("Italia" plus the eleven Augustan regions), the
  Latin West (Gauls, Germanies, Britannia, Hispaniae, African
  provinces), and the Danube-and-frontier provinces (Noricum,
  Raetia, Pannoniae, Dalmatia, Dacia, Moesiae). Three frontier
  classifications (Moesia Inferior, Moesia Superior, Sicilia) are
  judgement calls — administrative-language Latin but with
  significant bilingual or Greek-speaking populations; this is
  flagged in §9 known limitations as a known scope choice.

### Consequences

- **§5** acquires a new exploratory item:
  "Hanson-population measurement-error sensitivity for H3a" with
  the spec above.
- **§4** (or wherever the Western-Empire subset is referenced)
  acquires the operational definition: "Western-Empire provincial
  subset: all LIRE v3.0 provinces where
  `province_language == 'Latin' AND province != 'Roma'`. Specific
  list reproducible from the project's `province_language_map`
  classification (committed to the public repository)."
- **§9 known limitations** acquires a sentence on the three
  frontier-province classification judgement calls (Moesia
  Inferior, Moesia Superior, Sicilia).
- Data-cleaning task added (off-prereg): correct the
  `Aquitani(c)a` typo in the working `province_language_map` to
  match LIRE v3.0's actual field value.

### Revisit triggers

- The Hanson-population sensitivity returns σ_pop = 0.3 results
  that materially differ from the primary — would inform whether
  σ_pop should be a hyperparameter rather than a fixed sensitivity
  axis.
- Martin's consultation recommends an alternative measurement-
  error model (e.g. a hierarchical prior with σ_pop estimated
  jointly with the regression).
- The Western-Empire-subset analysis is destabilised by the
  Moesia / Sicilia frontier-province classifications — would
  trigger a sensitivity excluding those three provinces.


---

## Decision 27 — 2026-05-17: Recovery-simulation refinements — replicate-count floor bumped to ≥ 100; Wasserstein-1 supplementary shape metric

**Status:** committed; provisional pending Martin's eventual review (any
revision filed as OSF amendment)
**Decided by:** Shawn 2026-05-17 (informed by stand-in cross-model
statistical review — ChatGPT 5.5 + Gemini 3 Pro, 2026-05-17 —
undertaken as a hedge against delayed feedback from the planned
statistician consultation with Martin; both reviewers independently
flagged the ≥ 50 replicate floor as thin and Pearson r alone as too
forgiving for localised mass-redistribution failures).

### Context

The Decision 21 H2.1 recovery-simulation grid pre-commits two
quantities that the stand-in cross-model review flagged as
under-specified:

1. **Replicate floor.** The prereg-binding floor of ≥ 50 replicates
   per cell yields a per-cell Wilson 95 % interval on coverage at a
   true 90 % rate of approximately [0.79, 0.96] — too wide to give a
   stable pass / fail boundary. A cell observed at 45 / 50 passes and
   44 / 50 fails; that boundary is brittle, and brittleness
   propagates into the global ≥ 90 % cells-pass rule.
2. **Shape-recovery metric.** Pearson r between recovered posterior-
   median and true genuine SPA is scale- and shift-invariant; it can
   remain high (≥ 0.95) even when localised mass is mis-allocated by
   the model. For a recovery-validation context this is precisely
   the failure mode we want to catch.

### Options considered

- **A — Status quo.** Keep ≥ 50 floor; Pearson r as sole shape
  metric. Cheapest; under-validated.
- **B — Bump replicate floor + add a distribution-sensitive
  supplementary shape metric.** Cost: roughly linear in replicates ×
  cells; expect O(50–100) cells, so the bump from 50 to 100 doubles
  compute cost in the recovery stage. Adds Wasserstein-1 (Earth
  Mover's distance) — the standard distribution-comparison metric
  for compositional data — alongside Pearson r.
- **C — More aggressive: ≥ 200 replicates; replace Pearson r with
  Wasserstein-1.** Higher cost; risks de-emphasising the field-
  familiar Pearson r continuity check.

### Decision

**Option B.**

- **Replicate floor:** bumped from ≥ 50 to **≥ 100 replicates per
  cell** as the prereg-binding floor. Design-artefact default
  pinned at 100 (push to 200 in boundary cells if compute permits;
  a two-stage variant — 50 across the full grid to identify failure
  regions, 200 at boundary cells — is also acceptable per the
  design artefact).
- **Shape-recovery rule:** Pearson r ≥ 0.95 in ≥ 90 % of cells
  remains the **binding** rule. **Wasserstein-1 (Earth Mover's
  distance)** between recovered posterior-median and true genuine
  SPA is added as a **supplementary** shape-recovery metric,
  reported per cell with a flagging threshold pinned in the design
  artefact. The supplementary is descriptive — not part of the
  binding confirmatory rule — but is reported alongside the Pearson
  r outcome for every cell.

### Consequences

- §3 (Bayesian deconvolution-mixture model / Validation) — rule
  updated.
- §4 (Phase 2 / "Confirmatory recovery simulation (H2.1)") — grid
  axes table updated (replicates ≥ 100); shape-recovery rule
  rewritten to include Wasserstein-1 supplementary.
- §6 (effect-size table) — H2.1 shape-recovery row extended:
  Pearson r row plus a new Wasserstein-1 supplementary row.
- Design-artefact spec extended: pin specific Wasserstein-1
  flagging threshold; pin replicate count (default 100).
- Decision 21's Revisit triggers list inherits the additional
  trigger "Martin recommends a different replicate count or a
  different shape metric."

### Revisit triggers

- Martin's consultation recommends a different replicate count
  (e.g. ≥ 200) or a different shape metric (Jensen-Shannon
  divergence; integrated absolute error; KS distance).
- The pilot fit's recovery simulation reveals systematic localised
  mass-redistribution failures that Wasserstein-1 also misses — a
  different distribution-sensitive metric (e.g. KL divergence with
  a smoothing prior) becomes preferred.
- Compute cost at ≥ 100 replicates proves prohibitive for the final
  grid size — would prompt the two-stage variant or reduction in
  cell count.

---

## Decision 28 — 2026-05-17: Aoristic-Monte-Carlo supplementary mixture fit

**Status:** committed; provisional pending Martin's eventual review
(any revision filed as OSF amendment)
**Decided by:** Shawn 2026-05-17 (informed by stand-in cross-model
statistical review; ChatGPT 5.5 proposed the supplementary fit as a
direct test of the upstream-aoristic assumption underlying the
primary mixture model).

### Context

Decision 19's Bayesian mixture observation model absorbs aoristic
uncertainty upstream in the SPA construction: per-inscription
uniform-aoristic mass is summed into 5-year bins deterministically,
and a single empirical SPA enters one mixture fit. The Law-of-Large-
Numbers expectation is that per-inscription uniform aoristic averages
out at the 5-year bin level for N_eff ~ 10^5 inscriptions — but this
is an unverified expectation. Where wide template intervals dominate
the corpus (the [1, 100] template alone is 26.3 % of LIRE v3.0),
the LLN argument's premises are weaker than at a more uniform
interval-width distribution.

A sensitivity is wanted: how much does the posterior on α move under
per-inscription latent-date variation? Decision 19's Revisit triggers
already flag aoristic-uncertainty propagation as a candidate for
revisiting; the stand-in cross-model review surfaces a concrete
mechanism for testing it cheaply.

### Options considered

- **A — Propagate latent dates into the likelihood directly.** Full
  Bayesian propagation: each inscription with date range
  `[nb_i, na_i]` carries a latent `t_i ~ Uniform(nb_i, na_i)` in the
  model. Parameter space expands by ~ 10^5; sampler convergence
  becomes a non-trivial engineering problem. Methodologically the
  purest answer; computationally expensive.
- **B — Aoristic-Monte-Carlo supplementary fit.** Run the mixture
  on N_MC independently-sampled aoristic SPA realisations — each
  realisation built from a different per-inscription latent-date
  draw within `[nb_i, na_i]` — and report the cross-realisation
  posterior on α as a sensitivity alongside the primary single-SPA
  posterior. Compute cost: N_MC extra mixture fits (N_MC ~ 20–50);
  cheaper than Option A by orders of magnitude; directly tests the
  LLN expectation without requiring it.
- **C — Status quo.** Single-SPA fit only; defend the upstream-
  aoristic choice in prose.

### Decision

**Option B.**

- An **aoristic-Monte-Carlo supplementary fit** is preregistered as
  a sensitivity analysis on the upstream-aoristic assumption.
- **Procedure:** N_MC independently-sampled aoristic SPA realisations
  are constructed (each from a different per-inscription latent-date
  draw `t_i ~ Uniform(nb_i, na_i)`); each realisation produces a
  separate mixture fit with the primary multinomial likelihood. The
  **cross-realisation posterior** of α — the union of all per-
  realisation posteriors on α, equally weighted across realisations
  — is reported alongside the primary single-SPA posterior.
- **N_MC:** pinned in the pre-Phase-2 design artefact, in the range
  N_MC ∈ [20, 50]. The exact value is pinned before any mixture fit
  is run.
- **Divergence flag (preregistered):** if the cross-realisation 95 %
  range on α exceeds **1.5× the primary single-SPA posterior 95 %
  CI width**, this is reported as a *material* limitation of the
  upstream-aoristic primary choice in the paper. Does not trigger
  an OSF amendment by itself (this is a preregistered sensitivity,
  not a confirmatory test); the result is reported transparently.
- The aoristic-MC supplementary is run only on the **primary
  multinomial fit**; the Dirichlet-multinomial and rescaled NegBin
  supplementaries of Decision 19 are not separately aoristic-MC'd.

### Consequences

- §3 (Bayesian deconvolution-mixture model) — a new subsection
  "Aoristic-uncertainty sensitivity (supplementary)" added.
- §5 (Exploratory analyses) — cross-reference added pointing back
  to the §3 spec.
- §6 (effect-size table) — a supplementary row added under H2:
  reports the cross-realisation posterior of α and the divergence
  flag.
- Plain-English walkthrough Step 2: one sentence added noting the
  aoristic-MC supplementary.
- Design artefact spec: pin specific N_MC and the divergence-flag
  threshold (default 1.5× the primary posterior width).

### Revisit triggers

- Cross-realisation posterior on α moves materially (the 1.5×
  divergence flag is tripped) — consider promoting to full latent-
  date propagation (Option A) in a follow-up paper or OSF amendment.
- Pilot fit reveals N_MC mixture fits is computationally infeasible
  at scale — would force reduction in N_MC or fall-back to Option
  C (status quo) via OSF amendment before final lodgement.
- Martin recommends Option A directly, or a different sensitivity
  design (e.g. importance-resampling within a single fit).

---

## Decision 29 — 2026-05-17: 8th PPC category — posterior-predictive spatial autocorrelation on H3a residuals

**Status:** committed; provisional pending Martin's eventual review
(any revision filed as OSF amendment)
**Decided by:** Shawn 2026-05-17 (informed by stand-in cross-model
statistical review; ChatGPT 5.5 recommended adding a posterior-
predictive spatial-autocorrelation check as an H3c-specific PPC).

### Context

The current PPC categories (Decision 25, seven categories: prior
99th-percentile cap; PP mean / std / tail-count / proportion-of-
zeros; residual-vs-fitted slope; province-level residual dispersion)
test marginal and conditional moments of the posterior-predictive
distribution but do not test whether the model can *generate* spatial
structure in residuals of the magnitude observed.

H3c(ii) (Decision 23) tests whether the H3a residuals exhibit spatial
clustering (Moran's I > 0). If the H3a posterior-predictive routinely
*fails* to generate residual spatial structure of the observed
magnitude, then H3c(ii) is testing something the model is structurally
incapable of producing — a tautology risk: a "significant Moran's I
on observed residuals" would mean "observed residuals exhibit a
structure the model cannot produce," which is a different — weaker —
finding than "observed residuals exhibit a real spatial pattern."

The model-generates-the-pattern check is a standard Bayesian-workflow
PPC; absent from the original spec because the seven categories were
drafted before H3c(ii) was specified in its current Pearson-residual
form (Decision 23).

### Decision

**An 8th PPC category is added.**

- **Test:** for each H3a posterior draw, compute `y_pred,c` for each
  city; compute Pearson residuals of `y_pred,c` against
  `μ_c,s`; compute Moran's I on the resulting posterior-predictive
  residual surface with the same k-NN spatial weights as H3c(ii)
  (primary k = 8). Repeat across posterior draws to obtain the
  posterior-predictive distribution of Moran's I.
- **Trigger:** observed Moran's I (from H3c(ii)'s posterior-mean
  Pearson residual computation) lies *outside* the design-artefact-
  pinned range of the posterior-predictive distribution (default:
  outside the 5th–95th percentile of posterior-predictive I).
- **Severity (per Decision 30):** critical if observed I lies
  outside the 1st–99th percentile range; minor if outside 5th–95th
  but within 1st–99th.
- **Interpretation:** a tripped trigger means the model is unable
  to generate the observed degree of residual spatial structure
  under its own posterior — H3c(ii) results from such a model
  must be reported with the tautology caveat ("the model is
  structurally underspecified for the spatial pattern observed").

### Consequences

- §3 (Posterior predictive checks) — PPC category list extended to
  eight categories.
- §3 (Residual analysis / Spatial clustering H3c) — cross-
  reference: the 8th PPC is run before H3c(ii); the H3c(ii)
  interpretive language is conditional on the 8th PPC outcome.
- §4 (Phase 3 description) — added bullet point.
- §6 (effect-size table) — PPC subsection extended.
- §7 (contingencies) — PPC-failure trigger language updated to
  include the new category.

### Revisit triggers

- Martin's consultation recommends a different spatial PPC
  (e.g. semivariogram instead of Moran's I; geographically-weighted
  posterior-predictive density).
- The 8th PPC trips on the pilot fit — would require revisiting
  H3c(ii)'s decision rule given that the model fails to produce
  observed spatial structure.
- The 8th PPC and H3c(ii) together produce an interpretively
  confused result (e.g. PPC trips on the low side — model under-
  generates spatial structure — but H3c(ii) is permutation-
  significant; how to report?).

---

## Decision 30 — 2026-05-17: Two-tier severity scheme for PPC trigger response

**Status:** committed; provisional pending Martin's eventual review
(any revision filed as OSF amendment)
**Decided by:** Shawn 2026-05-17 (informed by stand-in cross-model
statistical review; ChatGPT 5.5 flagged the current uniform "any
tripped trigger initiates revision" rule as too aggressive).

### Context

Decision 25's PPC failure response is uniform: any tripped trigger
initiates model revision (priors, link, or structure), reports the
originally-preregistered model alongside the revised model in the
paper, and files an OSF amendment before final results are lodged.

This rule treats all numerical PPC failures identically — a mild
tail discrepancy (e.g. PP mean off by 6 % when the design-artefact
bound is 5 %) triggers the same response as a critical failure
(e.g. PP mean off by 50 %; sign-flipped residual-vs-fitted slope).
For a paper with eight PPC categories per Decision 29's addition,
this aggregates: a routinely-mild trigger in one category forces
the full revision + amendment overhead even when the main model is
substantively adequate.

The amendment-filing overhead is non-trivial (OSF amendments are
public-record commitments); routinely filing for mild discrepancies
risks both procedural fatigue and a "noisy" public amendment trail
that obscures genuinely material revisions.

### Options considered

- **A — Status quo.** Uniform "any tripped trigger" rule. Maximally
  conservative; high overhead.
- **B — Two-tier severity scheme.** Critical (significantly tripped
  — e.g. > 2× the design-artefact bound, or sign-flipped where
  applicable) retains the full response; minor (marginally tripped
  — e.g. tripped at > 1× but ≤ 1.5× the bound) is reported as a
  caveat in the paper without forcing model revision.
- **C — Three-tier scheme.** Critical / moderate / minor with
  graded responses. More precise; more parameters to pin.

### Decision

**Option B, two-tier severity scheme.**

- **Critical trigger:** PPC value lies outside the design-artefact
  bound by > 2× the bound's magnitude (e.g. for "PP mean within X %
  of observed," critical means PP mean off by > 2X %); or, for
  trigger categories with directional bounds (residual-vs-fitted
  slope), the sign is unexpected.
  - **Response:** model revision (priors, link, or structure);
    originally-preregistered model reported alongside the revised
    model; OSF amendment filed before final results are lodged.
    (Current Decision-25 rule preserved.)
- **Minor trigger:** PPC value lies outside the design-artefact
  bound by ≤ 1.5× the bound's magnitude (i.e. tripped, but
  marginally).
  - **Response:** reported as a caveat in the paper; no model
    revision required; no OSF amendment.
- **Cutoffs (1.5× / 2×):** straw values; pinned in the design
  artefact for each PPC category. The cutoffs may differ across
  categories (e.g. proportion-of-zeros may warrant a tighter
  minor / critical cutoff than tail-count).
- **The "no trigger used to test a hypothesis" rule is unchanged**
  — these are diagnostic checks on model fit, not confirmatory
  tests.

### Consequences

- §3 (PPC failure-response paragraph) rewritten with the severity-
  conditional response.
- §7 (contingencies) — "If any numerical PPC threshold is tripped
  for H3a" bullet rewritten to the severity-conditional form.
- Design-artefact spec: pin per-category critical / minor cutoffs.
- Decision 25's uniform "any tripped trigger" wording superseded
  for the response side; the trigger-category list of Decision 25
  is preserved (and extended by Decision 29).

### Revisit triggers

- Martin recommends a three-tier scheme or different cutoffs
  (e.g. critical at > 3×; minor at > 1× ≤ 2×).
- A pilot fit reveals a trigger category where the 2× cutoff is
  empirically vacuous (the posterior-predictive distribution is
  narrow enough that 2× the bound is well within the prior-
  predictive support) — would prompt revising the design-artefact
  bound or the severity cutoff for that category.
- A pilot fit reveals a category where the 1.5× minor cutoff is
  routinely tripped — would prompt revising the design-artefact
  bound to a more permissive value before lodgement.

---

## Decision 31 — 2026-05-17: Three-case interpretive guardrail for H3c(ii) Moran's I

**Status:** committed; provisional pending Martin's eventual review
(any revision filed as OSF amendment)
**Decided by:** Shawn 2026-05-17 (informed by stand-in cross-model
statistical review; ChatGPT 5.5 proposed the three-case guardrail to
prevent over-claiming when the confirmatory rule passes but posterior
uncertainty is wide).

### Context

Decision 23's H3c(ii) decision rule (Moran's I > 0 at *p* < 0.05 in
≥ 2 of {k = 5, 8, 10} on posterior-mean Pearson residuals; field-
standard frequentist conditional permutation inference) is a
posterior-mean-summarised frequentist test. The supplementary
posterior distribution of `I_s` across draws is reported (per k) as
2.5 / 50 / 97.5 percentiles, but does not enter the confirmatory
verdict.

This creates a reporting risk: a result that is permutation-
significant on the posterior-mean residual surface but for which the
posterior distribution of `I_s` straddles zero is, by the literal
rule, a *supported* H3c(ii) — even though the posterior uncertainty
is wide enough that the "spatial clustering" claim is not
substantively robust. Without a pre-committed interpretive
framework, the paper's prose around this case is a researcher
degree of freedom.

### Options considered

- **A — Three-case interpretive guardrail.** Preserves the
  confirmatory rule unchanged; commits to specific interpretive
  language for the three posterior-distribution cases.
- **B — Status quo.** Report the supplementary I_s percentiles;
  let interpretive language be ad hoc.
- **C — Promote posterior I_s to the binding rule.** Replace the
  permutation rule with `P(I > 0) ≥ 0.95` (across draws per k).
  Field-non-standard for spatial autocorrelation tests; departs
  from the Decision 23 rationale for the asymmetric draw-wise /
  posterior-mean split.

### Decision

**Option A, three-case interpretive guardrail.**

The **decision rule** (Moran's I > 0 at *p* < 0.05 in ≥ 2 of {k = 5,
8, 10} on posterior-mean Pearson residuals; field-standard
conditional permutation inference) is **unchanged**. The guardrail
governs only the interpretive language used in the paper:

- **Case 1 — clean replication.** Confirmatory rule passes AND the
  posterior distribution of `I_s` shows ≥ 95 % of draws above 0 at
  the primary k = 8. Reported as: "the spatial-clustering finding
  replicates Hanson 2021 robustly, with posterior support."
- **Case 2 — permutation-significant but posterior-sensitive.**
  Confirmatory rule passes BUT the 95 % posterior interval of
  `I_s` at primary k = 8 crosses zero. Reported as: "the spatial-
  clustering finding is permutation-significant on the posterior-
  mean residual surface but sensitive to posterior uncertainty —
  not described as a clean replication of Hanson 2021."
- **Case 3 — confirmatory rule passes without substantive support.**
  Confirmatory rule passes AND the posterior distribution of `I_s`
  is centred near zero (< 50 % of draws above 0 at primary k = 8).
  Reported as: "the confirmatory rule passes but does not survive
  posterior-uncertainty diagnostics — H3c(ii) is **not** claimed as
  substantively supported."

Thresholds (≥ 95 % for Case 1; < 50 % for Case 3) are committed in
the prereg.

### Consequences

- §3 (Spatial clustering H3c(ii)) extended with the guardrail
  table.
- Field 3 H3c(ii) wording extended (one sentence on each case's
  interpretation).
- §6 (effect-size table) — H3c(ii) row footnoted with the three-
  case framework.

### Revisit triggers

- Martin recommends Option C (full draw-wise posterior rule) or
  different posterior-distribution thresholds.
- Observed result lands in Case 2 and the "permutation-significant
  but posterior-sensitive" wording proves contested in peer
  review.
- Across k = 5, 8, 10 the three k's land in different cases —
  would prompt a refinement of the guardrail to a per-k version.

---

## Decision 32 — 2026-05-17: Three-weighting sensitivity for f_within (unweighted primary; population- and inscription-weighted supplementaries)

**Status:** committed; provisional pending Martin's eventual review
(any revision filed as OSF amendment)
**Decided by:** Shawn 2026-05-17 (informed by stand-in cross-model
statistical review; ChatGPT 5.5 flagged the unweighted-variance
choice as defensible but arbitrary, and recommended a population-
or inscription-weighted sensitivity).

### Context

The H3a primary estimand `f_within = Var(β_within · within-deviation)
/ Var(log E[insc_c])` (Decision 12, refined by Decision 18) is
computed with both numerator and denominator variances **unweighted**
across cities. Under this choice, every city contributes equally to
the variance calculation regardless of its population or its
inscription count — answering the substantive question "what share of
city-to-city *systematic variation* does within-province population
explain?"

An alternative reading of the same primary RQ is "what share of
*inscription-weighted variation*?" or "what share of *population-
weighted variation*?" — the population-weighted denominator gives
disproportionate weight to the largest cities (matching the natural
"this is where most of the demographic action happens" reading), and
the inscription-weighted denominator gives disproportionate weight
to inscription-rich cities (matching "this is where most of the
epigraphic action happens"). The three weightings answer related but
different questions; the unweighted primary is defensible, but
arbitrary, and a reviewer may ask why we chose it.

### Decision

**Add a three-weighting sensitivity as a §5 pre-specified
exploratory.**

- The **unweighted** `f_within` remains the **binding primary
  confirmatory** estimand (the H3a three-way verdict is computed on
  this and only this version).
- Two **supplementary** weighted variants are pre-specified as §5
  exploratories:
  1. **Population-weighted** — both numerator and denominator
     variances computed with city weight `w_c = population_c`,
     normalised so weights sum to N_cities. Answers "what share of
     population-weighted log-count variance does within-province
     population explain?"
  2. **Inscription-weighted** — same with `w_c = y_c`. Answers "what
     share of inscription-weighted log-count variance does within-
     province population explain?"
- Both supplementaries are reported as full posterior distributions
  alongside the unweighted primary.
- **Material divergence:** if the spread across the three weightings
  exceeds **half the primary unweighted posterior 95 % CI width**,
  this is flagged as a limitation in the paper (the substantive
  reading of the primary depends on which variation we're
  partitioning). Does *not* trigger an OSF amendment (this is a
  preregistered exploratory sensitivity, not a confirmatory test).

### Consequences

- §5 (Exploratory analyses) gains the three-weighting sensitivity
  item with the spec above.
- §3 (H3a confirmatory estimand and decision rule) — one sentence
  added clarifying that the binding primary is unweighted; the
  weighted supplementaries are §5 sensitivities, not co-binding.
- §6 (effect-size table) — H3a row footnoted with the supplementary
  weightings.

### Revisit triggers

- Spread between the three weightings exceeds the material-
  divergence threshold — would prompt a discussion of whether the
  unweighted variant is the appropriate substantive primary, or
  whether (e.g.) the population-weighted variant better matches
  the paper's primary substantive question.
- Martin recommends a different weighting (e.g. inverse-variance
  weighting; weighting by city `1/SE(log_pop_c)`).
- A reviewer asks for a fourth weighting variant (e.g. log-
  population-weighted) — would prompt either an exploratory
  addition or a justified refusal.

## Decision 33 — 2026-06-02: Recovery-grid binding-criterion metric correction (α demoted to diagnostic; operating-envelope reframe)

**Status:** committed; **lodged in OSF Amendment 01 §A5.5.1 on 2026-06-04**
(Stage-3 launch gate cleared); provisional pending Martin's draft-stage
sign-off.
**Decided by:** Shawn 2026-06-02 — the demote-α and operating-envelope-reframe
choices were made this session after reviewing the evidence. Informed by the
Grid A adjudication, a closed-loop prior-art scout, and a `/review-implementation`
pass.

> **Update 2026-06-04 — the 91.9% Grid A figure below is historical (now 98.6%).**
> The convergence precondition was sharpened to a *field-standard* gate after the
> 2026-06-02 preview reported below. The 91.9% used a zero-tolerance divergence
> gate later found non-standard (Stan diagnostics guidance; Betancourt 2017;
> Vehtari et al. 2021 — no source endorses a divergence-rate threshold; see
> working-notes Obs 70). Under the R̂ / bulk-ESS-only gate the 24 excluded
> `flat_baseline` cells all converge, so Grid A headline **B = diagnostic A =
> 98.6% (355/360)** within the operating envelope (the 5 non-passers are
> `bimodal_α=0.70_N=2000` genuine-shape failures). The harness was corrected the
> same day to re-derive convergence from the stored per-replicate R̂ / bulk-ESS
> (no re-fit) and now reproduces 98.6% in-pipeline with a passing regression check
> (commits `4f96e47` code, `0a15667` re-aggregated artefacts). The gate change is
> encoded in OSF Amendment 01 §A5.5.1 + §A5.7; cross-grid verdict (inscription
> PASS / letter FAIL → Stage 3 inscription-mass only) is unaffected.

### Context

Adjudicating Grid A (inscription mass) of the two-unit recovery simulation
returned a FAIL under the lodged binding criterion (42.7% both-pass). Diagnosis
(re-verified from the stored posteriors) localised the failure to two
mathematical/asymptotic defects rather than recovery failure:

1. **Criterion (ii) is undefined for the flat genuine shape.** Pearson r against
   a constant truth is `0/0`; all 75 `flat_baseline` cells auto-fail, capping
   shape-pass at 83.3% irrespective of model quality.
2. **Criterion (i) — exact 95% credible-interval coverage of the mixing weight
   α — collapses at large N.** Holding (shape, α, tier) fixed and increasing N,
   coverage falls from ~1.0 to ~0.0 while bias stays small and roughly constant
   (posterior concentration / semiparametric Bernstein–von Mises). It measures
   asymptotic interval calibration, not recovery adequacy.

A prior-art scout established that **no surveyed community** (radiocarbon SPD via
rcarbon/Crema 2022; the baorista Bayesian-aoristic analogue, Crema 2025;
Bayesian-workflow SBC, Talts 2018 / Modrák 2025) gates on exact CI coverage of a
mixing parameter; that flat/uniform is a standard *tested null* in SPD work; and
that Wasserstein-1 is the theoretically-justified deconvolution-recovery metric
(Rousseau & Scricciolo 2021). A `/review-implementation` pass additionally found
that (a) SBC does **not** fit our fixed-true-value grid (it needs α drawn from
the prior), so ROPE/tolerance is the right large-N-robust α check, not SBC;
(b) posterior z-score carries the *same* large-N fragility as coverage; and
(c) a single global Wasserstein-1 threshold is unfair across shapes, so a hybrid
(patch only the undefined flat case) is cleaner. A preview (recomputed from
stored posteriors, no re-fit) showed α is recoverable only to ≈±0.18 (90th-pct
|bias| in the operating envelope) — so gating α honestly fails; gating on p_gen
shape within the operating envelope passes at 91.9% (this 2026-06-02 preview
figure is superseded — now 98.6% under the field-standard gate; see the
2026-06-04 update note above).

### Decision

**Correct the recovery-grid binding criterion (OSF Amendment 01 §A5.5.1) and
report the grid as a recoverability map with an operating envelope:**

- **Shape gate (binding), hybrid:** Pearson r ≥ 0.95 for **non-flat** shapes
  (**unchanged from lodged prereg**); Wasserstein-1 ≤ **T_flat = 10 y** for the
  flat shape only. W1 reported supplementary for all shapes.
- **Convergence precondition** (≥90% replicates, R̂ < 1.01) made an explicit gate.
- **α demoted** from binding gate to a **quantified diagnostic** (report signed
  bias and its ≈±0.18 precision); all α-derived paper claims hedged to that
  precision. This is supported by the project already characterising the
  convention component (`p_conv`) **descriptively** from raw interval structure
  (the F1+F3 family classifier), so a precise model-derived α dial is not
  required.
- **Operating-envelope reframe:** the binding criterion is evaluated where the
  deconvolution is identifiable (empirically α ≤ 0.70); cells with α ≥ 0.95 are a
  reported stress sensitivity. Where the real corpus exceeds the envelope,
  genuine-signal claims are flagged as degraded.

### Consequences

- **Thresholds pre-committed** (T_flat from well-recovered flat cells' max W1;
  envelope from near-unidentifiability at α ≥ 0.95) before the headline verdict;
  failing scenarios (full-grid, α-gated) reported alongside the passing one.
- **Real-corpus check (diagnostic b, 2026-06-02):** the descriptive convention
  fraction is **≈0.65 corpus-wide** (just inside the envelope) but **exceeds 0.70
  across AD ~142–347** (21 of 80 bins) — so late-corpus genuine-signal claims sit
  in the degraded zone and must be hedged. (`runs/2026-06-02-recovery-utility-
  check/`.)
- **Band-calibration check (diagnostic a, 2026-06-02):** the p_gen credible band
  is honest for *smooth* timelines (≈0.99 pointwise 95% coverage) but
  **overconfident for sharply-peaked timelines and degrades at large N** (mean
  coverage 0.90 at N=2000 → 0.67 at N=50000; regnal_cluster 0.23 at N=50000) — the
  same posterior-concentration mechanism, compounded by the GRW smoothness prior
  not representing sharp features. The *median* (point) timeline stays trustworthy
  (the gated quantity); reported *bands* for peaked regimes must be widened/caveated.
  Logged as a limitation, not a new gate. (`runs/2026-06-02-recovery-utility-check/`.)
- **Harness update pending:** `grid-summariser.py` / `compare-grids.py` still
  compute the lodged criterion; they will be updated to §A5.5.1 (no re-fit needed:
  W1 and α intervals are stored) once Martin signs off the α-diagnostic
  operationalisation.

### Provenance / links

- OSF Amendment 01 §A5.5.1: `planning/osf-amendment-2026-05-29-two-measure-framework.md`.
- Scout + review record: `planning/prior-art-scout-2026-06-02-recovery-validation-metrics.md`.
- Utility review: `planning/recovery-grid-utility-review-2026-06-02.md`.
- Grid A verdict: `runs/2026-05-26-recovery-grid-two-unit/inscription-mass/outputs/REPORT.md` (commit `0638093`).
- Diagnostics: `runs/2026-06-02-recovery-utility-check/`.

### Revisit triggers

- Martin recommends a different α-diagnostic operationalisation or a different
  operating-envelope cut.
- The real-corpus fits land α materially above 0.70 even at empire level (would
  widen the degraded-zone caveat).
- The band-calibration check shows the p_gen bands are materially miscalibrated
  (would require widening reported bands or a calibration adjustment).

## Decision 34 — 2026-06-03: Subset analyses use subset-specific deconvolution; do NOT de-fog subsets with the empire-wide p_conv

**Status:** decided by Shawn 2026-06-03; supersedes the prereg's implicit
"empire-correction-applied-to-subsets" framing for H3b; amendment-relevant
(to be folded into an OSF amendment alongside the §A5.5.1 criterion clarification).
**Decided by:** Shawn 2026-06-03, in the strategic discussion of where the
method's utility lies.

### Context

Verifying the H3b mechanism (2026-06-03) found that the prereg says H3b "scans
mixture-corrected SPAs on subsets" but **does not pin how** a subset SPA is
corrected, and that the Stage-3 convention component `p_conv` is **corpus-wide-
fixed** (Stage-3 plan risk ii: province-/type-level convention heterogeneity "not
yet absorbed"). So the only specified path was to impose the empire-average
convention shape on every subset.

Shawn's position: **the empire-scale fit is a valuable proof-of-concept and
narrowly useful in its own right (e.g. as a population / information-flow proxy
after cohort de-skewing), but the real research payoff is at the subset level** —
provinces, cities, regions, and inscription subcategories. The motivating
re-application case is a collaborator's ~2,000 mother–daughter inscriptions, for
which the desired contribution is a **temporal element beyond eyeballing
histograms**. Imposing the corpus-average convention structure on a subset that
may have its own convention profile (e.g. a Greek-East province, an epitaph-heavy
subcategory) is an unvalidated approximation and undercuts the subset payoff.

### Decision

**Subset SPAs are de-fogged by a subset-specific mixture fit** (the model learns
the subset's own convention mix — `build_model_f1_f3` already learns
`tier_weights`, i.e. the convention composition, from the subset's own data; only
the universal template-width *basis* is fixed, not corpus content). **The empire-
wide `p_conv` is NOT applied to subsets.** The empire fit remains a proof-of-
concept and a candidate empire-scale proxy (see the significance/applications
note), not the engine of subset analysis.

### Consequences

- **Feasibility is N-dependent — floor now MEASURED (2026-06-03).** A standalone
  per-subset fit is harder to identify at small N. The **small-N deconvolution-
  reachability study** (`runs/2026-06-03-small-n-reachability/`; 4,200 fits across
  84 cells = 3 shapes × 4 α × 7 N, checkpointed) measured the floor under the
  Decision-33 criterion. **Within the operating envelope (α ≤ 0.70), reliable
  recovery has a worst-case floor of N ≈ 2000**, dropping to **N ≈ 500** for the
  easiest subsets (α ≈ 0.30, smooth_growth / rise_and_fall); two α = 0.70 cells
  (regnal_cluster, smooth_growth) are **unreached even at N = 2000**, and the
  α = 0.85 stress row is unreached throughout. Mean shape-recovery rate (α ≤ 0.70)
  climbs 12 % (N=50) → 94 % (N=2000); convergence ≈ 100 %; band coverage degrades
  0.98 → 0.88 with N (the Decision-33 band-overconfidence finding) and mean
  |α-bias| ≈ 0.13 (inside the ±0.18 envelope precision). This replaces the
  prereg's rough "unidentified below N≈100" prior with a measured reachability map
  (`outputs/REPORT.md`, `outputs/figures/reachability-map.png`). The ~2,000
  mother–daughter motivating corpus sits **right at this worst-case floor** —
  feasible but near the boundary.
- **Below the floor:** fall-back options (partial-pooling of convention across
  subsets — a §5-style borrow; or descriptive reporting; or the §5 hierarchical
  trajectory model). Out of scope for the reachability study; logged for later.
- **Prereg/amendment:** this supersedes the H3b "empire-correction-applied"
  reading and the "per-city mixture not pursued" framing. Fold into the OSF
  amendment (with §A5.5.1). H3b subsets become per-subset fits gated by the
  measured reachability floor (and by the existing Phase-1 detection thresholds).
- **Paper framing:** the subset-level temporal de-fogging is the **core
  re-application case** that justifies the detailed JAMT methods presentation and
  a reusable/repurposable codebase (see
  `planning/paper-significance-and-applications-2026-06-03.md`).

### Provenance / links

- H3b mechanism verification: prereg §"Scope of the mixture correction" (line 35),
  H3b §(lines 96–99); Stage-3 plan exec-summary risk (ii)
  (`planning/h2.1-stage-3-implementation-plan-2026-05-25.md`).
- Reachability study: `runs/2026-06-03-small-n-reachability/spec.md`.
- Significance/applications: `planning/paper-significance-and-applications-2026-06-03.md`.

### Revisit triggers

- The reachability floor turns out so high that few real subsets qualify — would
  promote the pooled-convention fall-back from "later" to "needed."
- A subset class is found to have a convention profile so different from the
  corpus that even subset-specific fitting with the universal template basis is
  inadequate (would motivate per-class convention bases).

## Decision 35 — 2026-06-04: H2 production model is the validated `build_model_f1_f3`; the empirical-Bayes calibration-cohort redesign is retired as primary (kept descriptive + one empire-level sensitivity); H2 scope = empire + province + city

**Status:** committed; consistent with the lodged prereg + OSF Amendment 01
(§A5.7 already names `build_model_f1_f3` with learned `tier_weights`). No new
amendment required. Sub-question 3 (the H2 → H3a data dependency) is **RESOLVED
2026-06-04** — see the addendum at the end of this decision.
**Decided by:** Shawn 2026-06-04, on the pre-launch reconciliation review of the
2026-05-25 Stage-3 implementation plan against Decisions 33 + 34 and the
completed two-unit recovery grid.

### Context

The Stage-3 implementation plan (`planning/h2.1-stage-3-implementation-plan-2026-05-25.md`)
was built around an **empirical-Bayes calibration-cohort** model redesign: *fix*
`p_conv` from the Stage 1 corpus estimate (SCUBIDO) and *centre* `p_gen` on the
Stage 2 cohort shape (BUMPER), to break the α–shape likelihood ridge behind the
2026-05-22 recovery FAIL. The pre-launch reconciliation review found that redesign
overtaken by events:

1. **The recovery grid validated a different (simpler) model.** `cell_lib.build_model_f1_f3`
   — the one that scored 98.6 % (Grid A) — *learns* `tier_weights ~ Dirichlet([1,1,1])`
   and uses a *zero-mean* GRW `p_gen`; only F1 (α ~ Beta(1,1)) and F3 (non-centred
   GRW reparameterisation) differ from the lodged-prereg model. It does **not** use
   the empirical-Bayes priors. The empirical-Bayes redesign has never had a recovery
   validation.
2. **Decision 33 dissolved its rationale.** The 2026-05-22 FAIL was predominantly a
   *metric* artefact; with the corrected criterion + F1+F3 the simple model passes,
   and α is demoted to a diagnostic (±0.18) — so "fix α-recovery bias" (the plan's
   stated goal) is no longer the target.
3. **Decision 34 contradicts fixed `p_conv`.** Subsets must learn their own
   convention mix; the empire-wide `p_conv` is not imposed. The plan's fixed-corpus-
   `p_conv` design is exactly what Decision 34 rules out, and Decision 34 (and OSF
   Amendment 01 §A5.7) name `build_model_f1_f3` explicitly.

### Decision

1. **Production model (confirmed).** H2 uses the validated `build_model_f1_f3`:
   learned `tier_weights` (convention mix) over the fixed universal template-width
   `tier_basis`; zero-mean non-centred GRW `p_gen`; α ~ Beta(1,1); default PyMC
   NUTS. The empirical-Bayes calibration-cohort model redesign is **retired as the
   primary**. The 2026-05-25 Stage-3 plan is **superseded** by this decision (a
   pointer banner is added to that file).
2. **Empirical-Bayes artefacts retained, but not as the primary fitted model.**
   The Stage 1 `p_conv` and Stage 2 `p_gen` empirical estimates are kept (a) as the
   project's **descriptive** characterisation of the convention component (the
   paper's account of the editorial-template structure; cf. Decision 33), and (b) as
   a **single optional empire-level informative-prior sensitivity** — the one level
   at which a corpus-wide `p_conv`/`p_gen` is defensible (no subset-heterogeneity
   objection at the empire scale). Not run on provinces/cities/subsets (Decision 34).
   *Watch-out:* report it as a sensitivity only, and keep the prior wide enough that
   it cannot manufacture the result it is meant to test against — it is a robustness
   check on the learned-`p_conv` primary, not a competing headline.
3. **(RESOLVED 2026-06-04 — see addendum below.)** Whether
   `data/processed/city_level_for_h3a.parquet` is the temporal-mixture-deconvolved
   output or the date-window-filtered city counts. Resolved against the prereg:
   it is the date-window-filtered counts; the mixture does NOT feed H3a.
4. **H2 scope for this paper = empire + province + city** analysis units
   (inscription-mass only — letter-mass FAILed recovery, Obs 72). Other named
   subsets (e.g. the ~2,000 mother–daughter corpus, the motivating re-application
   case) are **held for later**.

### Consequences

- **Lodged-record consistency.** OSF Amendment 01 §A5.7 already describes
  `build_model_f1_f3` with learned `tier_weights`, so the production model is
  amendment-consistent; no new amendment is needed for this decision. Two minor
  wording notes (no action on the lodged deposit; for paper-language accuracy
  only): (i) the amendment's parenthetical "(F1+F3, empirical-Bayes) pipeline"
  (line 286) loosely labels the model "empirical-Bayes" — the *primary* is the
  learned-`p_conv` F1+F3 model, and the paper should use that accurate description,
  reserving "empirical-Bayes" for the optional empire-level sensitivity. (ii) The
  lodged prereg (§3 line 206) states α ~ Beta(2,2); the production model uses F1's
  Beta(1,1), which the amendment references via "F1+F3" and the validated grid — a
  minor prior refinement, not a new substantive change (F1 follow-up: Δα ≈ +0.025).
- **Reporting discipline (carried from Obs 68 / 73).** Report the posterior-median
  `p_gen` timeline (the gated quantity); widen/caveat the credible band in peaked
  regimes — the real corpus has sharp regnal clustering and the late corpus
  (AD ~142–347) sits in the degraded-recovery zone (Obs 69).
- **Reachability gating (Decision 34).** Province/city fits are gated by the
  measured reachability floor (worst-case N ≈ 2000 in-envelope); units below the
  floor fall back to date-window-filtered counts or the §5 hierarchical model.
- **Next artefact.** Once sub-question (3) is resolved, write the H2 launch spec
  (validated model + Decision-34 scoping + real-corpus data prep) for sign-off.

### Provenance / links

- Reconciliation review: this session (2026-06-04), against
  `planning/h2.1-stage-3-implementation-plan-2026-05-25.md` (superseded).
- Validated model: `runs/2026-05-26-recovery-grid-two-unit/code/cell_lib.py`
  (`build_model_f1_f3`); Grid A 98.6 % (`…/comparison/COMPARISON-REPORT.md`).
- Upstream decisions: Decision 33 (criterion correction; α demoted); Decision 34
  (subset-specific deconvolution); Decision 22 (H3a date-window counts — bears on
  sub-question 3); OSF Amendment 01 §A5.5.1 / §A5.7.

### Revisit triggers

- Sub-question (3) resolution may add an addendum.
- If the empire-level empirical-Bayes sensitivity materially diverges from the
  learned-`p_conv` primary, that divergence becomes a reported finding (and a prompt
  to ask which is mis-specified), not a silent discard.

### Addendum 2026-06-04 — sub-question 3 (H2 ↔ H3a) resolved; sequencing = cross-sectional first

**Resolution (from the lodged prereg; nothing new to decide, only to record).**
H3a uses **date-window-filtered counts**; the Bayesian mixture is **not** applied
to H3a's input. Prereg §"Scope of the mixture correction" (line 35): "H3a and H3c
are cross-sectional analyses operating on date-window-filtered counts — H3a
directly"; §3 line 229: "`y_c` is the per-city inscription count under the 50 BC –
AD 350 date-window filter. The Bayesian mixture is *not* applied to `y_c`";
Decision 22 (the originating decision). Therefore:

- `data/processed/city_level_for_h3a.parquet` = per-city **date-window-filtered
  count + Hanson (2016) population + province label** — a filter-and-join data-prep
  product, **NOT** a mixture/deconvolution output. The priority-queue phrasing "H2
  (mixture) outputs `city_level_for_h3a.parquet`" was loose; it bundled this cheap
  prep under the "H2" label. The two are distinct artefacts.
- The mixture's empire-level posterior α is reported as **descriptive context**
  beside H3a, but neither H3a's confirmatory decision rule nor H3c's residuals are
  gated on it (prereg line 35 / 229).

**Consequence — two decoupled tracks; primary result does not wait on the mixture.**

- *Cross-sectional track:* date-window city-count prep → **H3a** (primary
  confirmatory result) → **H3c** (Pearson residuals from H3a). No mixture needed.
  Largely already built as preliminary/probe work: `runs/2026-05-21-talk-prep/code/`
  (`01-filter-and-prep.py`, `03-hanson-nbr-bootstrap.py`, `05-h3a-bayesian-mundlak.py`)
  and the letter-mass counterpart in `runs/2026-05-26-letter-count-probe/code/`.
- *Temporal track:* **H2.1 mixture deconvolution** (`build_model_f1_f3`, per unit)
  → **H3b** deviation-detection + **§5** trajectories. Mixture needed.

**Sequencing decision (Shawn, 2026-06-04): cross-sectional track FIRST.** Bring the
existing talk-prep H3a up to preregistered confirmatory standard (canonical
`city_level_for_h3a.parquet`; exact prereg priors; full PPC suite; brms shadow;
§5 variance partition; three-way decision rule; then H3c). The H2.1 mixture
(the methodological contribution, for H3b/§5) follows. Rationale: front-loads the
paper's headline confirmatory result, which is nearly in hand and independent of
the harder mixture build. Next artefact: an audit of the talk-prep H3a code against
the prereg, then the H3a confirmatory launch spec for sign-off.

## Decision 36 — 2026-06-05: Latin-speaking provinces are the first-class frame for hypothesis-testing; empire-wide is secondary/context (→ OSF Amendment 02)

**Status:** committed; **reshapes the primary analysis frame → required OSF
Amendment 02** (Shawn approved 2026-06-05). **Amendment 02 LODGED 2026-06-06**
(git tag `osf-amendment-02-2026-06-06`; package
`planning/osf-amendment-2026-06-06-latin-frame.{md,pdf}`,
`osf-amendment-02-justification.txt`, `osf-amendment-02-summary-addendum.md`) →
**the Latin-frame confirmatory gate is CLEARED**: the Latin-primary confirmatory
results (H3a `f_within` 0.480, SR1 0.505, H3c(i) capital SUPPORTED, H3c(ii)
not-supported) may now leave the repository as confirmatory. The 39-vs-41
province reconciliation is resolved in the amendment §A5.3
(`runs/2026-06-06-amendment-02-prep/`): Italia + Alpes Graiae classify Latin but
contribute zero Hanson-matched cities, so the realised frame is 817 cities / 39
provinces with no result impact. The empire-wide H3a result remains within the
original lodged prereg's "all cities" text and is retained as secondary/context.
**Follow-up:** the `PRELIMINARY -- pending OSF Amendment 02` labels in the Latin
result artefacts (`runs/2026-06-04-h3a-confirmatory/outputs/` h3c-latin /
sr1-latin / REPORT-latin-h3c-sr1 / REPORT-h3c-i-capital-contrast) can now be
flipped to confirmatory.
**Decided by:** Shawn 2026-06-05, reviewing the H3a confirmatory result (Latin-only
`f_within` 0.480 vs empire-wide 0.299) against the dataset-coverage rationale.

### Context

The H3a blind run showed the within-province population effect is markedly stronger
on the Latin-province subset (`f_within` 0.480, β_within 0.733; 817 cities / 39
provinces) than empire-wide (0.299, β_within 0.587; 1,044 cities / 56 provinces).
More importantly, there is a **coverage confound** in the empire-wide frame: the
dataset is **LIRE — "Latin Inscriptions of the Roman Empire"**, drawn from the
larger **LIST — "Latin Inscriptions through Space and Time"**. In Greek-speaking
provinces, Latin inscriptions are a distinct minority, so LIRE captures only a
non-representative Latin slice of those provinces' epigraphic production; Greek
epigraphic coverage is inconsistent and **new Greek datasets are in production**.
Empire-wide hypothesis-testing therefore mixes well-covered Latin provinces with
poorly-covered Greek ones — a confound for any claim about epigraphic *production*.

Note the irony: the prereg's stale parenthetical "~815 cities" figure **was** the
Latin-province filter (the 2024-notebook province→language map). So the Latin frame
was latent in the prereg's own number; the over-broad "all cities" text (1,044) was
the reading that introduced the confound. Shawn: "it should have been specified in
the original prereg, I just missed it."

### Decision

1. **Latin-speaking provinces are the primary / first-class frame** for the
   hypothesis-testing analyses — **H3a (primary), H3b, H3c, and SR1**. Empire-wide
   results are reported as **secondary / context**, with the coverage caveat stated.
2. **Unit = Latin-speaking provinces, not Latin-only inscriptions.** Latin-only
   *inscriptions* was considered but rejected for now (bilingual / mixed contexts,
   language-classification noise, and it abandons the provincial-coverage logic that
   is the actual motivation). The province-level frame is chosen; the **primary
   rationale is coverage** (the dataset is approximately complete for Latin
   provinces, incomplete for Greek ones). Operational definition: the
   province→language map at
   `runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv` (39 Latin
   provinces / 817 cities; to be promoted to a first-class tracked artefact).
3. **Rerun H3c + SR1 on the Latin subset.** The Latin H3a `f_within` (0.480) is
   already computed (blind-run Sensitivity B); H3c (Moran's I on Latin residuals)
   and SR1 (OLS log-log on Latin) are the outstanding pieces — cheap, off the
   existing Latin posterior (`idata-latin.nc` on sapphire). Run as the focused
   follow-up that finalises the cross-sectional track under the Latin frame.
4. **The H2.1 temporal track also focuses on Latin provinces** — informs the H2.1
   unit-set open decision (do not spend the mixture on Greek-province units whose
   coverage is the confound).

### Consequences

- **OSF Amendment 02** (to draft): reframe the primary hypothesis-testing frame to
  Latin-speaking provinces; H3a/H3b/H3c/SR1 primary-on-Latin; empire-wide secondary
  with the coverage caveat. Justification strengthened by the prereg's own ~815
  (Latin) figure. Until lodged, the Latin-primary numbers stay "preliminary".
- **Empire-wide H3a (`f_within` 0.299) is verified and retained as secondary/
  context** — within the original lodged prereg text, so not itself amendment-gated.
- **Latin-frame headline (preliminary, pending Amendment 02 + the Latin H3c/SR1
  rerun):** `f_within` 0.480 [0.401, 0.566], β_within 0.733 [0.648, 0.820].
- **The province→language map becomes a first-class artefact** (it defines the
  frame); copy it from the run dir to a tracked, documented location.
- The flexible-dispersion model refinement (a separate future improvement) is logged
  in the backlog (Phase 3).

### Provenance / links

- H3a REPORT: `runs/2026-06-04-h3a-confirmatory/outputs/REPORT.md` (Sensitivity B).
- Frame definition: `runs/2026-06-04-h3a-confirmatory/data/province-language-map.csv`.
- Upstream: Decision 22 (date-window counts); Decision 35 + addendum (model + H3a-first).
- Downstream: OSF Amendment 02 (to draft); the Latin H3c/SR1 rerun task.

### Revisit triggers

- The in-production Greek datasets arrive and materially improve Greek-province
  coverage — would reopen the empire-wide frame as a defensible primary.
- The Latin-only-*inscriptions* frame is revisited if the bilingual / classification
  issues prove tractable and a reviewer presses for it.

## Decision 37 — 2026-06-05: H2.1 temporal-mixture launch design (D1–D6 from the walkthrough) + cross-sectional sign-off

**Status:** committed; the design inputs for the (not-yet-written) H2.1 launch
spec. Captured here because the six decisions were worked through interactively
and otherwise live only in the session transcript. Nothing has been launched —
the H2.1 run is gated on (a) the template-dictionary scan (prerequisite, below)
and (b) Shawn's sign-off of the launch spec.
**Decided by:** Shawn 2026-06-05, in a decision-by-decision walkthrough.

**Cross-sectional-track sign-off (2026-06-05).** Shawn signed off the
cross-sectional track: **H3a** (f_within SUPPORTED), **H3c(i)** (capital contrast
SUPPORTED — capitals over-produce, OXREP-authoritative + AD-117 sensitivity),
**H3c(ii)** (Moran's I NOT-supported), **SR1** (OLS comparator), **SR2** (i+ii).
**Empire-frame results are now final**; **Latin-frame results remain
amendment-gated** (pending OSF Amendment 02, Decision 36) and must not leave the
repo as confirmatory until it is lodged.

### The six H2.1 launch decisions

- **D1 — unit set.** Empire-aggregate (180,609; secondary/context) + Latin-aggregate
  (109,646; primary) + the **19 Latin provinces clearing N ≥ 2,000** + the **5 Latin
  cities clearing N ≥ 2,000** (Ostia, Mogontiacum, Aquileia, Pompeii, Salona). Gate
  = deconvolution-reachability floor **N ≥ 2,000** (Decision 34); the 2 grey-band
  provinces (1,549–2,000) are a caveated option. Sub-floor units fall back to
  date-window counts / §5 (not a standalone mixture). ~26 primary fits.
- **D2 — H2.1 → H3b interface.** H2.1 hands H3b the **posterior-median** corrected
  genuine SPA; H3b's permutation envelope is the uncertainty representation — **no
  mixture-posterior propagation** (prereg line 35; Obs 68/73). Follow-up: a
  **raw-SPA-vs-corrected-SPA** H3b comparison (the GRW attenuates sharp peaks, so
  corrected may be conservative at the Antonine probe). H2.1 ⟂ §5 (complementary
  coverage; optional high-N cross-check on the 5 cities). **Reconcile the 39-vs-41
  Latin-province list in Amendment 02.**
- **D3 — bins.** 5-year bins / 80 bins / 50 BC – AD 350 (the recovery-validated
  configuration). No coarser-bin variant.
- **D4 — empire-level empirical-Bayes sensitivity.** One EB run on the
  empire-aggregate with corpus-wide Stage-1/2 priors, **informative-but-wide**
  (Dirichlet η ≈ 200·w_emp + 1.5× σ — data-dominated, can't manufacture the result);
  judged by Pearson r / Wasserstein-1 vs the learned-p_conv primary. Latin-re-derived
  EB deferred (run only if the empire EB diverges or a reviewer presses).
- **D5 — real-data acceptance (no ground truth).** Reportability gates: convergence
  (`cell_lib.convergence_pass`, R̂/bulk-ESS) AND operating envelope (N ≥ 2,000 AND
  posterior α ≤ 0.70). No-truth evidence: descriptive-`p_conv` consistency (model
  convention vs the F1+F3 family-mass fraction) + posterior-predictive adequacy.
  Reporting: posterior-median SPA; caveat bands in peaked regimes (Obs 68/73); flag
  the late corpus AD ~142–347 as `p_conv`-dominated (Obs 69); α with ±0.18 precision
  (Decision 33). Tiers: reportable / caveated / fall-back.
- **D6 — run plan.** Sapphire; validated sampler (`build_model_f1_f3` defaults;
  raise tune if a unit fails convergence, never relax the gate); **non-blind** (no
  preliminary real-corpus mixture exists). Observation model = **largest-remainder
  rounding** of the per-bin aoristic-mass SPA to integer counts summing to N_eff
  (prereg line 183), then `y ~ Multinomial(N_eff, p_mix)`. **Full-scope
  supplementaries** (Shawn): aoristic-MC (Decision 28) on **all 26 units** + the
  Dirichlet-multinomial and rescaled-NegBin model-comparison fits (Decision 19);
  pin N_MC ∈ [20,50] + the 1.5× divergence flag in the design artefact.
  **Parallelism capped at 12 physical cores** (`n_jobs=12`, `taskset -c 0-11`,
  `PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False`; 2026-05-22 SMT lesson). ~800 fits,
  ~1 h parallelised.

### Audit-driven additions the launch spec must also fold in (2026-06-05 audit)

- **Template-dictionary empirical scan — PREREQUISITE** (audit A2; Decision 20;
  prereg line 202). Scan LIRE exact-match interval templates; include templates with
  N ≥ a threshold to be **pinned from the empirical template-frequency distribution**
  and committed as the design artefact **before** the real-data mixture fit. The
  recovery grid used synthetic/proxy bases; no real-LIRE three-tier mixture has run.
- **Trapezoidal-aoristic sensitivity** (audit C11) on the empire SPA + every
  H3-eligible subset (empire r = 0.94 < 0.95 already trips "report alongside
  uniform").
- **H2.2 / H2.3 / H2.4 consistency checks + empire-α descriptive context** (audit
  C13–C16) — all off the same real-data fit.
- Latin-province focus (Decision 36) shapes the unit set; production model =
  `build_model_f1_f3` (Decision 35).

### Next-session actions (the H2.1 prep arc)

1. Template-dictionary empirical scan (propose + commit the N-threshold design
   artefact). 2. Write the H2.1 launch spec from D1–D6 + the audit additions →
   Shawn sign-off. 3. Launch H2.1 on sapphire. (Separately, Shawn: draft + lodge
   **OSF Amendment 02** — Latin-primary frame + 39-vs-41 reconciliation.)

---

## Decision 38 — 2026-06-06: Convention component is an empirical calendar-slab basis (no reign tier); reigns/dynasties/events are genuine-but-aoristic; fine-grained brackets ride as a sensitivity band; recovery re-validation + OSF amendment gate the H2.1 fit

**Status:** committed (design decision). **Supersedes** Decision 20's tier typing
(century / half-century / **reign**) and, specifically, the reign-interval-slab
*convention* tier. **Refines** Decision 37 (the H2.1 launch spec must be rewritten
around this, and the launch is now additionally gated on the recovery
re-validation below).
**Decided by:** Shawn 2026-06-06, in an extended decision-by-decision walkthrough
with CC. Grounded by: the template-dictionary scan (`runs/2026-06-05-template-dictionary/`,
commit `6d8950f`); a source re-read of the F1/F2_Other/F3/Tight/Big family
classifier and of `build_model_f1_f3` / `build_tier_basis`; the Stage-1 empirical
`p_conv` 9-slab decomposition (`runs/2026-05-24-empirical-pconv/`); and a
verified lit-scout on epigraphic dating practice (report
`/tmp/lit-scout-verifier/report-20260605-224611.md`; key works below).

### Context

- **The curated 3-tier basis is empirically inadequate (Decision 20 revisit
  trigger fired).** The template-dictionary scan found multi-century slabs are
  ~31 % of the F1+F3 convention pool and were **entirely absent** from the curated
  century / half-century / reign dictionary (the single most frequent template
  corpus-wide is `[301, 500]`, 8.8 %); reign templates are only ~2.7 %. The
  recovery grid (Grid A 98.6 %) ran on **synthetic proxy** tier weights over the
  curated basis — no real-LIRE three-tier mixture has ever been fit.
  > **Reconciliation note (added 2026-06-20, results-documentation uplift).** The
  > "~31 %" above does **not** reproduce from either cited artefact. The
  > template-dictionary scan
  > (`runs/2026-06-05-template-dictionary/outputs/tables/category-mass.csv`) gives
  > **24.96 %** for the *full* empire convention pool (`multi_century` group), and
  > the empirical-pconv Stage-1 decomposition
  > (`runs/2026-05-24-empirical-pconv/outputs/tables/slab-type-weights.csv`) gives
  > **35.93 %** for the *F1+F3* pool specifically (two_century 23.69 % +
  > one_and_a_half_century 7.29 % + three_century 4.95 %). "~31 %" is neither; it
  > reads as a rough split-the-difference across the two framings. The
  > load-bearing values are **24.96 % (full pool)** and **~36 % (F1+F3 pool)**.
  > Full reconciliation: **Obs 76** (`docs/notes/working-notes.md`).
  > **Write-up flag — DO NOT silently edit here:** the "~31 %" wording was carried
  > into **lodged OSF Amendment 03** (`planning/osf-amendment-03-justification.txt`,
  > `planning/osf-amendment-03-summary-addendum.md`,
  > `planning/osf-amendment-2026-06-07-convention-basis.md`), so this is not a
  > purely-internal figure. The lodged amendment text is left **unaltered** (its
  > "~31 %" is the historical lodged record). Whether to footnote the corrected
  > 24.96 % / ~36 % in the paper, lodge a clarifying amendment, or leave the
  > rounded approximation as-is in the lodged record is **Shawn's decision** — the
  > directional argument (multi-century mass is a large, previously-unmodelled
  > share; reigns are small) is robust under either exact value.
- **What the production model actually is.** `cell_lib.build_model_f1_f3` learns
  `tier_weights ~ Dirichlet` over a fixed `tier_basis`; it does **not** use the
  family classifier, and Decision 35 retired the empirical-Bayes fixed-`p_conv`
  redesign (the Stage-1/2 empirical estimates survive only as descriptive context
  + the optional empire-level EB sensitivity, Decision 37 D4). The Stage-1
  decomposition already splits F1+F3 into 9 width-based slab-types and already
  **excludes** reigns (F2_Other) — i.e. it already embodies the principle below,
  but on the population the production basis should adopt.
- **The reign contradiction.** The lodged prereg + Decision 20 place a
  reign-interval slab tier *inside* `p_conv` (convention). This contradicts (a)
  the family classifier, which holds reigns out as F2_Other ("signal-but-aoristic"),
  and (b) the conceptual reality. The classifier itself splits reigns
  inconsistently by width-accident: `[117, 138]` (Hadrian) → F2_Other (held out),
  but `[161, 180]` (Marcus, decade-aligned) → F3 (convention). No prior decision or
  amendment resolved this.
- **The grid-quantisation model of "convention" (the conceptual core).**
  Convention is **not** signal-free. Every recorded date carries evidential
  anchoring (Cooley 2012 — letterforms, onomastics/prosopography, formulae,
  consular dates, find-context). What makes a date *conventional* is the
  **arbitrary rounding of genuine-but-coarse evidence onto the BC/AD calendrical
  lattice** (centuries, half-centuries). That snapping introduces two artefacts:
  (i) **per-inscription distortion** — a true off-grid range (e.g. a letterform in
  use ~AD 178–323, perhaps trapezoidally) is truncated/shifted to a round century
  (`[200, 299]`) and flattened to uniform-within-bin; and (ii) **cross-inscription
  artificial alignment** — many different true distributions snap to the *same*
  bin, manufacturing the plateau-step pile-ups at century boundaries that the SPA
  shows. The discriminator between convention and genuine is therefore **grid-
  snapping (observable as grid-alignment)**, not criterion-type (which was dropped
  from LIRE — `raw_dating` preserves only the numeric range). This is distinct
  from radiocarbon SPD (genuine measurement/calibration uncertainty; no arbitrary
  rounding), and is likely **shared with ceramic typological dating** (round-period
  pinning) — which strengthens the methods-bridge framing.

### Options considered (tier structure)

- **A — keep the curated 3 tiers (century / half-century / reign).** Rejected:
  empirically broken (no home for the ~31 % multi-century mass; over-weights reign).
- **B — expand to ~5 typed tiers.** Faithful but changes the learned-weight count
  → full recovery re-validation and a larger amendment.
- **C — single combined fixed-shape convention (estimate α only).** Most
  parsimonious but discards the prereg-committed learned tier weights.
- **D — empirical calendar-slab basis grouped to ~3 structural tiers (chosen).**
  Adopts the Stage-1 slab shapes, drops the reign tier, keeps the learned-weight
  count near the recovery-validated 3.

### Decision

1. **Historical-anchor principle (generalisable).** Date assignments tied to real
   historical events — **reigns, dynasties, datable events** — are
   **genuine-but-aoristic** ("Flavian" carries signal that "second half of the
   first century" does not). Pure calendar-segment rounding (Nth century /
   half-century / quarter-century / decade-window) is **convention**. Year-precise
   `[t, t]` remain genuine (unchanged).
2. **Grid-quantisation reframing.** Reframe the artefact (prereg/paper §2) as
   *genuine-but-coarse evidence quantised onto the BC/AD calendar grid*, not
   "editorial rounding ≈ no information"; retire the last trace of the
   "midpoint-spike" story. Redescribe `p_gen` as *"the temporal distribution with
   the calendar-grid quantisation removed"* — and state the honest limit: the
   method **un-snaps the collective** (removes the aggregate boundary pile-ups and
   flat-within-bin shape under the GRW smoothness prior); it does **not**
   reconstruct any single inscription's true off-grid latent distribution.
3. **Convention basis = empirical calendar slab-types**, built frequency-weighted
   from the F1+F3 **calendar** population (quarter / half / century / 1.5- / 2- /
   3-century + calendar decade-windows), with reign/dynasty/event intervals
   **removed via a curated historical-anchor interval list** so the split is
   **non-width-accidental** (this fixes the `[161, 180]`-type leak). **No reign
   tier** — reign/dynasty/event mass has no matching basis slab and flows to
   genuine.
4. **Tier grouping for the learned weights: ~3 structural tiers** (e.g. sub-century
   / century / multi-century), not 9 free weights — the multi-century plateaus are
   collinear and the recovery-hard case. The exact count is **settled by the
   re-validation** (a tight `Dirichlet(η·w_empirical)` over 9 shapes is the
   alternative the re-validation can test).
5. **Decadal + quarter-century brackets = sensitivity band** (~4–5 % of the
   corpus), not a hard classification: they are grid-snapped (convention side) but
   **low-distortion** (fine grid), so deconvolving vs not barely moves the result.
   Report both as a robustness band (the ceramics stacked-band idiom).
   *Empirical confirmation:* the event-leak into convention is ~0.1 % (essentially
   `[161, 180]`/`[161, 200]`); F2_Other (9.6 %) already correctly holds the
   reign/dynasty/event content out.
6. **Recovery RE-VALIDATION required before H2.1.** Grid A's 98.6 % validated the
   *old* basis shapes and does **not** transfer to a multi-century-bearing basis (a
   long flat envelope-edge plateau is confusable with genuine quiescence —
   plausibly *harder* to recover). Re-generate synthetics from the new empirical
   basis; run an **α = 0.95 × multi-century × peaked-genuine stress-triage first**,
   then the full grid only if it passes.
7. **Novelty positioning (verified).** The bracket-level convention-vs-genuine
   deconvolution **survives a verified forward-citation pre-emption chain** from
   Crema 2025. **Cite-and-distinguish** the nearest competitor — Tobalina-Pulido &
   Martín-Rodilla 2026 (`10.5334/jcaa.220`), a fuzzy-logic framework that
   *quantifies/propagates* inherited dating uncertainty but does **not** deconvolve
   convention from genuine spread. Method-level warrant: **Crema 2025**
   (`10.1111/arcm.12984`, Bayesian critique of the uniform-aoristic assumption).
   Dating-method authority: **Cooley 2012** (`10.1017/cbo9781139020442`); current
   inscription-dating monograph **Hartmann 2025** (`10.46771/978-3-96769-729-2`).
8. **OSF amendment required before the H2.1 fit.** Redefining the convention typing
   (→ calendar-slab, no reign tier), the basis-construction method, and the
   reign→genuine reclassification is a substantive model-structure change.
   **Separable from Amendment 02** (Latin-primary frame): the signed-off
   cross-sectional results use date-window counts, not mixture output (audit C16 /
   Decision 35 addendum), so Amendment 02 can lodge independently while the
   convention-model change rides its own amendment before H2.1.

### Consequences

- The H2.1 launch spec (Decision 37) is rewritten around this basis; the launch
  gate becomes **template-dictionary scan (done) → curated historical-anchor list →
  empirical calendar-slab basis (grouped ~3) → recovery re-validation (stress-triage
  → full grid) → OSF amendment → Shawn sign-off**.
- New work: (a) build the curated historical-anchor interval list (small; drawn
  from the F2_Other set + the calendar-aligned leaks); (b) rebuild the tier basis
  empirically (calendar slabs only, frequency-weighted, grouped ~3); (c) re-run
  recovery.
- The **EDH dating-criteria enrichment** (re-joining criteria via `EDH-ID`) is the
  empirical gold standard for the convention/genuine line but is **parked** pending
  the SDAM reply (Shawn queried them 2026-06-05 re: why the criteria were dropped
  from LIRE). It is a *citation-of-data* situation — no DOI'd EDH taxonomy paper
  exists; cite the EDH data dump + a methodology chapter.
- §2 reframed (grid-quantisation); the trapezoidal-aoristic sensitivity (Decision 4
  / audit C11) is the adjacent within-interval-shape question and remains in the
  launch spec.

### Revisit triggers

- The recovery re-validation fails at the new basis (poor α-recovery at the
  multi-century stress cells) → reconsider tier count/structure (fewer tiers;
  tighter empirical-anchored Dirichlet; or move the hardest multi-century shapes to
  a fixed component).
- The SDAM reply enables the EDH-criteria enrichment → the direct dating-criteria
  classification may supersede the grid-alignment heuristic.
- A deeper pre-emption chain or peer review surfaces a genuine prior bracket-level
  convention/genuine deconvolution → revisit the novelty framing.

### References

- `runs/2026-06-05-template-dictionary/` (scan; commit `6d8950f`);
  `runs/2026-05-24-empirical-pconv/` (Stage-1 9-slab decomposition);
  `runs/2026-05-26-recovery-grid-two-unit/code/cell_lib.py`
  (`build_model_f1_f3`, `build_tier_basis`).
- Decisions 4, 19, 20, 33, 34, 35, 37; prereg §3 lines 196–210, §2 line 25.
- Verified lit-scout report `/tmp/lit-scout-verifier/report-20260605-224611.md`;
  BibTeX `/tmp/lit-scout-bibtex-20260605-224611.bib`. Key citations: Crema 2025
  (`10.1111/arcm.12984`), Cooley 2012 (`10.1017/cbo9781139020442`), Hartmann 2025
  (`10.46771/978-3-96769-729-2`), Tobalina-Pulido & Martín-Rodilla 2026
  (`10.5334/jcaa.220`).
