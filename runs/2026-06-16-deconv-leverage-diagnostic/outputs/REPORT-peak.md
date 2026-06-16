# Does the deconvolution move the peak — and would that shift a peak-window scaling?

> Cheap province-level proxy (29 deconvolved units) for Shawn's follow-up to the
> cumulative-scaling result. Generated from `peak-shift-diagnostic.json`. Exploratory;
> the definitive city-level peak-window test needs a per-city deconvolution.

## Two findings

**1. The deconvolution DOES move the peak** (as expected — a peak is a shape statistic,
not mass-conserved). 25-year window: median genuine/raw peak change
**+60%** (25 units rise, 1
fall, of 26); median absolute peak-year shift
**18 years**. This is exactly the reshaping (TV 0.24–0.50)
that the cumulative count was blind to.

**2. But the peak shift is ~flat across size** —
log(genuine/raw peak) vs log(population): Spearman -0.00,
Theil-Sen slope -0.005; vs log(n_eff): Spearman
-0.17, Theil-Sen -0.161.

## What this means for a peak-window Hanson test

Because the peak shift does not trend with size, a peak-window scaling exponent would be ~unchanged by the deconvolution — the deconvolution moves every units peak but not the size-gradient. So even the peak variant inherits the cumulative results robustness, at least at this province-level proxy.

The 5-year window tells the same story (median change +70%,
Theil-Sen vs logpop +0.026).

## Caveats

- **GRW peak-attenuation.** The deconvolution's smoothness prior attenuates sharp peaks
  (C8 / Amdt 01 §A5.7), so genuine peak heights are propagated over the posterior (median +
  95% band in the JSON), not point-estimated. A downward median ratio is partly model
  smoothing, not only convention-removal — read the direction with that in mind.
- **Province-level proxy.** A peak is a per-city quantity; these 29 units are mostly
  province/region-level. The definitive peak-window scaling test needs a per-city
  deconvolution (same dependency as D13). This proxy indicates low
  expected payoff for that build on the peak variant.
- **Not preregistered** — the peak-window scaling test is a tertiary/future-work item.

## Reproduce
```bash
uv run python runs/2026-06-16-deconv-leverage-diagnostic/code/peak_shift_diagnostic.py
```
