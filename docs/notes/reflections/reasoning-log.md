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
