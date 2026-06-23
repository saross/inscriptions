---
title: "Speaker script — *Dates-as-Data for Inscriptions* (RAC-TRAC 2026, TRAC7, Aarhus)"
author: "Adela Sobotková (presenting) — Shawn Ross (author, in absentia)"
date: 2026-05-22
target_length: "1500–1800 words (~ 12 min at 150 wpm)"
script_format: "Hybrid: continuous prose with slide-number headings as soft breaks. Slide advance cues in [brackets]."
delivery_target: "12 min spoken, leaving 8 min for Q&A in the 20-min slot."
---

# Speaker script

## Slide 1 — Are inscriptions a demographic proxy? *[opening]*

Good afternoon. I'm presenting work led by Shawn Ross at Macquarie, on whether Latin inscriptions can carry a demographic signal — or whether, as much of the field has argued, they're cultural artefacts and nothing more.

The starting point is forty years of summed-probability analysis in archaeology. From Rick in 1987 through Timpson and colleagues in 2014 and Crema and Bevan in 2021, archaeologists have read radiocarbon-date distributions as evidence about past population. The technique has its critics, but it's now a substantial methodological tradition.

Latin epigraphy has analogous data. LIRE version 3 — the corpus we use — gathers a hundred and eighty thousand inscriptions for the Western Roman Empire between roughly 50 BC and AD 350. So the question is natural: can we transfer the dates-as-data toolkit from radiocarbon to inscriptions?

The standard answer in classics has been no. MacMullen's foundational 1982 paper, reinforced by Hanson 2021, argues that inscription counts reflect the *epigraphic habit* — the cultural patterning of who chose to inscribe what, where, and when — and not demography. That position is well-founded. There's decades of evidence that inscription production is culturally patterned in ways that don't reduce to population.

What this talk does is take that critique seriously, and then ask: even granting that habit is real, *how much* of the variation in inscription counts traces to underlying population? If the answer is zero, the habit-only position holds. If it's anything more than a few percent, then inscriptions become at least a partial demographic proxy — and the radiocarbon toolkit becomes available for epigraphic studies.

*[advance]*

## Slide 2 — Problem: Serious editorial distortion of inscription dates

Before we can do any of that, we have to deal with how Roman inscriptions are actually dated.

When a Roman epigrapher writes "2nd century AD" on an inscription, they're not claiming the inscription is equally likely to be from any year between AD 100 and 199. They're using a convention — *the 2nd-century template* — to express a roughly-known date. The same goes for "mid-Flavian", "reign of Hadrian", or "second quarter of the 3rd century". These are conventions of dating practice, not uniform probability distributions over years.

That's the data hazard. If you treat those conventional dates as if they were uniform across their stated range — which is what standard uniform-aoristic does — you build a structured artefact into your summed-probability curve. You get big flat plateaus at the conventional intervals, with sharp steps at convention boundaries. The radiocarbon literature doesn't face this; calibration curves are messy, but they don't fall on round centuries.

You can see the artefact directly on the screen. Fifty-four and a half percent of `not_before` values in the LIRE corpus end in "01"; fifty-three percent of `not_after` values end in "00". That's the signature of century-template encoding. The largest single step is at the BC–AD boundary, where roughly eleven hundred and fifty inscriptions move between century templates simultaneously.

Some of you will be noticing the three narrow spikes at AD 77.5, 122.5, and 212.5. Those are *not* what this slide is about — but worth flagging, because someone always asks. They sit at dynasty midpoints, and they're a mix: partly convention (regnal-interval templates like "reign of Hadrian"), partly tighter consular-year dating that genuinely anchors back to ancient Roman practice. The Hadrianic spike at 122.5 is roughly seventy percent year-precise inscriptions dated to the consular pair of AD 123, and thirty percent broad reign-template. The mixture model on slide 5 separates both layers properly. The slabs are the cleaner case, and they're what this slide is asking you to notice.

*[advance]*

## Slide 3a — Minimum corpus required to detect deviations determined by simulation

So given that data hazard, what kinds of historical questions can we credibly ask? That's a question we have to settle *before* running any analysis, not after.

The work here is a power simulation. We generate synthetic corpora where we know the right answer in advance — we plant a known signal, like a fifty-percent-over-fifty-year shift in inscription production — and then run our detection methods on them to measure how often they catch the planted signal. Repeat across many combinations of sample size and event magnitude, and you get a map of where the method works and where it doesn't.

The headline reads: at empire scale, with our hundred and eighty thousand inscriptions, we can detect a crisis-of-the-third-century-scale change reliably. At province or city scale, we need at least about sixteen hundred inscriptions before the method gives us power. False-positive rates are below five percent under the null. That's the discipline the next four slides operate within.

*[advance]*

## Slide 3b — Deviation recovery across sample and effect sizes

Extending that map gives the full sensitivity picture. Below about a thousand inscriptions, formal change-detection isn't reliable at any event size. At roughly twenty-five hundred, we can detect crisis-scale events confidently. Sharper, smaller events — twenty-percent shifts over twenty-five years — are below our resolving power at any sample size we tested.

The implication for the field: corpora below the change-detection threshold aren't useless, but they should be used for descriptive shape comparison or cross-sectional regression rather than formal trend inference. That's the pre-analysis discipline we'd like to see become more common in inscription studies generally.

*[advance]*

## Slide 4 — What the data look like at multiple scales

Here's what eight provinces and eight cities actually look like, sample-size-ranked, Rome excluded, raw and uncorrected, with each curve normalised to its own peak so shapes are comparable across very different total counts.

Each curve has its own story. Some shapes map onto historical events you'd expect to see. Pompeii's curve cuts off cleanly at AD 79, because that's when Vesuvius buried the city — it's a literal preservation artefact you can read off the chart. Dacia's narrow window from roughly AD 100 to 270 maps almost exactly onto the period of Roman occupation, from Trajan's conquest to Aurelian's withdrawal. Latium and Campania's early spike includes Pompeii's contribution.

Other shapes don't reduce so cleanly. Pannonia superior peaks late; Britannia peaks in the mid-second century; Cirta has a single tight peak around AD 200. Some of that is real demographic and economic history, some is epigraphic culture, some is preservation. Distinguishing those is what the rest of the talk is about.

The point of *this* slide is empirical, not statistical: at every scale we look at, there's structure beyond a uniform distribution. The convention layer we identified on slide 2 lives in these curves, but it doesn't drown out the rest of the signal. There's something worth modelling here.

*[advance]*

## Slide 5 — Removing the convention layer

The model on this slide pulls the two layers apart. We say the observed SPA is a weighted sum of two shapes: a *convention component* — what we see when editors use wide-template intervals — and an *ancient-signal component* — what real Roman inscriptional production looked like over time. The model estimates both layers from the data.

The convention component isn't a free shape we let wander. It's built from a small dictionary of empirically-attested templates: century slabs; half-century slabs where editors used them; reign-interval templates for Augustan, Flavian, Hadrianic, Antonine, Severan periods. Year-precise inscriptions stay out of the convention component — they remain in the ancient signal as real anchors back to consular dating.

The framework isn't new in archaeology. Enrico Crema and colleagues developed Bayesian aoristic for interval-dated ceramics, where a sherd is dated to a fabric type with a known production window. The architecture transfers directly: template intervals play the role of fabric-type windows. Crema's recent `baorista` package is the explicit reference.

What you see on the right is a demonstration on synthetic data where we know the right answer in advance. The grey histogram is the simulated observation; the red curve is the convention layer the model recovered; the green curve is the ancient signal. They separate cleanly. The full validation grid runs post-talk — what we're showing today is the recovery principle, not a claim that the model is fully validated yet.

*[advance]*

## Slide 6 — What we found

This is the substantive punchline. To work out how much of the city-to-city variation in inscription counts is population versus everything else, we have to compare cities within the *same* province. That strips out province-level differences in epigraphic habit, economic and social structure, political and administrative practice, cultural patterning, and survival bias — the full territory the habit critique broadly points at. The within-province comparison is the cleanest within-empire comparison the data support.

On a corpus of one thousand and forty-four Hanson-matched cities, Rome excluded, the within-province population effect accounts for about *thirty percent* of the systematic city-to-city variation in inscription counts. The ninety-five-percent credible interval is twenty-four to thirty-seven percent. That sits comfortably above the ten-percent threshold we preregistered as the "supported" boundary.

So both sides of the long-running debate are partially right. The habit critique captures the larger share — about seventy percent of the systematic variation lives in province-level effects that we can't cleanly attribute to population alone. But the demographic signal is real, substantial, and measurable. As far as we can tell, this is the first preregistered quantitative partition of habit-versus-population on a major inscription corpus.

One caveat: this is a single-scale analysis — cities within provinces. Proper protection against the Modifiable Areal Unit Problem requires re-doing the partition at multiple aggregation levels — cities within macro-regions, provinces within the empire. The within-province construction handles part of the problem; the multi-scale check is the next-order protection. That work is on the post-talk to-do list; we expect the thirty percent to be robust, but that's testable rather than asserted.

*[advance]*

## Slide 7 — What it means

Three implications.

For the habit-only position: not refuted, but partially qualified. About a third of variation traces to within-province population; the other two-thirds is the habit-critique's territory. Both are real.

For epigraphic studies more broadly: inscription-SPA becomes a legitimate tool for population work, with sample-size tiering. Corpora above about sixteen hundred inscriptions can support formal change-detection. Smaller corpora can still do descriptive shape claims and cross-sectional analysis with population as a partial control.

For small-N studies — descriptive shape and cross-sectional claims are well-supported; continuous change-detection requires aggregation. Let me make that concrete.

*[advance]*

## Slide 7a — Worked example: marriage-age inscriptions

Adela has a paper later in this session on Roman marriage age, using the wife and daughter inscriptions from EDH and LIRE. About seventeen hundred records carry both an age and a familial role. The classic Shaw and Saller framing reads the age at which *wife* dedications overtake *daughter* dedications as a proxy for the average age at first marriage. The question Adela's paper asks is whether that crossover age *shifted* in response to demographic and economic shocks — the Antonine plague, the third-century crisis.

So how does our reachability work apply to that corpus? The static crossover — Shaw's original 1987 finding, computed over the whole corpus — has seventeen hundred records to work with. That sits comfortably above the descriptive-shape threshold; Adela has already reproduced Shaw under stricter spatio-temporal filters.

The harder version — has the crossover *moved* over time — slices the corpus by fifty-year bin, where you get two to three hundred records per bin. Below our change-detection floor on a continuous trajectory. But the question is categorical, not continuous, so the workaround is categorical comparison across pooled periods, with urban-versus-rural slicing where additional signal is needed.

Any small-corpus inscription project can map onto the same ladder. Figure out where you sit; choose claims accordingly.

*[advance]*

## Slide 8 — Questions for this room

Four things we'd value most from the discussion. Does the convention layer match dating practice you've seen in EDH, EDCS, or LIRE — are there template intervals we've missed? Which sub-mechanisms do you think drive the seventy-percent non-population variance — status display, monumental practice, religious cycles, administrative density? Which sub-corpora *should* habit-alone clearly dominate, as our natural falsification test? And what independent demographic anchors would you trust as ground-truth for validating the corrected SPA?

*[advance]*

## Slide 9 — Open science *[closing]*

Everything we've shown is preregistered — the OSF link is on screen, lodged 2026-05-20, embargoed for the moment. The repository is public and pinned at the lodgement tag, so you can clone it and audit what we did. This is a feedback-seeking talk; the confirmatory tests are pinned in the prereg and run post-talk.

Thank you. I'd value your feedback.

*[Q&A — backup slides ready under press `o`]*

---

**Word count**: ~ 1,900 spoken words across 10 slides (1, 2, 3a, 3b, 4, 5, 6, 7, 7a, 8, 9). At 150 wpm reading pace = ~ 12.7 min. Leaves ~ 7 min for Q&A in the 20-min slot.

**Pacing notes**:

- **Slide 6 is the substantive punchline.** Give it the most breathing room — Adela should let the 30 % land before moving on, and pause briefly after the "first preregistered quantitative partition" line.
- **Slide 5** is the most technically dense; Adela can speed up the second half ("framework isn't new in archaeology...") if running long.
- **Slide 7a** (worked example) can compress to ~ 45 s if Adela has already explained her own data structure earlier in the session; the full 70 s is for first-time exposure.
- **Slide 8** (questions): read each question and pause briefly before moving on — invites the audience to engage rather than just filling time.
- **If running long**: the worked-example slide 7a is the natural cut — the implications on slide 7 still land without it.
