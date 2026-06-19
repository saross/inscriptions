# §5 Layer B — β-inversion to time-varying population (SPEC, pre-launch)

- **Status:** ✅ EXECUTED — signed off and run; results in `REPORT.md` (COMPLETE;
  the validation gate passes against both independent anchors, Ostia + Pompeii)
  and lodged as **Obs 96**. The original "DRAFT — Do not execute" stamp is
  superseded.
- **Author / date:** Claude (Opus 4.8, 1M context), 2026-06-16, on Shawn's brief.
- **Run dir:** `runs/2026-06-16-s5-layer-b-beta-inversion/`
- **Type:** Exploratory (Decision 13; preregistration §5 "Extension (Layer B)").
  Illustrative comparative-shape outputs only — **not** quantitative population
  claims (prereg wording, carried verbatim into the deliverable).
- **Estimated effort:** ~1 day (no new sampling; this is a deterministic
  posterior transform + plotting + the validation gate).

---

## 1. Purpose and provenance

§5 Layer A produced, for each of 268 small-N target cities (plus seven large
validation anchors and 45 provinces), a posterior over the **time-binned
inscription rate** `lam[c, t]` — the per-city latent log-rate exponentiated,
across `T = 16` bins of 25 years spanning 50 BC – AD 350 (`runs/2026-05-30-s5-
small-n-trajectories/`, `RESULTS.md`, commit `eb3aef3`; model in
`code/hier_model.py`). Layer A is *estimation, not hypothesis testing*.

**Layer B inverts each city's inscription-rate trajectory into a relative
population trajectory** via the H3a cross-sectional scaling law. The
preregistration (`planning/preregistration-draft.md`, lines 366–374) states the
inversion formula directly:

> **Extension (Layer B) — tentative inversion to time-varying population.**
> Under the assumption that the cross-sectional β-scaling estimated from H3a
> holds within-city over time, invert each city's trajectory to an illustrative
> time-varying population estimate: `pop_t ≈ pop_max × (insc_t / insc_max)^(1/
> β_within)`. Strong assumption flagged: within-city β stability over time is
> only approximately true. Reported as illustrative comparative-shape outputs
> only — *not* as quantitative population claims.

This spec operationalises that formula draw-wise (propagating both the Layer-A
trajectory posterior and the H3a β posterior), resolves the four staged design
decisions, and defines the validation gate.

---

## 2. The inversion, and its one non-obvious consequence

The H3a scaling law is `insc ∝ pop^β` with **β < 1 (sublinear)**. Inverting
gives `pop ∝ insc^(1/β)` with **1/β > 1**, so a proportional change in
inscriptions implies a *larger* proportional change in population:

- empire β_within = 0.587 ⇒ 1/β = **1.704**
- Latin  β_within = 0.733 ⇒ 1/β = **1.364**

**Consequence (critical-friend flag, must be stated in the write-up):** the
inversion *amplifies* temporal swings. A 50 % drop in inscriptions maps to a
0.5^1.704 ≈ **31 %** of peak population (a 69 % decline) under the empire β, and
0.5^1.364 ≈ **39 %** (a 61 % decline) under the Latin β. The choice of β
therefore changes the *amplitude* of every population trajectory materially,
even though it leaves the *shape* (peak timing, monotonicity) untouched. This is
the single most important reason the deliverable is framed as illustrative-shape
and the β choice is surfaced for sign-off (§6.i).

Using **β_within specifically** (not the pooled or between-province slope) is the
defensible choice: β_within is the within-province cross-sectional slope from the
Mundlak decomposition, i.e. the "holding province fixed" relationship — the
closest cross-sectional analogue to a within-city temporal relationship. The
between-province slope (β_between = −0.24, CI crosses 0) is unusable.

---

## 3. Inputs (all paths and values re-verified this session)

| Input | Source (verified) | Value / shape |
|---|---|---|
| Layer-A trajectory posterior (primary) | `runs/2026-05-30-s5-small-n-trajectories/code/production/monolithic-inscription-25y.nc` (gitignored; zbook + rpi-server backup `…/2026-05-30-s5-small-n-trajectories-posteriors/`; **now also on sapphire, sha256-verified**) | `lam[c, t]`, 4 chains × **2,000 = 8,000 draws** (verified by opening the file, not the argparse default), **C = 268 *target* cities** (the 7 large anchors are NOT in this fit — see below), T = 16 bins. Gate **PASS** (R̂ 1.0000, ESS 2571, 0 div). |
| H3a β posterior — **empire** | `runs/2026-06-04-h3a-confirmatory/outputs/h3a-results.json` → `primary.betas.beta_within`; underlying `idata-primary.nc` for draw-wise (**on sapphire**) | median **0.5869** [0.5187, 0.6574]; 1,044 cities / 56 provinces; ~12,000 draws (tune 6000 / draws 3000 / 4 chains). |
| H3a β posterior — **Latin** (sensitivity) | same JSON → `sensitivity_B_latin.betas.beta_within`; underlying `idata-latin.nc` (**on sapphire**) | median **0.7331** [0.6483, 0.8198]; 817 cities / 39 provinces. |
| Hanson per-city population (anchor) | `data/hanson2016/hanson2016_cities_oxrep.csv`, column **`urban_context_pop_est`** | one static point estimate per city (not time-resolved). All Layer-A target cities are Hanson-matched by construction, so all have a value. |
| Dataprep cache (for the anchor gate only) | `runs/2026-05-30-s5-small-n-trajectories/code/prepared/` — 275 `aoristic-<city>.npz` + `city-index.parquet` (**now on sapphire, 1.3 MB**) | per-city aoristic matrices incl. `aoristic-ostia.npz`, `aoristic-pompeii.npz`. Needed to re-fit the validation anchors standalone (§7). |

**The 268-city scope and the anchors.** The monolithic primary fit covers the
**268 small-N target cities** — that *is* the §5 Layer-B deliverable. The seven
large validation anchors (incl. **Ostia** and **Pompeii**) are deliberately not
in it; Layer A validated them via *standalone* single-city fits computed on the
fly (`orchestrate.py` `anchor_internal_consistency` / `pompeii_ad79_check`),
which were **not persisted**. So the Layer-B validation gate (§7) must re-fit the
anchors standalone from the dataprep cache — a small, fast addition, not part of
the 268-city core transform.

**Stack / read note (verified on sapphire 2026-06-16):** sapphire's project
`.venv` has **arviz 1.1.0, h5netcdf 1.8.1, xarray 2026.4.0, pymc 6.0.1**, and
*successfully read* the primary `.nc` (`lam` dims chain 4 × draw 2000 × city 268
× bin 16). The H3a `idata-*.nc` are pymc-6/arviz-1.1 also.

**Draw-wise pairing:** the two posteriors are independent fits on overlapping but
non-identical city sets; there is no joint sample. We propagate by Monte Carlo
under independence — for each of the **8,000** Layer-A draws, draw one β with
replacement from the β posterior (seeded). This is valid MC integration of two
independent uncertainties; the independence simplification is flagged in §10.

---

## 4. Method

For city `c`, bin `t`, posterior draw `k`:

1. Take the Layer-A draw `lam_k[c, t]` (inscription rate; already a full
   posterior trajectory).
2. Draw `β_k` from the β posterior (resampled, seeded; §3).
3. **Relative shape:** `s_k[c, t] = ( lam_k[c, t] / max_t lam_k[c, t] )^(1/β_k)`
   — each draw normalised to its own epigraphic peak (peak = 1).
4. **Hanson-anchored absolute:** `pop_k[c, t] = pop_max[c] × s_k[c, t]`, where
   `pop_max[c]` is the city's `urban_context_pop_est` — i.e. peak population is
   set to Hanson's estimate (prereg formula, exact).

Summaries per city: posterior median trajectory + 95 % credible band, for both
the relative-shape and Hanson-anchored versions (they differ only by the
constant `pop_max[c]`, so both fall out of one computation). Peak-bin posterior,
and the posterior on (peak population, decline-by-AD-350) where the absolute
version is shown.

**Segmentation by reliability.** Layer A's calibration floor is **N\* = 300**
(coverage ≥ 0.90 and shape r ≥ 0.90 only at N ≥ 300; `RESULTS.md` §2). Layer-B
outputs inherit this floor exactly (the transform adds no information). Cities
are tagged `reliable` (N ≥ 300) vs `below-floor` (N < 300, shown but flagged);
headline figures and any clustering use the reliable set, the rest are an
explicitly-caveated appendix.

For the **268 target cities** this is a deterministic transform of an existing
posterior — **no MCMC, no new sampling** — fast and fully reproducible from the
`.nc` + the β draws + a seed.

**Validation anchors (Ostia, Pompeii).** These are not in the monolithic fit
(§3), so the gate (§7) first re-fits each standalone via the single-city
`model.py` at full N from the dataprep cache (seeded; ~minutes each — the only
MCMC in Layer B), saves the anchor `.nc`, then applies the *identical* inversion
transform. This mirrors Layer A's own anchor-validation step exactly.

---

## 5. Deliverables

1. `outputs/layerb-population-trajectories.nc` (or parquet) — per-city
   posterior population trajectories (relative-shape + Hanson-anchored), reliable
   and below-floor tagged.
2. `outputs/layerb-summary.json` — per-city peak-bin, peak-population (anchored),
   net-decline summaries, β frame used, seed, provenance hashes of the input
   `.nc`.
3. Figures: small-multiples of population trajectories for the validation anchors
   and a sample of target cities; the empire-vs-Latin β amplitude overlay for a
   handful of illustrative cities.
4. `REPORT.md` — methods, the validation-gate outcomes (§7), and the
   illustrative-only framing carried verbatim from the prereg.

---

## 6. Design decisions (resolved — Shawn sign-off 2026-06-16)

**(i) Which β — empire vs Latin. → DECIDED: empire primary + Latin overlay.**
Empire β_within 0.587 as primary (the full-corpus H3a frame matches the
full-corpus Layer-A trajectories); Latin 0.733 as a sensitivity overlay (the 817
Latin-subset cities; most relevant to the Latin-epigraphic western cities). Both
cheap.

**(ii) Point vs posterior-propagated. → DECIDED: posterior-propagated, draw-wise**
(the established H3b idiom). Propagate both the Layer-A trajectory posterior and
the β posterior; a point estimate is strictly dominated (it would discard the β
uncertainty, which is large in the exponent — 1/0.519 = 1.93 vs 1/0.657 = 1.52).

**(iii) Absolute-scale anchoring. → DECIDED: produce both** — relative-shape
(peak = 1; the honest core, no extra assumption beyond β-stability) **and** the
Hanson-anchored absolute version (prereg-faithful, illustrative). They differ
only by the per-city constant `pop_max`, so both are free. *Caveat to state:* the
anchor sets peak *population* equal to Hanson's estimate at the bin of peak
*epigraphy* — i.e. it assumes Hanson's figure corresponds to the peak-epigraphy
era (~AD 150–200 for many cities, roughly defensible) and ignores Hanson's own
level uncertainty.

**(iv) Validation gate — Ostia c. AD 250. → DECIDED: descriptive-only** (prereg
default; no pass/fail threshold). See §7. *Still pending:* Shawn's stated
historical expectation for Ostia, to report the trajectory against.

---

## 7. Validation gate (audit H3)

The prereg lists the gate as an *aggregate diagnostic* at independently-dated
cities — "Pompeii AD 79, Ostia c. AD 250, etc." — and explicitly **defines no
pass/fail threshold**: "A negative result is itself a methodological
contribution" (prereg line 372). Consistent with Decision 13 (exploratory
throughout, no pre-committed thresholds).

- **Pompeii AD 79 — already passed in Layer A.** Genuinely-post-79 mass (bins ≥
  AD 100) = 0.12 % (`RESULTS.md` §3). The Layer-B inversion preserves this (the
  transform is monotone in `lam`), so Pompeii's population trajectory will
  collapse to ~0 after AD 79 by construction — a consistency check, not new
  evidence.
- **Ostia c. AD 250 — descriptive expectation (light lit search, 2026-06-16).**
  Ostia is a large anchor (N = 2380; standalone Layer-A trajectory exists). AD
  250 falls near the bin-11/12 edge of the 25y grid, well inside the envelope.
  Independent expectation, grounded in:
  - **Oxford Classical Dictionary, "Ostia"** (oxfordre.com/classics; OCD entry):
    "Much of what we know of Ostia refers to the 2nd and 3rd cents."; "Most of
    what is visible at Ostia is a development of the Flavian, Antonine, and
    Severan periods … suggesting wholesale redevelopment and large-scale
    investment in urban property"; the city was "abandoned in the 5th cent. ce".
  - **R. Meiggs, *Roman Ostia* (2nd edn, 1973)** — the foundational synthesis
    (the post-Severan phases were comparatively under-studied there).
  - **Revisionist caveat — D. Boin, *Ostia in Late Antiquity* (Cambridge, 2013)**:
    "theories that Ostia experienced 'decline' … in the third and fourth
    centuries are generally unfounded." A simple 3rd–4th-c. collapse is
    contested.

  **Expectation for the gate:** growth across the 1st–2nd c. AD to an apogee in
  the **2nd c. (broadly Antonine, with strong Flavian–Severan activity)**; our
  Hanson anchor estimate corresponds to this 2nd-c. apogee. Decline thereafter is
  the *traditional* reading (Portus competition + the wider 3rd-c. crisis) but is
  scholarly-contested for the 3rd–4th c.

  **Confound to state prominently (critical-friend flag).** The empire-wide
  *epigraphic-habit* decline after ~AD 250 (MacMullen 1982) depresses inscription
  counts independent of population, so any post-peak *population* fall the
  inversion shows is partly a habit artefact, not demonstrated depopulation. The
  Ostia gate is therefore read most cleanly on the **growth-to-peak (1st–2nd c.)**
  segment, where the habit is comparatively stable; the post-peak segment is
  reported descriptively with the habit caveat (and is exactly what Decision 13's
  H5 habit-removed residual analysis would later disentangle).

  **Gate verdict mode — descriptive-only** (Shawn, 2026-06-16; prereg default; no
  pass/fail threshold): report the Layer-B Ostia trajectory against the above and
  comment on fit to the growth-to-peak expectation; sustained-vs-declining late
  activity is *not* treated as pass/fail.

---

## 8. Compute plan

- **Host: sapphire (default; Shawn 2026-06-16).** All inputs are staged and
  verified there (2026-06-16): the 4 Layer-A `.nc` (primary sha256-identical to
  zbook + opens cleanly), the 2 H3a β `.nc`, and the dataprep cache. Sapphire's
  `.venv` reads the arviz-1.1 posteriors (versions in §3). zbook remains a viable
  fallback (the data and an identical stack live there too).
- **Cost shape:** the 268-city core is a numpy transform over a loaded posterior
  — minutes, no MCMC. The validation gate adds **two small single-city fits**
  (Ostia, Pompeii) — the only sampling in Layer B, a few minutes each.
- **Reproducibility:** seed fixed; input `.nc` sha256 recorded in
  `layerb-summary.json`; β draws resampled deterministically from the seed;
  anchor re-fit seeds recorded.
- **No model/LLM API calls.** (Flagged for the API review gate: this stage spends
  no API budget; compute is sapphire CPU only.)

---

## 9. Code plan

A single self-contained script `code/layerb_invert.py` in this run dir:

- `load_trajectory_posterior(nc_path)` → `lam` draws + city/bin coords (268).
- `load_beta_draws(h3a_nc, frame)` → β posterior draws (empire | latin).
- `invert(lam, beta_draws, pop_max, seed)` → relative-shape + anchored posteriors.
- `summarise(...)` → per-city medians, bands, peak-bin, decline; write `.nc`/json.
- `fit_anchor_standalone(city, cache, seed)` → re-fit Ostia/Pompeii via the
  single-city `model.py` at full N (the only MCMC), save the anchor `.nc`, then
  feed the same `invert(...)`.
- `validate_ostia(...)`, `validate_pompeii(...)` → gate outcomes vs §7.
- `plots(...)` → small-multiples + the empire-vs-Latin overlay.

`/audit` (or a focused review) before launch, per the standing pre-launch rule.

---

## 10. Critical-friend caveats (to carry into the write-up)

1. **Cross-sectional → temporal.** The inversion assumes the cross-sectional
   β-scaling holds *within a city over time*. This is the prereg's explicitly
   flagged "strong assumption"; it makes the output illustrative-shape, not a
   population estimate. β_within (within-group slope) is the least-bad
   cross-sectional analogue, but it is still a substitution of space for time.
2. **Amplification (§2).** 1/β > 1 magnifies every swing; the population
   trajectory always looks more dramatic than the inscription trajectory, and the
   empire-vs-Latin β gap changes amplitude by a visible margin.
3. **Posterior independence.** The Layer-A and H3a posteriors are combined under
   an independence assumption (separate fits, overlapping city sets). Any shared
   data-driven correlation between a city's trajectory and the global β is
   ignored — a minor simplification given β is a global structural parameter.
4. **Hanson anchor.** The absolute version pins peak population to a single
   static Hanson figure at the peak-epigraphy bin and ignores Hanson's level
   uncertainty; it is illustrative only.
5. **N\* = 300 floor.** Below ~300 inscriptions the underlying Layer-A trajectory
   is not reliable (Layer-A calibration); Layer-B inherits this exactly and tags
   accordingly.

---

## 11. Pre-launch sign-off checklist (Shawn)

- [x] **(i)** β frame: empire primary + Latin sensitivity — confirmed 2026-06-16.
- [x] **(ii)** posterior-propagated, draw-wise — settled by spec.
- [x] **(iii)** anchoring: produce both relative-shape and Hanson-anchored —
  confirmed 2026-06-16.
- [x] **(iv)** Ostia gate: descriptive-only — confirmed 2026-06-16.
- [x] **Ostia historical expectation** — grounded by a light lit search (OCD /
  Meiggs / Boin) rather than asserted, per Shawn (not an Ostia specialist); §7.
- [x] **Inputs staged + verified on sapphire** (2026-06-16): 4 Layer-A `.nc`
  (primary sha256-identical + opens), 2 H3a β `.nc`, dataprep cache (Ostia +
  Pompeii present); host = sapphire confirmed.
- [ ] Run script `code/layerb_invert.py` written + reviewed (`/audit` before
  execution).
- [ ] Final sign-off to launch.
