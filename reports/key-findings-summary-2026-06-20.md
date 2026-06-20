# Inscriptions / LIRE deconvolution paper — key-findings summary (DRAFT v2)

**Date:** 2026-06-20 **Status:** DRAFT for Shawn's review before circulation to co-authors.
**Audience:** archaeologists and ancient historians — no statistical background assumed. Every
statistical term is explained in plain language the first time it appears, and every number is tagged
with the Observation ("Obs N") or run REPORT it came from.

> **A note on traceability and on two things that look alike but aren't.** Every figure below is tagged
> with the Observation ("Obs N") in `docs/notes/working-notes.md` or the run REPORT it came from, all
> re-read at source for this draft. Two recurring traps for the reader, flagged here once:
>
> 1. **There are two different quantities both written "α" (alpha).** The **genuine-fraction α** is the
>    share of a place's dated inscriptions that carry a *real* date signal rather than an editorial
>    round-number dating convention — this is the main output of our de-fogging method. The **dispersion
>    α** is a completely unrelated nuisance knob inside the count regression (it just tells the model how
>    "lumpy" the counts are). Where confusion is possible I write "genuine-fraction α" or "mixture α".
>    They are not the same number and never interact.
> 2. **Which set of provinces a number describes matters.** The project's lodged **primary** analytical
>    unit is the **Latin-speaking provinces with the city of Rome excluded** ("Latin-minus-Roma";
>    Amendment 02 / Decision 36). The **empire-wide / all-provinces** frame is reported as *context* only.
>    Numbers from the two frames are never merged. Within a frame, results can also be *unweighted* (the
>    primary), *population-weighted*, or *inscription-weighted*; and they can be measured in *inscription
>    counts* ("acts") or in *letter-mass* ("content"). Each figure below names its frame, weighting, and
>    measure.

---

## 1. The method, in one paragraph (plus: why we bother)

The corpus is LIRE v3.0 (Latin Inscriptions of the Roman Empire): **182,853 inscriptions × 63 data
columns** (`runs/2026-04-23-descriptive-stats/outputs/summary.md`, corrected count). Many inscriptions
are not dated to a true historical moment but assigned a *round-number date slab* by editorial
convention — a tidy "AD 1–100" or a half-century box — which dumps artificial lumps of probability mass
on round years and century boundaries. To stop those cataloguing habits being mistaken for real history,
we built a **Bayesian deconvolution-mixture model**. Two plain-language glosses for the Bayesian
machinery, used throughout: a **posterior** is simply the model's probability distribution for a
quantity *after* it has seen the data (its full considered opinion, not a single guess); a **95% credible
interval** is the Bayesian "we are 95% sure the true value lies in this range". For each unit the model
estimates a **genuine fraction α** — the proportion of that unit's dated inscriptions whose dating is a
real signal rather than a round-slab convention — and it separates the genuine dating signal from the
convention artefact. (Mechanically it does this by detecting **θ (theta)**, the rate at which a unit's
dates "snap to" round-number calendar slabs; high snapping means low genuine fraction.) The production
model is the **cross-classified ("library") likelihood**, adopted after an earlier design was shown to
add a spurious upward bias; the adopted version is recovery-validated. In a full simulation where the
right answer was planted and known — 300 parameter cells × 100 repeats — it passed all four pre-set
adoption criteria cleanly: it recovered the planted genuine fraction with essentially no bias (mean
absolute error ≈ 0.021, i.e. on average it lands within ~2 percentage points of the truth) without
harming the cases it should leave alone (Obs 89, `cc-VERDICT-library.md`). A separate validity test (C10)
plants a known α in synthetic data and confirms the recovery works in the controlled setting (Obs 110).
On the **whole empire pooled together**, the estimated genuine fraction is **α = 0.6798, 95% credible
interval [0.6649, 0.6970]** — i.e. roughly **two-thirds** of empire-wide dated inscriptions carry a
genuine date signal and about one-third are round-slab convention (Obs 111, supp-wave REPORT;
Latin-speaking provinces pooled: α = 0.7387 [0.6596, 0.7893]). All results below are
**model-conditional**: they hold *given* this aoristic mixture plus hierarchical (partial-pooling) model.

**Why go to all this trouble?** The point is not the empire number itself but the *instrument*. De-fogging
converts a date distribution that is contaminated by editorial convention into a defensible **genuine
temporal signal**, which lets a researcher do chronological analysis on a *subset* — a province, a region,
a thematic class of inscriptions — "beyond eyeballing histograms", with honest uncertainty bands instead
of a shape that is half cataloguing artefact. Crucially it comes with a **reachability map** (its "spec
sheet"): a validated rule for *when* it works — recovers the genuine trajectory from roughly N ≈ 500
inscriptions for the easiest subsets, rising to a worst-case floor of N ≈ 2,000 inside the operating
envelope (genuine fraction α ≤ ~0.70), and is unreliable above that. The motivating re-application is a
collaborator's corpus of mother–daughter / marriage-age inscriptions, which wants a temporal dimension on
"when did this commemorative practice rise and fall?" — exactly what subset-specific de-fogging supplies,
and which sits right at the measured worst-case floor (`paper-significance-and-applications-2026-06-03.md`;
Decision 34: subsets get their own fit and are *not* de-fogged with the empire-wide convention shape).

**Key results**

- The corpus is LIRE v3.0: 182,853 inscriptions × 63 columns (`summary.md`, corrected).
- About **two-thirds** of empire-wide dated inscriptions carry a genuine date signal; one-third is
  editorial round-slab convention (pooled α = 0.6798 [0.6649, 0.6970]; Obs 111).
- The de-fogging model is **recovery-validated** — it recovers a planted genuine fraction with
  near-zero bias (~2 percentage points) and does no harm to cases it should leave alone (Obs 89, 110).
- The deliverable is a **reusable instrument with a known reachability envelope** (works from N ≈ 500 for
  easy subsets, worst-case floor N ≈ 2,000, requires α ≤ ~0.70), for putting a temporal dimension on
  subset epigraphy (Decision 34; significance doc).

---

## 2. Temporal variation across scales — empire, province, city

A second, nested model (the "§5 Layer-A" decomposition) splits each city's inscription-rate-over-time
into shared and idiosyncratic parts, on **mid-sized cities** (268 small-N target cities; large
data-rich anchor cities deliberately held out — see §6). It separates: an **empire-wide common temporal
component** (the time-shape every city shares), a **province component** (the extra time-shape cities in
the same province share), and a **city-specific component** (each city's own departure), plus a
between-city *level* spread — the cross-sectional, population-related axis of "how much each city produces
overall, regardless of when".

**How we measure size, and what the numbers mean.** Each component's size is reported as a **standard
deviation (SD) on the log inscription-rate scale** — and that scale is the key to reading the table.
Working in logs means a one-SD swing does not *add* a fixed number of inscriptions; it *multiplies or
divides* the rate by a constant factor, namely e^SD. So an SD of **1.0** means a typical one-standard-
deviation swing multiplies (or divides) a city's inscription rate by about e¹ ≈ **2.7×**; an SD of
**0.78** corresponds to a factor of about e^0.78 ≈ **2.2×**. These are *spreads*, not single events: they
say how widely the rate ranges around its average once you move one notch along that axis. The four
numbers (Obs 97, H5 `h5-decomposition.json`):

| Component | log-rate SD | typical one-SD swing multiplies the rate by ≈ |
|---|---|---|
| Empire-wide common temporal component | **1.11** | 3.0× |
| Province temporal component | **1.02** | 2.8× |
| City-specific temporal component | **0.98** | 2.7× |
| Between-city *level* spread (cross-sectional / population axis) | **0.78** | 2.2× |

[FIGURE: variance partition — stacked-bar of the four component sizes; cf.
`runs/2026-05-26-letter-count-probe/outputs/figures/fig-05-variance-partition-bars.png`. A clean stacked
bar conveys the relative shares far better than the table.]

**So the typical province and the typical city…** The three *temporal* components are very nearly the
same size (1.11, 1.02, 0.98) — say so plainly: when it comes to *how inscription output changes over
time*, the empire-wide trend, the province's own trend, and the city's own quirks each contribute roughly
comparable amounts of swing. The empire-wide component is the single largest, but only modestly so: it
accounts for about **54% of a typical city's temporal variance** (`h5-decomposition.json`
`median_common_share_of_temporal_var` 0.540; Obs 97). In words: a little over half of how a typical
city's inscribing rises and falls over time is the empire-wide tide that lifts and drops everyone
together; the remaining ~46% is split, in roughly equal measure, between its province's shared deviation
(**≈24%**) and its own city-intrinsic idiosyncrasy (**≈22%**). So the three-way reading of a typical
city's temporal variation is **≈54% empire-wide common · ≈24% province-contributed · ≈22% city-intrinsic**
— no single layer dominates timing, but the empire-wide tide is first among near-equals. (The 54% is the
sourced per-city common share; the province/city sub-split is apportioned by the near-equal component
variances, SD 1.02 vs 0.98, so treat ≈24 / ≈22 as indicative — the exact per-city three-way decomposition
will be pinned from the §5 idata when it is regenerated for the figures.) (The fourth row,
the level/population axis at 0.78, is a *different axis entirely* — it is about overall output, not timing
— and is read in §4.)

**Important caveat to state plainly:** the level/population axis (0.78) is *understated here* because this
mid-sized set excludes the size extremes, so this is **not** "timing beats population" in the full corpus
— temporal variation and the population axis simply live on different axes and are not in competition. On
the **Latin-minus-Roma diagnostic unit** (257 of the 268 cities) the decomposition is essentially
identical to all-provinces (level SD 0.785 vs 0.777; common-share 0.540 vs 0.540), because the set is
~96% Latin-West (Obs 97).

**When does the empire-wide common component peak?** **AD 187.5** — late-Antonine / Severan (Obs 97,
`h5-summary.json: empire_habit_peak_year`). This coincides with both MacMullen's epigraphic-habit curve
and the Antonine demographic apogee. **We deliberately do not call this "the epigraphic habit"** — see
the caveat in §6.

**The apparent post-AD-250 "collapse" — what it really is.** Inverting each city's *raw* trajectory into
a population-shape (Layer B) makes the median city look as though it falls to ~0% of peak by AD 250. That
is **not** demonstrated depopulation: it is mostly the empire-wide common component falling away,
amplified by the inversion (because the inversion raises everything to the power 1/β > 1, every dip is
magnified; Obs 96). Once the empire-wide common component is *removed*, the dramatic universal collapse
dissolves into **moderate, heterogeneous, provincial-tier relative decline** (Obs 103, Layer B residual).
Reading the median city's level relative to the empire baseline (q = 1 means "exactly on the empire
trend"; q = 0.5 means "at half the empire trend"; empire-β frame, reliable cities):

| Era (bin centre) | median q vs empire | share of cities below the empire trend |
|---|---|---|
| early-Antonine (AD 112) | 0.48 | 0.65 |
| empire-common peak (AD 188) | 1.01 | 0.50 |
| 3rd century (AD 262) | 0.32 | 0.68 |
| late (AD 338) | 0.67 | 0.53 |

So the typical mid-sized western city sits at about **one-third of its empire-relative baseline by the
3rd century** — a factor-of-~3 *relative* dip, not collapse — and about a third of reliable cities are
still at or above the empire trend even then (Obs 103). When the *province* layer is also stripped out,
the purely city-specific 3rd-century position is a mild ≈ 0.78: most of a small city's apparent
divergence is **its province's shared deviation, not its own** (Obs 103, the q_v-versus-q_uv finding). The
late-imperial under-production of these small western cities is largely a **provincial-tier** phenomenon.
A companion probe (Obs 104) finds the *same*: city size does not predict purely city-specific dynamics (a
null result on the city-specific axis), but larger cities do tend to sit in less-declining provinces — the
size–buffering gradient is mostly province-mediated. (Whether *province size itself* drives this is not
supported and is underpowered — Obs 105.)

**Scaling-over-time (H7).** "Scaling" here means the **β (beta) scaling exponent** — how steeply
inscription output rises with population on a log-log plot. (β = 1 would be exactly proportional; β < 1
means less than proportional — a city ten times larger produces fewer than ten times the inscriptions.)
Recomputing β *within provinces* (β_within) across eight 50-year periods, on the all-provinces frame
(1,044 cities, baseline context; Obs 99): β traces a shallow **U-shape** — **0.701** [0.596, 0.809] in
50 BC–AD 0, a **~0.58 plateau across the high empire (AD 100–250)** (exactly the pooled value 0.587),
then back up to **0.659** in the 4th century. The credible intervals overlap throughout, so this is a
descriptive trend, not a sharp break. On the Latin-minus-Roma primary frame the same U-shape replicates,
shifted upward: **0.886** early → a **~0.69–0.71 high-empire plateau** → **0.799** late (Obs 106,
H7-Latin), confirming the U is a feature of the diagnostic unit and **not** a Greek-East mixing artefact.

**Capitals (H3c).** Provincial capitals over-produce inscriptions **in every one of the eight periods,
on both frames** — the posterior probability that the capital effect is positive is 1.00 throughout
(Obs 99, Obs 106). This replicates Hanson 2021's capital over-production and shows it is temporally
stable, not a high-empire artefact. (The original cross-sectional H3c: capitals supported in all four
cells, e.g. empire median contrast +0.96 [0.74, 1.21], Latin +1.08 [0.81, 1.41]; residual spatial
*clustering* is NOT supported — the province intercepts absorb it; Obs 74.) Residual spatial clustering,
where present, is an **early-empire-only** phenomenon (significant only in the earliest period; Obs
99/106).

**Key results**

- The three *temporal* drivers are near-equal in size — empire-wide common (SD **1.11**), province (SD
  **1.02**), city-specific (SD **0.98**) — each a roughly 2.7–3.0× multiplicative swing in rate (Obs 97).
- The empire-wide common component is the single largest, at **~54% of a typical city's temporal
  variance**, and peaks at **AD 187.5** (Obs 97).
- The "post-AD-250 collapse" is mostly the empire-wide component falling away; once removed it is a
  **moderate, provincial-tier relative decline** (median city ≈ ⅓ of its empire baseline in the 3rd
  century), not depopulation (Obs 96, 103).
- The population–output scaling exponent traces a shallow, overlapping **U-shape** over time (≈0.58
  plateau in the high empire), the same on both frames — a trend, not a break (Obs 99, 106).
- Provincial **capitals over-produce in every period on both frames** (Hanson 2021 replicated and shown
  temporally stable; Obs 74, 99, 106).

---

## 3. What letter count (content) adds over inscription count (acts)

The project measures epigraphic output two different ways, and it is worth being concrete about what each
one *is*:

- **Acts** = the **number of inscriptions** a city produced (how often people inscribed at all).
- **Content** = the **total letter-mass**, i.e. the summed count of Latin A–Z letters across all of a
  city's inscriptions (Greek excluded). This indexes *how much text* was inscribed, not just how many
  times.

The question §3 answers is whether the content measure tells us anything the act measure does not — is it
a genuinely new lens, or just a re-labelling of "acts"?

- **Both measures corroborate the population–epigraphy relationship (H9).** Re-running the headline
  cross-sectional analysis with **letter-mass** as the outcome, on the Latin primary frame (817 cities /
  39 provinces): the within-province population effect is **SUPPORTED** — its share-of-variation measure
  **f_within = 0.448, 95% CI [0.364, 0.535]** (the whole interval sits above the pre-registered 0.10
  threshold), with scaling exponent β_within = 0.681 [0.595, 0.769] (Obs 109, H9 REPORT). So acts *and*
  content independently point to the same within-province population–epigraphy scaling.

- **The two over-production channels are independent (orthogonal) traits (A01 content residual).** A city
  can stand out in two unrelated ways. "**Prolific for its size**" means it produces *more inscriptions*
  than its population would predict (the scaling/act residual). "**Verbose per act**" means its
  inscriptions run *longer than the corpus norm* — more letters per inscription (the content residual).
  The key finding is that these two traits are **uncorrelated**: knowing a city is prolific tells you
  nothing about whether it is verbose, and vice versa. Statistically their correlation is essentially zero
  (Latin Spearman ρ = +0.004, p = 0.913; empire ρ = +0.006; Obs 108, A01 REPORT) — and ρ ≈ 0 simply means
  "no linear relationship between the two". This is the substantive payoff: content is **not** a rescaling
  of acts. If verbosity were just a stand-in for prolificness, the two residuals would move together; they
  do not, so reporting both measures is not redundant — each indexes a genuinely different urban trait.

- **And *which* cities are verbose? Not the obvious ones.** A quick descriptive check (2026-06-20) of the
  per-city content residual against city type finds that high verbosity (more letters per inscription than
  the corpus norm) is **not** a marker of status or scale: it is **no higher in provincial capitals** than
  elsewhere (capitals are if anything marginally *lower*; Mann–Whitney p = 0.59, n = 41 capitals), is
  essentially **uncorrelated with city population** (Spearman −0.02), and is uncorrelated with output
  volume (vs act-count ρ ≈ 0.00). The most letter-rich-per-inscription cities are smaller provincial towns
  (e.g. Aregenua, Cillium, Veleia, Malaca), not the great centres. Verbosity is, in short, **idiosyncratic**
  — which *reinforces* the orthogonality result above: per-inscription wordiness is genuinely its own axis,
  not a stand-in for a city's importance, size, or prolificness. (Descriptive/exploratory; computed from
  `runs/2026-06-20-a01-content-residual/outputs/content-residual-per-city.csv` ×
  `data/processed/provincial-capitals.csv`.)

- **The "too-good-to-be-true" R², explained and set aside.** R² (R-squared) is the **fraction of
  variation in one quantity explained by another**, from 0 (explains nothing) to 1 (explains everything).
  If you regress a city's total letter-mass directly on its inscription *count*, you get a slope of about
  1 and an **R² of 0.841** (Latin frame, n = 809; Obs 108). That looks spectacular, but it is **not a
  finding** — it is near-mechanical, because a corpus with more inscriptions trivially has more letters in
  it (more acts ⇒ more letters, almost by definition). Strip out that mechanical part and the genuinely
  *informative* content signal is small: the city-by-city departure from a constant letters-per-act ratio
  has an SD of only ≈ 0.73 log units, and when you regress the content measure against *population* the
  log-log slope is just 0.470 with R² 0.075 (Obs 109) — population explains only ~7.5% of the variation in
  letter-mass beyond what acts already capture.

- **Bottom line for §3:** letter count adds a distinct **"verbosity" axis** — how wordy a city is per
  inscription — that is independent of its size-scaling, but it does **not** give the population signal any
  extra explanatory power. Content is a **complement, not an upgrade**: a second, orthogonal trait worth
  reporting, not a stronger version of the acts result.

(One scope limit: letter-mass *temporal* detection is out of reach — the letter-mass detection grid fails
recovery and is corpus-wide unreachable, so all letter-mass *confirmatory* claims are bounded to the
cross-section; Obs 109.)

**Key results**

- "Acts" = number of inscriptions; "content" = total Latin letter-mass — two different output measures.
- Letter-mass **independently supports** the within-province population effect (f_within 0.448
  [0.364, 0.535], SUPPORTED; Obs 109).
- "Prolific for its size" and "verbose per act" are **statistically orthogonal** city traits (ρ ≈ 0;
  Obs 108) — content is not a rescaling of acts.
- **Verbosity is idiosyncratic** — *not* associated with capital status (Mann–Whitney p = 0.59), city
  size (ρ −0.02), or output (ρ ≈ 0); the most verbose cities are smaller provincial towns, not capitals
  (descriptive check, 2026-06-20) — reinforcing that content is genuinely its own axis.
- The eye-catching R² = 0.841 of letters-on-inscription-count is **near-mechanical, not a finding**
  (more inscriptions trivially means more letters; Obs 108).
- Content adds a distinct **verbosity axis** but **no extra population-signal power** — a complement, not
  an upgrade (Obs 109).

---

## 4. The Hanson population ↔ inscription-count relationship

This is the hinge between empirical pattern and interpretation. We follow the project's framing rule
strictly: we describe an **association with Hanson's population estimates**, not "population scaling" with
causal force.

- **The headline within-province scaling (H3a) — in plain terms first.** "**Within-province**" means we
  compare cities *against the other cities in their own province*, asking: among cities that share a
  province, do the bigger ones inscribe more? "**Between-province**" is the separate question of whether
  *whole provinces* with larger total populations inscribe more in aggregate. The two are genuinely
  different, and we report them separately. Two quantities carry the within-province answer: **β_within**
  (the scaling exponent — how steeply output rises with population on a log-log scale) and **f_within**
  (the **fraction of the between-city variation in output, within a province, that is attributable to
  those cities' population differences** — the rest being city-specific). On the **Latin primary frame**
  (817 cities), f_within = **0.480 [0.401, 0.566]** (unweighted, primary; SUPPORTED) with **β_within =
  0.733** on the Latin frame and **0.587** on the empire frame
  (`runs/2026-06-04-h3a-confirmatory/outputs/REPORT.md`; Obs 75). The empire frame is secondary/context:
  f_within = 0.299 [0.240, 0.365] (1,044 cities). The Latin restriction *strengthens* the signal — exactly
  the corroboration of the LIRE coverage argument (LIRE under-covers Greek-speaking provinces).
  β_within = 0.587 [0.519, 0.657] is the paper's reference cumulative value.

- **What "sub-linear" means substantively.** β_within < 1 means inscription output grows **less than
  proportionally** with city population: a city ten times larger does not produce ten times the
  inscriptions, but fewer. Larger cities are, per head, *less* epigraphically prolific than smaller ones
  — a sub-linear, diminishing-returns relationship rather than a one-to-one one.

- **Capitals over-produce on top of that.** Provincial capitals produce more than their size predicts,
  in every period and on both frames (Obs 74, 99, 106) — Hanson 2021 replicated.

- **The association is robust to whether or not we apply the convention correction — and why that
  matters.** A sceptic might worry that the population signal is an accident of the editorial-dating habit:
  perhaps big cities just happen to attract more round-slab dating, and *that* — not population — is what
  the scaling picks up. We tested exactly that worry by adding each unit's **genuine-fraction α** (its
  de-fogging score) into the scaling regression as an extra explanatory variable. The logic is simple: if
  the dating habit were secretly manufacturing the population signal, then accounting for the habit (via
  per-unit α) should make the scaling exponent move. **It doesn't budge** — which means the editorial
  habit is *not* the hidden source of the population association. We confirmed this at two levels:
  - *Province-level proxy* (Obs 94, deconv-leverage): the genuine-fraction α is essentially uncorrelated
    with population (Spearman −0.11) or corpus size (Spearman −0.22) across the 26 non-aggregate units,
    and robust estimators of the implied change in the scaling exponent sit at ≈ 0 (Theil-Sen Δβ −0.030;
    a naïve estimate of +0.292 turned out to be a single-city Pompeii artefact, caught on a robustness
    check).
  - *City-level confirmation* (Obs 107, D13): adding a per-city genuine-fraction α to the scaling
    regression (163 Latin cities, N ≥ 100) shifts β_within by only −0.0086 (0.142 posterior SD), and
    propagating the (large) per-city α uncertainty leaves it untouched. City-level and province-level
    agree tightly. The editorial-convention confound the test was designed to detect is **absent**.

- **BOTTOM LINE on population.** Of the between-city variation in inscription output *within a province*,
  about **48%** is attributable to those cities' population differences (Latin primary frame; f_within
  0.480 [0.401, 0.566]) — the remaining ~52% is city-specific. (On the empire context frame the figure is
  lower, ~30%; f_within 0.299.) By contrast, the *between*-province effect — whether whole provinces with
  larger populations inscribe more in aggregate — is **weak and uncertain**: on the empire frame
  β_between ≈ **−0.24** with a 95% interval of [−0.701, 0.238] that straddles zero, i.e. not reliably
  distinguishable from no effect at all (it is not independently identifiable per prereg §9; h3a
  REPORT:91–92). State it plainly: **the population–epigraphy association is primarily a within-province,
  city-level phenomenon, not a province-aggregate one.** It is about how cities rank against their
  neighbours, not about how provinces rank against each other.

- **Peak-scaling.** Peak inscription intensity scales with population by essentially the same law as
  cumulative output — raw-peak β 0.557 [0.490, 0.624] vs cumulative 0.587 on the all-provinces frame
  (Obs 100), and 0.700 [0.618, 0.784] vs cumulative 0.733 on the Latin frame (Obs 106); the credible
  intervals overlap heavily. Bigger cities have proportionally higher peaks *and* higher totals by the
  same exponent.

[FIGURE: within- vs between-province scaling — a two-panel log-log scatter (cities coloured by province),
showing the steep within-province slope against the flat/uncertain between-province one.]

**Key results**

- The within-province population effect is **SUPPORTED**: about **48%** of between-city output variation
  within a province tracks population (Latin f_within 0.480 [0.401, 0.566]; ~30% empire context; Obs 75).
- The relationship is **sub-linear** (β_within 0.733 Latin / 0.587 empire) — bigger cities are *less*
  prolific per head, not more.
- It is **primarily a within-province, city-level** phenomenon; the between-province effect is weak and
  uncertain (empire β_between ≈ −0.24, interval crosses zero; h3a REPORT).
- The association is **robust to the convention correction** at both province and city level — the
  editorial-dating habit is *not* secretly creating the population signal (Obs 94, 107).
- **Capitals over-produce**, and **peak** intensity scales by essentially the **same exponent** as
  cumulative output (Obs 74, 100, 106) — Hanson 2021 replicated on both counts.

---

## 5. Headline takeaways

1. **About two-thirds of empire-wide dated inscriptions carry a genuine date signal** (pooled
   genuine-fraction α = 0.6798 [0.6649, 0.6970]); the rest is editorial round-slab convention that the
   de-fogging method separates out. The model is recovery-validated (Obs 89, 110, 111).

2. **The population–epigraphy association is real, sub-linear, within-province, and robust.** Among cities
   in the same province, inscription output rises with size but less than proportionally — about **48%** of
   between-city variation tracks population (Latin f_within 0.480; β_within 0.733 Latin / 0.587 empire,
   SUPPORTED). The between-*province* effect is weak and uncertain (empire β_between ≈ −0.24, crosses
   zero). The within-province signal holds whether or not we correct for dating convention — confirmed at
   both province and city level (Obs 94, 107) — and on both the act and the content measure (Obs 109).

3. **Provincial capitals over-produce, everywhere and always** — in all eight time-periods and on both
   frames (Obs 74, 99, 106). Hanson 2021's capital effect is replicated and shown to be temporally stable.

4. **Three temporal drivers, near-equal in size, with the empire-wide one first among near-equals.** How a
   city's inscribing rises and falls over time is driven roughly equally by an empire-wide common
   component (log-rate SD **1.11**), its province's shared component (SD **1.02**), and its own
   city-specific component (SD **0.98**) — each a ~2.7–3.0× multiplicative swing. The empire-wide
   component is the single largest (**~54%** of a typical city's temporal variance) and peaks ≈ AD 188,
   but only modestly ahead of the province and city layers. We deliberately do **not** label the
   empire-wide component the "epigraphic habit" — it conflates four things (Obs 97, 98; see §6).

5. **The apparent post-AD-250 collapse is mostly an artefact of that shared component.** Removed, it
   becomes a moderate, heterogeneous, **provincial-tier** relative decline (median city ≈ ⅓ of its
   empire-relative baseline in the 3rd century), not demonstrated depopulation (Obs 96, 103).

6. **Acts and content are complementary, not redundant.** "Prolific for its size" and "verbose per act"
   are statistically orthogonal city traits (Obs 108); the content measure adds a distinct verbosity axis
   but no extra population-signal power.

7. **The deliverable is a reusable, honestly-bounded instrument.** De-fogging turns a
   convention-contaminated date distribution into a defensible genuine temporal signal for *any* coherent
   subset, with a published reachability envelope (works from N ≈ 500 for easy subsets to a worst-case
   floor of N ≈ 2,000, requires α ≤ ~0.70) — a tool other researchers can apply to their own subcorpora
   (Decision 34; significance doc).

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
  reshapes *when* the mass sits, not the full-window total. So the headline scaling does not depend on the
  mixture being right — and separately, the convention correction was shown not to move it (Decision 22;
  Obs 94, 107).

- **Small-N reachability limits the fine-grained work.** Per-city genuine-fraction α is unreliable below
  ~N = 500 (only ~16% reliable at N = 100; Obs 107), and only 34 of the 268 §5 mid-sized cities meet the
  N ≥ 300 reliability floor (Obs 96). The §5 size-and-dynamics findings (Obs 104, 105) are **suggestive,
  not established** (the size–dynamics probe runs on the 34 reliable cities; the separate province-size
  regression on ~20–35 provinces; both underpowered). The honesty layer (multiple imputation) shows this
  uncertainty does not contaminate the headline scaling, but it does cap what the city-level trajectory
  work can assert.

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
