# §5 Layer B — β-inversion to time-varying population — RESULTS

- **Status:** COMPLETE (exploratory; Decision 13 / preregistration §5 "Extension
  (Layer B)"). **Illustrative comparative-shape outputs only — NOT quantitative
  population claims.**
- **Run:** sapphire, 2026-06-16; `code/layerb_invert.py --frames empire latin
  --seed 20260616`; log at `run.log`. Deterministic transform (268 cities) +
  two standalone anchor re-fits (the only MCMC). Exit 0.
- **Spec + sign-off:** `spec.md` (four design decisions signed off 2026-06-16);
  inputs staged + verified on sapphire (`INPUTS.md`).

---

## 1. What was done

Each city's Layer-A posterior inscription-rate trajectory `lam[c, t]` (8,000
draws, 16 × 25 y bins, 50 BC – AD 350) was inverted to a relative population
trajectory via the H3a scaling law, draw-wise:

`pop_t = pop_max · ( insc_t / max_t insc_t )^(1/β_within)`

- **β frame:** empire `β_within = 0.587` primary; Latin `0.733` overlay (both
  posteriors propagated, 12,000 draws each, resampled to the 8,000 Layer-A
  draws).
- **Outputs:** relative-shape (peak = 1) **and** Hanson-anchored absolute
  (`pop_max` = `urban_context_pop_est`), median + 95 % bands per city.
- **Scope:** the 268 small-N **target** cities (the §5 deliverable). The large
  anchors are not in that fit, so the validation gate re-fit Ostia and Pompeii
  standalone and applied the identical transform.

---

## 2. Validation gate (audit H3) — PASS

Both anchor fits converged cleanly (R̂ = 1.0000, 0 divergences, ESS 1166 / 1420).
Gate is **descriptive** (no preregistered threshold). Figure:
`outputs/layerb-anchor-gate-empire.png`.

| Anchor | Inverted-population peak | P(peak in 2nd c. AD) | post-AD-79 mass frac | Verdict |
|---|---|---|---|---|
| **Ostia** | **AD 125–150** (Hadrianic), sustained through 2nd c. | **0.99** | — | **matches** the OCD/Meiggs 2nd-c. apogee |
| **Pompeii** | **AD 50–75** (immediately pre-eruption) | 0.00 | **0.000** | **terminus reproduced** (consistency) |

- **Ostia** rises through the 1st–2nd c. to a 2nd-c. apogee and falls sharply
  after ~AD 200 — exactly the independent expectation grounded this session
  (OCD "Ostia"; Meiggs, *Roman Ostia* 1973). A descriptive curiosity worth a
  cautious note: a dip ~AD 160–175 between two 2nd-c. peaks coincides with the
  **Antonine Plague (AD 165–180)** — intriguing but not a claim (it could equally
  be a binning/aoristic feature, amplified by 1/β).
- **Pompeii** peaks just before AD 79 and the inverted population is ~0
  thereafter — the eruption terminus, reproduced from the data alone (Layer A
  found post-79 mass 0.12 %; here the inverted-population fraction after AD 79 is
  0.000). The post-AD-250 segment is irrelevant for Pompeii (already terminated).

The two anchors bracket the gate well: one tests the **growth-to-2nd-c.-peak**
expectation (Ostia, clean pass), the other a hard **terminus** (Pompeii, clean
pass).

---

## 3. The 268 target cities

- **Reliability:** 34 / 268 cities meet the Layer-A calibration floor N ≥ 300
  (`reliable` flag in the trajectory `.nc`); the remaining 234 are below-floor
  (retained but flagged — the N\* = 300 honest-negative result from Layer A
  carries through unchanged).
- **Peak timing:** the *typical* small-N target city does **not** peak in the
  2nd c. (median P(peak 2nd c.) = 0.21 across cities) — small/frontier cities
  have more varied and often earlier peaks than the great anchors. A descriptive
  map of small-N trajectory shapes, now in population terms.
- **The amplification effect is the headline caveat, borne out.** Because
  β < 1 ⇒ 1/β > 1, the inversion magnifies every swing. For the **median** target
  city, inverted population at AD 250 is ≈ **0 % of peak** (empire β) / ≈ 1 %
  (Latin β), and similarly by AD 325–350. This near-total "collapse" is the
  *amplified* late-period inscription decline, which after ~AD 250 is dominated
  empire-wide by the **epigraphic-habit collapse** (MacMullen 1982), **not**
  demonstrated depopulation. It vindicates the illustrative-only framing and is
  precisely what the Decision-13 H5 habit-removed residual analysis is designed
  to disentangle. The Latin frame (smaller exponent 1.36 vs 1.70) is uniformly
  less extreme — the `outputs/layerb-amplitude-overlay.png` overlay shows the
  amplitude sensitivity directly.

---

## 4. Caveats (carried into any write-up)

1. **Illustrative comparative-shape only** — not a population estimate (prereg
   wording).
2. **Cross-sectional → temporal substitution** — uses the within-province H3a
   slope as a within-city-over-time relationship (prereg's flagged "strong
   assumption"; β_within is the least-bad analogue).
3. **1/β amplification** — population swings exceed inscription swings; the β
   frame changes amplitude materially (peak timing/shape unaffected).
4. **Epigraphic-habit confound after ~AD 250** — read the gate on the
   growth-to-peak (1st–2nd c.) segment; the post-peak decline is partly artefact.
5. **Hanson anchor** — pins peak population to a single static figure at the
   peak-epigraphy bin; ignores Hanson's own level uncertainty.
6. **N\* = 300 floor** — only 34 / 268 target cities are reliable; the rest are
   flagged.
7. **Posterior independence** — Layer-A and H3a posteriors combined under
   independence (separate fits).

---

## 5. Outputs

`outputs/` (small artefacts committed; full anchor posteriors regenerable, on
sapphire):

- `layerb-trajectories-empire.nc`, `layerb-trajectories-latin.nc` — per-city
  summary trajectories (relative-shape + anchored; median + bands; `reliable`
  flag, `pop_max`, `N`, `peak_bin_mode`, `p_peak_2c`).
- `layerb-summary.json` — per-frame + per-city peak/decline summaries, gate
  outcomes, β frames, seed, input sha256 provenance.
- `layerb-anchor-gate-empire.png` — the Ostia/Pompeii gate panels.
- `layerb-amplitude-overlay.png` — empire-vs-Latin β amplitude sensitivity.
- `layerb-anchor-{ostia,pompeii}.nc` — standalone anchor posteriors (on
  sapphire; regenerable in 15 / 119 s).

---

## 6. Bottom line

The β-inversion runs cleanly and **validates against both independent anchors**
(Ostia's 2nd-c. apogee; Pompeii's AD-79 terminus). The deliverable is a set of
per-city *illustrative* population-trajectory shapes for the small-N target
cities, with the 1/β amplification and the post-AD-250 epigraphic-habit confound
as the dominant interpretive caveats — exactly the honest, bounded, exploratory
contribution preregistered under Decision 13.
