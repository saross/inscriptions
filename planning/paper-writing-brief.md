# Paper writing brief — inscriptions / LIRE deconvolution paper

**Status:** governing brief for the write-up phase (locked with Shawn 2026-06-20).
**Supersedes** ad-hoc framing notes; read this before drafting any section.
**Companion docs:** `reports/key-findings-summary-2026-06-20.md` (the on-ramp),
`runs/2026-06-20-figures/outputs/figure-captions.md` (figures at target level).

---

## 1. Target & scope

- **Journal:** *Journal of Archaeological Method and Theory* (JAMT, Springer).
- **Length:** **aim ~10,000 words** for the main text. JAMT sets no explicit word
  limit and publishes long articles, but we self-impose 10k for discipline and
  accessibility. Overflow of technical material goes to the supplement, not the
  main text.
- **Figures:** the built 14-figure set (`runs/2026-06-20-figures/`), vector PDF,
  sans-serif, JAMT/Springer artwork specs. Plain-language captions already drafted.

## 2. Audience — the dual readership (design every paragraph for both)

- **Primary reader:** a *typical* classicist / epigrapher / ancient historian /
  archaeology postgrad with **only rudimentary statistics**. They must be able to
  follow the argument, the findings, and *why they matter* without a stats
  background.
- **Expert reviewer:** assume **Crema, Bevan, or a peer of that calibre** (SPD /
  aoristic / Bayesian-archaeology specialists). The statistical core must be
  **tight and bulletproof** — no hand-waving they could puncture.
- The craft is serving both at once: plain-English exposition in the main text,
  full rigour available (in the supplement) for anyone who looks.

## 3. Governing principles

1. **Plain English first, alongside the statistics — never instead of, never
   after-only.** Explain *what* a method does and *what a result means* in plain
   language **before or alongside** the formal statement. No unexplained jargon;
   define every term on first use (SPD, aoristic, deconvolution, credible
   interval, sublinear scaling, Mundlak within/between, etc.).
2. **Push statistical detail, support, and argumentation to the supplement.** This
   serves *both* goals at once: it keeps the main paper accessible to the typical
   reader **and** makes the work bulletproof to a statistician reviewer (the full
   derivations, recovery grids, validation, sensitivity analyses, and prereg are
   all there to be checked). Main text states the result + the plain-English why;
   supplement carries the proof.
3. **Empirical-first / interpretation-later** (Obs 101). Present the empirical
   nested-unit decomposition and the corrected curves *first*; bring in
   interpretation (epigraphic habit, population, Hanson) *later*, in the
   discussion. Results stay model-conditional; use "association with population",
   "empire-wide common temporal component" (not "epigraphic habit") in results.
4. **Honesty framing baked in** (already in the figures): "illustrative relative
   shape, NOT a population estimate" (F8); convention *removal* + peak *recovery*,
   not "smoothing" (F1); the clean 38/29/33 partition with the 54% standalone
   footnoted (F9).

## 4. Main-text vs supplement split (working rule)

**Main text (accessible, ~10k words):**
- The problem (editorial-convention contamination of inscription dates) in plain terms.
- The method in concept (deconvolution: what it does, why), with one explainer figure.
- The validation in concept (Pompeii AD 79, Ostia apogee) — convincing, not technical.
- The findings, each stated plainly then supported: scaling is within-province;
  capitals over-produce; the temporal decomposition (38/29/33); the U-shape; the
  two orthogonal over-production channels; the reachability envelope as honest limits.
- Interpretation / significance for Roman history (discussion).

**Supplement (rigour, bulletproofing):**
- The full mixture/deconvolution model + the cross-classified likelihood derivation.
- The recovery-grid validation, θ re-derivation + sweep, convergence diagnostics.
- The preregistration + amendments trail (OSF), the obligations audit.
- Sensitivity analyses (DM/NegBin, aoristic-MC, measurement error, stratified sampling).
- The variance-decomposition maths (covariance-attributed partition) and the
  reachability simulation in full.

## 5. Style exemplar — how to explain the statistics

**Eftimoski, Ross & Sobotkova 2017**, "The impact of land use and depopulation on
burial mounds in the Kazanlak Valley, Bulgaria: An ordered logit predictive model"
(2017, vol. 23, pp. 1–10; Zotero key `ENPYIZQF`). This is **Shawn's own model** of
the register to hit: he explained an ordered-logit statistical approach to an
archaeology audience *after* extensive debriefing with Martin Eftimoski plus his
own web-searching and reading — i.e. a domain expert (not a statistician)
explaining a non-trivial method clearly and correctly. Re-read it before drafting
the methods sections; match its way of making a statistical model intuitive for an
archaeologist without dumbing it down.

## 6. Assets already at the right level

- **Key-findings summary** (`reports/key-findings-summary-2026-06-20.md`) — the
  non-specialist results narrative; the drafting on-ramp.
- **Figure captions** (`runs/2026-06-20-figures/outputs/figure-captions.md`) —
  "what is this? / what does it mean? / why does it matter?" prose at exactly the
  target accessibility; reuse and adapt for the main-text figure references.
- **14-figure set** — the visual backbone, honesty-framed.

## 7. Definition of "tight / bulletproof"

For the anticipated Crema/Bevan-calibre reviewer, every statistical claim in the
main text must have its full support reachable in the supplement, every method
choice must be justified (prereg + audit), and every limitation must be stated by
us *first* (reachability envelope, model-conditionality, anchors-held-out,
identifiability caveats) rather than discovered by the reviewer.
