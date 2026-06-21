# Spec — Option 2: women-corpus de-fogging CASE-STUDY (in-paper, co-authored)

**Status:** DRAFT for sign-off (recorded 2026-06-21 on Shawn's brief; not yet
executed). The **middle rung** of the three-option women-corpus ladder (see
`spec.md` §2): more than the Option-1 feasibility vignette (done), short of the
Option-3 EJA companion (the full crossover-age history, deferred).
**Author:** Claude Code (Opus 4.8, 1M context). UK/Australian English; Oxford comma.

> **α is the CONVENTION fraction** (1 − α = genuine). All α below are convention
> fractions (corrected 2026-06-21; matches the lodged prereg).

## 1. Purpose & position

A **bounded, co-authored substantive case-study** for the JAMT paper: what
rigorous editorial-convention deconvolution reveals about a real, hard,
demographically-important familial-inscription corpus (Adela Sobotkova's
wives/daughters). The point is not "the method applies" (that is Option 1) and not
"here is the Roman marriage-age history" (that is Option 3, the EJA companion) —
it is **"here is what de-fogging does to, and tells us about, a corpus the
demographic literature actually relies on."**

| rung | claim | venue | status |
|---|---|---|---|
| 1 feasibility | "the method applies + reachability verdict" | JAMT (method §) | **DONE** |
| **2 case-study** | **"a real, caveated de-fogged result + source-criticism"** | **JAMT (case-study §)** | **this spec** |
| 3 companion | "the crossover-age history" | EJA companion | deferred |

## 2. Scope boundary (hard — same as Option 1)

Reports the de-fogged **temporal distribution**, the **source-critical** findings,
and the **C2–C3 trough read**. It does **NOT** compute the wife-vs-daughter
**crossover-age trajectory** — that is Option 3 (the EJA companion). Per-role
fits remain for reachability + the temporal comparison, never for the age crossover.

## 3. The substantive content (what Option 2 actually claims)

Built on the Option-1 fits (3 converged cc-library fits; `outputs/`):

1. **Source-criticism (the strongest, most transferable claim).** The datable
   conjugal corpus is **~90 % editorial convention** (α ≈ 0.90 overall / 0.84
   daughters). This is a *quantified, transferable* caveat for the large body of
   Roman demographic work that dates familial / funerary inscriptions: when genuine
   dating is rigorously separated from editorial convention, ~90 % of this corpus's
   *apparent* temporal signal is convention. A genuine methodological-substantive
   contribution with relevance well beyond Adela's corpus.
2. **A worked reachability instance.** This corpus sits **below / at the floor**
   (daughters N = 453 < 500; α ≫ 0.70 envelope) — a concrete demonstration of the
   reachability map applied to a real demographic corpus, and of *why* time-resolved
   claims on such corpora need hedging.
3. **The indicative C2–C3 read.** De-fogging **shifts temporal mass *into* the
   trough window** (overall raw 0.57 → genuine 0.64, +0.07; daughters 0.50 → 0.60,
   +0.10) — so the apparent thinness of the record there may be partly an editorial
   artefact. **Indicative only** (genuine CIs are very wide, e.g. daughters
   [0.35, 0.88]); framed as a hypothesis, not a result. Directly relevant to the
   crossover-trough *timing* without computing the crossover.
4. **(If Adela provides `tempun` output) de-fogging vs aoristic MC.** A
   genuine-vs-raw-vs-`tempun` overlay shows that convention de-fogging removes a
   *different* artefact from aoristic uncertainty — the methodological point that
   her existing pipeline and ours are complementary, not redundant.

## 4. New analytical work beyond Option 1 (the key piece)

- **The "better-dated subset" probe (THE decisive new analysis).** Does restricting
  to narrow-interval inscriptions (e.g. date-range width ≤ 50 y, or a securely-dated
  sub-corpus) move a sub-corpus **into the reliable envelope** (α ≤ 0.70 AND
  N ≥ ~500)? If **yes**, that sub-corpus can carry an *actual reliable* de-fogged
  substantive read — materially strengthening Option 2 from "source-criticism +
  indicative" to "a defensible temporal result on the well-dated core." If **no**,
  Option 2 rests honestly on §3.1–3.3. Either outcome is reportable. *(A few more
  cc-library fits on the width-filtered subset — minutes on sapphire.)*
- Confirm Adela's exact `datable` / `conjugal` definitions + any quality gate
  (`link_status` / `confidence`); re-run on her definitions if they differ.
- (Optional) the `tempun` overlay, pending her output.

## 5. Deliverables

- A **JAMT case-study subsection draft** (~1–2 pages), co-authored framing with
  Adela: the source-critical headline (~90 % convention), the reachability instance,
  the better-dated-subset outcome, and the indicative C2–C3 read — all caveated.
- The **better-dated-subset probe** results (JSON + a verdict) + an updated figure
  (the reliable sub-corpus's genuine-vs-raw, if it reaches the envelope).
- Reuse the Option-1 figure (`fig-women-genuine-vs-raw`) + `c2c3-trough-read.json`.

## 6. Governance & compute

- **Collaboration data** (Adela, Aarhus); **co-authored**; not published without her
  involvement; AI-use collaboration-governed. Her substantive framing input is
  required before this is paper-ready.
- Compute: the better-dated-subset probe is a handful of cc-library fits (minutes on
  sapphire); the rest is analysis + writing. No grid.

## 7. Open decisions for sign-off

1. Confirm Option 2 lands as a **case-study section in the JAMT paper** (vs a short
   standalone note).
2. Approve the **better-dated-subset probe** (the decisive new analysis) — and the
   width threshold(s) to test.
3. Co-authorship + timing with Adela (and whether to wait on her `tempun` output /
   filter confirmation before drafting).
4. How prominent the source-critical "~90 % convention" headline should be — it is
   the most broadly-relevant finding and could anchor the case-study.
