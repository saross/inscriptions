# Key-findings figure set — build spec

**Status:** DRAFT for Shawn's sign-off (2026-06-20). **Produce in a fresh session** (context
economy — this spec freezes every design + data decision so no re-derivation is needed).
**Author:** Claude Code (Opus 4.8) on Shawn's brief, 2026-06-20. UK/Australian English.
**Companion:** these figures illustrate `reports/key-findings-summary-2026-06-20.md` (v2) and the
paper; the summary carries `[FIGURE: …]` placeholders that map to F9 (variance partition) and F7
(within/between scatter).

---

## 1. Agreed design / visual language

- **Code-based, NOT Claude Design** (Shawn 2026-06-20). Claude Design reserved, at most, for one
  optional conceptual schematic; all data figures in code for reproducibility + statistical
  correctness + journal-spec vector output.
- **Stack:** Python + **matplotlib** (fine control over CI/fan/caterpillar encodings + vector
  output). One shared theme module `code/figtheme.py` (rcParams: serif font for journal; base
  sizes; tight layout; PDF + 300-dpi PNG preview per figure).
- **Encoding conventions (consistent across the set):**
  - **Corrected (genuine)** = solid, saturated; **uncorrected (raw aoristic)** = muted / dashed.
  - **Uncertainty** = translucent ribbon (SPD/time series), **fan** (trajectories, F8), or
    **caterpillar interval** (per-unit posteriors, F6). Always show 95% credible bands; never a
    bare median line for a posterior quantity.
  - **Frame colours fixed:** one colour for *empire/all-provinces (context)*, one for
    *Latin-minus-Roma (primary)*; use the same two throughout.
  - Colourblind-safe, perceptually-uniform palettes (viridis/cividis for sequential; an
    Okabe–Ito-style qualitative set for categories).
- **Honest-framing rules baked into captions/labels (non-negotiable):**
  - F8 fans labelled **"illustrative relative shape — NOT a population estimate"** (Obs 96/103).
  - Keep the **two-α** distinction (genuine-fraction α vs NBR dispersion α) out of captions that
    don't need α; never conflate.
  - Obs 101 language: "association with Hanson's population estimates"; "empire-wide common
    temporal component" (never "epigraphic habit" in a figure title); results model-conditional.
- **Outputs:** `outputs/figXX-*.{pdf,png}` + a `figindex.md` mapping each figure → its data
  source(s) → its build script. One script per figure under `code/` (or a figures module),
  reproducible (seeded where it samples).

---

## 2. Verified numbers (FROZEN — use these; re-confirm at source when plotting)

All re-verified at source this session (accuracy-certified set, `planning/doc-accuracy-audit-2026-06-20.md`):

- **Genuine-fraction α:** empire 0.6798 [0.6649, 0.6970]; Latin-aggregate 0.7387 [0.6596, 0.7893]
  (Obs 111).
- **Temporal decomposition** (`runs/2026-06-17-s5-h5-habit-removed/outputs/h5-decomposition.json`):
  empire-common SD 1.1103 (peak AD 187.5), province SD 1.0195, city SD 0.9759, level SD 0.7765
  (all-provinces) / 0.7851 (Latin-minus-Roma); common share of temporal var 0.540.
- **H3a** (`runs/2026-06-04-h3a-confirmatory/outputs/REPORT.md`): f_within Latin **0.480**
  [0.401, 0.566], empire **0.299** [0.240, 0.365]; β_within 0.587 empire / 0.733 Latin;
  β_between empire −0.242 [−0.701, 0.238] (crosses zero).
- **H9 letter-mass** (`runs/2026-06-18-h9-letter-mass-h3a/`): f_within 0.448 [0.364, 0.535],
  β_within 0.681 [0.595, 0.769].
- **q-trajectory medians** (empire-β, reliable cities; Obs 103): AD 112 = 0.48, AD 188 = 1.01,
  AD 262 = 0.32, AD 338 = 0.67; v-only AD 262 ≈ 0.78.
- **Peak-scaling** (Obs 100/106): all-provinces raw-peak β 0.557 [0.490, 0.624] vs cumulative
  0.587; Latin 0.700 [0.618, 0.784] vs 0.733.
- **Capital contrast** (Obs 74): empire +0.96 [0.74, 1.21], Latin +1.08 [0.81, 1.41]; P(>0)=1.00
  in all periods (Obs 99/106).
- **A01 content vs scaling residual** (Obs 108): Spearman ρ +0.004 (p 0.913); letters~count slope
  0.971, R² 0.841.
- **Reachability** (Obs 96 / Decision 34): floor N≈500 (easy subsets) → worst-case N≈2,000;
  operating envelope α ≤ ~0.70.

---

## 3. Data availability

- **LOCAL — ready to plot now:** cc `p_gen` draws, 29 units
  (`runs/2026-06-13-cc-production-refit/outputs/posterior-draws/*-pgen.npz`); Layer-B residual
  q-trajectory idata (`runs/2026-06-17-s5-layer-b-residual/outputs/layerb-residual-trajectories-{empire,latin}.nc`);
  `h7-summary.json`; `content-residual-per-city.csv`; reachability REPORT/json; `h3c-results.json`
  (+ latin); `peak-scaling-summary.json`; `h9-results.json`; the H3a city frames
  (`data/processed/city_level_for_h3a*.parquet`). Raw (uncorrected) aoristic SPDs are recomputed
  from the corpus via `h2_lib.aoristic_spa` (local).
- **NEEDS A SAPPHIRE REGEN (one step):** the §5 small-N monolithic idata
  (`runs/2026-05-30-s5-small-n-trajectories/code/production/monolithic-inscription-25y.nc`,
  gitignored) — required only for **F13** (per-province SPD atlas) and any **per-small-N-city**
  SPD-with-uncertainty. F4 can use the 5 anchor cities from the cc draws instead, so the atlas is
  the only figure that strictly needs the regen.

---

## 4. Figure list (all approved by Shawn 2026-06-20)

Each: what it shows · panels · data · encoding/uncertainty · framing notes · base figure to
upgrade (if any) · status.

- **F1 — Deconvolution before/after (hero/explainer).** Empire raw lumpy SPD (convention round-slab
  spikes highlighted) → genuine smooth SPD, with 95% bands. *Data:* cc empire `p_gen` draws +
  recomputed raw aoristic. *Framing:* the method's value (summary §1). *Base:* martin-consultation
  `spa-uncorrected.png` / `spa-slab-*.png`. *Status:* ready.
- **F2 — Empire + Latin SPD, corrected vs uncorrected, with uncertainty.** Two-frame overlay or
  2×2 panel. *Data:* cc empire + latin-aggregate `p_gen` draws + raw. *Base:* `fig-04a-empire-spa`.
  *Status:* ready.
- **F3 — Province-level SPD, corrected vs uncorrected, with uncertainty.** Small-multiple of the
  fitted province units (or a chosen informative subset). *Data:* cc province-unit `p_gen` draws.
  *Base:* `fig-04b-province-spa`. *Status:* ready.
- **F4 — City-level SPD, corrected vs uncorrected, with uncertainty.** The anchor cities (Ostia,
  Pompeii, Salona, Aquileia, Mogontiacum) from cc draws. *Note:* small-N city trajectories are the
  §5 model (F13/atlas), not these. *Data:* cc city `p_gen` draws. *Status:* ready.
- **F5 — Letter-count (content) SPD analogue, with uncertainty.** Content-measure SPD(s), framed
  to parallel F2 but distinct. *Data:* `h9-results.json` / letter-count-probe outputs. *Base:*
  `fig-02-empire-spa-overlay-*` (letter-count-probe). *Status:* ready.
- **F6 — Capital over-production caterpillar/forest.** Per-period capital contrast posteriors with
  95% CIs, both frames; a reference line at 0 to show "always > 0". *Data:* `h3c-results.json` +
  per-period contrasts (h7). *Status:* ready.
- **F7 — Population–epigraphy scatter (within vs between).** Two-panel log–log: (a) within-province
  (steep, supported, β_within 0.733 Latin) with CI ribbon, capitals highlighted; (b)
  between-province (flat/uncertain, β_between crosses zero). *Data:* H3a city frame + fitted
  posterior. *Framing:* "association"; the summary's `[FIGURE: within/between]` placeholder.
  *Base:* `hanson-scaling-nbr-bootstrap.png`. *Status:* ready.
- **F8 — Relative-trajectory fans (the reframed #7).** Median city q vs empire trend over time as
  an uncertainty **fan**, with the independently-dated anchors (Ostia, Pompeii) marked; **label
  "illustrative relative shape, NOT a population estimate."** Optionally the v-only (city-specific)
  overlay. *Data:* `layerb-residual-trajectories-{empire,latin}.nc` (local). *Base:*
  `layerb-residual-*`. *Status:* ready.
- **F9 — Variance-partition composition.** Stacked bar / nested composition of the four components
  (empire-common, province, city, level) showing relative sizes + the ~54% common-share. *Data:*
  `h5-decomposition.json`. *Base:* `fig-05-variance-partition-bars.png` (upgrade). *Status:* ready.
- **F10 — β scaling exponent over time (U-shape).** Line + 95% CI ribbon across the 8 periods,
  both frames; the ~0.58 high-empire plateau annotated. *Data:* `h7-summary.json` + h7-latin.
  *Status:* ready.
- **F11 — Two-measure orthogonality scatter.** Acts-residual (x) vs content-residual (y), ρ ≈ 0
  annotated; shows "prolific for size" and "verbose per act" are independent. *Data:*
  `content-residual-per-city.csv`. *Base:* `content-residual-space-map.png`. *Status:* ready.
- **F12 — Reachability map (the instrument's spec sheet).** N × α grid shaded by de-foggability
  (reliable / marginal / unreached), with the operating-envelope boundary. *Data:* reachability
  REPORT/json. *Status:* ready.
- **F13 — Per-province corrected-SPD atlas (optional, approved).** Small-multiple chronology of
  the provinces. *Data:* §5 monolithic idata — **NEEDS sapphire regen** (or build from cc province
  units as a fallback). *Status:* needs regen.

---

## 5. Build plan (fresh session)

1. **(If F13 / per-small-N-city wanted)** regen `monolithic-inscription-25y.nc` on sapphire
   (the §5 small-N trajectory fit; reuse its existing code). Otherwise skip — all other figures
   are local.
2. Write `code/figtheme.py` (the shared theme) FIRST; lock the palette/fonts/format.
3. Build F1–F12 from local data (one script each → `outputs/figXX-*.{pdf,png}`).
4. Build F13 after the regen (or the cc-province fallback).
5. Write `outputs/figindex.md` (figure → data source → script → which summary `[FIGURE]` it fills).
6. Commit per logical batch; gitignore any large regenerated `.nc`.

## 6. Sign-off

Confirmed by Shawn 2026-06-20: code-based approach + visual language; the F7→within/between and
F8→relative-trajectory framing; all 13 figures incl. the optional atlas. **Open for the build
session:** (a) regen the §5 `.nc` on sapphire for F13, yes/no; (b) any palette/format preference
beyond the defaults above; (c) target dimensions (journal column vs full-page) per figure.
