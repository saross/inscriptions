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

## 4. New analytical work beyond Option 1 (the key piece) — DONE 2026-06-21

- **The "better-dated subset" probe — RUN, verdict NO** (`probe_better_dated.py`;
  `better-dated-probe-summary.json`). Fitting the cc-library deconvolution to the
  datable conjugal corpus restricted to date-range width ≤ {50, 75, 100, 150} y
  (all converged, 0 div): **every subset stays above the α ≤ 0.70 envelope** —
  width ≤ 50y **α = 0.97** (N 287), ≤ 75y **0.74** (N 390), ≤ 100y **0.82** (N 792),
  ≤ 150y **0.85** (N 1123). **No width-restricted subset reaches the reliable
  envelope.**
- **Why (the finding that makes this a *stronger* source-criticism):** width is the
  WRONG axis — the editorial convention is *structural*, sitting at *round* widths
  (F1_round 25-year slabs = 68 % of rows; widths 49/99/149y), so narrowing the
  interval *raises* the convention fraction (≤ 50y is the most convention-dated at
  0.97, dominated by round half-century slabs). The genuinely-precise core (Tight,
  width ≤ 4y) is **N = 6**; the non-aligned "genuine class" is **N = 315** — both
  far below the 500 floor. So there is **no well-dated sub-corpus large enough to
  rescue a reliable temporal read.**
- **Consequence for Option 2:** it rests on §3.1–3.3 (source-criticism + the
  reachability instance + the indicative C2–C3 read), now *strengthened* — the
  convention is not just ~90 % in aggregate but pervasive and structural, with no
  clean well-dated core. The crossover-trough *timing* cannot be put on solid
  ground by de-fogging at any scale (a definite, useful answer for Adela).
- Still to do: confirm Adela's exact `datable`/`conjugal` definitions; the
  optional `tempun` overlay; the case-study subsection draft (with her).
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
