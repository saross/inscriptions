---
title: "36-hour analysis roadmap — RAC-TRAC 2026 conference talk"
date: 2026-05-20 (overnight)
target: "12-minute talk inside a 20-minute slot. Shawn's TRAC7 slot: Friday 22 May 2026 14:20 Aarhus time, room Preben Hornung. See conference-context.md."
scope: "A+ (lean A core + synthetic mixture-recovery demo + stretch Bayesian H3a). Fallback to lean A if A+ runs over time."
speaker-question: "OPEN: who is presenting? Shawn's slot (14:20) per programme; Adela has her own 12:20 marriage-ages slot. User originally framed this as 'Adela giving the talk' — confirm Friday morning."
---

# 36-hour analysis roadmap

## Scope decision

**Primary scope (A+)**: lean A (Phase 1 reuse + raw SPAs + frequentist Hanson scaling + mixture-model schematic) + one synthetic mixture-recovery demo cell + stretch Bayesian H3a within-between NBR.

**Fallback (lean A)**: drop the Bayesian H3a stretch; keep frequentist Hanson scaling + the synthetic mixture-recovery demo. If the synthetic-recovery demo over-runs by more than 4 hours, drop it too and ship the mixture schematic.

**Decision gates**: explicit at hour 18 and hour 26 — see schedule below.

## Critical-path artefacts (must-produce, in priority order)

1. **Empire / province / city raw SPA figures** — slide #4. Re-renders of 2024 notebook cells 134–161 against the prereg date-window filter (50 BC – AD 350; 180,609 rows).
2. **Frequentist NBR scaling result** — slide #6 numerical content. β estimate + bootstrap 95 % CI from notebook cell 197, applied to the prereg-filtered corpus.
3. **Phase 1 reachability figure** — slide #3. Re-use `runs/2026-04-25-h1-simulation/outputs/heatmaps/empire_*.png` (or a one-off summary heatmap if a better visual is needed).
4. **Editorial-distortion figure(s)** — slide #2. Re-use `runs/2026-05-17-empirical-spa-shape/outputs/figures/` and `runs/2026-05-17-interval-width-diagnostic/outputs/figures/`. May need cosmetic re-render at slide aspect (16:9 rather than print).
5. **Slide deck assembled in Quarto + speaker notes** — slide-outline.qmd populated with the above figures and the numerical NBR result.

## Stretch artefacts (try to produce, drop if needed)

6. **Synthetic mixture-recovery demo** — slide #5 main figure. A+ stretch. ~50–100 LOC pymc multinomial mixture; one synthetic cell (known α, known genuine shape, known template-slab convention); show recovered posterior on α and recovered shape. **Not** the preregistered grid validation.

7. **Bayesian within-between H3a fit** — slide #6 either replacing or supplementing the frequentist result. Stretch beyond A+; only attempt if hours 26–32 have spare bandwidth.

## 36-hour schedule (proposed; flex as needed)

Times relative to start of next session.

### Block 1 — Hours 0–4: Orientation + filter-and-prep

- [ ] **0:00–0:30** New CC session reads handoff prompt + this roadmap + asset-inventory.md
- [ ] **0:30–1:00** Smoke-test the LIRE parquet load + 2024 notebook environment (`uv run python ...`); confirm pymc / statsmodels / pandas all import
- [ ] **1:00–2:30** Apply prereg date-window filter (50 BC – AD 350 intersect, `is_geotemporal`, `is_within_RE` flags) to LIRE v3.0; produce a clean filtered DataFrame; cache to `runs/2026-05-21-talk-prep/data/lire-filtered.parquet`
- [ ] **2:30–4:00** Verify counts match prereg expectations: 180,609 rows after filter; 65,435 Rome inscriptions; 115,174 Rome-excluded; ~815 Hanson-matched cities. **HALT and report if any count diverges from prereg by > 1 %**.

**Output by end of Block 1**: clean filtered corpus on disk; reproducible script that runs end-to-end.

### Block 2 — Hours 4–10: Empirical SPA figures

- [ ] **4:00–6:00** Empire SPA on filtered corpus (5-year bins; uniform aoristic per prereg §4). Compare to the 2024 notebook's full-corpus empire SPA; document any visible differences from the date-window filter.
- [ ] **6:00–7:30** Provincial-aggregate SPAs (Latin-speaking provinces excluding Roma); produce one combined figure showing each province's SPA scaled to unit height.
- [ ] **7:30–9:00** City-level SPAs for the largest Hanson-matched cities (top 6–10 by inscription count after Rome exclusion); produce a small-multiples figure.
- [ ] **9:00–10:00** Final figure polish at 16:9 slide aspect; save PNGs to `planning/conference-talk-rac-trac-2026/figures/`; include high-DPI versions for the slide deck.

**Output by end of Block 2**: slide-#4-ready figures (empire / province / city).

### Block 3 — Hours 10–18: Frequentist Hanson scaling

- [ ] **10:00–12:00** Build the per-city aggregation DataFrame (cell 71 of 2024 notebook): one row per Hanson-matched city with date-window-filtered `inscription_count` + `urban_context_pop_est`. Rome-excluded variant.
- [ ] **12:00–14:00** Fit statsmodels NBR with log-population predictor (notebook cell 197, modernised: confirm statsmodels NBR is `GLM(family=NegativeBinomial(alpha=))`, current syntax). Report point estimate of β.
- [ ] **14:00–16:00** Bootstrap NBR with 1,000 replicates (rows resampled with replacement); compute 95 % bootstrap percentile CI on β; compare to Hanson 2021's β = 0.672 [0.588, 0.756] and Carleton et al. 2025's β ≈ 0.3–0.5.
- [ ] **16:00–17:00** Diagnostic plot: log–log scatter + fitted line + bootstrap CI band. **Stretch**: residual diagnostic; per-province colour coding.
- [ ] **17:00–18:00** Final figure polish at 16:9; save to figures dir. Insert numerical β into slide #6 outline.

**Output by end of Block 3**: slide-#6-ready figure + numerical β + bootstrap CI.

### **GATE 1 — Hour 18**: A vs A+ decision

- If Blocks 1–3 are complete and on schedule → **continue to Block 4 (A+ synthetic mixture demo)**.
- If any block is behind by > 2 hours → **drop A+; freeze deck at slide #5 schematic; proceed to Block 5 (slide assembly) at hour 18**.

### Block 4 — Hours 18–26: Synthetic mixture-recovery demo (A+ stretch)

- [ ] **18:00–20:00** Pymc multinomial-mixture skeleton (per prereg §4 Decision 19): observation model `y_t ~ Multinomial(N, α·p_conv + (1−α)·p_gen)`; convention component built from a simplified template-slab structure (one century slab as minimum); single empire-level α.
- [ ] **20:00–22:00** Construct synthetic ground-truth: choose known α ∈ {0.3, 0.5, 0.7} (one cell); choose known genuine SPA shape (e.g., smooth Gaussian peaking AD 150); construct convention component from template intervals; combine and add aoristic smearing.
- [ ] **22:00–24:00** Run pymc NUTS sampling (~ 1,000 warmup + 2,000 sampling, 4 chains); diagnostics (R̂ < 1.01 on α; ESS ≥ 400); recover posterior on α and on the genuine SPA shape.
- [ ] **24:00–26:00** Recovery figure: known α + 95 % posterior CI on α; known genuine shape overlaid with posterior median + 95 % credible band of recovered shape. Pearson r between recovered median and true genuine SPA.

**Output by end of Block 4 (A+ successful)**: slide-#5-ready synthetic recovery figure.

### **GATE 2 — Hour 26**: Bayesian H3a stretch decision

- If Block 4 succeeded and there's spare bandwidth → **attempt the Bayesian within-between H3a fit (Block 4b below)**.
- Otherwise → **proceed directly to Block 5 (slide assembly)**.

### Block 4b — Hours 26–30: Bayesian within-between H3a (further stretch)

- [ ] **26:00–28:00** Pymc within-between Mundlak NBR (preregistered §4 specification, lines ~215–268 of original prereg, ~ lines 195+ of supplementary): `log_pop_c` decomposed into `log_pop_province_mean[c]` + `(log_pop_c − log_pop_province_mean[c])`; intercepts `α_0`, province random effects, dispersion. ~50–80 LOC.
- [ ] **28:00–30:00** Fit on the Rome-excluded ~ 815 Hanson-matched cities; sample ~ 1,000 warmup + 2,000 samples; compute `f_within` posterior; compare to frequentist β.

**Output (further-stretch success)**: posterior on `f_within` + comparator panel in slide #6. **If this doesn't converge or is unstable, drop entirely and keep frequentist as the slide-#6 main result**.

### Block 5 — Hours 26 (or 30) – 32: Slide assembly

- [ ] **start**: populate `slide-outline.qmd` placeholders with the figures from `planning/conference-talk-rac-trac-2026/figures/`
- [ ] Render slide #1 opening figure (LIRE temporal coverage at a glance — empire 5-y-binned SPA)
- [ ] Insert numerical results into slide #6
- [ ] Adjust speaker notes for what was / wasn't produced
- [ ] Add the OSF DOI (if Shawn has it by then) to slide #7 footer and slide #5 caveats
- [ ] Render Quarto deck (`quarto render slide-outline.qmd --to revealjs`)
- [ ] Visually QA the rendered HTML in a browser (check for figure clipping, text overflow, image quality)

**Output**: rendered `slide-outline.html` plus PDF export (`quarto render --to pdf`) for Adela's printout reserve

### Block 6 — Hours 32–34: Speaker notes polish + handoff to Adela

- [ ] Refine the speaker-notes in the .qmd
- [ ] Write a short briefing markdown for Adela: what's in the deck; what's preliminary vs final; how to handle anticipated audience pushback; what backup material to consult in Q&A
- [ ] Save as `planning/conference-talk-rac-trac-2026/adela-briefing.md`
- [ ] Confirm with Shawn that Adela has access (Aarhus filesystem; or sent via WeTransfer / email)

### Block 7 — Hours 34–36: Final sanity check + buffer

- [ ] End-to-end run of all scripts on a clean checkout (one final reproducibility check)
- [ ] Confirm Quarto HTML loads in modern browsers; PDF exports correctly
- [ ] Final commit + push
- [ ] Note any failure modes / known-issues for post-talk follow-up

## Critical-friend gates (standing rules)

- **No silent parameter reductions.** Notebook cells use various sample sizes / bootstrap counts; do NOT silently reduce. If compute is tight, halt and report. (Per-incident learned lesson; see continuity.md §"Failure modes".)
- **Critical-friend on statistics**: for every statistical choice, ask (a) more appropriate test for the data structure? (b) more powerful / robust alternative? (c) more current best-practice approach? (d) do the method's assumptions actually hold? Surface any concerns before executing.
- **Honest preliminary framing**: all quantitative slide content must be explicitly labelled "preliminary, post-lodgement; the preregistered analysis is forthcoming". This is non-negotiable for prereg compliance.
- **Anti-confabulation**: every numerical claim re-checked against the source dataframe at write-time. No stale references to old corpus sizes / β values.

## Risk register

| Risk | Likelihood | Mitigation |
|---|---|---|
| 2024 notebook environment broken (dependency drift) | Medium | Use the project's `.venv` rather than the notebook's; test imports in Block 1 |
| Date-window filter changes city aggregation in unexpected ways | Medium | Verify counts against prereg's published figures (180,609 / 65,435 / 115,174 / ~815) in Block 1; halt if divergence > 1 % |
| Bootstrap NBR overruns | Low | 1,000 replicates is small; should be minutes on sapphire / local |
| Pymc mixture demo fails to converge | Medium | Have schematic-only backup slide ready; document failure mode in speaker notes; cap fix time at 4 hours, then move to schematic |
| Slide rendering issues at Adela's setup | Medium | Produce both Quarto HTML (embed-resources: true) and PDF export; test on a second machine before handoff |
| OSF DOI not available by talk time | Low | Adela can read it from her phone if Shawn finalises lodgement before her session; backup is the github tag URL |
| Audience-pushback derails Q&A | Medium | Pre-write responses to the top 3 anticipated objections (in talking-points-feedback.md); rehearse with Adela |

## Compute placement

- All Block 1–3 work runs locally on Shawn's machine in the project `.venv`. No sapphire needed.
- Block 4 (pymc mixture) and Block 4b (pymc H3a) can run locally too — sample sizes are small.
- Sapphire is overkill for this work; no need to introduce remote-execution overhead under time pressure.

## Things explicitly NOT in scope for this talk

- **Full preregistered H2 mixture validation** (the 100-replicate-per-cell recovery grid)
- **H3b deviation-detection at Antonine / Crisis**
- **H3c Moran's I + capitals contrast**
- **§5 small-N city trajectory work (Layers A + B)**
- **Hanson population-uncertainty sensitivity (σ_pop sweep)**
- **Letter-count alternative analysis**
- **brms shadow validation**
- **The HMM post-lodgement extension** (mention in backup slide B6 only)

These are all preregistered Phase 2 / 3 work to be tackled post-talk, on the project's normal cadence. The talk is for *preliminary feedback*, not for *settling* any of these analyses.
