---
title: "Letter-count probe — sensitivity of SPA shape and Hanson scaling to unit-of-analysis choice"
audience: "Shawn (PI); future readers reproducing the annex; Stage 3 design follow-up"
status: spec — pre-implementation; design locked 2026-05-26
date: 2026-05-26
related-artefacts:
  - runs/2026-05-21-talk-prep/code/   (template pipeline; adapted, not modified)
  - planning/h2.1-stage-3-implementation-plan-2026-05-25.md   (downstream consumer)
  - docs/notes/reflections/continuity.md §"Martin Eftimoski consultation outcome — recalibration (2026-05-26)"
---

# Letter-count probe — specification

## Motivation

The 2026-05-25 Martin Eftimoski consultation surfaced a substantive nudge: switching the unit of analysis from inscription count to letter count is "crucial" — the letter is a better basic unit for evaluating epigraphic production and information flow. This probe tests whether the unit-swap materially changes (a) the SPA temporal shape, (b) the Hanson scaling exponent β, and (c) the within-province variance partition that drives the slide-6 punchline.

Result feeds back into the Stage 3 (empirical-Bayes mixture) design — Stage 3 will adopt whichever unit the probe identifies as primary.

## Scope and time-budget

Freestanding annex, not folded into Stage 3 yet. Wall-clock target: complete within today's session (~ 5 hours of pipeline + report time). No new statistical methodology; weight-swap on an existing pipeline.

## Locked design decisions

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| 1 | Text field for letter count | **Both** `clean_text_conservative` AND `clean_text_interpretive_word` — as a sensitivity pair | Robustness against the interpretive-supply judgement; pre-empts reviewer objection |
| 2 | Date-window filter for Hanson NBR | **Match prereg** (Decision 22 — date-window-filtered counts) | Keeps Stage 3 downstream comparable; cumulative-totals variant logged to continuity tertiary backlog #5 |
| 3 | Province / city top-N selection | **Present both** — same ranks as 2026-05-21 inscription-count selection, plus letter-total re-ranking; note where ranks change | Different views answer different questions; cheap to compute both |
| 4 | Verdict thresholds | Three flags (below) | Pre-committed to limit confirmation bias on output |
| 5 | Output framing | Freestanding annex; Stage 3 picks "winning" unit afterwards | Don't entangle decisions |

## Letter-count computation

Compute per row from each text field independently:

```python
import re
LATIN_GREEK_LETTER = re.compile(r"[A-Za-zΑ-Ωα-ωÀ-ÿ]")  # Latin + Greek; includes diacritics
letter_count_conservative   = len(LATIN_GREEK_LETTER.findall(text_conservative_or_empty))
letter_count_interpretive   = len(LATIN_GREEK_LETTER.findall(text_interpretive_or_empty))
```

Rules:

- Strip spaces and punctuation by counting only alphabetic characters via the regex above.
- `NA` in the source text field → letter count = 0 (treated as "no readable letters under this cleaning"). Surfaced in descriptive output, not papered over.
- Greek and Latin both counted as letters; no script-specific weighting.
- No row-dropping based on letter count = 0; those rows are real data and a real signal.

## Pipeline

```
01-compute-letter-counts.py
    Input:  runs/2026-05-21-talk-prep/data/lire-filtered.parquet  (180,609 rows, already
            filtered to 50 BC – AD 350 per prereg envelope)
    Adds:   letter_count_conservative, letter_count_interpretive (two int columns)
    Output: data/lire-filtered-with-letters.parquet
    Plus:   outputs/tables/letter-count-descriptive.csv (n, median, IQR, mean,
            max, zero-count rate, by text-field choice)
    Plus:   outputs/figures/fig-01-letter-count-histograms.png (2 panels, one
            per text-field choice; log y-axis)

02-empire-spa-letter.py
    Inputs: lire-filtered-with-letters.parquet
    Computes the empire-wide SPA three ways:
        - inscription-mass    (weight = 1.0; matches 2026-05-21 figure)
        - letter-mass (conservative)
        - letter-mass (interpretive)
    Each row's mass distributed uniformly across [not_before, not_after] in
    5-y bins on [50 BC, AD 350] (prereg-canonical aoristic deposit).
    Output: fig-02-empire-spa-overlay.png  (three-line overlay, normalised
            to common max for shape comparison)
            fig-02b-empire-spa-absolute.png (three-line overlay, absolute
            mass — to surface the scale ratio)
            tables/empire-spa-pearson-r.csv  (Pearson r between inscription-mass
            and each letter-mass variant; bin-by-bin paired comparison)

03-province-city-spas-letter.py
    Per-province SPAs for top-N provinces (Rome excluded), under each
    weighting choice; same for top-N cities.
    Re-rank table: which provinces / cities change rank order when ranked
    by letter total vs inscription count? Output as
    outputs/tables/province-rank-change.csv  and  city-rank-change.csv.
    Figures: fig-03a-province-spa-grid.png (small multiples; one panel per
    province; three lines per panel),
    fig-03b-city-spa-grid.png (likewise for top-8 cities).

04-hanson-nbr-letter.py
    Frequentist NBR of city-level response on log Hanson population, three
    variants:
        - response = count(inscriptions per city)       (matches 2026-05-21)
        - response = sum(letter_count_conservative)     (new)
        - response = sum(letter_count_interpretive)     (new)
    1,000-replicate row-resample bootstrap 95% CI on β.
    Date-window: match the prereg H3a date-window filter (Decision 22).
    Outputs: tables/nbr-summary.csv (β, SE, 95% CI per variant);
             fig-04-nbr-beta-comparison.png  (forest plot or three-panel
             scatter with fitted line + bootstrap envelope per variant).

05-within-province-variance-partition.py
    Mundlak within-between decomposition (matches slide-6 punchline ~ 30 %
    within-province). Three response variants as in 04.
    Outputs: tables/variance-partition.csv  (within-share % per variant);
             fig-05-variance-partition-bars.png  (stacked bars, three
             panels).

REPORT.md
    Final verdict + figures + tables.
```

All scripts share the same paths convention as 2026-05-21 talk-prep code.

## Verdict thresholds (pre-committed)

Three flags, evaluated for each text-field choice (conservative, interpretive):

| Flag | Threshold for "no meaningful change" | Threshold for "material change" |
|------|--------------------------------------|---------------------------------|
| **SPA shape** (empire-level Pearson r, inscription-mass vs letter-mass, bin-by-bin) | r > 0.95 | r < 0.85 |
| **Hanson β** | Bootstrap-CI overlap substantial (point estimate of one falls inside other's 95% CI) | No CI overlap |
| **Within-province variance partition** | Shift < 2 pp (percentage points) | Shift > 5 pp |

Intermediate ranges (0.85–0.95 r; partial CI overlap; 2–5 pp shift) → "modest shift, document and proceed".

**Action rules**:

- All three quiet (no meaningful change for both text-field choices) → keep inscription-count as primary unit; letter-count documented as robustness annex.
- Any one flag tripping at the upper threshold for either text-field choice → letter-count becomes the headline unit for Stage 3 and forward.
- Mixed signal (one text-field choice trips, the other doesn't) → escalate to Shawn for design call; do not auto-decide.

## Out of scope (explicitly)

- Cumulative-totals (envelope-aggregate) version of the Hanson NBR — logged to continuity tertiary #5 for later.
- Bayesian (Mundlak / pymc) refit under letter-count weighting — happens at Stage 3 if and only if letter-count is selected as primary.
- §5 small-N city-trajectory analyses under letter-count — separable; deferred.
- Mixture-model recovery-grid re-run under letter-count weighting — separable; deferred.
- Sensitivity to inscription type (epitaph share etc.) — descriptive only in 01's output; not its own analysis here.

## Reproducibility

- Random seed for bootstrap: `20260526` (today's date, NUMERIC `int()` cast).
- All scripts callable from project root via `.venv/bin/python runs/2026-05-26-letter-count-probe/code/<script>.py`.
- A `runs/2026-05-26-letter-count-probe/RUN-LOG.md` will be appended after each script with timestamp + wall-clock + headline output.
- All figures + tables copied to `outputs/` only; nothing mirrored into `planning/` (this is an annex, not a paper-facing artefact yet).

## Critical-friend review notes (against standing-rule four-test)

a. **More appropriate test for the data structure?** NBR on counts is appropriate for both unit choices. The letter-total response is technically over-dispersed counts (more so than inscription counts because letters per inscription is itself dispersed) — NBR handles this. No more appropriate alternative for the comparator role this script plays.
b. **More powerful / robust alternative?** A city-level Bayesian Mundlak NBR (the prereg-specified H3a) is more powerful but is downstream — Stage 3 inherits the unit choice from this probe.
c. **More current best-practice approach?** Letter-count as unit is itself the best-practice nudge from Martin; the comparator pipeline is current.
d. **Do assumptions hold?** Standing reservation: row-resample bootstrap propagates within-city sampling variability but treats Hanson populations as fixed. Same standing caveat as 2026-05-21 talk-prep; not introduced by this probe.

## Definition of done

- All five script outputs present and inspectable.
- REPORT.md with verdict against all three thresholds, for both text-field choices.
- Pre-commit critical-friend pass to surface any anomalies that need Shawn's attention before commit.
- Single batched commit to git; not pushed without Shawn's call.
