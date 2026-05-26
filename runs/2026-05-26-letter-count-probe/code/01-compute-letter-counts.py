#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01-compute-letter-counts.py --- Block 1 of the 2026-05-26 letter-count probe.

Purpose
-------
Compute two letter-count columns on the already-filtered LIRE v3.0 corpus, to
support the Martin-Eftimoski-nudged sensitivity analysis (`runs/2026-05-26-
letter-count-probe/spec.md`).

Two text fields are counted independently and emitted as a sensitivity pair
per spec Decision 1:

  letter_count_conservative   := letters in `clean_text_conservative`
                                 (only preserved letters + expanded
                                 abbreviations).
  letter_count_interpretive   := letters in `clean_text_interpretive_word`
                                 (above + scholarly reconstruction of
                                 supplied text).

"Letter" is defined as a single alphabetic character in either the Latin
alphabet (including diacritics in the Unicode Latin-1 supplement range) or
the Greek alphabet. Spaces, brackets, punctuation, and digits are excluded
by construction.

Critical-friend gate
--------------------
1. Output row count must equal input row count (no row drops; rows with no
   readable letters legitimately get count = 0).
2. No negative counts.
3. Interpretive count must be >= conservative count for every row that
   contains text in both fields, since interpretive includes supplied text
   absent from the conservative reading. Violation count is reported and
   triggers a one-line HALT-warning to stdout (but is not strict-halted ---
   editorial-cleanup peculiarities can produce single-character irregularities).

Inputs
------
runs/2026-05-21-talk-prep/data/lire-filtered.parquet (180,609 rows; already
filter-and-prepped per the lodged preregistration's §3 spec).

Outputs
-------
runs/2026-05-26-letter-count-probe/data/lire-filtered-with-letters.parquet
runs/2026-05-26-letter-count-probe/outputs/tables/letter-count-descriptive.csv
runs/2026-05-26-letter-count-probe/outputs/figures/fig-01-letter-count-histograms.png

Reproducibility
---------------
RANDOM_SEED = 20260526 (no stochastic resampling here; recorded for ritual
consistency with the rest of the pipeline).

Date
----
2026-05-26

Author / Who-asked
------------------
Shawn Ross, post-Martin-Eftimoski-consultation 2026-05-25. Analysis run by
Claude (Opus 4.7, 1M context) on Shawn's brief.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths --- resolved relative to this script so the run is portable.
# ---------------------------------------------------------------------------
SCRIPT_PATH = Path(__file__).resolve()
RUN_DIR = SCRIPT_PATH.parent.parent
PROJECT_ROOT = RUN_DIR.parent.parent
INPUT_PATH = PROJECT_ROOT / "runs" / "2026-05-21-talk-prep" / "data" / "lire-filtered.parquet"
OUT_DATA = RUN_DIR / "data" / "lire-filtered-with-letters.parquet"
OUT_TBL = RUN_DIR / "outputs" / "tables" / "letter-count-descriptive.csv"
OUT_FIG = RUN_DIR / "outputs" / "figures" / "fig-01-letter-count-histograms.png"

for d in (OUT_DATA.parent, OUT_TBL.parent, OUT_FIG.parent):
    d.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 20260526  # ritual; no stochastic work in this block.

# ---------------------------------------------------------------------------
# Letter-count primitive.
#
# Unicode classes:
#   [A-Za-z]                 --- ASCII Latin alphabet (covers the vast bulk of
#                                Latin epigraphy after the LIRE cleaning steps).
#   [À-ÿ]                    --- Latin-1 supplement, covers e.g. é, ç, ñ which
#                                may appear if any diacritic survived the
#                                cleaning steps (defensive; expected rare).
#   [Α-Ωα-ω]                 --- Greek alphabet (LIRE contains some bilingual
#                                or Greek-only inscriptions).
#
# Punctuation, digits, brackets, parentheses, slashes, and whitespace are
# excluded by construction --- the regex only matches letters.
# ---------------------------------------------------------------------------
LATIN_GREEK_LETTER = re.compile(r"[A-Za-zÀ-ÿΑ-Ωα-ω]")


def count_letters(text):
    """
    Count the number of Latin or Greek alphabetic characters in a string.

    Parameters
    ----------
    text : str | float | None
        A text field from LIRE; may be NaN/None for rows where the relevant
        cleaning step yielded no readable text.

    Returns
    -------
    int
        Count of alphabetic characters; 0 if `text` is NaN/None/empty.
    """
    if text is None:
        return 0
    if isinstance(text, float) and np.isnan(text):
        return 0
    if not isinstance(text, str):
        return 0
    return len(LATIN_GREEK_LETTER.findall(text))


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------
def main():
    if not INPUT_PATH.exists():
        sys.exit(f"FATAL: input parquet not found at {INPUT_PATH}")

    print(f"Loading {INPUT_PATH.name}...")
    df = pd.read_parquet(INPUT_PATH)
    n_in = len(df)
    print(f"  loaded {n_in:,} rows.")

    # Confirm the expected text columns are present. If LIRE schema drifts in
    # the future, fail loudly here rather than emit silently-empty columns.
    required_cols = {"clean_text_conservative", "clean_text_interpretive_word"}
    missing = required_cols - set(df.columns)
    if missing:
        sys.exit(f"FATAL: required text columns missing from input: {missing}")

    print("Counting letters (conservative)...")
    df["letter_count_conservative"] = df["clean_text_conservative"].apply(count_letters).astype("int32")

    print("Counting letters (interpretive)...")
    df["letter_count_interpretive"] = df["clean_text_interpretive_word"].apply(count_letters).astype("int32")

    # -----------------------------------------------------------------------
    # Critical-friend gates.
    # -----------------------------------------------------------------------
    n_out = len(df)
    if n_out != n_in:
        sys.exit(f"FATAL: row-count drift {n_in} -> {n_out}; expected lossless.")

    if (df["letter_count_conservative"] < 0).any() or (df["letter_count_interpretive"] < 0).any():
        sys.exit("FATAL: negative letter counts; regex / dtype issue.")

    # Interpretive-vs-conservative monotonicity check. Only meaningful where
    # both fields have text; expected violations are rare and editorial.
    both_have_text = df["clean_text_conservative"].notna() & df["clean_text_interpretive_word"].notna()
    monotonic_violations = (
        df.loc[both_have_text, "letter_count_interpretive"]
        < df.loc[both_have_text, "letter_count_conservative"]
    ).sum()
    pct_violations = 100.0 * monotonic_violations / max(1, both_have_text.sum())
    print(
        f"  monotonicity check: {monotonic_violations:,} rows ({pct_violations:.2f} %) "
        f"have interpretive < conservative."
    )
    if pct_violations > 5.0:
        print(
            f"  WARN: > 5 % monotonicity violation --- inspect "
            f"clean_text_interpretive_word vs clean_text_conservative cleaning logic."
        )

    # -----------------------------------------------------------------------
    # Descriptive table.
    # -----------------------------------------------------------------------
    def describe(col_name):
        s = df[col_name]
        return {
            "field": col_name,
            "n": len(s),
            "n_zero": int((s == 0).sum()),
            "pct_zero": 100.0 * (s == 0).sum() / len(s),
            "median": float(s.median()),
            "q25": float(s.quantile(0.25)),
            "q75": float(s.quantile(0.75)),
            "mean": float(s.mean()),
            "max": int(s.max()),
            "sum": int(s.sum()),
        }

    desc = pd.DataFrame([
        describe("letter_count_conservative"),
        describe("letter_count_interpretive"),
    ])
    desc.to_csv(OUT_TBL, index=False, float_format="%.3f")
    print(f"  descriptive table -> {OUT_TBL.relative_to(PROJECT_ROOT)}")
    print(desc.to_string(index=False))

    # -----------------------------------------------------------------------
    # Two-panel histogram (log y-axis; bins capped visually at the 99th
    # percentile to avoid the long-tail mega-inscriptions swallowing the
    # bulk of the distribution).
    # -----------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)

    for ax, (label, col) in zip(
        axes,
        [
            ("Conservative cleaning", "letter_count_conservative"),
            ("Interpretive cleaning", "letter_count_interpretive"),
        ],
    ):
        vals = df[col].values
        # Visual upper bound: 99th percentile of nonzero. The data extends
        # well past it (see desc table's `max`); zoomed view shows the bulk.
        nonzero = vals[vals > 0]
        upper = int(np.percentile(nonzero, 99)) if len(nonzero) else 1
        ax.hist(vals, bins=np.linspace(0, upper, 60), color="#3a6ea5", edgecolor="white")
        ax.set_yscale("log")
        ax.set_xlim(0, upper)
        ax.set_xlabel("Letters per inscription")
        ax.set_title(f"{label}\n(visual upper bound = 99th pct = {upper:,})")
        ax.grid(True, axis="y", alpha=0.3)
    axes[0].set_ylabel("Inscriptions (log)")
    fig.suptitle(
        f"Letter-count distributions over {n_in:,} filtered LIRE rows "
        f"(50 BC – AD 350; geotemporal + in-Roman-Empire predicates applied)",
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(OUT_FIG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  figure -> {OUT_FIG.relative_to(PROJECT_ROOT)}")

    # -----------------------------------------------------------------------
    # Write augmented parquet.
    # -----------------------------------------------------------------------
    df.to_parquet(OUT_DATA, index=False)
    print(f"  data -> {OUT_DATA.relative_to(PROJECT_ROOT)}")
    print(f"Done. n_in = n_out = {n_in:,}.")


if __name__ == "__main__":
    main()
