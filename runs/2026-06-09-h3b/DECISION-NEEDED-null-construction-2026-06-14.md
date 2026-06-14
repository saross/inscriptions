# H3b draw-wise — interim findings + decisions needed (2026-06-14, overnight)

**For Shawn, morning review.** The draw-wise H3b pipeline is built, verified, and
run end-to-end. It works — but the headline result runs into a known limitation of
the Timpson global test on real data, and resolving it well needs two methodological
calls that are yours, plus a correction to OQ-5 as I'd confirmed it. Nothing here is
final; I stopped rather than make these calls unilaterally.

---

## What is DONE and verified

- **Stage A** — `run_refit.py --emit-draws` re-ran the seeded 29-unit cc-library
  refit on sapphire (5.8 min, 0 errors) and persisted the genuine-SPA **posterior**
  (8,000 draws/unit) it previously discarded. **Provenance gate PASS** 29/29: the
  re-run reproduces the committed adopted-θ fits to within MCMC noise (α Δ ≤ 1.8e-3,
  SPA Δ ≤ 9.3e-4; draws↔median 4.6e-9). Draws are local + on sapphire.
- **Stage B engine** (`h3b_drawwise.py`) — builds the featureless-null MC envelope
  once per unit × null and evaluates all 8,000 draws against it. A **faithfulness
  self-test passes**: the inlined envelope reproduces the library
  `forward_envelope_test` / `permutation_envelope_test` bit-for-bit (exp + cpl), so
  any result below is a property of the *method*, not a coding divergence.
- Marginal-*p* headline + P(deviation) + per-draw spread, the λ=1.0/1.2 coverage
  sensitivity pair, the two probe windows (signed + one-sided), Holm (descriptive),
  soft-annotation + reachability flags, raw-vs-corrected — all computed and written
  to `outputs/drawwise/`.

---

## The core finding: the global Timpson test saturates at these corpus sizes

**Under both nulls, the global marginal-*p* = 0 for all 29 units** (exp: exactly 0;
cpl: ≤ 0.04). This is **not a bug** (the self-test rules that out) and it
**reproduces the 2026-06-09 draft's own conclusion** (`REPORT.md` lines 73–79).

The mechanism is the well-documented large-N over-power of the basic SPD/Timpson
envelope test:

- The real Roman epigraphic curve is strongly **humped** (the epigraphic-habit rise
  to ~AD 200, then decline). A featureless null can't reproduce that shape: the
  **exponential** is monotone (hopeless — empire shows 77/80 bins out-of-envelope),
  and even a flexible **3-knot CPL** underfits the full curve.
- At n_eff = 1,577 – 151,361 the pointwise MC envelope is Poisson-tight, so any
  residual misfit between the smooth null and the real curve registers as a
  "deviation". With enough inscriptions, *everything* is significant.
- Phase-1 calibrated detection at N ≈ 1,600 against a null that **matched** the
  generating smooth shape (single injected event on a matching baseline). On real
  data the null is misspecified relative to the true smooth shape, so baseline
  misfit + large N ⇒ global saturation.

**Implication:** the *global* marginal-*p* is an uninformative gate here (it always
says "there is structure", which is trivially true). The informative readout is the
**probe windows** — does the curve dip *locally* at the Antonine / Crisis windows
relative to its own smooth trend — which is what the prereg actually names.

---

## DECISION 1 — the CPL fit target (a correction to OQ-5 as I confirmed it)

When I asked OQ-5 you confirmed "null fit to the raw intervals/SPA". For the **exp**
forward-fit that is unambiguous (and right — the documented FP-fix). For **CPL** it
is ambiguous, and the two readings diverge sharply:

| CPL fit target | Global *p* | Probe windows | Verdict |
|---|---|---|---|
| **Raw** corpus SPA (my first build, the literal "fit to raw") | 0 | **also saturated** (P(dev)≈1 everywhere) | uninformative — the *correction itself* reshapes the whole curve, so the corrected curve departs from the raw trend everywhere, not just at events |
| **Observed corrected** curve (standard SPD; the 2026-06-09 draft's choice) | 0 | **differentiated** (P(deficit) 0.0–1.0) | the null tracks the curve's own smooth trend, so only *local* departures show |

I **switched CPL to fit the observed corrected curve** (the standard self-referential
SPD null, matching your draft) so you'd have informative results to look at — but this
**contradicts OQ-5 as literally confirmed**, so I'm flagging it rather than burying it.

> **Need from you:** confirm CPL should fit the **observed corrected** curve (my
> recommendation; standard practice; what your draft did), or insist on fit-to-raw
> (which saturates the probes and I'd argue is wrong — it conflates convention removal
> with historical events).

---

## DECISION 2 — how to treat the global saturation

The 2026-06-09 draft's answer was: *"Report the exp result as a saturation finding;
read deviations off the CPL-3 probe windows."* The draw-wise pipeline does exactly
that, with the probe deficit now a **posterior probability** rather than a binary.
Three options:

- **(a) Accept it (recommended, lowest-risk):** report the global test as a saturated
  gate (an honest methodological finding), and make the **probe-window P(deficit)**
  the H3b deliverable. Matches the draft + the prereg's named-probe emphasis.
- **(b) Large-N correction:** adopt a reduced-significance / mark-permutation variant
  or thin to an effective N so the global test is not over-powered. More work; changes
  the lodged test.
- **(c) More flexible null:** logistic, more CPL knots, or the **baorista**
  Bayesian-aoristic null (already a planned sensitivity, prereg line 378). Best
  principled fix but a real build; risks the null absorbing the events.

My recommendation: **(a)** for the DRAFT, with **(c)/baorista** noted as the
principled follow-up. Both are consistent with H3b being exploratory.

---

## DECISION 3 — the exp null's role

The exp null is degenerate on this data (monotone vs humped → 77/80 bins out). Keep it
as a **clearly-labelled saturated cross-check** (transparency; what the draft did), or
drop it from the DRAFT entirely? My recommendation: keep it, explicitly labelled
saturated, with CPL-fit-to-observed as the informative primary (this inverts the
spec's "exp primary / CPL secondary" — a sensible inversion for real humped data).

---

## What the (pending-confirmation) results show — CPL, fit-to-observed, λ=1.0

The probe-deficit posteriors are differentiated and historically coherent:

- **Named scopes:** empire-aggregate — Antonine **P(deficit)=1.00** and Crisis
  **P(deficit)=1.00**, both ≥20% bracket. latin-aggregate (the Western-Empire-
  provincial scope) — Antonine P(deficit)=1.00; Crisis P(deficit)=1.00 (sub-bracket
  magnitude). Consistent with the Antonine-plague and Third-Century-Crisis decline
  narratives.
- **Spread across units:** Crisis P(deficit) ranges from ~0 (Pompeii, Mogontiacum) to
  1.0 (empire, Italia, Africa, Numidia). Britannia (soft-annotated) Crisis
  P(deficit)=0.03; Moesia inferior (soft-annotated) 0.99.
- **Coverage-inflation sensitivity (λ=1.2)** behaves as designed: it nudges only
  borderline units (Hispania citerior Crisis 0.32→0.45; Britannia 0.03→0.08) and
  leaves saturated/near-zero ones unchanged.

Full per-unit × null × λ numbers: `outputs/drawwise/deviations-table.csv`.

---

## Reproduce

```bash
# Stage A (sapphire): re-emit posterior + provenance gate — already done.
# Stage B (local):
uv run python runs/2026-06-09-h3b/code/run_h3b_drawwise.py
```

Not yet produced (deliberately — pending Decisions 1–3): the DRAFT `REPORT.md` and the
per-unit envelope plots. Once you confirm the construction I'll finalise both.
