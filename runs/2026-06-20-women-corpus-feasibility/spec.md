# Women-corpus deconvolution — feasibility study (spec)

**Status:** DRAFT for Shawn's sign-off (2026-06-20). Proof-of-feasibility for the
"From Graveyard to Time Series" collaboration (Adela Sobotkova, Aarhus University;
co-author on the current JAMT paper). To be **run after her canonical dataset
arrives** (the 813-daughter version, requested, expected this evening). The repo's
`data/women.csv` (1,397 rows / 504 daughters, gzip-compressed despite the `.csv`
name) is **STALE — for a pipeline dry-run only**, never for a number shown to Adela.
**Author:** Claude Code (Opus 4.8, 1M context) on Shawn's brief, 2026-06-20.
UK/Australian English; Oxford comma.

---

## 1. Purpose

Does subset-specific **convention-deconvolution** change the **temporal distribution**
of Adela's datable conjugal corpus — especially in the **C2–C3 window where her
crossover-age trough sits** — and is the corpus **above the reachability floor** for
reliable de-fogging?

**Why it matters (the collaboration rationale).** Adela's interpretive claim rides on
the *timing* of the crossover trough (between the Antonine Plague and the Plague of
Cyprian; the inflection apparently *predating* the material shocks). That timing is
read off the temporal distribution of datable inscriptions — and her trough sits in
the later-imperial window, which **our own LIRE corpus analysis finds is where
editorial-convention date-contamination is highest** (the high-α zone; confirm the
exact window from `runs/2026-06-02-recovery-utility-check/` before citing a figure to
her). So de-fogging bears directly on her load-bearing claim. Her current pipeline
uses `tempun` Monte Carlo (uniform-prior aoristic + nested bootstrap + 90 % CI) —
respectable aoristic treatment, but it does **not** remove convention artefacts. That
is precisely our value-add; it is *not* "add uncertainty" (she has that).

## 2. Scope boundary (Shawn-approved 2026-06-20) — protects against preempting her paper

**Methodological feasibility ONLY.** We produce the genuine-vs-raw temporal SPA and a
reachability verdict. We do **NOT** compute the wife-vs-daughter **crossover-age
trajectory** — that substantive result is reserved for the companion (European Journal
of Archaeology-style) paper. Per-role *temporal-SPA* fits (below) are for
**reachability assessment**, not crossover inputs; we report temporal distributions and
de-fogging, never the age-crossover.

Mapping to the two papers:
- **Current JAMT paper** — the instrument demonstrated on a real subset (genuine-vs-raw
  temporal de-fogging); a methodological vignette, interpretation deferred + cited to
  the in-prep companion.
- **Companion (EJA)** — the substantive marriage-age history (the crossover trajectory,
  Life History Theory reading, plague/economy correlation); Adela's, we contribute the
  temporal method.

## 3. Deliverables (for the Denmark conversation)

1. **Genuine SPA vs raw aoristic SPA** of the datable corpus (figure + arrays); overlay
   her `tempun` output too **if she provides it** (otherwise genuine-vs-raw only).
2. **A focused read on the C2–C3 region:** does the temporal mass in the trough window
   shift under de-fogging (e.g. change in mass fraction over ~AD 150–275, and the shift
   in the SPA's relevant quantiles)? Descriptive — no hypothesis test.
3. **Reachability verdict** per subset (overall, wives, daughters): the learned α and
   where each sits vs the measured floor (N ≈ 500 easy → N ≈ 2,000 worst-case;
   Decision 34 / `runs/2026-06-03-small-n-reachability/`). Honest reliable / marginal /
   below-floor call — this tells Adela whether her *time-resolved* analysis is on solid
   ground for de-fogging.
4. **A one-page memo** for a co-author (method + caveats), explicitly deferring the
   substantive crossover history to the companion.

## 4. Data and adapter

- **Input:** Adela's canonical dataset (813-daughter version). **Confirm her exact
  `datable` + `conjugal` filters** so our subset matches her ~850 datable conjugal
  (and her 50–349 CE window). Do not infer them — ask.
- **Required fields:** role (wife/daughter), date interval (`not_before`/`not_after`),
  the conjugal/datable flags.
- **Adapter:** map her corpus into the format the production deconvolution machinery
  expects — `h2_lib`/`refit_lib` consume `nb`/`na` + the LIRE structure; her file has
  `not_before`/`not_after`. A thin adapter builds the aoristic SPA + cross-classified
  observables (aligned/non-aligned, rule C) from her intervals, then reuses
  `refit_lib.build_unit_cc_data`.
- **Convention basis:** the FIXED corpus-wide slab library
  (`runs/2026-06-13-cc-production-refit/outputs/production-slab-library.json`). The
  universal template basis is corpus-wide and applies to any Latin epigraphic subset
  (Decision 34: a subset learns its own `tier_weights` from the fixed basis). Her
  corpus is EDH + LIRE Latin material → applicable. **Sanity-check the aligned-fraction
  / L1 fit** as the production refit does; if her corpus's convention profile is wildly
  off the library's span, flag it (the per-class-basis caveat, Decision 34 revisit).

## 5. Method

- **Model:** the production cc-library deconvolution
  (`joint_lib.build_model_cross_classified(pconv_mode="library")`) under the adopted θ
  prior (θ_conv ≈ 0.930, θ_gen ≈ 0.025, κ = 40) — identical to D13 / the production
  refit. Reuse `fit_one` / `build_unit_cc_data` / `adopted_theta_priors` /
  `load_library_basis` verbatim; the women corpus is just another "unit" (a filter).
- **Fits:** (1) overall datable corpus; (2) wives; (3) daughters — (2)/(3) for
  per-subset reachability only.
- **Date window:** match Adela's 50–349 CE (confirm); report the corpus's own range too.
- **Per-fit outputs:** genuine SPA (`p_gen` median + draws), raw aoristic SPA, learned
  α (+95 % CI), convergence (R̂/ESS/divergences), aligned/mass fractions, PPC adequacy.
- **Reachability:** classify each subset against the Decision-34 map (N + learned α).
- **C2–C3 read:** quantify the genuine-vs-raw temporal-mass shift in the trough window.

## 6. Governance & hard-stops

- **Collaboration data** (Adela, Aarhus). Feasibility outputs are for the co-author
  conversation, **not for publication without her involvement**. AI use is
  collaboration-governed (already in her pipeline: Gemini 3.0 + Opus 4.7).
- **Do NOT** compute or report the crossover-age trajectory (the boundary, §2).
- **Reachability honesty:** if a subset is well below the floor, report that plainly —
  do not force a de-fogged result. This is a feasibility study; a "marginal / not
  reliably applicable" verdict is itself a valid and useful outcome.
- **Convergence:** if a fit fails to converge, report it; do not silently tweak.
- No silent parameter reduction (standing rule).

## 7. Compute

1–3 cc-library fits, ~minutes each on sapphire (**single fits, not a grid — does not
tie up sapphire during travel**). Reuse the refit launch pattern (spawn / atomic /
root-fs TMPDIR / per-unit seed; base seed `20260620`).

## 8. Outputs / artefacts

`runs/2026-06-20-women-corpus-feasibility/`: `spec.md`, `code/` (adapter + driver),
`outputs/` (per-fit JSON + `p_gen` arrays, the genuine-vs-raw comparison figure, the
reachability table), `MEMO.md` (the one-pager for Denmark). Conform to the exemplar
template (`runs/2026-06-18-province-size-regression/`).

## 9. Open items for sign-off

1. Scope boundary (no crossover trajectory) — **CONFIRMED** (Shawn 2026-06-20).
2. Worked-example boundary (method vignette in JAMT; substantive history in companion)
   — **CONFIRMED** (Shawn 2026-06-20).
3. **Need from Adela:** the canonical 813-daughter dataset **and her exact
   datable/conjugal filter definitions** (+ ideally her `tempun` SPA output to overlay).
   Requested; expected this evening.
4. Date window 50–349 CE — confirm matches her analysis.
5. Per-subset fits (overall + wives + daughters) for reachability — confirm scope is
   acceptable within the boundary.
