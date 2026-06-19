# Amendment 01 §A5.4 content residual (inter-measure delta) — RESULTS

- **Status:** COMPLETE (exploratory; **DESCRIPTIVE — no threshold, no verdict**,
  per A01 §A5.4). Run locally (zbook-ubuntu), 2026-06-20; OLS + a small pooled-NBR
  scaling-residual fit, no API spend.
- **What this closes:** the single outstanding *analytical* preregistration item
  — AM01-d in `planning/prereg-obligations-coverage-sweep-2026-06-20.md` (the
  content residual was previously only narratively mentioned, never computed).

---

## 1. What was computed

**Content residual (A01 §A5.4).** OLS `log(letter_mass) ~ log(inscription_count)`
across the cross-sectional cities; the per-city residual is the content residual
(positive = more content per act than the corpus norm). On the **Latin primary
frame** (817 cities, 39 provinces): slope **0.971** (SE 0.015), intercept 3.941,
**R² 0.841**, n = 809 (8 zero-mass cities dropped — inscriptions present, no
readable Latin A–Z letters). The slope ≈ 1 says content scales **near-linearly**
with act count: letters-per-act is roughly constant across the corpus, and the
content residual is the small per-city departure from that constant. Residual SD
0.729 (in log units); range [−3.91, +3.65].

**Scaling residual (D12 SAMOC, recomputed on the Latin frame).** Pooled NBR
power-law `insc ~ NB(exp(a + β·log_pop), φ)`, then `r_c = log(insc_c) − (â +
β̂·log_pop_c)`. Latin pooled **β 0.687** (R̂ 1.0000, min ESS-bulk 5,422, 0
divergences).

**Self-check — D12 reproduction (PASS).** Recomputing the same construction on
the **empire** (all-provinces, 1,044-city) frame gives pooled **β 0.5656**, which
reproduces the persisted D12 all-provinces fit
(`runs/2026-06-16-s5-sensitivities/outputs/d12-scaling-residual-results.json`,
`stage1_pooled_scaling.beta_median` = **0.5654**) to within MCMC noise (Δ ≈
0.0002). This confirms the scaling-residual construction here is the canonical
D12 estimator.

---

## 2. The two-dimensional residual space — cross-tab

Both residuals are mean-~0 by construction; the sign split gives four quadrants.
On the Latin primary frame (n = 809 cities with both residuals):

| quadrant | meaning | count |
|---|---|---|
| Q1 | hi scaling, hi content (over-produces acts AND content/act) | 116 |
| Q2 | lo scaling, hi content (under-produces acts, over-produces content/act) | 298 |
| Q3 | lo scaling, lo content | 289 |
| Q4 | hi scaling, lo content | 106 |

**Association between the two residuals (Latin):** Spearman ρ **+0.004**
(p = 0.913); Pearson r **+0.008** (p = 0.825). **Empire context** (n = 1,001):
Spearman ρ **+0.006** (p = 0.859); Pearson r **+0.007**. The two residual axes
are **statistically orthogonal** on both frames.

The 2-D residual-space map is `outputs/content-residual-space-map.png` (Latin
primary + empire context panels) — a centred, structureless cloud, as the ~0
correlation implies.

---

## 3. Read (descriptive — no verdict)

The two over-production channels are **independent**. A city's tendency to
produce *more inscriptions than its population predicts* (the scaling residual —
the H3a/Hanson signal) carries **no** information about whether it produces *more
letters per inscription than the corpus norm* (the content residual): ρ ≈ 0 on
both frames. In plain terms, "epigraphically prolific for its size" and
"verbose per act" are **separate** properties of a city.

This is the informative descriptive result the amendment anticipated: the content
measure is **not** a rescaling of the act measure (if it were, the two residuals
would be collinear), so reporting both measures (acts and content) is not
redundant — they index different things. It also means the content residual adds
a genuinely new axis to the descriptive characterisation of city epigraphic
behaviour, orthogonal to the population-scaling axis the paper's confirmatory
spine sits on.

**No confirmatory bearing.** A01 §A5.4 pre-commits to no threshold and no
verdict; this result changes nothing in H3a/H9/H3c. It is a §5/descriptive
deliverable for the write-up.

---

## 4. Caveats

1. **Descriptive only** — no threshold, no verdict (A01 §A5.4). Cannot move any
   confirmatory result.
2. **8 zero-mass Latin cities dropped** from the content-residual fit (43 on the
   empire frame); reported, not imputed.
3. **Scaling residual recomputed per frame** for coherence; the persisted D12 is
   the all-provinces aggregate fit (the cross-check, not the source).
4. **Near-linear content–act slope (≈ 0.97)** means the content residual is a
   *small* departure from constant letters-per-act; its orthogonality to the
   scaling residual is the substantive point, not the slope magnitude.
5. **Orthogonality is on the cross-section** — it does not speak to temporal
   behaviour (letter-mass temporal analyses remain exploratory and corpus-wide
   unreachable, A01 §A5.2).

---

## 5. Outputs

`outputs/content-residual-results.json` (OLS fit, per-frame residual summaries,
cross-tab, seed, input sha256, provenance — source for all numbers here);
`outputs/content-residual-per-city.csv` (per-city Latin-frame residual pair +
quadrant); `outputs/content-residual-space-map.png` (the 2-D residual-space map).
Cross-refs: Amendment 01 §A5.4 (the pre-specified definition); D12
(`runs/2026-06-16-s5-sensitivities/`, the scaling-residual construction + the
reproduction cross-check); H9 (`runs/2026-06-18-h9-letter-mass-h3a/`, the
letter-mass frame builder + the letter-mass H3a confirmatory result); Obs 108
(the content-residual register entry).
