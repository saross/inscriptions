# Outline — Option-2 case-study section (JAMT)

**Status:** OUTLINE for discussion → drafting (shaped with Shawn 2026-06-21; two
review rounds). Short, source-critical methods case study. Co-authored with Adela
Sobotkova. Drafting begins once this conceptual approach is agreed.
**Scope:** no crossover-age trajectory (that is the EJA companion, Option 3).

## Conceptual spine (the frame for the whole section)

**The deconvolution is a *diagnostic* and a *hypothesis generator*, not a
prover.** On a corpus like this — heavily convention-dominated and below the
reachability floor — de-fogging does **not** answer the demographic question. What
it does is (1) **quantify how far the time axis can be trusted** (here: not far),
and (2) **surface specific, testable hypotheses** for better-dated future work. The
honest "limits" verdict *is* the contribution: a transferable caution for
inscription-based Roman demography, plus a worked demonstration of the method as a
source-critical instrument.

Two framing commitments (Shawn 2026-06-21):
- **Hypothesis-generating, not hypothesis-confirming.** Every substantive read in
  the section is explicitly a *hypothesis to test*, never a finding or a proof.
- **A "limits" result is a legitimate, useful result** — we lead with it, not bury it.

## Section-by-section

1. **Setup — the demographic stakes.** The Shaw–Saller crossover-age tradition
   reads age-at-marriage off the *temporal distribution* of dated familial
   inscriptions; Adela's "Graveyard → Time Series" extends this to a time series.
   The prerequisite nobody checks: **is that time axis trustworthy enough for
   time-resolved claims?** That is the question this case study answers (for one
   real corpus, and by extension the genre).

2. **Corpus + method (brief).** The datable conjugal corpus — N = 1,291 (838
   wives, 453 daughters); we used exactly Adela's analysis set (same date window,
   no quality gate — confirmed 2026-06-21), dropping only 106 undated/out-of-window
   rows. The same cc-library deconvolution as the main paper's units; the
   reachability envelope (α ≤ 0.70 & N ≥ floor) as the trust criterion.

3. **Result 1 — the time axis is ~two-thirds-to-90 % editorial convention**
   (α ≈ 0.90 overall / 0.84 daughters; convention fraction). Contextualise: the
   ~100-year median date range and the 68 % round-25-year (F1) slabs make this
   *expected*, not surprising — which is precisely the point for the genre. **The
   headline source-criticism.**

4. **Result 2 — there is no rescuable well-dated core** (the better-dated probe).
   Width is the wrong axis: convention is *structural* (it lives at round widths),
   so narrowing the interval *raises* α (≤ 50y band = 0.97); no width-restricted
   subset reaches the envelope; the genuinely-precise core is N ≈ 6 (Tight) to 315
   (non-aligned), below the floor. **So the limit is intrinsic to how the corpus is
   dated, not a sample-size problem we could filter around.**

5. **Result 3 — an indicative, hypothesis-generating read of the trough window**
   (heavily caveated). De-fogging *shifts mass into* the C2–C3 window (overall raw
   0.57 → genuine 0.64; daughters 0.50 → 0.60), so **a hypothesis worth testing on
   better-dated data is that the apparent thinness of the record there is partly an
   editorial-convention artefact.** But the genuine credible intervals are very wide
   (daughters [0.35, 0.88]); this is explicitly a *hypothesis*, never a result.

6. **De-fogging vs `tempun` (KEEP — Shawn 2026-06-21).** Adela's `tempun` Monte-Carlo
   handles *aoristic dating uncertainty*; our deconvolution removes *editorial
   convention*. They are **complementary, not redundant** — they correct different
   artefacts. Show genuine-vs-raw-vs-`tempun` to make the point concrete. (Requires
   her `tempun` output, or we run `tempun` ourselves — see "Open / pending" below.)

7. **Implications — the diagnostic as a hypothesis engine.** For inscription-based
   Roman demography: convention de-fogging is a **necessary first diagnostic** —
   it tells you whether a corpus's time axis can carry time-resolved claims, and
   when it can't (as here), it converts apparent patterns into *hypotheses for
   better-dated work* rather than conclusions. Many familial-inscription corpora may
   be similarly convention-bound. The substantive crossover-age history is reserved
   for the EJA companion (Option 3). *(Framing check pending Shawn: keep the
   genre-wide implication, but as a hypothesis-engine point, not a sweeping verdict.)*

## Open / pending (not blocking the conceptual agreement)

- **`tempun`** — install + run ourselves over the women corpus for §6 (and keep as a
  reusable cross-check tool); or use Adela's output if she shares her repo. (Shawn
  greenlit installing it 2026-06-21.)
- **Adela's co-author input** on the substantive framing + the §7 genre claim.
- **Placement** — short section in JAMT; final placement held (Shawn 2026-06-21).

## Material already in hand (drafting inputs)

Obs 115 (feasibility), Obs 117 (probe), `MEMO.md`, `option-2-case-study-spec.md`,
`better-dated-probe-summary.json`, `c2c3-trough-read.json`, the women figure
(`fig-women-genuine-vs-raw`). All α = convention fraction (Obs 116).
