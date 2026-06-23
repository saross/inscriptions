# Significance and applications — the "why" of the mixture-deconvolution method

**Date:** 2026-06-03
**Status:** paper-facing framing material (intro / significance / discussion).
Captured at Shawn's request to anchor the contribution's motivation.
**Venue framing:** JAMT (Journal of Archaeological Method and Theory) — a
**primarily methodological** contribution. The arguments below answer the
question a methods-paper reviewer will ask: *"why go to all this trouble?"*

**Related records:** Decision 33 (criterion), Decision 34 (subset-specific
deconvolution), `recovery-grid-utility-review-2026-06-02.md` (reliability),
`prior-art-scout-2026-06-02-recovery-validation-metrics.md` (methods),
`runs/2026-06-03-small-n-reachability/spec.md` (the reachability study).

---

## 1. The core re-application case (the spine of the "why")

The payoff is **giving subset analyses a temporal dimension that is currently
done by eyeballing histograms.** Most Roman-epigraphy research operates on
*subsets* — provinces, cities, regions, and inscription subcategories — and most
of those subsets are dated with the same editorial-convention fog (century slabs,
regnal windows) that distorts the whole corpus. A researcher who wants to ask
*"how did this practice rise and fall over time?"* of a subcategory currently has
little better than a raw aoristic histogram, whose shape is partly an artefact of
how the inscriptions were catalogued.

The motivating example: a collaborator is studying **~2,000 mother–daughter
inscriptions** to estimate age at marriage / first childbirth, and wants a
**temporal element beyond eyeballing histograms** — when did this commemorative
practice wax and wane, with honest uncertainty, corrected for dating convention.
That is exactly what subset-specific deconvolution provides: a de-fogged temporal
trajectory with credible bands, for a coherent subcorpus, where before there was
a suggestive but artefact-contaminated histogram. The reachability study (§4)
confirms ~2,000 sits right at the method's worst-case floor within the α ≤ 0.70
envelope — feasible, if near the boundary (`runs/2026-06-03-small-n-reachability/`).

**This is the contribution that justifies the detailed JAMT methods presentation
and a reusable/repurposable codebase.** The method is an *instrument other
researchers apply to their own subcorpora.*

## 2. Why subsets, not empire (and what the empire fit is still good for)

The empire-scale fit is a **proof of concept** — it demonstrates the method works
and is narrowly valuable in its own right — but it is not where the research
payoff lies (Decision 34: subsets get their own fit; the empire-wide convention
shape is not imposed on them). The empire fit's genuine standalone uses:

- **A convention-corrected "epigraphic habit" curve.** The classic
  MacMullen / Meyer epigraphic-habit debate runs on the *raw* rise-and-fall of
  inscribing; a de-fogged version is a real substantive intervention in a
  long-standing question.
- **α(t) as a finding about cataloguing practice itself** — *"what fraction of the
  dated corpus is editorial template, and how does that shift over time and
  region?"* This is directly useful to the **LIRE / SDAM digital-epigraphy
  community** (the RAC-TRAC conference audience), who would *use* such a
  characterisation of their own data.
- **A population / information-flow proxy** (after cohort de-skewing) — the
  empire-level de-fogged signal as a coarse proxy for demographic or
  communicative intensity.
- **Latin West vs Greek East comparison** at province aggregation — a de-fogged
  cross-regional contrast.

## 3. The method as a shipped instrument (the JAMT framing)

The squarely methodological framing: **we ship an instrument, and the
reachability map is its spec sheet.** A reusable codebase plus a validated
"use it when N ≥ X, with these caveats" rule turns a clever model into a tool the
field can pick up. This reframes the paper from "here is a result" to "here is a
*method*, here is *exactly when it works*, and here is the *code*."

## 4. Answering the reviewer's "why go to all this trouble?"

A three-part answer, in order of force:

1. **The reachability map (the N-floor).** A validated rule — *subset-specific
   de-fogging recovers the genuine trajectory (≥90 % of replicates at Pearson
   r ≥ 0.95) from N ≈ 500 for the easiest subsets (low convention fraction
   α ≈ 0.30, smooth signals), rising to a worst-case floor of **N ≈ 2000** within
   the operating envelope (α ≤ 0.70); above α ≈ 0.70 it is unreliable at every
   tested N, and credible bands grow overconfident for sharply-peaked signals* —
   is a *reusable deliverable*, not a one-off result. It tells every future
   researcher with a subcorpus whether the method is in their toolkit *before*
   they invest in it. (Delivered by the small-N reachability study, 2026-06-03;
   map + table at `runs/2026-06-03-small-n-reachability/outputs/`.)
2. **At least one substantive subset demonstration** where it works — a large
   province or a real subcategory (e.g. the mother–daughter corpus, ~2,000, which
   sits **right at the measured worst-case floor of N ≈ 2000** — recoverable
   provided its convention fraction stays within the α ≤ 0.70 envelope) — showing
   a de-fogged trajectory that the raw histogram could not give.
3. **The honest-negative characterisation of where it fails.** The radiocarbon
   (rcarbon / Crema) and ceramics-aoristic communities **explicitly value**
   knowing where a method breaks, not just where it works. Reporting the floor and
   the degraded regimes *is* a contribution, not an admission.

The combination converts the anticipated critique ("relatively little utility")
into the paper's central value proposition: a bounded, reusable, honestly-
characterised instrument for putting a temporal dimension on subset epigraphy.

## 5. Honest scope boundaries (so the toolkit isn't over-sold)

- **Temporal questions only.** De-fogging fixes the *temporal distribution* of
  inscribing. It does **not** serve content/demographic questions directly (e.g.
  the mother–daughter *age-at-marriage* estimate itself is a content question; the
  de-fogging earns its keep only for the *"when did this practice vary"* part).
- **Sufficient N.** Below the reachability floor (**measured 2026-06-03: N ≈ 2000
  worst-case within the α ≤ 0.70 envelope; as low as N ≈ 500 for low-α,
  simple-shape subsets** — `runs/2026-06-03-small-n-reachability/outputs/REPORT.md`),
  a subset cannot be reliably de-fogged on its own; fall-backs (pooled convention,
  descriptive, the §5 hierarchical model) apply.
- **α ≤ ~0.70 and smooth-enough signals.** Heavily template-dominated regimes and
  sharply-peaked signals carry the caveats from Decisions 33 and the band-
  calibration check.
