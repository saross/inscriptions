#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
c10_ii_lib.py — realism-graded generator variants for the C10 follow-up "(ii)".
================================================================================

This is the **new** code for the C10 follow-up (the "(ii)" wave) that resolves the
puzzle the first validity test left open. It IMPORTS and EXTENDS — never modifies —
the lodged, recovery-validated machinery (``joint_lib``, ``refit_lib``, ``h2_lib``)
and the first-wave ``c10_lib`` (the §2 idealised generator + count builders +
arm-fitters).

THE PUZZLE (what (ii) resolves)
-------------------------------
The first validity test (``run_c10.py`` / ``VALIDITY-REPORT.md``) found:

* **1b (synthetic, idealised §2 generator):** the point-date aoristic-MC RECOVERS
  the planted α just as well as the mass arm — verdict **(a)**.
* **1c (real empire):** point-collapse α = **0.100** vs mass-preserving α = **0.615**
  — a large divergence the synthetic did **NOT** reproduce.

So the idealised §2 generator is missing whatever REAL-DATA feature drives the
collapse. (ii) finds it by GRADING the realism of the generator and asking, for
each variant: *does the point-date arm now DIVERGE from the mass arm (and/or
collapse toward the ~0.1 floor), reproducing the 1c gap?*

WHERE THE IDEALISATIONS LIVE (the load-bearing mechanism — design crux)
-----------------------------------------------------------------------
Point-date sampling draws ``t ~ Uniform(RECORDED interval)``. It NEVER uses the
latent true date. Therefore — for a convention inscription whose recorded interval
IS the slab — both arms see a flat-over-slab shape *regardless* of the true-date
distribution. The idealisations that could drive the collapse therefore live in the
**RECORDED-interval / observed dimensions**, NOT in the latent true-date shape.

The first-wave (R0) generator idealises the recorded dimension two ways:

1. **Interval widths.** Convention = exact (wide, round) library slabs; genuine =
   tight ±2.5 y (one 5-year bin). Real data is very different: the real NON-aligned
   subset carries a broad spread of widths — many WIDE non-round intervals (e.g.
   59, 78, 129 y), not just tight ones. A point-date sample of a wide non-aligned
   interval spreads as broadly as a wide aligned one, so the TEMPORAL CONTRAST
   between the two alignment subsets (which is what the cross-classified α reads)
   is washed out. → **variant R1 (PRIMARY hypothesis).**
2. **θ separation.** R0 gives P(aligned|convention) = 1.000, P(aligned|genuine) =
   0.000 — a PERFECTLY separable alignment signal. Production θ is
   θ_conv ≈ 0.93, θ_gen ≈ 0.025 (``refit_lib.adopted_theta_priors``): ~7 % of
   convention inscriptions are recorded non-aligned and ~2.5 % of genuine ARE
   aligned. That cross-contamination puts convention mass into the non-aligned
   subset and genuine mass into the aligned subset, again eroding the contrast.
   → **variant R2.**
3. **In-slab true-date shape** (the originally-named variant). R0 draws a convention
   true date Uniform(slab). A NON-uniform in-slab shape is the obvious "realism"
   knob — but by the mechanism above it should make NO difference to recovery,
   because neither arm uses the true date (both sample/spread over the RECORDED
   interval). → **variant R3, included as a CONFIRMATORY NULL** documenting the
   mechanism.

We also support combinations (at least **R1+R2**), because the real driver may be
joint.

R0 == THE EXISTING IDEALISED GENERATOR (parameterisation invariant)
-------------------------------------------------------------------
``generate_inscriptions_variant(..., variant="R0")`` delegates **verbatim** to the
first-wave ``c10_lib.generate_inscriptions`` (same RNG seed, same arguments). So R0
is byte-identical to the generator the first wave used — the realism knobs are
strictly additive, and R0 reproduces the (a)-verdict baseline.

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief,
2026-06-19. UK/Australian English; Oxford comma. BUILD-ONLY: this module performs
NO MCMC — it generates synthetic data and integer count vectors only. Fits live in
the runner (``run_c10_ii.py``), executed only after audit sign-off.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Wire the lodged modules + the first-wave c10_lib (import, do NOT modify).      #
# c10_lib already inserts h2_lib / joint_lib / refit_lib onto sys.path.         #
# --------------------------------------------------------------------------- #
CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import c10_lib as C  # noqa: E402  (also wires h2_lib / joint_lib / refit_lib)
import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402
import refit_lib as R  # noqa: E402

# Envelope constants — single source of truth via c10_lib (which asserts no drift).
N_BINS = C.N_BINS
ENV_START = C.ENV_START
ENV_END = C.ENV_END
BIN_SIZE = C.BIN_SIZE
BIN_EDGES = C.BIN_EDGES

# The rule-C family width sets (round F1 / periodic F3) — used to confirm that an
# R1-placed convention interval lands on an aligned width, and to keep R2's
# convention-misrecorded / genuine-aligned brackets consistent with their target
# alignment. Imported from the lodged classifier's source of truth (h2_lib).
F1_WIDTHS = sorted(H.F1_WIDTHS)   # {24, 49, 99, 149, 199, 299}
F3_WIDTHS = sorted(H.F3_WIDTHS)   # {19, 29, 39}
TIGHT_MAX = H.TIGHT_MAX           # 4

# The four realism variants + the baseline.
VARIANTS = ("R0", "R1", "R2", "R3", "R1+R2")


# =========================================================================== #
# Real empire RECORDED-WIDTH distributions, by alignment subset (for R1).        #
# =========================================================================== #
@dataclass
class RealWidthDist:
    """Empirical per-subset recorded-width (``date_range``) distribution from the
    REAL empire corpus, used by R1 to draw realistic interval widths.

    Stored as the observed ``(width, count)`` histogram for each subset so a width
    can be drawn by inverse-CDF sampling that exactly reproduces the empirical
    distribution (no kernel smoothing — the data ARE discrete integer widths).

    Attributes
    ----------
    aligned_widths, aligned_probs : the support and categorical probabilities of the
        aligned-subset ``date_range`` (the convention-ish widths: round F1/F3 widths
        dominate, median ≈ 99 y).
    nonaligned_widths, nonaligned_probs : same for the non-aligned subset (the
        genuine-ish widths: a broad spread, many WIDE non-round intervals, median
        ≈ 41 y) — the feature R1 is built to inject.
    n_aligned, n_nonaligned : the source subset sizes (for the provenance record).
    """

    aligned_widths: np.ndarray
    aligned_probs: np.ndarray
    nonaligned_widths: np.ndarray
    nonaligned_probs: np.ndarray
    n_aligned: int
    n_nonaligned: int

    def sample_aligned(self, rng: np.random.Generator, size: int) -> np.ndarray:
        """Draw ``size`` recorded widths from the empirical ALIGNED-subset histogram."""
        return rng.choice(self.aligned_widths, size=size, p=self.aligned_probs)

    def sample_nonaligned(self, rng: np.random.Generator, size: int) -> np.ndarray:
        """Draw ``size`` recorded widths from the empirical NON-aligned-subset histogram."""
        return rng.choice(self.nonaligned_widths, size=size, p=self.nonaligned_probs)


def real_empire_width_dist(unit_name: str = "empire-aggregate") -> RealWidthDist:
    """Build the per-subset recorded-width distribution from the REAL empire corpus.

    Exactly the SPEC path: ``h2_lib.load_filtered_lire`` → the empire subset
    (``refit_lib.subset_for``) → ``joint_lib.aligned_indicator(rule="C")`` → the
    per-subset distribution of ``date_range = na − nb``. This is the SAME data the
    1a / 1c real-empire arms use, so R1's injected widths match the real corpus the
    puzzle came from.

    NO MCMC; pure data profiling. Returns a :class:`RealWidthDist`.
    """
    df = H.load_filtered_lire()
    latin = H.latin_provinces()
    units = {u["name"]: u for u in R.enumerate_refit_units()}
    if unit_name not in units:
        raise ValueError(f"unknown unit {unit_name!r}")
    sub = R.subset_for(df, units[unit_name], latin)
    amask = J.aligned_indicator(sub, rule=R.ALIGN_RULE).astype(bool)
    dr = sub["date_range"].to_numpy().astype(int)

    def _hist(widths: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        vals, cnts = np.unique(widths, return_counts=True)
        return vals.astype(int), (cnts / cnts.sum()).astype(float)

    aw, ap = _hist(dr[amask])
    nw, npb = _hist(dr[~amask])
    return RealWidthDist(
        aligned_widths=aw, aligned_probs=ap,
        nonaligned_widths=nw, nonaligned_probs=npb,
        n_aligned=int(amask.sum()), n_nonaligned=int((~amask).sum()),
    )


# =========================================================================== #
# Variant configuration.                                                        #
# =========================================================================== #
@dataclass
class VariantConfig:
    """Switches controlling which realism idealisations are RELAXED in a variant.

    Each flag defaults to the R0-idealised value; setting one ON relaxes that
    idealisation. The named variants (:func:`variant_config`) are convenience
    presets; the dataclass is exposed so the audit / runner can build arbitrary
    combinations.

    r1_real_widths : if True, draw each synthetic inscription's RECORDED-interval
        WIDTH from the real empire per-subset width distribution (R1, PRIMARY).
    r2_theta_contamination : if True, assign a realistic ALIGNMENT mix consistent
        with θ_conv ≈ 0.93 / θ_gen ≈ 0.025 (R2) instead of the perfect 1.0 / 0.0.
    r3_nonuniform_true_date : if True, draw the convention in-slab TRUE date from a
        non-uniform (edge-weighted Beta) shape instead of Uniform(slab) (R3,
        CONFIRMATORY NULL — predicted to NOT change recovery).
    """

    r1_real_widths: bool = False
    r2_theta_contamination: bool = False
    r3_nonuniform_true_date: bool = False


def variant_config(variant: str) -> VariantConfig:
    """Map a named variant in :data:`VARIANTS` to its :class:`VariantConfig`."""
    presets = {
        "R0": VariantConfig(),
        "R1": VariantConfig(r1_real_widths=True),
        "R2": VariantConfig(r2_theta_contamination=True),
        "R3": VariantConfig(r3_nonuniform_true_date=True),
        "R1+R2": VariantConfig(r1_real_widths=True, r2_theta_contamination=True),
    }
    if variant not in presets:
        raise ValueError(f"unknown variant {variant!r}; choose from {VARIANTS}")
    return presets[variant]


# =========================================================================== #
# Recorded-interval PLACEMENT helpers (the R1 / R2 interval-emission logic).      #
# =========================================================================== #
def _nearest_aligned_width(w: np.ndarray) -> np.ndarray:
    """Snap an array of widths to the nearest rule-C ALIGNED family width.

    A convention inscription must be RECORDED as an aligned interval (rule C). Rule C
    credits round F1 widths (24, 49, 99, …) and periodic F3 widths (19, 29, 39) when
    BOTH endpoints sit on the 25-y (F1) or 10-y (F3) grid, OR a ``Big`` slab (width
    ≥ 49) whose endpoints are both on the 25-y grid. To honour the SPEC's "centred on
    a slab/round position" while sampling a REAL aligned width, we snap the sampled
    width to the nearest F1-or-F3 family width — a value guaranteed alignable with
    round endpoints. (The real aligned subset is itself dominated by exactly these
    widths: 99, 199, 49, 149, 299, 29, 39, … — see :func:`real_empire_width_dist` —
    so the snap is small and rarely binds.)
    """
    family = np.array(sorted(set(F1_WIDTHS) | set(F3_WIDTHS)), dtype=float)
    w = np.asarray(w, dtype=float)
    idx = np.abs(w[:, None] - family[None, :]).argmin(axis=1)
    return family[idx].astype(int)


# Lowest common multiple of the two round-residue grids rule C uses (25 for F1/Big,
# 10 for F3). The set of lower-endpoint residues mod 50 that align a given width is
# periodic with period 50, so a per-width residue lookup keyed on ``nb % 50`` is exact.
_ALIGN_GRID_PERIOD = 50


def _aligned_nb_residues(width: int) -> np.ndarray:
    """The set of lower-endpoint residues ``nb % 50`` that make a width rule-C aligned.

    Probes the REAL ``joint_lib.aligned_indicator(rule="C")`` directly (rather than
    re-deriving the residue arithmetic by hand) for every residue ``r ∈ [0, 50)`` with
    ``nb = r``, ``na = r + width``. Because rule-C alignment of ``[nb, nb + width]``
    depends on ``nb`` only through ``nb % 25`` and ``nb % 10`` — both of which repeat
    with period ``lcm(25, 10) = 50`` — this 0..49 probe captures the full residue set
    for ANY integer ``nb`` of that residue. Returns the sorted ascending residues.

    Built from the indicator so it stays correct if the lodged rule-C definition ever
    changes (it would not silently drift back to the buggy 25-grid assumption).
    """
    nb = np.arange(_ALIGN_GRID_PERIOD, dtype=int)
    na = nb + int(width)
    dr = np.full(_ALIGN_GRID_PERIOD, int(width), dtype=int)
    al = J.aligned_indicator(
        pd.DataFrame({"nb": nb, "na": na, "date_range": dr}), rule=R.ALIGN_RULE)
    return nb[np.asarray(al, dtype=bool)]


def _place_aligned_interval(width: np.ndarray, t_anchor: np.ndarray,
                            rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Place an ALIGNED (convention-ish) recorded interval of a given width.

    Given an aligned family ``width`` and an anchor year ``t_anchor`` (the convention
    true date), choose a lower endpoint ``nb`` so that the recorded interval
    ``[nb, nb + width]`` is rule-C ALIGNED *and* brackets the anchor
    (``nb ≤ t_anchor ≤ nb + width``) — so the slab the editor chose contains the
    inscription's true date, exactly as in R0 where ``t_true ~ Uniform(slab)`` ⊂ slab.

    Why NOT just a 25-y grid (the original bug)
    -------------------------------------------
    The first implementation placed ``nb`` on a multiple of 25. That is WRONG for two
    reasons against the real rule-C residue rule
    (``round_aligned(x, mod)`` ≡ ``x % mod ∈ {0, 1, mod − 1}``):

    * **F3 widths (19, 29, 39)** need BOTH endpoints round on the *10-y* grid
      (``x % 10 ∈ {0, 1, 9}``). An ODD multiple of 25 (75, 125, 175, …) has
      ``nb % 10 == 5``, which fails — so every F3-width convention placed on an odd
      25-multiple LEAKED to non-aligned, dragging realised θ_conv below 1.0.
    * The audit's suggested "snap to multiples of 50" is itself wrong: a 50-grid is
      coarser than the F1/F3 widths < 50 (24, 49, 19, 29, 39), so it cannot always
      bracket the anchor.

    The correct placement (verified against the REAL indicator)
    -----------------------------------------------------------
    For each width we read the EXACT set of valid lower-endpoint residues ``nb % 50``
    from :func:`_aligned_nb_residues` (i.e. from ``joint_lib.aligned_indicator`` — not
    a hand re-derivation). The valid residues are dense enough that for EVERY
    aligned width the largest gap between consecutive valid residues is ≤ 24 ≤ width,
    so the largest valid ``nb ≤ t_anchor`` always satisfies ``nb + width ≥ t_anchor``
    — the slab brackets the anchor. We pick that ``nb``: the valid lower endpoint
    closest below the anchor. (Verified at ~40 k rows: realised θ_conv = 1.000,
    bracket rate = 1.000 — see ``C10-FOLLOWUP-NOTES.md``.)
    """
    width = np.asarray(width, dtype=int)
    t_anchor = np.asarray(t_anchor, dtype=float)
    nb = np.empty(len(width), dtype=int)
    ti = np.floor(t_anchor).astype(int)   # integer year at or below the anchor
    # Group by distinct width so the per-width residue lookup is computed once each.
    for w in np.unique(width):
        m = width == w
        res = _aligned_nb_residues(int(w))           # ascending residues in [0, 50)
        tt = t_anchor[m]
        ti_w = ti[m]
        # For each valid residue r, the largest nb ≤ ti_w with nb % 50 == r is
        # nb_r = ti_w − ((ti_w − r) mod 50). Among residues whose slab brackets the
        # anchor (nb ≤ t ≤ nb + w), take the one CLOSEST below the anchor (largest nb).
        cand = ti_w[:, None] - np.mod(ti_w[:, None] - res[None, :], _ALIGN_GRID_PERIOD)
        brackets = (cand <= tt[:, None]) & (cand + int(w) >= tt[:, None])
        cand_ok = np.where(brackets, cand, np.iinfo(np.int64).min)
        nb[m] = cand_ok.max(axis=1)
    na = nb + width
    return nb.astype(int), na.astype(int)


# Lower-endpoint shifts (added to a 25-grid base) that make ``nb`` fail BOTH the 25-y
# and 10-y round-residue tests for EITHER parity of the 25-grid multiple — so rule C
# fails on the lower endpoint, hence on the whole interval, for ANY width. Derived from
# the real residue rule and verified empirically (0 % leak to aligned) — see the M2
# note in ``C10-FOLLOWUP-NOTES.md``. The old set {3, …, 22} included shifts (e.g. 4, 5,
# 9, 10) whose ``nb`` could still land round on one grid for one base parity, leaking
# ~0.1 % of non-aligned-intent rows to aligned.
_NONALIGNED_SHIFTS = np.array([2, 3, 7, 8, 12, 13, 17, 18, 22, 23], dtype=int)


def _place_nonaligned_interval(width: np.ndarray, t_anchor: np.ndarray,
                               rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Place a NON-aligned (genuine-ish) recorded interval of a given width.

    Brackets the genuine true date ``t_anchor`` with a recorded interval of the
    sampled ``width``, OFFSET so the interval is non-round (fails rule C). The anchor
    sits at a uniform position inside the interval; the lower endpoint is then snapped
    to the 25-y grid and shifted off it so ``round_aligned`` fails on the LOWER
    endpoint, classifying the interval non-aligned for ANY width.

    The non-alignment GUARANTEE (corrected)
    ---------------------------------------
    Rule-C alignment of ``[nb, na]`` requires the LOWER endpoint to be round on the
    relevant grid: the 25-y grid (``nb % 25 ∈ {0, 1, 24}``) for F1/Big widths, or the
    10-y grid (``nb % 10 ∈ {0, 1, 9}``) for the F3 widths 19/29/39. If ``nb`` fails
    BOTH grids, the interval is non-aligned regardless of width or upper endpoint.

    The shift is therefore drawn from :data:`_NONALIGNED_SHIFTS` =
    ``{2, 3, 7, 8, 12, 13, 17, 18, 22, 23}`` — the shifts ``s`` for which
    ``(25k + s) % 25 ∉ {0, 1, 24}`` AND ``(25k + s) % 10 ∉ {0, 1, 9}`` hold for BOTH
    parities of ``k`` (note ``25k % 10`` cycles {0, 5}, so the shift must dodge the
    round residues for both). The previous set ``{3, …, 22}`` did NOT — shifts like 4,
    5, 9, 10 could leave ``nb`` round on one grid for one base parity, leaking a small
    fraction of non-aligned-intent rows back to aligned.

    Tight widths (≤ TIGHT_MAX) are left as-is — they are ``Tight`` → non-aligned
    regardless of endpoint, reproducing the genuine tight brackets (a tight width < 19
    can never be an F1/F3/Big aligned family anyway).
    """
    width = np.asarray(width, dtype=int)
    t_anchor = np.asarray(t_anchor, dtype=float)
    offset = rng.uniform(0.0, 1.0, size=len(width)) * width
    nb = np.rint(t_anchor - offset).astype(int)
    na = nb + width
    # For non-tight widths, force an off-grid lower endpoint (so rule C fails) using a
    # shift that dodges BOTH the 25-y and 10-y round residues for either base parity.
    non_tight = width > TIGHT_MAX
    if non_tight.any():
        # snap nb to the 25-grid then add a guaranteed-off-both-grids shift.
        base = (np.round(nb[non_tight] / 25.0) * 25.0).astype(int)
        shift = rng.choice(_NONALIGNED_SHIFTS, size=int(non_tight.sum()))
        nb_off = base + shift
        nb[non_tight] = nb_off
        na[non_tight] = nb_off + width[non_tight]
    return nb.astype(int), na.astype(int)


def _nonuniform_inslab_true_date(lo: np.ndarray, hi: np.ndarray,
                                 rng: np.random.Generator) -> np.ndarray:
    """Draw a convention TRUE date from a NON-uniform (edge-weighted) in-slab shape.

    R3's realism knob: instead of ``t_true ~ Uniform(slab)`` (R0), draw from a
    Beta(0.5, 0.5) (U-shaped, mass piled at the slab edges) scaled to ``[lo, hi]``.
    This is the most adversarial departure from uniform-in-slab. By the mechanism
    (neither arm uses the true date) recovery should be UNCHANGED — R3 is the
    confirmatory null. Returns one true date per slab.
    """
    lo = np.asarray(lo, dtype=float)
    hi = np.asarray(hi, dtype=float)
    u = rng.beta(0.5, 0.5, size=len(lo))   # U-shaped on [0, 1]
    return lo + u * (hi - lo)


# =========================================================================== #
# THE REALISM-GRADED GENERATOR (R0 == c10_lib; R1/R2/R3/combinations new).        #
# =========================================================================== #
def generate_inscriptions_variant(
        variant: str,
        alpha_true: float, n: int, seed: int,
        slabs: list[list[int]],
        p_gen: np.ndarray,
        *,
        width_dist: RealWidthDist | None = None,
        theta_conv: float | None = None,
        theta_gen: float | None = None,
        slab_weights: np.ndarray | None = None,
        genuine_half_width: float = C.GENUINE_HALF_WIDTH_DEFAULT,
        ) -> pd.DataFrame:
    """Generate ``n`` synthetic inscriptions for a named realism variant.

    The planted-α machinery is IDENTICAL across variants: ``type_i ~
    Bernoulli(alpha_true)`` (1 = convention, 0 = genuine). The variants change ONLY
    the recorded-interval emission and (R3) the in-slab true-date shape:

    * **R0** — delegates VERBATIM to ``c10_lib.generate_inscriptions`` (the §2
      idealised generator). Same seed, same arguments → byte-identical to the first
      wave. ``width_dist`` / ``theta_*`` are ignored.
    * **R1** — recorded WIDTHS drawn from the real empire per-subset width
      distribution (``width_dist``): convention widths from the aligned-subset
      histogram (snapped to the nearest aligned family width, centred on a 25-grid
      slab position bracketing the true date); genuine widths from the non-aligned-
      subset histogram (placed off-grid around the true date). Requires ``width_dist``.
    * **R2** — alignment assigned as the realistic θ mix: a convention inscription is
      recorded ALIGNED with probability ``theta_conv`` (≈ 0.93) — else recorded
      non-aligned (a wide non-round bracket); a genuine inscription is recorded
      ALIGNED with probability ``theta_gen`` (≈ 0.025) — else tight non-aligned. The
      recorded interval is made CONSISTENT with the assigned alignment. Requires
      ``theta_conv`` / ``theta_gen``.
    * **R3** — convention in-slab true date drawn U-shaped (Beta(0.5, 0.5)) instead
      of Uniform(slab); recorded interval otherwise as R0. Confirmatory null.
    * **R1+R2** — both R1 widths AND R2 θ-contamination (requires both
      ``width_dist`` and ``theta_*``).

    Alignment is ALWAYS assigned at the end by the REAL
    ``joint_lib.aligned_indicator(rule="C")`` on the recorded ``[nb, na]`` (never
    hand-set) — so the aligned / non-aligned SPLIT is produced exactly as production
    does it. The R2 "assign alignment" step controls only HOW the recorded interval
    is BUILT (aligned-shaped vs non-aligned-shaped); the indicator then re-derives the
    label from that interval, and the two agree by construction (verified in the
    runner's invariant check).

    Returns a DataFrame with the same columns as
    ``c10_lib.generate_inscriptions`` (``type``, ``t_true``, ``nb``, ``na``,
    ``date_range``, ``aligned``), plus ``recorded_as`` (the INTENDED alignment shape:
    "aligned" | "nonaligned") for the audit / θ-realisation record.
    """
    if variant not in VARIANTS:
        raise ValueError(f"unknown variant {variant!r}; choose from {VARIANTS}")
    cfg = variant_config(variant)

    # ---- R0: delegate VERBATIM to the first-wave idealised generator ----
    if variant == "R0":
        df = C.generate_inscriptions(
            alpha_true, n, seed, slabs, p_gen,
            slab_weights=slab_weights, genuine_half_width=genuine_half_width)
        # R0 records convention AS the slab (aligned), genuine AS tight (non-aligned).
        df["recorded_as"] = np.where(df["type"] == "convention", "aligned", "nonaligned")
        return df

    # ---- R3: CLEAN confirmatory NULL — recorded interval IDENTICAL to R0; only the
    #          latent convention TRUE date changes (Uniform(slab) → U-shaped Beta). ----
    # Building R3 through the general R1/R2 path would RE-PLACE the recorded interval
    # (its own RNG draw of nb/na), so the recorded columns would NOT match R0 and the
    # "null" would silently confound a recorded-interval change with the true-date
    # change. To isolate the true-date shape we delegate the WHOLE recorded interval to
    # R0 (byte-identical nb / na / date_range / aligned) and override ONLY t_true for
    # convention rows. Because R0 records a convention's interval AS its slab, the
    # recorded [nb, na] IS the slab [lo, hi]; redrawing the within-slab true date over
    # [nb, na] is exactly the R3 idealisation knob with the recorded interval frozen.
    if variant == "R3":
        df = C.generate_inscriptions(
            alpha_true, n, seed, slabs, p_gen,
            slab_weights=slab_weights, genuine_half_width=genuine_half_width)
        df["recorded_as"] = np.where(df["type"] == "convention", "aligned", "nonaligned")
        conv = (df["type"] == "convention").to_numpy()
        if conv.any():
            # A SEPARATE generator (seed offset) draws the U-shaped within-slab true
            # date, so R0's recorded-interval RNG stream is left untouched.
            rng_r3 = np.random.default_rng(seed + 777)
            lo = df.loc[conv, "nb"].to_numpy(dtype=float)
            hi = df.loc[conv, "na"].to_numpy(dtype=float)
            new_t = _nonuniform_inslab_true_date(lo, hi, rng_r3)
            df.loc[conv, "t_true"] = new_t
        return df

    if not (0.0 <= alpha_true <= 1.0):
        raise ValueError(f"alpha_true {alpha_true} not in [0, 1]")
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")
    p_gen = np.asarray(p_gen, dtype=float)
    if p_gen.shape != (N_BINS,):
        raise ValueError(f"p_gen shape {p_gen.shape} != ({N_BINS},)")
    if cfg.r1_real_widths and width_dist is None:
        raise ValueError(f"variant {variant!r} needs width_dist (R1 width sampling)")
    if cfg.r2_theta_contamination and (theta_conv is None or theta_gen is None):
        raise ValueError(f"variant {variant!r} needs theta_conv / theta_gen (R2 mix)")

    rng = np.random.default_rng(seed)
    slab_w = C.slab_mixture_weights(slabs, slab_weights)
    slab_lo = np.array([s[0] for s in slabs], dtype=float)
    slab_hi = np.array([s[1] for s in slabs], dtype=float)
    pgen_norm = p_gen / p_gen.sum()

    # ---- type assignment: type_i ~ Bernoulli(alpha_true) (UNCHANGED) ----
    is_conv = rng.random(n) < alpha_true
    n_conv = int(is_conv.sum())
    n_gen = n - n_conv

    # ---- latent TRUE dates (per the §2 semantics; unchanged by R1/R2) ----
    t_true = np.empty(n, dtype=float)
    conv_lo = conv_hi = None
    if n_conv > 0:
        slab_idx = rng.choice(len(slabs), size=n_conv, p=slab_w)
        conv_lo = slab_lo[slab_idx]
        conv_hi = slab_hi[slab_idx]
        # The NAMED "R3" variant is intercepted above (clean null: recorded interval
        # frozen to R0). This branch only fires for an AD-HOC VariantConfig that turns
        # r3_nonuniform_true_date ON together with R1/R2 — where re-placement of the
        # recorded interval is intended, so the within-slab redraw rides the main RNG.
        if cfg.r3_nonuniform_true_date:
            t_true[is_conv] = _nonuniform_inslab_true_date(conv_lo, conv_hi, rng)
        else:
            t_true[is_conv] = rng.uniform(conv_lo, conv_hi)   # Uniform(slab) — R0 default
    if n_gen > 0:
        bin_choice = rng.choice(N_BINS, size=n_gen, p=pgen_norm)
        within = rng.uniform(0.0, BIN_SIZE, size=n_gen)
        t_true[~is_conv] = BIN_EDGES[bin_choice] + within

    # ---- recorded-alignment INTENT (R2 contaminates; else type-pure) ----
    # "recorded_as" is whether the editor recorded the inscription with an ALIGNED
    # (round-slab) interval or a NON-aligned one. R0/R1/R3 record convention aligned,
    # genuine non-aligned (the pure θ_conv = 1, θ_gen = 0 case). R2 flips a fraction:
    # a convention recorded non-aligned with prob (1 − θ_conv); a genuine recorded
    # aligned with prob θ_gen.
    recorded_aligned = is_conv.copy()
    if cfg.r2_theta_contamination:
        u = rng.random(n)
        # convention recorded aligned with prob theta_conv (else non-aligned).
        recorded_aligned[is_conv] = u[is_conv] < float(theta_conv)
        # genuine recorded aligned with prob theta_gen (else non-aligned).
        recorded_aligned[~is_conv] = u[~is_conv] < float(theta_gen)

    # ---- recorded WIDTHS (R1 draws real; else the idealised widths) ----
    # Width is keyed to the INTENDED alignment shape (so a θ-contaminated convention
    # recorded non-aligned gets a non-aligned-style width, and vice versa).
    width = np.empty(n, dtype=int)
    n_rec_al = int(recorded_aligned.sum())
    n_rec_non = n - n_rec_al
    if cfg.r1_real_widths:
        if n_rec_al > 0:
            width[recorded_aligned] = _nearest_aligned_width(
                width_dist.sample_aligned(rng, n_rec_al))
        if n_rec_non > 0:
            width[~recorded_aligned] = width_dist.sample_nonaligned(rng, n_rec_non)
    else:
        # Idealised widths: aligned-recorded → the slab's own width (for convention)
        # or a default aligned family width (for a θ-contaminated genuine recorded
        # aligned); non-aligned-recorded → tight 2*half (for genuine) or a wide
        # non-round default (for a θ-contaminated convention recorded non-aligned).
        DEFAULT_ALIGNED_WIDTH = 99    # the modal real aligned width (F1)
        DEFAULT_WIDE_NONALIGNED = 60  # a wide non-round genuine-subset width
        tight_w = int(round(2 * genuine_half_width))
        width[:] = tight_w
        width[recorded_aligned] = DEFAULT_ALIGNED_WIDTH
        # convention recorded aligned uses its OWN slab width (kept round + wide).
        conv_recorded_aligned = is_conv & recorded_aligned
        if conv_recorded_aligned.any() and conv_lo is not None:
            # map the per-convention slab width onto the convention rows.
            cw = (conv_hi - conv_lo).astype(int)
            # place cw into the convention slots in order.
            width_conv = np.empty(n_conv, dtype=int)
            width_conv[:] = cw
            width[is_conv] = np.where(
                recorded_aligned[is_conv], width_conv, DEFAULT_WIDE_NONALIGNED)

    # ---- PLACE the recorded interval per intended alignment shape ----
    nb = np.empty(n, dtype=int)
    na = np.empty(n, dtype=int)
    if n_rec_al > 0:
        nb[recorded_aligned], na[recorded_aligned] = _place_aligned_interval(
            width[recorded_aligned], t_true[recorded_aligned], rng)
    if n_rec_non > 0:
        nb[~recorded_aligned], na[~recorded_aligned] = _place_nonaligned_interval(
            width[~recorded_aligned], t_true[~recorded_aligned], rng)

    # ---- order-correct + integer years (LIRE records integer not_before/after) ----
    nb_i = np.rint(nb).astype(int)
    na_i = np.rint(na).astype(int)
    swap = na_i < nb_i
    nb_i[swap], na_i[swap] = na_i[swap], nb_i[swap]
    date_range = (na_i - nb_i).astype(int)

    df = pd.DataFrame({
        "type": np.where(is_conv, "convention", "genuine"),
        "t_true": t_true,
        "nb": nb_i,
        "na": na_i,
        "date_range": date_range,
        "recorded_as": np.where(recorded_aligned, "aligned", "nonaligned"),
    })
    # Alignment ASSIGNED by the REAL production indicator (NOT hand-set).
    df["aligned"] = J.aligned_indicator(df, rule=R.ALIGN_RULE)
    return df


# =========================================================================== #
# Realised-θ diagnostics (for the per-variant record).                          #
# =========================================================================== #
def realised_theta(df: pd.DataFrame) -> dict[str, float]:
    """Observed P(aligned | type) in a generated frame (the realised θ separation).

    Reads the REAL ``aligned`` indicator against the latent ``type`` — so it reports
    what θ_conv / θ_gen the recorded intervals actually produced (R0 ≈ 1.0 / 0.0; R2
    should land near the production 0.93 / 0.025). Diagnostic only.
    """
    is_conv = (df["type"] == "convention").to_numpy()
    aligned = df["aligned"].to_numpy().astype(bool)
    n_conv = int(is_conv.sum())
    n_gen = int((~is_conv).sum())
    return {
        "theta_conv_realised": float(aligned[is_conv].mean()) if n_conv else float("nan"),
        "theta_gen_realised": float(aligned[~is_conv].mean()) if n_gen else float("nan"),
        "n_conv": n_conv, "n_gen": n_gen,
        "row_aligned_frac": float(aligned.mean()),
    }
