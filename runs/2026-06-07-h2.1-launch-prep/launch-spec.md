# H2.1 temporal-mixture — launch spec

**Date:** 2026-06-07 · **Author:** Claude Code (Opus 4.8) on Shawn Ross's brief
**Status:** **SIGNED OFF (Shawn 2026-06-08).** Gate (a) CLEARED (re-validation
**PASSED**, B = 96.4 %; `FULL-GRID-REPORT.md`) and gate (c) CLEARED (this sign-off,
with grey-band included caveated, all six supplementaries, `women.csv` deferred,
`TMPDIR`-on-disk guard added). **The one remaining gate is (b): Shawn lodges the
Decision-38 convention-model OSF amendment (Amendment 03).** The production fit
must not run until A03 is lodged; the harness may be built + smoke-tested before.
**Binds:** Decisions **37 (D1–D6)**, **38** (empirical convention basis), 33, 34,
35, 36; the lodged prereg §3 + Amendments 01/02; the 2026-06-05 prereg-completeness
audit.

This is the production run of the preregistered temporal deconvolution-mixture: it
fits, per unit, the editorial-convention-corrected genuine summed-probability
analysis (SPA) of inscription dates, and hands the corrected curves to H3b.

---

## 1. Gates (what licenses the launch)

| Gate | Status |
|---|---|
| Template-dictionary scan (prereg line 202) | **DONE** (`runs/2026-06-05-template-dictionary/`, `6d8950f`) |
| Convention basis rebuilt (Decision 38, Option 2) | **DONE** (`runs/2026-06-06-convention-basis-redesign/design.json`) |
| Recovery re-validation (Decision 38 §6) | **PASS** — Stage-1 triage PASS; full grid 450/0, B = 96.4 % (2026-06-08, `FULL-GRID-REPORT.md`) |
| Decision-38 convention-model OSF amendment | **DRAFT complete (§A5.5 filled), awaiting lodgement — THE ONE OPEN GATE** |
| This launch spec sign-off | **CLEARED** (Shawn 2026-06-08) |

No production mixture fit runs until all five clear. (Amendment 02, Latin-frame
cross-sectional, is already lodged and is independent of this temporal track.)

## 2. Unit set (Decision 37 D1; verified `unit-set.json`)

**26 primary mixture fits** = 2 aggregates + 19 Latin provinces + 5 Latin cities,
all clearing the N ≥ 2,000 deconvolution-reachability floor (Decision 34):

- **Empire-aggregate** — N = 180,609 (incl. Rome). **Secondary/context.**
- **Latin-aggregate** — N = 109,646 (39 Latin provinces, Rome excluded). **Primary.**
- **19 Latin provinces** N ≥ 2,000: Latium et Campania (18,512), Dalmatia (7,088),
  Hispania citerior (6,312), Germania superior (5,874), Venetia et Histria (5,872),
  Dacia (4,870), Britannia (4,647), Pannonia superior (4,460), Samnium (4,187),
  Africa proconsularis (3,518), Germania inferior (3,390), Apulia et Calabria
  (3,132), Pannonia inferior (3,132), Numidia (3,014), Etruria (2,801), Umbria
  (2,763), Noricum (2,761), Baetica (2,593), Transpadana (2,434).
- **5 Latin cities** (`urban_context_city`) N ≥ 2,000, Rome excluded: Pompeii
  (4,508), Salona (3,465), Ostia (2,644), Mogontiacum (2,398), Aquileia (2,034).

**Grey-band — INCLUDED caveated (Shawn 2026-06-08; N ∈ [1,549, 2,000)):** Moesia
inferior (1,952), Lusitania (1,685) — run as **caveated-tier** (below the validated
N≈2,000 floor), bringing the run to **28 fits (26 primary + 2 grey-band)**.
**Sub-floor units (< 1,549)** fall back to date-window counts / §5 — not a
standalone mixture (prereg "Scope of the mixture correction").

**Deferred exploratory candidate (Shawn 2026-06-08):** the wife/daughter thematic
subset (`data/women.csv` — 893 wife + 504 daughter roles over 1,284 inscriptions,
**~1,200 in-envelope**) is sub-floor *and* thematic (outside the preregistered
geographic confirmatory frame). Revisit as a dedicated **exploratory worked
example**, not in this confirmatory run. Prep notes for then: the file is
gzip-compressed (despite the `.csv` name), is person-role-level (dedup to the 1,284
inscriptions), and its dating schema should be checked against LIRE before an SPA.

## 3. Model (Decision 35 + Decision 38)

Production model = **`cell_lib.build_model_f1_f3`** (the recovery-validated builder;
F1 = `Beta(1,1)` α prior, F3 = non-centred GRW on `log_pgen_increments`):

```
α            ~ Beta(1, 1)
tier_weights ~ Dirichlet(ones(3))            # 3 tiers; Decision 38 Option 2
p_conv       = tier_weights · tier_basis      # FIXED empirical calendar-slab basis
σ_smooth     ~ HalfNormal(1)
z_pgen       ~ Normal(0, 1, shape=n_bins-1)
p_gen        = softmax(cumsum(σ_smooth · z_pgen))   # GRW genuine component
p_mix        = α·p_conv + (1-α)·p_gen
y_obs        ~ Multinomial(N_eff, p_mix)
```

**Convention basis (Decision 38, Option 2).** `tier_basis` is the **fixed,
empirical 3-tier calendar-slab basis** (sub-century [half-50] / century /
multi-century [150+200+300]), built frequency-weighted from the anchor-stripped
F1+F3 calendar population. **No reign tier** (reigns/dynasties/events are
genuine-but-aoristic). **Basis population per frame** (Shawn 2026-06-06):

- **Empire-aggregate** → `tier_basis_empirical` (empire frame);
- **Latin-aggregate + all 19 provinces + 5 cities** → `tier_basis_empirical_latin`
  (the shared Latin basis). **Not per-unit** — a per-unit basis would absorb that
  unit's genuine temporal signal into `p_conv` and defeat the deconvolution.

The fine brackets (quarter-century + 20/30/40-y windows, ~7 % of the convention
pool) are **excluded from primary `p_conv`** and ride as the add-them-back
sensitivity band (§6).

## 4. Observation model (Decision 37 D6; prereg line 183)

Per unit: build the per-bin aoristic-mass SPA on the 80-bin envelope (each
inscription deposits mass uniformly across its `[not_before, not_after]` interval,
clipped to 50 BC – AD 350), then **largest-remainder (Hare) rounding** of the
per-bin mass to integer counts summing to `N_eff` (the unit's in-envelope
inscription mass), and `y ~ Multinomial(N_eff, p_mix)`. Uniform within-interval is
primary; trapezoidal is a sensitivity (§6, Decision 4 / audit C11).

## 5. Bins & sampler (Decision 37 D3, D6)

- **Envelope:** 50 BC – AD 350, **5-year bins, 80 bins** (the recovery-validated
  configuration). No coarser-bin variant.
- **Sampler:** validated defaults — `n_draws=2000, n_tune=1000, n_chains=4,
  target_accept=0.95, cores=1`. Raise `n_tune` on a convergence failure; **never
  relax the gate**.
- **Non-blind** (no prior real-corpus mixture exists; Decision 37 D6).

## 6. Supplementaries (Decision 37 D6 "full scope" + audit C11–C16)

Run on the same real-data fits:

1. **Fine-bracket sensitivity band** (Decision 38 §5, Option 2): re-fit with the
   four fine brackets moved into convention (anchor-stripped via
   `historical-anchor-intervals.json`); report primary vs sensitivity as a
   robustness band (the ceramics stacked-band idiom). Expected to barely move
   (fine brackets are low-distortion).
2. **Aoristic-Monte-Carlo mixture** (Decision 28) on **all 26 units** — `N_MC ∈
   [20, 50]`; flag if the MC-aoristic posterior diverges from the
   largest-remainder posterior by > 1.5× the posterior SD.
3. **Model-comparison fits** (Decision 19): Dirichlet-multinomial and
   rescaled-negative-binomial observation models alongside the multinomial primary.
4. **Trapezoidal-aoristic sensitivity** (Decision 4 / audit C11) on the
   within-interval mass shape — report alongside uniform (empire SPA r ≈ 0.94 < 0.95
   already trips "report alongside").
5. **H2.2 / H2.3 / H2.4 consistency checks + empire-α descriptive context**
   (audit C13–C16) — off the same fits.
6. **Empire-level empirical-Bayes sensitivity** (Decision 37 D4): one EB run on the
   empire-aggregate with corpus-wide Stage-1/2 priors, informative-but-wide
   (Dirichlet η ≈ 200·w_emp + 1.5σ — data-dominated, cannot manufacture the
   result); judged by Pearson r / Wasserstein-1 vs the learned-`p_conv` primary.
   Latin-re-derived EB deferred (run only if the empire EB diverges or a reviewer
   presses).

## 7. Acceptance — no ground truth (Decision 37 D5) · filled from the re-validation

**Reportability gates (per unit):**
- **convergence** — `cell_lib.convergence_pass` (max R̂ < 1.01 ∧ min bulk-ESS ≥ 400);
- **operating envelope** — **N ≥ 2,000 AND posterior α ≤ 0.70** ⟵ *CONFIRMED by the
  full grid: clean-pass B = 96.4 % within α ≤ 0.70, degrading sharply only at the
  out-of-envelope α = 0.95 stress row; no basis to tighten or loosen the ceiling
  (`FULL-GRID-REPORT.md` §3).*

**No-truth evidence (reported per unit):**
- descriptive-`p_conv` consistency — the model's learned convention fraction vs the
  unit's F1+F3 family-mass fraction (the two should agree in regime);
- posterior-predictive adequacy (PPC).

**Reporting:**
- posterior-**median** corrected genuine SPA (the H3b hand-off, §8);
- **α reported as a shape-conditioned diagnostic** (Bland–Altman limits of
  agreement), **not a precise dial** — Amendment 01 §A5.5.1; coarse directional
  convention-fraction statements only; ± precision from the re-validation:
  in-envelope 95 % LoA **[−0.12, +0.13]** (mean signed bias +0.005), shape-conditioned
  **±0.09** (smooth/flat) to **±0.18** (multimodal) — within Decision 33's ±0.18
  envelope (`FULL-GRID-REPORT.md` §4; `tables/alpha-loa-summary.json`);
- caveat bands in peaked-genuine regimes (Obs 68/73 — the GRW attenuates sharp
  peaks, so the corrected SPA may be conservative at the Antonine probe);
- flag the late corpus (AD ~142–347) as `p_conv`-dominated (Obs 69).

**Tiers:** reportable (gates pass) / caveated (peaked regime or grey-band) /
fall-back (sub-floor → date-window).

## 8. H2.1 → H3b interface (Decision 37 D2)

H2.1 hands H3b the **posterior-median** corrected genuine SPA per unit; H3b's
permutation envelope is the uncertainty representation — **no mixture-posterior
propagation** (prereg line 35; Obs 68/73). **Follow-up:** a raw-SPA-vs-corrected-SPA
H3b comparison (the GRW attenuates sharp peaks, so the corrected may be
conservative at the Antonine probe). H2.1 ⟂ §5 (complementary coverage; optional
high-N cross-check on the 5 cities).

## 9. Run plan (Decision 37 D6)

- **Host:** sapphire; `taskset -c 0-11`, `PYTENSOR_FLAGS=mode=FAST_RUN,allow_gc=False`,
  BLAS threads pinned to 1; **`n_jobs=12`** (the 2026-05-22 SMT lesson).
- **Scratch/temp on disk (the 2026-06-08 disk lesson):** export **`TMPDIR` to a
  disk-backed path** (e.g. `/home/shawn/.cache/inscriptions-pytensor-tmp`, on the
  264 GB root fs) so PyTensor's numba compile temp files do not fill the 31 GB
  RAM-backed tmpfs `/tmp` — the cause of the re-validation's 12-cell ENOSPC failure.
  **Pre-flight assert:** refuse to launch if `TMPDIR` free space < 20 GB
  (halt-and-report, per the standing rule).
- **Scale:** 28 fits (26 primary + 2 grey-band) × (primary + aoristic-MC +
  Dirichlet-MM + NegBin) + the empire EB + trapezoidal + fine-bracket-sensitivity
  ≈ **~850 fits, ~1 h parallelised** (Decision 37 D6 estimate; all six
  supplementaries confirmed in scope, Shawn 2026-06-08).
- **Hard stops (standing rules):** do not silently negotiate scope down to fit a
  time budget; do not relax the convergence gate; halt and report on any unit that
  fails convergence after a `n_tune` bump.
- Commit the design + this spec **before** launch; resumable per-unit; `STATUS.txt`
  + per-unit progress on sapphire.

## 10. Pre-launch checklist
- [x] 2026-06-08 Recovery re-validation full grid **PASS** (B = 96.4 %; `FULL-GRID-REPORT.md`) — gate.
- [ ] Decision-38 convention-model OSF amendment **lodged** — Shawn (still open — the one gate left before the production fit).
- [x] 2026-06-08 This spec **signed off — Shawn** (grey-band included caveated; all six supplementaries; `women.csv` deferred; `TMPDIR`-on-disk guard added).
- [x] 2026-06-08 Fill the §7 grid-dependent lines from the re-validation REPORT (envelope + α LoA).
- [ ] Build the H2.1 production harness (adapt the validated `build_model_f1_f3`
      pipeline to real-unit SPAs + the largest-remainder observation model + the
      per-frame basis selection) → smoke-test → launch on sapphire.

## 11. Provenance
- Unit set: `runs/2026-06-07-h2.1-launch-prep/{outputs/unit-set.json,code/verify-unit-set.py}`.
- Basis: `runs/2026-06-06-convention-basis-redesign/design.json` (`tier_basis_empirical[_latin]`).
- Model: `runs/2026-05-26-recovery-grid-two-unit/code/cell_lib.py::build_model_f1_f3`.
- Decisions 37 (D1–D6), 38, 33, 34, 35, 36; prereg §3; Amendments 01/02.
