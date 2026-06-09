#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_h3b_lib.py — unit tests for the pure-logic H3b helpers.

Covers the deterministic, non-MC pieces: Holm–Bonferroni adjustment, probe-window
bin selection, and the descriptive-bracket mapping. The MC envelope test itself is
exercised by the smoke run (``run_h3b.py --quick``); these tests guard the logic
that does not depend on the (reused, separately-validated) sampler.

Run::

    uv run python -m pytest runs/2026-06-09-h3b/code/test_h3b_lib.py -q

Author: Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-09.
"""

from __future__ import annotations

import numpy as np

import h3b_lib as H


def test_holm_monotone_and_ordering() -> None:
    """Holm output is monotone along the sorted order and in input order."""
    raw = [0.01, 0.04, 0.03, 0.005]
    adj = H.holm_adjust(raw)
    # m = 4; smallest (0.005, rank0) -> 4*0.005=0.02; (0.01,rank1)->3*0.01=0.03;
    # (0.03,rank2)->2*0.03=0.06; (0.04,rank3)->1*0.04=0.04 -> max-running enforces
    # monotonicity so it becomes 0.06.
    assert adj[3] == 0.02  # 0.005 entry
    assert adj[0] == 0.03  # 0.01 entry
    assert abs(adj[2] - 0.06) < 1e-12  # 0.03 entry
    assert abs(adj[1] - 0.06) < 1e-12  # 0.04 entry, lifted by monotonicity
    # All clipped to [0, 1].
    assert all(0.0 <= a <= 1.0 for a in adj)


def test_holm_empty_and_singleton() -> None:
    assert H.holm_adjust([]) == []
    assert H.holm_adjust([0.5]) == [0.5]
    assert H.holm_adjust([1.5]) == [1.0]  # clipped


def test_window_bin_indices_antonine() -> None:
    """Antonine window AD 165–180 selects bin centres 167.5, 172.5, 177.5."""
    idx = H.window_bin_indices(H.ANTONINE_WINDOW)
    centres = H.BIN_CENTRES[idx]
    assert set(np.round(centres, 1)) == {167.5, 172.5, 177.5}


def test_window_bin_indices_crisis() -> None:
    """Crisis window AD 235–284 selects centres 237.5 … 282.5 (10 bins)."""
    idx = H.window_bin_indices(H.CRISIS_WINDOW)
    centres = H.BIN_CENTRES[idx]
    assert len(idx) == 10
    assert np.isclose(centres.min(), 237.5)
    assert np.isclose(centres.max(), 282.5)


def test_describe_bracket() -> None:
    assert "doubling" in H._describe_bracket(1.2)
    assert "50%" in H._describe_bracket(-0.7)
    assert "20%" in H._describe_bracket(0.3)
    assert "sub-bracket" in H._describe_bracket(-0.05)
    # Sign carried through.
    assert "surplus" in H._describe_bracket(0.6)
    assert "deficit" in H._describe_bracket(-0.6)


def test_bin_grid_is_80() -> None:
    """Sanity: the reused bin grid is the prereg 80-bin / 5-y envelope."""
    assert len(H.BIN_CENTRES) == 80
    assert np.isclose(H.BIN_EDGES[0], -50.0)
    assert np.isclose(H.BIN_EDGES[-1], 350.0)


if __name__ == "__main__":
    # Allow running without pytest.
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"ok  {name}")
    print("all tests passed")
