# Paper writing brief — inscriptions / LIRE deconvolution paper

**Status:** governing brief for the write-up phase (locked with Shawn 2026-06-20).
**Supersedes** ad-hoc framing notes; read this before drafting any section.
**Companion docs:** `reports/key-findings-summary-2026-06-20.md` (the on-ramp),
`runs/2026-06-20-figures/outputs/figure-captions.md` (figures at target level).

---

## 1. Target & scope

- **Journal:** *Journal of Archaeological Method and Theory* (JAMT, Springer).
- **Length:** **aim ~10,000 words** for the main text. JAMT sets no explicit word
  limit and publishes long articles, but we self-impose 10k for discipline and
  accessibility. Overflow of technical material goes to the supplement, not the
  main text.
- **Figures:** the built 14-figure set (`runs/2026-06-20-figures/`), vector PDF,
  sans-serif, JAMT/Springer artwork specs. Plain-language captions already drafted.

## 2. Audience — the dual readership (design every paragraph for both)

- **Primary reader:** a *typical* classicist / epigrapher / ancient historian /
  archaeology postgrad with **only rudimentary statistics**. They must be able to
  follow the argument, the findings, and *why they matter* without a stats
  background.
- **Expert reviewer:** assume **Crema, Bevan, or a peer of that calibre** (SPD /
  aoristic / Bayesian-archaeology specialists). The statistical core must be
  **tight and bulletproof** — no hand-waving they could puncture.
- The craft is serving both at once: plain-English exposition in the main text,
  full rigour available (in the supplement) for anyone who looks.

## 3. Governing principles

1. **Plain English first, alongside the statistics — never instead of, never
   after-only.** Explain *what* a method does and *what a result means* in plain
   language **before or alongside** the formal statement. No unexplained jargon;
   define every term on first use (SPD, aoristic, deconvolution, credible
   interval, sublinear scaling, Mundlak within/between, etc.).
2. **Push statistical detail, support, and argumentation to the supplement.** This
   serves *both* goals at once: it keeps the main paper accessible to the typical
   reader **and** makes the work bulletproof to a statistician reviewer (the full
   derivations, recovery grids, validation, sensitivity analyses, and prereg are
   all there to be checked). Main text states the result + the plain-English why;
   supplement carries the proof.
3. **Empirical-first / interpretation-later** (Obs 101). Present the empirical
   nested-unit decomposition and the corrected curves *first*; bring in
   interpretation (epigraphic habit, population, Hanson) *later*, in the
   discussion. Results stay model-conditional; use "association with population",
   "empire-wide common temporal component" (not "epigraphic habit") in results.
4. **Honesty framing baked in** (already in the figures): "illustrative relative
   shape, NOT a population estimate" (F8); convention *removal* + peak *recovery*,
   not "smoothing" (F1); the clean 38/29/33 partition with the 54% standalone
   footnoted (F9).

## 4. Main-text vs supplement split (working rule)

**Main text (accessible, ~10k words):**
- The problem (editorial-convention contamination of inscription dates) in plain terms.
- The method in concept (deconvolution: what it does, why), with one explainer figure.
- The validation in concept (Pompeii AD 79, Ostia apogee) — convincing, not technical.
- The findings, each stated plainly then supported: scaling is within-province;
  capitals over-produce; the temporal decomposition (38/29/33); the U-shape; the
  two orthogonal over-production channels; the reachability envelope as honest limits.
- Interpretation / significance for Roman history (discussion).

**Supplement (rigour, bulletproofing):**
- The full mixture/deconvolution model + the cross-classified likelihood derivation.
- The recovery-grid validation, θ re-derivation + sweep, convergence diagnostics.
- The preregistration + amendments trail (OSF), the obligations audit.
- Sensitivity analyses (DM/NegBin, aoristic-MC, measurement error, stratified sampling).
- The variance-decomposition maths (covariance-attributed partition) and the
  reachability simulation in full.

## 5. Style exemplar — how to explain the statistics

**Eftimoski, Ross & Sobotkova 2017**, "The impact of land use and depopulation on
burial mounds in the Kazanlak Valley, Bulgaria: An ordered logit predictive model"
(2017, vol. 23, pp. 1–10; Zotero key `ENPYIZQF`). This is **Shawn's own model** of
the register to hit: he explained an ordered-logit statistical approach to an
archaeology audience *after* extensive debriefing with Martin Eftimoski plus his
own web-searching and reading — i.e. a domain expert (not a statistician)
explaining a non-trivial method clearly and correctly. Re-read it before drafting
the methods sections; match its way of making a statistical model intuitive for an
archaeologist without dumbing it down.

## 6. Assets already at the right level

- **Key-findings summary** (`reports/key-findings-summary-2026-06-20.md`) — the
  non-specialist results narrative; the drafting on-ramp.
- **Figure captions** (`runs/2026-06-20-figures/outputs/figure-captions.md`) —
  "what is this? / what does it mean? / why does it matter?" prose at exactly the
  target accessibility; reuse and adapt for the main-text figure references.
- **14-figure set** — the visual backbone, honesty-framed.

## 7. Definition of "tight / bulletproof"

For the anticipated Crema/Bevan-calibre reviewer, every statistical claim in the
main text must have its full support reachable in the supplement, every method
choice must be justified (prereg + audit), and every limitation must be stated by
us *first* (reachability envelope, model-conditionality, anchors-held-out,
identifiability caveats) rather than discovered by the reviewer.

## 8. LLM-use disclosure (required by JAMT — in the methods)

JAMT expects LLM/AI use to be written up in the methods section (the Springer
Nature / COPE position: AI tools are **not** authors and cannot be credited as
such; their use **must be disclosed**, typically in methods or acknowledgements).
**Verify the exact current JAMT wording before submission** (the live guidelines
were auth-gated when checked 2026-06-20). Given how extensively this project used
an LLM agent, the disclosure should be unusually thorough and specific — it fits
the open-science ethos and pre-empts reviewer concern. It is a *strength* to be
candid here, not a liability. Draft content (the author knows the project; this is
the LLM's own honest account of what it did, for the authors to verify and edit):

- **Tools / models.** Claude Code (Anthropic) as the primary agent — principally
  **Claude Opus 4.8 (1M-context)**, with at least one analysis session run under
  **Fable 5**, plus task-specific subagents (literature scout, code auditor,
  adversarial verifiers). State the models, the period of use, and that it was an
  agentic coding/analysis tool, not a text generator for the prose.
- **Role — the "lab, not dev team" model.** The agent operated as a senior
  research-software-engineer / data analyst *under the PI's direction*. It
  implemented the analysis pipeline (the editorial-convention mixture
  deconvolution, the recovery-simulation validation grids, the Mundlak negative-
  binomial within/between scaling models, the §5 hierarchical trajectory models,
  and the sensitivity analyses), ran the computation (MCMC, bootstrap, permutation
  tests, grid sweeps on local servers), produced the figures, conducted literature
  scouting, and drafted documentation.
- **Human authorship & oversight.** All scientific decisions — the research
  questions, the hypotheses, the **preregistered** design, every methodological
  choice, and all interpretation — were made by the authors. The agent's work was
  gated by explicit pre-launch sign-offs and an API-call review gate, subject to a
  standing critical-friend statistical review, and corrected by the PI's domain
  expertise at key points (e.g. the α-identifiability diagnosis was the PI's
  catch). **The authors take full responsibility for all content.**
- **Verification.** Agent outputs were independently checked: adversarial
  verification subagents re-queried every cited DOI and re-checked results; a
  multi-agent accuracy audit re-verified ~677 numerical specifics against source
  files; analysis code was audited; and results reproduce from committed seeds.
- **Reproducibility / research record.** The analysis is preregistered (OSF
  `https://osf.io/uycs6/`); all code, data processing, and figure scripts are
  version-controlled (git); the agent sessions were captured as a persistent,
  auditable research record.
- **What the LLM did *not* do.** It did not originate the scientific claims or the
  interpretation, and it made no undisclosed methodological choices — all are
  logged in the prereg, the decisions register, and the git history.

**Ground it in the actual apparatus — this is the project's edge.** Unusually,
every claim in the disclosure is *auditable* against artefacts the project already
keeps, so the write-up can cite evidence rather than assert good practice (pull
exact counts at drafting; these are current as of 2026-06-20):

- **Observations registers** — `docs/notes/working-notes.md` (the research
  observations log, through **Obs 112**) and `docs/notes/claude-observations.md`
  (a separate "Claude observing Shawn" register): a contemporaneous record of
  findings and methodological turns as they happened.
- **Decisions register** — the logged design decisions (through **Decision 38**),
  in `planning/` + the continuity doc: every methodological choice, dated, with
  rationale.
- **Reflection apparatus** — `docs/notes/reflections/` (`reasoning-log.md`,
  `session-reflection.md`, `abductive-reasoning.md`, `session-log.md`, and the
  `continuity.md` session-close beacons): the agent's own reasoning trail.
- **Preregistration** — OSF `https://osf.io/uycs6/` (lodged 2026-05-20) + **four
  amendments** (git tags `osf-amendment-01..04`): the analysis was registered
  *before* it ran, and every deviation is tagged.
- **Independent verification** — `planning/doc-accuracy-audit-2026-06-20.md` (the
  multi-agent audit, ~677 numerical specifics re-verified) and the lit-scout /
  prior-art verifier passes.
- **Full git history** + the captured agent sessions (transcript location to
  confirm — `archive/cc-sessions/` is not in this repo; the in-repo distillations
  are the reflection + observation logs).

Cross-references for drafting: the working-relationship register in `continuity.md`
("Standing rules") documents the PI/analyst/consultant model. A short version of
the disclosure may also belong in a Data/Code-availability or author-contributions
statement, per JAMT's structure. The candour + the audit trail together make this
a model of transparent human–AI research collaboration, not a caveat to bury.
