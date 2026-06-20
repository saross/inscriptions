# Memo — convention de-fogging of the wives/daughters corpus (feasibility)

**To:** Adela Sobotkova (co-author) · **From:** Shawn Ross (with Claude Code) ·
**Date:** 2026-06-21 · **Re:** "From Graveyard to Time Series" — can our
editorial-convention de-fogging sharpen the *timing* of your datable conjugal
corpus? · **Status:** Stage-1 feasibility; methodological only.

> **Scope (agreed):** this is a *feasibility* check — genuine-vs-raw temporal
> de-fogging and a reachability verdict. It does **not** compute the
> wife-vs-daughter crossover-age trajectory; that substantive result is reserved
> for the companion (EJA) paper. Operational `datable`/`conjugal` filters are
> ours and need your confirmation before any number is quoted (see §4).

## The short answer

**De-fogging cannot reliably sharpen the time-resolution of this corpus as it
stands.** The datable conjugal corpus is **~90 % editorial-convention dated** and
sits **below / at the reliability floor** of the method. So the *timing* of the
crossover trough cannot be put on firmer ground by convention-correction here —
which is itself useful to know: it tells us the trough's timing rests on a
temporal distribution that is mostly editorial artefact, and the honest move is to
hedge the timing claim accordingly rather than over-read it.

## The numbers (canonical `data/women.csv`, 504 daughters)

Datable conjugal corpus: **1,291** inscriptions (838 wives, 453 daughters), fitted
with our production cross-classified deconvolution (same model as the JAMT paper's
29 units). "α" below is the **convention fraction** — the share of apparent dating
that is editorial round-number convention, not a real date signal (so 1 − α is
genuine).

| subset | N | convention fraction α | 95 % CI | reachability |
|---|---|---|---|---|
| overall | 1,291 | **0.90** | [0.81, 0.99] | marginal on N; α far above envelope |
| wives | 838 | 0.90 | [0.80, 1.00] | marginal on N |
| daughters | 453 | 0.84 | [0.75, 0.98] | **below the 500 floor** |

All three fits converged cleanly (R̂ ≈ 1.003, ESS ≈ 1 000–1 500, 0 divergences).

## Why "not reliable" (two independent reasons)

1. **Too convention-dominated.** Our method has a validated operating envelope of
   **convention fraction α ≤ ~0.70**; above that the genuine component is too
   weakly constrained to trust. Your corpus is α ≈ 0.84–0.90 — well outside it.
2. **Too small for the hard regime.** The reachability floor is N ≈ 500 for *easy*
   (low-α) subsets, rising to **N ≈ 2,000 for hard (high-α) ones**. Your corpus is
   high-α, so the worst-case floor applies: overall (1,291) and wives (838) are
   *marginal*; daughters (453) is *below even the easy floor*.

The de-fogged genuine SPD (Figure `fig-women-genuine-vs-raw`) shows this directly:
the 95 % band is very wide — the genuine temporal shape is highly uncertain.

## What this means for the crossover paper

- The **crossover trough's timing** (your C2–C3 inflection, ~AD 150–275) is read
  off a temporal distribution that is ~90 % editorial convention. De-fogging can't
  rescue the time-resolution, so the timing claim should be **hedged** (it may be
  robust to convention for other reasons — e.g. if the trough is driven by the
  *ages*, which `tempun` handles, rather than the *dating* — but convention
  de-fogging does not add confidence to the *when*).
- This does **not** undermine the substantive crossover-age result (the *ages* and
  their Monte-Carlo treatment are your `tempun` pipeline's domain, which we are not
  touching). It is specifically a statement about the **datability/timing** axis.
- A larger or more tightly-dated subset (e.g. inscriptions with narrower intervals,
  or a securely-dated sub-corpus) could move into the reliable envelope — worth
  exploring if the timing claim is load-bearing.

## §4 — confirm before we quote any figure to anyone

- Our operational **`conjugal`** = role ∈ {wife, daughter} ∧ type = familial (the
  whole file); **`datable`** = valid `not_before`/`not_after` overlapping 50 BC –
  AD 350. Do these match your definitions? Any `link_status` / `confidence` gate?
- Your analysis window (we used the model's −50 … 350; your interest is ~50–349 CE).
- If you can share your `tempun` SPA output, we can overlay genuine-vs-raw-vs-tempun.

*Reproduce:* `runs/2026-06-20-women-corpus-feasibility/` (driver
`code/run_women_feasibility.py`, figure `code/fig_women_genuine_vs_raw.py`).
Collaboration data — not for publication without Adela's involvement.
