# Layer B — staged inputs and provenance (2026-06-16)

All Layer-B inputs staged on **sapphire** (the default run host) and verified
this session. Recorded here as re-checkable anchors.

## Layer-A trajectory posteriors (gitignored; zbook + rpi-server backup + sapphire)

`runs/2026-05-30-s5-small-n-trajectories/code/production/`

| File | Size (bytes) | Notes |
|---|---|---|
| `monolithic-inscription-25y.nc` | 1218429538 | **primary**; sha256 below |
| `monolithic-inscription-50y.nc` | 629817698 | bin-width sensitivity |
| `monolithic-letter-25y.nc` | 1211871686 | letter-mass unit |
| `monolithic-letter-50y.nc` | 626126406 | letter-mass, 50y |

- **sha256 (`monolithic-inscription-25y.nc`), zbook == sapphire:**
  `21e9856693cbcd13d7c5d3ed7241020eebdfe09eff081b491c2185c983524f14`
- **Primary `lam` dims (read on sapphire):** chain 4 × draw 2000 × city 268 ×
  bin 16 ⇒ **8,000 posterior draws**, 268 *target* cities (anchors excluded).

## H3a β posteriors (on sapphire; also on amd-tower)

`runs/2026-06-04-h3a-confirmatory/outputs/`

| File | Size (bytes) | β_within median [95% CI] | n cities / prov |
|---|---|---|---|
| `idata-primary.nc` (empire) | 113223938 | 0.5869 [0.5187, 0.6574] | 1044 / 56 |
| `idata-latin.nc` (Latin) | 88162218 | 0.7331 [0.6483, 0.8198] | 817 / 39 |

β values re-read from `runs/2026-06-04-h3a-confirmatory/outputs/h3a-results.json`
(`primary.betas.beta_within`, `sensitivity_B_latin.betas.beta_within`).

## Dataprep cache — for the anchor validation gate (on sapphire; 1.3 MB)

`runs/2026-05-30-s5-small-n-trajectories/code/prepared/` — 275 `aoristic-*.npz`
(incl. `aoristic-ostia.npz`, `aoristic-pompeii.npz`) + `city-index.parquet`.

## Hanson population anchor

`data/hanson2016/hanson2016_cities_oxrep.csv`, column `urban_context_pop_est`
(one static estimate per city).

## Sapphire `.venv` (verified read of the arviz-1.1 posteriors)

arviz 1.1.0 · h5netcdf 1.8.1 · xarray 2026.4.0 · pymc 6.0.1.
