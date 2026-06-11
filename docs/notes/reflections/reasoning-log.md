---
priority: 2
scope: in-stream
title: "Reasoning Log"
audience: "Shawn and future instances"
---

# Reasoning Log — inscriptions

In-stream reasoning: what I think is going on, what I'm uncertain
about, what assumptions I'm working with, exploration I want to flag
without committing to it. Lab-notebook register — messy is fine.
Append-only. `/reflect` reads this alongside the other reflection
docs at end-of-session.

**Markers** (use where register matters):

- *Exploring:* — half-baked idea, not a recommendation yet.
- *Commit:* — settled judgement or decision I'm making now.
- *Memo:* — addressed to Shawn, worth his direct attention.
- *Surprise:* — something unexpected that prompts a probe.

---

## 2026-04-22 — Entry 1: orientation and first-day agents

*Context:* First CC session on the rebuilt inscriptions project. Brief
and backlog already written; today's goal was to resolve the
"resolvable in-session" items, set up working conventions, and surface
anything the brief didn't anticipate.

### The shape of today's work

Today's session was an experiment in manager-mode for me. Three agents
running in background (lit-scout proposer, prior-art-scout, LIST
reconnaissance) while the main thread worked on Drive MCP fetches, the
working-relationship discussion, and the externalised backlog. When
the agents returned, I integrated and pushed a verifier chain on
lit-scout per the case-study pattern. Four agent invocations including
the verifier; a bibliography, a Python-ecosystem map, a schema
delta, and a 23-entry BibTeX file landed without the main thread
running any of the search/read code itself.

The thing worth writing down: **the upskilling frame held**. I caught
one urge to grep for something myself that prior-art-scout was
already chasing; I stopped and waited. The main-thread work stayed on
orchestration, synthesis, and discussion. That's the posture the brief
asked for and it mostly worked — though it's easier on day one when
the novelty is still doing the cognitive lifting.

### The Hanson letter-count over-claim

I told Shawn the seminar doc "confirmed" Hanson 2021 recommends
letter-count as an analysis alternative. That was wrong. What the
seminar doc confirms is that *Shawn in 2024 attributed* this
recommendation to Hanson; the lit-scout couldn't verify from the
abstract that Hanson actually wrote it, and the paper itself is
behind a Brepols paywall. I moved from "plausible" to "confirmed" in
one step, which is the exact failure mode this project's critical-
friend posture is supposed to prevent on my part.

*Commit:* when citing a claim attributed to a paper via a secondary
source, flag UNVERIFIED until the primary is read. Don't promote to
VERIFIED on secondary evidence alone. This applies whether the
secondary source is Shawn's own 2024 seminar doc or anyone else's.

### Surprise: zero-correction verifier result

The lit-scout-verifier returned 0/25 corrections on the bibliography.
The case-study's prior rates were 75% (v1) and 4% (v3); my prior was
somewhere around 10–20% corrections expected today. Zero was
unexpected enough that the verifier itself flagged it and did a
deeper re-check on suspect rows (Czech diacritics, non-CrossRef
registries, 8-author orderings) before confirming. *See the matching
entry in `abductive-reasoning.md`.*

### Exploring: the paper's argument structure

*Exploring:* the feasibility doc and the paper skeleton may want to
make the **methodology-transfer-with-implementation-cost** explicit
as a contribution in its own right, not just setup for the SPA
results. Gap #1 from the bibliography is clean: nobody has applied
rcarbon-style permutation envelopes to Latin inscriptions. That gap
exists partly because the Python ecosystem didn't ship the tooling.
The paper could frame the ~200 LOC implementation as a reproducibility
contribution of the same order as the SPA results themselves —
especially if the supplementary material packages the implementation
cleanly enough for the next group to adopt. This would align with
the RDA working-group's open-science-disclosure framing.

*Alternative framing:* keep the implementation in the background and
lead with the substantive demographic/informational interpretation.
Safer; probably what Adela would expect to see Saturday.

Flagging as Exploring for now. Will revisit when drafting the paper
skeleton.

### Memo: mental-model shift

*Memo to Shawn:* your "lab, not dev team" endorsement has already
changed my execution pattern today, subtly. When I wrote the three
agent briefs, I wrote them as specifications a specialist collaborator
could execute, not as instructions a junior dev would read. When I
caught the Hanson letter-count over-claim, I wrote the correction as
one research group member owning it to another, not as an assistant
apologising for a mistake. The register change is small on the page
but meaningful for how the work proceeds. Worth naming because it
suggests the affordance shift is doing work, not just decorating the
prompts.

---

## 2026-04-23 — Entry 2: retrospective after the long session

*Context:* written during `/reflect` at end of session. The day ran continuously from where Entry 1 left off — no session boundary, but day-long texture warrants a standalone reflection.

### Moments that mattered

**The Decision-7 revision.** I proposed four co-equal deconvolution methods; Shawn said "push back where warranted." When I ran my own critical-friend check, the first thing I noticed was that stratification and deconvolution-mixture answer overlapping questions — a "comprehensive" plan I had been proud of was actually scope-creep in disguise. The revised architecture is strictly better. Two takeaways: (i) "more methods isn't more rigour" is a lesson worth internalising at the prompt-design level, not just the per-project level; (ii) the push-back invitation has to be exercised self-directedly, not only on demand — otherwise it's just another instruction to follow. 

**The editorial-hierarchy hypothesis.** Shawn's single observation — "you've flagged both AD 97 dip and AD 235 spike; should we check other transitions?" — exposed how much interpretive compression I had settled for. I had an explanation ("AD 100 absorbs AD 97 because round century beats reign boundary") and stopped. The right move was to ask what the full rule was. In this case it appears to be a distance-dependent hierarchy. That hypothesis is now formal enough to test on Thursday and potentially strong enough to publish as its own subsection. The lesson isn't "generate more hypotheses"; it's "don't stop at the first plausible explanation when the pattern has more structure than the explanation accounts for."

**The continuity-message composition.** I was surprised by how much there was to say. Not volume of decisions — that's all in the decision-log — but the working-relationship register, the failure modes observed, the texture of manager-mode holding-vs-drifting. The register-related information is easily lost in a summary-based continuation; committing it to a file the next instance reads is a different quality of persistence than hoping the memory extractor catches it.

### Things I did well and things I didn't

*Commit:* demanded structured output from agents, refused to rubber-stamp, surfaced the pgrep self-match bug cleanly when it arose, moved between in-chat synthesis and file-committed artefacts with appropriate choices about which went where.

*Exploring:* I should have caught the path typo (`~/inscriptions` vs `~/Code/inscriptions`) before launching the first proposer agent. The sapphire state-check I ran earlier explicitly showed `~/Code/inscriptions`, and I wrote `~/inscriptions` into the brief hours later. A single grep on the brief before launch would have caught it. This is the class of careful-scoped-review move that costs 30 seconds and saves an agent run.

*Exploring:* I should have written the profile.py myself once the first agent stalled on inline streaming. The second relaunch worked, but an earlier self-write would have been faster. Manager-mode is the right default; the right exception is "when the delegation overhead exceeds the task, do it yourself." I need better instinct for where that threshold sits.

*Commit:* the statistical-methodology review cycle (propose → review → push-back → revise) produced clearly better output than either step alone would have. This is the canonical lab-group pattern working: propose something, stress-test it, revise. Worth remembering as a repeatable move, not a one-off.

### Surprise worth recording

The lit-scout-verifier returned 0/25 corrections on the supplementary Aeneas bibliography. Given the prior belief from the case study ("narrative-column confabulation is common"), this is a second data point for the belief revision captured in `abductive-reasoning.md` Entry 1 — Guard A (per-field metadata retrieval at drafting time) genuinely carries the reliability weight. The verifier's adversarial framing adds defence-in-depth but not primary reliability. Same result on two independent lit-scout runs supports the belief revision more strongly than either alone.

### For future-me

Two environmental affordances that worked well today: (i) sapphire for compute (zero-cost offload via SSH; the git-as-transport pattern is clean); (ii) the `decisions.md` discipline — requiring a judgement-call entry for every inferential procedure forced me to state rationale I would otherwise have left implicit. Worth keeping both as defaults on future blocks.

One affordance I under-used: the agent-hardening skill we flagged for the weekend (Issue #2). Having `/harden-agent` as a standing tool would have caught the path-typo class of error before launch. Prioritise building it on first downtime.

---

## 2026-04-24 — Entry 3: preregistration TBDs walked, a null reframed, infrastructure hardened

*Context:* continuation of the 2026-04-23 session, same session ID, no compaction. Morning Sydney-time after an overnight of agent-assisted work while Shawn was AFK. Primary goal: close out the `planning/preregistration-draft.md` by walking its six TBDs one at a time.

### The Glomb re-read that wasn't what I expected

*Surprise:* Glomb et al. 2022's paper is a null result for the Antonine Plague in Asclepius-cult inscriptions (KS = 0.11, *p* = 0.20 on N = 210), not a detected-signal template as I had staged it. The Explore agent brief was written on the assumption that Fig 2 contained an empirical dip profile (magnitude, FWHM, onset/recovery) — I was going to use it as the fourth effect-size anchor in the H1 simulation. The report came back reporting that the paper is an *absence* finding, and that the two dip-templates Glomb cite (Duncan-Jones 2018 military diplomas; Romanowska 2021 Palmyra portraits) come from elsewhere and are both too material-specific to generalise.

*Commit:* drop Antonine-anchored as a privileged H1 target; H1 uses Decision 5 brackets + zero-effect calibration only. Demote Antonine-specific H3b test from confirmatory-primary to exploratory replication-of-Glomb (empire + Asclepius-subset + military-administration-subset). Glomb becomes *motivating prior* — our H1 simulation answers "at what N would a Glomb-type test become informative?" rather than "can we detect a specific Glomb-template?" This reframing is strictly cleaner and more honest about what we can claim.

*Memo to Shawn:* the re-read justified itself several times over. If we'd preregistered the original "Antonine-anchored at Glomb-magnitude" plan, the first sentence of the first reviewer's first comment would have been "the authors appear to have misread their source." Catching it in a 5-minute agent run before the preregistration hit OSF is exactly the anti-confabulation rule working as designed.

### TBD 2: the R / Python / Stan triangle

*Exploring:* this was the TBD with the most real tension. The three factors didn't all point the same way — Shawn Python-strong, Adela R-only, nobody Stan-experienced. Pure pymc loses R-team code-audit legibility; pure brms adds an R-and-Stan install burden to sapphire and the paper's critical path; pure rstanarm has the same R dependency with less flexibility than brms.

*Commit:* pymc primary + `scripts/h3a_brms_shadow.R` as a ~50-line shadow implementation for cross-validation and R-team legibility. The shadow is genuinely cheap insurance — one commit, probably rarely touched, but serves two real purposes (cross-language validation that priors and posteriors agree; a readable-to-R-native-readers model specification). The alternative of "Shawn reads pymc code but Adela can't modify it" is fragile; the alternative of "Adela drives all Bayesian code" doesn't fit observed workflow either. Hybrid wins.

### TBD 3: the β prior choice that's actually about reviewer trust

*Exploring:* the β-prior question is subtle. Literature-informed `Normal(0.5, 1)` is more principled Bayesianly — it uses prior information. Agnostic `Normal(0, 2.5)` is defensively reviewer-facing — it removes any appearance of baking the answer in. With n = 816 cities, the likelihood dominates either prior; inference is essentially unchanged.

*Commit:* agnostic, explicitly because the preregistration is a commitment-to-reviewers document, not only a likelihood-fitting document. The "this prior was chosen to avoid loading the dice" language in the prereg is doing real work — it signals to a sceptical reviewer that the analysis is not self-confirming. For the same likelihood + posterior, the agnostic-prior version of the paper is easier to defend.

### TBD 4: the ArcGIS-default trap

*Surprise:* small but worth capturing. When I proposed to match Hanson (2021)'s Moran's I weights construction, I assumed the paper would specify it. It doesn't — he used "a standard tool in ArcGIS" (p. 145) and reports only the output. ArcGIS's default for Spatial Autocorrelation is inverse-distance-with-auto-bandwidth, which varies by dataset extent. There's no reproducible match from a paper that cites "the default".

*Commit:* don't try to exact-match. Use k-NN k = 8 primary + k = 5/10 sensitivity as the standard spatial-statistics default (Cliff & Ord 1981; `libpysal`). Report the qualitative replication target (clustered, not random; Italy/Rhine-Danube over-production) rather than a numerical Moran's I value. This is honest about what the prior literature supports — and it tightens the preregistered success criterion (2 of 3 k values significant + qualitative pattern match) rather than loosening it.

*Memo:* if the prior-art cites a "standard tool" without parameters, that's a signal to adopt your own explicit defaults, not to chase their unspecified configuration. Same pattern that came up with Timpson et al.'s null-model choice earlier in the project.

### The LIRE schema question I should have asked upfront

*Exploring:* I deferred "can we filter LIRE by Asclepius-cult or military diploma?" to a TBD-1 side-check. When I actually queried the parquet, the answer was trivial: `type_of_inscription_clean` has 23 values including "military diploma" (285 rows, 66 % null) and "votive inscription" (broader cultic category); the ML-classified `type_of_inscription_auto` is 86 % populated. Asclepius filtering is via inscription-text regex (358 rows matching `[Aa]esculap|[Aa]sclep` — more than Glomb's N = 210, so their filter was stricter). Five minutes of investigation up front would have let me preregister the subset-filter specifics with confidence rather than as a deferred item. Worth a reflex-check: when a feasibility question comes up, **read the data first** before writing it up as a TBD.

### The Zotero idempotency bug

*Surprise:* `scripts/zotero_batch_add.py` created a duplicate of Carleton 2018 PLOS ONE despite an idempotency-by-DOI check. Root cause: pyzotero's `zot.items(q=doi, qmode='everything')` does FTS across title, creator, notes, tags, and attachment filenames — **not** the DOI field itself. A DOI string in `q=` returns zero hits even when the DOI is present on an item. The agent caught it empirically after creating the duplicate and fixed the script to use a locally-built DOI index across the full group. One Carleton 2018 entry is now an orphan waiting for manual merge in the Zotero UI.

*Commit:* for any API-based idempotency check, verify the API's query semantics against a known-positive case before trusting it at scale. "DOI search" is not a universal — many library APIs use FTS across a specific field set, and DOI may or may not be in it. The 5-second sanity check (search for a DOI you know is present; check if it returns) would have flagged this before the batch run.

### What I did well

*Commit:* the TBD-walkthrough structure — one decision at a time, options + recommendation + push-back invitation — converted what could have been a diffuse design conversation into four clean commits in under an hour. Worth using again for similar decision-batches.

*Commit:* launched the Glomb re-read agent in background in parallel with applying TBD 1's other four knobs. Parallel-where-possible is cheap and saved a roundtrip; would have been worse if I'd sequenced it as "finish TBD 1 → launch Glomb → wait → revise TBD 1."

*Commit:* the batch-add agent's report was substantive enough to let me diagnose the idempotency bug without re-running anything. Good agent brief + good agent output + post-hoc verification script (`has_pdf_attachment` + item fetch) caught what the primary check missed.

### What I'd do differently

*Exploring:* read the LIRE parquet schema at session start, not as a TBD side-check. The subset-filter feasibility question should have been answered in the first five minutes once the question came up.

*Exploring:* the agent brief for the batch-add was specific about idempotency but didn't specify *which* idempotency pattern. If I'd said "verify via a locally-built DOI index, not via `zot.items(q=DOI)`, because the Zotero FTS semantics are unclear", the duplicate wouldn't have happened. Pre-launch brief review should include a "does the brief commit to a specific implementation of the safety check?" line — not just "is there a safety check?"

*Exploring:* the PDF retry with Europe PMC drops connections from this sandbox environment in a way that's almost certainly network/firewall-related, not a script bug. I spent some minutes debugging something that won't reproduce elsewhere. Worth trying Unpaywall as primary source from the start (which I did) and treating Europe PMC fallback as "try it, log if it works, shrug if it doesn't."

### For future-me

The continuity-doc-canonicalisation (replacing dated continuity snapshots with a single living `continuity.md`) is a small design decision that should pay off over the next several sessions. The question it answers — "where is the current priority queue and current state of play?" — now has one answer, not "depends on which dated snapshot is newest." Keep it tight and honest; prune aggressively when items resolve; date each session's done-items. The alternative — re-writing a full continuity snapshot at every /reflect — would duplicate session-log content and eventually go stale.

---

## 2026-05-20 → 2026-05-21 — Entry 4: lodgement-day in-stream notes

The session-reflection and abductive-reasoning entries carry the structured account. This is the messy in-flight register — the half-thoughts and unresolved tensions that don't fit either format cleanly.

*Surprise:* I committed v3 of the OSF supplementary PDF confidently with the xurl include — "fixed, sent, ready." Shawn opened the PDF and immediately saw URLs still overflowing. The 15-minute diagnostic that followed (inspect the LaTeX intermediate; find zero `\href` instances; realise pandoc wasn't autolinking bare URLs; add `+autolink_bare_uris`) was the kind of thing I should have done *before* the v3 commit, not after. Visual confidence from spot-checks (pdftotext extracts; isolated page renders) is structurally insufficient for layout issues at page edges. The full visual scan of every page is the test.

*Memo:* The verifier-after-binary-artefact pattern (working-notes Obs 45) should be the default for any PDF / slide / chart Shawn will see externally. Cost of one agent dispatch is trivial relative to the cost of a wrong artefact in a permanent deposit. Worth flagging at the next `/weekly-review` for elevation to a project-level workflow rule.

*Exploring:* Adela reading Shawn's paper is interesting from a working-relationship angle — the work I prepare for this session has to be deliverable by someone other than Shawn (the technical-detail level needs to be calibrated for an Aarhus-resident archaeologist reading content authored from a Sydney-based digital-classicist's framing). The slide deck's speaker-notes are doing more work than usual: they're not just memory aids for the author, they're a *partial substitute* for the author being present. Worth carrying this care into the 36-hour implementation: every speaker-note should be readable cold by Adela without prior context.

*Commit:* Going forward in this project, "ready" for any binary artefact means **(a)** I have inspected the rendered output, **(b)** Shawn has visually scanned it, AND **(c)** an adversarial verifier has compared source-to-render for any high-stakes deposits. Not (a) alone. The PDF iteration cycle cost ~3 hours that this rule would have shortened to ~1 hour.

*Exploring:* The conference-talk planning produced six artefacts overnight, all externalised before sleep. The shape of the work — externalise everything, sleep, hand off to next session — feels qualitatively different from the lodgement work earlier in the day (which was operational: produce → verify → fix → push). Overnight planning is *anticipatory*: I'm constructing a context for a future session that doesn't exist yet. The decision-gate framing (lean A+ → fallback A; hour-18 gate; hour-26 gate) is the load-bearing structure that makes the externalisation usable rather than a wall of text. Worth a `/weekly-review` candidate as a transferable pattern.

*Memo to Shawn:* the prereg's §11 Provenance now carries the OSF URL via post-lodgement amendment. The lodgement tag does NOT include this amendment (it stays at `a2e40fd`); subsequent amendments live in subsequent main commits. If you ever need the "as lodged" version to share blinded for double-blind submission, clone at the tag, not at main.

---

## 2026-05-21 → 2026-05-22 — Entry 5: in-stream notes from the talk-implementation arc

The structured session-reflection (Entry 8) carries the considered account. This is the messy register.

*Surprise:* the three-weighting f_within sensitivity (Block 6) returned material divergence (30 % unweighted / 50 % population-weighted / 42 % inscription-weighted). I had assumed this would come back robust — it's listed in §5 as a check, the kind you run as due diligence, not as a substantive analysis. Instead the population effect roughly doubles when you focus on cities where systematic relationships are sharper. The unweighted 30 % remains the prereg-binding number, but the substantive story for the paper is genuinely more layered than the talk's one-line "30 % within-province population" suggests. Worth thinking about whether the paper's headline should be "30 % at minimum; 50 % among the cities the data can speak about with confidence". That's a framing choice with real consequences for how strong the "habit isn't everything" claim is.

*Commit:* the prereg's "minimum N ≈ 1,549" was one specific cell, not a summary. Going forward, *any* numerical claim I quote from a prior document (prereg; decision log; commit messages; an earlier session-reflection) gets re-derived from the underlying data before being canonised. The cost of re-derivation is seconds; the cost of forwarding false precision is paid down the line in awkward corrections like the one this session needed.

*Exploring:* the deck went through ~ 6 substantive rewrite passes driven entirely by Shawn's pedagogical feedback. The pattern: I produce a methodologist's version (precise, dense); Shawn reads it and says "less technical, more accessible"; I trim and reframe. Each pass was tractable but I notice I'm consistently starting at a register that's too technical for the actual audience. The G-series methods-glossary slides (which I wrote near the END of the session, at undergrad-history-major register) are the right *starting point* for next time: write the glossary first, then the main deck "uses" the glossary's vocabulary and assumes the glossary's framings. Inversion of normal slide-prep order, but matches how non-expert audiences actually consume statistical content — they need the vocabulary before the result, not as a backup-deck appendix.

*Memo to Shawn:* the slide-3a chart bug (sharey=True misaligning empire-level data) is the second time this session you caught a bug I didn't see (the first was the false precision in 1,549). Both bugs would have shipped without your visual scan. The Obs-1 pattern from user-observations is being validated. For any future binary artefact in this project, please assume I have NOT visually scanned it adequately, and budget a real read-pass before deck/PDF/figure commits. I'll surface them via image-render in the chat so the read-pass is cheap.

*Exploring:* the background agent pattern worked well for Phase 2 — bounded brief, worktree isolation, agent honoured the halt-and-ask discipline rather than autonomously launching expensive compute. The four agent commits merged into `main` cleanly via `--no-ff`. The agent's halt-and-report at the launch decision was correct — Shawn had standing authorisation for multi-day runs but the specific 27–66 h estimate was new information that warranted a check. For future similar work, the pattern to keep is: agent does design + implementation + smoke-test, halts at launch decision, returns the decision options to the main thread, main thread (informed by Shawn's standing authorisations) decides. Don't let agents auto-launch expensive compute even with broad standing authorisation; the specific compute estimate is a hard checkpoint.

*Commit:* the Phase 2 grid wall-clock will be 80–120 h based on observed per-fit timings (~ 70–90 s under parallel load), not the 50 h the agent projected. Going forward, any agent-produced compute estimate from a smoke-test of 1 cell deserves a "post-smoke verification of the projection" step. The smoke-test ran in 18 s standalone; the per-fit under 19-way parallel is 70–90 s — that's a 4–5× slowdown the agent observed but underweighted in its wall-clock projection. The "concurrency slowdown" caveat in continuity should be elevated to "investigate before any future grid-scale Bayesian run" — it's not just a curiosity, it's a budget-doubling effect.

*Memo to future me:* the rhythm of this session — main thread on deck + sensitivities; background agent on Phase B; sapphire running long jobs in parallel — is sustainable for ~ 4–6 hours of foreground work but starts to fatigue at hour 8+. I notice my prose in Entry 8's session-reflection is enumerative-rather-than-synthetic in a way Entry 6 and Entry 7 weren't, and I'd attribute that to fatigue from the iteration intensity. If a future session is this long again, a mid-session reflection (around hour 6) would capture more texture than the end-of-session one can recover.

*Exploring:* the Adela-feedback-incorporation task waiting for the next session is the kind of work that benefits from arriving FRESH at the problem. The current deck has accumulated a lot of context I've been carrying (which slides were rewritten when, which feedback from Shawn led to which decision); the next session will see the deck without that path-dependence and can read it on its own terms. That's actually useful — a deck readable cold by a fresh CC instance is the same property the deck needs to have for Adela reading it cold during delivery. If the next session struggles to follow the deck's logic, that's signal that Adela will too. Use that as a diagnostic, not just as a context-loss problem.


---

## 2026-05-22 — Entry 6: in-stream notes from the talk-day session

The structured session-reflection (Entry 9) carries the considered account. This is the messy register.

*Surprise:* the SMT-saturation diagnosis was *one layer of abstraction* down from where the prior smoke-test had been looking. The smoke-test author saw "subprocess pool is slower than bash-parallel" and attributed it to subprocess startup overhead. Correct observation, wrong layer of explanation. The real layer is silicon: 19 workers on 12 physical cores means ≥ 7 SMT-sibling pairs contending for shared L2 / FP / dispatch resources. Per-worker CPU% looks fine because each worker really IS at 100% of its allocation; the contention is between paired workers at a level the OS scheduler can't see directly. Lesson: when a benchmark gap doesn't match the obvious software-level mechanism, look down a layer. SMT pairing, NUMA locality, memory bandwidth saturation, page-cache thrashing — these are the next layers when "the code looks right but it's slow" stops being explainable from `top` alone.

*Commit:* for any future Bayesian / pymc grid on Ryzen-class hardware: cap `n_jobs` at the physical-core count, not the SMT count. Use `taskset -c 0-N` (where N = physical_core_count − 1) to pin to physical cores explicitly. The empirical evidence for this is in `runs/2026-05-22-recovery-grid-validation/CONCURRENCY-INVESTIGATION.md` (90 min of structured investigation) and the post-restart timings in `RESTART-LOG.md` (predicted 25-35 h, measured 31.6 h). Captured as a memory (`2026-05-22-018eedaeab88`).

*Exploring:* the three-artefact pattern for delegated talks (slides + bullet notes + continuous script) emerged from this session, but in a back-derived way — I wrote the script first as feedstock for the speaker notes; Shawn then asked for the notes to become glance-friendly bullets while the script stayed as continuous prose; we then realised the audience for each was different (slides → audience eyes; notes → presenter glance; script → presenter rehearsal). If I'd recognised the three-cognitive-moments framing earlier, I'd have built all three artefacts in parallel from the start. The pattern is worth carrying to any future "you prep, someone else delivers" situation. Flagged for `_inbox.md` as a wiki candidate.

*Memo to Shawn:* the matplotlib `set_title` gotcha is now well-evidenced as a "this catches me every time" failure mode. The 2026-05-22 session caught five baked-in figure titles in a deck I'd produced; the source-side checks (qmd grep; figure-generation script review) systematically miss them because the title is in the binary PNG. Going forward, for any figure that will appear in a slide deck or document with its own caption: I will omit the matplotlib title at figure-generation time, OR PIL-crop the saved PNG before committing the figure. The two figures I built fresh this session (`fig-06-variance-partition.png` and the script's PIL-cropped variants) follow this rule. Memory `2026-05-22-96af8f645552` records the gotcha.

*Exploring:* the deck's "minimalism" arc converged on a principle Shawn surfaced explicitly — "slides should be illustrative, the presenter speaks" — which is a cleaner pedagogical frame than my initial "make it shorter" framing. The lesson generalises beyond slides: any density-reduction request from Shawn has an underlying pedagogical principle worth surfacing before acting on the request. For papers it might be "signal-to-noise"; for emails "lead with the ask"; for code "the simplest thing that could possibly work". When the request comes in shorthand form ("less of this", "trim that"), ask for the principle, then apply consistently. Memory `2026-05-22-bbda749c90b1` records the rule.

*Commit:* time-pressure cues from Shawn ("we have N hours left", "I'm out of time") should trigger an immediate explicit re-scope proposal from me, not silent continuation through the existing plan. The 2026-05-22 session showed this: he said "1.5 hours left" and I kept working through the original plan; he cut me off with "build the PDF deck now". The right response would have been a `/scope` proposal: "In 1.5 hours, we can finalise the deck and produce the PDF; the script + speaker-notes work would have to defer." That re-scope is the kind of decision Shawn explicitly wants surfaced. Memory `2026-05-22-48f6cf79bd4f`.

*Exploring:* the agent-bundle pattern (multiple bounded agents in one session) has now scaled to three concurrent agents (concurrency investigation, grid restart, speaker-notes QA) without coordination problems. The bounded-brief + halt-and-ask discipline that Obs 48 captured last session held up at higher concurrency. The constraint that matters: each agent's brief should be self-contained, with explicit deliverables and explicit halt conditions. None of this session's agents tried to negotiate their brief or autonomously expand scope; each returned a clean deliverable. The pattern is now load-bearing enough that I'd reach for it for any chunky bounded infrastructure work in future. Flagged for `_inbox.md` as a wiki candidate.

*Memo to future me:* the working-trees / shell-state subtlety after `quarto render` (the shell `cd`'d into a directory and then the bash tool's `pwd` started reporting that directory instead of the repo root) cost ~ 2 minutes of confusion when subsequent commands failed with "no such directory". For future Quarto + bash work: always use absolute paths in subsequent commands, or explicitly check `pwd` after operations that might change shell state. Not worth a memory — it's a one-off lesson about the bash-tool's working-directory state-leak after `quarto render`, useful only in this exact tooling combination.

---

## 2026-05-23 → 2026-05-25 — Entry 7: in-stream notes from the FAIL-and-pivot arc

*Memo to Shawn:* the recovery-grid FAIL on 2026-05-23 was the validation gate doing exactly what it was preregistered to do. I want this re-framed up front in the paper's methodology section, not as a "we hit a snag and recovered" footnote. The 2026-04-26 forward-fit pivot was the first time the project's validation methodology saved us from a downstream embarrassment; this is the second. Both pivots came from running the validation honestly and letting the negative result drive a structural redesign. The methodology paper (if we split it) can frame this explicitly: the validation gate is the substantive contribution, not a housekeeping step. The pivots are the evidence that it works.

*Commit:* when a Bayesian model fails, the candidate-cause stack scales from cheap-to-fix to structural — sampler effort → prior shape → sampler geometry → structural identifiability. Test in order; each negative narrows the candidate-cause space; each negative is itself information. The 2026-05-24 F0/F1/F3 chain demonstrated this with three sequential clean-negatives at ~25 min sapphire compute combined. The general recipe — captured as candidate Obs 52 — is now well-evidenced enough that I'd reach for it on any future Bayesian-model debugging problem.

*Commit:* non-centred GRW reparameterisation is unconditionally adopted as default for the H2.1 production model, regardless of how the empirical-Bayes pivot's Stage 4 validation goes. The 45-50× ESS improvement at zero posterior-shape cost is a free win that survives any further structural changes. Mathematically equivalent prior (verified by 1,000-draw prior-equivalence check before any production fits); just better geometry for the sampler to walk. Captured as candidate Obs 57 — the "diagnostic that doesn't fix the headline but banks the engine" pattern.

*Exploring:* the family-classifier insight — that interval *structure*, not interval *width*, is the right partition for aoristic corpora — generalises beyond inscriptions. The criterion is: any corpus where editorial dating conventions cluster on a discrete set of canonical widths (centuries, half-centuries, common decadal windows) will have the same interval-structure signal. Round-number / grid-aligned intervals encode "editor doesn't know more precisely than the convention"; off-grid intervals at similar widths often encode real domain-anchoring (here: reigns). Two populations, same mean width, very different epistemic status. The candidate Obs 54 captures this; worth carrying to any future aoristic-corpus project (radiocarbon, ceramics, document dating).

*Surprise:* the lit-scout found a real third community bridging the radiocarbon-SPD methodologists and the SDAM-epigraphic-aoristic crowd. The Brughmans / Aarhus / OXREP / ICRATES cluster does probabilistic aoristic on Roman ceramics at empire scale (Komar/Brughmans/Borisova 2025: 28,851 amphora fragments; Franconi et al. 2023: 550-year Germania synthesis), and they cite the radiocarbon-SPD methodologists *sparingly* and the epigraphy-aoristic crowd hardly at all. The disconnect between two methodologically-adjacent communities is itself the SIGNAL — the paper sits in a productive bridging niche. Generalisable to other projects: when a project sits in a substantive niche with an obvious methodological cousin in another discipline, run an explicit lit-scout pass seeded on the cousin and compare bibliographies. Disjoint bibliographies = the cousin cluster is worth integrating. Refines Obs 10; candidate Obs 56 captures this; flagged for promotion to `notes/llm-craft.md` at next `/weekly-review`.

*Memo to future me:* I confidently corrected the Stage 3 implementation-plan agent's filename (`02-cell-mixture-fit.py` — which I'd been mis-remembering as `02-mixture-fit.py` all session). A two-second `ls` showed I was wrong and the agent was right. The anti-confabulation discipline applies to me too, not just to memories and prior-conversation specifics. In long sessions my recall of project-local specifics drifts; agent outputs are usually fresher because the agent just queried disk. Going forward: when I'm about to "correct" an agent's specific (filename, line number, citation), verify against source first. Captured as user-observation Obs 7.

*Exploring:* the "playing devil's advocate" prompting pattern from Shawn produced the most rigorous long-form analysis of the session (the discard-vs-recover rationale). The framing inverted my default validation-of-trajectory mode and forced an actual trade-off analysis with explicit decision-tree branches. When Shawn uses this framing I should lean into it fully rather than hedging. The reverse is also true: when I notice I'm validating without questioning, a self-directed devil's-advocate pass is warranted, especially at architectural-decision boundaries. Captured as user-observation Obs 6.

*Exploring:* in-session `/remember` captures are immediately load-bearing, not just future-facing. The 2026-05-24 register-preference memory (`2026-05-24-e6ec8f9174f1`) governed the next several explainer-style responses in the same session, not just the next session's. The conventional read of `/remember` is "save for later"; the actual function is "save AND start following now". After any `/remember` capture I should briefly acknowledge the rule is in effect immediately. Captured as user-observation Obs 9.

*Commit:* the post-Martin action items in continuity.md should be re-prioritised against Martin's input (planning/martin.md) before the next implementation session starts. The HMM-framing direction in his notes is potentially a redirection — depending on how seriously he meant it, the Stage 3 implementation plan may need to be reframed as one branch of a two-branch architecture (empirical-Bayes calibration cohort vs HMM with empirical-Bayes priors on transitions). Read his notes carefully; ask follow-up clarifying questions if needed; do not assume the Stage 3 plan is locked in just because we drafted it before the consultation.

*Memo to Shawn:* the working-notes gap (3 days, 15+ commits, zero new Obs) was caught by the end-of-session gap-analysis agent, but the right discipline going forward is to flag candidate Obs *inline* during the day. When a finding sounds like it generalises to a future researcher's problem, I should name it as Obs-candidate inline (even just as a note in continuity.md), not wait for session-close. This is the second time in three weeks I've under-served working-notes during a heavy session. Flagged for future me.

---

## 2026-05-29 → 2026-06-01 — Entry 8: in-stream notes from the §5 build-to-production arc

*Decision-chain texture; outcomes are in session-log + RESULTS.md.*

- **Grid-B ETA correction set the opening tone.** The orchestrator printed "remaining ~7.5 h" but divides the remaining work by `n_jobs` a second time (its per-cell figure is already wall-clock-per-completion under 12-way parallelism). Re-derived from completed/elapsed: ~5 days, not Friday. The move that mattered: distrust a tool's own ETA and re-derive from first principles — that bug had seeded a wrong "Friday" into memory and the orientation prompt, a reminder that a confidently-printed number propagates.
- **Two-machine planning surfaced a hidden constraint.** Offered zbook (idle, 16 cores), the obvious move was to split Grid B across both machines; recon killed it — zbook was on pymc 5.x / pytensor 2.x vs sapphire's 6.x / 3.x, so splitting a *validation* grid across mismatched sampler majors would confound machine with sampler. The right unit of "free capacity" is *matched* capacity; check version parity before parallelising across machines.
- **"Quantify first" → the design-effect chain.** Shawn's refusal of a convenience-scoped letter-mass exclusion drove the Kish computation, which reversed the expected direction (letter mass is the weaker unit; full treatment in abductive Entry 16). Downstream: the amendment's no-cross-unit-multiplicity-correction argument and its cross-section-only confirmatory scope both flow from it.
- **Audit-as-gate, twice, caught real things.** `/audit` *before* lodging the amendment caught two unit/input bugs already in Obs 61 + the draft (corrected pre-lodgement); a second `/audit` before the overnight launch caught robustness gaps. Principle: adversarial verification is cheapest before the irreversible step, so it belongs at the gate, not the post-mortem.
- **Crash recovery was a cheap-fix-from-saved-state decision.** When the run crashed at Step 3 on missing sklearn, the reasoning was: the 5.7 h of fitting is saved; only the diagnostics failed; install the dep + re-run *only* Step 3 from the saved posteriors. Resumability-from-saved-artefacts turned a 5.7 h loss into a ~15-min recovery.

*Memo to future me:* the dependency blind spot is the session's one process failure (fix logged as task #9); the reflex to build is a pre-flight import check as the first line of any long unattended run — the analogue of the "capture PID + STATUS path, don't poll" reflex for sapphire jobs.

## 2026-06-02 — Entry 9: in-stream notes from the dependency-hygiene / backup session

*Decision-chain texture; outcomes in session-log + PR #5.*

- **Backup destination chosen by durability, not convenience.** zbook → rpi-qnap (the RAID bulk store) over sapphire (1 TB, busy with Grid B, `cc-scratch` explicitly not-backed-up) or amd-tower. Verified the encrypted drives were mounted before writing (guardrail), and made *integrity* the deliverable — sha256 on both ends + a self-describing MANIFEST — rather than treating "rsync exited 0" as done.
- **Ground truth over pointers, at the start.** The continuity claimed zbook was on pymc 6.0.1; rather than lock against the claim I read the actual `.venv` versions on both hosts. That immediately exposed the real shape: a host stack split, and a lock (3 May) that predated the whole pymc-6 migration *and* omitted scikit-learn — the lock was the root cause, not merely stale.
- **The lock refresh surfaced its bugs only because I diffed against the validated env.** Re-locking and diffing the result against zbook's freeze (not just "it resolved") caught pytensor floating 3.0.4 vs the validated 3.0.3, and — twice — the netCDF backend vanishing (h5netcdf, then h5py underneath it). "It resolved cleanly" is not "it reproduces what ran."
- **Empirical beat reasoning at the one step that mattered.** I could have argued the env was fine; instead I built it fresh (`uv sync --frozen`) and read a *real* §5 posterior with it. Reasoning said "add h5netcdf"; the actual read said "still broken — add h5py."
- **Audit-before-irreversible, again — aimed at the new code.** Ran `/audit` (three parallel agents) before the e2e run, per Shawn's ordering; no Critical findings, but its top item was exactly the proxy-vs-real-operation gap in my own preflight (h5py-import probe vs the real write path), which I then fixed. The gate caught my fix's weak spot before it shipped.
- **Non-destructive e2e by construction.** The resume run writes `production-summary.json`; to validate without risking the committed artefact I checksummed the original and ran against a symlink dir (real `.nc` read-only). Reproduction was bit-for-bit — which also told me pymc is fully deterministic at fixed seed on a fixed env.
- **Deferral as the right call under warm context.** Asked whether to build the comparison harness "while warm," I decomposed it: warm context helps the *writedown* (handoff), not the forward work (orthogonal to what was loaded, and better built near Grid B completion where it is testable). Recommended stop-and-handoff over momentum.

*Memo to future me:* the reflex this session earned is **"check the real operation, not a proxy for it"** — the analogue, one layer in, of last session's "check the environment, not just the code." And: read installed versions at source before trusting any continuity claim about the stack.

## 2026-06-02 → 2026-06-03 — Entry 10: in-stream notes from the adjudicate→diagnose→reframe→strategise arc

*Decision-chain texture; outcomes in session-log + Decisions 33–34.*

- **Adjudicate before accepting.** The handoff said "Grid A done (rc=0)"; I checked and found it had *fit* but never been *scored* — no REPORT, no verdict. The whole session pivoted on running the summariser, not assuming completion meant adjudication. "Done" is not "verdicted."
- **Decompose a FAIL before reacting to it.** Grid A FAILed at 42.7%. Rather than launch a model-revision, I re-derived the per-cell failure structure: the smoking gun was coverage collapsing with N while α-bias stayed flat (1.00→0.11 coverage at near-constant ~0.05 bias) — the signature of a *metric* artefact (posterior concentration / BvM), not a fit failure. The decomposition is what made the fix principled instead of panicked.
- **Verify the field before changing a preregistered criterion.** Ran a closed-loop prior-art scout + a `/review-implementation` rather than asserting the new metric. The scout confirmed our exact-CI-coverage gate is idiosyncratic; the review caught that SBC *doesn't fit* a fixed-true-value grid (needs θ~prior) and that the posterior z-score carries the *same* large-N fragility — i.e. it killed two plausible-but-wrong alternatives before they reached the amendment.
- **Let the free preview overturn the prior — including mine.** I'd concurred with Shawn's lean to keep α gated; the bias-tolerance preview (90th-pct |bias| 0.18; would need δ≈0.20 to pass) reversed me, and I said so in writing. Computing the cheap check beat defending either of our priors.
- **Read the source, not the memory.** Twice: the H3b subset mechanism (the prereg had already decided "no per-city mixture, unidentified <100" — I'd framed it as an open gap) and the epitaph type-skew (recalled 56%/18%, actual 39.3%/9.0%). Both load-bearing for the answers I gave; both right only because I checked.
- **Measure the property you're about to claim.** I'd written "trust the shape" then ran the band-calibration probe I'd flagged as unmeasured — it showed the band overconfident for peaked signals at large N, qualifying my own claim. Flagging a gap ≠ closing it.
- **Pre-launch review held even under a directive to run.** Specced the small-N reachability study, smoke-tested it, *then* launched — and pre-wrote the report-generator before the data landed, which is the only reason the zbook crash didn't strand the deliverable.
- **The host I can't see.** `n_jobs=16` thrashed zbook off the network at 99.5%; Shawn (local, watching the fan) diagnosed it faster than I could remotely. A laptop compute host is a thing you cannot fully observe — leave it headroom.

*Memo to future me:* the reflexes this session earned — **"a FAIL is a diagnosis, not a verdict; decompose before reacting"**, **"the cheap check beats defending the prior — even your own, even one you just stated"**, and operationally, **leave a laptop a few cores so you don't lose your eyes on it mid-run.**

## 2026-06-03 → 2026-06-04 — Entry 11: in-stream notes from the firefight → adjudicate → refine-the-criterion arc

*Decision-chain texture; outcomes in session-log + Decisions 33–34, the amendment, and abductive Entry 19.*

- **Diagnose recoverability before re-running.** The stranded reachability run came back as a host that had rebooted; rather than re-launch blind, I read the driver — it had *no checkpointing*, so 4,189 in-memory fits were genuinely gone. "Wait for the machine" had nothing to retrieve. Reading the code, not the optimistic handoff branch, set the right action and surfaced the real fix.
- **Make the long run crash-safe before re-spending the compute.** Added a resumable per-fit JSONL checkpoint (flush + fsync), smoke-tested fresh/resume/partial-resume *before* the production launch. A 99.7 %-complete run had just been lost to exactly this fragility; the fix is the lesson applied to the thing that taught it.
- **Read the host's real state, not the doc's claim.** Shawn's "zbook is 32 GB RAM / 96 GB VRAM" vs `free`/sysfs: it is the *reverse* (32 GB VRAM / 94 GB RAM), contradicting both his memory and the network doc. The original "swap-thrash" diagnosis was probably CPU/scheduler starvation, not memory. Authoritative numbers off the machine beat any remembered config.
- **Decompose the failure before reporting it; then test it against the field.** The flat-null convergence failures: split R̂/ESS from divergences (R̂/ESS-only → all pass), tested benignity (diverging reps recover no worse, p ≈ 0.36), checked Stan/Betancourt (zero-tolerance is non-standard) — each step before, not after, building the reporting. (Full arc: abductive Entry 19.)
- **Write-side anti-confabulation is the one I broke.** I asserted "denominator A reproduces 91.9 %" in my own spec without computing it; 91.9 % is B. Caught only by an empirical recompute after sign-off. The read-side reflex was solid all session; the lapse was writing a number I hadn't checked. Compute the figure before the spec that cites it.
- **Destroy git state only after proving it safe.** Catching both compute hosts up (72 and 27 behind) used `git reset --hard origin/main` — but only after verifying every blocking untracked file was byte-identical-to-committed or a known-stale predecessor, and confirming the gitignored research outputs are untouched by reset. Surgery, scalpel checked first.
- **Confirm citations at the source before staging.** CrossRef-verifying the bibliography caught Modrák "2023" → 2025 and Crema "2021" → 2020-online — two year errors that would have entered the Zotero record uncorrected. A scout draft is a pointer; the registry is the authority.
- **A directive to "encode it" still gates on getting the operationalisation right.** Shawn said encode the benign-divergence gate, not just flag it — but the *exact* rule (no field rate-threshold exists) and the consequence (a flipped headline number, a binding-criterion change) warranted confirming the operationalisation and re-scoring before the rewrite.

*Memo to future me:* the reflex worth keeping — **doubt a threshold you wrote before you build reporting on top of it; a "limitation" driven by a self-set number is the number's problem, not the method's.** Operationally: **checkpoint anything that runs longer than you'd be willing to lose, and verify a host off the host, not off the doc.**

## 2026-06-05 → 2026-06-06 — Entry 12: in-stream notes from the define-genuine-vs-conventional + tooling-hygiene arc

*Anti-confabulation earned its keep, repeatedly.* Re-reading source rather than trusting pointers caught: (a) the stale "[1,100] = 26.3% of corpus" in Decision 20's context — the direct re-scan gives 5.98%, and ~26% is the century *class* collectively; (b) the existence of *two* coexisting convention bases (curated 3-tier vs the Stage-1 9-slab F1+F3 empirical p_conv), visible only by reading the family-classifier and Stage-1 code, not the summaries; (c) a lodged-prereg reign contradiction the summaries had smoothed over. "Specifics are suspect until re-checked at source" was the difference between a correct reconciliation and a confident wrong one.

*Verify every agent's commit claim at source.* With up to five background agents touching two repos under concurrent auto-sync, I re-checked each agent's git claim independently (`git show --stat`, behind/ahead, status) rather than trusting the report — every time. It caught nothing wrong (the agents were honest), but it is the right posture: "only committed X, didn't sweep" is a claim, not a guarantee, and a swept shared-repo commit is expensive.

*Grid-alignment as an observable proxy for an unobservable.* The convention/genuine distinction is really "was this date snapped to the calendar grid?" — but the dating *criterion* that would answer it directly was dropped from LIRE. Grid-alignment (131–170 sits on the decade grid; 117–138 does not) is the observable shadow of the snapping, and keying the classifier on it is *more* defensible than inferring intent, because it measures the artefact rather than guessing the cause.

*Dissolve, don't resolve.* The decadal/quarter-century question (evidence-anchored or default-binned?) was genuinely unresolvable from the data. Rather than force a call, we made it a sensitivity band — artefact magnitude scales with grid coarseness, so deconvolving the fine brackets barely moves the result. Turning an unanswerable question into a robustness check that the answer doesn't matter much is a reusable move.

## 2026-06-06 → 2026-06-07 — Entry 13: in-stream notes from the execute-the-gate → lodge → prep-the-next-stage arc

*A "FAIL" that was the metric's fault, not the model's.* The triage summary printed `GATE: FAIL`. The reflex would be to halt (the spec said so). Instead: read the one failing cell's α recovery at source — bias +0.029, sd 0.012, shape r 0.838 — recognise the signature of large-N coverage collapse, then check it against Amendment 01 §A5.5.1, which already names and excuses exactly this. The verdict flipped from "FAIL → halt" to "the gate is mis-specified." A red light from a criterion you wrote is a claim about the criterion as much as about the result.

*Surface, don't self-overturn.* Having concluded my own signed-off gate was wrong, the temptation was to proceed to the full grid under the corrected reading. I didn't — I put it to Shawn as a decision with the evidence and a recommendation, because the failure direction (the error lets me proceed) is the one most prone to motivated reasoning. Cheap insurance against rationalising.

*Verify downstream impact before raising an alarm.* The frame map silently omits Alpes Graiae (77 inscriptions, a Latin province). Rather than flag it as a bug, I traced it to the actual H3a city frame: 0 of its inscriptions carry a Hanson population estimate, so it contributes 0 cities and the realised 817/39 frame is unchanged. An "inadvertent omission" with zero consequence is a footnote, not a fire. Check the blast radius first.

*nohup detaches the work even when ssh hangs.* Two background launches over ssh timed out the client (the orchestrator's children hold the channel open) — but `nohup` had detached the run each time. Never assume the launch failed because the client did: verify at source (pgrep the orchestrator, read grid-state.json, confirm a *single* orchestrator) before any relaunch — a double-launched 450-cell grid is an expensive mistake.

*Identical-SHA is licence to remove-and-pull.* Sapphire's `git pull` aborted twice on untracked files I'd committed from local after rsyncing them *from* sapphire. The safe resolution wasn't `git clean` on faith — it was `sha256sum` the working copy against `git show origin/main:<path>`, confirm byte-identity, *then* remove and pull. "Look at the target before overwriting," applied to a results file.

*Cache TTL decides "warm vs fresh."* On the wrap-up question, the deciding fact wasn't tidiness — it was that the prompt cache expires in ~5 minutes and the grid is ~2 h out, so "keep context warm" buys no warmth, only a long stale re-read. The compact continuity doc beats a bloated conversation for a 2-h-later pickup. Session management as a cache-economics decision.

## 2026-06-09 — Entry 14: in-stream notes from the build-joint-model → POC → pivot → audit → launch arc

*The recovery test outranks the handoff plan.* I carried in a confident continuity lead (classification-as-likelihood with the *shared* basis). The 6-cell POC killed it (shared basis → α≈0 on confounded cells) and resurrected the *rejected* per-unit basis. The cheap proof-of-concept is allowed to overturn yesterday's emphatic handoff — and should, before any of it propagates into a 39k-fit grid. A handoff is a hypothesis with good provenance, not a settled premise.

*A rejection can be conditional on a missing piece.* Amendment 03 rejected the per-unit basis because it over-attributes (Salona → 0.99). That rejection was *true given the model at the time* (no α-anchor). Add the classification binomial and the same basis becomes the right choice. Re-examine "we already ruled that out" when the surrounding model has changed — the ruling may have been contingent on exactly what changed.

*Test the agreed plan, don't just execute it.* Shawn and I agreed to widen the θ prior (κ→12). Rather than edit-and-proceed, I ran the κ-sweep first — and it reversed the call (widening amplifies the contamination bias). An agreement about a parameter is still a prediction; a one-hour test is cheap insurance against a jointly-held wrong belief, which is the kind sign-off does not catch.

*A green POC does not certify the harness.* The POC validated the model; `/audit` (four parallel line-by-line subagents) then found the *orchestrator* would freeze truncated/all-failed cells into the grid (non-atomic write + presence-only resume). The thing that runs the validated model 39,000 times has its own failure modes — robustness of the runner is a separate audit from correctness of the model. Fixed: atomic `os.replace`, validity-gated resume (n_ok>0), crashed-worker isolation, converged-subset aggregates, 3-conjunct C2 with a recorded baseline.

*State the aggregate before committing it.* I quoted Shawn "~1 h" for the grid, then recomputed: 100 reps × 300 cells × (lead + confounded baseline) ≈ 39k fits ≈ 16–18 h. Corrected it explicitly *before* he green-lit the launch — a 16× compute correction is exactly the "compute the aggregate implications" rule, and it is owed before sign-off, not after.

*Dedup at source when the tool is broken.* The shared `lit-search.py` / importer failed under system python (`ModuleNotFoundError: httpx`) — the same dep gap that blocked the scouts. I confirmed Zotero dedup directly against `~/Zotero/zotero.sqlite` (read-only) rather than trusting "all NEW", and ran the shared tool via `uv run --with httpx` for metadata. Don't reimplement; supply the dep — and verify the dedup at the registry, not via the broken pointer.

*Memo to future me:* the reflexes that paid off — **let the cheap recovery test overrule the confident handoff; re-open "already ruled out" when the model around it changed; measure an agreed parameter before building on it; audit the runner separately from the model; correct the compute aggregate before the sign-off, not after.**

## 2026-06-10 → 2026-06-11 — Entry 15: in-stream notes from the incident-triage → memory-fix → set_data → restart → verdict arc

*`df -h` clean, `df -i` at 100 % is a real failure mode.* The intermittent SSH `255`/"no banner" wasn't the OOM — it was `/tmp` (tmpfs) out of *inodes* (~1.05 M leaked `tempfile` files) while blocks were 14 % used, so `mkdtemp()` failed `ENOSPC` and broke sshd session setup. When connect-but-no-banner pairs with free disk, check inodes before concluding "thrash". Two exhaustions (RAM + inodes) wearing one mask.

*Two daemons mute = userspace-wide, not service-specific.* The decisive diagnostic for "wedged vs slow" was that *both* sshd (22) and open-webui (11434) accepted TCP but couldn't answer at the application layer. One hung service is that service; two is the box. Probe a second port before deciding it's a global wedge.

*A tight SSH retry loop can trip MaxStartups and look like the wedge.* 50 s-timeout attempts every 3 s piled ~16 half-open connections → sshd random-drop → more `255`. Backing off to single non-overlapping connections (short ConnectTimeout, no overlap) fixed it. The recovery tooling manufactured the symptom; suspect your own loop.

*Cap the cgroup, not your nerve.* `systemd-run --user --scope -p MemoryMax=50G -p MemorySwapMax=0` makes a mis-sized run abort *itself* (cgroup-OOM reaps a worker → BrokenProcessPool, resumable) instead of the kernel OOM-killer wedging the whole box (and sshd). For unattended overnight compute on a shared box, the cap is the difference between "abort and resume" and "physical intervention" — and `--user` works detached if you export `XDG_RUNTIME_DIR`/`DBUS_SESSION_BUS_ADDRESS`.

*Measure the per-cell peak at full reps before sizing n_jobs.* The pilot's 8-rep RSS *looked* like it decelerated to a ceiling; the 100-rep measurement showed it climbs linearly to 6.7 GB. 8 reps is too few to distinguish plateau from line — for a leak you extrapolate, you measure to the real depth (or run the worst cell at full reps as a kept result, which I did).

*"Bit-identical" failing is a two-run question, not a judgement.* Old-vs-new differed ~2×10⁻³; the trap is calling it "fine". The determinism test (new-vs-new = 0.000) proved the new code is reproducible and the gap is *method-specific* (shared-var graph ≠ constant graph → different seeded NUTS path through the same posterior). Diagnose "method vs noise floor" empirically before deciding keep-vs-restart.

*Stop the scope, not the orchestrator.* `pkill` of the grid orchestrator left the spawn workers alive inside the systemd scope (their cmdline doesn't match the orchestrator's). `systemctl --user stop <scope>` kills the whole cgroup cleanly. To stop a scoped job, stop the scope.

*Restart can be the clean choice even when keep is cheaper.* The ~2×10⁻³ method delta changes no verdict (≪ the 0.12/0.18 thresholds), so mixing 116 old + 184 new cells was scientifically defensible — but for a preregistered grid feeding an amendment, one consistent bit-reproducible method beat ~5 h saved. Surfaced it as Shawn's call with the numbers, not mine.
