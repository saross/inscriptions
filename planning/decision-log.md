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
