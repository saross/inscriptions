# Convention-basis redesign — PART 2 (the empirical 3-tier calendar-slab basis)

**Date:** 2026-06-06
**Author:** Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief
**Status:** **PROPOSAL** pending Shawn sign-off → recovery re-validation → OSF amendment. Nothing wired into a production fit.
**Binds:** Decisions 35, 36, 37, **38** (Option 2). Supersedes the Decision-20 tier structure (century / half-century / **reign**) and the 2026-05-22 recovery-grid `template_intervals_by_tier`.

This is PART 2 of the template-dictionary work: PART 1 (`runs/2026-06-05-template-dictionary/`, commit `6d8950f`) measured the exact-template frequency distribution; this part commits the basis the H2.1 mixture consumes, rebuilt around Decision 38.

---

## 1. What Decision 38 / Option 2 changed

The lodged-prereg + Decision-20 convention component was a hand-curated 3-tier
template dictionary (century / half-century / **reign**). The template-dictionary
scan showed it empirically inadequate (no home for the ~31 % multi-century mass;
over-weighted reign at ~2.7 %). Decision 38 replaced it with an **empirical
calendar-slab basis, no reign tier**, and reclassified reigns/dynasties/events as
**genuine-but-aoristic**. Shawn chose **Option 2** (2026-06-06): three learned
tiers from the **5 core calendar slabs only**, with the four fine brackets
**excluded from the primary `p_conv`** and ridden as an add-them-back sensitivity
band.

| | Decision 20 (old) | Decision 38 / Option 2 (this artefact) |
|---|---|---|
| Tiers | century / half-century / **reign** | sub_century / century / multi_century |
| Reign | a convention tier | **genuine-but-aoristic** (no tier) |
| Basis rows | uniform over hand-curated templates | **empirical** freq-weighted aoristic SPA of real F1+F3 inscriptions |
| Multi-century mass (~31 %) | unhoused | the `multi_century` tier |
| Fine brackets (quarter-c + 20/30/40-y) | folded in ad hoc | **excluded from primary**; sensitivity band |
| Learned-weight count | 3 | **3** (keeps the recovery-validated count) |

The learned-weight count stays at 3, so the Dirichlet structure that Grid A
validated is unchanged. Decision 38 §6 still requires re-validation because the
basis **shapes** change (they now carry a multi-century plateau).

---

## 2. The convention population (re-verified on the prereg-filtered corpus)

`01-verify-convention-population.py` recomputed the family split on the
**prereg-filtered** corpus (the 2026-05-24 slab CSV was built on *unfiltered*
LIRE; recomputing matters because the production model sees the filtered
population).

- Empire frame: **180,609** rows (filter reproduced). Latin frame: **109,646**.
- Family split (empire): Tight 14,277 (7.9 %) · F2_Other 17,354 (9.6 %) ·
  F1_round 109,853 (60.8 %) · F3_periodic 7,915 (4.4 %) · Big 31,210 (17.3 %).
- **F1+F3 convention pool: empire 117,768; Latin 62,733** (not the stale ~119 k).
- Reign/event leak into F1+F3: **129 inscriptions = 0.11 %, entirely `[161,180]`
  (Marcus)** — confirming Decision 38 §5 exactly.

A clean consequence of Option 2: both leak intervals (`[161,180]` w19,
`[161,200]` w39) are **fine-bracket widths**, already excluded from the primary
`p_conv`. So the historical-anchor list's numerical role is confined to the
sensitivity variant; the **5 core slabs are anchor-clean by construction**
(verified: zero canonical-reign matches at widths 49/99/149/199/299 under
25-year alignment).

---

## 3. The basis (`design.json`, `tier_basis_empirical`)

Each tier row is the **frequency-weighted aoristic SPA** of all anchor-stripped
F1+F3 inscriptions whose exclusive width is in that tier's slab-widths
(`02-build-empirical-basis.py`). Original interval width is the SPA denominator,
clipped to the 50 BC – AD 350 envelope — identical convention to the model's
observed `y`.

| Tier | Slab widths (excl.) | Empire N | Empirical weight |
|---|---|---|---|
| sub_century | 49 (half-century) | 20,084 | 0.184 |
| century | 99 | 47,004 | 0.431 |
| multi_century | 149 + 199 + 299 (pooled) | 42,060 | 0.385 |

Empire core total 109,148 (anchor-clean). The empirical weight vector
`[0.184, 0.431, 0.385]` is committed as the `empirical` (pilot-proxy) tier-weight
case — the realistic operating point for the recovery grid.

**Shapes** (`outputs/figures/basis-rows.png`): the `sub_century` row is
dominated by the `[1,50]` half-century spike (the single most common
half-century slab); `century` shows the classic boundary-stepped plateaus
(`[1,100]`/`[101,200]`/`[201,300]`); `multi_century` is a long flattish body with
a **late envelope-edge bump (15.3 % of its mass in AD 300–350)** from wide late
slabs such as `[301,500]` depositing only their in-envelope tail. The fine
brackets (excluded; grey dashed) are more peaked around AD 50–100.

The fine-bracket pooled SPA (anchor-stripped; empire n=8,491) is stored as
`fine_bracket_row_empire` for the sensitivity variant.

---

## 4. The recovery-hard risk (Decision 38 §6) — quantified

The `multi_century` row is the case Decision 38 §6 flags as *not* covered by Grid
A: a long flat body plus an envelope-edge plateau is **confusable with genuine
quiescence**. Diagnostics (empire): max/min density ratio 226; flat-core (AD
50–250) mean density 0.0158; late-edge mass (AD 300–350) 0.153. When the
`multi_century` tier dominates and `α` is high, the model must distinguish this
convention plateau from a smooth (or peaked) genuine signal — the explicit object
of the re-validation stress-triage (see `spec.md`).

---

## 5. Open design point for Shawn — basis population (empire / Latin / per-unit)

The basis SHAPE is built **once per frame** and applied as a **fixed,
unit-independent** convention template to every H2.1 unit. I built **empire** and
**Latin** bases (both in `design.json`). I did **not** build per-unit bases, and
recommend against them: a per-unit basis would encode that unit's genuine
temporal distribution (e.g. a 2nd-century-active province would peak its own
`century` row in `[101,200]`) into `p_conv`, defeating the deconvolution. The
learned tier weights + α + GRW `p_gen` carry per-unit variation instead.

**Decision needed:** confirm (a) **fixed shared basis per frame** (recommended),
not per-unit; and (b) the empire fits use the empire basis, the Latin fits
(Decision 36 primary) use the **Latin** basis. The recovery re-validation uses
the **empire** basis (broadest; bears the multi-century plateau most heavily).
This is flagged, not silently baked.

---

## 6. Artefacts

- `historical-anchor-intervals.json` — Decision 38 step 1 (21 reign/dynasty
  intervals + events policy; ±1-y match rule; leak measurement).
- `design.json` — the basis artefact (3×80 empirical basis, empire + Latin;
  fine-bracket rows; new tier-weight grid; reused shape_library / alpha_grid /
  n_grid; provenance counts).
- `code/01-verify-convention-population.py`, `code/02-build-empirical-basis.py`.
- `outputs/tables/{family-split,slab-frequencies,anchor-leak,tier-weights-empirical}.csv`.
- `outputs/figures/basis-rows.png`.

## 7. Next (gated)

1. **Recovery re-validation** — `spec.md` (stress-triage first: α=0.95 ×
   multi-century-heavy × peaked-genuine; full grid only if it passes). **Shawn
   sign-off before any sapphire launch.**
2. **OSF amendment** (convention-model revision; separable from Amendment 02).
3. **H2.1 launch spec** rewrite around this basis (Decision 37 D1–D6) → sign-off → launch.
