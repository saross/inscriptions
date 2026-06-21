# JAMT paper — paper-wide outline

**Status:** OUTLINE for discussion → drafting. Built 2026-06-21 with Shawn.
**Governing brief:** `planning/paper-writing-brief.md` (LOCKED 2026-06-20).
**On-ramp / results narrative:** `reports/key-findings-summary-2026-06-20.md`.
**Figures:** `runs/2026-06-20-figures/outputs/` (F1–F19 + W1); index `figindex.md`,
plain-language captions `figure-captions.md`.
**Style exemplar to match:** Eftimoski, Ross & Sobotkova 2017 (Zotero `ENPYIZQF`) —
re-read before drafting the methods.

> **Three structural decisions locked with Shawn 2026-06-21:**
> 1. **Balanced two-act structure** — Act I (the instrument: method + validation +
>    reachability envelope) and Act II (what it reveals: substantive findings), at
>    roughly equal weight.
> 2. **The wives-and-daughters case study sits in Act II as the *thematic*
>    (non-city/province) subsetting example** — contrasting the *geographic*
>    (province/city/capital) subsetting that carries the rest of Act II. This gives
>    Act II a single organising principle: **what de-fogging reveals when you point
>    it at a coherent subset**, geographic first, then thematic.
> 3. **The population–epigraphy comparison must feature prominently in Act II**
>    (Shawn 2026-06-21) — it is the **headline substantive result**, not one finding
>    among several. It leads Act II (§5), is the marquee Act II figure (F7), and is
>    foregrounded in the Act II opener, the Introduction contribution preview, the
>    Abstract, and the Discussion. The temporal, content, Rome/Italia, and women
>    sections support and extend it; they do not crowd it.

> **Anti-confabulation note.** Every number below is a pointer to its source
> (Observation register `docs/notes/working-notes.md`, run REPORTs, or the figure
> index), re-read at source for the key-findings summary on 2026-06-20. Re-verify
> each at the source file when it lands in actual draft prose, per the standing rule.

---

## 0. Front matter

- **Working title (placeholder — Shawn's call):** *"De-fogging editorial convention
  from Roman inscription dates: a Bayesian deconvolution instrument and what it
  reveals about urban epigraphy."* Alternatives to weigh at drafting: lead with the
  method ("A Bayesian deconvolution for editorial-convention dating in epigraphic
  corpora") vs lead with the dual contribution (above).
- **Authors (TBD — confirm):** Ross (lead); Sobotkova (co-author; leads the
  thematic case study, §11); statistician acknowledgement / co-authorship for
  Eftimoski per his draft-stage read (Martin recalibration, continuity). Confirm
  the author list and order with Shawn before drafting front matter.
- **Abstract** (~250 words) — write last. Must carry, in plain English: the
  convention-contamination problem; the deconvolution instrument + its validated
  reachability envelope as the headline *method* contribution; and — as the headline
  *substantive* result — the **population–epigraphy comparison** (within-province
  sublinear scaling, capitals over-producing), then the near-equal three-tier
  temporal decomposition and the diagnostic case study. Give the population finding a
  full sentence of its own; do not let it be a clause in a list.
- **Keywords:** epigraphic habit; aoristic dating; summed probability
  distributions; Bayesian deconvolution; Roman urbanism; settlement scaling;
  source criticism. (Finalise against JAMT keyword conventions.)

---

## 1. Introduction (~1,300 words)

**Goal:** state the problem, the gap, and the two-act contribution; promise
empirical-first; set the open-science frame. Plain English throughout.

- **The problem, in plain terms.** Many Roman inscriptions are not dated to a real
  moment but assigned a round-number *date slab* by editorial convention ("AD
  1–100", a half-century box). This dumps artificial probability mass on round
  years and century boundaries, so the *apparent* epigraphic chronology is partly a
  cataloguing artefact. Make it concrete with the round-25-year-slab fact (68 % of
  some corpora) and a one-line preview of the empire headline (≈ two-thirds
  convention).
- **The gap.** Archaeology's summed-probability / aoristic toolkit (cite Crema,
  Bevan; Carleton & Groucutt 2021; Roberts 2012) models *dating uncertainty* but
  does **not** target *editorial convention* specifically. Define SPD and aoristic
  here, in plain English, on first use. The convention artefact is the unaddressed
  problem this paper solves.
- **The contribution (two-act preview).**
  - *Act I:* a Bayesian deconvolution-mixture **instrument** that separates the
    convention artefact from the genuine date signal, recovery-validated, and — the
    deliverable that makes it usable — shipped with a **reachability envelope** (a
    validated rule for when it works).
  - *Act II:* what the instrument reveals when applied to coherent subsets of the
    corpus. The **headline result is the population–epigraphy comparison** — how
    inscription output scales with city population (sublinear, within-province, with
    capitals over-producing) — demonstrated **geographically** (provinces, cities,
    capitals), then extended by the temporal decomposition, the content axis, the
    Rome/Italia comparison, and **thematically** (a real demographic corpus, as a
    diagnostic). Name the population finding here, in the contribution preview.
- **Empirical-first promise + open science.** State that results are presented
  before interpretation (Obs 101), that the analysis is preregistered (OSF
  `https://osf.io/uycs6/`) with four amendments, and that the corpus is LIRE v3.0
  (182,853 inscriptions × 63 columns; `runs/2026-04-23-descriptive-stats/outputs/
  summary.md`). Fold the brief materials note (analytical units: **Latin-minus-Roma
  primary**, empire-wide as context; Amendment 02 / Decision 36) in here rather than
  a standalone Materials section.

*No figure (or a small schematic of the round-slab problem if one is wanted — not
yet built).*

---

# ACT I — THE INSTRUMENT

## 2. The method, in concept (~1,400 words)

**Goal:** make a non-statistician understand *what the deconvolution does and why*,
with the maths alongside (not instead). Full derivation → Supplement S1.

- **Aoristic foundation.** Each inscription's date range spread as probability mass;
  summed across a unit = the raw SPD. Plain-English first.
- **The mixture idea.** `p_mix = α·p_conv + (1 − α)·p_gen`: each unit's dated record
  is a mixture of a **convention** component (round-slab mass, `p_conv`) and a
  **genuine** component (`p_gen`). **α is the convention fraction** (1 − α =
  genuine; higher α = more editorial dating) — state this once, unambiguously, and
  early (the inversion that bit the draft summary; Obs 116). The mechanism: **θ**,
  the rate at which a unit's dates "snap to" round slabs.
- **The production likelihood, in concept.** The cross-classified ("library")
  likelihood — a fixed round-endpoint slab library shared across units, with
  per-unit genuine shape — adopted after an earlier shared-basis design was shown to
  add spurious upward bias. Derivation, the concomitant-variable-mixture grounding
  (Feller 2016; Gustafson 2010; Huang & Bandeen-Roche 2004; Bronk Ramsey 2009), and
  the θ priors → **Supplement S1**.
- **Hierarchical partial pooling** — define in one plain sentence (units borrow
  strength from each other); detail → supplement.
- **Bayesian glosses** — define *posterior* and *95 % credible interval* in plain
  English on first use (reuse the key-findings §1 wording).

**Figure:** **F1** (empire deconvolution before/after hero; convention component
highlighted — framed as convention *removal* + peak *recovery*, NOT "smoothing").

---

## 3. Does it recover the truth? Validation (~900 words)

**Goal:** convince the reader (and the Crema/Bevan reviewer) the instrument works,
*in concept* — technical grids → Supplement S2.

- **Recovery simulation.** Plant a known convention fraction, see if the model gets
  it back: 300 parameter cells × 100 repeats, passed all four pre-set adoption
  criteria, mean absolute error ≈ 0.021 (~2 percentage points), no harm to cases it
  should leave alone (Obs 89, `cc-VERDICT-library.md`). State the result plainly;
  the grid, θ re-derivation + sweep, and convergence diagnostics → **Supplement S2**.
- **External anchors (the convincing, non-technical check).** **Pompeii**: genuine
  mass collapses to ~0 after AD 79 — the sealed-site external validation (the
  model was not told about Vesuvius). **Ostia**: de-fogged apogee AD 125–150,
  matching the historical record. (Obs 102; `key-findings` §1, §6.)

**Figure:** **F4** (five anchor cities; Pompeii AD 79 external check). Recovery-grid
figures (the simulation detail) → supplement.

---

## 4. Honest limits as a deliverable — the reachability envelope (~800 words)

**Goal:** present the envelope as a *contribution*, not a caveat — the instrument's
spec sheet, which is what makes it reusable.

- **The spec sheet.** A validated rule for *when* de-fogging works: recovers the
  genuine trajectory from N ≈ 500 for the easiest subsets, rising to a worst-case
  floor of N ≈ 2,000 inside the operating envelope (convention fraction
  α ≤ ~0.70), unreliable above that (`paper-significance-and-applications-
  2026-06-03.md`; Decision 34: subsets get their own fit, not the empire shape).
- **First demonstration / sanity result.** The empire-pooled estimate:
  **α = 0.6798 [0.6649, 0.6970]** — roughly **two-thirds** of empire-wide dated
  inscriptions are editorial round-slab convention, only a third genuine (Obs 111);
  Latin-pooled α = 0.7387 [0.6596, 0.7893]. This is the motivating number, but the
  *point is the instrument*, not the number — say so.

**Figure:** **F12** (N × α reachability heatmap + operating envelope). Optionally
**F2** (empire + Latin SPD raw vs genuine) here as the first "what de-fogging does
to a real curve" exhibit, or hold F2 for Act II.

---

# ACT II — WHAT IT REVEALS (subsetting the corpus)

*Act II opener (~150 words): the instrument is subset-agnostic. We demonstrate it on
coherent subsets — first **geographic** (provinces, cities, capitals), then
**thematic** (a demographic corpus). **Foreground the headline:** the central
substantive result of the paper is the **population–epigraphy comparison** (§5) —
state up front that Act II leads with it, with the temporal decomposition, content
axis, Rome/Italia, and women case study supporting and extending it. Empirical-first:
patterns now, interpretation in the Discussion. Restate the frame rule: "association
with population", "empire-wide common temporal component" (not "epigraphic habit") in
results.*

## 5. Geographic subsetting I — population and epigraphic output (HEADLINE; ~1,400 words)

*The centrepiece substantive result of the paper (Shawn 2026-06-21). Give it the
fullest treatment in Act II and the marquee figure (F7). Everything that follows in
Act II builds on or qualifies it.*

- **Within vs between province (define both in plain English).** The within-province
  population effect is **SUPPORTED**: about **48 %** of between-city output variation
  within a province tracks population (Latin f_within 0.480 [0.401, 0.566]; ~30 %
  empire context, f_within 0.299; Obs 75). **Sublinear** scaling: β_within = 0.733
  (Latin) / 0.587 (empire) — bigger cities are *less* prolific per head. The
  between-province effect is weak and uncertain (empire β_between ≈ −0.24, interval
  crosses zero). Define "sublinear" substantively.
- **Capitals over-produce** on top of size, in every period and on both frames
  (Hanson 2021 replicated; Obs 74).
- **Robust to the convention correction** — the de-fogging does *not* manufacture
  the population signal: confirmed at province level (Obs 94; Theil-Sen Δβ ≈ 0) and
  city level (Obs 107, D13; β_within shift −0.0086, robust under M=50 multiple
  imputation). This is the methodological payoff that ties Act II back to Act I.
- **Peak-scaling** = essentially the same exponent as cumulative output (Obs 100, 106).

**Figures:** **F7** (within vs between scaling scatter — the headline), **F6**
(capital over-production: forest + per-period medians).

## 6. Geographic subsetting II — temporal structure across scales (~1,300 words)

- **The nested decomposition (§5 Layer-A).** Splits each city's
  inscription-rate-over-time into an **empire-wide common** component, a **province**
  component, and a **city-specific** component, plus a between-city *level* spread.
  The three temporal tiers are **near-equal** (log-rate SD 1.11 / 1.02 / 0.98; each
  a ~2.7–3.0× multiplicative swing); the clean covariance-attributed partition is
  **38 % empire-common / 29 % province / 33 % city-unique** (Latin 37/30/33; sums to
  100). Footnote the 54 % *standalone* common share (tiers anti-correlated). (Obs 97;
  `h5-decomposition.json`, `temporal-three-way-split.json`.)
- **Peak of the empire-wide component: AD 187.5** (late-Antonine/Severan). State
  plainly that we do **not** call this "the epigraphic habit" — the four-driver
  conflation is held for the Discussion (Obs 98; the Obs 101 rule).
- **The apparent post-AD-250 "collapse"** is mostly the shared component falling
  away; once removed it is a **moderate, heterogeneous, provincial-tier relative
  decline** (median city ≈ ⅓ of its empire baseline in the 3rd century), not
  demonstrated depopulation (Obs 96, 103). Size–buffering gradient is
  province-mediated (Obs 104); province size itself not supported (Obs 105).
- **Scaling-over-time (U-shape).** β_within traces a shallow, overlapping U over
  eight 50-year periods — ~0.58 high-empire plateau — same on both frames (Obs 99,
  106): a descriptive trend, not a break.

**Figures:** **F9** (variance partition + component magnitudes), **F8**
(relative-trajectory fan — labelled "illustrative shape, NOT a population
estimate"), **F10** (β over time, the U-shape). Province/city atlases **F13 / F14**
→ candidates for supplement (see figure budget).

## 7. A second, orthogonal measure — content vs acts (~600 words)

- **Acts vs content** defined: acts = number of inscriptions; content = total Latin
  letter-mass. Letter-mass **independently supports** the within-province population
  effect (f_within 0.448 [0.364, 0.535]; Obs 109). "Prolific for its size" and
  "verbose per act" are **statistically orthogonal** traits (ρ ≈ 0; Obs 108) — content
  is not a rescaling of acts. Verbosity is idiosyncratic (not capitals, not size).
  The eye-catching R² = 0.841 of letters-on-count is near-mechanical, not a finding.
- **Scope limit (state it):** letter-mass *temporal* detection is out of reach;
  content claims are bounded to the cross-section (Obs 109).

**Figures:** **F11** (orthogonality scatter); **F5** (letter-mass SPD tracks the
count SPD — *raw*, no credible band; flag) → F5 is a supplement candidate.

## 8. Geographic subsetting III — Rome and Italy de-fogged (~600 words; EXPLORATORY)

*Flag clearly: exploratory / not preregistered; Rome stays excluded from every
confirmatory regression (Decision 36).*

- **Rome is the most convention-dated unit** (α ≈ 0.80 — four-fifths editorial).
  **Provincial capitals less** (α ≈ 0.56) — and *less* than ordinary provinces
  (≈ 0.71): capital epigraphy is *more* genuinely dated than its hinterland.
- **Italian exceptionalism:** Rome + Italian municipia (≈ 0.80 / 0.79) the empire's
  most convention-dated material. **Severan watershed:** Italy peaks early (~AD 80),
  provinces overtake by the AD 212 universal-citizenship horizon.
- (Obs 114; `runs/2026-06-21-rome-capital-comparison/REPORT.md`. Caveat:
  Italia-incl-Rome ESS-marginal; Rome's genuine *shape* weakly constrained — the
  *fraction* is the robust result.)

**Figures:** **F16** (capital comparison + α-convention strip) and **F19** (Italian
vs provincial chronology — Severan watershed) for the main text; **F15** (Rome
before/after), **F17** (why Rome excluded), **F18** (Italia exceptionalism) →
supplement candidates.

## 9. Thematic subsetting — a real-corpus case study: wives & daughters (~900 words)

*Co-authored with Adela Sobotkova; gated on her co-author pass before circulation.
Spec/outline: `runs/2026-06-20-women-corpus-feasibility/option-2-case-study-outline.md`.
This is the **thematic** (non-geographic) subset exemplar — the method pointed at a
coherent class of inscriptions rather than a place.*

- **The stakes.** The Shaw–Saller crossover-age tradition reads age-at-marriage off
  the *temporal distribution* of dated familial inscriptions; Adela's "Graveyard →
  Time Series" extends it to a time series. The prerequisite nobody checks: **is that
  time axis trustworthy enough for time-resolved claims?**
- **The conceptual frame (Shawn 2026-06-21):** on a corpus like this, de-fogging is
  a **diagnostic + hypothesis-generator, not a prover**. Every substantive read is a
  *hypothesis to test*; the honest "limits" verdict **is** the contribution.
- **Result 1 — the time axis is ~90 % convention** (α ≈ 0.90 overall / 0.84
  daughters; ~100-year median range, 68 % round-25-year slabs). The headline
  source-criticism (Obs 115).
- **Result 2 — no rescuable well-dated core.** Width is the wrong axis: convention is
  *structural* (lives at round widths), so the tightest intervals are the *most*
  convention-laden (≤ 50y band = 97 %); the genuine core is N ≈ 6–315, below the
  floor. The limit is **intrinsic to the dating, not a sample-size problem** (Obs 117).
- **Result 3 — an indicative, hypothesis-generating read** (heavily caveated):
  de-fogging tentatively shifts mass into the C2–C3 trough; a hypothesis for
  better-dated data, never a result (credible intervals far too wide).
- **De-fogging vs `tempun`.** `tempun` (Adela's group's tool) models *dating
  uncertainty*; de-fogging removes *editorial convention* — different artefacts. We
  ran `tempun` ourselves: its curve overlays the raw, convention-contaminated shape
  (both peak ~AD 188) — complementary, not redundant.
- **Forward pointer:** the substantive crossover-age history is the EJA companion
  (Option 3), not this paper.

**Figure:** **W1** (women corpus genuine vs raw + verdict). The tempun-comparison
figure → supplement or fold into W1 discussion.

---

# DISCUSSION & CLOSE

## 10. Discussion (~1,000 words)

*Interpretation now permitted (empirical-first discharged).*

- **What convention-dominance means** for Roman epigraphic chronology: most of the
  *apparent* dated record's shape is editorial artefact; histogram-eyeballing of
  dated inscriptions is unsafe without de-fogging.
- **The empire-wide common component, interpreted.** The four-driver conflation —
  (a) cultural epigraphic habit, (b) empire-wide demography/economy, (c) taphonomy,
  (d) residual convention — and why the AD-188 peak cannot be cleanly attributed
  (matches both MacMullen's habit curve and the Antonine apogee; no external proxy).
- **The population link, interpreted.** Association with Hanson's population
  estimates, sublinear within-province, capital over-production — situate against
  settlement-scaling theory (Hanson 2021; Ortman et al. on scaling) without
  over-claiming causation.
- **The instrument for the field.** A reusable, honestly-bounded source-critical
  tool applicable to *any* coherent subset — geographic or thematic — with a
  published reachability envelope. The women case study generalises the caution to
  inscription-based Roman demography at large.

## 11. Limitations (~400 words)

State, by us, first: model-conditionality; the reachability floor (per-city α
unreliable below N ≈ 500; only 34/268 §5 cities meet the N ≥ 300 floor); anchors
held out by design; identifiability caveats; the exploratory status of §8 and the
indicative §9 read; empire-aggregate under-convergence (R̂ = 1.0126); the
point-date aoristic-MC "collapse" is a classify-then-analyse plug-in artefact, the
mass-preserving arm the sound read (Obs 110); the Layer-B inversion is illustrative
shape only.

## 12. Conclusion (~300 words)

The instrument + the envelope as the durable contribution; the substantive findings
as the demonstration; the diagnostic stance as a transferable discipline for the
field.

## 13. Methods admin (in/after methods, per JAMT)

- **LLM-use disclosure** (REQUIRED — `paper-writing-brief.md` §8): the thorough,
  auditable account (Claude Code agent across 30 sessions; role; human authorship &
  oversight; verification; reproducibility). **Verify exact current JAMT wording
  before submission.** Candour is a strength here.
- **Data & code availability:** OSF prereg `https://osf.io/uycs6/`; git-versioned
  code, data processing, figure scripts; captured agent sessions as research record.
- **Preregistration statement:** lodged 2026-05-20 + four amendments (tags
  `osf-amendment-01..04`).
- **Author contributions** (CRediT) — confirm with co-authors.

---

## Supplement (rigour / bulletproofing — mirrors brief §4)

- **S1 — The model in full.** Mixture/deconvolution + cross-classified ("library")
  likelihood derivation; θ priors; hierarchical structure; concomitant-variable
  grounding + citations.
- **S2 — Validation in full.** The 300×100 recovery grid + four adoption criteria;
  θ re-derivation + sweep (27/29 stable); convergence diagnostics; the C10
  aoristic-MC validity battery.
- **S3 — Preregistration & governance.** OSF prereg + four amendments; the
  obligations audit; the multi-agent accuracy audit (~677 specifics).
- **S4 — Sensitivity analyses.** DM/NegBin (|Δα| ≤ 0.0156); measurement error
  (Berkson); stratified-sampling; flexible-null annex (NO-GO); the point-date vs
  mass-preserving aoristic-MC.
- **S5 — Variance-decomposition maths.** Covariance-attributed partition derivation;
  the standalone-vs-partition reconciliation.
- **S6 — Reachability simulation in full** + per-cell table.
- **S7 — Per-unit tables.** The 29 production units + Roma/Italia: α (convention
  fraction, both bounds), N, convergence; per-province / per-city atlases (F13/F14
  if moved here); the women-corpus probe tables.

---

## Word budget (aggregate check — per the "state the total" rule)

| Section | Target words |
|---|---:|
| 1 Introduction (incl. materials) | 1,300 |
| **Act I** | |
| 2 Method in concept | 1,400 |
| 3 Validation | 900 |
| 4 Reachability envelope | 800 |
| **Act II** | |
| Act II opener | 150 |
| 5 Scaling (HEADLINE) | 1,400 |
| 6 Temporal decomposition | 1,300 |
| 7 Content vs acts | 600 |
| 8 Rome & Italy (exploratory) | 600 |
| 9 Women case study (thematic) | 900 |
| **Close** | |
| 10 Discussion | 1,000 |
| 11 Limitations | 400 |
| 12 Conclusion | 300 |
| 13 Methods admin (+ LLM disclosure) | 400 |
| **Total (main text)** | **≈ 11,950** |
| Abstract (front matter) | 250 |

**This is ~1.95k over the ~10k self-imposed aim.** JAMT sets no hard limit, but if
we hold the line, the trim levers (in priority order) are: (a) compress §8 Rome &
Italy to ~400 or move most of it to the supplement (it is exploratory); (b) fold §7
content into the end of §5 (~−300); (c) tighten §6 (the post-AD-250 paragraph is the
densest); (d) move F13/F14 atlases to the supplement (frees no words but eases the
figure load). Doing (a)+(b) alone brings the main text to ≈ 10.9k. **Recommend
drafting full, then trimming at the revision pass** rather than starving sections now.

## Figure budget (20 built: F1–F19 + W1)

- **Main-text set (~11):** F1 (method), F4 (validation), F12 (reachability),
  F7 (scaling), F6 (capitals), F9 (variance partition), F8 (relative trajectory),
  F10 (U-shape), F11 (orthogonality), F16 + F19 (Rome/Italia), W1 (women). Optionally
  add F2 (empire/Latin SPD) → ~12.
- **Supplement set (~8):** F2 or F3 (province SPD small-multiple), F5 (letter SPD),
  F13 (province atlas), F14 (city atlas), F15 (Rome before/after), F17 (why Rome
  excluded), F18 (Italia exceptionalism), the tempun-comparison figure.
- 11–12 main-text figures is on the high side for a 10k article; the split above is
  a starting proposal, not locked.

---

## Open items / drafting sequence

1. **Confirm with Shawn:** title direction; author list & order; the word/figure
   budget calls (esp. §8 depth).
2. **Re-read the style exemplar** (Eftimoski, Ross & Sobotkova 2017, `ENPYIZQF`)
   before drafting §§2–4.
3. **Gate:** the women case study (§9) needs Adela's co-author pass before
   circulation; draft it from the agreed Option-2 outline meanwhile.
4. **Verify** the exact current JAMT LLM-disclosure + author-contribution wording
   before submission (live guidelines were auth-gated 2026-06-20).
5. **Draft order (empirical-first friendly):** Act I §§2–4 first (method is the
   spine and the hardest exposition), then Act II §§5–9, then Discussion/close, then
   Introduction and Abstract last (write them once the body exists).
