#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
figtheme.py — shared matplotlib visual language for the key-findings figure set.
================================================================================

One theme module for all 13 figures (build spec
``runs/2026-06-20-figures/spec.md``). It fixes — in ONE place, so the set is
visually coherent and a restyle is a one-file edit:

* **rcParams** — a serif journal font (sized for legibility when a figure is
  shrunk to single-column width), thin spines, light grids, vector-friendly text.
* **Dimensions** — single-column (89 mm) and full-width (180 mm) canvases (the
  "mixed" decision, Shawn 2026-06-20: simple figures single-column, multi-panel
  figures full-width).
* **Palette** — the fixed two-frame encoding (empire/all-provinces = *context*,
  Latin-minus-Roma = *primary*) as an Okabe–Ito colourblind-safe pair; sequential
  maps stay viridis/cividis; a qualitative Okabe–Ito list for categories.
* **Encoding conventions** — corrected (genuine) = solid + saturated; uncorrected
  (raw aoristic) = muted + dashed; 95 % uncertainty as a translucent ribbon /
  fan / caterpillar interval (spec §1).
* **Save helper** — writes each figure to ``outputs/figXX-*.{pdf,png}`` (vector
  PDF for the journal + a 300-dpi PNG preview), with a consistent tight bbox.

Import surface (used by every ``figNN_*.py`` script)::

    import figtheme as T
    T.apply()                                  # set rcParams (call once)
    fig, ax = T.figure_1col()                  # or figure_2col(...)
    ax.plot(..., **T.GENUINE)                  # corrected style
    ax.plot(..., **T.RAW)                      # uncorrected style
    T.band(ax, x, lo, hi, color=T.EMPIRE)      # 95 % ribbon
    T.save(fig, "fig01-deconvolution-before-after")

Author / Date
-------------
Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-20.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------- #
# Output location — the figures run's own outputs/ dir (sibling of code/).      #
# --------------------------------------------------------------------------- #
CODE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = CODE_DIR.parent / "outputs"

# --------------------------------------------------------------------------- #
# Canvas dimensions (inches). Target journal: Journal of Archaeological Method  #
# and Theory (JAMT, Springer). Standard Springer Nature artwork widths —        #
# single column 84 mm, full/double 174 mm (CONFIRM against the live JAMT        #
# guidelines; the page is auth-gated). 1 inch = 25.4 mm.                        #
# --------------------------------------------------------------------------- #
MM = 1.0 / 25.4
WIDTH_1COL = 84.0 * MM    # ~3.31 in — single-column figures
WIDTH_2COL = 174.0 * MM   # ~6.85 in — full-width figures (F2, F3, F4, F6, F13)

# Default golden-ratio heights; individual figures override as needed.
_GOLDEN = 0.618

# --------------------------------------------------------------------------- #
# Palette — Okabe & Ito (2008) colourblind-safe qualitative set.                #
# https://jfly.uni-koeln.de/color/  (the eight-colour CUD palette).            #
# --------------------------------------------------------------------------- #
OKABE_ITO = {
    "black": "#000000",
    "orange": "#E69F00",
    "skyblue": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
    "grey": "#666666",
}

# The fixed two-frame encoding (Shawn 2026-06-20). Used IDENTICALLY across the
# whole set so a colour always means the same frame.
EMPIRE = OKABE_ITO["blue"]        # empire / all-provinces = analytical CONTEXT
LATIN = OKABE_ITO["vermillion"]   # Latin-minus-Roma = the PRIMARY diagnostic unit
NEUTRAL = OKABE_ITO["grey"]       # raw/uncorrected, reference lines, de-emphasis

FRAME_COLOUR = {
    "empire": EMPIRE,
    "latin": LATIN,
    "all-provinces": EMPIRE,
    "context": EMPIRE,
    "primary": LATIN,
}

# Ordered qualitative cycle for categorical series (avoids yellow on white).
QUALITATIVE = [
    OKABE_ITO["blue"],
    OKABE_ITO["vermillion"],
    OKABE_ITO["green"],
    OKABE_ITO["orange"],
    OKABE_ITO["purple"],
    OKABE_ITO["skyblue"],
    OKABE_ITO["black"],
]

# Sequential maps (spec §1): viridis (general), cividis (the most CVD-robust).
SEQ_CMAP = "viridis"
SEQ_CMAP_CVD = "cividis"

# --------------------------------------------------------------------------- #
# Line / marker style conventions (spec §1).                                   #
#   corrected (genuine) -> solid, saturated, full alpha                        #
#   uncorrected (raw)   -> muted (grey), dashed, lighter                       #
# Spread these into a plot call: ``ax.plot(x, y, **T.GENUINE)``.               #
# --------------------------------------------------------------------------- #
GENUINE = {"linestyle": "-", "linewidth": 1.6, "color": OKABE_ITO["black"],
           "alpha": 1.0, "zorder": 5}
RAW = {"linestyle": "--", "linewidth": 1.2, "color": NEUTRAL,
       "alpha": 0.85, "zorder": 3}

# Default translucency for 95 % uncertainty ribbons / fans.
BAND_ALPHA = 0.22


def apply() -> None:
    """Install the shared rcParams. Idempotent; call once at the top of a script.

    Sizes are tuned so text stays legible when a single-column figure is printed
    at ~84 mm. A SANS-SERIF family is requested (JAMT / Springer require Helvetica
    or Arial for figure lettering), with robust fallbacks (Nimbus Sans / DejaVu
    Sans always ship on Linux / with matplotlib).
    """
    mpl.rcParams.update({
        # --- fonts: sans-serif (Springer figure requirement) ----------------
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "Nimbus Sans",
                            "DejaVu Sans"],
        "mathtext.fontset": "dejavusans",
        "font.size": 9.0,
        "axes.titlesize": 9.5,
        "axes.labelsize": 9.0,
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 8.0,
        "legend.fontsize": 8.0,
        "figure.titlesize": 10.0,
        # --- spines / ticks: thin, outward, de-cluttered --------------------
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        # --- grid: light horizontal guide only ------------------------------
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": "#CCCCCC",
        "grid.linewidth": 0.5,
        "grid.alpha": 0.6,
        # --- colour cycle ---------------------------------------------------
        "axes.prop_cycle": mpl.cycler(color=QUALITATIVE),
        # --- legend ---------------------------------------------------------
        "legend.frameon": False,
        "legend.handlelength": 1.8,
        "legend.borderaxespad": 0.3,
        # --- layout / output: vector-friendly, tight -----------------------
        # Raster preview at 600 dpi = Springer "combination art" spec; the
        # vector PDF is the submission artefact (resolution-independent).
        "figure.dpi": 120,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,   # embed TrueType (editable text in the PDF)
        "ps.fonttype": 42,
    })


# --------------------------------------------------------------------------- #
# Canvas factories.                                                            #
# --------------------------------------------------------------------------- #
def figure_1col(height_ratio: float = _GOLDEN, **kw):
    """A single-column figure (≈89 mm wide). ``height = WIDTH_1COL * ratio``."""
    fig, ax = plt.subplots(
        figsize=(WIDTH_1COL, WIDTH_1COL * height_ratio),
        constrained_layout=True, **kw)
    return fig, ax


def figure_2col(height_ratio: float = 0.5, nrows: int = 1, ncols: int = 1, **kw):
    """A full-width figure (≈180 mm wide), optionally a panel grid.

    Args:
        height_ratio: total height as a fraction of the full width.
        nrows, ncols: panel grid (``plt.subplots`` arguments).

    Returns:
        ``(fig, axes)`` from ``plt.subplots`` (``axes`` is an array if multi-panel).
    """
    fig, axes = plt.subplots(
        nrows=nrows, ncols=ncols,
        figsize=(WIDTH_2COL, WIDTH_2COL * height_ratio),
        constrained_layout=True, **kw)
    return fig, axes


def custom(width: float, height: float, nrows: int = 1, ncols: int = 1, **kw):
    """An explicitly-sized figure (inches) — for atlases / tall caterpillars."""
    fig, axes = plt.subplots(
        nrows=nrows, ncols=ncols, figsize=(width, height),
        constrained_layout=True, **kw)
    return fig, axes


# --------------------------------------------------------------------------- #
# Encoding helpers.                                                            #
# --------------------------------------------------------------------------- #
def band(ax, x, lo, hi, color: str, alpha: float = BAND_ALPHA,
         label: str | None = None, zorder: int = 2, **kw):
    """Fill a 95 % uncertainty ribbon between ``lo`` and ``hi`` over ``x``."""
    return ax.fill_between(x, lo, hi, color=color, alpha=alpha,
                           linewidth=0, label=label, zorder=zorder, **kw)


def zero_line(ax, orient: str = "h", value: float = 0.0, **kw):
    """A thin reference line at ``value`` (horizontal by default).

    Used wherever "the interval should sit above/below 0" is the visual point
    (F6 capital contrast, F7 between-province slope, F11 orthogonality axes).
    """
    style = {"color": NEUTRAL, "linewidth": 0.8, "linestyle": (0, (4, 3)),
             "alpha": 0.8, "zorder": 1}
    style.update(kw)
    if orient == "h":
        return ax.axhline(value, **style)
    return ax.axvline(value, **style)


def bc_ad_label(year: float) -> str:
    """Format an envelope year as a BC/AD label (Shawn's standing preference —
    BC/AD, never BCE/CE). The grid uses astronomical years (0 = 1 BC); the
    boundary tick at 0 is labelled ``"AD 1"`` (the start of the era), within a
    year of the true 1 BC/AD 1 turn — immaterial at axis scale.

    ``-50 -> "50 BC"``, ``0 -> "AD 1"``, ``200 -> "AD 200"``.
    """
    y = int(round(year))
    if y < 0:
        return f"{-y} BC"
    if y == 0:
        return "AD 1"
    return f"AD {y}"


def year_axis(ax, ticks=(-50, 0, 100, 200, 300), xlabel: str = "Year") -> None:
    """Apply the shared BC/AD x-axis to an SPD figure (F1–F4, F13).

    The "AD" prefix appears only ONCE — on the first AD tick (the BC/AD
    boundary) — to avoid repeating "AD" across the axis (Shawn 2026-06-20). BC
    ticks keep their "BC" suffix; later AD ticks are bare numbers. Assumes ticks
    are in ascending order.
    """
    ticks = list(ticks)
    labels, first_ad = [], True
    for t in ticks:
        y = int(round(t))
        if y < 0:
            labels.append(f"{-y} BC")
        else:
            yy = 1 if y == 0 else y          # the boundary tick reads "AD 1"
            labels.append(f"AD {yy}" if first_ad else f"{yy}")
            first_ad = False
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    ax.set_xlabel(xlabel)


def panel_tag(ax, tag: str, x: float = -0.02, y: float = 1.02, **kw):
    """Stamp a panel label (``"(a)"`` …) at the top-left of an axis."""
    style = {"fontsize": 9.5, "fontweight": "bold", "va": "bottom",
             "ha": "right", "transform": ax.transAxes}
    style.update(kw)
    return ax.text(x, y, tag, **style)


# --------------------------------------------------------------------------- #
# Save.                                                                        #
# --------------------------------------------------------------------------- #
def save(fig, stem: str, *, outdir: Path | None = None, close: bool = True) -> dict:
    """Write ``fig`` to both a vector PDF and a 300-dpi PNG preview.

    Args:
        fig: the figure.
        stem: filename stem, e.g. ``"fig01-deconvolution-before-after"``.
        outdir: target dir (defaults to the run's ``outputs/``).
        close: close the figure after saving (free memory in batch builds).

    Returns:
        ``{"pdf": <path>, "png": <path>}``.
    """
    out = outdir or OUTPUT_DIR
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / f"{stem}.pdf"
    png = out / f"{stem}.png"
    fig.savefig(pdf)
    fig.savefig(png)
    if close:
        plt.close(fig)
    return {"pdf": pdf, "png": png}
