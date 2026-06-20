# Key-findings figure set — index

Built 2026-06-20 (Claude Code, Opus 4.8) on Shawn's brief, per
`runs/2026-06-20-figures/spec.md`. UK/Australian English; BC/AD era notation.

**Target journal:** Journal of Archaeological Method and Theory (JAMT, Springer).
**Format:** vector PDF (submission artefact) + 600-dpi PNG preview per figure.
**Theme:** `code/figtheme.py` — sans-serif (Nimbus Sans, Helvetica-metric),
single-column 84 mm / full-width 174 mm, Okabe–Ito frame pair (empire = blue,
Latin-minus-Roma = vermillion), viridis/cividis sequential.
**Shared data access:** `code/figdata.py` (grid, raw aoristic + convention
component via `h2_lib`, genuine `p_gen` draws, quantile bands).

All figures reproducible: `cd code && ../../../.venv/bin/python figNN_*.py`.

**Plain-language captions** (for non-statistician readers — "what is this? / what
does it mean? / why does it matter?") are in **`figure-captions.md`**.

| Fig | File stem | Width | What it shows | Data source(s) | Build script |
|-----|-----------|-------|---------------|----------------|--------------|
| F1 | `fig01-deconvolution-before-after` | 1-col | Empire deconvolution before/after (hero); convention component highlighted | cc `empire-aggregate-pgen.npz` + raw aoristic (`h2_lib`) | `fig01_deconvolution_before_after.py` |
| F2 | `fig02-empire-latin-spd` | full | Empire + Latin SPD, raw vs genuine + 95 % band | cc `empire-aggregate` / `latin-aggregate` draws + raw | `fig02_empire_latin_spd.py` |
| F3 | `fig03-province-spd` | full | 6-province small-multiple, raw vs genuine (core → frontier) | cc province draws + raw | `fig03_province_spd.py` |
| F4 | `fig04-city-spd` | full | 5 anchor cities; Pompeii AD 79 external check | cc city draws + raw | `fig04_city_spd.py` |
| F5 | `fig05-letter-content-spd` | 1-col | Letter-mass (content) SPD tracks the inscription SPD (raw) | `empire-spa-three-ways.csv` (letter-count-probe) | `fig05_letter_content_spd.py` |
| F6 | `fig06-capital-overproduction` | full | Capital over-production: overall forest (95 % CI) + per-period medians | `h3c-i-results-oxrep-primary.json`; `h7-summary.json` + `h7-latin-summary.json` | `fig06_capital_overproduction.py` |
| F7 | `fig07-pop-epigraphy-within-between` | 1-col | **Within vs between scaling** (β_within 0.73 steep; β_between 0.04 crosses 0) | `city_level_for_h3a_latin.parquet` + `h3a-results.json` (Latin) + capital list | `fig07_pop_epigraphy_scatter.py` |
| F8 | `fig08-relative-trajectory-fan` | full | Relative city trajectory; "illustrative shape, NOT a population estimate" | `layerb-residual-trajectories-empire.nc` | `fig08_relative_trajectory_fan.py` |
| F9 | `fig09-variance-partition` | 1-col | **Magnitude of nested log-rate components** + ~54 % common share | `h5-decomposition.json` | `fig09_variance_partition.py` |
| F10 | `fig10-beta-over-time` | 1-col | β_within over 8 periods (U-shape, ~0.58 plateau, sublinear) | `h7-summary.json` + `h7-latin-summary.json` | `fig10_beta_over_time.py` |
| F11 | `fig11-orthogonality-scatter` | 1-col | Scaling vs content over-production are orthogonal (Spearman ρ +0.004) | `content-residual-per-city.csv` | `fig11_orthogonality_scatter.py` |
| F12 | `fig12-reachability-map` | 1-col | N × α reachability heatmap + operating envelope | `reachability-by-cell.csv` (small-n-reachability) | `fig12_reachability_map.py` |
| F13 | `fig13-province-atlas` | full | Per-province genuine-SPD atlas (25 provinces, §5 hierarchical model) | `monolithic-inscription-25y.nc` + `city-index.parquet` | `fig13_province_atlas.py` |

## Summary `[FIGURE]` placeholders (spec §intro)

- **`[FIGURE: variance partition]`** → **F9** (`fig09-variance-partition`).
- **`[FIGURE: within/between]`** → **F7** (`fig07-pop-epigraphy-within-between`).

## Companion numerical deliverable

- `temporal-three-way-split.json` (`compute_temporal_split.py`): the exact
  per-city three-way temporal variance split from the monolithic `.nc`. The
  common share reproduces the published 54 % (guard-checked); the three tiers are
  **anti-correlated** (marginal shares sum to 131 %, covariance remainder −31 %),
  so they do not partition cleanly. Three candidate normalisations recorded
  (marginal / covariance-attributed / proportional-remainder) — **awaiting
  Shawn's choice** for how to report the province/city split (the summary's
  indicative 54/24/22 is the proportional-remainder method, which hides the
  covariance).

## Honesty / framing notes baked in

- F1: framed as convention *removal* + peak *recovery* (genuine is peakier than
  raw — Obs 94), NOT "smoothing".
- F8: "illustrative relative shape — NOT a population estimate"; anchors held out.
- F9: SD magnitudes (not a forced partition); Obs 101 language ("empire-wide
  common temporal component", not "epigraphic habit").
- F13: §5 trajectory model (a different correction from the F1–F4 deconvolution);
  small-N cities, anchors held out.

## Data needing a host copy (gitignored)

- `monolithic-inscription-25y.nc` (1.22 GB) + `prepared/city-index.parquet`:
  copied from sapphire (md5-verified). No regen was needed — the original
  2026-05-31 run's posteriors were intact on sapphire/zbook.
