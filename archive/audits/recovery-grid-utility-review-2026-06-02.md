# Recovery-grid utility review — what the Bayesian deconvolution is for, and how reliable it is

**Date:** 2026-06-02
**Status:** review record (qualitative + two diagnostics). Feeds Decision 33 and
OSF Amendment 01 §A5.5.1.
**Audience:** Shawn (and a non-specialist reader); a check that the analysis
provides real utility and aligns with good statistical practice.

**Links:**

- Decision 33 (`planning/decision-log.md`).
- OSF Amendment 01 §A5.5.1 (`planning/osf-amendment-2026-05-29-two-measure-framework.md`).
- Prior-art scout + implementation review (`planning/prior-art-scout-2026-06-02-recovery-validation-metrics.md`).
- Grid A verdict (`runs/2026-05-26-recovery-grid-two-unit/inscription-mass/outputs/REPORT.md`, commit `0638093`).
- Diagnostics this review commissioned (`runs/2026-06-02-recovery-utility-check/`).

---

## 1. What the model does (plain language)

Every inscription carries a *guess* at its date. Some guesses are sharp
("Hadrian's reign, AD 117–138"); many are blunt, snapped to editorial
conventions ("2nd century" = AD 100–199). Pile up all the guesses across time
and the blunt, century-rounded ones manufacture **fake structure** — plateaus
and steps at century boundaries — that looks historical but really records *how
the inscriptions were catalogued*, like everyone calling old buildings "from the
1800s" and producing a fake spike at 1850.

The model **separates the real timeline from the cataloguing fog**, splitting the
piled-up curve into:

- **the genuine signal** (`p_gen`) — the real rise-and-fall of inscribing
  activity over time;
- **the convention component** (`p_conv`) — the artefactual mass created by blunt
  editorial dating;
- **α** — one dial: how much of the total is convention fog vs genuine signal.

`observed = α · p_conv + (1 − α) · p_gen`.

**Two useful products, not one.** The primary payload is `p_gen` — the de-fogged
timeline, so historical analysis is about real behaviour, not cataloguing habits.
But **`p_conv` is itself a finding**: how communities and editors snapped dates to
templates characterises epigraphic practice. Crucially, we characterise the
convention component **descriptively, straight from the raw interval structure**
(endpoint frequencies, slab widths, the F1/F3 family classifier) — those are
robust facts independent of the Bayesian fit. That is why we do **not** need a
precise model-derived α *dial*: the descriptive characterisation already carries
the convention story (see §4b), and it lets us treat α as a coarse diagnostic
rather than a load-bearing estimate.

## 2. What it's for, and how reliable — three tiers

The **recovery grid** is a "bury known objects, then test the metal detector"
exercise: manufacture datasets where we secretly know the truth, fit the model,
and check it recovers them — *before* trusting it on real data. Under the
corrected metrics (Decision 33), the picture is:

| Claim you'd want to make | Reliability | Verdict |
|---|---|---|
| **The *shape* of genuine activity over time** (rises, peaks, falls, deviations) | **Strong** — correlation ≈0.998; passes the shape test in **~92%** of cases within the safe zone | **Trust it** — this is the model's real payload |
| **How much is editorial fog** (the α dial) | **Coarse only** — recoverable to ≈**±0.18** | Use *directionally* ("mostly fog" vs "mostly genuine"); not as a precise % |
| Anything in the **heavy-fog regime** (α > ~0.70) | **Weak** — genuine signal too swamped | **Don't trust** fine claims; flag as a limitation |

**One-line answer:** use it for the **de-fogged shape of epigraphic activity over
time**, for periods/places not dominated by editorial templates — exactly what the
temporal analyses (deviation detection, the §5 city curves) need. It is *not* a
precision instrument for "exactly what fraction was editorial."

**Important refinement from the band-calibration check (§4a):** "trust the shape"
means trust the **median timeline** (the point estimate). The **uncertainty band**
around it is honest for *smooth* timelines but **overconfident (too narrow) for
sharply-peaked timelines, especially at large N** — so recovered peaks are likely
attenuated and their error bars understated. The real corpus has sharp regnal
clustering (AD ~77, ~122, ~212), so this caveat bites in practice.

## 3. The four confirmations

**(1) Principled? — Yes, with transparent judgement calls.** The two things we
changed were *broken*, not inconvenient: Pearson r on a flat target is literally
`0/0` (undefined), and exact interval-coverage collapsing as data grows is a known
theorem (posterior concentration / Bernstein–von Mises), not a model fault. We
kept the original shape test (Pearson ≥0.95) unchanged wherever it is defined, set
thresholds *before* seeing the verdict, and report the failing scenarios beside
the passing one. The genuinely judgement-laden bits (the α≤0.70 envelope; demoting
α) are *defensible but not forced*, and are flagged for Martin's sign-off.

**(2) Literature-grounded, good fit? — Yes, strongly.** A verified prior-art scout
found that *no* relevant community gates on exact interval-coverage of a mixing
dial; Wasserstein-1 (our flat-case metric) is the *theoretically justified*
measure for this de-convolution problem (Rousseau & Scricciolo 2021); and a flat
timeline is a *standard test case* in radiocarbon work, not a degenerate one. The
closest published cousin (`baorista`, Crema 2025) validates *less* than we do — so
we are more thorough than the field, not less. We also identified that the fanciest
option (SBC) does not fit our design and chose the right alternative.

**(3) Aligns with broader good statistical practice? — Yes.** Validate-on-
simulated-truth-before-real-data, report an *operating envelope* rather than a
binary pass, demote an un-pin-downable parameter to a clearly-labelled diagnostic
with stated precision, and show failures alongside successes — all squarely good
practice (Gelman's "Bayesian workflow"). The one live risk is *appearance*:
changing a preregistered criterion after it failed invites scrutiny, which is why
the amendment is built around explicit integrity checks and stays gated behind
lodgement.

**(4) Confidence intervals / error presentation? — The method supplies everything;
presentation is partly still to-do, with two honesty points.** Being Bayesian,
every quantity has a full posterior, so we natively have credible intervals for the
timeline (per bin) and for α, plus convergence diagnostics (R-hat, ESS,
divergences).

- **Honesty point A — α's own error bars are *overconfident*.** The recovery grid
  showed that, with lots of data, the model's stated interval for α gets *too
  narrow*. The honest error bar for α is therefore the wider **±0.18** from the
  recovery study, *not* the raw posterior interval from a single fit. Reporting the
  raw interval at face value would understate uncertainty.
- **Honesty point B — RESOLVED (and it's a real limitation).** Shape *point*
  recovery is strong (≈0.998), but the band-calibration check (§4a) shows the
  *uncertainty band* is honest only for smooth timelines; for sharply-peaked
  timelines it is overconfident and degrades at large N (regnal-cluster coverage
  falls to 0.23 at N=50000). So for peaked regimes the reported band understates
  uncertainty and must be widened or explicitly caveated — not presented at face
  value.

Good paper presentation therefore means: timeline figures as a **median line +
shaded credible band** (the field idiom); α as a coarse estimate **with the ±0.18
recovery caveat**; convergence diagnostics reported; and the operating-envelope
limitation stated plainly. The banded figures are Stage-3 work, not yet done.

## 4. Diagnostics commissioned 2026-06-02

### 4a. Does the timeline's credible band have honest coverage? (band calibration)

*(Re-fit of a representative operating-envelope subset on zbook — the grid stored
only the posterior median curve, so the band had to be recomputed.
`runs/2026-06-02-recovery-utility-check/code/band-calibration.py`.)*

**Result (360 fits, 12 cells × 30 reps; zbook, pymc 6.0.1).** Pointwise 95%
coverage of the true `p_gen` (fraction of time-bins where the 95% band contains
the truth; target 0.95):

| shape | α | N=2000 | N=50000 |
|---|---|---|---|
| smooth_growth | 0.3 | 1.00 | 0.99 |
| smooth_growth | 0.7 | 0.99 | 0.99 |
| rise_and_fall | 0.3 | 0.77 | 0.55 |
| rise_and_fall | 0.7 | 0.79 | 0.57 |
| regnal_cluster | 0.3 | 0.89 | **0.23** |
| regnal_cluster | 0.7 | 0.98 | 0.69 |

**Mean coverage: 0.90 at N=2000 → 0.67 at N=50000.**

**The honest verdict is two-sided, and it qualifies the "trust the shape" message
of §2:**

1. **For *smoothly-varying* genuine signals the bands are well-calibrated**
   (≈0.99 at both sample sizes). Where the real timeline is smooth, the reported
   credible band can be taken at face value.
2. **For *sharply-peaked* signals (regnal clustering, rise-and-fall) the bands are
   overconfident — too narrow — and they degrade at large N**, exactly the
   posterior-concentration mechanism that broke α coverage (regnal_cluster falls
   to 0.23 coverage at N=50000). The cause is twofold: the smoothness
   (Gaussian-random-walk) prior on `log p_gen` cannot fully represent sharp
   features, so the posterior concentrates on a slightly-too-smooth curve, and a
   narrow band around it misses the true peaks.

**Consequence for the paper.** The recovered *median* timeline (the point estimate)
remains trustworthy — that is what the Pearson-r shape gate validates, and it is
high throughout. But the **uncertainty band must not be presented at face value
for peaked regimes**: where the genuine signal may be sharply peaked, the band
understates uncertainty and the recovered peaks are likely attenuated. This
matters concretely because the **real corpus does contain sharp regnal clustering**
(AD ~77, ~122, ~212). The honest options are to (i) report band calibration as a
stated limitation and widen/caveat the bands in peaked regions, or (ii) add a
roughness-tolerant prior component — a fit-side change, deferred. Band calibration
is reported as a **diagnostic/limitation, not a new binding gate** (the point
recovery is the gated, primary quantity). Data:
`runs/2026-06-02-recovery-utility-check/outputs/band-calibration-by-cell.csv`.

### 4b. Where does the real corpus sit relative to the α≤0.70 envelope?

*(`runs/2026-06-02-recovery-utility-check/code/real-corpus-convention-fraction.py`;
descriptive convention-mass fraction from the F1+F3 family classifier, the same
definition the model's `p_conv` is built from.)*

- **Corpus-wide convention fraction ≈ 0.65** — *just inside* the 0.70 envelope,
  but with little margin. (F1_round century-templates alone are 59.5% of aoristic
  mass; the corpus is heavily century-templated.)
- **21 of 80 time-bins exceed 0.70, spanning AD ~142–347** — the **late corpus
  sits in the degraded-recovery zone**. Genuine-signal claims for the mid-2nd to
  4th centuries therefore need explicit hedging — and that is often the
  historically richest period (e.g. the third-century crisis).
- An upper-bound sensitivity that also counts broad non-template ("Big") intervals
  as convention puts the corpus-wide fraction at ≈0.85 and most bins above 0.70 —
  a reminder that broad-but-non-aligned datings are their own deconvolution
  challenge.
- Figure: `runs/2026-06-02-recovery-utility-check/outputs/convention-fraction-over-time.png`.
  The dips at the era boundary and at regnal years (AD ~77, ~212) — precisely-dated
  material lowering the local convention fraction — are a sanity check that the
  classifier captures something real.

## 5. Honest caveats — what would make this fully confident

- **It's provisional.** The ~92% figure is a Grid A preview under the new
  criterion; Grid B (letters) is not yet adjudicated; the harness still computes
  the old criterion; the amendment is not lodged; Martin has not reviewed.
- **Simulation ≠ reality.** Recovery-in-simulation is necessary, not sufficient.
  It is empirically anchored (fog patterns and prior come from the real corpus),
  which helps.
- **The safe-zone line bites in the late corpus.** §4b confirms the real corpus
  exceeds α=0.70 across AD ~142–347, so those periods are in the degraded zone.
- **Band calibration (§4a) shows the timeline bands are honest only for smooth
  signals** — overconfident for peaked signals at large N. Reported bands for
  peaked regimes need widening/caveating; a roughness-tolerant prior is the
  deferred fit-side fix.

## 6. Bottom line

The model reliably recovers the **de-fogged *shape* (median timeline)** of
epigraphic activity within the safe zone — the payload the temporal analyses need.
Three honest qualifications: (1) it gives only a **coarse** read on *how much* is
editorial (we lean on the robust descriptive characterisation of convention for
that); (2) it is **untrustworthy where editorial templates dominate — including
much of the late corpus** (real-corpus α exceeds 0.70 across AD ~142–347); and
(3) the **uncertainty band** around the timeline is honest for smooth signals but
**overconfident for sharply-peaked ones at large N**, so peaks are attenuated and
their error bars understated. The approach is principled, literature-grounded, and
aligned with good practice; the outstanding work is presentational (banded figures,
the α caveat, peaked-region band caveats) plus the deferred fit-side options
(roughness-tolerant prior; informed α prior).
