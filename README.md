# Inscriptions

**Mixture-corrected SPAs of Latin inscriptions vs Hanson urban population: a preregistered three-phase analysis.**

This repository hosts the code, decision log, run reports, and supplementary planning artefacts for an open-science project applying summed probability analysis (SPA) to the Latin Inscriptions of the Roman Empire (LIRE v3.0) corpus, together with a Bayesian deconvolution-mixture model that corrects for editorial-template dating artefacts in the source data.

## Preregistration

- **OSF preregistration**: <https://osf.io/uycs6/> — lodged 2026-05-20; currently under embargo pending publication review.
- **Lodgement-state tag**: `osf-lodgement-2026-05-20` (commit `a2e40fd`) pins the repository state at lodgement. Readers verifying any claim in the preregistration should clone or browse at this tag, not at `main`.
- **Source documents**: `planning/preregistration-draft.md` (working version, may have post-lodgement amendments); `planning/osf-supplementary-2026-05-20.md` + `.pdf` (lodged supplementary).

## Authors

- Shawn Ross (Macquarie University) — author
- Adela Sobotková (Aarhus University) — co-author

## Methodology overview

The project is structured in three phases.

1. **Phase 1 (complete; reported in the preregistration)** establishes minimum-sample-size thresholds for permutation-envelope deviation-detection across analysis levels (empire, province, urban-area). The simulation pipeline, fixed random seed (20260425), and threshold tables are committed at `runs/2026-04-25-h1-simulation/`.
2. **Phase 2** validates a Bayesian mixture model that decomposes the observed SPA into a parametric "convention" component (built from the empirically-attested template-interval slab structure that dominates the LIRE corpus) and a smoothed "genuine" temporal signal. Validation is by recovery simulation against a pre-specified parametric grid; the design artefact is committed alongside this README.
3. **Phase 3** quantifies the population dimension's footprint on inscription variation via a Bayesian within-between (Mundlak) negative-binomial regression, permutation-envelope deviation-detection at the Antonine and Crisis-of-the-Third-Century probes, and a Hanson-replication residual analysis (provincial-capital contrast plus Moran's I spatial clustering).

The interpretive question — what inscription production proxies (urban-information-infrastructure, socio-political complexity, or some combination) — is deliberately scoped out of the preregistration. The paper's primary contribution is methodological.

## Repository layout

- `planning/` — the preregistration, decision log, changelog, OSF supplementary upload, conference-talk planning, and the prior-art scouts.
- `runs/` — per-run artefacts (specification, code, outputs, REPORT.md) for each analysis stage.
- `scripts/` — long-lived helper scripts (e.g., `h3a_brms_shadow.R`, `zotero_batch_add.py`).
- `archive/` — superseded notebooks and historical materials; reference only.
- `docs/notes/reflections/` — the living continuity document and working-notes log.

## Reproducibility

- **Code**: Python 3.13 with `numpy`, `scipy`, `pandas`, `pyarrow`, `pymc`, `statsmodels`, `libpysal`. R 4.4.3 with `cmdstanr`, `brms`, `baorista`, `nimble` for shadow validation and Bayesian-aoristic cross-checks.
- **Environment**: pinned via `pyproject.toml` and `uv.lock`.
- **Data**: LIRE v3.0 (Kaše, Heřmánková & Sobotková 2023, Zenodo DOI `10.5281/zenodo.8431452`; CC-BY-4.0). Hanson (2016) OXREP Roman Cities Dataset (tDAR record 448563) for `urban_context_pop_est`.
- **Seeds**: fixed random seed `20260425` for the Phase 1 simulation; per-stage seeds documented in each `runs/<date>-<name>/spec.md`.

## Licence

Code: see `LICENSE` (default project licence). Data: as licensed by their respective sources (LIRE CC-BY-4.0; Hanson per OXREP terms).
