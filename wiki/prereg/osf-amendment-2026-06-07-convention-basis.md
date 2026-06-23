---
title: "OSF Amendment 03 — Convention component is an empirical calendar-slab basis (grid-quantisation reframe; no reign tier)"
amendment-number: 03
status: LODGED 2026-06-08 (OSF; Amendment 03; git tag osf-amendment-03-2026-06-08 → 90897d6). [Header corrected 2026-06-18: previously read "DRAFT … not yet lodged", which was stale — lodgement confirmed by the tag, the summary-addendum, and the 2026-06-14 continuity close.]
date-drafted: 2026-06-07
scope: "Redefine the H2.1 mixture's editorial-convention component (p_conv) as an empirical calendar-slab basis with NO reign tier; reclassify reigns/dynasties/datable events as genuine-but-aoristic; reframe the artefact as grid-quantisation of genuine-but-coarse evidence onto the BC/AD calendar lattice; ride decadal/quarter-century brackets as a sensitivity band. Gated on a fresh recovery re-validation."
preregistration: "https://osf.io/uycs6/ (lodged 2026-05-20; embargoed)"
lodged-version: "git tag osf-lodgement-2026-05-20 (https://github.com/saross/inscriptions/tree/osf-lodgement-2026-05-20)"
filed-under: "preregistration §7 / contingency clause (preregistration-draft.md line 423): substantive methodology changes after lodgement are filed as an OSF amendment before implementation."
author: "Shawn Ross (with Claude Code as analyst/RSE)"
gate: "BINDING — the H2.1 temporal-mixture production fit must not run until this amendment is lodged. The cross-sectional track (H3a/H3c/SR1, Amendments 01/02) uses date-window counts, not mixture output, and is NOT gated by this amendment."
relationship: "Independent of Amendment 01 (two-measure framework, lodged 2026-06-04) and Amendment 02 (Latin-primary frame, lodged 2026-06-06). Both used date-window counts; this one concerns only the temporal mixture's convention component. Separable lodgement."
skeleton-note: "§A5.5 filled 2026-06-08 from the full-grid PASS (B = 96.4 %; FULL-GRID-REPORT.md). justification.txt + summary-addendum generated this session; PDF pending. Awaiting Shawn's review + lodgement."
---

# OSF Amendment 03 — Convention component is an empirical calendar-slab basis (grid-quantisation reframe; no reign tier)

## Plain-language summary

Roman inscriptions are mostly dated by convention — "2nd century AD", "Hadrianic"
— rather than to a year. Our method separates that conventional dating fog from
the genuine timeline of inscribing. The lodged protocol modelled the convention
component as three hand-picked interval types (centuries, half-centuries, and
imperial-reign spans). On building the actual dictionary from the corpus, two
problems appeared: a large block of the conventional datings are *multi-century*
slabs ("[301,500]") that fit none of the three types, and reign spans turned out
to belong on the *genuine* side, not the convention side. This amendment makes
three connected changes:

1. **The convention component becomes an empirical, data-built basis** of calendar
   slab-types (sub-century, century, multi-century), with **no reign tier**. It is
   built directly from the corpus's own round-number datings rather than from a
   hand-picked dictionary.
2. **Reigns, dynasties, and datable events are reclassified as
   genuine-but-aoristic.** "Flavian" carries real historical information that "the
   later first century" does not; such dates are genuine signal with wide
   uncertainty, not editorial convention.
3. **We reframe what "convention" *is*.** It is not information-free editorial
   rounding; it is genuine-but-coarse evidence *quantised onto the BC/AD calendar
   grid*. The method removes that grid-snapping artefact (the boundary pile-ups and
   flat-within-bin shape) from the collective curve; it does not pretend to recover
   any single inscription's true off-grid date. Fine brackets (quarter-centuries,
   decade windows) are grid-snapped but low-distortion, so they ride as a reported
   sensitivity band rather than a hard classification.

Because this changes the model's structure, it is re-validated on fresh synthetic
data with known answers before any real fit, and the change is lodged before
implementation. The technical statement follows.

## A1. Identification and trigger

This is the third amendment to the project's preregistration (Open Science
Framework, OSF, record osf.io/uycs6/, lodged 2026-05-20, currently embargoed),
filed under the preregistration's own contingency rule (`preregistration-draft.md`
line 423). It is a **binding gate**: the H2.1 temporal-mixture production fit does
not run until this amendment is lodged.

**Trigger.** The pre-Phase-2 template-dictionary empirical scan (prereg line 202;
`runs/2026-06-05-template-dictionary/`) — a preregistered prerequisite for the
mixture fit — found the lodged curated three-tier convention dictionary
empirically inadequate: multi-century slabs are ~31 % of the F1+F3 convention pool
and fit none of the three curated tiers (the single most frequent template
corpus-wide is the multi-century `[301, 500]`, 8.8 %), while reign templates are
only ~2.7 % and, on inspection, belong on the genuine side. This fired Decision
20's own revisit trigger. The full deliberation is **Decision 38**
(`planning/decision-log.md`).

## A2. Summary of the change

Three connected changes to the **temporal mixture's convention component only**;
the model's likelihood, the F1/F3 structural fixes, the learned-weight count (3),
and the cross-sectional track are unchanged (§A6).

1. **Convention basis → empirical calendar slab-types, no reign tier** (§A5.1).
2. **Reigns / dynasties / datable events → genuine-but-aoristic** (§A5.2).
3. **Grid-quantisation reframe of the artefact** (§A5.3); fine brackets as a
   sensitivity band (§A5.4).

Lodgement is gated on a **fresh recovery re-validation** (§A5.5) because the basis
*shapes* change (they now carry a multi-century plateau), even though the learned
tier-weight count stays at the recovery-validated 3.

## A3. Rationale

- **The curated three-tier basis is empirically broken.** It has no home for the
  ~31 % multi-century mass and over-weights reign (~2.7 %). The recovery grid that
  returned 98.6 % α-coverage ran on *synthetic proxy* tier weights over the curated
  basis; **no real-LIRE three-tier mixture has ever been fit**.
- **Reigns are genuine, not convention.** The family classifier that operationalises
  the convention pool already holds reign intervals out (as "F2_Other"), and it
  even split reigns inconsistently by width-accident (`[117,138]` Hadrian held out;
  `[161,180]` Marcus leaked in). The lodged prereg's placement of a reign tier
  *inside* convention contradicts both the classifier and the conceptual reality.
- **Convention is grid-quantisation, not absence of information.** Every recorded
  date carries evidential anchoring (letterforms, onomastics, formulae, consular
  dates, find-context — Cooley 2012). What makes a date *conventional* is the
  arbitrary rounding of that genuine-but-coarse evidence onto the BC/AD calendar
  lattice. That snapping introduces (i) per-inscription distortion (an off-grid
  range truncated to a round century and flattened to uniform) and (ii)
  cross-inscription artificial alignment (many true distributions snap to the same
  bin, manufacturing the boundary pile-ups the SPA shows). The discriminator
  between convention and genuine is therefore **grid-snapping** (observable as
  grid-alignment), not criterion-type (which LIRE's `raw_dating` does not preserve).

## A4. Relationship to already-observed results (transparency)

This change is **method-structure, decided before any real-data mixture fit
exists** — there is no real-corpus `p_conv`/`p_gen`/α result to have steered it.
It was triggered by a descriptive *template-frequency scan* (counts of interval
shapes), not by any hypothesis-test outcome. The re-validation (§A5.5) runs on
synthetic data with known answers. The change therefore cannot be result-driven in
the confirmatory sense; it is a faithfulness correction to the convention model,
disclosed and re-validated before implementation.

## A5. Pre-specifications

### A5.1 Convention basis — empirical calendar slab-types (no reign tier)

`p_conv = tier_weights · tier_basis`, with `tier_weights ~ Dirichlet(ones(3))` over
a **fixed empirical basis** of three calendar-slab tiers — **sub-century**
(half-century), **century**, and **multi-century** (1.5- + 2- + 3-century, pooled)
— each row the frequency-weighted aoristic SPA of the anchor-stripped F1+F3
calendar population of that width-class. **No reign tier.** The basis is a fixed,
unit-independent convention template, built once per language frame (empire and
Latin) and shared across that frame's units; a per-unit basis would absorb genuine
temporal signal into `p_conv`. Artefact:
`runs/2026-06-06-convention-basis-redesign/design.json`
(`tier_basis_empirical[_latin]`).

### A5.2 Reigns / dynasties / events — genuine-but-aoristic

Date assignments tied to real historical anchors (reigns, dynasties, datable
events) are **genuine-but-aoristic** and are **not** modelled in `p_conv`; their
aoristic mass contributes to the observed SPA and is therefore attributed to the
genuine component. A curated historical-anchor interval list
(`runs/2026-06-06-convention-basis-redesign/historical-anchor-intervals.json`)
removes width-accidental reign/event leaks (empirically just `[161,180]`, 0.11 %
of the convention pool) from the basis-building population so the split is
non-width-accidental. Year-precise `[t, t]` dates remain genuine (unchanged).

### A5.3 Grid-quantisation reframe (prereg/paper §2)

Reframe the artefact as *genuine-but-coarse evidence quantised onto the BC/AD
calendar grid*, retiring the "editorial rounding ≈ no information" / "midpoint-
spike" description. Redescribe `p_gen` as *"the temporal distribution with the
calendar-grid quantisation removed"*, with the honest limit stated: the method
un-snaps the **collective** (removes the aggregate boundary pile-ups and
flat-within-bin shape under the GRW smoothness prior); it does **not** reconstruct
any single inscription's true off-grid latent distribution. This is distinct from
radiocarbon SPD (genuine measurement uncertainty, no arbitrary rounding) and likely
shared with ceramic typological dating (round-period pinning).

### A5.4 Fine brackets — sensitivity band

Decadal and quarter-century brackets (~4–5 % of the corpus) are grid-snapped
(convention side) but **low-distortion** (fine grid), so deconvolving them vs not
barely moves the result. They are **excluded from the primary `p_conv`** and added
back as a reported robustness band (the ceramics stacked-band idiom), not a hard
classification.

### A5.5 Recovery re-validation (the gate) — **PASS** (triage + full grid)

Grid A's 98.6 % validated the *old* basis shapes and does **not** transfer to a
multi-century-bearing basis (a long flat envelope-edge plateau is confusable with
genuine quiescence). The re-validation re-generates synthetics from the new
empirical basis and runs an **α = 0.95 × multi-century × peaked-genuine
stress-triage first**, then the full grid.

- **Stage-1 stress-triage: PASS** (2026-06-06). 8 cells, convergence 1.00; at the
  hardest corner the model recovers α to within +0.029 (0.979 vs true 0.95) — the
  multi-century plateau is attributed to convention, *not* confused for genuine
  quiescence. Scored under the Amendment 01 §A5.5.1 criterion (α-coverage = a
  shape-conditioned diagnostic, not a gate; shape + convergence binding).
- **Stage-2 full grid: PASS** (450 cells, 0 failed; sapphire, 2026-06-08). Headline
  **B = 96.4 %** of in-envelope (α ≤ 0.70) cells are clean passes (convergence AND
  shape), against the ≥ 90 % bar; diagnostic A = 97.2 %. The 13 in-envelope
  non-passes (3 non-converged + 10 shape-misses) concentrate in the peaked shapes
  (`regnal_cluster`, large-N `bimodal`); **the `multicentury_heavy` tier is NOT a
  systematic failure** (it clean-passes at the same rate as every other tier), so
  the §6 plateau-confusion failure mode is **absent at scale**, and α is recovered
  essentially unbiased (mean signed bias +0.005). The operating envelope (α ≤ 0.70)
  is confirmed; shape recovery collapses only at the out-of-envelope α = 0.95
  stress row. α-recovery precision (Bland–Altman 95 % LoA, in-envelope) is
  **[−0.12, +0.13]** pooled — shape-conditioned ±0.09 (smooth/flat) to ±0.18
  (multimodal) — **within Decision 33's ±0.18 envelope**, so the lodged
  shape-conditioned α-hedge carries over unchanged. Basis-shift vs the validated
  Grid A: 96.4 % vs 98.6 % (Δ −2.2 %; informational, not a regression target).
  REPORT: `runs/2026-06-06-convention-basis-redesign/revalidation/FULL-GRID-REPORT.md`
  (auto-tables `inscription-mass/outputs/REPORT.md`; α LoA
  `tables/alpha-loa-summary.json`).

### A5.6 Novelty positioning (verified)

The bracket-level convention-vs-genuine deconvolution survives a verified
forward-citation pre-emption chain from Crema 2025. **Cite-and-distinguish** the
nearest competitor — Tobalina-Pulido & Martín-Rodilla 2026 (`10.5334/jcaa.220`), a
fuzzy-logic framework that *quantifies/propagates* inherited dating uncertainty but
does **not** deconvolve convention from genuine spread. Method-level warrant:
**Crema 2025** (`10.1111/arcm.12984`). Dating-method authority: **Cooley 2012**
(`10.1017/cbo9781139020442`); current inscription-dating monograph **Hartmann
2025** (`10.46771/978-3-96769-729-2`).

## A6. What does NOT change

- **The mixture likelihood and the F1/F3 structural fixes** (`build_model_f1_f3`:
  `Beta(1,1)` α prior; non-centred GRW `p_gen`) are unchanged.
- **The learned tier-weight count stays 3** — the Dirichlet structure the recovery
  grid validated is structurally identical; only the basis *shapes* change.
- **The envelope (50 BC – AD 350, 5-y/80-bin) and the observation model**
  (largest-remainder multinomial) are unchanged.
- **The cross-sectional track** (H3a/H3c/SR1; Amendments 01/02) uses date-window
  counts, not mixture output, and is untouched.
- **Year-precise dates** remain genuine.

## A7. Changes by preregistration section (a standalone addition, not in-place edits)

- **§2 (the artefact description).** Reframed as grid-quantisation of
  genuine-but-coarse evidence onto the BC/AD lattice; retire the
  midpoint-spike/round-period-≈-no-information description.
- **§3 (the mixture / `p_conv`).** Convention component = empirical 3-tier
  calendar-slab basis (no reign tier); reigns/dynasties/events → genuine-but-aoristic;
  fine brackets → sensitivity band. Supersedes Decision 20's tier typing; refines
  Decision 37.
- **§3 (validation).** The H2.1 recovery validation is re-run on the new basis
  (§A5.5) before the production fit.

## A8. Provenance

- **Decision record:** Decision 38 (`planning/decision-log.md`); supersedes Decision
  20's reign tier; refines Decision 37.
- **Basis + anchor list:** `runs/2026-06-06-convention-basis-redesign/`
  (`design.json`, `historical-anchor-intervals.json`, `outputs/REPORT.md`).
- **Template-dictionary scan:** `runs/2026-06-05-template-dictionary/` (`6d8950f`).
- **Re-validation:** `runs/2026-06-06-convention-basis-redesign/revalidation/`
  (`spec.md`, `STAGE1-TRIAGE-REPORT.md`; full-grid REPORT pending).
- **Lodged authority:** the original supplementary (git tag `osf-lodgement-2026-05-20`)
  remains authoritative for all unchanged specifications.
- **Independence:** separable from Amendments 01 and 02 (both date-window-count
  based); this concerns only the temporal mixture's convention component.
- **Repository-state provenance:** the git lodgement tag for this amendment (to be
  created at lodgement) is the reproducibility anchor, distinct from any
  OSF-assigned amendment identifier.
