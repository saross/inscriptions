# §5 H5 — habit-removed residual trajectory — RESULTS

- **Status:** COMPLETE (exploratory; Decision 13 / prereg §5; no thresholds).
- **Run:** sapphire, 2026-06-17; deterministic read of the Layer-A posterior
  (no MCMC). `code/h5_habit_removed.py`; log `run.log`.

---

## 1. Empire-wide epigraphic habit

The empire-wide habit component (`g_shape`) peaks at **AD 187.5** (bin
[175, 200) — late-Antonine/Severan), consistent with the known epigraphic-habit
curve (MacMullen) and the h3b "hump". This is the temporal shape every city's
raw trajectory is partly inheriting. Figure: `outputs/h5-empire-habit.png`.

## 2. The epigraphic-habit lag

Per city, lag = peak-year(raw `lam`) − peak-year(habit-removed residual),
draw-wise.

- **Corpus median lag ≈ 0 yr** (all cities and reliable-only), **IQR [0, 50] yr**,
  fraction-positive 0.48.
- **Read:** there is *no systematic directional* habit lag in the corpus median,
  but the habit shifts *individual* cities' apparent peaks by up to ~one or two
  25-year bins (IQR to 50 yr). For data-rich (reliable, N≥300) cities the city's
  own signal dominates, so raw ≈ residual peak; the habit confound bites hardest
  on small-N cities, which partial-pool toward the AD-188 habit. Figure:
  `outputs/h5-habit-lag-hist.png`.

## 3. Foundation-date terminus validation

Hanson `Start Date` name-joined to all **268 cities** (clean match); **99** are
founded *within* the envelope (Start Date > 50 BC) and so bind.

- **Median pre-foundation inscription mass = 0.07 %** — essentially zero: the
  Layer-A trajectories respect foundation termini corpus-wide (the lower-terminus
  analogue of Pompeii's AD-79 upper terminus).
- **Notable exceptions are archaeologically sensible:** the worst offenders are
  frontier *military* sites — Corstopitum/Corbridge (Start 200, 59 %), Corinium
  Dobunnorum/Cirencester (100, 30 %), Luguvalium/Carlisle (100, 27 %),
  Centumcellae (106, 26 %), Lauriacum (191, 17 %), Argentoratum/Strasbourg
  (80, 17 %) — where epigraphy from the earlier military presence predates the
  *town's* Barrington foundation date. A real signal (military-before-civilian),
  not a model error; flag descriptively.

## 4. Deliverables

`outputs/`: `h5-residual-trajectories.nc` (per-city residual + raw median/bands,
raw & residual peak bins, habit-lag with CI, reliability flag; empire habit
curve), `h5-summary.json`, figures (`h5-empire-habit.png`,
`h5-residual-samples.png`, `h5-habit-lag-hist.png`).

## 5. Caveats

Exploratory, no thresholds (Decision 13; GPT-5.5 flagged the design fragile —
read descriptively). Habit = within-sample (268-city) empire trajectory.
Foundation anchors limited to within-envelope foundations. N\*=300 floor (34/268
reliable).

## 6. Bottom line

The empire habit peaks ~AD 188; removing it reveals **no systematic corpus lag
but real ±50-year per-city shifts** (habit-dominated small-N cities most
affected), and the trajectories pass a corpus-wide foundation-terminus check
(0.07 % pre-foundation mass) bar archaeologically-explicable frontier-military
exceptions.
