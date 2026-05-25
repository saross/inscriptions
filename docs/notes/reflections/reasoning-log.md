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
