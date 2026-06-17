# §5 H5 — habit-removed residual trajectory (SPEC)

- **Status:** spec + run (Shawn authorised launch 2026-06-17). Exploratory
  (Decision 13 / prereg §5); **no pre-committed thresholds** — descriptive.
- **Author / date:** Claude (Opus 4.8, 1M context), 2026-06-17.
- **Run dir:** `runs/2026-06-17-s5-h5-habit-removed/`.

---

## 1. What H5 is

The naive "does a city's inscription peak match its demographic peak?" is
confounded by the empire-wide **epigraphic habit's** own temporal shape. H5
decomposes each city's trajectory into an *empire-wide habit component* plus a
*city-specific residual trajectory*, and reports the residual + the
**epigraphic-habit lag** (prereg §5, lines 358–364; Decision 13).

## 2. Key realisation — the decomposition already exists

The §5 Layer-A hierarchical model already factors the per-city log-rate:

`log_lam[c,t] = α_g + g_shape[t] + b_u[p] + u_shape[p,t] + b_v[c] + v_shape[c,t]`

So **no new sampling is needed** — H5 is a deterministic read of the Layer-A
posterior (`monolithic-inscription-25y.nc`, on sapphire; 8,000 draws, 16×25y
bins, 50 BC–AD 350, 268 target cities; 35 non-singleton provinces with a `u`
tier):

- **Empire-wide habit component** = `α_g + g_shape[t]` (peak-of-habit = argmax
  `g_shape`).
- **Habit-removed residual trajectory** (shape; level-free, zero-sum over t) =
  `u_shape[p(c),t] + v_shape[c,t]` (province tier folded into the residual;
  singleton-province cities have no `u`, so residual = `v_shape[c,t]`).

## 3. Deliverables

1. **Per-city habit-removed residual trajectories** (median + 95 % band), 268
   cities. [deterministic]
2. **Epigraphic-habit lag** (the registered headline): per city, the offset
   `peak_year(raw lam) − peak_year(residual)`, propagated draw-wise; report the
   per-city distribution and the corpus-wide summary (median lag + spread). The
   empire habit peak year (argmax `g_shape`) is reported alongside — the lag is
   the habit pulling city peaks toward it.
3. **Foundation-date terminus check** (corpus-wide, best-effort): join Hanson
   `Start Date` (`data/hanson2016/hanson2016_cities_oxrep.csv`, by ancient
   toponym) and, for cities founded *within* the envelope (Start Date > 50 BC),
   confirm ~zero raw SPA mass before foundation (analogue of Pompeii's AD-79
   upper terminus). Report match coverage; do not block on unmatched cities.
4. **Independent-peak calibration (bounded set):** note the Layer-B anchors
   (Ostia 2nd-c. apogee; Pompeii AD-79) against their residual peaks.

## 4. Design decisions (made + documented; Shawn can redirect — re-runnable)

- **(i) Habit component = Layer-A `g_shape`** (the within-sample empire
  trajectory), not the h3b mixture-corrected curve — `g_shape` is hierarchically
  coherent with the per-city `u`/`v` residuals (same fit). 
- **(ii) Residual = `u_shape + v_shape`** (remove the empire habit only; keep
  province + city structure as the residual), matching Decision 13's two-way
  "empire habit + city residual".
- **(iii) Lag metric = raw-peak − residual-peak**, per draw, in years (bin
  centres). Level offsets don't move argmax, so the residual peak uses the
  shape only.
- **(iv) Foundation dates = Hanson `Start Date`**, name-joined best-effort;
  terminus check only meaningful for within-envelope foundations.

## 5. Caveats (carry into write-up)

- Exploratory, no thresholds (Decision 13); GPT-5.5 review flagged the design as
  "statistically fragile" — read descriptively.
- The habit component is the *within-sample* (268-city) empire trajectory, a
  proxy for the true empire-wide habit.
- Foundation-date anchors are sparse and name-join-limited; most cities predate
  the envelope so the terminus check applies to a subset.
- N\* = 300 reliability floor carries from Layer A (34/268 reliable).

## 6. Outputs

`outputs/`: `h5-residual-trajectories.nc` (per-city residual + raw median/bands,
peak bins, lag), `h5-summary.json` (habit peak, corpus lag summary, foundation
coverage), figures (empire habit curve; sample residual trajectories; lag
histogram).

## 7. Compute

Sapphire; deterministic transform of the Layer-A posterior — no MCMC. Minutes.
