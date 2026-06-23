---
title: "Next-session prompt — RAC-TRAC delivery + post-talk pivot (2026-05-22)"
date: 2026-05-22 (drafted at session-close)
audience: "Shawn (paste into the new CC session) + the new CC instance"
purpose: "Brief continuity prompt for the next session picking up after the RAC-TRAC 2026 talk."
---

# Next-session prompt — RAC-TRAC delivery + post-talk pivot

Paste the block below into the new CC session as the first message.

---

Picking up the inscriptions project from the 2026-05-21 / 2026-05-22 session that produced the conference talk + deck + briefing + sensitivity analyses + Phase 2 grid launch. **Adela delivers the paper on Shawn's behalf at TRAC7, Aarhus, Friday 22 May 14:20 (Aarhus time)**.

## Current state at handoff (commit `3e1d74a` on origin/main)

**Deck and briefing ready to deliver as-is.** All artefacts at `planning/conference-talk-rac-trac-2026/`:

- `slide-outline.html` (33 slides; primary delivery format; press `s` for speaker view, `o` for slide overview)
- `slide-outline-slides.pdf` (slide-format backup via Decktape)
- `slide-outline.pdf` (LaTeX paper-document backup)
- `adela-briefing.md` (cheat sheet + Q&A reserve + backup-slide map; ~ 15 min read)

**Deck structure (33 slides total)**:
- title + 9 main (1, 2, 3a, 3b, 4, 5, 6a, 6b, 7)
- deep-dive intro + 12 B-slides (anticipated-question reserve)
- glossary intro + 9 G-slides (plain-English methods explainers)

**Phase 2 mixture-recovery grid is running on sapphire** at `~/cc-scratch/inscriptions-recovery-grid/`. Started 2026-05-22 00:26 sapphire-local. Status as of session-close: 9 of 450 cells completed in ~ 10 hours elapsed. The initial 50 h wall-clock projection looks optimistic — actual mean per-fit wall-clock is 70–90 s under parallel load, putting the realistic estimate closer to **80–120 h**. **Check status first thing**: `ssh sapphire 'cat ~/cc-scratch/inscriptions-recovery-grid/runs/2026-05-22-recovery-grid-validation/outputs/grid-state.json'`. If completion rate is < 5 cells/hour, investigate or accept the longer wall-clock — Shawn has authorised multi-day runs.

## Immediate priorities (in order)

### 1. Adela's feedback on the deck (HIGHEST)

Adela has sent feedback on the deck. **Find it** (Shawn's email; possibly saved to `planning/conference-talk-rac-trac-2026/adela-feedback.md` if Shawn captured it). **The headline framing** Adela has asked for:

- **Less technical detail; more "implications + contribution to the study of Rome / our understanding of Roman history"**.
- Some methodological detail needs to stay, **but briefer** and mostly around three themes:
  - "**Correcting for biases like editorial distortion**" (currently slide 5 + B6 territory)
  - "**Sample size**" (currently slides 3a / 3b territory)
  - "**Regression against Hanson's population**" (currently slides 6a / 6b territory)
- The right statistical-detail level is **"explain to an undergrad history major"** — the G-series methods-glossary slides are written at exactly this level and can serve as a starting point / source for any rewrites needed.
- Plus: any specific feedback Adela called out should be incorporated / clarified directly.

**How to approach**: read Adela's full feedback first; map each request to a specific slide; revise per-slide rather than wholesale. The G-slides are the right tonal anchor for what "undergrad-history-major" reads like in this project's voice. Don't lose the substantive findings (the 30% within-province + the f_within posterior + the editorial-template signature numbers); reframe their presentation.

### 2. Compose full speaker notes / script for Adela

Currently the speaker notes are embedded as HTML comments in `slide-outline.qmd` and render in the revealjs speaker view (press `s` during delivery). They're written in deliverable-prose style but are **per-slide notes**, not a continuous script.

Adela may want a **continuous full-text script** she can rehearse from. Action: extract the speaker notes from the qmd, polish into a flowing read-aloud script that covers ~ 12 minutes of speech (target ~ 1,500–1,800 words), preserve the per-slide structure but smooth the transitions. Save to `planning/conference-talk-rac-trac-2026/full-script.md`.

**Timing constraint**: the talk slot is 20 minutes; ~ 12 min target for delivery leaves Q&A buffer. ~ 1,800 spoken words at standard 150 wpm reading pace = 12 min. So the script should be around that length.

### 3. Phase 2 grid monitoring

Check progress at session start (`grid-state.json`); decide whether to:

- **Let it continue** — the standing authorisation covers multi-day runs.
- **Investigate the concurrency slowdown** flagged in continuity ("Concurrency slowdown unresolved" caveat from 2026-05-22 work). pymc/pytensor incurs 3–5× slowdown under heavy parallel load even with single-threaded BLAS; ~ 1 h of profiling work could shave hours off the remaining time.
- **Reduce scope** — drop replicates per cell, or drop a grid axis. Only if completion looks badly off-track AND Shawn approves the scope-reduction (per the prereg's "no silent parameter reductions" rule).

When the grid finishes, run `runs/2026-05-22-recovery-grid-validation/code/05-grid-summariser.py` to produce the per-cell pass-rate table + the binding-criterion verdict.

## Read in this order to get oriented

1. **Adela's feedback** (location TBC) — first.
2. `planning/conference-talk-rac-trac-2026/adela-briefing.md` — the as-built briefing, useful for understanding which slides do what.
3. `planning/conference-talk-rac-trac-2026/slide-outline.qmd` — the deck source; speaker notes are in HTML comments at the end of each slide section.
4. `docs/notes/reflections/continuity.md` — full project continuity, especially the "Open caveats" section's four post-2026-05-22 entries (concurrency slowdown, pilot_proxy proxy, W-1 thresholds deferred, R-hat gate borderline) and the "Tertiary / future-work analyses" Tier 2/3/4 entries.
5. `runs/2026-05-21-talk-prep/spec.md` and the Phase A sensitivity outputs in `runs/2026-05-21-talk-prep/outputs/tables/sensitivity-*.csv` — the supporting analytical record for what landed in the deck.
6. `runs/2026-05-22-reachability-guide/` — the historian-facing reachability table (Tier 1; in deck as slide 3b) + paper fragment.

## What's done and committed (don't redo)

- Phase A sensitivities (Block 6 three-weighting + Block 7 measurement-error) — both complete; results in `runs/2026-05-21-talk-prep/outputs/tables/`. The measurement-error result is **ROBUST under all σ_pop ∈ {0.1, 0.2, 0.3}**; the three-weighting result shows **material divergence** (population-weighted f_within ≈ 0.50, inscription-weighted ≈ 0.42, unweighted = 0.30 — binding) per the prereg's §5 decision rule. Reported on slide 6b speaker notes + B3 backup.
- Phase 2 mixture-recovery grid — designed, harness implemented, smoke-tested, launched on sapphire. **In flight.**
- Historian-facing reachability guide (Tier 1) — done; slide 3b in main deck; paper fragment at `planning/paper-subsection-reachability.md`.
- Decks: 33 slides; 4 commits since the original 8-slide version.
- Continuity doc: four open caveats from Phase B work logged; Tier 2/3/4 future-work TODOs logged.

## Things explicitly NOT to do unless asked

- **Don't push to the lodged OSF preregistration** — it's committed and embargoed. Any methodology drift goes into the amendment trail, not the lodged doc.
- **Don't auto-launch Phase 2 follow-ups** (Tier 2 finer-bracket grid; Tier 3 per-subset reachability; Tier 4 baorista comparison). All logged in continuity for post-talk work. Wait for Shawn's direction.
- **Don't run anything compute-intensive on the local machine** (amd-tower). Sapphire is the compute target; zbook is a fallback. See scratchpad's 2026-03-24 rule.

## Things this session learned that the next session should keep

- Slide 6 is now 6a + 6b (slide 6a = frequentist NBR comparator, 6b = Bayesian Mundlak — the substantive headline).
- Slide 3 is now 3a + 3b (3a = Phase 1 methodology, 3b = historian-facing reachability).
- The "1,549" headline minimum has been retired in favour of "~ 1,600 (range 1,400 – 1,950 across nulls)" because 1,549 was one specific cell, not a robust headline.
- "Empire reachable at n = 50,000" reads as "the only n tested at empire scale", not "needs 50k to detect" — the actual filtered empire is N = 180,609.
- Decktape + Brave is the slide-format-PDF render path (installed in `~/tools/decktape/`); pass `PUPPETEER_EXECUTABLE_PATH=/usr/bin/brave-browser`. Not a sapphire dependency; runs locally fine.

---

End of prompt block.
