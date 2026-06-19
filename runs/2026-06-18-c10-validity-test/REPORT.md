# C10 aoristic-MC validity test — REPORT (top-level)

- **Status:** ✅ COMPLETE — two result waves ran (first wave 2026-06-18;
  follow-up "(ii)" 2026-06-19; base_seed 20260618). This top-level report was
  added 2026-06-20 (pre-write-up uplift) to surface the verdict that previously
  lived only inside `outputs/` (the dir's BUILD-NOTES said "NOT RUN"). The full
  results are in the two `outputs/` reports cross-referenced below.
- **What C10 is.** The preregistered aoristic-Monte-Carlo supplementary
  (prereg §3/§4/§6; Decision 28) on the real-data primary. It asks whether the
  point-date aoristic-MC recovers the deconvolution's α, and — when it does not
  on the real empire — *why*. N_MC and the 1.5× divergence flag are pinned in
  `SPEC.md`.

---

## Verdict (re-read from the two outputs reports)

**(a) SUPPORTED — point-date aoristic-MC tracks planted α on synthetic; C10
stands** (`outputs/VALIDITY-REPORT.md`). On synthetic ground truth the
point-date arm recovers the planted α within tolerance (max |Δα| = **0.046**;
mass arm max |Δα| = 0.043), across planted α ∈ {0.30, 0.50, 0.68, 0.80}.

**The real-empire point-date collapse is a METHOD ARTEFACT, not a genuine
α-sensitivity.** On the real empire the point-date arm collapses (point-collapse
α ≈ 0.10 vs mass-preserving α ≈ 0.62). The realism-graded follow-up (ii)
(`outputs/followup-ii-report.md`) decomposes the cause: the collapse is
**REPRODUCED by variants R2 and R1+R2** and **NOT** by R0 or R3 (controls
clean). I.e. it is driven by **θ-contamination (R2) — the three-step
classify-then-analyse plug-in bias — NOT by interval width (R1)**:

| variant | mass recovers | mean arm divergence | point-date median α | reproduces collapse |
|---|---|---|---|---|
| R0 (control) | True | 0.003 | 0.622 | False |
| R1 (width) | False | 0.206 | 0.438 | False |
| R2 (θ-contamination) | True | 0.224 | 0.301 | **True** |
| R3 (control) | True | 0.004 | 0.614 | False |
| R1+R2 | True | 0.197 | 0.318 | **True** |

**Disposition (consistent with the prereg).** By the prereg rule the aoristic-MC
divergence flag is explicitly **NOT an amendment trigger**; the point-date
collapse is reported as a **method limitation** of the three-step plug-in
estimator, not as a genuine α-sensitivity. The mass-preserving aoristic-MC is the
sound read. (Coverage sweep item C10; matches Obs 110.)

---

## Outputs (the two result-bearing reports + artefacts)

- `outputs/VALIDITY-REPORT.md` — first wave: synthetic ground-truth recovery
  (1b), the slab-concentration diagnostic (1a), the real-empire read (1c), and
  the SPEC §3b decision-rule verdict "(a) SUPPORTED".
- `outputs/followup-ii-report.md` — follow-up (ii): the realism-graded R0–R3 /
  R1+R2 decomposition isolating θ-contamination (R2) as the collapse driver.
- `outputs/results.json`, `outputs/followup-ii-results.json` — the persisted
  numbers (config, planted α, per-variant tables; base_seed 20260618).
- `outputs/run-c10-full.log`, `outputs/precheck-mass-arm-alpha068.{json,log}` —
  run traces.

Cross-refs: SPEC.md (the decision rule + N_MC/1.5× pins); BUILD-NOTES.md +
C10-FOLLOWUP-NOTES.md (build-decision records); the coverage sweep C10 row
(`planning/prereg-obligations-coverage-sweep-2026-06-20.md`); Obs 110 (the C10
register entry).
