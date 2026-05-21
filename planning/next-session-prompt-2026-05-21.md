---
title: "Next-session prompt — RAC-TRAC 2026 talk implementation (2026-05-21)"
date: 2026-05-20 (drafted overnight)
audience: "Shawn (to paste into the new CC session) + the new CC instance"
purpose: "Brief continuity prompt for the new CC instance picking up the conference-talk implementation."
---

# Next-session prompt — RAC-TRAC 2026 talk implementation

Paste the block below into the new CC session as the first message.

---

Picking up the inscriptions project from end-of-session 2026-05-20. **The OSF preregistration was lodged that day** (git tag `osf-lodgement-2026-05-20`, commit `a2e40fd`; OSF DOI pending Shawn's confirmation). Immediately after lodgement, the project pivoted to producing preliminary results for **a TRAC7 conference talk on Friday 2026-05-22 14:20 Aarhus time**, with overnight planning already externalised.

## Resolved questions (both confirmed 2026-05-21 morning)

1. **Presenter**: **Adela** is reading the paper on Shawn's behalf at the 14:20 Friday TRAC7 slot. Shawn cannot travel to Denmark, and remote presentations are not supported by RAC-TRAC. Adela also has her own paper at 12:20 (marriage ages); the 14:20 slot delivers the LIRE / SPA / Hanson-scaling content prepared in this planning.
2. **OSF preregistration URL**: `https://osf.io/uycs6/` — lodged 2026-05-20; currently **embargoed pending decision on submission to a journal requiring double-blind review**. The URL is publicly visible; the deposit contents are gated. Already folded into:
   - `planning/conference-talk-rac-trac-2026/slide-outline.qmd` (footer, slide #5, slide #7)
   - `planning/preregistration-draft.md` §11 Provenance (post-lodgement amendment trail)
   - `README.md` (project landing page)

The lodgement tag `osf-lodgement-2026-05-20` remains at its original commit; post-lodgement amendments live in subsequent `main` commits.

**Embargo handling for the talk**: cite the URL on the closing slide; if anyone asks for access, Adela can say "the prereg is currently embargoed pending a journal-submission decision; the embargo will lift when we choose a venue." Authorship is public (Adela is delivering on Shawn's behalf); content is gated; a double-blind submission package would supply a blinded version. No conflict.

## Read in this order to get oriented

1. `planning/conference-talk-rac-trac-2026/conference-context.md` — full conference briefing (~470 lines). The programme, audience details (incl. session organisers being LIRE creators), format expectations, theoretical orientation. **Start here.**
2. `planning/conference-talk-rac-trac-2026/asset-inventory.md` — every figure, dataset, code module, REPORT available to feed into the talk. The 2024 exploratory notebook (`archive/2026-04-22-inscriptions-spa.ipynb`) is the goldmine — it has most of the empirical work already done.
3. `planning/conference-talk-rac-trac-2026/analysis-roadmap.md` — hour-by-hour 36-hour plan with explicit decision gates at hour 18 (A+ go / no-go) and hour 26 (Bayesian H3a stretch go / no-go).
4. `planning/conference-talk-rac-trac-2026/slide-outline.qmd` — 7-slide Quarto revealjs skeleton with speaker notes (HTML comments) and figure placeholders. Edit in place as you populate.
5. `planning/conference-talk-rac-trac-2026/talking-points-feedback.md` — anticipated objections, audience framing, feedback prompts. **Read before the slide-polish stage to align tone.**
6. `planning/preregistration-draft.md` — the lodged preregistration (since the talk's preregistered framing matters for slide #5 and the closing slide). Reference, not for editing.
7. `docs/notes/reflections/continuity.md` — the canonical living continuity doc with the updated "in flight: conference talk" section at the top of the staging-work area.

## Scope and decision rule

**Primary target (A+)**: Lean-A core (Phase 1 reuse + raw SPAs at empire/province/city + frequentist Hanson NBR-GLM + mixture model schematic) **plus** one synthetic mixture-recovery demo cell **plus** stretch Bayesian H3a within-between NBR.

**Fallback (lean A)**: if the synthetic mixture demo over-runs by > 4 hours, drop it; ship the schematic-only mixture slide.

**Decision gates** (explicit, do not skip):
- **Hour 18 gate**: Blocks 1–3 (filter, raw SPAs, frequentist Hanson scaling) done? If not, drop A+ and proceed to slide assembly.
- **Hour 26 gate**: Block 4 (synthetic mixture demo) done? If yes, attempt Block 4b (Bayesian H3a). If no, skip 4b and proceed to slide assembly.

## What the analytical work in hour 0–4 should look like

1. New session reads the prompts above (estimate 20 min) — do not skip; the asset inventory and roadmap save many hours of rediscovery.
2. **Confirm the two open questions with Shawn.**
3. Create `runs/2026-05-21-talk-prep/` with the standard `spec.md` / `plan.md` / `code/` / `outputs/` structure (per-project convention).
4. Smoke-test the project's `.venv`: `cd ~/Code/inscriptions && source .venv/bin/activate` (or `uv run python ...`); confirm `pymc`, `statsmodels`, `pandas`, `pyarrow` all import.
5. Apply the prereg date-window filter to LIRE v3.0 (parquet at `archive/data-2026-04-22/LIRE_v3-0.parquet`). Expected post-filter row count: **180,609** (≈ 98.8 % of 182,853). **HALT and report if any sanity-check count diverges from prereg figures by > 1 %** — these counts are referenced verbatim in the lodged preregistration and any divergence is a methodological flag.

## Critical-friend gates (standing rules — re-read before any block)

- **No silent parameter reductions.** Anywhere. Halt and report if compute is tight.
- **Critical-friend on statistics**: for every choice — (a) more appropriate test for the data structure? (b) more powerful / robust alternative? (c) more current best-practice approach? (d) do the method's assumptions actually hold? Surface concerns before executing.
- **Honest preliminary framing**: every quantitative slide content must be labelled "preliminary, post-lodgement; the preregistered analysis is forthcoming." Non-negotiable for prereg compliance.
- **Anti-confabulation**: every numerical claim re-checked at write-time against the source dataframe. No stale references to old corpus sizes, β values, or city counts.
- **Sapphire is overkill here**: all compute fits on Shawn's local machine. Don't introduce remote-execution overhead under a 36-hour deadline.

## Audience reality (refresher — critical for talk framing)

- The TRAC7 session organisers are **Petra Heřmánková, Tomáš Glomb, Vojtěch Kaše** — the SDAM / Masaryk group, **the LIRE creators**. Heřmánková is on our cited 2021 paper; Glomb is the first author of our cited 2022 Asclepius-cult paper.
- Adjacent talks: **Sommerschield (14:00, Aeneas neural-net)** directly precedes Shawn's slot — natural Q&A overlap; **Lynne Bennett (15:00, global epitaphs)** follows.
- Session abstract explicitly welcomes "statistical methods for mitigating selection biases in the epigraphic record" — the room is the right room.
- Audience will reward: honest treatment of corpus bias; explicit linkage of method to historical questions; reflexivity about what numbers can and cannot license; engagement with post-colonial / decolonising current.

## Risks to track

| Risk | Mitigation |
|---|---|
| 2024 notebook dependencies fail to import in current `.venv` | Block 1 smoke-test catches this; fallback is `uv pip install` from the notebook's requirements |
| Date-window filter changes counts in unexpected ways | Block 1 sanity check halts and reports |
| Pymc mixture demo fails to converge | Cap fix time at 4 h; fall back to schematic-only slide |
| Bayesian H3a doesn't converge | Drop entirely; frequentist β stays as the slide-6 main |
| Slides break at Adela's / Shawn's setup | Produce HTML (embed-resources: true) + PDF export; test on a second machine |
| OSF DOI not available before talk | Slide footer falls back to the github tag URL; insert DOI later as amendment |

## What's explicitly out of scope for this 36-hour push

- Full preregistered H2 recovery-grid validation
- H3b deviation-detection at Antonine / Crisis probes
- H3c Moran's I + capitals contrast
- §5 small-N city trajectory work (Layers A + B)
- Hanson population-uncertainty sensitivity (σ_pop sweep)
- Letter-count alternative analysis
- brms shadow validation
- The HMM post-lodgement extension (mention in backup slide B6 only)

These are post-talk Phase 2 / 3 work; the talk is for *preliminary feedback*, not for *settling* any of them.

---

End of prompt block.
