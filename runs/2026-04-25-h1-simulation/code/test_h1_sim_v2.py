#!/usr/bin/env python3
"""
test_h1_sim_v2.py --- Lightweight smoke + schema tests for h1_sim_v2.

Two tests:

  - test_smoke_two_cells: limit to the first 2 cells, n_iter=2, n_mc=20.
    Verifies the driver runs end-to-end without errors.
  - test_schema_v2: verifies the output parquet has the v2 schema, with
    correct cpl_k handling (one row for exp cells, two rows per CPL
    iteration for k in {3, 4} per Decision 9).

Run:
  .venv/bin/python3 -m pytest \\
    runs/2026-04-25-h1-simulation/code/test_h1_sim_v2.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from h1_sim_v2 import main as v2_main  # noqa: E402


REPO_ROOT = _HERE.parent.parent.parent
LIRE_PATH = REPO_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"


@pytest.fixture
def smoke_outdir(tmp_path: Path) -> Path:
    """Fresh tmp_path for each test."""
    return tmp_path / "h1v2"


def test_smoke_two_cells(smoke_outdir: Path) -> None:
    """Smoke: 2 cells x n_iter=2 x n_mc=20 completes without error."""
    if not LIRE_PATH.exists():
        pytest.skip(f"LIRE parquet not present at {LIRE_PATH}")

    rc = v2_main([
        "--data", str(LIRE_PATH),
        "--out", str(smoke_outdir),
        "--seed", "20260425",
        "--n_iter", "2",
        "--n_mc", "20",
        "--cells", "2",
        "--n_jobs", "1",
    ])
    assert rc == 0, "v2 driver returned non-zero exit code"
    parquet = smoke_outdir / "cell-results.parquet"
    assert parquet.exists(), f"Expected output parquet at {parquet}"


def test_schema_v2(smoke_outdir: Path) -> None:
    """Output parquet has all expected v2 columns; CPL emits 2 rows / iter.

    We use a 4-cell smoke run (2 exp + 2 cpl). At n_iter=2 and k in {3, 4}
    that yields 2*2 + 2*2*2 = 12 expected rows.
    """
    if not LIRE_PATH.exists():
        pytest.skip(f"LIRE parquet not present at {LIRE_PATH}")

    rc = v2_main([
        "--data", str(LIRE_PATH),
        "--out", str(smoke_outdir),
        "--seed", "20260425",
        "--n_iter", "2",
        "--n_mc", "20",
        "--cells", "4",
        "--n_jobs", "1",
    ])
    assert rc == 0
    parquet = smoke_outdir / "cell-results.parquet"
    df = pd.read_parquet(parquet)

    expected_cols = {
        "cell_id", "level", "bracket", "shape", "n", "null_model",
        "cpl_k", "cpl_aic", "iter", "detected", "pval_global",
        "n_bins_outside", "null_log_likelihood", "b_hat",
        "b_null_or_cpl_truth", "province_counts", "city_counts",
        "seed_hex", "wall_ms", "converged",
    }
    missing = expected_cols - set(df.columns)
    assert not missing, f"Missing columns in v2 parquet: {missing}"

    # First 4 cells in enumeration order are:
    #   empire / a_50pc_50y / step / n50000 / exponential
    #   empire / a_50pc_50y / step / n50000 / cpl
    #   empire / a_50pc_50y / gaussian / n50000 / exponential
    #   empire / a_50pc_50y / gaussian / n50000 / cpl
    # i.e. 2 exp + 2 cpl cells.
    n_exp_iters = (df["null_model"] == "exponential").sum()
    n_cpl_iters = (df["null_model"] == "cpl").sum()
    # Exp: 2 cells x 2 iter = 4 rows.
    # CPL: 2 cells x 2 iter x 2 k-values (k=3, k=4 per Decision 9) = 8 rows.
    assert n_exp_iters == 4, (
        f"Expected 4 exp rows, got {n_exp_iters}"
    )
    assert n_cpl_iters == 8, (
        f"Expected 8 CPL rows (2 cells x 2 iter x 2 k = {{3, 4}}), "
        f"got {n_cpl_iters}"
    )

    # cpl_k sanity: NaN for exp, in {3, 4} for CPL (k=2 dropped per
    # Decision 9).
    cpl_rows = df[df["null_model"] == "cpl"]
    assert set(cpl_rows["cpl_k"].astype(int).unique()) == {3, 4}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
