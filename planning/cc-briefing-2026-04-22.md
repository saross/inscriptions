# Claude Code Briefing — Inscriptions SPA Rebuild

**Date:** 2026-04-22
**Author:** Shawn Ross (with drafting assistance from CC on personal-assistant repo)
**Intended reader:** a fresh Claude Code session launched in `~/Code/inscriptions/`
**Status:** working brief — expected to be revised in the first session

---

## 1. Purpose of this document

This is a context-transfer and intent document for a new CC session. It is
**not** a task list to execute top-to-bottom. It exists because Shawn is
deliberately shifting his working mode with CC from "in-the-trenches
co-worker" to "manager" — specifying, delegating, and orchestrating rather
than pair-programming one step at a time. Read the whole brief before
proposing a plan; then propose the plan.

The prior LIRE-based notebook has been archived at
`archive/2026-04-22-inscriptions-spa.ipynb` along with its data and error
CSVs. Root infrastructure (`environment.yml`, `requirements.txt`,
`runtime.txt`, `.envrc`, `LICENSE`, `.gitignore`) has been retained but
may need updating.

---

## 2. Concrete deliverable and deadline

**By Saturday 2026-04-25**, produce:

1. A **feasibility assessment** for the statistical programme in §5 below —
   can the analyses actually be done on LIST with current tools, and if so
   how; if not, what the blockers are.
2. A **skeleton for a 20-minute conference paper** (May 2026, venue TBC) —
   outline, figure stubs, estimated analyses, and a clear statement of
   what the paper argues.

The audience for the Saturday deliverable is **Adela Sobotkova**, co-author,
who is physically in Canberra through Sunday 2026-04-26 and thereafter
available by email. The Saturday output should be sufficient to convince
her that the paper is viable for the May conference.

---

## 3. Upskilling frame (equally important as the deliverable)

This project is a **test case for agentic and managerial workflows**, not
just a paper. Design the session around the following learning goals:

- **Specification over narration.** Prefer writing briefing documents,
  specs, and prompts that delegate work to agents, over stepping CC
  through code one edit at a time.
- **Agent orchestration.** Use specialist agents where appropriate:
  - `lit-scout` for prior-art searches (already used for this project —
    found Hermankova/Voitek code repos, not yet in Zotero).
  - `prior-art-scout` for finding existing implementations of statistical
    methods and filtering pipelines.
  - `Explore` for codebase reconnaissance.
  - `Plan` for designing implementation strategies before writing code.
  - General-purpose agents for bounded research tasks.
- **Modes:** foreground, background, headless. Scheduled agents are not
  yet tried and may be appropriate here (e.g., a nightly lit-scout
  pass on new citations).
- **Push the limits.** Shawn has a Max plan and wants to explore how far
  CC can be pushed for a research workflow. Cost is not the primary
  constraint; API call gating (§9) still applies.
- **Leverage personal-assistant infrastructure.** The memory system,
  Zotero integration, craft notebook (`~/personal-assistant/notes/`),
  and scratchpad are all available. Read `CLAUDE.md` (both user-global
  and personal-assistant project) to understand Shawn's working style
  before proposing how to work.

**The learning-target failure mode to avoid:** reverting to line-by-line
pair-programming because it feels more controlled. If you notice this
happening, name it.

### Shawn's starting skill level (do not re-teach the basics)

Shawn has already been through the **basic agents tutorial** in earlier
CC sessions (2026-04-16 / 2026-04-17). Assume he knows:

- What agents are, when to spawn them, foreground vs. background vs.
  headless modes.
- The built-in agent types (`lit-scout`, `prior-art-scout`, `Explore`,
  `Plan`, general-purpose) and their basic affordances.
- How to define a custom agent in `personal-assistant/agents/`.
- The proposer/verifier pattern and why adversarial verification beats
  same-context self-check.

The next escalation — and what this project is meant to build — is
**engineering for long-running, large, and complex tasks**: scheduling
routines, orchestrating multi-agent pipelines, capturing agent sessions
for publication, and specifying at a level high enough that the
main-thread CC never touches a line of analysis code itself. Do not
re-cover the basics; start above them.

### Required reading before proposing a plan

The following files in `~/personal-assistant/notes/` distil what Shawn
has already learned about LLM craft and agent orchestration. Read
them before §10's plan proposal — they are more current and more
specific than anything this brief restates.

- `notes/llm-craft.md` — rolling craft log. Especially the
  **2026-04-18 / 2026-04-19 entries** on agent orchestration:
  *Agent definitions are specifications, not personas*;
  *Orchestration patterns are a 2×2, not a menu*;
  *Subagents are context management, not just delegation*;
  *Trust-but-verify structural vs. narrative fields*;
  *Adversarial verifier beats same-context self-check*;
  *Primary-plus-verifier pattern for fact-heavy outputs*;
  *Prior-art search before building*;
  *Externalise deferred items or lose them*.
  Also **2026-04-21 / 2026-04-22** on planning capture:
  *Abstract todos complete by producing their descendants*;
  *Capture everything at plan time — "obvious" dies in three weeks*.
- `notes/lit-scout-case-study.md` — the multi-version refinement run
  from which the primary-plus-verifier architecture emerged. Worked
  example of iterating on an agent spec rather than on the analysis.

### Open-science dimension of the upskilling work

Shawn is a co-proposer of a Research Data Alliance working group on AI
disclosure and openness in research. **Agent session capture is an open
infrastructure task this project must tackle**, not just a nice-to-have.
By the end of this project there should be a defensible workflow for:

- Preserving the prompts, specs, and agent outputs that produced a given
  analytical result.
- Publishing those alongside the paper's code and data.
- Citing them properly.

This is one of the "one or two infrastructure issues" to schedule
alongside the analytical work.

---

## 4. Dataset

### LIST — Latin Inscriptions through Space and Time

- Published on Zenodo. **Set up the Zenodo API** as a first-session task
  so the dataset can be pulled reproducibly rather than manually
  downloaded. Confirm the canonical DOI/record ID before downloading.
- LIST is the **parent dataset** of the LIRE dataset used in the archived
  notebook. LIST provides **extended chronological coverage** beyond
  LIRE — this is the primary reason for the rewrite.
- The **LIRE Zenodo documentation** is reported to discuss known problems
  with LIST that LIRE was designed to address. Read it before filtering —
  those same issues apply here and must be handled explicitly.

### Filtering criteria (to apply to LIST)

All are necessary; most need refinement once the data is in hand:

- **Must have spatial coordinates** / be localised to an urban area.
- **Must have reasonably complete metadata.** Criterion to be operationalised
  after exploratory analysis.
- **Chronological cap:** likely AD 600 (to be confirmed).
- **Geographical cap:** within the Roman Empire (probably). Inspect what
  LIST contains outside the Empire before deciding.

### Prior art and code to locate

Petra Hermankova and Vojtěch ["Voitek"] \<surname TBC\> and team have
published GitHub code related to LIST, including:

- A **LIST filtering pipeline**.
- An **aoristic analysis / SPA implementation** (the old notebook rolled
  its own; the Hermankova/Voitek version should be evaluated and likely
  preferred).

`lit-scout` has surfaced these in a previous session but the outputs are
**not yet in Zotero**. **First-session tasks:** locate the repos, add the
relevant papers to Zotero, read the code, decide what to reuse.

---

## 5. Research programme

Same structural research questions as the archived notebook, but this
time the statistics must actually work. The previous attempt failed on
the minimum-count step (§5.3). Sequence:

### 5.1 Baseline descriptive statistics

Of the full filtered LIST dataset: counts, temporal distribution,
geographical distribution, metadata completeness profile.

### 5.2 Division and descriptive statistics by subunit

Partition by **province** and by **urban area**. Report descriptive
statistics for each.

### 5.3 Minimum-count determination (the crucial blocker from last time)

Rigorous determination of the **minimum inscription/letter count**
required for a meaningful SPA analysis at a given level:

- How many inscriptions/letters do we need at the **city** level to
  distinguish signal from noise?
- How many per **decade** to justify including that decade?

This step failed last time. **A prior-art assessment is required before
implementing.** Methods to investigate include but are not limited to:

- The summed-probability-distribution (SPD) methods literature on
  radiocarbon analogues — see Williams (2012) below.
- Permutation / bootstrap approaches.
- Null-model comparison (e.g., taphonomic or sampling null models from
  the SPD literature).

### 5.4 SPA across levels and subsets

Run SPA at **dataset, province, and urban area** levels, with
sub-analyses:

- Exclude Roma.
- Exclude Italy.
- Latin-speaking provinces only.
- Non-Latin-speaking provinces only.

And on **both** measures:

- Inscription count.
- Letter count. (One of the sources recommended this; citation
  currently lost — **follow up to identify and record it**.)

### 5.5 Demographic vs. cultural/economic/informational signal

Compare inscription/letter counts against the **population proxies
presented in Hanson (2021)** to decompose how much of the SPA signal is
demographic versus economic, cultural, "complexity", or informational.

### 5.6 Interpretation

Serious reflection — not an afterthought. What does a signal in the SPA
mean? Population? Wealth? Cultural proclivity towards inscription?
Social competition? An information-access proxy? What additional proxies
would operationalise each of these? Even a bounded outcome — "X% of
variation is plausibly population-driven" — is a useful foundation.
Pushing further is the ambition.

### Key citations (not yet in Zotero — add in first session)

- Hanson, J. W. 2021. "Cities, Information, and the Epigraphic Habit:
  Re-Evaluating the Links between the Numbers of Inscriptions and the
  Sizes of Sites." *Journal of Urban Archaeology* 4: 137–52.
  <https://doi.org/10.1484/J.JUA.5.126597>
- Williams, A. N. 2012. "The Use of Summed Radiocarbon Probability
  Distributions in Archaeology: A Review of Methods." *Journal of
  Archaeological Science* 39(3): 578–89.
  <https://doi.org/10.1016/j.jas.2011.07.014>

### Prior Shawn material on this project (read first)

- **Slides:** "SPA ANU Classics 2024-05-29" —
  <https://docs.google.com/presentation/d/1ORQI3f2Xx2xcRm-H7B8nfdQt8X7eQySo-6IDCaGqNwI/edit>
- **Seminar doc:** "2024-05-29 | ANU Classics seminar" —
  <https://docs.google.com/document/d/1UsyeWRTNfsXpUgWQHYJiRabMBklAK4eUaEXUfDg7jz8/edit>

Both were delivered at an ANU Classics seminar on 2024-05-29 and are
the most recent sustained articulation of the project's aims and
preliminary results.

---

## 6. Collaborators

### Adela Sobotkova — co-author, visiting

- **In Canberra until Sunday 2026-04-26.** Afterwards available by email.
- Member of the LIST/LIRE team; **geospatial specialist in archaeology**.
- Receives the Saturday deliverable (§2). Pitch it as: is this paper
  viable for the May conference?

### Petra Hermankova — principal LIST/LIRE author

- Seen in person at a conference later in 2026; available online before
  then.
- Source of the filtering pipeline and likely the aoristic/SPA code
  (§4).

### Vojtěch ["Voitek"] \<surname TBC\> — LIST/LIRE team

- Co-author of the code Shawn wants to reuse. **Identify full name and
  affiliations** during the prior-art pass in the first session.

---

## 7. Infrastructure tasks (schedule alongside the analysis)

In rough priority order:

1. **Zenodo API** — for reproducible dataset pulls (LIST, LIRE docs).
2. **Zotero integration** — this machine's Zotero is already wired into
   the personal-assistant commands (`/read`, `/cite-new`, `/synthesise`,
   `/gaps`). Add Hanson 2021, Williams 2012, and the
   Hermankova/Voitek papers as a first pass.
3. **Agent session capture** — see §3. The approach used should be
   defensible for publishing alongside the paper.
4. **Conda/pip environment** — `environment.yml` and `requirements.txt`
   are retained from the old project but will need updating once the
   statistical stack is decided.

---

## 8. Governance and working conventions

Adopt from day one:

- **Open science / FAIR / FAIR4RS throughout.** All code will be
  published — so it must be well-documented, reasonably hardened, and
  reproducible. Write as if a stranger will try to rerun it next year,
  because one will.
- **Archive, don't delete.** Stale files go to `archive/` with dated
  suffixes (see `archive/2023-09-08-inscriptions-spa.ipynb` and the
  2026-04-22 archive already in the repo). Exception: trivially
  recreatable intermediate artefacts.
- **Completion dates on to-dos.** Mark items `[x]` with the completion
  date; do not delete.
- **GitHub issues for anything that needs a durable record** — code
  bugs, project to-dos, open design questions. Casual in-session
  to-dos can live in CC's task tracker.
- **Commit granularity and style** per global `CLAUDE.md`: conventional
  commits, ≤50-char subject in imperative mood, body wraps at 72,
  `Co-Authored-By: Claude` trailer.
- **UK/Australian English** in all output, code comments, docstrings,
  commits, and variable names (per global `CLAUDE.md`). Oxford comma.

---

## 9. API call gating

**Before any paid API call** (batch or real-time, not just Anthropic —
also Zenodo if it hits quota, Zotero writes, etc. where applicable),
stop and report: (1) model/service, (2) batch vs real-time, (3) number
of calls, (4) estimated cost. Get explicit approval. Approval for one
batch does **not** imply approval for subsequent batches. This
convention was established during the map-reader-llm project and is
recorded in Shawn's memories and scratchpad.

CC's own internal tool use within the Max plan does not require gating;
external paid APIs do.

---

## 10. What Shawn expects from the first session

In approximate order (confirm and adjust — don't execute blindly):

1. Read `CLAUDE.md` (user global and personal-assistant project),
   scratchpad, and relevant memories for working style.
2. Read this briefing, the two Google Drive documents, and skim the
   archived notebook at `archive/2026-04-22-inscriptions-spa.ipynb`.
3. **Propose a revised plan** — not an execution, a plan. Include:
   - How you'll allocate work to agents vs. main thread.
   - Prior-art targets (code, papers, methods) and which agent fetches
     each.
   - A sketch of the §5.3 minimum-count method you think is most
     promising, with a one-paragraph justification.
   - A proposed shape for the Saturday deliverable.
4. Flag the **known-unknowns** this brief leaves open — especially
   anything that affects feasibility.
5. Only then begin execution, in specification-first mode.

If at any point you notice the session has slipped back into step-by-step
pair-programming, surface it to Shawn. That is a failure of the
upskilling frame and should be corrected, not tolerated.

---

## 11. Open questions this brief doesn't answer

Flagged so the first session knows to resolve rather than assume:

- Voitek's surname and affiliation.
- Which source recommended letter count as a complement to inscription
  count (§5.4).
- The May 2026 conference — venue, exact date, abstract deadline, length
  (20-minute talk confirmed; paper format unknown).
- Whether the AD 600 chronological cap is the final choice or a starting
  point for sensitivity analysis.
- Whether `environment.yml` or `requirements.txt` is the canonical env
  spec going forward (both are retained; pick one).
