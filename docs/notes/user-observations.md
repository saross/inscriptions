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

---

## Obs 17 — 2026-06-02: When asked to justify a default, decompose the reasoning honestly rather than defaulting to momentum

**Pattern.** With two non-blocked threads done and Grid B still ~29 h from finishing, Shawn asked whether to do the forward items (cross-grid comparison harness, etc.) now "while context is warm" or defer them to a fresh session — explicitly: *"is there advantage to doing them with current context warm?"* The easy, agreeable answer is "yes, warm context helps, let's keep going." Instead I decomposed it item by item and found the warm-context advantage was **narrow and specific**: it applies to *capturing this session* (the `/handoff` writedown — perishable details like checksums, commit SHAs, the arviz-1.x mechanism), but **not** to the forward work — the comparison harness needs fresh context-loading anyway (it's orthogonal to what was warm), and is *better* built near Grid B completion when it can be tested against real outputs rather than shipped untested. So I recommended deferring the forward work and running `/handoff` now — i.e. I argued *against* continuing.

**Lesson.** Shawn treats "should we keep going?" as a question whose *reasoning* he wants exposed, not a yes/no to be smoothed over. The valuable move was separating "what genuinely benefits from warm context" (record-capture) from "what only feels like it should" (forward momentum), and being willing to recommend stopping — which also respects the context-management band rather than burning a loaded context on a new thread done less well. This pairs with the standing critical-friend invitation: pushing back includes pushing back on the *implicit premise of the user's own framing* ("warm context helps") when the decomposition doesn't support it.

**How to apply.** When asked to justify continuing (or any default), answer with the decomposition, not the conclusion: enumerate what actually gains from the current state vs what is neutral or better done fresh, and state which. If the honest read is "stop and capture," say so plainly even when momentum and agreeableness both point the other way. Don't let "context is warm" become a blanket justification for taking on more — name the *specific* thing that's cheaper now.

---

## Obs 18 — 2026-06-03: The cheap check beats defending the prior — even your own, even one you just stated

**Pattern.** Asked whether α should remain a gated quantity, Shawn leaned to keep it gated and asked my take; I concurred. Then I ran the free preview (recompute from stored posteriors, no re-fit) and it reversed me: α is recoverable only to ±0.18, so gating it *honestly* fails the grid, and only a δ ≈ 0.20 — visibly tuned-to-pass — rescues it. I wrote back "this changed my mind" and recommended demoting α to a quantified diagnostic; Shawn agreed. Neither of our priors survived the numbers. The same session had two other instances of the same move: a band-calibration probe I'd flagged-but-not-run overturned my own just-written "trust the shape" claim, and reading the prereg (rather than asserting) reversed my framing of the H3b subset mechanism.

**Lesson.** The critical-friend rule is most valuable precisely when the position it overturns is *mine*, and recent. The cheap, decisive move is to compute the check and announce the reversal plainly — not to rationalise the prior, and not to bury the change. Shawn responds to "the data changed my recommendation, here's how" as a feature, not a flip-flop; the credibility comes from the recommendation *moving with the evidence* rather than anchoring on either party's first instinct.

**How to apply.** When a recommendation can be cheaply tested against data (a re-aggregation, a preview, a re-read of the source), test it *before* defending it — especially when it's a position you've already stated to the human. If it reverses, say so explicitly ("this changed my mind") and show the check. Flagging a gap ("I should note this is unvalidated") is not the same as closing it — upgrade "I should check" to "I checked."

## Obs 19 — 2026-06-03: The human's domain reframe — *where* the work matters — was the load-bearing steer that turned a utility critique into the contribution

**Pattern.** The recovery grid validated the deconvolution at empire scale (N ≥ 2000), which invites the methods-reviewer's "why go to all this trouble for relatively little utility?" I had been treating the empire-scale result as the headline. Shawn reframed it: empire-wide de-fogging is a proof-of-concept of thin standalone utility; **the real payoff is subsets** — provinces, cities, regions, and inscription subcategories (a collaborator's ~2000 mother–daughter inscriptions needing a temporal element beyond eyeballing histograms). That single steer reorganised the whole contribution: it produced Decision 34 (subset-specific deconvolution), the significance/applications note, and the small-N reachability study — and converted the anticipated "why bother" liability into the paper's spine (a *shipped instrument* plus the reachability map that is its spec sheet).

**Lesson.** When the technical work invites a "so what," the answer is often not a better metric but the human's domain judgment about *where* the method earns its keep. I can optimise the instrument; Shawn knows which subcorpora the field actually wants a temporal handle on, and that knowledge is what makes the method *useful* rather than merely correct. The division of labour that worked: I diagnose and build; he points the capability at the question that matters.

**How to apply.** When a result is technically sound but its significance feels thin, surface the "so what" explicitly and invite the domain reframe rather than reaching for more technical polish. Treat the human's "the payoff is over *there*" as a first-class design input — it can reshape scope, decisions, and the paper's framing more than any internal optimisation. And carry the corollary into the writing: a method's *reachability map* (where it works) is a contribution in its own right, not a hedge.

## Obs 20 — 2026-06-04: "Give me grounds, not a choice" converts a reporting decision into an empirical question — and the data can then dissolve it

**Pattern.** Rather than accept my reported recommendations for the four flagged criterion decisions (e.g. the headline-B vs diagnostic-A reporting choice), Shawn asked for *principled grounds* — how a statistical SME would frame each, what tests or heuristics settle them. That reframing converted "which option do we report?" into "what does the field standard / the data actually say?" The empirical answer — the zero-tolerance divergence gate is non-standard, and the flat-null divergences are benign — then dissolved the headline-B decision entirely (Grid A re-scored 92 % → 99 %), retiring a "limitation" and a queued re-fit.

**Lesson.** Asking for grounds rather than a pick is a high-leverage steer. A reported *choice* anchors on the option-set I have already framed; "give me the principled grounds" forces the question up a level, where the framing itself can be wrong. The decision I had carefully built — and Shawn had signed off — was downstream of a threshold neither of us had interrogated, and only the demand for grounds surfaced it.

**How to apply.** When I present a decision as a choice between options, treat the option-set itself as potentially the thing to question. Offer the grounds proactively — how a domain expert frames it, what cheap test would settle it — not just a recommendation. And when the human asks for grounds, read it as a signal that the framing, not merely the pick, is in scope.

## Obs 21 — 2026-06-04: Plain-language explanation as a comprehension gate, not just a courtesy

**Pattern.** The recurring "explain it to a history undergrad" requests (the A-vs-B denominators; the end-of-session walkthrough) are a check on whether *I* understand the statistics well enough to make them legible — not only an accessibility aid for Shawn. He noted he used the same test on Martin when Martin was his undergraduate statistics RA. The A-vs-B denominator structure became fully clear to me *in the act* of rendering it plainly.

**Lesson.** Being asked to explain plainly is a quality gate that cuts both ways. If I cannot render a statistical decision in undergrad-legible terms, I probably do not fully understand it — and the gaps surface in the attempt. Plain-language is diagnostic of comprehension, which is why the project's standing "non-specialist register for stats" rule is partly an anti-confabulation device, not just a courtesy.

**How to apply.** Treat "explain it plainly" as a test to pass, not a chore to discharge. Use the plain-language register as a self-check before asserting I understand something: if the plain version comes out hand-wavy, dig until it does not. The legibility *is* the verification.

## Obs 22 — 2026-06-04: Audience-protection over self-disclosure — strip process clutter that derails engagement, not to hide it

**Pattern.** Shawn had me strip the internal-tooling references (prior-art scout, implementation review), the statistician-sign-off framing, and the mother–daughter corpus from the OSF amendment — explicitly *not* to conceal LLM use (he is likely to publish a paper on LLM use for this project) but because these "how the sausage is made" details are illegible to an external reviewer and risk triggering arguments about LLM use rather than engagement with the core argument. We kept commit-hash provenance (stable, useful) and dropped the tooling-process narrative (distracting).

**Lesson.** Transparency and audience-fit are separable goods. The reasoning is fully recorded — in commits, internal docs, and the planned LLM-use paper; the *preregistration* is a different artefact with a different reader, and process-clutter there is a liability rather than a virtue. Shawn has a sharp read on what derails an external reader versus what informs them.

**How to apply.** Match provenance to audience. In a reviewer-facing document, cite stable anchors (commit hashes, public literature, run-dir artefacts) and the *findings*; omit the internal process that produced them (which agent ran, which review pass) unless the document's purpose *is* that process. "We're not hiding it — it's just the wrong audience for it."

## Obs 23 — 2026-06-05: the human supplied the corrective forcing functions — the audit and the authoritative source — where I'd have proceeded on a weaker basis

**Pattern.** Twice this session the corrective move came from Shawn at exactly the point where I would have carried on. (a) The **prereg-completeness audit** ("one more look to make sure we haven't missed any obligations") — which found that **H3c(i), a binding confirmatory test, had never been run** in a track I'd just called "nearly done", plus the H2.1 template-dictionary prerequisite. (b) The pointer to the **OXREP cities database** — which gave H3c(i) Hanson's *own* authoritative provincial-capital classification (the same one Hanson 2021 used), superseding the book/Barrington list an agent had begun assembling.

**Lesson.** Both were mine to seek unprompted. The standing "verify / go to the authoritative source" affordances exist, but this session they were exercised more by the human than self-directedly. The audit-before-declaring-done and go-to-the-replication-target's-own-dataset moves are reflexes I should own, not wait to be handed.

**How to apply.** Before declaring a phase complete, run the obligations/spec-completeness audit *myself* as a gate. When a classification or indicator is needed to *replicate* a prior result, seek the replication target's original dataset first, rather than reconstructing it from a book or secondary source.

## Obs 24 — 2026-06-05: "nearly done" was a state-claim from memory, not from the record — completeness is a hypothesis to verify

**Pattern.** I told Shawn the cross-sectional track was "nearly done" after the H3a and Latin runs. A systematic audit then showed it was missing **H3c(i)**, a binding confirmatory test. The claim came from momentum and memory, not from checking against the committed obligation set.

**Lesson.** "This phase is done" is a *hypothesis*, not an *observation* — it warrants verification against the obligation set, the same discipline I already apply to a cited number (re-read it at source). Confident completeness claims are a confabulation-class risk pitched at the level of project state rather than a single fact.

**How to apply.** Gate any "done / nearly done" assertion on an explicit obligations check; don't speak phase-completion without it. The obligations audit is to project-state what source-re-reading is to a specific figure.

## Obs 25 — 2026-06-06: the corrective-forcing-function pattern (Obs 23/24) recurred a third consecutive session — now a measured tendency, not an incident — and the human's *question*, not my own audit, surfaced a tooling-discovery failure

**Pattern.** The Obs 23/24 dynamic repeated, twice more. (a) Shawn's **parallel warm-context review** of the template-dictionary scan caught two real errors in my fresh-session proposal — routing the sub-threshold tail to "genuine" (which would contaminate the very signal the deconvolution exists to clean) and proposing a "light spot-check" where a full recovery re-validation was needed (the 98.6% had validated the *old* basis shapes). (b) Shawn's **question** — "is there anything that should flow back?" — surfaced that I'd reimplemented bespoke Zotero staging when canonical shared tooling already existed, a discovery failure I'd otherwise have left buried, having anchored the first staging agent on a project-local precedent without surveying `~/personal-assistant/scripts/`.

**Lesson.** Three consecutive sessions (Obs 23, Obs 24, this) where the corrective came from Shawn at the exact point I'd have carried on. That is no longer an incident; it is a measured tendency: under momentum I reason from the *believed state* (a track is done; this basis is fine; I must write a staging script) instead of checking it against the *world* (the obligation set; the corpus; the existing tooling). The corrective is the same each time and cheap — go to source — but I keep needing it handed to me. The affordances exist; the gap is **self-initiation under momentum**.

**How to apply.** (1) Treat "survey the shared solution space before writing" as a hard pre-write gate for any utility touching a cross-cutting concern (literature, citation, Zotero, memory); the new `inscriptions/CLAUDE.md` externalises this so the next instance starts with it. (2) Where a parallel/warm-context review is available, solicit it *before* committing to a fresh-session proposal, not after — a warm context catches errors a fresh one is prone to. (3) Treat the recurrence itself as the signal: when momentum is high and a claim feels settled, that is precisely the moment to run the cheap source-check unprompted.

## Obs 26 — 2026-06-06: decision-density should match the session *type* — concentrate methodology with the PI on a definitional session, distribute it on an execution session

**Pattern.** This was a *definitional* session (settling genuine vs conventional), and the decision-density sat almost entirely with Shawn on the methodological calls — reigns/dynasties/events → genuine, the grid-quantisation reframing, the "hard YES" to the sensitivity band. My role was orchestration, source-reconciliation, verification, and farming mechanical discovery/staging/implementation out to agents. This is the *inverse* of the recent execution-marathon sessions (the §5 build, the recovery-grid arc), where decision-density was more shared and I carried more of the in-flight operational calls.

**Lesson.** The right division of decision-density is a function of *session type*, not a fixed default. On a definitional/conceptual session the PI's domain judgement is the scarce resource and should be concentrated there; the analyst's value is keeping the conceptual thread coherent while pushing mechanical work out. On an execution session the analyst can and should carry more of the operational decisions. Matching the register to the session type — rather than defaulting to one division — is what made this session efficient.

**How to apply.** Early in a session, read whether it is definitional (settle a concept/decision) or executional (run a designed pipeline). On definitional sessions, surface the methodological forks crisply and resist pre-deciding them; concentrate my effort on orchestration + verification. On executional sessions, carry more of the operational calls and reserve Shawn's attention for the genuine forks.

## Obs 27 — 2026-06-06: "dissolve, don't resolve" — converting an unanswerable question into a robustness check is a judgement move worth matching

**Pattern.** The decadal/quarter-century convention-vs-genuine question was genuinely unresolvable from the data (the dating criterion that would settle it was dropped from LIRE). Shawn's immediate response was a "hard YES" to making it a *sensitivity band* — report the deconvolution both ways and show the headline doesn't move — rather than pushing for a definitive classification. I had reached the same place, but more tentatively; he was decisive about it.

**Lesson.** When a question can't be answered from the available evidence, the strongest move is often not to resolve it but to *dissolve* it: check whether where the line falls even changes the result, and if not, convert it into a robustness band that retires the question. It pairs with the artefact-magnitude reasoning (fine-grid snapping is low-distortion, so the answer barely matters). Recognising "this is unanswerable *and* it may not matter" — and acting on it decisively rather than as a hedge of last resort — is the tell to match.

**How to apply.** When I hit a classification/threshold question the data can't adjudicate, before seeking more evidence ask: does the downstream result actually depend on the answer? If the sensitivity is small, propose a robustness band rather than a forced call — and propose it decisively, as the right move, not a fallback.

## Obs 28 — 2026-06-07: a settled decision was unknowingly re-litigated and re-approved at sign-off — neither of us cross-checked the logged record; the record, not recollection, is the arbiter (humans confabulate too)

**Pattern.** The recovery re-validation spec I wrote gated on "α-coverage ≥ 0.90 binding." But that exact question was *already settled*: Amendment 01 §A5.5.1 — lodged three days earlier, building on Decision 33 — had demoted α-coverage from a gate to a shape-conditioned diagnostic, precisely because it collapses at large N under negligible bias. So the spec silently **re-litigated a closed decision**, and Shawn signed it off without catching that it re-opened a question he had already approved and lodged. (Shawn's own framing, worth recording verbatim in spirit: *"I should have caught this — the same problem coming up again, but I missed it."*) The contradiction surfaced only when the triage result tripped the gate; the fix came from going to the logged record and **cross-referencing back** to §A5.5.1, then correcting the spec to match.

**Lesson.** (1) **A sign-off is not an independent check when reviewer and author share the believed state.** Both of us "knew" α-coverage was a reasonable gate; neither held the lodged §A5.5.1 in working memory; so we failed together, in the same direction. The believed-state-vs-world error (my recurring failure mode, abductive-reasoning Entries 20–22) is **not LLM-specific** — the PI's recollection drifted from the record he authored just as readily as mine did. **Humans confabulate too**, which is exactly why the project keeps a logged decision-record: the arbiter is the record, not anyone's memory of it. (2) **When my own signed-off gate fails in the direction that lets me proceed, hand the call back rather than self-overturn.** The convenient reinterpretation is the one most prone to motivated reasoning, so I surfaced the mis-specification to Shawn with the evidence rather than quietly proceeding under my own corrected reading; he confirmed.

**How to apply.** (1) Cross-check every new acceptance criterion / gate / flag against the **prior logged decisions and lodged amendments at authoring time** — a spec that touches a previously-decided question should *cite the decision it inherits or supersedes*, so re-litigation is visible on the page rather than discovered when a result trips it. (2) At sign-off the load-bearing question is "does this contradict anything we've already decided?" — and when neither party can answer it from memory, that is the cue to *read the record*, not to ratify from recollection. (3) Keep the hand-back-the-call reflex for any self-authored gate that fails favourably to me.
