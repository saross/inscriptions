---
title: "Scout synthesis — is auxiliary-classification identifiability-remediation principled?"
date: 2026-06-09
purpose: "Ground the planned joint-likelihood remediation (classification as a second likelihood term informing the convention fraction alpha) in established statistical + archaeological practice, before the next-session build."
verification: "All headline DOIs independently spot-verified against CrossRef/DataCite (Opus orchestrator, 2026-06-09); both scout drafts self-verified every DOI via the metadata APIs. Status below per item."
scouts: "lit-scout (statistical, 17 candidates) + prior-art-scout (archaeological, 12 candidates), run as parallel background agents."
---

# Scout synthesis — identifiability remediation by auxiliary classification

## Verdict: YES — the joint-likelihood approach is established practice, with a sharply-defined novel core

Both scouts converge. The design — **bring the grid-alignment classification in as a second
likelihood term that informs the mixing weight α, not as a prior** — is a principled
composition of two well-established traditions, and our empirical finding (the informed-α
*prior* failed) is now backed by formal theory.

### The statistical argument (clean, citable, three steps)

1. **The diagnosis is textbook.** Under weak component separation a mixing weight is only
   weakly identified and the likelihood can be *confidently wrong* — **Feller, Greif, Ho,
   Miratrix & Pillai (2016)** prove the MLE behaves as a threshold estimator that can declare
   components identical when they are not (`10.48550/arxiv.1602.06595`; journal version *Ann.
   Appl. Stat.* 2019). **Kim & Lindsay (2015)** give the "empirical identifiability" diagnostic
   for *which* units fall in the non-identified regime (`10.1007/s10463-014-0474-9`).
2. **A prior cannot fix it — a formal result.** For a partially-identified parameter the prior
   over the identification region is *never updated by the data* — **Gustafson (2010)**
   (`10.2202/1557-4679.1206`) and **Giacomini & Kitagawa (2021)** (`10.3982/ecta16773`). This
   is exactly why our wide/tight informed-α *prior* could not bite (the informed-alpha
   prototype + small-N re-test): the result was predicted by theory.
3. **Auxiliary info as a LIKELIHOOD term is the canonical remedy** — the concomitant-variable /
   latent-class-with-covariates tradition: **Dayton & Macready (1988)**
   (`10.1080/01621459.1988.10478584`) → **Wedel (2002)** (`10.1111/1467-9574.t01-1-00072`) →
   **Huang & Bandeen-Roche (2004)**, which develops the *identification theory* for adding
   covariate effects that restore identifiability (`10.1007/bf02295837`) → **Grün & Leisch
   (2008)** FlexMix (`10.18637/jss.v028.i04`) → **Berrettini et al. (2024)** Bayesian instance
   (`10.1093/jrsssc/qlae004`).

So "a prior cannot fix the confounded likelihood; a second likelihood term can" is a
two-citation argument (Feller + Gustafson for the problem; Huang & Bandeen-Roche for the fix).

### The archaeological precedent (mainstream — licenses the structure)

- **Bronk Ramsey (2009)**, OxCal "Dealing with Outliers", *Radiocarbon*
  (`10.1017/S0033822200034093`) — the structural archetype and about as mainstream as Bayesian
  archaeology gets: a **two-component reliable/unreliable latent mixture with per-sample quality
  weights inside one Bayesian model**. Our joint model is a frequency-distribution-level
  extension of this accepted structure.
- **Bayliss (2015)**, *World Archaeology* (`10.1080/00438243.2015.1067640`) — the authority that
  **quality classification is a prerequisite** for sound chronological inference (how we frame
  the move to reviewers).
- **Verhagen et al. (2016)**, *JAS Reports* (`10.1016/j.jasrep.2016.10.006`) — closest
  **Roman-period** precedent: dating-quality classification + per-quality-class aoristic analysis.
- Per-region stratification is standard (**Timpson et al. 2014** `10.1016/j.jas.2014.08.011`;
  **Crema, Bevan & Shennan 2017** `10.1016/j.jas.2017.09.007`); pooled-vs-tailored bias
  correction is explicitly studied (**Contreras & Codding 2023** `10.1007/s10816-023-09634-5`;
  **Surovell et al. 2009** `10.1016/j.jas.2009.03.029`; ADMUR / **Timpson et al. 2020**
  `10.1098/rstb.2019.0723`) — supports our pooled-vs-per-region `p_conv` choice.

### The novel core (sharply defined — a gap on BOTH sides)

No published work does a **joint frequency-distribution mixture that uses a classification
covariate as the identification instrument** to simultaneously estimate the convention shape and
the genuine shape over a *temporal* axis. Statistical side: concomitant-variable work is almost
all cross-sectional latent-class, not temporal-axis mixtures. Archaeological side: the field
filters upstream, subtracts an external-proxy bias curve, or stratifies post-hoc — none jointly
estimates both shapes. **We sit coherent with established practice, advancing beyond it** — the
ideal position for a methods contribution.

### On the two-regime fallback

Supported *in spirit* (point- vs set-identified inference, Gustafson / Giacomini & Kitagawa,
gated by the Kim & Lindsay diagnostic) but **not codified as named mixture practice** — frame it
as a principled composition of established pieces, not cite-wholesale. This **reinforces leading
with the single joint model** (which has a whole established literature — concomitant-variable
mixtures + the OxCal outlier model) over the two-regime switch.

## Read in full before the next-session build (verified)

**Statistical (Tier 1 → 2):**
1. Feller et al. 2016 — `10.48550/arxiv.1602.06595` (the weak-separation/confidently-wrong proof)
2. Gustafson 2010 — `10.2202/1557-4679.1206` (why a prior can't fix partial-ID)
3. Huang & Bandeen-Roche 2004 — `10.1007/bf02295837` (identification theory for the joint fix)
4. Giacomini & Kitagawa 2021 — `10.3982/ecta16773` (prior-vs-information-set; two-regime scaffold)
5. Dayton & Macready 1988 — `10.1080/01621459.1988.10478584` (concomitant-variable origin)

**Archaeological:**
1. Bronk Ramsey 2009 — `10.1017/S0033822200034093` (the OxCal two-component mixture archetype)
2. Bayliss 2015 — `10.1080/00438243.2015.1067640` (quality classification as prerequisite)
3. Verhagen et al. 2016 — `10.1016/j.jasrep.2016.10.006` (Roman-period quality-class aoristic)
4. Contreras & Codding 2023 — `10.1007/s10816-023-09634-5` (pooled vs tailored correction)
5. Surovell et al. 2009 — `10.1016/j.jas.2009.03.029` (auxiliary-proxy correction founding paper)

## Verification status

- Headline DOIs (10 above): independently spot-verified vs CrossRef (DataCite for Feller) —
  author, year, title, venue all match.
- Both scout drafts self-verified every DOI via `lit-search.py metadata` (CrossRef→DataCite→
  OpenAlex). Full claims.jsonl in the agent transcripts.
- **Two flags:** (a) Feller 2016 row is the arXiv DataCite DOI; a journal DOI (*Ann. Appl.
  Stat.* 2019) may be preferable for citation — confirm at staging. (b) Feller's author/year
  came from OpenAlex (no CrossRef record) — one tier less canonical, corroborated by DataCite +
  arXiv landing.

## Zotero staging

Both scouts report all candidates as **NEW** (none in the library) — but neither could fully
query Zotero (a missing `httpx` dep in the scout env), so **dedup is unconfirmed**. Surovell &
Bayliss may already be held (cited by the Crema 2022 paper already in the library). Highest-value
new adds: **Verhagen 2016, Contreras & Codding 2023** (archaeology) and the **Tier-1 statistical
trio** (Feller, Gustafson, Huang & Bandeen-Roche). Stage via the canonical pattern
(`/lit-scout-iterate` → `lit-scout-zotero-import.py <workspace> --live`).

## Optional deeper chaining (go/no-go for next session)

1. Forward-chain **Feller 2016** — most likely place to find a temporal-axis application and/or
   anyone already pairing the weak-separation diagnosis with an auxiliary-likelihood remedy
   (the exact prior art for our joint model).
2. Forward-chain **Kim & Lindsay 2015** — to settle whether a diagnostic-gated two-regime switch
   has been built before (the one "novel-ish" piece of the fallback).
3. Backward-chain **Huang & Bandeen-Roche 2004** — for the precise identifiability lemmas to cite
   in formally justifying the joint model's identifiability.
