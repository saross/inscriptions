#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
c10_lib.py — synthetic per-inscription generator + count builders for the C10 test.
===================================================================================

This is the **new** code for the C10 aoristic-Monte-Carlo (aoristic-MC) validity
test (``runs/2026-06-18-c10-validity-test/SPEC.md``). It decides, with ground
truth, whether point-date sampling **destroys** the convention signal the
cross-classified α exists to detect — reading (b) — or whether it reveals a
**genuine** α-fragility — reading (a).

The module imports (does NOT reimplement) the lodged, recovery-validated machinery:

* ``joint_lib`` — ``aligned_indicator`` (the production rule-C convention-typed
  indicator), ``slab_mixture_spa`` (deterministic aoristic box of a slab), the
  ``gaussian_pgen`` genuine-shape helper, ``largest_remainder``, and the envelope
  constants (``N_BINS`` = 80, ``ENV_START`` = −50, ``ENV_END`` = 350, ``BIN_SIZE``
  = 5).
* ``h2_lib`` — ``aoristic_spa`` (the aoristic-mass SPA convention the deconvolution
  basis was built with), ``largest_remainder``, ``load_filtered_lire``, the
  envelope constants, and the binning grid.
* ``refit_lib`` — ``load_library_basis`` (the locked 27-slab production basis +
  the slab ``[lo, hi]`` list), ``adopted_theta_priors`` (the production θ prior),
  ``build_unit_cc_data`` / ``subset_for`` / ``ALIGN_RULE`` for the real-empire arms.

The slab library itself is the locked production artefact
``runs/2026-06-13-cc-production-refit/outputs/production-slab-library.json``: a list
of 27 round-endpoint slabs ``[lo, hi]``. A slab's recorded interval is exactly its
``[lo, hi]``; the convention inscription's TRUE date is Uniform over that support.

==============================================================================
THE LOAD-BEARING GENERATIVE ASSUMPTION (SPEC §2 — the key audit target)
==============================================================================

A **convention** inscription was recorded as a round-number **slab** by an editor
who could not date it precisely:

    its recorded interval = the slab [nb, na] = [lo, hi];
    its TRUE date ~ Uniform(lo, hi).

A **genuine** inscription has a **tight** recorded interval bracketing its true
date, the true date drawn from a smooth activity shape ``p_gen``:

    its TRUE date ~ p_gen   (empire posterior median, or a Gaussian bump);
    its recorded interval = [t − half, t + half]   (tight; ``half`` ~ 2.5 y).

Under this model, point-date sampling ``t_i ~ Uniform(recorded interval)``
**reconstructs the true-date distribution** — which for convention inscriptions
deliberately erases the slab-concentration that α quantifies. The two count
representations therefore measure DIFFERENT things:

* the **aoristic-mass** SPA spreads each inscription's mass over its recorded
  interval → convention mass stays piled on the round-number slab → α recoverable;
* the **point-date** SPA collapses each inscription to one sampled year → for
  convention inscriptions that year is Uniform(slab), so the slab structure is
  washed back into the smooth genuine shape → α destroyed (reading (b)).

Alignment is NOT hand-set. Each synthetic inscription's recorded ``[nb, na]`` is
fed to the REAL ``joint_lib.aligned_indicator(rule="C")``, so the aligned /
non-aligned split is produced exactly as in production.

Author / Date — Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief,
2026-06-18. UK/Australian English; Oxford comma. BUILD-ONLY: this module performs
NO MCMC — it generates synthetic data and integer count vectors. Fits live in the
runner (``run_c10.py``), executed only after audit sign-off.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Wire the lodged modules (import, do NOT modify).                              #
# --------------------------------------------------------------------------- #
PROJECT_ROOT = Path("/home/shawn/Code/inscriptions")
H2_DIR = PROJECT_ROOT / "runs" / "2026-06-07-h2.1-launch-prep" / "code"
JOINT_DIR = PROJECT_ROOT / "runs" / "2026-06-09-joint-identifiability" / "code"
REFIT_DIR = PROJECT_ROOT / "runs" / "2026-06-13-cc-production-refit" / "code"
for _d in (H2_DIR, JOINT_DIR, REFIT_DIR):
    if str(_d) not in sys.path:
        sys.path.insert(0, str(_d))

import h2_lib as H  # noqa: E402
import joint_lib as J  # noqa: E402
import refit_lib as R  # noqa: E402

# --------------------------------------------------------------------------- #
# Envelope constants — single source of truth via the lodged modules.           #
# Asserted equal across the three modules so a silent drift would fail-fast.     #
# --------------------------------------------------------------------------- #
N_BINS = H.N_BINS  # 80
ENV_START = H.ENV_START  # −50
ENV_END = H.ENV_END  # 350
BIN_SIZE = H.BIN_SIZE  # 5
BIN_EDGES = H.BIN_EDGES
BIN_CENTRES = H.BIN_CENTRES
assert (J.N_BINS, J.ENV_START, J.ENV_END, J.BIN_SIZE) == (
    N_BINS, ENV_START, ENV_END, BIN_SIZE), "envelope drift between h2_lib and joint_lib"

# Path to the empire posterior p_gen (the preferred smooth genuine shape, SPEC §3b).
EMPIRE_PGEN_NPZ = (
    PROJECT_ROOT / "runs" / "2026-06-13-cc-production-refit" / "outputs"
    / "posterior-draws" / "empire-aggregate-pgen.npz")

# Default tight half-width for the GENUINE recorded interval (SPEC §3b: "±2.5 y").
# half = 2.5 → recorded width 5 y = exactly one 5-year bin. half = 0 → the [t, t]
# year-precise case. Made a parameter (``genuine_half_width``) so the audit can vary it.
GENUINE_HALF_WIDTH_DEFAULT = 2.5


# =========================================================================== #
# Genuine smooth shape p_gen (SPEC §3b: empire posterior, else a Gaussian bump). #
# =========================================================================== #
def load_empire_pgen() -> np.ndarray:
    """The empire posterior-median ``p_gen`` (length ``N_BINS``), renormalised to 1.

    This is the preferred smooth GENUINE shape (SPEC §3b: "use the empire posterior
    ``p_gen`` if available"). Read from the locked production artefact
    ``empire-aggregate-pgen.npz`` (``p_gen_median_raw``); renormalised because the
    per-bin median of a simplex sums to ≈ 0.999, not exactly 1 (the
    median-of-simplex artefact ``h2_lib.fit_unit`` documents).
    """
    if not EMPIRE_PGEN_NPZ.exists():
        raise FileNotFoundError(f"empire p_gen artefact missing: {EMPIRE_PGEN_NPZ}")
    arr = np.load(EMPIRE_PGEN_NPZ)
    pgm = np.asarray(arr["p_gen_median_raw"], dtype=float)
    if pgm.shape != (N_BINS,):
        raise ValueError(f"empire p_gen has shape {pgm.shape}, expected ({N_BINS},)")
    s = float(pgm.sum())
    if s <= 0:
        raise ValueError("empire p_gen has non-positive sum")
    return pgm / s


def resolve_pgen(pgen_spec: str | np.ndarray) -> tuple[np.ndarray, str]:
    """Resolve the GENUINE shape ``p_gen`` from a spec into a (vector, label).

    Parameters
    ----------
    pgen_spec : str | np.ndarray
        * ``"empire"`` — the empire posterior-median ``p_gen`` (preferred; SPEC §3b).
        * ``"gauss"`` — a fallback Gaussian bump centred in the active AD 100–300
          window (``joint_lib.gaussian_pgen(200, 60)``), used when the empire
          artefact is unavailable or the audit wants a clean synthetic control.
        * a length-``N_BINS`` array — supplied directly (renormalised to 1).

    Returns
    -------
    (p_gen, label) — the normalised shape and a human-readable provenance label.
    """
    if isinstance(pgen_spec, np.ndarray):
        v = np.asarray(pgen_spec, dtype=float)
        if v.shape != (N_BINS,):
            raise ValueError(f"supplied p_gen shape {v.shape} != ({N_BINS},)")
        if v.min() < 0 or v.sum() <= 0:
            raise ValueError("supplied p_gen must be non-negative with positive sum")
        return v / v.sum(), "supplied-array"
    if pgen_spec == "empire":
        return load_empire_pgen(), "empire-posterior-median"
    if pgen_spec == "gauss":
        # Gaussian bump in the active window (the genuine activity the corpus shows).
        return J.gaussian_pgen(200.0, 60.0), "gaussian-bump(mu=200,sigma=60)"
    raise ValueError(f"unknown pgen_spec {pgen_spec!r} (use 'empire', 'gauss', or array)")


# =========================================================================== #
# Slab mixture weights (SPEC §3b: "draw a slab S from the slab-library mixture   #
# weights").                                                                    #
# =========================================================================== #
def slab_mixture_weights(slabs: list[list[int]],
                         weights: np.ndarray | None = None) -> np.ndarray:
    """Normalised categorical weights over the slab-library rows.

    The locked production slab library stores NO per-slab mixture weights — it is a
    list of 27 round-endpoint slabs ``[lo, hi]`` (``library_slabs``). The SPEC calls
    for drawing a convention inscription's slab "from the slab-library mixture
    weights"; absent stored weights, the **honest, audit-flagged default is UNIFORM**
    over the 27 slabs (every round-number bracket equally likely to be the editor's
    choice). A non-uniform vector may be supplied (e.g. an empirical slab-frequency
    profile) — it is renormalised to a categorical.

    AUDIT NOTE: uniform-over-slabs is a *modelling choice*, not data. It spreads
    convention mass broadly across the envelope (many slabs are wide). The recovery
    test's logic does NOT depend on the exact weights — it depends only on convention
    inscriptions being recorded AS slabs (mass on the bracket) while their true date
    is Uniform(slab). Vary ``weights`` in the audit to confirm robustness.
    """
    n = len(slabs)
    if weights is None:
        return np.ones(n, dtype=float) / n
    w = np.asarray(weights, dtype=float)
    if w.shape != (n,):
        raise ValueError(f"slab weights shape {w.shape} != ({n},)")
    if w.min() < 0 or w.sum() <= 0:
        raise ValueError("slab weights must be non-negative with positive sum")
    return w / w.sum()


# =========================================================================== #
# THE SYNTHETIC PER-INSCRIPTION GENERATOR (SPEC §2 / §3b — the crux).            #
# =========================================================================== #
def generate_inscriptions(alpha_true: float, n: int, seed: int,
                          slabs: list[list[int]],
                          p_gen: np.ndarray,
                          slab_weights: np.ndarray | None = None,
                          genuine_half_width: float = GENUINE_HALF_WIDTH_DEFAULT,
                          ) -> pd.DataFrame:
    """Generate ``n`` synthetic inscriptions with a planted convention fraction α.

    This is the **new code** the whole test rests on; it implements SPEC §2
    verbatim. Per inscription:

        type_i ~ Bernoulli(alpha_true)          # 1 = convention, 0 = genuine

    **CONVENTION** (``type_i == 1``) — recorded as a round-number slab:
        S       ~ Categorical(slab_weights)     # draw a slab from the library
        nb, na  = S's [lo, hi]                  # recorded interval = the slab
        t_true  ~ Uniform(lo, hi)               # TRUE date uniform over the slab

    **GENUINE** (``type_i == 0``) — tight bracket around a smooth activity shape:
        t_true  ~ p_gen                         # TRUE date from the smooth shape
        nb, na  = [t_true − half, t_true + half]  # TIGHT recorded interval (±half y)

    The genuine ``p_gen`` is sampled on the 5-year bin grid (a bin centre is drawn
    with probability ``p_gen``, then jittered Uniform within the bin) so the true
    date is continuous within the active window; ``half = 0`` gives the year-precise
    ``[t, t]`` case, ``half = 2.5`` (default) gives a one-bin-wide recorded bracket.

    Alignment is assigned AFTERWARDS by the real ``joint_lib.aligned_indicator(rule
    ="C")`` on the recorded ``[nb, na]`` (NOT hand-set) — so the synthetic
    aligned/non-aligned split is produced exactly as production does it. The indicator
    needs integer ``nb`` / ``na`` / ``date_range``; recorded bounds are rounded to the
    nearest integer year (the LIRE corpus records integer years; ``load_filtered_lire``
    casts to ``int``).

    Parameters
    ----------
    alpha_true : float
        The planted convention fraction (the ground truth to recover), in [0, 1].
    n : int
        Number of synthetic inscriptions.
    seed : int
        RNG seed (deterministic; the runner derives per-(α, seed) seeds).
    slabs : list[list[int]]
        The slab library's ``[lo, hi]`` rows (from ``refit_lib.load_library_basis``).
    p_gen : (N_BINS,) float array
        The smooth GENUINE true-date shape (sums to 1; from ``resolve_pgen``).
    slab_weights : (n_slabs,) array, optional
        Categorical weights over slabs (default uniform; see ``slab_mixture_weights``).
    genuine_half_width : float
        Half-width of the GENUINE tight recorded bracket in years (default 2.5).

    Returns
    -------
    pandas.DataFrame with one row per inscription and columns:
        ``type``        — "convention" | "genuine"
        ``t_true``      — the true date (float year)
        ``nb`` / ``na`` — the recorded interval bounds (int years)
        ``date_range``  — na − nb (int; the aligned_indicator covariate)
        ``aligned``     — the real rule-C aligned indicator on (nb, na, date_range)
    """
    if not (0.0 <= alpha_true <= 1.0):
        raise ValueError(f"alpha_true {alpha_true} not in [0, 1]")
    if n <= 0:
        raise ValueError(f"n must be positive, got {n}")
    p_gen = np.asarray(p_gen, dtype=float)
    if p_gen.shape != (N_BINS,):
        raise ValueError(f"p_gen shape {p_gen.shape} != ({N_BINS},)")
    if genuine_half_width < 0:
        raise ValueError("genuine_half_width must be >= 0")

    rng = np.random.default_rng(seed)
    slab_w = slab_mixture_weights(slabs, slab_weights)
    slab_lo = np.array([s[0] for s in slabs], dtype=float)
    slab_hi = np.array([s[1] for s in slabs], dtype=float)
    pgen_norm = p_gen / p_gen.sum()

    # ---- type assignment: type_i ~ Bernoulli(alpha_true) ----
    is_conv = rng.random(n) < alpha_true  # True = convention
    n_conv = int(is_conv.sum())
    n_gen = n - n_conv

    t_true = np.empty(n, dtype=float)
    nb = np.empty(n, dtype=float)
    na = np.empty(n, dtype=float)

    # ---- CONVENTION inscriptions: recorded interval = slab; t_true ~ Uniform(slab) --
    if n_conv > 0:
        slab_idx = rng.choice(len(slabs), size=n_conv, p=slab_w)
        lo = slab_lo[slab_idx]
        hi = slab_hi[slab_idx]
        nb[is_conv] = lo
        na[is_conv] = hi
        # TRUE date uniform over the slab's [lo, hi] support (SPEC §2).
        t_true[is_conv] = rng.uniform(lo, hi)

    # ---- GENUINE inscriptions: t_true ~ p_gen; recorded interval TIGHT ----
    if n_gen > 0:
        # Sample a bin index with probability p_gen, then jitter Uniform within the
        # 5-year bin so the true date is continuous within the active window.
        bin_choice = rng.choice(N_BINS, size=n_gen, p=pgen_norm)
        within = rng.uniform(0.0, BIN_SIZE, size=n_gen)
        tg = BIN_EDGES[bin_choice] + within
        t_true[~is_conv] = tg
        # TIGHT recorded bracket around the true date (±genuine_half_width years).
        nb[~is_conv] = tg - genuine_half_width
        na[~is_conv] = tg + genuine_half_width

    # ---- recorded bounds → integer years (LIRE records integer not_before/after) ---
    # Round to the nearest integer year and order-correct (na >= nb) defensively.
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
    })
    # ---- alignment assigned by the REAL production indicator (NOT hand-set) ----
    df["aligned"] = J.aligned_indicator(df, rule=R.ALIGN_RULE)
    return df


# =========================================================================== #
# COUNT REPRESENTATION (i): aoristic-MASS largest-remainder (deconvolution input). #
# =========================================================================== #
def mass_cc_counts(df: pd.DataFrame) -> dict[str, Any]:
    """Aoristic-MASS cross-classified counts from synthetic inscriptions (SPEC §3b).

    The deconvolution input: each inscription's unit mass is spread Uniformly over
    its RECORDED interval (``h2_lib.aoristic_spa``), separately for the aligned and
    non-aligned subsets, then largest-remainder-rounded to integers. This is exactly
    ``refit_lib.build_unit_cc_data`` applied to the synthetic frame (it consumes the
    same ``nb`` / ``na`` / ``aligned_indicator`` machinery) — convention mass stays
    piled on the round-number slab, so α is recoverable.

    Honours the k_cc / n_rows invariants in aoristic-EFFECTIVE counts:
    ``k_cc == y_aligned.sum()`` and ``n_rows == y_aligned.sum() + y_nonaligned.sum()``
    (asserted by ``build_unit_cc_data``'s downstream consumer; re-asserted here).

    Returns a dict with ``y_aligned``, ``y_nonaligned``, ``k`` (= k_cc), ``n_rows``,
    plus the raw-row descriptive fractions — the exact shape
    ``build_model_cross_classified`` consumes.
    """
    data = R.build_unit_cc_data(df)
    ya = np.asarray(data["y_aligned"], dtype="int64")
    yn = np.asarray(data["y_nonaligned"], dtype="int64")
    k = int(data["k"])
    n_rows = int(data["n_rows"])
    # Re-assert the lumping/thinning invariants the model requires.
    assert int(ya.sum()) == k, f"mass: y_aligned.sum()={int(ya.sum())} != k={k}"
    assert int(ya.sum() + yn.sum()) == n_rows, (
        f"mass: aligned+non-aligned={int(ya.sum() + yn.sum())} != n_rows={n_rows}")
    return {"y_aligned": ya, "y_nonaligned": yn, "k": k, "n_rows": n_rows,
            "n_rows_raw": int(data["n_rows_raw"]),
            "n_aligned_raw": int(data["n_aligned_raw"]),
            "row_aligned_frac": float(data["row_aligned_frac"]),
            "mass_aligned_frac": float(data["mass_aligned_frac"])}


# =========================================================================== #
# COUNT REPRESENTATION (ii): POINT-DATE per realisation (the aoristic-MC input).  #
# =========================================================================== #
def point_date_cc_counts(df: pd.DataFrame, rng: np.random.Generator,
                         amask: np.ndarray | None = None,
                         ) -> tuple[np.ndarray, np.ndarray, int, int]:
    """One point-date realisation of cross-classified counts (SPEC §3b / C10).

    Samples ``t_i ~ Uniform(recorded interval)`` per inscription, clips to the
    envelope, bins to the 5-year grid WITHIN each FIXED alignment subset — the exact
    method the lodged C10 driver uses
    (``run_supp.aoristic_mc_realisation``; reproduced here so the test arm matches
    production bit-for-method, NOT imported because that lives in the concurrent
    supp-wave dir we must not couple to).

    Alignment membership is FIXED (it depends on the recorded interval + rule C, not
    the sampled date), so ``k_cc`` (aligned inscription count) and ``n_rows`` (total)
    are held CONSTANT across realisations: each inscription deposits exactly one count
    into exactly one bin of its own subset.

    For CONVENTION inscriptions the sampled date is Uniform(slab) — i.e. it
    reconstructs the convention's TRUE date and erases the slab concentration; this is
    the destruction mechanism reading (b) predicts.

    Parameters
    ----------
    df : pandas.DataFrame
        Inscriptions with recorded ``nb`` / ``na`` columns.
    rng : numpy.random.Generator
        Seeded generator (per-realisation seed handled by the caller).
    amask : (N,) bool array, optional
        The FIXED aligned indicator. Defaults to ``df["aligned"]`` (present on
        synthetic frames from ``generate_inscriptions``); supply it explicitly for a
        REAL corpus subset (which carries no ``aligned`` column) so the rule-C split
        is the production one — used by the 1c point-collapse arm.

    Returns ``(y_aligned, y_nonaligned, k_cc, n_rows)`` with
    ``y_aligned.sum() == k_cc`` and ``y_aligned.sum() + y_nonaligned.sum() == n_rows``.
    """
    nb = df["nb"].to_numpy().astype(float)
    na = df["na"].to_numpy().astype(float)
    if amask is None:
        amask = df["aligned"].to_numpy().astype(bool)
    else:
        amask = np.asarray(amask, dtype=bool)
    k_cc = int(amask.sum())
    n_rows = int(len(df))

    # Sample one point date per inscription (half-open [lo, hi); degenerate [t, t]
    # returns t exactly — the year-precise case). VERBATIM convention from
    # run_supp.aoristic_mc_realisation.
    t = np.where(na > nb, rng.uniform(nb, na), nb)
    t = np.clip(t, ENV_START, ENV_END - 1e-9)
    bin_idx = np.floor((t - ENV_START) / BIN_SIZE).astype(int)
    bin_idx = np.clip(bin_idx, 0, N_BINS - 1)

    y_aligned = np.bincount(bin_idx[amask], minlength=N_BINS).astype("int64")
    y_nonaligned = np.bincount(bin_idx[~amask], minlength=N_BINS).astype("int64")
    # Invariants (the M2 guard; DM/Multinomial silently returns −inf if violated).
    assert int(y_aligned.sum()) == k_cc, (
        f"point-date: y_aligned.sum()={int(y_aligned.sum())} != k_cc={k_cc}")
    assert int(y_aligned.sum() + y_nonaligned.sum()) == n_rows, (
        f"point-date: aligned+non-aligned={int(y_aligned.sum() + y_nonaligned.sum())} "
        f"!= n_rows={n_rows}")
    return y_aligned, y_nonaligned, k_cc, n_rows


# =========================================================================== #
# Diagnostics shared by 1a (real data) and the synthetic SPA inspection.         #
# =========================================================================== #
def aoristic_mass_spa(df: pd.DataFrame, mask: np.ndarray | None = None) -> np.ndarray:
    """Normalised aoristic-MASS SPA of the (optionally masked) recorded intervals.

    Uses ``h2_lib.aoristic_spa`` (the basis-construction convention). Normalised to
    sum 1 (an SPA shape for the L1/round-boundary diagnostics). Returns a flat-zero
    vector if the subset is empty.
    """
    sub = df if mask is None else df.loc[mask]
    spa = H.aoristic_spa(sub["nb"].to_numpy(), sub["na"].to_numpy())
    s = float(spa.sum())
    return spa / s if s > 0 else spa


def point_date_spa(df: pd.DataFrame, rng: np.random.Generator,
                   mask: np.ndarray | None = None) -> np.ndarray:
    """Normalised POINT-DATE SPA: one sampled year per inscription, binned.

    Samples ``t_i ~ Uniform(recorded interval)`` (the C10 point-date scheme),
    restricted to the optional subset ``mask``, and normalises to sum 1. Used by the
    1a diagnostic to contrast the point-date SPA shape against the aoristic-mass one.
    """
    sub = df if mask is None else df.loc[mask]
    nb = sub["nb"].to_numpy().astype(float)
    na = sub["na"].to_numpy().astype(float)
    if len(nb) == 0:
        return np.zeros(N_BINS)
    t = np.where(na > nb, rng.uniform(nb, na), nb)
    t = np.clip(t, ENV_START, ENV_END - 1e-9)
    bin_idx = np.clip(np.floor((t - ENV_START) / BIN_SIZE).astype(int), 0, N_BINS - 1)
    spa = np.bincount(bin_idx, minlength=N_BINS).astype(float)
    s = float(spa.sum())
    return spa / s if s > 0 else spa


# --- round-number boundary bins (50 BC, AD 0, 50, 100, ...) for metric (ii) ---
def round_boundary_bins(step: int = 50) -> np.ndarray:
    """Bin indices whose 5-year bin contains a round-number boundary (every ``step``
    years: −50, 0, 50, 100, ...). A boundary year ``y`` falls in bin
    ``floor((y − ENV_START) / BIN_SIZE)``. Returns the unique in-range indices."""
    years = np.arange(ENV_START, ENV_END + 1, step)
    idx = np.floor((years - ENV_START) / BIN_SIZE).astype(int)
    return np.unique(idx[(idx >= 0) & (idx < N_BINS)])


def l1_to_nearest_slab_row(spa: np.ndarray, basis: np.ndarray) -> dict[str, Any]:
    """Minimum L1 distance from an SPA shape to any single slab-library row (metric i).

    Low = slab-like (the SPA sits near one round-number bracket). The fixed
    ``production-slab-library.json`` basis (each row a normalised aoristic box) is the
    reference; both ``spa`` and the rows sum to 1, so L1 ∈ [0, 2].
    """
    if spa.sum() <= 0:
        return {"l1_min": float("nan"), "nearest_row": -1}
    p = spa / spa.sum()
    l1 = np.abs(basis - p[None, :]).sum(axis=1)
    j = int(np.argmin(l1))
    return {"l1_min": float(l1[j]), "nearest_row": j}


def round_boundary_mass_fraction(spa: np.ndarray, step: int = 50,
                                 within_bins: int = 1) -> dict[str, Any]:
    """Fraction of SPA mass within ``within_bins`` bins of a round-number boundary
    (metric ii). Compared against the uniform expectation (the same windowed bin
    count over ``N_BINS``) — slab-like SPAs concentrate mass on round boundaries
    above uniform; flat point-date SPAs sit near it.
    """
    if spa.sum() <= 0:
        return {"frac": float("nan"), "uniform_expectation": float("nan"),
                "ratio": float("nan"), "n_window_bins": 0}
    p = spa / spa.sum()
    centres = round_boundary_bins(step)
    window = set()
    for c in centres:
        for d in range(-within_bins, within_bins + 1):
            b = c + d
            if 0 <= b < N_BINS:
                window.add(b)
    window_idx = np.array(sorted(window), dtype=int)
    frac = float(p[window_idx].sum())
    uniform_exp = float(len(window_idx) / N_BINS)
    return {"frac": frac, "uniform_expectation": uniform_exp,
            "ratio": (frac / uniform_exp) if uniform_exp > 0 else float("nan"),
            "n_window_bins": int(len(window_idx))}


def best_fit_slab_mixture_weight(spa: np.ndarray, basis: np.ndarray) -> dict[str, Any]:
    """Best-fit non-negative slab-mixture weight: how much of the SPA the slab library
    explains (metric iii).

    Solves ``min_w ||basis^T w − p||_2`` subject to ``w >= 0`` (non-negative least
    squares), then reports the total explained weight ``sum(w)`` (the fraction of the
    SPA mass the library accounts for; ≈ 1 when the SPA is a slab mixture, lower when
    it is a smooth non-slab shape) and the residual L2. Uses ``scipy.optimize.nnls``.
    """
    from scipy.optimize import nnls

    if spa.sum() <= 0:
        return {"total_weight": float("nan"), "residual_l2": float("nan")}
    p = spa / spa.sum()
    # nnls solves min ||A x − b||_2, x >= 0; A = basis^T (N_BINS × n_slabs).
    a_mat = basis.T
    w, rnorm = nnls(a_mat, p)
    recon = a_mat @ w
    return {"total_weight": float(w.sum()), "residual_l2": float(rnorm),
            "recon_l1": float(np.abs(recon - p).sum())}
