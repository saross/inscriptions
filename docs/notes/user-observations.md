---
priority: 2
scope: always
title: "User-observations register — inscriptions project"
audience: "next CC instance; Shawn (rare reads)"
status: living; entries land at `/handoff` time and accumulate
started: 2026-05-21
last-updated: 2026-05-21
---

# User-observations register — inscriptions project

## How to use this file

- Per-project log of meta-level observations about *how we work together* on this project. Distinct from `working-notes.md` (substantive empirical observations) and `continuity.md` (state).
- Entries land at `/handoff` time as Shawn-accepted candidates. Each entry captures a working-relationship pattern, a learned lesson about Shawn's preferences, or a session-dynamic worth carrying forward.
- New CC instances **should read this file** before substantial work, to calibrate to the working style.
- Do not modify accepted entries in place — corrections go in as new entries that cross-reference the older one with `[[obs-N]]` (the entry's slug or number).
- Entries here may feed `~/personal-assistant/notes/working-with-claude.md` at `/weekly-review` curation time.

---

## Obs 1 — 2026-05-21: Visual checking of binary artefacts cannot be delegated upstream

**Pattern.** During the OSF supplementary PDF iteration cycle, I claimed "fixed" four times (v1 → v4). Each time I had run a small inspection (rendered a page; spot-checked text extraction; verified the source had the right escape) and concluded the artefact was ready. Each time, Shawn caught a new rendering issue by visually scanning the full PDF and pointing at a specific page: the H3c(i) table cell on p. 24; the ASCII flowchart overflow on p. 30; the H3a NBR formula on p. 12; the DOI URLs in §13. My author-side checks consistently failed to catch what Shawn's visual scans caught immediately.

**Lesson.** When generating a visual artefact (PDF, slide deck, figure, chart), my "fixed" claim should be treated as provisional until Shawn has visually scanned the rendered output himself. The fix-and-confirm cycle must explicitly route through his eyes, not just my spot-checks. For high-stakes one-shot artefacts (lodgement deposits, submission deliverables, conference outputs), assume the first generation is wrong and the second-or-third is closer.

**How to apply.** After generating any non-trivial PDF / slide deck, surface it via SendUserFile *before* declaring "ready." State "v_N PDF generated; please visually scan before I commit and consider it ready." Then iterate on the feedback. Don't commit the artefact as the lodgement copy until Shawn has confirmed visually. Captured from PDF iterations v1 → v4 of `planning/osf-supplementary-2026-05-20.pdf`.

**Cross-references.** Working-notes Obs 45 (adversarial verifier for source-vs-render comparison) — the verifier caught what neither I nor Shawn could have caught from the source markdown alone; visual + adversarial-verifier together are the safety net.

---

## Obs 2 — 2026-05-21: "A+ with lean A fallback" framing translates cleanly to gated planning; Shawn values that

**Pattern.** When I proposed the conference-talk scope and asked "lean A or A+?", Shawn answered: *"A+ if possible with fallback to lean A if required."* That phrasing — explicit best-case scope, explicit fallback, explicit gate condition — translated directly into the analysis roadmap as hour-18 and hour-26 decision gates with concrete go / no-go criteria. The structure made the work modular, protected against scope creep, and gave the implementation session clear permission to bail on the stretch without renegotiating.

**Lesson.** When scoping time-bounded work, ask Shawn for the **scope ceiling AND fallback**, not just "what scope?" His default framing seems to be "ambition with explicit retreat conditions," and planning artefacts should mirror that shape.

**How to apply.** For any time-bounded task (analysis run, talk prep, lodgement push, demo build), structure the scoping question as: "best-case scope; minimum-viable fallback; explicit gate criteria for the transition between them." Build the gates into the roadmap, not as afterthought caveats. Captured from the 36-hour analysis roadmap at `planning/conference-talk-rac-trac-2026/analysis-roadmap.md`.

---

## Obs 3 — 2026-05-21: Anti-confabulation discipline holds best when re-verification is part of the build pipeline, not an afterthought

**Pattern.** The LIRE v2.3 vs v3.0 DOI mismatch was caught because the BibTeX-generation step routed through CrossRef + DataCite + Zenodo API calls — *not* through "look up what the prereg already cites." When the API returned `v2.3 / 2023-07-14` for what the prereg had cited as `v3.0 / 11 October 2023`, the mismatch surfaced immediately. If I had trusted the existing prereg's stated DOI without re-verification, the wrong-version citation would have entered the permanent OSF deposit. The verifier-after-PDF-generation step similarly caught the pipe-in-cell bug because it independently extracted PDF text rather than trusting "the source markdown looks right."

**Lesson.** Re-verification works when it's structurally embedded — fresh API calls, fresh agent contexts, fresh source-vs-render diffs. It fails when it's a "double-check by re-reading what I already wrote" exercise (which can't catch the welded-fragment errors Opus 4.7 is prone to). This session's anti-confabulation wins all came from structural separation, not from extra care.

**How to apply.** When producing high-stakes artefacts, build verification steps that go to *external sources* (APIs, fresh agents, original files) rather than internal re-reads. Author cannot reliably audit author. Especially: any cited DOI / identifier should be re-fetched from its registrar; any rendered artefact should be compared against its source by a fresh-context agent. Captured from the OSF lodgement workflow (Zenodo DOI fix at commit `3da5711`; verifier dispatch leading to `42f639d`).

**Cross-references.** Working-notes Obs 44 (Zenodo concept-DOI vs version-DOI confusion) and Obs 45 (adversarial verifier for binary artefacts) — the empirical / pattern complements to this user-observation.

---

## Obs 4 — 2026-05-21: Externalising overnight planning ahead of a new session pays off — but visible uncertainty markers are what make it usable

**Pattern.** The overnight planning session for the RAC-TRAC talk produced five planning docs + continuity update + handoff prompt before Shawn signed off. None of that work would have been usable in the next session if I had buried the speaker-identity and OSF-DOI ambiguities inside the docs. Instead, the handoff prompt led with a `⚠️ TWO OPEN QUESTIONS TO CONFIRM` block and the analysis-roadmap had a `speaker-question:` field at the top of its YAML frontmatter. When Shawn returned in the morning, the two questions were the first thing he addressed — both resolved within minutes, freeing the rest of the session for substantive work.

**Lesson.** An externalised plan is only as useful as its *visible uncertainty markers*. Burying open questions in dense planning prose makes them invisible at handoff-read time; surfacing them at the top with explicit `⚠️` / `❓` markers makes the receiving session start with them.

**How to apply.** Whenever an overnight or session-spanning plan is produced, ensure the handoff document opens with **explicitly-marked unresolved questions** as the first content section. Treat them as the gating items for the next session, not buried alongside the body content. The handoff is for unblocking the next session, not for displaying the work done. Captured from `planning/next-session-prompt-2026-05-21.md`'s opening structure.

---

## Obs 5 — 2026-05-22: Visual-scan verification is the only real review for visual deliverables

**Pattern.** During the RAC-TRAC deck rewrite I made several errors that were structurally invisible to automated review and only catchable by Shawn's manual visual scan of the rendered PDF. Three explicit cases in one session: (1) the "A1." baked-in matplotlib title at the top of `fig-02a-empirical-spa.png` — invisible to grep, invisible to qmd review, only seen when Shawn opened the rendered PDF; (2) the slide-3a caption I wrote saying "Top row = null with no planted event" when the figure's null row is at the bottom — visible in the figure but caption-wrong, only caught when Shawn looked at the rendered slide; (3) backup slides B1, B3, B7, B13 overflowing the slide-area in PDF render — caught only when Shawn paged through the deck. In every case the source markdown looked fine. My author-side review consistently failed to catch what the rendered-artefact visual scan caught immediately. This is the same pattern as Obs 1 (OSF supplementary PDF), now with three more data points from a different artefact class.

**Lesson.** For visual deliverables — slide decks, rendered PDFs, figures, dashboards — the only reliable review pass is a human visual scan of the rendered output. Source-side review of the markdown / code / Quarto is necessary but not sufficient. My "looks fine to me" is *systematically* less reliable than "let me actually look at the PDF". This is not a "I should try harder" failure; it's a structural property of how the artefact is generated (binary outputs hide content from text-based review).

**How to apply.** Whenever I produce a visual artefact (PDF, slide deck, rendered figure, chart, screenshot), do NOT declare it "ready" or "fixed" based on source-side checks alone. Surface the rendered output to Shawn and explicitly ask for a visual scan: *"Rendered PDF attached; please visually scan before treating as ready."* For multi-page artefacts, ask him to page through. Build the visual-scan step into the workflow rather than deferring it. The cost of one extra round-trip is trivial; the cost of an artefact-with-defect going out the door is substantial. Captured from three errors in one session — figure-title baked-in (commit `47ff7ce`), caption row direction (commit `47ff7ce`), backup-slide overflow (commits `47ff7ce` / `80f3805`).

**Cross-references.** This is the same pattern as Obs 1 (OSF supplementary PDF iterations); this entry adds three new data points (figure titles, caption-figure misalignment, slide overflow). Together they suggest the pattern is general to *any* visual artefact, not specific to one document class. Also relates to memory `2026-05-22-96af8f645552` (matplotlib `set_title` bakes invisibly into PNGs).
