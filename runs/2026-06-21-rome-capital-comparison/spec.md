# Spec — Roma + Italia analyses (de-fogged units)

*(Covers the Rome capital-comparison §§1–7 AND the Italia-exceptionalism thread §8.
One driver, one library basis, all units comparable. Originally "Rome
capital-comparison"; broadened 2026-06-21 on Shawn's brief.)*

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

**Machinery — the PRODUCTION cross-classified "library" deconvolution, verbatim**
(`runs/2026-06-13-cc-production-refit/code/refit_lib.py` + `joint_lib`;
`build_model_cross_classified(pconv_mode="library")` under `adopted_theta_priors`
θ_conv ≈ 0.930 / θ_gen ≈ 0.025, κ=40). This is the **same model and the same
fixed corpus-wide slab library** that all 29 production units used — including the
empire-aggregate and latin-aggregate we compare against. Each new unit is just a
corpus subset → `build_unit_cc_data` → `fit_one(..., emit_draws_dir=...)`, exactly
as the production refit did. NOTE: this corrects an earlier draft that referenced
`h2_lib.fit_unit` — that is the *superseded* per-frame-basis model, NOT production.

**IMPORTANT consequence (supersedes the old §3.1):** the cc-library model has a
**single universal slab basis** shared by every unit; each unit only learns its own
`tier_weights` from it. So there is **no "empire basis vs Latin basis" choice** —
Rome, the capital composites, the Italia units, and the aggregates are **all fit on
the identical basis**, and every comparison below is apples-to-apples *by
construction*. The only thing that varies across units is **membership** (which
rows are pooled). Seeds: assign fresh `unit_index` values (≥ 100) so per-unit seeds
(`REFIT_BASE_SEED + unit_index`) never collide with the 0–28 production set.

### New units to fit (all same machinery, one library basis)

**Capital comparison — two tracks (Shawn 2026-06-21; membership differs, basis does not):**
- **Track 1 (empire frame, Rome-inclusive):**
  - `Roma` — `subset_for` on `province == "Roma"` (~65,457 rows).
  - `capitals-empire-62` — the 62 `empire.capital_cities` (match on
    `urban_context_city`) from
    `runs/2026-06-04-h3a-confirmatory/outputs/h3c-i-results-oxrep-primary.json`.
  - Compared against `empire-aggregate` (existing draws).
- **Track 2 (Latin frame, Rome-free — clean standalone, no caveat):**
  - `capitals-latin-41` — the 41 `latin.capital_cities` from the same JSON.
  - Compared against `latin-aggregate` (existing draws).
  - This completes the Latin-primary transition: a self-consistent Latin-frame
    capital-vs-province comparison that never touches Rome.
  - *Do not over-claim a direct empire-62-vs-Latin-41 contrast:* they differ in
    membership (the ~21 eastern capitals); read each within its own frame.

**Italia thread (Shawn 2026-06-21; see §8):**
- `Italia-incl-Rome` — `province_in` (Italian "/ Regio" provinces ∪ "Roma").
- `provinces-non-Italian-Latin` — Latin provinces minus the Italian regions
  (the clean "provinces" comparator for the Italia contrast).
- `Italia (excl. Rome)` — **already fitted** (production unit; load its draws).

### Already in hand (no re-fit) — load from `…/cc-production-refit/outputs/posterior-draws/`
`empire-aggregate`, `latin-aggregate`, `Italia (excl. Rome)`.

---

## 3. Design decisions — SETTLED (Shawn 2026-06-21)

1. **Convention basis → DISSOLVED (single universal library basis).** The
   production cc-library model uses one fixed corpus-wide slab basis for *every*
   unit (§2); there is no per-frame basis to choose, so the comparison is clean by
   construction. *(This supersedes the original "empire basis throughout" decision,
   which was framed around the superseded `h2_lib` per-frame model.)*
2. **Capital comparison → TWO tracks (membership only).** Track 1 empire-frame
   (Rome + empire-62 capitals vs empire-aggregate) AND Track 2 Latin-frame
   (Latin-41 capitals vs latin-aggregate). Because the basis is universal, Track 2
   is a **clean standalone Latin-primary comparison, not a caveated sensitivity** —
   it completes the make-Latin-primary transition (Shawn 2026-06-21). Read each
   track within its own frame; do not force a direct empire-62-vs-Latin-41 contrast
   (they differ in membership).
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

- Per-unit genuine-SPD draws (`outputs/<unit>-pgen.npz`) for: `Roma`,
  `capitals-empire-62`, `capitals-latin-41`, `Italia-incl-Rome`,
  `provinces-non-Italian-Latin`; plus per-unit JSON (α median/CI, n_eff,
  convergence, aligned/mass fractions, PPC) and a `roma-italia-summary.json`.
- **Figure F15 — Rome before/after** (single-column): Rome's raw aoristic SPD vs
  its de-fogged genuine SPD + 95 % band + convention component, in the F1 idiom
  (reuse `figtheme`/`figdata`). The "capital de-fogged" exhibit.
- **Figure F16 — capital comparison, TWO panels** (full-width): (a) Track 1
  empire frame — Rome vs capitals-empire-62 vs empire-aggregate; (b) Track 2 Latin
  frame — capitals-latin-41 vs latin-aggregate. Genuine SPD densities, shared axis;
  plus an α-comparison strip (all units, medians + CIs).
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

Across the whole programme (capital comparison + Italia §8): **~5 new cc-library
fits** (Roma, capitals-empire-62, capitals-latin-41, Italia-incl-Rome,
provinces-non-Italian-Latin), each minutes on sapphire — all the most reachable
units in the corpus (large N). A single short sapphire session. Existing units
(empire-aggregate, latin-aggregate, Italia excl. Rome) load from draws.

---

## 8. Italia-exceptionalism thread (Shawn 2026-06-21)

**Motivation.** Secondary literature treats Italia as a special case in the empire
— privileged status up to roughly the Severan period, eroding through the Antonine
Constitution (AD 212) and the Diocletianic provincialisation. Does the de-fogged
epigraphic record carry a distinctive "Italian" signature, and does it fade across
that watershed?

**Key data fact (shapes the design).** Rome is ~65 k of ~109 k Italian-region rows
— so "Italia incl. Rome" is ~60 % Rome. Lumping Rome into Italia just yields a
Rome-dominated unit. The discriminating question is therefore **three-way**:
**Rome vs Italia-excl-Rome (Italian *municipal* epigraphy, ~43.7 k rows) vs the
non-Italian provinces** — does Italian municipal epigraphy pattern with the capital
or with the provinces?

**Analyses (all descriptive / exploratory; not preregistered):**
1. **α (genuine-fraction / convention-intensity) comparison** — Rome vs
   Italia-excl-Rome vs provinces-non-Italian-Latin vs the empire/Latin aggregates.
   Is Italian convention behaviour distinctive?
2. **Genuine-SPD shape comparison** — the three de-fogged chronologies overlaid:
   does Italian municipal epigraphy track Rome or the provinces in *shape*?
3. **Temporal / Severan-watershed read (the historical hook).** Compare the
   **full-window genuine-SPD trajectories** of Italia-excl-Rome vs the non-Italian
   provinces and locate **when** they diverge/converge — is Italian
   distinctiveness concentrated *before* the Severan period and does it fade
   after? **Method choice (critical-friend):** use the full-window de-fogged
   trajectories, **NOT** per-50-year-period deconvolution fits — within a single
   50 y period the 50–300 y convention slabs are not separable from genuine (the
   identifiability needs the full envelope), so per-period α would be unsound. The
   full-window genuine trajectories already carry the temporal divergence
   descriptively.
   - *Optional future extension (NOT in this run):* a per-period H7-style scaling
     premium (Italian cities vs provincial cities, Mundlak NBR × periods) would
     test whether the Italian *scaling* premium fades — heavier, model-different,
     and companion-paper-adjacent; flag, do not run blind.

**Deliverables (Italia):**
- **Figure F18 — Italia exceptionalism:** the three-way genuine-SPD overlay (Rome
  vs Italia-excl-Rome vs non-Italian provinces) + an α-comparison strip.
- **Figure F19 — Italia temporal/Severan read:** Italia-excl-Rome vs non-Italian
  provinces genuine-SPD trajectories with the divergence window highlighted; an AD
  212 / Severan marker for orientation.
- An **Obs** entry; a short summary paragraph (new mini-section or §2/§4 addition).

**Italia scope guard.** Descriptive/exploratory, not preregistered; the Italian
regions stay as defined by `refit_lib._italian_provinces()` ("/ Regio" rule). No
confirmatory claim; the Severan-watershed reading is descriptive and explicitly
framed as a first-order result to calibrate the historical debate, not to resolve
it.

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
