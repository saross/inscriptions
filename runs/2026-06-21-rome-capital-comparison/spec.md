# Spec — Rome capital-comparison (de-fogged unit)

**Status:** DRAFT for pre-launch sign-off (Shawn). Do NOT run until signed off.
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
- **Unit B — `provincial-capitals-aggregate`.** `subset_corpus` to the capital
  city list (from
  `runs/2026-06-04-h3a-confirmatory/outputs/h3c-i-results-oxrep-primary.json`;
  62 empire capitals / 41 Latin capitals — pick per the frame decision in §3),
  pooled into one unit, same fit. This is the *comparison target* that makes it a
  "capital comparison" rather than a bare reference SPD.

Already in hand (no re-fit): `empire-aggregate` and `latin-aggregate` genuine
draws (`runs/2026-06-13-cc-production-refit/outputs/posterior-draws/`).

---

## 3. Design decisions for sign-off

1. **Convention basis for Rome (and the capitals).** The cc machinery selects a
   fixed per-frame basis: `tier_basis_empirical` (empire) vs
   `tier_basis_empirical_latin` (Latin) (`h2_lib.select_basis`). Rome is in
   neither aggregate (the empire basis was built across the whole corpus *incl.*
   Rome; the Latin basis *excludes* Rome). **Proposed primary: the empire basis**
   (Rome is sui generis, and the empire basis already "saw" it), with the Latin
   basis as a one-line sensitivity. **Decision needed:** confirm empire basis as
   primary.
2. **Capital frame for Unit B.** Empire capitals (62) or Latin capitals (41)? To
   keep the comparison clean against the *Latin* diagnostic frame, the Latin-41
   composite is the natural primary, with the empire-62 as context. **Decision
   needed.**
3. **Scope guard — Rome stays out of all regressions.** Confirm this is a
   descriptive reference + comparison ONLY; it is **not** added to H3a/H3c/§5, and
   it is labelled exploratory/non-preregistered. (Recommended: yes.)
4. **α reporting.** Report Rome's α descriptively (with CI) and *expect it may be
   low/distinctive* (heavy convention dating) — that is the finding, not a
   problem. Confirm we report it as a descriptive reference, not against the 0.70
   confirmatory envelope.

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

## 6. Pre-launch checklist

- [ ] Shawn signs off §3 design decisions (basis; capital frame; scope guard; α
      reporting).
- [ ] Driver script written + `/audit`-reviewed before the fit (reuse `h2_lib`;
      no new model code — assembly + fit + extract only).
- [ ] Run on sapphire under the standard thread-pinned + cgroup-capped wrapper.
- [ ] Results → Obs + figures; commit per stage.

## 7. Caveats to carry into the write-up

- Descriptive/exploratory, **not** preregistered; Rome remains excluded from all
  confirmatory regressions (Decision 36 stands).
- Rome's α is a reference value, read descriptively (not against the 0.70
  confirmatory envelope).
- The provincial-capitals-aggregate pools heterogeneous cities; it is a composite
  reference, not a per-city result (the per-city capital effect is H3c/F6).
