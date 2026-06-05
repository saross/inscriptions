# H3c(i) — provincial-capital residual contrast — REPORT (preliminary)

**Status:** PRELIMINARY — pending Shawn's sign-off. The **Latin frame** is additionally **pending OSF Amendment 02** (Decision 36 amendment-gate); nothing here is final.

**What this closes.** The 2026-06-05 preregistration-completeness audit (`planning/prereg-obligations-audit-2026-06-05.md`, F1) found that **H3c(i) — a binding confirmatory test — had never been run**: the H3a confirmatory run computed only H3c(ii) Moran's I. This report runs it, on both frames, off the existing H3a posteriors (no re-fit). It also answers secondary question **SR2(i)** (do provincial capitals over-produce inscriptions?).

## The test (prereg §3 line 81; §4 line 345; Decision 23)

Per posterior draw *s*: `contrast_s = mean(Pearson resid | provincial capitals) − mean(Pearson resid | non-capitals)`. **Confirmatory rule: `P(contrast_s > 0) ≥ 0.95`** (a draw-wise *posterior contrast*, not a frequentist *t*-test — Decision 23). Pearson residuals are identical to H3c(ii) (`r_c,s = (y_c − μ_c,s)/√(μ_c,s + μ_c,s²/φ_s)`).

## Capital indicator — source and definition

- **Primary: the Hanson 2016 OXREP Cities Database "Civic Status" table** (`data/hanson2016_civic-status_oxrep.csv`), `Civic Status = "Provincial capital"` (67 cities incl. one `"Provincial capital?"`). This is **Hanson's own dataset variable — the same classification Hanson 2021 (our H3c replication target) used**, so it is the faithful source. Matched to our cities by **exact Ancient-Toponym string** (our names and OXREP's both embed the province disambiguator, e.g. `Nicopolis (Achaea)`, so the exact-string match is **collision-safe** — it cannot flag a non-capital that merely shares a bare toponym with a capital elsewhere). Builder: `code/build-provincial-capitals-oxrep.py` → `data/processed/provincial-capitals.csv`. **62/67 present in the empire frame**; 5 absent (Greek-East / Dacian, genuinely not in our Latin-inscription sample): Apulum (1), Nicomedia, Perge, Sepphoris, Tiberias.
- **Sensitivity: the AD-117 snapshot** — Hanson 2016 Fig. 120 reports **40 provincial capitals in AD 117** (the OXREP `Provincial capital` flag is "ever a provincial capital" across 100 BC – AD 300, hence 67). The AD-117 set was assembled from the standard province→capital mappings cross-checked against the Barrington Atlas (`code/build-provincial-capitals-ad117.py` → `data/processed/provincial-capitals-ad117.csv`; 39 in the empire frame).

## Result — SUPPORTED in every cell

| indicator | frame | n capitals | n non-capitals | median contrast | 95% CI | P(contrast>0) | verdict |
|---|---|---|---|---|---|---|---|
| **OXREP (primary)** | **empire** | 62 | 982 | **+0.964** | [+0.736, +1.213] | **1.000** | **SUPPORTED** |
| **OXREP (primary)** | **Latin** | 41 | 776 | **+1.081** | [+0.806, +1.408] | **1.000** | **SUPPORTED** |
| AD-117 (sensitivity) | empire | 39 | 1005 | +1.296 | [+0.993, +1.636] | 1.000 | SUPPORTED |
| AD-117 (sensitivity) | Latin | 27 | 790 | +1.261 | [+0.915, +1.671] | 1.000 | SUPPORTED |

Posterior-mean Pearson residuals (OXREP primary): capitals **+0.91** (empire) / **+1.03** (Latin) vs non-capitals **−0.06** / **−0.05**. Provincial capitals over-produce inscriptions relative to non-capitals of the same modelled expectation — strongly and unambiguously (P = 1.000 in all four cells). The verdict is **robust to the capital definition** (OXREP ever-capital vs AD-117 snapshot) and **to the frame** (empire vs Latin); the OXREP magnitudes are slightly smaller, as expected when the larger 62-city set adds lower-residual capitals.

## Interpretation

- **SR2(i) is answered: yes — capitals over-produce.** This **replicates Hanson 2021's provincial-capital over-production finding.**
- Note the contrast with **H3c(ii)** (residual spatial clustering), which was **NOT replicated** (Moran's I ≈ 0, both frames). So the two halves of the Hanson-2021 residual replication diverge: **H3c(i) capital over-production replicates; H3c(ii) spatial clustering does not.** A coherent reading: the Mundlak province random intercepts already absorb the broad spatial structure (H3c(ii) ≈ 0), while the capital-vs-non-capital *level* difference (H3c(i)) is a within-province effect the model leaves in the residuals — capitals out-produce their provincial peers.

## Provenance

- Code: `code/06-h3c-i-capital-contrast.py` (parametrised: `--capitals-csv`, `--label`); `code/build-provincial-capitals-oxrep.py`; `code/build-provincial-capitals-ad117.py`.
- Indicators: `data/processed/provincial-capitals.csv` (OXREP primary); `data/processed/provincial-capitals-ad117.csv` (sensitivity). Source data: `data/hanson2016_*_oxrep.csv` (OXREP, downloaded 2026-06-05).
- Results: `outputs/h3c-i-results-oxrep-primary.json`, `outputs/h3c-i-results-ad117-sensitivity.json`. Posteriors: `outputs/idata-{primary,latin}.nc` (sapphire; no re-fit).
- **Label:** preliminary — pending sign-off; Latin frame pending OSF Amendment 02.
