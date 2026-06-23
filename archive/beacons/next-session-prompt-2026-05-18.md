---
title: "Next-session prompt — lodgement-staging session (post-D27–32)"
date: 2026-05-17 (drafted at end of session)
audience: "Shawn (to paste into the new CC session) + the new CC instance"
purpose: "Brief continuity prompt for the next CC instance picking up the pre-lodgement staging work after Decisions 27–32 incorporated the stand-in cross-model statistical review."
note-on-handoff-skill: "A new /handoff skill may be available in the new session — invoke it instead of/in addition to this prompt if so; this prompt is the ad-hoc-handoff fallback."
---

# Next-session prompt — pre-lodgement staging work

Paste the block below into the new CC session as the first message.

---

Picking up the inscriptions preregistration project from end-of-session 2026-05-17. **The preregistration is now lodgement-ready** — three rounds of adversarial review reached saturation, a stand-in cross-model statistical review (ChatGPT 5.5 + Gemini 3 Pro in an "applied econometrician / statistician" role) surfaced seven items now incorporated as **Decisions 27–32**, and the prereg, decision log, changelog, and consultation pack are all up to date. **Lodgement target: Tuesday 2026-05-19** (or whatever date Shawn confirms).

**Read in this order to get oriented** (continuity.md is the canonical first read):

1. `docs/notes/reflections/continuity.md` — research-state snapshot + pre-lodgement staging-work queue + done milestones. **Start here.**
2. `planning/preregistration-changelog.md` — the "2026-05-17 (later) — Stand-in cross-model statistical review; Decisions 27–32" section is the most relevant; everything before it is context.
3. `planning/decision-log.md` — **Decisions 27–32 (lines ~2532 onwards)** are the most recent and most relevant. Each is tagged "provisional pending Martin's eventual review; subject to OSF amendment."
4. `planning/preregistration-draft.md` — the target document; ~477 lines; incorporates D27–32.
5. `planning/martin-consultation-pack-2026-05-17.md` — the consultation pack sent to Martin 2026-05-17; ~863 lines; reflects D27–32. Useful background for what Martin may push back on.
6. `planning/GPT55-statistical-review.md` + `planning/gemini-statistical-review.md` — the source data for D27–32.
7. `docs/notes/reflections/working-notes.md` — Obs 40 (the diagnostic-triplet substantive findings) and Obs 41 (the stand-in-review methodological lesson) are the most recent entries.

**Open question for Shawn at the start of the new session:** (a) Has Martin replied yet? If yes, his feedback gets folded in before lodgement (and may shift the priority order below). (b) What's the confirmed lodgement date? Tuesday 2026-05-19 is the default; might shift to Wednesday depending on artefact-building progress.

## Priority queue for this session (in order)

1. **[BLOCKING] Shawn's final read-through of the preregistration.** ~30 minutes. The critical gate before lodgement. If any issue surfaces, it gets fixed before steps 2–5.

2. **Build the pre-Phase-2 template-dictionary design artefact.** A bounded ~3-hour task:
   - Create `runs/2026-05-19-template-dictionary/` (or whatever date you commit on).
   - Code: scan filtered LIRE v3.0 for exact-match interval templates (`[not_before, not_after]` pairs with N ≥ threshold). Threshold is a free parameter — straw N ≥ 100, but worth thinking about whether some templates with lower counts should be included for completeness.
   - Outputs: code + dictionary CSV (template intervals × counts × template-type-tier) + REPORT.md.
   - Output should slot directly into Decision 20's slab-structure component of the Bayesian mixture.

3. **Draft the pre-Phase-2 recovery-grid-design artefact.** ~½ day:
   - Create `runs/2026-05-19-recovery-grid-design/` (same date as above).
   - Pin concrete numerical values for: the six genuine-shape-library parameterisations (smooth growth rate; smooth decline rate; rise-and-fall mean/sd; multi-modal frequencies/amplitudes; regnal-cluster anchors at AD 77.5 / 122.5 / 212.5; flat-baseline level); the five tier-weight vectors; sample-size N values from Phase 1 reachability map; replicate count 100; cell-deterministic seed policy; Wasserstein-1 flagging threshold straw; per-category 2× / 1.5× severity cutoffs; per-category numerical PPC bounds (use our straws + Gemini's concrete suggestions in `planning/gemini-statistical-review.md`); aoristic-MC N_MC value (default 30) and divergence-flag threshold (1.5× primary CI width).
   - Mark the α grid axis as "TBD from pilot fit (range to span empirical pilot ± buffer)" — this genuinely requires the pilot fit; do not over-commit.

4. **Date-stamp the prereg's `2026-05-XX` references.** Trivial sed-style edit once steps 2 & 3 are committed. The placeholder appears in six places:
   - `runs/2026-05-XX-recovery-grid-design/` in §3 (validation paragraph), §4 (Phase 2 grid spec), §4 (numerical PPC thresholds line), plain-English walkthrough Step 3.
   - `runs/2026-05-XX-template-dictionary/` in §3 (convention component dictionary-build line), plain-English walkthrough Step 2.
   - Replace `2026-05-XX` with whatever date the artefacts are committed on.

5. **OSF lodgement.** Once steps 1–4 are done and Shawn confirms ready:
   - Commit the date-stamped prereg.
   - Lodge on OSF (Shawn does this; he has the OSF account).
   - Add the OSF DOI to the prereg's §11 Provenance and the project README; this is a post-lodgement edit that goes in as part of the post-lodgement amendment trail.

6. **(Optional, parallel) pymc mixture-model scaffold.** 2–3 days. Could begin in parallel with steps 2–5 if there's bandwidth. The scaffold:
   - `scripts/mixture_model_pymc.py` (or `runs/<date>-mixture-implementation/`).
   - Multinomial primary likelihood; Dirichlet-multinomial supplementary; rescaled NegBin supplementary.
   - Aoristic-MC sensitivity (D28): wrapper that runs the model on N_MC independently-sampled aoristic SPA realisations.
   - Test on synthetic data (recovery-sim infrastructure can drive this).
   - This is **not blocking** for lodgement but de-risks the path from lodgement to Phase 2.

## Branching paths

- **Branch A — Martin has replied before this session starts.** Fold his feedback into the prereg + decision log (likely a new Decision 33+ if any of D27–D32 are revised). Then proceed to steps 2–5.
- **Branch B — Martin has not replied.** Proceed to steps 1–5 as the default lodgement path; Martin's eventual feedback is handled as post-lodgement OSF amendments per §7.
- **Branch C — Martin has replied with substantial revisions.** The lodgement may need to slip to Wednesday or Thursday; revise the queue accordingly. Adela's Friday presentation is the hard deadline; lodgement before then is the goal.

## Critical-friend gates (standing rules from continuity)

- **No silent parameter reductions** in any code that runs. If compute is tight on the template-dictionary scan or the design-artefact draft, halt and report — do not silently scale down.
- **Critical-friend on statistics is a standing rule.** The design-artefact values are statistical commitments; for every threshold value you pin, run the four checks: (a) more appropriate test for the data structure? (b) more powerful / robust alternative? (c) more current best-practice approach? (d) do the method's assumptions actually hold?
- **Sapphire for any non-trivial compute.** The template-dictionary scan is small enough to run locally; the recovery-grid-design draft is just text; the pymc scaffold's synthetic-data testing should run on sapphire.

## Methodological note: the stand-in-statistician review pattern is now part of the toolkit

This project's Obs 41 (in `docs/notes/reflections/working-notes.md`) documents the discovery that **late-stage adversarial review at saturation is role-conditional, not document-conditional**. Stand-in cross-model review in an applied-statistician role surfaced cross-model-agreement items that three rounds of adversarial-rubric review had missed. The pattern is transferable: when a high-stakes document has saturated under one role's review, running it through a stand-in review in a complementary role is cheap insurance. Worth applying to future preregistrations, conference papers, and grant proposals before sending to high-bandwidth-cost human reviewers.

---

End of prompt block.
