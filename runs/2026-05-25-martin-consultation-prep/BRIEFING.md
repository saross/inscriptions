---
title: "Martin consultation 2026-05-25 — Shawn's pre-meeting briefing"
audience: "Shawn (PI), going into the consultation"
register: "Plain-language; for Shawn to read once, scan twice, refer to during the meeting"
date: 2026-05-25
status: pre-meeting brief
related-artefacts:
  - planning/h2.1-mixture-model-problem-explained-2026-05-24.md (the problem)
  - planning/h2.1-discard-vs-recover-rationale-2026-05-24.md (the strategic case)
  - planning/h2.1-prior-art-scout-empirical-bayes-calibration-2026-05-24.md (prior art)
  - planning/h2.1-stage-3-implementation-plan-2026-05-25.md (implementation spec)
  - planning/martin-consultation-2026-05-25-followup.md (the formal consultation pack)
  - runs/2026-05-25-martin-consultation-prep/outputs/figures/ (the four figures)
---

# Martin consultation briefing — 2026-05-25

Pre-meeting briefing for the 90-minute consultation. Plain language;
structured around how Martin will probably want to run the conversation.

---

## 1. The two-minute opener — what's changed since last week

In one paragraph: the recovery-grid validation of the H2.1 mixture
model **failed** its preregistered binding criteria (40.9 % of cells
passing both α-coverage and shape-recovery). We've spent the week
diagnosing the failure and developing a structural fix. The
diagnostic identified a **likelihood ridge** between α (the editorial-
convention mixing weight) and the genuine-activity shape — the data
can't uniquely identify α from the shape, so the posterior splits the
difference, biasing α toward 0.5. Two cheap candidate fixes were
ruled out empirically: a sharper α prior moved the posterior by only
+0.025 (it's not prior-pull), and a non-centred reparameterisation of
the smoothness component moved the posterior by +0.001 (it's not
funnel geometry). The bias is structural identifiability. The leading
candidate fix is an **empirical-Bayes calibration cohort**: use the
narrow-dated subset of LIRE to inform the prior on the genuine
component, and the editorial-slab structure of the wide-dated subset
to inform the convention component. Both empirical building blocks
are now built (Stages 1-2); the modified-model implementation
specification is ready to execute (Stage 3); the validation diagnostic
plan is in place (Stage 4).

**One number to remember**: roughly 65 % of LIRE is editorial templates
(century, half-century, two-century slabs predominantly); 17 % is
hard signal (tight-dated + reign-window); 17 % is wide non-round
intervals (ambiguous). The 65/17/17 split is the headline
data-quality finding.

**The big "free win" we've already banked**: the non-centred GRW
reparameterisation gives a 45-50 × effective-sample-size improvement
at zero posterior-shape cost. Worth adopting unconditionally. Mention
this early — Martin will appreciate the diagnostic discipline and
this is the easy good-news item.

---

## 2. The high-level decisions Martin will probably open with

Martin is more comfortable with frequentist econometric framings than
with hierarchical Bayes / MCMC. Frame these in his native vocabulary
where possible.

### Decision A — "Recover from the editorial 2/3, or discard it?"

Martin may open here because it's the most fundamental strategic
choice. We have a written rationale at
`planning/h2.1-discard-vs-recover-rationale-2026-05-24.md`.

**The case for recover** (which we lean toward): editorial-templated
inscriptions contain partial information — an `AD 101-200` inscription
rules out 75 % of the timeline. Throwing them away costs ~ 2.4 × in
effective sample size and blocks per-province × per-half-century
stratification. The radiocarbon-SPA community had this exact debate
twenty years ago and settled on "use all data with proper uncertainty
modelling".

**The case for discard** (which we hold as fallback): simplicity;
robustness to mis-specification; 30,000+ records is still large by
field standards; the discard approach gives unbiased (though noisier)
estimates immediately, whereas the recover approach needs a model fix
that we haven't yet validated.

**What we want from Martin**: confirmation that the radiocarbon-SPA
analogy is the right one. If he agrees, we proceed with the modified
mixture model and use the discard approach as a supplementary
triangulation. If he disagrees, we may need to rethink the primary-vs-
supplementary roles.

### Decision B — "Is the empirical-Bayes calibration cohort the right structural fix?"

Once we agree on recover, the next question is whether our specific
approach is methodologically sound.

The approach: **separate LIRE into a "convention cohort" (F1+F3 —
inscriptions whose intervals match editorial templates like 'AD
101-200') and a "calibration cohort" (Tight + F2_Other — tight-dated
and reign-window content)**. The convention cohort defines the
shape of the editorial component. The calibration cohort defines an
informative prior on the genuine-activity component. The mixture
model's only remaining job is to estimate α (the mixing weight) and
let the genuine-component shape refine within the prior's window.

**Key methodological supports**: SCUBIDO (Boyall et al. 2025) for
palaeoclimate; Christophe et al. 2018 (MD2) for OSL dating; BUMPER
(Holden et al. 2017) for palaeo-environmental reconstruction; Wraith
et al. 2014 for the theoretical mechanism; Betancourt 2017 for the
identifiability proof.

**Key risk**: Spektor & Kellen 2018 — empirical priors in non-
identifiable models can shift the posterior without resolving the
ridge if the calibration cohort is itself biased. Our calibration
cohort IS biased (honorific over-represented, epitaph under-
represented relative to corpus); we correct via type-reweighting
(post-stratification), but residual bias is unavoidable.

**What we want from Martin**: a frequentist sanity-check. Does this
look like a Bayesian-source-apportionment problem to him (which is a
solved problem)? Does the type-reweighting actually correct the bias?
Or does he see other failure modes we should flag?

### Decision C — "What does 'the fix works' actually mean operationally?"

The recovery-grid binding criteria are α-coverage ≥ 90 % per cell and
shape-Pearson-r ≥ 0.95 per cell, both at ≥ 90 % of cells. We propose
running the same recovery grid under the modified model. But Martin
may prefer additional or alternative diagnostics:

- A **profile-likelihood plot** — fix α at a grid of values, find the
  best-fit p_gen for each, plot the maximised log-likelihood. A flat
  profile is direct evidence of weak identification. *We haven't built
  this yet; if Martin wants it, it's ~1-2 hours.*
- **Fisher information at the data-generating parameters** — does the
  Fisher matrix become better-conditioned under the modified model?
  Frequentist identifiability diagnostic.
- **Posterior contraction** — does the posterior CI on α narrow
  enough under the modified model? Bayesian equivalent.

**What we want from Martin**: which of these diagnostics he'd
prioritise to demonstrate convincingly that the fix works.

---

## 3. The four key figures

Stage these on screen / print before the meeting. All in
`runs/2026-05-25-martin-consultation-prep/outputs/figures/`.

### Figure 1 — Uncorrected SPA (`spa-uncorrected.png`)

What it is: the full LIRE corpus, aoristic SPA, 5-y bins, 50 BC – AD
350 envelope.

What to point out:

- The plateau-step pattern at AD 1, 100, 200, 300 — these are
  editorial-template discontinuities (each century-slab template's
  start and end edges).
- The spike at AD ~ 78 — the Vesuvius / Pompeii dated-event cluster
  (and the start of the Flavian dynasty), tight dating.
- The spike at AD ~ 122 — Hadrianic period.
- The step-up at AD 1 and the gentle decline after AD 300 — the
  corpus envelope effects.

What Martin will probably ask: "How much of this is real activity
and how much is editorial?" — which is exactly the question Figure 2
answers.

### Figure 2 — Slab-highlighting SPA (`spa-slab-highlighting.png`)

What it is: the same SPA, now stacked by Family classification. Red +
orange = editorial templates (F1 + F3). Greens = signal (Tight +
F2_Other). Grey = wide non-round (Big).

What to point out:

- **The body of the corpus (AD 1-300) is 60-70 % editorial templates
  by aoristic mass.** Per-region numbers (printed in caption / in the
  script's output): editorial fraction 62 %, 68 %, 61 %, 80 % for
  AD 1-100, 100-200, 200-300, 300-350 respectively.
- **The signal fraction (greens) is 10-19 % across the body of the
  envelope** — small but non-zero. Specific signal peaks visible: AD
  78 (Vesuvius), AD 211-217 (Caracalla), AD 290-325 (tetrarchic).
- **The 50 BC – AD 1 region is mostly Big (grey)** — editorial
  templates don't extend much into the BC era; what's there is wide
  non-round intervals (`AD -50 to AD 50` etc.).

What Martin will probably ask: "Are F1 and F3 actually editorial, or
could they be genuine clusters that happen to land on these widths?"
— answer: we validated this empirically by looking at the dominant
`(not_before, not_after)` pairs at each family. F1 is dominated by
`AD 101-200`, `AD 1-100`, `AD 301-400`, `AD 1-50`, `AD 51-100`, etc.
F3 is dominated by `AD 31-70`, `AD 71-100`, `AD 131-170`. These are
unmistakably editorial round-number templates, not historical
clusters.

### Figure 3 — Slab-excluding SPA (`spa-slab-excluding.png`)

What it is: Cohort B (Tight + F2_Other) only — the family-filtered
signal subset, n = 31,841 records, 17.4 % of corpus. Shown both
unweighted (light green) and type-reweighted to match corpus
composition (dark blue, the empirical-Bayes prior on p_gen).

What to point out:

- **Three clear signal peaks**: AD 78 (Vesuvius / Flavian), AD
  211-217 (Caracalla solo reign), AD 290-325 (Diocletian-to-
  Constantine, tetrarchic). All are reign-window or dated-event
  driven.
- **The reweighting tightens the AD 290-325 peak** — that peak is
  driven by tightly-dated epitaphs in the tetrarchic reign-window;
  reweighting up-weights epitaphs but also redistributes the
  contribution across types.
- **This is what the empirical-Bayes prior on p_gen will be.** The
  modified mixture model centres on this shape with a ~ ± 9 %
  multiplicative variance (bootstrap-derived sigma_prior).

What Martin will probably ask: "Why these three peaks specifically?
Are they over-fitting to the cohort's biases?" — partly yes. The
peaks reflect what got dated tightly in the corpus; not all of the
actual historical activity was tightly-dated. The reweighting
correction is our attempt to balance this. The bootstrap CI tells us
the uncertainty: tight in the body, wider at the edges.

### Figure 4 — Hanson scaling (`hanson-scaling-nbr-bootstrap.png`)

What it is: the substantive H3a question — log(LIRE inscription
count) vs log(Hanson urban-area population estimate), N = 1,044
Roman cities (Rome excluded), date-window-filtered LIRE counts. Red
line = negative-binomial regression fit, β = 0.566 (95 % CI 0.543-
0.574). Green dashed = OLS log-log, β = 0.284. Comparators: Hanson
2021 β = 0.672 (CI 0.588-0.756); Carleton et al. 2025 β ∈ [0.3, 0.5].

What to point out:

- **Our β = 0.566 falls between Hanson's 0.672 and Carleton's 0.3-0.5
  range** — interpretively interesting. We're using the LIRE corpus
  with the prereg date-window filter; Hanson used CIL; Carleton used
  a stricter filter.
- **This is the substantive headline result** — population-inscription
  scaling exists, is sub-linear, and is in the range expected.
- **This was done with the discard approach** — only narrow-dated
  inscriptions contributed. So the H3a result is already publishable
  on the discard pipeline; the mixture-model approach is for
  enriching it with wider-corpus data.

What Martin will probably ask: "Is the date-window filter doing the
work, or is the scaling robust?" — sensitivity tests in the prereg
(date-window-narrow vs date-window-permissive) are designed to
answer this.

---

## 4. The seven implementation-level decisions (the Stage 3 spec)

These are the tactical decisions. The Stage 3 implementation plan
(`planning/h2.1-stage-3-implementation-plan-2026-05-25.md`) has these
flagged in detail. Brief versions, in order of importance:

1. **Fixed vs Dirichlet-prior on slab-type weights for p_conv.** Stage
   1 gave us empirical weights for the 9 slab types (century 40 %,
   two-century 24 %, etc.). Should the model FIX these (SCUBIDO-style,
   no slack) or use them as the centre of a Dirichlet prior
   (informative but not fixed)?

   Our default: Dirichlet with concentration matched to empirical
   counts. Lets the model refine within a tight window. Martin may
   prefer fixed.

2. **Per-bin vs scalar sigma_prior on p_gen.** Stage 2 gave us a
   bin-wise bootstrap SD on log p_gen (median 0.044). Should the
   modified model use the per-bin values (more accurate but
   parameter-heavy) or a single scalar (median across bins; simpler)?

   Our default: per-bin. Lets the prior naturally widen at envelope
   edges where coverage is thin. Martin may prefer scalar for
   simplicity.

3. **Robustness inflation factor on sigma_prior.** The bootstrap CI
   captures within-cohort variability but not the (uncertain) bias
   between cohort and true ancient activity. Should we inflate
   sigma_prior by 1.5 × or 2 × as a robustness measure?

   Our default: 1.0 × (no inflation) initially; check if posterior is
   too tight. Martin's call.

4. **α prior choice.** Current is Beta(2, 2). F1 showed a small
   prior-pull effect. We've proposed Beta(1, 1) (uniform) for the
   modified model — but Martin may want something more or less
   informative.

5. **Unknown-type residual handling.** 23 % of Cohort B is type =
   "unknown" (the type-of-inscription_auto classifier returned NaN).
   We reweight at 0.60 × — but if these unknowns are systematically
   under-classified epitaphs (the corpus majority), the reweighting
   is under-correcting. Worth a sensitivity check.

6. **sigma_smooth prior unchanged vs re-estimated.** The GRW
   smoothness σ has its own prior in the current model
   (`HalfNormal(0.3)`). Under the empirical-Bayes prior on p_gen,
   the role of σ_smooth changes — should its prior be re-tightened
   or left unchanged?

7. **Stage 4 synthetic-data regeneration.** The current 450-cell
   recovery grid generates synthetic data using the old
   tier-template basis. Should Stage 4 use the *same* synthetic data
   (a like-for-like test of the new model on the same simulated
   ground truth) or regenerate synthetic data using the new empirical
   basis (a test of internal consistency)?

   Our default: use the same synthetic data for direct comparability.
   Generate new synthetic data only if the same-data test fails in a
   way that suggests the design has shifted.

---

## 5. Where Martin might push back productively — anticipate these

Three areas to be ready for.

### "Why not a state-space / HMM model instead?"

Martin previously suggested HMM (the 2026-05-19 pre-meeting exchange,
prior-art scout at `planning/prior-art-scout-2026-05-19-hmm-aoristic.md`).

Our position: HMM is a substantial methodological pivot. The mixture-
model approach is closer to what's currently in the prereg. We're
willing to consider HMM in a future iteration but not at the cost of
re-doing months of work for the current paper. The mixture model with
the empirical-Bayes fix should be sufficient for the substantive
questions.

### "Why is your prior centred on the cohort SPA, not on a theoretical model?"

Martin may prefer a parametric prior — e.g., a Gaussian process with
a hyperprior on length-scale — rather than the empirical cohort-derived
shape. Empirical priors are less interpretable and harder to defend.

Our position: the cohort SPA *is* informative about ancient inscription
activity in a way that theoretical priors aren't (we'd have to invent
the parametric form ourselves). The cohort is biased but the bias is
characterised and corrected via reweighting. A theoretical prior would
just push the bias somewhere else (into the parametric form's
assumptions).

### "What if the modified model still fails the recovery grid?"

Real risk. We have a decision tree (in
`planning/h2.1-discard-vs-recover-rationale-2026-05-24.md` §10).
Short version: if the fix doesn't work, we fall back to the discard
pipeline as primary with the mixture model as exploratory + methodology
discussion. The paper still ships; the methodological framing shifts.

---

## 6. Things we want from Martin, in priority order

1. **Sign off (or push back) on the empirical-Bayes calibration-cohort
   approach.** If he disagrees, everything else is moot.
2. **Guidance on the seven Stage 3 design decisions** — particularly
   #1 (Dirichlet vs fixed p_conv), #2 (per-bin vs scalar sigma_prior),
   #4 (α prior choice).
3. **A "yes, that's a valid diagnostic" verdict on Stage 4** —
   recovery-grid validation of the modified model under the same
   binding criteria as the original prereg.
4. **A specific recommendation on the OSF amendment timing** — when
   to lift the embargo, when to file the amendment, whether the
   methodology paper splits off.
5. **Acknowledgement on the methodology paper** if he's comfortable
   being named.

---

## 7. The 30-second wrap if conversation runs short

If the consultation runs short or Martin needs a quick out, the
priority list:

1. **Approach is empirical-Bayes calibration cohort.** ✓ or ✗
2. **Defaults on seven decisions are documented.** Quick override on
   any of them or accept defaults.
3. **Stage 4 diagnostic is recovery-grid on modified model.** ✓ or
   alternative.
4. **We'll have empirical Stage 4 verdict in ~ 1 week** (implementation
   6-8 h + smoke test + Stage 4 diagnostic 30 min + reporting 2 h).

End of brief.
