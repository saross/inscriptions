# Spec — Rome capital-comparison (de-fogged unit)

**Status:** Design decisions SETTLED (Shawn 2026-06-21; §3). Remaining gate before
a run: write + `/audit` the driver script (reuse `h2_lib`, no new model code), then
launch on sapphire. Do NOT run until the driver is audited.
**Created:** 2026-06-21 (Claude Code, Opus 4.8, on Shawn's brief).
**Provenance of the idea:** recovered from the session archive — first raised as a
peer-review flag (2026-04-23: "exclude Roma … *or run them separately*?"),
quantified in the prereg (2026-05-14: Rome = 65,435 inscriptions, 36.2 % of the
filtered corpus; the *only* site that meets Hanson's outlier rule), and proposed
as a standalone option (2026-06-07: "Rome … stays excluded per Decision 36 — but
it's there as its own unit if you ever want **the capital comparison**"). Never
spec'd until now.

---

## 1. Motivation — why give Rome a place without breaking the methodology

Rome is **excluded from every scaling/contrast regression** (H3a/H3c/§5) for a
sound, lodged reason: at 65,435 inscriptions (~36 % of the filtered corpus) it is
the *only* unit that meets Hanson 2021's own outlier threshold, and including it
would dominate any regression (Decision 36; lodged prereg; `c322de6`). That
exclusion is correct and stays.

But it leaves the **imperial capital — the epigraphic centre of gravity — with no
de-fogged chronology anywhere in the paper.** The fix is the one flagged in 2026:
run Rome as its **own deconvolution unit** (never folded into a regression) so we
can do a **capital comparison** — set Rome's genuine SPD and convention-intensity
beside (a) the provincial capitals (the H3c capital-over-production story, F6) and
(b) the empire and Latin aggregates we already have.

This is **descriptive / exploratory**, not preregistered — label it as such
throughout (cf. the A01 content-residual descriptive check). It adds a reference
unit and a comparison; it changes **no** confirmatory result.

### Questions it answers
1. **What does the capital's de-fogged chronology look like?** Rome's raw dating
   is heavily convention-laden (the AD 1–100 / 100–200 round slabs are enormous
   for Rome), so the raw→genuine correction should be the most dramatic in the
   paper — a strong "why de-fogging matters" exhibit.
2. **Does the imperial capital over-produce / behave differently from provincial
   capitals?** Compare Rome's genuine SPD *shape* and peak timing against the
   provincial-capitals composite and the aggregates.
3. **Is the capital's convention-contamination distinctive?** Compare Rome's
   genuine fraction α against the provincial capitals' and the aggregates' α —
   does the centre carry more (or less) round-slab dating than the provinces?

---

## 2. What to compute

Reuse the cross-classified ("library") production machinery verbatim
(`runs/2026-06-07-h2.1-launch-prep/code/h2_lib.py` `fit_unit`; the same model the
29 production units used). **Two new units**, both fit exactly as the production
units were:

- **Unit A — `Roma`.** `subset_corpus` on `province == "Roma"` (the 65,435-row
  unit). Build the aoristic-SPA count vector (`build_unit_y`), fit `fit_unit` with
  the **empire basis** (see §3 design decision), extract: genuine-SPD posterior
  draws (`Roma-pgen.npz`, 8 000 × 80), α posterior (median + 95 % CI),
  convergence, PPC.
- **Unit B — `provincial-capitals-aggregate`.** `subset_corpus` to the **empire-62
  capital city list** (the `empire.capital_cities` array in
  `runs/2026-06-04-h3a-confirmatory/outputs/h3c-i-results-oxrep-primary.json`),
  pooled into one unit, fit with the **empire basis** (§3.1/3.2). This is the
  *comparison target* that makes it a "capital comparison" rather than a bare
  reference SPD. (Latin-41 / Latin-basis = optional sensitivity panel only.)

Already in hand (no re-fit): `empire-aggregate` and `latin-aggregate` genuine
draws (`runs/2026-06-13-cc-production-refit/outputs/posterior-draws/`).

---

## 3. Design decisions — SETTLED (Shawn 2026-06-21)

1. **Convention basis → EMPIRE basis, throughout.** Rome, the provincial-capitals
   composite, and the empire-aggregate baseline all use the corpus-wide empire
   basis (`tier_basis_empirical`; `h2_lib.select_basis(design, "empire")`). The
   point is that the units being compared then differ ONLY in capital status, not
   in the basis used to deconvolve them — basis is not a confound. (The Latin
   basis deliberately excludes Rome, so using it for Rome would be a mismatch.)
2. **Capital set → the EMPIRE-62 provincial capitals**, deconvolved with the same
   empire basis, as the comparison composite (Unit B). This is the natural home
   for a Rome-inclusive comparison: Rome is an empire-level outlier, not a
   within-Latin unit. The Latin-41 / Latin-basis version is kept only as a
   secondary sensitivity panel (and carries Rome's basis caveat, so it is not the
   primary).
3. **Scope guard → descriptive comparison PLUS one illustrative "why Rome breaks
   the regression" exhibit.** Rome stays out of all *confirmatory* regressions
   (H3a/H3c/§5; Decision 36 stands). In addition, we add ONE clearly-labelled
   illustrative scaling fit/scatter *with Rome included*, shown only to
   demonstrate how the capital dominates/distorts the fit — a methods-section
   exhibit for *why* the exclusion is justified (see §4, F17). It changes no
   confirmatory result.
4. **α reporting → descriptive reference.** Report Rome's α as median + 95 % CI,
   read as a reference value ("the capital carries ~X % genuine date signal"). We
   expect it distinctive (Rome is heavily convention-dated) — that is the finding.
   No pass/fail against the 0.70 confirmatory envelope (Rome is the most
   data-rich/reachable unit of all, so reachability is not in question).

---

## 4. Deliverables

- `outputs/Roma-pgen.npz` + `outputs/provincial-capitals-aggregate-pgen.npz`
  (genuine-SPD draws), and a small `outputs/capital-comparison-summary.json`
  (per-unit α median/CI, n_eff, convergence, peak-bin).
- **Figure F15 — Rome before/after** (single-column): Rome's raw aoristic SPD vs
  its de-fogged genuine SPD + 95 % band + convention component, in the F1 idiom
  (reuse `figtheme`/`figdata`). The "capital de-fogged" exhibit.
- **Figure F16 — capital comparison** (single- or full-width): genuine SPDs
  overlaid — Rome vs provincial-capitals-aggregate vs empire-aggregate vs
  latin-aggregate (densities, shared axis) — plus a small α-comparison inset
  (Rome vs provincial capitals vs aggregates, medians + CIs).
- **Figure F17 — "why Rome is excluded" (illustrative, §3.3).** A pooled scaling
  scatter (log inscription count vs log Hanson population, all cities) with Rome
  plotted as the extreme high-leverage point, and the fitted scaling line shown
  **with vs without Rome** — making Hanson 2021's Fig. 7.4 exclusion point
  visually concrete (Rome's residual dwarfs every other city). **Framing note:**
  use the *pooled / between-city* scaling for this, NOT the within-province
  Mundlak — Rome is alone in its own province ("Roma"), so it carries no
  within-province contrast and would not distort β_within; the distortion Hanson
  documents (and that we illustrate) is the high-leverage outlier in the pooled
  count-vs-population fit. **Data requirement:** Rome's Hanson population estimate
  (Hanson 2016, ~1 M — confirm it is present in the source population table before
  building) + Rome's filtered inscription count (65,435). Clearly labelled
  illustrative; not a confirmatory fit.
- An **Obs** entry (working-notes) recording the result + the descriptive/
  exploratory status, cross-referencing Obs 74/99/106 (capital over-production)
  and the Rome-exclusion rationale (Decision 36).
- Optional: a short paragraph for the key-findings summary §4 (capital story).

---

## 5. Compute + cost

- **Two MCMC fits** on the 80-bin count vector (the mixture fit is over the binned
  count vector, so it does **not** scale with N — Rome's 65 k rows collapse to an
  80-bin vector). Each is comparable to one production-unit fit: **minutes on
  sapphire**, well inside the reachability envelope (Rome is the *most* reachable
  unit of all — N ≫ 2 000).
- Standard cc sampler config (`N_DRAWS=2000, N_TUNE=1000, N_CHAINS=4,
  TARGET_ACCEPT=0.95`); convergence gate as production.
- Figures are local, code-based (no compute). Total: a single short sapphire
  session + two figure scripts.

Plus the **F17 illustrative demo** (§3.3): a scatter + a pooled OLS/NBR line with
vs without Rome — negligible compute (no MCMC), local; needs Rome's Hanson
population + count.

## 6. Pre-launch checklist

- [x] Shawn signs off §3 design decisions — **SETTLED 2026-06-21** (empire basis +
      empire-62 capitals; descriptive + the F17 "why Rome breaks it" demo;
      α as a descriptive reference).
- [ ] Driver script written + `/audit`-reviewed before the fit (reuse `h2_lib`;
      no new model code — assembly + fit + extract only).
- [ ] Confirm Rome's Hanson population is present in the source table (for F17).
- [ ] Run the two fits on sapphire under the standard thread-pinned +
      cgroup-capped wrapper.
- [ ] Results → Obs (cross-ref Obs 74/99/106 + Decision 36) + figures F15/F16/F17;
      commit per stage.

## 7. Caveats to carry into the write-up

- Descriptive/exploratory, **not** preregistered; Rome remains excluded from all
  confirmatory regressions (Decision 36 stands).
- Rome's α is a reference value, read descriptively (not against the 0.70
  confirmatory envelope).
- The provincial-capitals-aggregate pools heterogeneous cities; it is a composite
  reference, not a per-city result (the per-city capital effect is H3c/F6).
