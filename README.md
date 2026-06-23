# Inscriptions

**Mixture-corrected SPAs of Latin inscriptions vs Hanson urban population: a preregistered three-phase analysis.**

[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8F%20%20%E2%97%8B-orange)](https://fair-software.eu)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![FAIR software check](https://github.com/saross/inscriptions/actions/workflows/fair-software.yml/badge.svg)](https://github.com/saross/inscriptions/actions/workflows/fair-software.yml)

This repository hosts the code, decision log, run reports, and supplementary planning artefacts for an open-science project applying summed probability analysis (SPA) to the Latin Inscriptions of the Roman Empire (LIRE v3.0) corpus, together with a Bayesian deconvolution-mixture model that corrects for editorial-template dating artefacts in the source data.

## Preregistration

- **OSF preregistration**: <https://osf.io/uycs6/> — lodged 2026-05-20; currently under embargo pending publication review.
- **Lodgement-state tag**: `osf-lodgement-2026-05-20` (commit `a2e40fd`) pins the repository state at lodgement. Readers verifying any claim in the preregistration should clone or browse at this tag, not at `main`.
- **Source documents**: `wiki/prereg/preregistration-draft.md` (working version, may have post-lodgement amendments); `wiki/prereg/osf-supplementary-2026-05-20.md` + `.pdf` (lodged supplementary). The full preregistration record — draft, changelog, the four OSF amendments, and the obligations/compliance audits — lives under `wiki/prereg/`.

## Authors

- Shawn Ross (Macquarie University) — author
- Adela Sobotková (Aarhus University) — co-author

## Citing this work

If you use this software or analysis, please cite it via the metadata in
[`CITATION.cff`](CITATION.cff) — GitHub's "Cite this repository" button reads it
directly. Machine-readable metadata is also provided as
[`codemeta.json`](codemeta.json) (CodeMeta) and [`.zenodo.json`](.zenodo.json)
(for Zenodo deposition). A preferred citation pointing to the forthcoming JAMT
article will be added on publication.

Underlying data should be cited separately: LIRE v3.0 (Kaše, Heřmánková &
Sobotková 2023, DOI `10.5281/zenodo.8431452`) and the Hanson (2016) OXREP Roman
Cities Dataset (tDAR 448563).

## Methodology overview

The project is structured in three phases.

1. **Phase 1 (complete; reported in the preregistration)** establishes minimum-sample-size thresholds for permutation-envelope deviation-detection across analysis levels (empire, province, urban-area). The simulation pipeline, fixed random seed (20260425), and threshold tables are committed at `runs/2026-04-25-h1-simulation/`.
2. **Phase 2** validates a Bayesian mixture model that decomposes the observed SPA into a parametric "convention" component (built from the empirically-attested template-interval slab structure that dominates the LIRE corpus) and a smoothed "genuine" temporal signal. Validation is by recovery simulation against a pre-specified parametric grid; the design artefact is committed alongside this README.
3. **Phase 3** quantifies the population dimension's footprint on inscription variation via a Bayesian within-between (Mundlak) negative-binomial regression, permutation-envelope deviation-detection at the Antonine and Crisis-of-the-Third-Century probes, and a Hanson-replication residual analysis (provincial-capital contrast plus Moran's I spatial clustering).

The interpretive question — what inscription production proxies (urban-information-infrastructure, socio-political complexity, or some combination) — is deliberately scoped out of the preregistration. The paper's primary contribution is methodological.

## Repository layout

The repository follows the canonical four-artefact `wiki/` layout (migrated from the legacy `docs/notes/` + `planning/` layout on 2026-06-23; `wiki/index.md` carries the full old→new path concordance).

- `wiki/` — project memory: `continuity.md` (the living handoff doc), `working-notes.md` (research log), `reflections/` (meta-research logs), `decision-log.md`, `research-intent.md`, `ai-contributions.md`, the **preregistration record** (`wiki/prereg/` — lodged prereg, OSF amendments, compliance audits), and **active plans** (`wiki/planning/`, incl. `future-papers/`).
- `sources/` — bibliographic inputs: BibTeX (`*.bib`) and annotated bibliographies.
- `data/` — datasets (Hanson 2016, processed inputs, `women.csv`).
- `runs/` — per-run artefacts (specification, code, outputs, REPORT.md) for each analysis stage.
- `scripts/` — long-lived helper scripts. `h3a_brms_shadow.R` is the R/brms cross-language shadow of the H3a within-between (Mundlak) negative-binomial regression: it refits the preregistered model (priors matched to the pymc primary, including the `1/shape` Jacobian) and writes `beta_within`, `beta_between`, `f_within`, and Bayesian R² for a posterior-level agreement check against the pymc primary, plus R-native legibility for co-authors. Run as `Rscript scripts/h3a_brms_shadow.R [INPUT_PARQUET] [OUTPUT_DIR]`. (The earlier pooled-model shadow is retired to `archive/superseded-code/`.) Bespoke Zotero-staging one-offs have been retired to `archive/superseded-code/zotero-staging/`; for literature/citation/Zotero work, use the shared cross-project tooling in `~/personal-assistant/scripts/` (see `CLAUDE.md`).
- `reports/` — curated output reports (the key-findings summary; the LLM-use inventory).
- `archive/` — completed history (superseded code/notebooks, archived plans, beacons, specs, scouts, cross-model reviews, audits, consultation, conference talk); reference only.

## Reproducibility

- **Code**: Python 3.13 with `numpy`, `scipy`, `pandas`, `pyarrow`, `pymc`, `statsmodels`, `libpysal`, `esda` (the latter two for H3c spatial autocorrelation — Moran's I). R 4.4.3 with `cmdstanr`, `brms`, `posterior`, `arrow`, `baorista`, `nimble` for shadow validation and Bayesian-aoristic cross-checks.
- **Environment**: pinned via `pyproject.toml` and `uv.lock`.
- **Data**: LIRE v3.0 (Kaše, Heřmánková & Sobotková 2023, Zenodo DOI `10.5281/zenodo.8431452`; CC-BY-4.0). Hanson (2016) OXREP Roman Cities Dataset (tDAR record 448563) for `urban_context_pop_est`.
- **Seeds**: fixed random seed `20260425` for the Phase 1 simulation; per-stage seeds documented in each `runs/<date>-<name>/spec.md`.

## FAIR4RS compliance

This repository follows FAIR-for-Research-Software (FAIR4RS) practice for documentation and metadata:

- **Citation/metadata:** `CITATION.cff`, `codemeta.json`, and `.zenodo.json` (see *Citing this work*).
- **Self-assessment:** scores 3/5 on the [fair-software.eu](https://fair-software.eu) checklist (open repository ✓, licence ✓, citation ✓). The two unmet checks are deliberately not pursued for a research-*analysis* repository: a package **registry** entry (PyPI/RSD — this is analysis code, not a distributed package) and an OpenSSF best-practices **checklist** badge (disproportionate for a solo analysis repo). The check re-runs in CI (`.github/workflows/fair-software.yml`).
- **Persistent identifier (at submission):** the analysis will be deposited to Zenodo via the GitHub–Zenodo integration to mint a DOI (and a Software Heritage SWHID), per Springer Nature's code-availability policy — done at manuscript submission, not before. `.zenodo.json` pre-stages the deposit metadata.

Provenance and the FAIR4RS prior-art basis for these choices: `wiki/planning/prior-art-scout-2026-06-23-fair4rs-docs-uplift.md`.

## Licence

Code: Apache-2.0 (see `LICENSE`). Data: as licensed by their respective sources (LIRE CC-BY-4.0; Hanson per OXREP terms).
