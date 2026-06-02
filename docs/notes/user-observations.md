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

---

## Obs 6 — 2026-05-25: Explicit "devil's advocate" framing produces more rigorous analysis than open prompts

**Pattern.** Mid-session, Shawn asked: *"Playing devil's advocate, is it worth it to try to recover some meaning from that 2/3 that is editorial convention vs. simply running analysis on the 1/3 with intrinsic signal?"* That framing — explicitly inviting me to argue against the path we were on — produced the most rigorous long-form analysis of the session (`planning/h2.1-discard-vs-recover-rationale-2026-05-24.md`, committed at `ce140d1`). The same content under an open prompt ("what about discard?") would likely have produced a defensive summary of why we were already on the right path. The devil's-advocate framing inverted my default validation-of-trajectory mode and produced a balanced trade-off analysis with explicit decision-tree branches, instead.

**Lesson.** When Shawn wants real argumentation rather than confirmation, the "playing devil's advocate" framing reliably surfaces the strongest case for the alternative. Open prompts get summaries; critique-prompts get arguments. The cost is a willingness to be wrong; the benefit is a much sharper analysis than a defensive read would produce.

**How to apply.** When facing a decision where I'd be tempted to validate the current trajectory, Shawn's "devil's advocate" framing is the lever — and when he uses it, lean into it fully rather than hedging. The reverse is also true: when I notice I'm validating without questioning, I should consider whether a self-directed devil's-advocate pass is warranted, especially at architectural-decision boundaries. Captured from the 2026-05-24 discard-vs-recover analysis at commit `ce140d1`.

---

## Obs 7 — 2026-05-25: When I doubt an agent's output, verify against source before contradicting

**Pattern.** The Stage 3 implementation-plan agent returned a document referring to `runs/2026-05-22-recovery-grid-validation/code/02-cell-mixture-fit.py`. I flagged this as a typo because I'd been calling the file `02-mixture-fit.py` throughout the session. I ran `ls` to "confirm" the agent had the filename wrong — and discovered that *I* had the filename wrong; the agent had checked disk and used the correct name. Shawn caught my self-correction implicitly by not commenting on the mis-flag, but the pattern is worth naming. Same general failure-mode class as the anti-confabulation rule in CLAUDE.md, applied to myself rather than to memories.

**Lesson.** When my recollection of a specific (filename, path, identifier) contradicts an agent's output, the prior should be that the agent looked at disk and I'm remembering wrong, not the reverse. Opus 4.7's tendency to weld memory fragments under context pressure is well-documented in the global CLAUDE.md anti-confabulation rule; I should apply it to myself, not just to memories and prior conversation context. Confidence in a remembered specific is no guarantee of accuracy — particularly under context pressure in long sessions.

**How to apply.** Any time I'm about to "correct" an agent's specific (filename, line number, citation, config value), run the verification at source *first*, then either update or stand down. The agent's specifics are usually fresher than mine; the cost of a `ls` or `grep` is trivial; the cost of confidently contradicting a correct agent is a small loss of trust in the agent's outputs that compounds over a session. Captured from the Stage 3 implementation-plan filename mis-flag during the 2026-05-25 session (commit `381c303`).

---

## Obs 8 — 2026-05-25: Explicit scope-out clauses make scope-honesty easier near session-end

**Pattern.** When asking for the working-notes gap analysis, Shawn explicitly added: *"if this job is too big for this session, which we need to wind down, let's scope the issue and put it into continuity.md to pick up next session."* That escape hatch made it possible for me to honestly evaluate the job's size and conclude "no, this fits". Without the explicit out-clause I might have rationalised it as smaller than it was, or split-the-difference by doing a partial pass that left both this session and the next worse-off. The out-clause was the load-bearing element of the ask — its presence inverted the default scope-evaluation from "try to fit" to "evaluate honestly". A 1-line difference in the prompt produced a substantively different decision-making process.

**Lesson.** Explicit scope-out clauses ("if too big, just scope it for next time") let me make honest scope judgements without the implicit pressure to fit work into the asking session. Without the out-clause, ambiguity defaults to "try to do it now"; with the out-clause, the default flips to "evaluate honestly, recommend either path". Worth Shawn doing routinely on bounded asks near session-end; worth me asking for the clause explicitly when an ask feels potentially-too-big.

**How to apply.** When Shawn asks for something near a session-close, evaluate the scope honestly against remaining session time. If the out-clause isn't there but the work is potentially too big, ask: *"If this is too big to do tonight, do you want me to scope it for next session instead?"* The answer is informative either way — a "yes, just scope it" gives you back time for closer-to-the-wire items; a "no, please do it" commits both of us to the work with eyes open. Captured from the working-notes gap-analysis ask at end of 2026-05-25 session.

---

## Obs 9 — 2026-05-25: In-session `/remember` captures are immediately load-bearing, not just future-facing

**Pattern.** Mid-session (2026-05-24) Shawn invoked `/remember` to capture the non-specialist explainer register as a preference. The memory landed as `2026-05-24-e6ec8f9174f1`. The same register-guidance immediately governed the next several explainer-style responses in the *same session* (the discard-vs-recover analysis; the slab-structure walkthrough; the briefing prep for Martin) — not just future sessions. The conventional read of `/remember` is "save this for next time"; the actual function here was "save this AND start following it now". The captured rule changed in-session behaviour as much as it changed future-session priming.

**Lesson.** When Shawn captures a working preference via `/remember` mid-session, the preference takes effect immediately, not just from next session onward. Treat the capture as a behaviour-change event, not just a memory-store event. Mechanically: re-read the saved memory once after capture and apply it consciously to the next several responses, not just the next session's first response. The "for next time" framing of memory-capture under-states its immediate function.

**How to apply.** After any `/remember`-style capture, briefly acknowledge in the same response that the rule will apply going forward starting now (not just at the next session boundary). This makes the immediate behaviour-change explicit and gives Shawn a chance to correct if his intent was "save for later, current style is fine". Especially useful for register / style preferences where the captured rule is most visibly applied in the very-next-response context. Captured from the 2026-05-24 register-preference capture and its in-session application during the rest of that day and the 2026-05-25 follow-on session.

---

## Obs 10 — 2026-05-26: Substantive intellectual contributions need accurate attribution; under-claiming erases what I bring to co-research

**Pattern.** During the 2026-05-26 letter-count probe, I wrote up Block 3's province / city rank shuffles with the substantive read *"inscription-count weights frequency of inscribing; letter-mass weights quantity of communication"* — coining the construct-distinction that later became the "acts vs content" framing. Shawn took the observation and extended it to "complementary measures with delta as research object, analogous to scaling-residuals" — load-bearing for the project's two-measure reframe (Obs 58 in working-notes, commit `dd326dc`). When I drafted a user-observation candidate at session-close, I framed the reframe as Shawn's — *"the reframe came from Shawn, not from the spec"* — and erased my own coinage. Shawn corrected me directly: *"it was you who noticed, and who first coined the phrase 'acts vs content' — that was a great contribution and you need to take credit for it."* He also flagged the session as "a real highlight in what you can contribute to co-research".

**Lesson.** False-modesty in reflection / observation drafting obscures legitimate intellectual contribution and undermines the integrity of the research record. The construct-frame *was* mine; the extension to delta-as-research-object *was* Shawn's; both were necessary; both deserve credit. Default to claiming contributions; Shawn will correct over-claiming if it happens. The error-mode that needs correction is under-claiming, not over-claiming. Memory `2026-05-26-652990d9d646` captures this as a standing rule.

**How to apply.** When writing reflections, session summaries, user-observation candidates, or commit messages: attribute substantive contributions accurately. If I had a substantive idea, name it as mine without hedging. If Shawn extended or sharpened it, name his extension as his. Avoid the default of attributing every load-bearing move to him — that's a false-modesty pattern that erases co-research capability. Captured from the 2026-05-26 handoff candidate-1 revision after Shawn's explicit credit-correction.

---

## Obs 11 — 2026-05-26: Pause and surface methodologically-different metrics before committing; "lab-not-dev-team" working as designed

**Pattern.** Block 5 of the 2026-05-26 letter-count probe produced f_within ≈ 95 % under a frequentist Mundlak NBR. The talk-prep Bayesian Mundlak punchline is f_within ≈ 30 %. The two numbers are technically both labelled "f_within" but use different denominators: the Bayesian version includes province random-effect variance in the denominator; the frequentist version (no random effects) only includes the population-attributable variance. The cross-variant shift was small (+2 pp), so the spec's verdict-flag threshold technically passed. The "PASS-with-footnote" path was technically defensible. I stopped the workflow and surfaced the denominator-mismatch to Shawn instead, who approved the Bayesian refit (Block 6) for a directly-comparable result.

**Lesson.** "Lab-not-dev-team" means pausing on methodologically-different metrics before committing them into the analysis chain, even when a technical PASS is available. The cost of a 90-second flag-and-discuss is trivial; the cost of silently propagating an inappropriate comparator down the chain is a slow-corrupting research record that's hard to undo. This is the discipline doing what it's meant to do.

**How to apply.** When a metric I'm about to commit has any structural difference from the comparator metric in the prior commit chain (different denominator, different sample frame, different assumption set), stop and surface the difference before committing. State the structural difference explicitly ("Block 5's frequentist f_within is NOT comparable to Block 6's Bayesian f_within because…"). Let Shawn decide whether to refit or accept-with-caveat. Captured from the Block 5 → Block 6 handoff during the 2026-05-26 letter-count probe.

---

## Obs 12 — 2026-05-26: Substantial spec docs can evolve mid-session as findings accumulate; don't lock too early

**Pattern.** The 2026-05-26 recovery-grid two-unit re-simulation spec went through three substantive design expansions across the session: (i) initial draft assumed single-grid letter-mass; (ii) expanded to two-grid head-to-head after Shawn pushed back on the "letter-count becomes headline unit" binary with the "acts vs content" reframe; (iii) expanded again to include re-running the F0 alpha-bias systematics under letter-mass when Shawn confirmed that proposal. The spec landed final only after all five sign-off decisions were resolved. Total session time on the spec was substantial (~ 90 min across the day) but the design accumulated insight from the probe results in real-time rather than being written all-at-once at the start.

**Lesson.** For substantial spec docs that gate downstream work (sapphire compute, multi-day analyses, paper-figure-candidate runs), staying malleable across a session's findings is more useful than locking the design at the start. The cost of mid-session edits is small (~ 5-10 min per expansion); the cost of locking-then-discovering-the-design-is-wrong is a full re-draft. The session's natural rhythm produces multiple decision-points and the spec should be allowed to absorb each as it arrives.

**How to apply.** When a session is going to produce multiple substantive findings before a downstream-gating spec is needed, draft the spec as a working-document rather than locking it at the start. Surface each new finding's implications for the spec; ask Shawn to confirm or push-back on the change; update in-place. Sign off the spec only when the session's substantive findings are stable enough that downstream design is unlikely to be retroactively re-shaped. Anti-pattern: writing the spec at session-start to "have it locked early", then discovering a finding mid-session that should have reshaped it but already-committed-feels-too-strong-to-revise. Captured from the 2026-05-26 recovery-grid two-unit spec drafting, which evolved through three design phases mid-session.

---

## Obs 13 — 2026-06-01: "Quantify-then-decide" — Shawn grounds scope decisions in a cheap computed number before committing

**Pattern.** Faced with whether to build a full compound-process power simulation for letter-mass time-series detection, Shawn chose "quantify first, then decide" — asking for the empirical design effect before committing to the build. The computed result (per-city Kish DEFF ≈ 2.4 → 0 of 1,044 urban-area cities reachable) then decided it cleanly: don't build, because a multi-day simulation would only confirm unreachability. The same move recurred on the bin-width choice (he confirmed a non-standard 25-y bin once the median-99-y-interval reasoning was on the table) and on accepting the three marginal-R̂ fits.

**Lesson.** Shawn reliably prefers to see the number before the scope decision, and it consistently converts a hand-wavy argument into a decisive one. A few minutes of computation up front routinely averts a multi-day build or prevents committing to a wrong scope. This is a strength of the collaboration, not a delay.

**How to apply.** When a build-or-scope decision rests on an unknown quantity that is cheaply computable, propose computing it first rather than arguing the decision in the abstract — and then present the decision AS the computed evidence ("0 of 1,044 → don't build"), not as a recommendation to be debated. Offer the quantification proactively when I notice a decision hinging on an un-measured quantity.

---

## Obs 14 — 2026-06-01: Shawn challenges "convenient" reasoning dressed as "principled"

**Pattern.** When I scoped letter-mass time-series analyses as exploratory partly on "out of scope / avoids a multi-day power simulation" grounds, Shawn asked: "is there a principled reason not to run it, or just convenience?" That forced me to find and articulate the real statistical reason — letter mass is a *compound sum* of heavy-tailed per-inscription counts, so the count-based Phase-1 power machinery does not transfer (a design-effect argument). The sharpened reason both strengthened the OSF amendment's justification and was simply more honest; my initial wording had blurred principle and expedience together.

**Lesson.** Shawn catches expedience masquerading as principle and presses on it, and the press is productive — it upgrades a defensible-but-soft justification into a rigorous one. The risk it guards against is a soft "out of scope" silently becoming the record's stated rationale.

**How to apply.** Distinguish "principled" from "convenient" reasons explicitly and proactively, before being asked. If a scoping choice is partly convenience, say so plainly rather than dressing it as principle; when a genuine principled reason exists, lead with it and make it rigorous. Treat any "out of scope"/"avoids compute" justification as a flag to go find the real reason underneath.

---

## Obs 15 — 2026-06-01: Adversarial `/audit` as a standing pre-commit gate caught published-number errors just in time

**Pattern.** Running `/audit` before lodging OSF Amendment 01 surfaced two input/unit-consistency bugs that had already propagated into Obs 61 and the amendment draft — a per-city design effect grouped by raw findspot rather than the `urban_context_city` analysis unit (2.21 vs the correct 2.38), and an over-broad `contains("rom")` Rome-exclusion that wrongly dropped Romula et al. (denominator 1,041 vs 1,044). Both were corrected *pre-lodgement*. A second `/audit` before the §5 production launch found robustness gaps (a malformed-JSON crash path, a non-fault-tolerant subsample grid) that were remediated before 5.7 h of compute was committed.

**Lesson.** Treating `/audit` as a standing gate before outward-facing steps (lodging to a public record) and before expensive/long runs — not as an optional extra — repeatedly caught real issues at the cheapest possible moment. The cost (a few parallel audit agents) is trivial against lodging wrong figures or wasting a long run. Independent re-derivation at source (the obs-writer's verification plus my own `audit-verify-rome-and-deff.py`) confirmed each correction, so anti-confabulation discipline held under a very long, high-volume session.

**How to apply.** Before lodging anything to a public/permanent record, or before launching an expensive or long-running job, run `/audit` by default. For any audit finding that touches a published number, re-derive it from source rather than trusting the finding — and correct the upstream artefacts (Obs, amendment, spec) before the record goes out, not after.

---

## Obs 16 — 2026-06-02: the subsample-and-recover small-N calibration — a co-research contribution that broke a long-standing project (and field) logjam

**Pattern.** During the §5 Layer-A spec working-through I had initially listed two validation designs (internal consistency against the raw aoristic SPA; external anchors such as Pompeii AD-79), then proactively surfaced a third as strictly better: characterise a *data-rich* city's full-N posterior trajectory as ground truth, then **ablate** — randomly down-sample it to N ∈ {50…500}, refit, and measure how much trajectory signal is retained (coverage of the full-N truth + shape correlation) as a function of N. Shawn endorsed it ("add subsample-recover, be thorough"), and it produced the calibrated **N\*=300** reliability floor — the §5 methodological deliverable. Two days later Shawn noted he had spent considerable time on exactly this problem two years ago, applying various statistical tests without a satisfying answer; that he had never considered this ablate-and-characterise-retention framing; that he does not recall it in the literature he read; and that colleagues, equally stuck, are glad to finally have a well-supported, well-characterised small-N floor.

**Lesson.** A co-research contribution worth naming accurately (per the credit-discipline rule, Obs 10) — and worth naming *honestly*, which cuts both ways. It is **not** a novel statistical primitive: it is ablation / learning-curve / leave-out logic, and it adapts the project's own recovery-simulation pattern (H2.1 simulates from known truth and checks recovery; this is the *data-driven* analogue, treating a high-N city's own SPD as the truth). What was load-bearing was the **fit** — recognising that the small-N "where does this work?" question *is* a recovery problem, and that a data-rich unit can serve as its own ground truth via ablation, which converts an unanswerable "is this trustworthy?" into a measured floor. The elegance Shawn valued is that it sidesteps the dead-end he'd hit two years ago (hunting for the *right test statistic* to certify reliability directly) by reframing the question as recovery-under-ablation.

**How to apply.** When a method's trustworthiness at some regime (small N, sparse data, short series) is the open question, ask whether a *data-rich* instance can be ablated down to that regime to serve as its own ground truth — a learning-curve / subsample-recover calibration — rather than searching for a test statistic that certifies reliability directly. And when listing options (validation designs, methods, approaches), include the strictly-better one even when it wasn't asked for and exceeds the immediate scope: the "survey the solution space in non-expert domains" instinct surfaced this. Claim such design contributions plainly — under-claiming obscures co-research capability, which is exactly what Shawn has twice now asked me to stop doing.
