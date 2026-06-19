# Lit-scout draft: Point-date Monte Carlo sampling vs mass-apportionment — bias of plug-in latent dates on mixture-component share under classification contamination

⚠ **VERIFICATION PENDING** — this is a draft from the proposer (lit-scout). The `/lit-scout` slash command runs the `lit-scout-verifier` serial agent against this draft before returning the final output. If you are reading this marker in final output, verification failed — see the banner at top of the document.

## TL;DR

There is **no single named phenomenon** in archaeology covering your exact effect, but it is **two well-documented effects that meet at your problem**, both citeable: (a) in archaeological dating, the critique that **point-wise / Monte-Carlo date-sampling distorts downstream quantitative inference relative to probability-mass apportionment** is established — Carleton & Groucutt 2021 (10.1177/0959683620981700) name the pointwise problem, Roberts et al. 2012 (10.1016/j.jas.2011.12.022) is the canonical "chronological apportioning" alternative, and Crema 2012/2025 frame the apportionment-vs-sampling distinction directly; (b) the **general statistical mechanism is the "three-step"/"classify-analyze" plug-in bias** in latent-class and mixture models — Bolck, Croon & Hagenaars 2004 (10.1093/pan/mph001) proved that plugging point-estimated latent class assignments into a downstream model **systematically attenuates the structural association**, with the bias driven by *classification/measurement error* in the assignment, which is precisely your "collapse driven by indicator misclassification". The biggest gap: nobody (that I found) has joined these two literatures around a cross-classified time×alignment deconvolution, so your contribution is novel, and you can cite both halves plus the imputation framing (Nielsen 2003; Rubin's proper-imputation/integrate-out principle via Blomberg & Todorov 2025) to explain *why* apportionment ≈ integrating-out recovers α while single sampling ≈ improper plug-in collapses it.

## Findings table

| # | Fit | Cites | Authors (Year) | Title | DOI | Chain | Chains | Cluster | Status |
|---|-----|-------|----------------|-------|-----|-------|--------|---------|--------|
| 1 | HIGH — names the pointwise-interpretation problem for aggregated-date proxies; your point-date MC is the pointwise operation it warns against | 60 | Carleton, W. Christopher; Groucutt, Huw S. (2021) | Sum things are not what they seem: Problems with point-wise interpretations and quantitative analyses of proxies based on aggregated radiocarbon dates | 10.1177/0959683620981700 | seed; refs-of #2 | 2 | A: Aoristic/SPD pointwise-vs-mass critique | [IN ZOTERO] |
| 2 | HIGH — the canonical mass-apportionment method for date-uncertain assemblages; this *is* your "mass-apportionment" arm, with named provenance | 34 | Roberts, John M.; Mills, Barbara J.; Clark, Jeffery J.; Haas, W. Randall; Huntley, Deborah L.; Trowbridge, Meaghan A. (2012) | A method for chronological apportioning of ceramic assemblages | 10.1016/j.jas.2011.12.022 | refs-of #5 | 1 | A: Aoristic/SPD pointwise-vs-mass critique | NEW |
| 3 | HIGH — foundational aoristic MC paper; explicitly sets out the Monte-Carlo date-sampling vs probability-mass ("aoristic sum") distinction you are contrasting | 99 | Crema, Enrico R. (2012) | Modelling Temporal Uncertainty in Archaeological Analysis | 10.1007/s10816-011-9122-3 | seed; refs-of #5 | 2 | A: Aoristic/SPD pointwise-vs-mass critique | [IN ZOTERO] |
| 4 | HIGH — argues aoristic/apportionment is misused and advocates integrating-out (Bayesian) over ad-hoc weighting; closest archaeological articulation of plug-in-vs-integrate | 7 | Crema, Enrico R. (2025) | A Bayesian alternative for aoristic analyses in archaeology | 10.1111/arcm.12984 | seed | 1 | A: Aoristic/SPD pointwise-vs-mass critique | [IN ZOTERO] |
| 5 | HIGH — "the plug-in bias keystone": proves naive plug-in of point-estimated latent class scores into a downstream model systematically attenuates the structural association; your α-collapse is this bias | 1083 | Bolck, Annabel; Croon, Marcel; Hagenaars, Jacques (2004) | Estimating Latent Structure Models with Categorical Variables: One-Step Versus Three-Step Estimators | 10.1093/pan/mph001 | seed | 1 | C: Three-step / classify-analyze plug-in bias | NEW |
| 6 | HIGH — generalises BCH; shows the downward bias is governed by *classification error* and corrects by carrying the misclassification matrix; matches "collapse driven by indicator misclassification, not interval width" | 507 | Bakk, Zsuzsa; Tekle, Fetene B.; Vermunt, Jeroen K. (2013) | Estimating the Association between Latent Class Membership and External Variables Using Bias-adjusted Three-step Approaches | 10.1177/0081175012470644 | cited-by #5 | 1 | C: Three-step / classify-analyze plug-in bias | NEW |
| 7 | HIGH — "classify-analyze" framing: assigning then analysing a hard class label biases estimates; the integrate-out ("inclusive"/model-based) approach removes it — direct analogue of mass-apportionment | 208 | Bray, Bethany C.; Lanza, Stephanie T.; Tan, Xianming (2015) | Eliminating Bias in Classify-Analyze Approaches for Latent Class Analysis | 10.1080/10705511.2014.935265 | cited-by #5 | 1 | C: Three-step / classify-analyze plug-in bias | NEW |
| 8 | MEDIUM — the standard "improved three-step" correction (ML and BCH); useful to cite for *how* one fixes the bias if you want to position apportionment as the fix | 1976 | Vermunt, Jeroen K. (2010) | Latent Class Modeling with Covariates: Two Improved Three-Step Approaches | 10.1093/pan/mpq025 | cited-by #5 | 1 | C: Three-step / classify-analyze plug-in bias | NEW |
| 9 | MEDIUM — recent overview of relating latent class membership to external variables; best single citeable review of the whole three-step bias literature | 121 | Bakk, Zsuzsa; Kuha, Jouni (2021) | Relating latent class membership to external variables: An overview | 10.1111/bmsp.12227 | cited-by #5 | 1 | C: Three-step / classify-analyze plug-in bias | NEW |
| 10 | HIGH — finite-mixture-of-experts representation of a *misclassified categorical covariate*; closest formal treatment of "noisy class indicator biases the mixing structure" and how modelling the misclassification recovers it | 3 | Xia, Michelle; Richard Hahn, P.; Gustafson, Paul (2020) | A Bayesian mixture of experts approach to covariate misclassification | 10.1002/cjs.11560 | seed | 1 | D: Mixtures under covariate/indicator misclassification | NEW |
| 11 | HIGH — proper-vs-improper imputation: stochastic single imputation that ignores predictive uncertainty is "improper" and yields inconsistent downstream inference; the integrate-out analogue is "proper" | 70 | Nielsen, Søren Feodor (2003) | Proper and Improper Multiple Imputation | 10.1111/j.1751-5823.2003.tb00214.x | seed | 1 | B: Single-imputation / plug-in vs integrate-out | NEW |
| 12 | MEDIUM — accessible recent statement that single (point) imputation of a latent value biases/mis-states downstream estimates and multiple imputation (mass over the predictive) fixes it; good "explain the implication" citation | 7 | Blomberg, Simone P.; Todorov, Orlin S. (2025) | The fallacy of single imputation for trait databases: Use multiple imputation instead | 10.1111/2041-210x.14494 | seed | 1 | B: Single-imputation / plug-in vs integrate-out | NEW |
| 13 | HIGH — the measurement-error analogue you asked for: using a noisy surrogate for a latent quantity attenuates the estimate toward null; conceptual sibling of your α-collapse, and very widely citeable | 626 | Hutcheon, J. A.; Chiolero, A.; Hanley, J. A. (2010) | Random measurement error and regression dilution bias | 10.1136/bmj.c2289 | seed | 1 | E: Measurement-error / regression-dilution analogue | NEW |
| 14 | MEDIUM — foundational result that covariate measurement error biases (functional) estimates and that the *conditional expectation* (regression calibration) is the correction — i.e. use E[date|interval], not a draw | 192 | Stefanski, Leonard A.; Carroll, Raymond J. (1985) | Covariate Measurement Error in Logistic Regression | 10.1214/aos/1176349741 | refs-of #13 (theme) | 1 | E: Measurement-error / regression-dilution analogue | NEW |
| 15 | HIGH — formal statistical treatment of aoristic models proper (Scandinavian J. Statistics); state-estimation framing supports "integrate over the interval" rather than sample one date | 2 | van Lieshout, Maria N. M.; Markwitz, Robin L. (2023) | State estimation for aoristic models | 10.1111/sjos.12619 | refs-of #4 | 1 | A: Aoristic/SPD pointwise-vs-mass critique | NEW |
| 16 | MEDIUM — interval-estimation (Poisson + Jeffreys) for date-uncertain counts; an apportionment-side, integrate-out treatment of artefact-over-time counts | 3 | Collins‐Elliott, S. A. (2019) | Quantifying artefacts over time: Interval estimation of a Poisson distribution using the Jeffreys prior | 10.1111/arcm.12481 | refs-of #4 | 1 | A: Aoristic/SPD pointwise-vs-mass critique | NEW |
| 17 | MEDIUM — establishes Monte-Carlo date-sampling as the significance-testing engine for SPDs; the "point-date MC" practice your paper interrogates is the operation defined here | 304 | Timpson, Adrian; Colledge, Sue; Crema, Enrico; Edinborough, Kevan; Kerig, Tim; Manning, Katie; Thomas, Mark G.; Shennan, Stephen (2014) | Reconstructing regional population fluctuations in the European Neolithic using radiocarbon dates: a new case-study using an improved method | 10.1016/j.jas.2014.08.011 | seed | 1 | A: Aoristic/SPD pointwise-vs-mass critique | [IN ZOTERO] |
| 18 | MEDIUM — review of probabilistic vs MC handling of radiocarbon in space-time; useful for positioning apportionment vs sampling in the SPD lineage | 97 | Crema, E.R.; Bevan, A.; Shennan, S. (2017) | Spatio-temporal approaches to archaeological radiocarbon dates | 10.1016/j.jas.2017.09.007 | seed | 1 | A: Aoristic/SPD pointwise-vs-mass critique | [IN ZOTERO] |
| 19 | MEDIUM — Baxter & Cool, user-named; shows aoristic/apportionment "reinvents" established density methods and discusses where MC simulation is and isn't needed | 16 | Baxter, M.J.; Cool, H.E.M. (2016) | Reinventing the wheel? Modelling temporal uncertainty with applications to brooch distributions in Roman Britain | 10.1016/j.jas.2015.12.007 | seed; refs-of #4 | 2 | A: Aoristic/SPD pointwise-vs-mass critique | [IN ZOTERO] |
| 20 | LOW-MEDIUM — applied aoristic/mass demonstration on intensive-survey finds; example of mass-apportionment in practice (the Antikythera case) | 30 | BEVAN, A.; CONOLLY, J.; HENNIG, C.; JOHNSTON, A.; QUERCIA, A.; SPENCER, L.; VROOM, J. (2013) | Measuring chronological uncertainty in intensive survey finds: a case study from Antikythera, Greece | 10.1111/j.1475-4754.2012.00674.x | refs-of #4 | 1 | A: Aoristic/SPD pointwise-vs-mass critique | [IN ZOTERO] |
| 21 | LOW-MEDIUM — modifiable-reporting-unit problem: aggregation/binning choices bias activity time-series; tangential support that *how* you spread mass matters | 22 | Bevan, A.; Crema, E. R. (2021) | Modifiable reporting unit problems and time series of long-term human activity | 10.1098/rstb.2019.0726 | cited-by #3 (theme) | 1 | A: Aoristic/SPD pointwise-vs-mass critique | [IN ZOTERO] |

## Proposer self-check

Re-queried 3 randomly chosen rows via fresh `metadata` calls: **Bray et al. 2015** (10.1080/10705511.2014.935265) → authors[0] "Bray, Bethany C.", year 2015, cites 208 — matches row 7. **Vermunt 2010** (10.1093/pan/mpq025) → authors[0] "Vermunt, Jeroen K.", year 2010, cites 1976 — matches row 8. **van Lieshout 2023** (10.1111/sjos.12619) → authors[0] "van Lieshout, Maria N. M.", year 2023, cites 2 — matches row 15. No mismatches; no rebuild needed.

Anomalies caught during Guard A (chain/memory vs metadata) and corrected in-table: Carleton "Sum things" is **2021** (chain listed 2020); van Lieshout is **2023** (chain listed 2021); Collins-Elliott is **2019** (chain listed 2016); Bevan Antikythera is **2013** (chain listed 2012); Blomberg & Todorov is **2025** (the 2024 hits were review/response artefacts, not the article of record). All Authors/Year/Cites in the table are taken verbatim from `metadata` JSON, not from chain output or memory.

Degraded-mode note: both MCP integrations were unavailable this run — `mcp__claude_ai_Scholar_Gateway__semanticSearch` and the Hugging Face tools all returned "No such tool available". I compensated per the corpus-bias mandate by running additional OpenAlex/CrossRef and Semantic Scholar queries via `lit-search.py` plus one WebSearch, so the two Scholar-Gateway seed searches were replaced by four extra keyword/chain searches. The corpus here is statistical and archaeological rather than ML-preprint, so loss of the HF tool has minimal impact; the loss of Scholar Gateway's full-text passage search is the real degradation and is the main reason I recommend the deeper-chaining go/no-go below.

## Landscape

Your empirical result sits at the intersection of two mature but **largely disconnected** literatures, plus two supporting framings.

**Archaeological dating (angle 1).** The field has an explicit, named debate about *point-wise* versus *probability-mass* handling of date-uncertain material. Crema 2012 introduced the two operations side by side: the "aoristic sum" (spread each item's unit mass across its interval) versus Monte-Carlo simulation (draw latent dates and aggregate). Roberts et al. 2012 independently formalised mass-apportionment for ceramic assemblages ("chronological apportioning"). Carleton & Groucutt 2021 ("Sum things are not what they seem") is the sharpest critique of treating aggregated-date proxies *pointwise* in downstream quantitative analysis — it is the paper that most nearly *names* your failure mode in archaeological vocabulary, though it targets SPD pointwise interpretation rather than a mixture share. Crema 2025 and van Lieshout & Markwitz 2023 push toward the integrate-out (Bayesian / state-estimation) treatment, which is the principled version of your mass-apportionment arm. What this literature does **not** contain (to my search) is a demonstration that point-date sampling *biases an estimated mixture-component proportion*, still less that the bias is driven by a *misclassified component indicator*. That is your novel cross.

**Three-step / classify-analyze plug-in bias (angle 3) — the general case, and it is very well documented.** This is the strongest match to your *mechanism*. Bolck, Croon & Hagenaars 2004 proved that the naive three-step procedure — (1) fit a latent/mixture model, (2) assign each unit a point estimate of its latent class, (3) plug those point assignments into a downstream model — yields **systematically attenuated** structural associations, and that the attenuation is a direct function of the **classification error** in step 2. Bakk et al. 2013 generalised this and showed the correction is to carry the misclassification (sensitivity/specificity) matrix forward rather than the hard labels; Bray, Lanza & Tan 2015 framed the same thing as the "classify-analyze" bias and showed the model-based ("inclusive") integrate-out alternative removes it; Bakk & Kuha 2021 review the whole strand. Map onto your problem: your "draw one latent date per item" is step 2's hard assignment; your downstream mixture fit is step 3; your indicator misclassification (θ_conv, θ_gen) is exactly the classification error that BCH show governs the bias; your mass-apportioned fit is the integrate-out correction. This is the literature that lets you say *the general case is documented* and cite a 1083-cite keystone plus a quantified, simulation-validated bias result.

**Single-imputation / plug-in vs integrate-out (angle 2).** Nielsen 2003 (proper vs improper imputation) and the Rubin tradition give the cleanest *principle*: a single stochastic draw of a latent value that ignores its predictive distribution is "improper" and produces inconsistent / mis-stated downstream inference, whereas propagating the full predictive distribution (≈ your mass apportionment, ≈ multiple imputation in the limit) is "proper". Blomberg & Todorov 2025 is a recent, readable "single imputation is a fallacy, integrate out instead" statement you can cite for the implication without a heavy theory burden.

**Measurement-error / regression-dilution (angle 4).** Hutcheon et al. 2010 and Stefanski & Carroll 1985 give the attenuation analogue: substituting a noisy surrogate for a latent quantity biases the estimate (classically toward the null), and the correction is to use the *conditional expectation* of the latent given the data (regression calibration) rather than a single noisy value. Your "use the mass over the interval, not a single draw" is the same move as "use E[latent|data], not a realisation".

## Thematic clusters

- **A — Aoristic / SPD pointwise-vs-mass critique** (members: #1, #2, #3, #4, #15, #16, #17, #18, #19, #20, #21 — 11 members, the densest cluster). The archaeological home of your contrast. Carleton & Groucutt 2021 + Roberts et al. 2012 + Crema 2012/2025 + van Lieshout 2023 are the load-bearing four.
- **C — Three-step / classify-analyze plug-in bias** (members: #5, #6, #7, #8, #9 — 5 members, dense and convergent). The statistical *mechanism* for your effect, with quantified bias and a named correction. The single most important cluster for "is the general case citeable" — answer: emphatically yes.
- **D — Mixtures under covariate/indicator misclassification** (member: #10 — 1 member, topical outlier but high-Fit). Xia, Hahn & Gustafson 2020 is the one paper that frames a misclassified categorical indicator *as a finite mixture* and recovers the structure by modelling the misclassification — almost a formal template for your two-component convention/genuine mixture with a noisy alignment indicator. Outlier status flags a thin but directly-on-point sub-literature; worth a forward chain (see gate).
- **B — Single-imputation / plug-in vs integrate-out** (members: #11, #12 — 2 members). The imputation-theory framing.
- **E — Measurement-error / regression-dilution analogue** (members: #13, #14 — 2 members). The attenuation analogue.

A paper appearing in only one chain but sitting in a dense cluster (e.g. #6, #7 in the 5-member cluster C) is still strongly validated by convergence; conversely #10 is a single-member cluster but high-Fit and deserves the forward chain.

## Suggested reading (tiered)

**Tier 1 — read first, these carry your argument:**
- Bolck, Croon & Hagenaars 2004 (10.1093/pan/mph001) — the general-case proof that plug-in of misclassified latent assignments attenuates the downstream estimate. *This is your "named/documented general phenomenon".*
- Carleton & Groucutt 2021 (10.1177/0959683620981700) — the archaeological-vocabulary statement of the pointwise problem.
- Bakk et al. 2013 (10.1177/0081175012470644) — quantifies the bias and shows the misclassification-matrix correction; ties bias to classification error specifically.
- Roberts et al. 2012 (10.1016/j.jas.2011.12.022) — the named mass-apportionment method.

**Tier 2 — frame the implication / the fix:**
- Bray, Lanza & Tan 2015 (10.1080/10705511.2014.935265) — classify-analyze bias and the integrate-out cure.
- Crema 2025 (10.1111/arcm.12984) and van Lieshout & Markwitz 2023 (10.1111/sjos.12619) — integrate-out aoristic.
- Nielsen 2003 (10.1111/j.1751-5823.2003.tb00214.x) — proper vs improper imputation principle.
- Xia, Hahn & Gustafson 2020 (10.1002/cjs.11560) — misclassified indicator as a mixture.

**Tier 3 — analogues and breadth:**
- Hutcheon et al. 2010 (10.1136/bmj.c2289), Stefanski & Carroll 1985 (10.1214/aos/1176349741) — regression-dilution / conditional-expectation correction.
- Blomberg & Todorov 2025 (10.1111/2041-210x.14494), Bakk & Kuha 2021 (10.1111/bmsp.12227), Vermunt 2010 (10.1093/pan/mpq025) — accessible review/framing.

## Gaps noticed

1. **No paper joins the two literatures around a cross-classified deconvolution mixture with a noisy class indicator.** The archaeological dating strand (cluster A) treats date uncertainty but does not study an *estimated mixture share*; the three-step strand (cluster C) studies the plug-in mixture-share bias but with no temporal/interval-width component and no Monte-Carlo date sampling. Your result is, on this search, the bridge — which is good news for novelty and means you should cite *both* halves explicitly rather than expecting a single prior source.
2. **"Driven by misclassification, not interval width" is exactly the BCH/Bakk decomposition, but nobody states it in the aoristic context.** You can claim that contribution; cluster C supports the *general* claim, cluster A supports the *archaeological* setting, but the conjunction is yours.
3. **The direction of your collapse (α 0.68 → 0.10, a strong collapse, not mild attenuation) may exceed the classical "attenuation toward the null" intuition.** Worth checking whether the BCH/Bakk simulations report collapses of comparable magnitude under high asymmetric misclassification (θ_conv 0.93 vs θ_gen 0.025 is very asymmetric); a forward chain on Bakk 2013 / Xia 2020 may locate a magnitude-matching simulation. Flagged in the gate below.
4. **I could not surface a paper that uses the precise phrase "mass apportionment vs point-date Monte Carlo" as a named dichotomy** — so there is no ready-made name to borrow. You may want to coin one and anchor it to Roberts 2012 (apportionment) + Carleton 2021 (pointwise) + BCH 2004 (plug-in bias).

## Venue analysis

No target venues named by the user. Observation for free: the high-Fit statistical keystones sit in *Political Analysis*, *Sociological Methodology*, *Structural Equation Modeling*, *International Statistical Review*, and *Canadian J. Statistics* — cross-disciplinary methods venues. The archaeological strand sits in *JAS*, *Archaeometry*, *J. Archaeological Method & Theory*, *The Holocene*, and *Scandinavian J. Statistics* (the van Lieshout state-estimation paper). If you target a methods-forward archaeology venue (*JAS*, *J. Computer Applications in Archaeology*, *J. Archaeological Method & Theory*), citing across both pools signals you have located the general statistical result rather than reinventing it — which is itself the Baxter & Cool 2016 cautionary point.

## Zotero actions

For papers marked NEW, recommend staging via the canonical pipeline (`/lit-scout-iterate` → `lit-scout-zotero-import.py --live`):

- 10.1016/j.jas.2011.12.022 — Roberts et al. 2012, chronological apportioning (Tier 1)
- 10.1093/pan/mph001 — Bolck, Croon & Hagenaars 2004 (Tier 1)
- 10.1177/0081175012470644 — Bakk, Tekle & Vermunt 2013 (Tier 1)
- 10.1080/10705511.2014.935265 — Bray, Lanza & Tan 2015 (Tier 2)
- 10.1093/pan/mpq025 — Vermunt 2010 (Tier 3)
- 10.1111/bmsp.12227 — Bakk & Kuha 2021 (Tier 3)
- 10.1002/cjs.11560 — Xia, Hahn & Gustafson 2020 (Tier 2)
- 10.1111/j.1751-5823.2003.tb00214.x — Nielsen 2003 (Tier 2)
- 10.1136/bmj.c2289 — Hutcheon et al. 2010 (Tier 3)
- 10.1111/2041-210x.14494 — Blomberg & Todorov 2025 (Tier 3)
- 10.1214/aos/1176349741 — Stefanski & Carroll 1985 (Tier 3)
- 10.1111/sjos.12619 — van Lieshout & Markwitz 2023 (Tier 2)
- 10.1111/arcm.12481 — Collins-Elliott 2019 (Tier 3)

Already held (no action): Crema 2012, Crema 2025, Baxter & Cool 2016, Carleton & Groucutt 2021, Timpson et al. 2014, Crema/Bevan/Shennan 2017, Bevan et al. 2013, Bevan & Crema 2021. Note: Crema 2012 and Baxter & Cool appear in multiple libraries (TRAP, SDAM-AU); the importer dedups by DOI so no duplication risk.

## Deeper chaining candidates

```text
DEEPER CHAINING CANDIDATES (go/no-go required):

1. FORWARD L2: Chase citations of Bakk, Tekle & Vermunt 2013 (10.1177/0081175012470644)
   — RATIONALE: cluster C is your strongest "general case" evidence; a forward chain may
   locate a simulation reporting an ASYMMETRIC-misclassification collapse of magnitude
   comparable to your α 0.68 → 0.10 (addresses Gap 3). High value, moderate explosion risk
   (capped at top 20 by cites).

2. FORWARD L1→L2: Chase citations of Xia, Hahn & Gustafson 2020 (10.1002/cjs.11560)
   — RATIONALE: cluster D is a 1-member outlier; this is the paper closest to "misclassified
   indicator AS a mixture". A forward chain (it has only 3 cites, so cheap) may reveal whether
   anyone has extended the misclassified-covariate-mixture idea, possibly toward your exact
   two-component setup. Low explosion risk, potentially high payoff for novelty-positioning.

3. BACKWARD L3: Chase references of Carleton & Groucutt 2021 (10.1177/0959683620981700)
   — RATIONALE: the pointwise-critique paper likely cites the specific simulation/MC-sampling
   methods papers that formalise the bias you observed in the SPD setting; may surface a
   archaeology-side citation bridging to the apportionment fix. Moderate value.

4. SKIP: forward chain on Crema 2012 / Timpson 2014 — already sampled (Phase 3); the
   citing literature is overwhelmingly demographic APPLICATIONS (population boom-bust),
   not methodological bias work. Would dilute with low-Fit results.

5. SKIP: backward chain on Bolck-Croon-Hagenaars 2004 — pre-2004 latent-structure
   theory; would lead to general LCA/EM foundations rather than the misclassification-bias
   specifics you need.
```

Recommendation: **go on 1 and 2** (both directly target the two open gaps — magnitude-matching and novelty-positioning — and 2 is cheap), **hold/optional on 3**, **skip 4 and 5**. Awaiting your go/no-go before proceeding past the gate.

## Machine-readable claims (for orchestrator extraction)

<!-- BEGIN claims.jsonl -->
```jsonl
{"claim_id":"10.1177-0959683620981700-doi","doi":"10.1177/0959683620981700","authors":"Carleton, W. Christopher; Groucutt, Huw S.","year":2021,"citation_count":60}
{"claim_id":"10.1016-j.jas.2011.12.022-doi","doi":"10.1016/j.jas.2011.12.022","authors":"Roberts, John M.; Mills, Barbara J.; Clark, Jeffery J.; Haas, W. Randall; Huntley, Deborah L.; Trowbridge, Meaghan A.","year":2012,"citation_count":34}
{"claim_id":"10.1007-s10816-011-9122-3-doi","doi":"10.1007/s10816-011-9122-3","authors":"Crema, Enrico R.","year":2012,"citation_count":99}
{"claim_id":"10.1111-arcm.12984-doi","doi":"10.1111/arcm.12984","authors":"Crema, Enrico R.","year":2025,"citation_count":7}
{"claim_id":"10.1093-pan-mph001-doi","doi":"10.1093/pan/mph001","authors":"Bolck, Annabel; Croon, Marcel; Hagenaars, Jacques","year":2004,"citation_count":1083}
{"claim_id":"10.1177-0081175012470644-doi","doi":"10.1177/0081175012470644","authors":"Bakk, Zsuzsa; Tekle, Fetene B.; Vermunt, Jeroen K.","year":2013,"citation_count":507}
{"claim_id":"10.1080-10705511.2014.935265-doi","doi":"10.1080/10705511.2014.935265","authors":"Bray, Bethany C.; Lanza, Stephanie T.; Tan, Xianming","year":2015,"citation_count":208}
{"claim_id":"10.1093-pan-mpq025-doi","doi":"10.1093/pan/mpq025","authors":"Vermunt, Jeroen K.","year":2010,"citation_count":1976}
{"claim_id":"10.1111-bmsp.12227-doi","doi":"10.1111/bmsp.12227","authors":"Bakk, Zsuzsa; Kuha, Jouni","year":2021,"citation_count":121}
{"claim_id":"10.1002-cjs.11560-doi","doi":"10.1002/cjs.11560","authors":"Xia, Michelle; Richard Hahn, P.; Gustafson, Paul","year":2020,"citation_count":3}
{"claim_id":"10.1111-j.1751-5823.2003.tb00214.x-doi","doi":"10.1111/j.1751-5823.2003.tb00214.x","authors":"Nielsen, Søren Feodor","year":2003,"citation_count":70}
{"claim_id":"10.1111-2041-210x.14494-doi","doi":"10.1111/2041-210x.14494","authors":"Blomberg, Simone P.; Todorov, Orlin S.","year":2025,"citation_count":7}
{"claim_id":"10.1136-bmj.c2289-doi","doi":"10.1136/bmj.c2289","authors":"Hutcheon, J. A.; Chiolero, A.; Hanley, J. A.","year":2010,"citation_count":626}
{"claim_id":"10.1214-aos-1176349741-doi","doi":"10.1214/aos/1176349741","authors":"Stefanski, Leonard A.; Carroll, Raymond J.","year":1985,"citation_count":192}
{"claim_id":"10.1111-sjos.12619-doi","doi":"10.1111/sjos.12619","authors":"van Lieshout, Maria N. M.; Markwitz, Robin L.","year":2023,"citation_count":2}
{"claim_id":"10.1111-arcm.12481-doi","doi":"10.1111/arcm.12481","authors":"Collins‐Elliott, S. A.","year":2019,"citation_count":3}
{"claim_id":"10.1016-j.jas.2014.08.011-doi","doi":"10.1016/j.jas.2014.08.011","authors":"Timpson, Adrian; Colledge, Sue; Crema, Enrico; Edinborough, Kevan; Kerig, Tim; Manning, Katie; Thomas, Mark G.; Shennan, Stephen","year":2014,"citation_count":304}
{"claim_id":"10.1016-j.jas.2017.09.007-doi","doi":"10.1016/j.jas.2017.09.007","authors":"Crema, E.R.; Bevan, A.; Shennan, S.","year":2017,"citation_count":97}
{"claim_id":"10.1016-j.jas.2015.12.007-doi","doi":"10.1016/j.jas.2015.12.007","authors":"Baxter, M.J.; Cool, H.E.M.","year":2016,"citation_count":16}
{"claim_id":"10.1111-j.1475-4754.2012.00674.x-doi","doi":"10.1111/j.1475-4754.2012.00674.x","authors":"BEVAN, A.; CONOLLY, J.; HENNIG, C.; JOHNSTON, A.; QUERCIA, A.; SPENCER, L.; VROOM, J.","year":2013,"citation_count":30}
{"claim_id":"10.1098-rstb.2019.0726-doi","doi":"10.1098/rstb.2019.0726","authors":"Bevan, A.; Crema, E. R.","year":2021,"citation_count":22}
```
<!-- END claims.jsonl -->

---

**Direct answer to your headline question:** Yes — the general case is documented well enough to cite, but it lives under two different names in two different fields, and the conjunction (your specific cross-classified time×alignment deconvolution) is novel. Cite the **three-step / classify-analyze plug-in bias** (Bolck, Croon & Hagenaars 2004; Bakk et al. 2013; Bray et al. 2015) for the *mechanism* — plug-in of a misclassified latent assignment systematically attenuates the downstream estimate, with the bias governed by classification error, exactly your θ_conv/θ_gen story — and the **aoristic pointwise-vs-mass critique** (Carleton & Groucutt 2021; Roberts et al. 2012; Crema 2012/2025) for the *archaeological setting*. The imputation framing (Nielsen 2003) and regression-dilution analogue (Hutcheon et al. 2010; Stefanski & Carroll 1985) explain *why* mass apportionment recovers α: it is the integrate-out / conditional-expectation correction, while a single date draw is the improper single-imputation / noisy-surrogate plug-in.
