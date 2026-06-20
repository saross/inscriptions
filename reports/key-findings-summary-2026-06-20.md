# Inscriptions / LIRE deconvolution paper — key-findings summary (DRAFT)

**Date:** 2026-06-20 **Status:** DRAFT for Shawn's review before circulation to co-authors.
**Audience:** archaeologists and ancient historians. Plain language; jargon expanded on first use; every number cited to its source.

> **A note on traceability and on two things that look alike but aren't.** Every figure below is tagged
> with the Observation ("Obs N") in `docs/notes/working-notes.md` or the run REPORT it came from, all
> re-read at source for this draft. Two recurring traps for the reader, flagged here once:
>
> 1. **There are two different quantities both written "α".** The **genuine-fraction α** is the share of
>    a place's dated inscriptions that carry a *real* date signal rather than an editorial dating
>    convention (this is the deconvolution output). The **dispersion α** is an unrelated nuisance
>    parameter of the count regression. Where it could be ambiguous I say "genuine-fraction α" or
>    "mixture α". They are not the same number.
> 2. **Which set of provinces a number describes matters.** The project's lodged **primary** analytical
>    unit is the **Latin-speaking provinces with the city of Rome excluded** ("Latin-minus-Roma";
>    Amendment 02 / Decision 36). The **empire-wide / all-provinces** frame is reported as *context* only.
>    Numbers from the two frames are never merged. Within a frame, results can also be *unweighted* (the
>    primary), *population-weighted*, or *inscription-weighted*; and they can be measured in *inscription
>    counts* ("acts") or in *letter-mass* ("content"). Each figure below names its frame, weighting, and
>    measure.

---

## 1. The method, in one paragraph

The corpus is LIRE v3.0 (Latin Inscriptions of the Roman Empire): **182,853 inscriptions × 63 data
columns** (`runs/2026-04-23-descriptive-stats/outputs/summary.md`, corrected count). Many inscriptions
are not dated to a true historical moment but assigned a *round-number date slab* by editorial
convention — a tidy "AD 1–100" or a half-century box — which puts artefactual lumps of probability mass
on round years and century boundaries. To stop those editorial habits being mistaken for real history,
we built a **Bayesian deconvolution-mixture model**: for each unit it estimates a **genuine fraction α**
— the proportion of that unit's dated inscriptions whose dating is a real signal rather than a
round-slab convention — and separates the genuine dating signal from the convention artefact. The
production model is the **cross-classified ("library") likelihood**, adopted after the earlier design was
shown to add a spurious upward bias; the adopted version is recovery-validated. In a full simulation
where the right answer was planted and known — 300 parameter cells × 100 repeats — it passed all four
pre-set adoption criteria cleanly: it recovered the planted genuine fraction with essentially no bias
(mean absolute bias ≈ 0.021) and did so without harming the cases it should leave alone (Obs 89,
`cc-VERDICT-library.md`). A separate validity test (C10) plants a known α in synthetic data and confirms
the recovery works in the controlled setting (Obs 110). On the **whole empire pooled together**, the
estimated genuine fraction is **α = 0.6798, 95% credible interval [0.6649, 0.6970]** — i.e. roughly
**two-thirds** of empire-wide dated inscriptions carry a genuine date signal and about one-third are
round-slab convention (Obs 111, supp-wave REPORT; Latin-speaking provinces pooled: α = 0.7387
[0.6596, 0.7893]). All results below are **model-conditional**: they hold given this aoristic mixture
plus hierarchical (partial-pooling) model.

---

## 2. Temporal variation across scales — empire, province, city

A second, nested model (the "§5 Layer-A" decomposition) splits each city's inscription-rate-over-time
into shared and idiosyncratic parts, on **mid-sized cities** (268 small-N target cities; large
data-rich anchor cities deliberately held out — see §6). It separates: an **empire-wide common temporal
component** (the time-shape every city shares), a **province component**, and a **city-specific
component**, plus a between-city *level* spread (the cross-sectional, population-related axis).

**How big is each piece?** In comparable log-rate standard-deviation units (Obs 97, H5
`h5-decomposition.json`):

| Component | log-rate SD |
|---|---|
| Empire-wide common temporal component | 1.11 |
| Province temporal component | 1.02 |
| City-specific temporal component | 0.98 |
| Between-city *level* spread (cross-sectional / population axis) | 0.78 |

The empire-wide common component is the single largest piece — about **54% of a typical city's
temporal variance** (Obs 97). **Important caveat to state plainly:** the level/population axis (0.78) is
*understated here* because this mid-sized set excludes the size extremes, so this is **not** "timing
beats population" in the full corpus — temporal variation and the population axis live on different
axes. On the **Latin-minus-Roma diagnostic unit** (257 of the 268 cities) the decomposition is
essentially identical to all-provinces, because the set is ~96% Latin-West (Obs 97).

**When does the empire-wide common component peak?** **AD 187.5** — late-Antonine / Severan
(Obs 97, `h5-summary.json: empire_habit_peak_year`). This coincides with both MacMullen's
epigraphic-habit curve and the Antonine demographic apogee. **We deliberately do not call this "the
epigraphic habit"** — see the caveat in §6.

**The apparent post-AD-250 "collapse" — what it really is.** Inverting each city's *raw* trajectory into
a population-shape (Layer B) makes the median city look as though it falls to ~0% of peak by AD 250.
That is **not** demonstrated depopulation: it is mostly the empire-wide common component falling away,
amplified by the inversion (the exponent 1/β > 1 magnifies every dip; Obs 96). Once the empire-wide
common component is *removed*, the dramatic universal collapse dissolves into **moderate, heterogeneous,
provincial-tier relative decline** (Obs 103, Layer B residual). Reading the median city's level relative
to the empire baseline (q = 1 means "on the empire trend"; empire-β frame, reliable cities):

| Era (bin centre) | median q vs empire | share below empire |
|---|---|---|
| early-Antonine (AD 112) | 0.48 | 0.65 |
| empire-common peak (AD 188) | 1.01 | 0.50 |
| 3rd century (AD 262) | 0.32 | 0.68 |
| late (AD 338) | 0.67 | 0.53 |

So the typical mid-sized western city sits at about **one-third of its empire-relative baseline by the
3rd century** — a factor-of-~3 *relative* dip, not collapse — and about a third of reliable cities are
still at or above the empire trend even then (Obs 103). When the *province* layer is also stripped out,
the purely city-specific 3rd-century position is a mild ≈ 0.78: most of a small city's apparent
divergence is **its province's shared deviation, not its own** (Obs 103, the q_v-versus-q_uv finding).
The late-imperial under-production of these small western cities is largely a **provincial-tier**
phenomenon. A companion probe (Obs 104) finds the *same*: city size does not predict purely
city-specific dynamics (a null on q_v), but larger cities do tend to sit in less-declining provinces —
the size–buffering gradient is mostly province-mediated. (Whether *province size itself* drives this is
not supported and underpowered — Obs 105.)

**Scaling-over-time (H7).** Recomputing the population–inscription scaling exponent (β_within) within
eight 50-year periods, on the **all-provinces** frame (1,044 cities, baseline context; Obs 99): β traces
a shallow **U-shape** — **0.701** [0.596, 0.809] in 50 BC–AD 0, a **~0.58 plateau across the high empire
(AD 100–250)** — which is exactly the pooled value 0.587 — then back up to **0.659** in the 4th century.
Credible intervals overlap throughout, so this is a descriptive trend, not a sharp break. On the
**Latin-minus-Roma primary frame** the same U-shape replicates, shifted upward: **0.886** early → a
**~0.69–0.71 high-empire plateau** → **0.799** late (Obs 106, H7-Latin), confirming the U is a feature
of the diagnostic unit and **not a Greek-East mixing artefact**.

**Capitals (H3c).** Provincial capitals over-produce inscriptions **in every one of the eight periods,
on both frames** — P(capital contrast > 0) = 1.00 throughout (Obs 99, Obs 106). This replicates Hanson
2021's capital over-production and shows it is temporally stable, not a high-empire artefact. (The
original cross-sectional H3c: capitals SUPPORTED in all four cells, e.g. empire median contrast +0.96
[0.74, 1.21], Latin +1.08 [0.81, 1.41]; residual spatial *clustering* is NOT supported — the province
intercepts absorb it; Obs 74.) Residual spatial clustering, where present, is an **early-empire-only**
phenomenon (significant only in the earliest period; Obs 99/106).

---

## 3. What letter count (content) adds over inscription count (acts)

The project measures epigraphic output two ways: **acts** (number of inscriptions) and **content**
(total letter-mass, the summed Latin A–Z letters; Greek excluded). The question is whether the content
measure tells us anything the act measure doesn't.

- **Both measures corroborate the population–epigraphy relationship (H9).** Re-running the headline
  cross-sectional analysis with **letter-mass** as the response, on the **Latin primary frame** (817
  cities / 39 provinces): the within-province population effect **f_within = 0.448 [0.364, 0.535],
  SUPPORTED** (95% CI wholly above the preregistered 0.10 threshold), β_within = 0.681 [0.595, 0.769]
  (Obs 109, H9 REPORT). So acts *and* content independently support the same within-province
  population–epigraphy scaling.

- **The two over-production channels are statistically orthogonal (A01 content residual).** "Prolific for
  its size" (the scaling/act residual — a city producing more inscriptions than its population predicts)
  and "verbose per act" (the content residual — more letters per inscription than the corpus norm) turn
  out to be **independent city properties**: their correlation is essentially zero (Latin Spearman ρ =
  +0.004, p = 0.913; empire ρ = +0.006; Obs 108, A01 REPORT). This is the substantive payoff: content is
  **not** a rescaling of acts. If it were, the two residuals would be collinear; they aren't, so
  reporting both measures is not redundant — each indexes a different thing.

- **The "too-good-to-be-true" pseudo-R², revisited.** Regressing letter-mass directly on inscription
  count gives a slope ≈ 1 and an R² of **0.841** (Latin frame, n = 809; Obs 108). That high R² is **not
  evidence of a finding** — it is near-mechanical, because longer corpora simply have more letters.
  Stripped of that, the *informative* content signal is small: the per-city departure from constant
  letters-per-act (content-residual SD ≈ 0.73 log units), and the content-measure OLS log-log slope
  against *population* is only 0.470 (R² 0.075; Obs 109). In short: **letter count adds a distinct
  content axis — how verbose a city is per inscription — that is orthogonal to its size-scaling, but it
  does not give the population signal extra explanatory power.** It is a complement, not an upgrade.

(Letter-mass *temporal* detection remains out of reach — the letter-mass detection grid fails recovery
and is corpus-wide unreachable, so all letter-mass *confirmatory* claims are bounded to the
cross-section; Obs 109.)

---

## 4. The Hanson population ↔ inscription-count relationship

This is the hinge between empirical pattern and interpretation. We follow the project's framing rule
strictly: we describe an **association with Hanson's population estimates**, not "population scaling" with
causal force.

- **The headline within-province scaling (H3a).** On the **Latin primary frame** (817 cities), the
  within-province population effect is **f_within = 0.480 [0.401, 0.566]** (unweighted, primary;
  SUPPORTED) with **β_within = 0.587** on the empire frame and **0.733** on the Latin frame
  (`runs/2026-06-04-h3a-confirmatory/outputs/REPORT.md`; Obs 75). The empire frame is
  secondary/context: f_within = 0.299 [0.240, 0.365] (1,044 cities). The Latin restriction *strengthens*
  the signal — exactly the corroboration of the LIRE coverage argument (LIRE under-covers Greek-speaking
  provinces). β_within = 0.587 [0.519, 0.657] is the paper's reference cumulative value.

- **What "sub-linear" means substantively.** β_within < 1 means inscription output grows **less than
  proportionally** with city population: a city ten times larger does not produce ten times the
  inscriptions, but fewer. Larger cities are, per head, *less* epigraphically prolific than smaller ones
  — a sub-linear, diminishing-returns relationship rather than a one-to-one one.

- **Capitals over-produce on top of that.** Provincial capitals produce more than their size predicts,
  in every period and on both frames (Obs 74, 99, 106) — Hanson 2021 replicated.

- **The association is robust to whether or not we apply the convention correction.** This is a key
  reassurance. Correcting for editorial dating convention does **not** move the scaling result, shown at
  two levels:
  - *Province-level proxy* (Obs 94, deconv-leverage): the genuine-fraction α is essentially uncorrelated
    with population (Spearman −0.11) or corpus size (Spearman −0.22) across the 26 non-aggregate units,
    and robust estimators of the implied change in the scaling exponent sit at ≈ 0 (Theil-Sen Δβ −0.030;
    the naïve OLS +0.292 is a single-unit Pompeii leverage artefact, caught on a robustness check).
  - *City-level confirmation* (Obs 107, D13): adding a per-city genuine-fraction α as a covariate to the
    scaling regression (163 Latin cities, N ≥ 100) shifts β_within only −0.0086 (0.142 posterior SD;
    +0.431 → +0.422), and propagating the (large) per-city α uncertainty via multiple imputation leaves
    it untouched (fraction of missing information 0.47%). City-level and province-level agree tightly
    (Spearman ≈ −0.11 at both). The editorial-convention confound the test was designed to detect is
    **absent**.

- **Peak-scaling.** Peak inscription intensity scales with population by essentially the same law as
  cumulative output — raw-peak β 0.557 [0.490, 0.624] vs cumulative 0.587 on the all-provinces frame
  (Obs 100), and 0.700 [0.618, 0.784] vs cumulative 0.733 on the Latin frame (Obs 106); the credible
  intervals overlap heavily. Bigger cities have proportionally higher peaks *and* higher totals by the
  same exponent.

---

## 5. Headline takeaways

1. **About two-thirds of empire-wide dated inscriptions carry a genuine date signal** (pooled
   genuine-fraction α = 0.6798 [0.6649, 0.6970]); the rest is editorial round-slab convention that the
   deconvolution separates out. The model is recovery-validated (Obs 89, 110, 111).

2. **The population–epigraphy association is real, sub-linear, and robust.** Within provinces, inscription
   output rises with city size but less than proportionally (β_within = 0.587 empire / 0.733 Latin;
   f_within SUPPORTED on the Latin primary frame). It holds whether or not we correct for dating
   convention — confirmed at both province and city level (Obs 94, 107) — and on both the act and the
   content measure (Obs 109).

3. **Provincial capitals over-produce, everywhere and always** — in all eight time-periods and on both
   frames (Obs 74, 99, 106). Hanson 2021's capital effect is replicated and shown to be temporally
   stable.

4. **The biggest single driver of temporal variation is empire-wide and shared** (~54% of a typical
   city's temporal variance; peaks ≈ AD 188), but we deliberately do **not** label it the "epigraphic
   habit" — it conflates four things (Obs 97, 98; see §6).

5. **The apparent post-AD-250 collapse is mostly an artefact of that shared component.** Removed, it
   becomes a moderate, heterogeneous, **provincial-tier** relative decline (median city ≈ ⅓ of its
   empire-relative baseline in the 3rd century), not demonstrated depopulation (Obs 96, 103).

6. **Acts and content are complementary, not redundant.** "Prolific for its size" and "verbose per act"
   are statistically orthogonal city properties (Obs 108); the content measure adds a distinct axis but
   no extra population-signal power.

---

## 6. What we can and cannot claim — honest caveats

- **The empire-wide common temporal component is NOT a clean "epigraphic habit."** It conflates four
  drivers we cannot separate within this model: (a) cultural epigraphic habit, (b) empire-wide
  demographic/economic trends, (c) empire-wide taphonomy and recovery bias, and (d) residual dating-
  convention structure (Obs 98). The AD-188 peak matches both MacMullen's habit curve *and* the Antonine
  demographic apogee — and the two cannot be disentangled here. No external habit proxy exists to
  partial it out. **In the results section we say "empire-wide common temporal component"; the
  four-driver interpretation belongs in discussion** (the Obs 101 framing rule).

- **The population link is an association, and everything is model-conditional.** We describe an
  association with Hanson's population estimates, not population "driving" or "scaling" epigraphy. All
  results hold *given* the aoristic mixture plus hierarchical partial-pooling model (Obs 101).

- **The cross-sectional scaling result is protected by the date-window filter, not by the mixture.** H3a
  uses the full envelope (50 BC – AD 350), which conserves each unit's total count; the deconvolution
  reshapes *when* mass sits, not the full-window total. So the headline scaling does not depend on the
  mixture being right — and separately, the convention correction was shown not to move it (Decision 22;
  Obs 94, 107).

- **Small-N reachability limits the fine-grained work.** Per-city genuine-fraction α is unreliable below
  ~N = 500 (only ~16% reliable at N = 100; Obs 107), and only 34 of the 268 §5 mid-sized cities meet the
  N ≥ 300 reliability floor (Obs 96). The §5 size-and-dynamics findings (Obs 104, 105) are **suggestive,
  not established** (the size–dynamics probe runs on the 34 reliable cities; the separate
  province-size regression on ~20–35 provinces; both underpowered). The honesty layer (multiple
  imputation) shows this uncertainty does not contaminate the headline scaling, but it does cap what the
  city-level trajectory work can assert.

- **"Sub-linear" and "relative" are load-bearing words.** β_within < 1 is diminishing returns, not
  decline; the q-trajectory dips are *relative to the empire trend*, not absolute population, and still
  carry city/province-level taphonomy, economy, and habit — "buffered" does not mean "demographically
  buffered" (Obs 98, 103, 104).

- **The §5 mid-sized set is range-restricted.** It excludes the largest and smallest cities, so any
  within-subset scaling (e.g. the 0.22 peak-scaling figure) is a range artefact, not a real flattening
  (Obs 100); the population-range-valid answer is the full-frame one. The large anchor cities (Ostia,
  Pompeii, etc.) are **held out by design** as out-of-sample validation, not refitted in (Obs 102).

- **A handful of known, reported limitations**, none amended: the empire-aggregate deconvolution fit
  under-converges (R̂ = 1.0126; Obs 111); the point-date aoristic Monte-Carlo "collapses" on the real
  empire — a method artefact driven by classify-then-analyse plug-in bias, with the mass-preserving arm
  the sound read (Obs 110); the Layer-B population inversion is **illustrative comparative-shape only**,
  not a population estimate (Obs 96).

---

*All figures re-read at source on 2026-06-20 against the working-notes Observation register and the run
REPORTs. The documentation set was accuracy-certified on 2026-06-20
(`planning/doc-accuracy-audit-2026-06-20.md`); corrected values are used throughout this draft.*
