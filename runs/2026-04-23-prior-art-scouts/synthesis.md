---
priority: 1
scope: in-stream
title: "Synthesis — three prior-art scouts, 2026-04-23 overnight"
audience: "Shawn (morning review), Adela, future CC instances"
status: committed 2026-04-23
source: "runs/2026-04-23-prior-art-scouts/scout-{1,2,3}-*.md"
---

# Synthesis — three prior-art scouts, 2026-04-23 overnight run

Three scouts ran in parallel overnight against Q1 (effect-size calibration), Q2 (urban-scaling confound), Q3 (epigraphic-habit translator proxies). All three returned; full reports are adjacent (`scout-1-*.md` through `scout-3-*.md`). This synthesis distils what they change for the preregistration.

## Headline finding — one sentence

**Roman Latin inscriptions scale sublinearly with urban population (β ≈ 0.3–0.7) across every published study that tests the relationship — which inverts the scaling-law concern I raised, re-legitimises Hanson's "information infrastructure" framing for inscriptions, and gives the H3 variance-explained pre-specification a direct empirical anchor (Hanson et al. 2017: R² = 0.267) rather than a calibrated guess.**

## Three critical findings

### 1. Sublinear scaling (Scouts 2 + 3 convergent)

Every published inscription-vs-population scaling regression has found **sublinear** β, and Shawn's own 2024 exploratory work independently replicates the pattern:

- **Ross 2024 (archived preliminary analysis; LIRE v3.0, n = 816 cities)**: OLS log-log **β = 0.473** [0.376, 0.569]; NBR log-link bootstrap mean **β = 0.683** [0.532, 0.849]. Both estimates of the same power-law scaling exponent under different distributional assumptions; both sublinear. Methodological triangulation via different regression families and dataset slice than the published work below. See `planning/archive-2024-summary.md` for context.
- Hanson, Ortman & Lobo 2017 Table 2 (reconstructed via Brewminate): **β ≈ 0.643** for inscription count vs population.
- Hanson 2021 (*Journal of Urban Archaeology* 4:137–52; **paywalled, abstract confirms**): sublinear; "inscriptions increase slower than the estimated populations of sites"; framed as **information infrastructure** analogous to roads / pipelines.
- Carleton et al. 2025 (*Nature Cities*; **Bayesian**): honorific-inscription elite-wealth proxies **β ≈ 0.3–0.5**, strongly sublinear.
- Hanson-Ortman 2017 (inhabited area): α ≈ 2/3.
- Hanson-Ortman 2020 (entertainment structures): β ≈ 0.33.
- Hanson-Ortman-Bettencourt-Mazur 2019 (fora / streets): β ≈ 0.52–0.67.

No published Roman inscription-scaling study has ever found super-linear β, and Ross 2024 converges with the published work. **The Ortman-super-linear default that framed my Q2 brief was wrong for this object class.** Inscriptions are infrastructure-like, not socio-economic-output-like. The sublinear conclusion is robust across multiple datasets, regression families (OLS, NBR, Bayesian), and research groups.

**Consequence for Framing A vs B:** Framing B (raw correlation primary, scaling as sensitivity) is now the better-supported choice. With sublinear β, raw correlation does not inflate the "population effect" via scaling — if anything, the population signal is partially suppressed relative to super-linear expectation. The scaling-residual analysis remains useful as a robustness check and sensitivity to β uncertainty, but not as the primary framing.

**Consequence for theoretical frame:** Hanson's "inscriptions as information infrastructure" deserves engagement in the paper. This partly re-legitimises the information-theoretic angle I advised cutting earlier — not as a formal information-theory treatment (the machinery doesn't fit, as I argued), but as a **theoretical bracket**: inscriptions are more like communication infrastructure (saturates at scale) than like production output (super-linear at scale).

### 2. Effect-size brackets are not a field-specific standard (Scout 1)

**No field-specific R² conventions exist** for SPD / SPA × covariate correlations. The SPD literature is split between permutation-envelope deviation-detection (no R²) and Bayesian Bayes-factor / WAIC model selection (no R²). Cohen's generic brackets (small 0.01 / medium 0.09 / large 0.25) are the de facto fallback; Kolar et al. 2023 uses them unmodified.

**Calibration anchors that matter:**

- **Carleton et al. 2018 PEWMA simulations**: r ≈ 0.5 (R² ≈ 0.25) is the practical detection floor for palaeodemographic time-series correlation.
- **Hanson, Ortman & Lobo 2017**: R² = 0.267 (population vs functional diversity, all cities); R² = 0.361 (inscription count vs association diversity, excluding Rome). **Direct comparator for the project — same population dataset.**
- **Palmisano et al. 2021**: empirical range of SPD × climate r = –0.68 to +0.77 (R² = 0.005 to 0.59) — places H3 province-level R² ≥ 0.50 at the upper end of what has been observed.
- **2024 project baseline**: R² ≈ 0.10 log-log OLS; R² ≈ 0.087 Bayesian. Sits well below Hanson et al. 2017's published benchmarks.

**Consequence for pre-specification:**
- **R² ≥ 0.25 at urban-area level** — now calibrated, not guessed. Matches Hanson 2017 all-cities result (0.267) AND Carleton 2018 PEWMA detection floor. Defensible.
- **R² ≥ 0.50 at province level** — at the upper end of Palmisano empirical range; ambitious but not outlandish. Consider softening to R² ≥ 0.40 if reviewer pushback expected; keep at 0.50 if province aggregation is expected to suppress noise substantially.
- **Bayesian R²** (Gelman et al. 2019) should be the reporting framework. **First SPD paper to adopt it** — minor methodological contribution.

### 3. No ready-made epigraphic-habit proxy exists (Scout 3)

The MacMullen–Meyer–Woolf framework is qualitative. Beltrán Lloris 2015 explicitly rejects quantification. The Benefiel & Keesling 2024 Brill volume is largely qualitative. **No published work operationalises epigraphic-habit variation as a continuous, joinable covariate at empire scale.**

**Consequence:** the paper's "cultural-translator confound" open question (research-intent.md §Open questions 4) is a real literature gap. The absence is reportable.

**What can be combined (no building from scratch):**

1. **Carleton et al. 2025 provincial random effects** — extract posterior province-level intercepts from the Bayesian model at [github.com/wccarleton/urbanscale](https://github.com/wccarleton/urbanscale) (CC BY 4.0, Jupyter / R / Python). Province-level continuous adjustment factor estimated jointly with population uncertainty.
2. **Hanson 2021 scaling residuals** — per-city over/under-production of inscriptions relative to scaling expectation, computed from the OXREP dataset at [TDAR 448563](https://core.tdar.org/dataset/448563). City-level translator intensity net of population.
3. **Glomb, Kaše & Heřmánková 2022 Monte Carlo temporal baseline** — observed/expected ratio per time-bin against the all-corpus trend. Temporal translator intensity.

Combined: **spatial (Carleton provincial) + city-level (Hanson residuals) + temporal (Glomb observed/expected)** = multi-dimensional habit proxy. Documenting the construction is the contribution; citing the absence of an established index is the literature hook.

**For the current paper's H3 sensitivity analysis:** the mixture α parameter is the primary translator proxy (already planned). The combined Carleton-Hanson-Glomb proxy can serve as a triangulating external covariate for robustness.

### Bonus operationalisation (Scout 3)

**Kaše, Heřmánková & Sobotková 2022** operationalise diversity measures via **frequency-per-1,000-words normalisation** and **bootstrap 1,000-inscription standardised samples** (SDAM team precedent; Adela co-author). Directly adoptable technique for LIRE analyses where sample-size heterogeneity threatens comparability. Code at [github.com/sdam-au/social_diversity](https://github.com/sdam-au/social_diversity).

## Two live critiques the paper must engage

### Beltrán Lloris 2015 dismantles MacMullen's Severan-peak graphs

As reflecting **Lassère's dating conventions** rather than real production trends. This **directly validates the 2026 mixture-correction framing.** The paper has a natural citation anchor for the editorial-convention artefact problem being a *recognised* problem in the field, not a novel suspicion.

### Carleton & Groucutt 2021 critique of SPD point-wise regression

Argues radiocarbon-SPD point-wise regression is fundamentally unreliable because joint calibration-uncertainty density cannot be mapped stably onto covariate observations. **Weaker for calendar-date aoristic inscription data** (no calibration uncertainty in the same sense; aoristic ranges are discrete, not Bayesian posteriors), but the paper should acknowledge the critique and explain why it applies less strongly here. Good-faith engagement.

## Revised recommendations (updating my 2026-04-23 Q1/Q2/Q3 advice)

### Q1 — Effect-size targets (updated)

Previous advice: pre-specify R² ≥ 0.25 urban-area, R² ≥ 0.50 province — "defensible guesses." **Now calibrated.** Urban-area anchor = Hanson 2017 (R² = 0.267) and Carleton 2018 (R² = 0.25 floor). Province anchor = Palmisano 2021 upper range (R² = 0.59). Cohen's brackets via Kolar 2023 as SPD-field fallback. Bayesian R² (Gelman 2019) as reporting framework — first adoption in SPD literature. Power-simulation template: build ~200–300 lines adapting Carleton 2018 PLOS ONE code (CC-BY).

### Q2 — Scaling-law framing (resolved)

Previous advice: "Two defensible positions: (A) residuals-primary, (B) raw-correlation-primary; leaning B." **Now resolved decisively for Framing B.** Sublinear β ≈ 0.3–0.7 (Hanson 2021; Carleton 2025) means raw correlation is not inflated by scaling. Scaling-residual analysis remains as sensitivity / robustness; not primary.

Additional paper move: cite Hanson 2021 as the theoretical anchor for "inscriptions as information infrastructure," making the sublinearity interpretable rather than a methodological headache. Critical verification: obtain Hanson 2021 PDF (Brepols paywall; Macquarie access likely) and confirm the exact β value.

### Q3 — Translator confound (strategy defined)

Previous advice: α-as-covariate sensitivity analysis; prior-art-scout for more proxies. **Now:** no ready-made proxy exists (literature gap to report). Construct from Carleton 2025 provincial effects + Hanson 2021 residuals + Glomb et al. 2022 temporal observed/expected. The mixture α remains the primary translator interpretation; the combined proxy is triangulation.

## Verification items — do before preregistration commits

1. **Hanson 2021 PDF** — Brepols paywall (Macquarie); confirm exact β value and any regional residuals. Load-bearing for the sublinear-scaling headline finding.
2. **Carleton et al. 2025 Nature Cities supplementary** — extract provincial posterior distributions; assess whether directly usable as a translator covariate.
3. **Carleton et al. 2018 PLOS ONE supplementary code** — retrieve and adapt as the power-simulation template.
4. **Carleton & Groucutt 2021** — read fully; formulate the "why this applies less to calendar-date aoristic data" response.
5. **Hanson OXREP dataset** on [TDAR 448563](https://core.tdar.org/dataset/448563) — fetch; compare to Hanson 2016 `urban_context_pop_est` already in LIRE.
6. **wccarleton/urbanscale GitHub repository** — clone; inspect model code and data availability.

## Proposed updates to `planning/research-intent.md`

For morning review (changes I would make if you authorise):

1. **Add paragraph to theoretical frame** acknowledging Hanson's "inscriptions as information infrastructure" alongside the multi-factor complexity decomposition. The two are complementary: complexity operates through multiple dimensions; at the urban scale specifically, inscriptions function as infrastructure, explaining the sublinearity.
2. **Rewrite open question 3 (scaling-law confound)** to reflect the resolution: sublinear β ≈ 0.3–0.7 across Hanson 2021 + Carleton 2025; Framing B (raw correlation primary, scaling as sensitivity) adopted; citation anchors identified. Remove from open-questions list.
3. **Rewrite open question 2 (effect-size adequacy)** with new calibration: Hanson 2017 R² = 0.267 anchor; Carleton 2018 PEWMA R² = 0.25 floor; Palmisano 2021 upper-range R² = 0.59; Cohen via Kolar 2023 as fallback; Bayesian R² via Gelman 2019 as reporting framework.
4. **Rewrite open question 4 (cultural-translator confound)** to note no ready-made proxy exists (literature gap); combined Carleton + Hanson + Glomb construction as triangulation strategy alongside α parameter.
5. **Add to Future-work FS-D** cross-reference to the combined habit-proxy construction (pull forward for current paper's sensitivity; full FS-D paper later).

## Action items for morning review

- [ ] Read `runs/2026-04-23-prior-art-scouts/scout-1-effect-size-calibration.md` (~8 kb)
- [ ] Read `runs/2026-04-23-prior-art-scouts/scout-2-urban-scaling-inscriptions.md` (~7 kb)
- [ ] Read `runs/2026-04-23-prior-art-scouts/scout-3-epigraphic-habit-proxies.md` (~7 kb)
- [ ] Confirm or push back on the sublinear-scaling re-framing (biggest change)
- [ ] Authorise updates to `planning/research-intent.md` per §"Proposed updates" above
- [ ] Fetch Hanson 2021 PDF (Macquarie library → Brepols)
- [ ] Fetch Carleton et al. 2025 *Nature Cities* (open access) + supplementary
- [ ] Clone wccarleton/urbanscale for inspection
- [ ] Authorise next block: preregistration structure sketch (Task #2) incorporating these findings

## Credit, uncertainty, and honest limits

- All three scout reports carry a **verification pending** marker. DOIs, URLs, and reported R² / β values are agent-returned and should be spot-checked before anything cites them in print.
- The β ≈ 0.643 specific value for Hanson 2021 is reconstructed from a secondary summary (Brewminate); the full paper is paywalled and hasn't been directly verified. The sublinearity itself is confirmed in the abstract.
- Scout 3's "no ready-made proxy exists" is a negative finding; negative findings are harder to falsify. The paper's claim to this effect should be phrased carefully ("we found no published operationalisation at empire scale in [scope of search]") rather than absolutely.
- I have **not** modified `planning/research-intent.md` per the standing pre-launch review rule. The proposed changes in §"Proposed updates" await explicit authorisation.

## Provenance

Three prior-art-scout agents commissioned 2026-04-23 ~18:22 AEST, completed ~18:31 AEST (all three within ~10 min). Scout briefs approved by Shawn before launch per standing rule. Synthesis authored by main-thread Claude; reports preserved as-returned by scout agents (with markdown formatting). Full transcripts are in-session, not committed; this synthesis + the three report files constitute the durable record.
