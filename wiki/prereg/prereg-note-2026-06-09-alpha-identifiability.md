---
title: "Prereg note (DRAFT) — α identifiability limit of the shared convention basis"
status: DRAFT — for inclusion in the next OSF amendment (not a stand-alone lodgement; Shawn 2026-06-09)
date-drafted: 2026-06-09
scope: "Post-hoc disclosure of a structural identifiability limitation of the H2.1 temporal-mixture's shared convention basis (Decision 38 / Amendment 03) for temporally-concentrated units, the four reporting responses adopted, the added Italia unit, and the planned informed-α remediation."
relates-to: "Amendment 03 (osf-amendment-2026-06-07-convention-basis); H2.1 production run (runs/2026-06-07-h2.1-launch-prep/); diagnostic runs/2026-06-07-h2.1-launch-prep/outputs/production/DIAGNOSTIC-alpha-identifiability-REPORT.md"
---

# Prereg note (DRAFT) — α identifiability limit of the shared convention basis

> **⚠ "Planned remediation" (§ below) is SUPERSEDED (2026-06-09).** That section
> still describes the **informed-α prior**, which has since been **REFUTED** (a prior
> over a partially-identified region is never updated by data — Gustafson 2010;
> `runs/2026-06-09-informed-alpha/`). The actual remediation is the **joint model**
> (flexible per-unit basis + grid-alignment **classification likelihood** sharing α),
> validated by POC and under full recovery-grid validation —
> `runs/2026-06-09-joint-identifiability/` (`POC-REPORT.md`, `full-grid-spec.md`). The
> diagnosis (§§ "The limitation" / "The diagnostic" / "Reporting responses adopted")
> still stands. This note is folded into the next OSF amendment, which **reverses
> Amendment 03's shared basis**. Read the diagnosis here; take the remediation from the
> joint-identifiability run.

## What prompted this

The H2.1 temporal-mixture production run (2026-06-08; 28 units, all converged)
returned convention fractions α spanning 0.001–0.88. A post-run diagnostic, on
the question "are such low/high α plausible given the actual inscription date
ranges?", found that the **shared, fixed convention basis** (Decision 38 /
Amendment 03 §3 — a single empire/Latin basis shared across all units, chosen so
a per-unit basis would not absorb a unit's genuine signal) **under-identifies α
for temporally-concentrated units**. This note discloses the limitation, the
reporting responses adopted, and the planned remediation. It is a post-hoc
finding; the preregistered method stands where α is identifiable.

## The limitation

α is identified only when a unit's editorial-convention (round-period) dating
matches the *temporal shape* of the shared basis (broad; Latin centroid ≈ 144 AD,
spread across 50 BC – AD 350). For units whose round-period dating is **concentrated
in a narrow window** — predominantly frontier/military provinces whose epigraphy
clusters in their Roman occupation period (≈ AD 100–300), where their *genuine*
signal also lives — convention and genuine are confounded in time. The smooth
genuine component (GRW) then absorbs the period-concentrated convention mass and
α collapses. The "corrected genuine SPA" for these units consequently retains
convention masquerading as genuine.

This is a structural identifiability limit, not a fitting artefact: a per-unit
basis *over*-attributes instead (it absorbs genuine signal — e.g. Salona α 0.54 →
0.99 under its own basis), so neither basis is correct and the temporal
distribution alone cannot pin the split. It is larger than the documented
α-diagnostic imprecision (Amendment 01's shape-conditioned ±0.18 limits of
agreement): the worst unit's range spans ≈ 0.82.

## The diagnostic (how affected units are identified)

The independent signal the temporal shape ignores is the **family classification /
grid-alignment** of the dating intervals (interval width + round endpoints) — the
"observable proxy for the criterion LIRE's `raw_dating` does not preserve"
(Decision 38). Comparing each unit's fitted α to its F1+F3 (grid-aligned)
family-mass fraction:

- **shared α ≈ family fraction** ⇒ α trustworthy (the well-identified units,
  including the empire and Latin aggregates, Latium, Noricum, Pompeii, Dalmatia,
  Etruria, and the Italia aggregate below);
- **shared α far below the family fraction** (gap > ~0.25) ⇒ under-attribution.
  On the production corpus this flags **≈ 9 units**: Moesia inferior, Samnium,
  Pannonia inferior, Venetia et Histria, Numidia, Salona, Britannia, Umbria,
  Ostia (with several further borderline cases).

(The raw basis-swing between shared and per-unit fits over-counts the problem,
because it also fires on per-unit over-attribution where the shared α is already
correct; the shared-α-vs-family-fraction gap is the operative flag.)

## Reporting responses adopted (post-hoc)

1. **Identifiability flag in the tiering** — units whose shared α falls far below
   their grid-alignment family fraction are flagged `under-identified`; their
   convention correction is not reported as reliable.
2. **Two-bound α sensitivity range** — for flagged units, α is reported as a range
   [shared-basis lower bound, per-unit-basis upper bound] rather than a point;
   identifiable units keep a point estimate.
3. **Confirmatory H3b restricted to identifiable units** — deviation-detection
   confirmatory claims are made only on units with identified α; flagged units are
   treated as exploratory (or carry the convention/genuine uncertainty forward).
4. **Added analytical unit: Italia (excl. Rome)** — the 11 Augustan regiones
   aggregated (N ≈ 40,500; Rome is a separate province and is excluded by
   construction, consistent with Decision 36). Reported alongside the per-regio
   breakdown. Aggregating Italy materially improves identifiability (shared α 0.53
   vs family fraction 0.62, gap 0.09 — vs its constituent regiones at 0.30–0.52),
   giving a reliable Italian convention/genuine split where the individual regiones
   do not.

## Planned remediation (under exploration; will be recovery-validated before use)

An **informed-α prior**: replace the flat `Beta(1,1)` α prior with a prior centred
on the unit's grid-alignment convention fraction (a wide prior, so the data can
still move it), optionally paired with a per-unit convention *shape*. This injects
the independent grid-alignment information the temporal shape lacks — the same
"build what is known about the inscriptions into the model" principle as the
grid-quantisation reframe itself — pulling under-attributing units toward their
family fraction without the per-unit basis's over-attribution. Alternatives
considered and set aside as weaker: a hierarchical/partial-pooling basis (adds
flexibility, not information — the wrong lever for an identifiability problem) and
a constrained-smooth genuine GRW (risks mis-attributing genuinely sharp occupation
peaks to convention). Any remediation will be recovery-validated on a synthetic
grid (must recover the identifiable units unchanged and pull flagged units toward
their true α without over-attribution) before replacing the production fits.

## Honest framing

The preregistered shared-basis deconvolution stands where α is identifiable (the
aggregates and broad-convention units); this note quantifies its boundary for
temporally-concentrated units and records the conservative reporting adopted in
the interim. The remediation is a candidate, not a commitment, and is gated on its
own recovery validation.
