# H9 letter-mass H3a — BUILD-NOTES

**Status:** CODE BUILT, NOT RUN. No fit, smoke test, or MCMC has been executed.
This run directory must be AUDITED before it is run (standing project rule:
audit before running). The exact run command for the post-audit run is in §6.

**What H9 is.** The cross-sectional confirmatory H3a within-between (Mundlak)
negative-binomial regression, with **per-city letter-count mass** as the
response in place of inscription count. It mirrors the inscription-count H3a
confirmatory run (`runs/2026-06-04-h3a-confirmatory/`) in every other respect.
H9 is pending because the letter *temporal* recovery grid failed convergence
(OSF Amendment 01 §A5.5.1, Grid B FAIL); the cross-sectional letter NBR is a
separate, simpler model that does **not** use the temporal mixture, and is
explicitly unaffected by that failure (Amendment 01 §A5.5).

**Author / date.** Claude Code (Opus 4.8, 1M context), 2026-06-18, on Shawn's
BUILD-AND-COMMIT-ONLY brief.

---

## 1. Provenance — what was copied, what was changed

Per the standing rule (do **not** edit any lodged/shared module; a prior agent
broke a lodged model by refactoring it), **no existing run-dir code or shared
module was modified**. The H3a machinery was **copied** into this run dir and
adapted:

| H9 file | Adapted from (H3a confirmatory, 2026-06-04) | Substantive change |
|---|---|---|
| `code/h9_common.py` | `code/h3a_common.py` | response = per-city letter mass; Latin frame promoted to PRIMARY; letter-count primitive added (Latin A–Z only) |
| `code/01-data-prep.py` | `code/01-data-prep.py` | emits Latin (primary) + empire (secondary) letter-mass frames |
| `code/prior-predictive.py` | `code/prior-predictive.py` | reads the Latin letter-mass frame; simulates per-city letter mass |
| `code/02-h9-fit.py` | `code/02-h3a-fit.py` | response = letter mass; Latin primary; letter-weighted variant; interpretive sensitivity |
| `code/03-ppc.py` | `code/03-ppc.py` | runs the same 10 checks against the Latin letter-mass posterior |
| `data/province-language-map.csv` | `data/province-language-map.csv` | verbatim copy (defines the Latin frame; Decision 36) |

The model, the six priors, the non-centred province parameterisation, the
sampler settings, the convergence gates, the `f_within` estimand, the three-way
verdict, the probability ladder, the Bayesian R², the OLS log-log comparator,
the standardisation sensitivity, and the ten-check PPC suite with two-tier
severity are **byte-for-byte the same logic** as the H3a template, with the
response variable swapped.

---

## 2. Design choices I had to make

### 2.1 The letter-count field (THE load-bearing choice)

**Decision: per-inscription letter count = Latin A–Z characters only, Greek
excluded, counted on `clean_text_conservative` (primary) and
`clean_text_interpretive_word` (sensitivity).**

- **Why.** This is the **lodged** definition. OSF Amendment 01 §A5.1: *"Summed
  `clean_text_conservative` characters (Latin A–Z only; Greek excluded), per
  the existing definition at `preregistration-draft.md` line 388."* Prereg line
  388 is explicit: *"the `clean_text_conservative` field — Latin A–Z characters
  only, Greek excluded."* `clean_text_interpretive_word` is the lodged
  sensitivity variant (§A5.1).
- **Implementation.** `h9_common.count_latin_letters` uses the regex
  `[A-Za-z]` — the 26-letter ASCII Latin alphabet, upper and lower case only.
- **Per-city letter mass** = the sum of that per-inscription count over the
  city's date-window-filtered, Hanson-matched, Rome-excluded inscriptions.

> **DIVERGENCE FROM THE 2026-05-26 PROBE — FLAG FOR AUDIT.** The earlier
> letter-count probe
> (`runs/2026-05-26-letter-count-probe/code/01-compute-letter-counts.py`) used a
> **broader** regex, `[A-Za-zÀ-ÿΑ-Ωα-ω]`, which **also counts Greek
> (`Α-Ωα-ω`) and Latin-1-supplement diacritics (`À-ÿ`)**. That probe pre-dates
> Amendment 01 and its measure is **NOT** the lodged one. H9 deliberately uses
> the narrower, lodged Latin-A–Z-only primitive. **The two will produce
> different per-city totals**, especially in provinces with Greek epigraphy.
> Auditor: confirm the lodged Latin-A–Z-only reading is what H9 should use (I
> believe it unambiguously is, per Amendment 01 §A5.1 + prereg line 388). If the
> project ever wants the probe's broader count, that is a *different* measure and
> would need its own amendment note — it is **not** the lodged content measure.

### 2.2 Primary frame = Latin-speaking provinces (not empire-wide)

**Decision: PRIMARY = Latin-speaking provinces; SECONDARY/context = empire-wide.**

- The H3a *confirmatory* run (2026-06-04) was built with empire-wide as PRIMARY
  and Latin as Sensitivity B, because at that date the Latin-primary reframe had
  not yet been decided. **Decision 36 (2026-06-05) → OSF Amendment 02 (lodged
  2026-06-06)** reframed the **primary hypothesis-testing frame to the
  Latin-speaking provinces**, with empire-wide retained as secondary/context
  with the LIRE-coverage caveat. The H9 brief explicitly instructs Latin =
  PRIMARY, empire = secondary/baseline, run both. H9 therefore **inverts** the
  H3a template's frame ordering to follow the lodged Latin-primary framing.
- The Latin frame is defined by the copied `data/province-language-map.csv` (the
  first-class artefact that defines the frame; Decision 36 §2). The realised
  inscription-count Latin frame is 817 cities / 39 provinces (Amendment 02
  §A5.3). The H9 letter-mass frame is built over the **same cities** (the
  eligibility predicate is identical; only the response differs), so the
  city/province counts are expected to match; `01-data-prep.py` HARD-STOPs if
  the Latin city count falls outside [750, 870].

### 2.3 Weighted f_within variants: population-weighted + LETTER-weighted

**Decision: the two Decision-32 weighted variants are population-weighted and
LETTER-weighted.**

- The H3a template's two weighted variants are population-weighted (`w_c =
  pop_c`) and **inscription-weighted** (`w_c = inscription_count_c`). Since the
  H9 response is letter mass, the natural analogue of the
  inscription-weighted variant is **letter-weighted** (`w_c = letter_mass_c`).
  Both are computed and labelled clearly in `h9-results.json`
  (`f_within_population_weighted`, `f_within_letter_weighted`).
- I did **not** also add an inscription-weighted variant. The brief says
  "letter-weighted as the natural analogue; include both and label clearly" —
  "both" = population-weighted + letter-weighted. If the auditor wants the
  inscription-weighted variant *as well* (3 weighted variants), that is a
  one-line addition (`w_insc = cities["inscription_count"]`); flagged here so the
  choice is conscious. The per-city `inscription_count` is carried in the frame,
  so the data is there.

### 2.4 Date-window / eligibility handling

**Decision: identical to H3a — no re-decision.**

- The date window (50 BC – AD 350, overlap not containment), the three filter
  predicates, and the Rome exclusion are taken verbatim from
  `h3a_common.load_filtered_lire` / `rome_mask`. Letters are counted on the
  **already-date-window-filtered** rows, then summed per city. So per-city letter
  mass is a date-window-filtered quantity by construction (Decision 22/35,
  unchanged by both amendments — Amendment 01 §A6).
- Frame eligibility (Hanson-matched, Rome-excluded, ≥1 date-window inscription)
  is identical to the H3a primary frame. A city with ≥1 inscription but a total
  letter mass of 0 (all its inscriptions have no readable Latin letters — e.g.
  Greek-only or figural) **remains in the frame with `letter_mass = 0`**; the NBR
  handles a zero response. This matches the H3a template's "LIRE-present cities
  only" choice (launch spec §3a option (i)) — I did not add the with-zeros
  Sensitivity A frame (see §3 below).

### 2.5 Seed

**Decision: `RANDOM_SEED = 20_260_618` (today's date).** The H3a confirmatory
run used `20_260_604` (its date); H9 uses its own run date, mirroring the
project's per-run-date seed convention (the 2026-05-26 probe used 20260526,
etc.).

### 2.6 Output paths kept under the H9 run dir

The processed letter-mass parquets are written to
`runs/2026-06-18-h9-letter-mass-h3a/data/processed/` (NOT the project-level
`data/processed/`), so the H9 letter-mass frames never collide with the
inscription-count H3a frames.

---

## 3. What in the H3a template I could NOT mirror cleanly (and why)

1. **The "with-zeros" Sensitivity A frame was dropped, not mirrored.** The H3a
   template builds a Sensitivity A "structural zeros" frame (Hanson cities with
   zero date-window *inscriptions*). For H9 this axis is **not meaningful in the
   same way**: a city already needs ≥1 inscription to have any text to count, and
   the H3a run found **0 structural zeros were actually added** (all 1,044 Hanson
   cities had ≥1 date-window inscription — see `02-h3a-fit.py` results note). So
   the inscription-level with-zeros frame would be identical to the primary, as
   it was for H3a. H9 instead carries **letter-mass zeros within the frame**
   (cities with inscriptions but no readable Latin letters; §2.4). If the auditor
   wants a Hanson-cities-with-zero-*letters* structural-zero frame, flag it — it
   is a different construct and not in the H3a template.

2. **The brms ↔ pymc cross-language shadow (launch spec step 4) is NOT
   included.** The H3a template ships `h3a_brms_shadow_mundlak.R`. I did **not**
   build an H9 brms shadow, because (a) it needs the R/Stan environment, which
   the brief does not provision and the run host (zbook) may not have; and (b)
   building it would mean adapting the lodged R script, which is more than a
   response-variable swap. **FLAG FOR AUDIT:** if the H9 confirmatory result
   needs the same cross-language agreement check the H3a result has, the R shadow
   should be added as a follow-up (adapt the R script *into this run dir*, do not
   edit the original). The pymc H9 fit is self-contained without it.

3. **H3c (Moran's I spatial-residual replication, launch spec step 5) is NOT
   included as a standalone script.** The brief scopes H9 to the *cross-sectional
   NBR* (H3a analogue). The **posterior-predictive Moran's I (check #10)** of the
   PPC suite **is** included (it is part of the mirrored PPC). A full H3c
   (conditional-permutation Moran's I at k = 5/8/10 on the posterior-mean
   residual) is **separately** flagged in Amendment 01 §A5.2 as **exploratory
   under letter mass** (not confirmatory), so omitting it from the *confirmatory*
   H9 pipeline is consistent with the lodged scope. If wanted, it is a follow-up
   (adapt `04-h3c.py` into this run dir).

4. **Prior-sanity gate band may not transfer to the letter-mass scale — FLAG.**
   The design-artefact prior-sanity gate `[0.1, 1e4]` on the median
   prior-predictive per-city response was calibrated for inscription **counts**.
   Letter mass is on a much larger numeric scale (per-city totals run into the
   thousands). Under the **same lodged priors** (`a0 ~ N(0,5)`, unit-scale
   slopes; unchanged by Amendment 01 §A6) the simulated median could legitimately
   sit near or above the upper bound. I kept the gate **identical** to the H3a
   template (I did not silently change a lodged threshold) and made
   `prior-predictive.py` **HALT for human adjudication** rather than auto-pass or
   auto-revise if the band is breached, with an explicit note that this may be a
   band-transfer issue rather than absurd priors. **Auditor: decide whether the
   sanity band needs a letter-mass-specific value before the run, or whether a
   breach should be read as informational only.** This is the single most likely
   thing to trip on first run.

5. **PPC bounds are reused verbatim — confirm they transfer.** The PPC suite's
   numeric bounds (mean ±10%, SD ±25%, q95 ±30%, mean-variance ratio [0.5×, 2×],
   proportion-of-zeros ≤ 0.02) were pinned in the H3a design artefact for the
   inscription-count response. They are reused unchanged for letter mass. These
   are *self-referential* (observed vs posterior-predictive of the same data), so
   they should transfer in principle; but the proportion-of-zeros and
   mean-variance-ratio checks in particular may behave differently for the
   heavier-tailed letter response. **Auditor: confirm the design-artefact PPC
   bounds are intended to apply unchanged to letter mass** (I believe they are —
   the amendment says the letter-mass confirmatory uses the *same* decision rules
   — but the design artefact itself predates the two-measure framework).

---

## 4. Convergence-risk note (informational, not a build choice)

Letter mass is a **compound sum of heavy-tailed per-inscription letter counts**;
its *temporal* recovery grid (Grid B) failed on R̂/ESS (Amendment 01 §A5.5.1).
The cross-sectional NBR here is a **different, simpler model** (no temporal
mixture) and is expected to be far better-behaved, but the heavier tail means
convergence is **not** guaranteed at the H3a-inherited settings (tune 6,000 /
draws 3,000 / target_accept 0.97). The fit script **HARD-STOPs on any gate
failure** and instructs the runner to raise tune / investigate per spec — it
does **not** relax the gate. If the primary Latin fit will not clear the gate
even with more warmup, that is a finding to report, not a thing to engineer
around silently.

---

## 5. Files created

```
runs/2026-06-18-h9-letter-mass-h3a/
├── .gitignore                       # *.nc, __pycache__
├── BUILD-NOTES.md                   # this file
├── code/
│   ├── h9_common.py                 # adapted from h3a_common.py
│   ├── 01-data-prep.py              # builds Latin + empire letter-mass frames
│   ├── prior-predictive.py          # prior-predictive thresholds (Latin)
│   ├── 02-h9-fit.py                 # the fits (primary Latin + sensitivities + empire)
│   └── 03-ppc.py                    # the 10-check PPC suite (Latin posterior)
└── data/
    └── province-language-map.csv    # copied; defines the Latin frame (Decision 36)
```

Outputs (`data/processed/*.parquet`, `outputs/*.json`, `outputs/*.csv`) and
posteriors (`outputs/*.nc`) are produced by the run; `*.nc` is gitignored.

---

## 6. Exact run command (for the later, POST-AUDIT run on zbook)

Run from the **project root** (`/home/shawn/Code/inscriptions`), with the
project venv. The scripts resolve their own paths relative to the module, and
import `h9_common` by name, so run them with the code dir as the working
directory (or on `PYTHONPATH`). The canonical sequence:

```bash
cd /home/shawn/Code/inscriptions/runs/2026-06-18-h9-letter-mass-h3a/code

# Step 1 — data prep (builds Latin + empire letter-mass frames; cheap).
/home/shawn/Code/inscriptions/.venv/bin/python 01-data-prep.py

# Step 0 — prior-predictive thresholds (commit BEFORE the fit; cheap).
/home/shawn/Code/inscriptions/.venv/bin/python prior-predictive.py

# Step 2 — the fits (PRIMARY Latin + standardised + interpretive + empire).
#          This is the MCMC step; the heavy one. Redirect TMPDIR to
#          disk-backed scratch (2026-05-23 lesson) on the run host.
/home/shawn/Code/inscriptions/.venv/bin/python 02-h9-fit.py

# Step 3 — PPC suite against the PRIMARY Latin posterior.
/home/shawn/Code/inscriptions/.venv/bin/python 03-ppc.py
```

(`03-ppc.py` needs `libpysal` + `esda` for the Moran's I check — the same
dependencies the H3a PPC needs; confirm they are present on the run host.)

**Step ordering:** `01-data-prep` → `prior-predictive` → `02-h9-fit` →
`03-ppc`. `prior-predictive.py` only needs the Latin parquet, so it can run any
time after step 1 and must run before step 3 (which reads
`prior-predictive-thresholds.json`).
