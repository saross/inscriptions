#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preflight.py — fail-fast environment check for the §5 Layer-A pipeline.
======================================================================

Why this exists
---------------
The 2026-05-31 production run sampled for **5.7 hours** and then crashed at the
*final* diagnostic step on a missing ``scikit-learn`` — an undeclared dependency
that was imported lazily, deep inside Step 3, long after the expensive work was
done. The cure for "crash 5 hours in on a missing import" is to check every
runtime import *before* anything samples. That is all this module does: it
imports each third-party package the §5 pipeline relies on, verifies the HDF5
netCDF backend is actually functional (arviz 1.x makes it an optional extra —
see ``pyproject.toml``), prints a version table, and reports any failures.

It is deliberately cheap (imports only; no sampling, no compilation) and has two
entry points:

- ``assert_ready()`` — called by ``orchestrate.run_production`` at the top of the
  run, so a missing dependency aborts in seconds, not hours.
- ``python preflight.py`` / ``orchestrate.py --check-env`` — a standalone report
  for provisioning a new host (see ``PROVISIONING.md``).

What it checks
--------------
The third-party packages actually imported by the §5 code (enumerated from the
source, not guessed): numpy, pandas, pyarrow (parquet I/O), pymc, pytensor,
arviz, scikit-learn (k-means clustering), matplotlib (plots), and the
h5netcdf + h5py pair (the HDF5 backend behind ``arviz.to_netcdf`` /
``arviz.from_netcdf`` — the four monolithic posteriors are HDF5-format ``.nc``).

This module does NOT check that pytensor can compile C extensions (that needs a
C toolchain + Python dev headers; see ``PROVISIONING.md``). It checks imports
and the HDF5 backend — the two things that have actually bitten the project.

Author / Date
-------------
Claude (Opus 4.8, 1M context), 2026-06-02, on Shawn's brief (task #9).
"""

from __future__ import annotations

import importlib
import importlib.metadata as md
import sys

# Distribution name -> import name. The §5 runtime set, enumerated from the
# source (top-level AND function-level imports, plus implicit backends). Keep
# this in sync with pyproject.toml's runtime dependencies for the §5 pipeline.
REQUIRED: dict[str, str] = {
    "numpy": "numpy",
    "pandas": "pandas",
    "pyarrow": "pyarrow",          # parquet engine for dataprep caches
    "scipy": "scipy",             # transitive (pymc/arviz) but assert it loads
    "pymc": "pymc",
    "pytensor": "pytensor",
    "arviz": "arviz",
    "scikit-learn": "sklearn",    # the 2026-05-31 crash: KMeans clustering
    "matplotlib": "matplotlib",
    "h5netcdf": "h5netcdf",       # netCDF backend (arviz 1.x optional extra)
    "h5py": "h5py",               # HDF5 binding h5netcdf calls at runtime
}


def _version(dist: str) -> str:
    """Best-effort installed version of a distribution (``"?"`` if unknown)."""
    try:
        return md.version(dist)
    except md.PackageNotFoundError:
        return "?"


def check_imports() -> tuple[list[tuple[str, str, str, str]], list[str]]:
    """Import every required package; collect a status row per package.

    Returns:
        ``(rows, missing)`` where each row is
        ``(distribution, import_name, version, status)`` and ``missing`` is the
        list of distribution names that failed to import.
    """
    rows: list[tuple[str, str, str, str]] = []
    missing: list[str] = []
    for dist, mod in REQUIRED.items():
        try:
            importlib.import_module(mod)
            rows.append((dist, mod, _version(dist), "OK"))
        except Exception as exc:  # noqa: BLE001 - report any import failure
            rows.append((dist, mod, _version(dist), f"FAIL: {exc!r}"))
            missing.append(dist)
    return rows, missing


def check_hdf5_backend() -> tuple[bool, str]:
    """Verify the HDF5 backend works, not merely that h5py imports.

    arviz 1.x writes/reads ``.nc`` as HDF5 via h5netcdf -> h5py. h5py importing
    is not sufficient: the binding to the underlying HDF5 C library can be
    broken independently. Create an in-memory HDF5 file (no disk) and round-trip
    a dataset — the cheapest decisive check of the path that actually fails.
    """
    try:
        import h5py
        import numpy as np

        with h5py.File("preflight-probe.h5", "w",
                       driver="core", backing_store=False) as f:
            f.create_dataset("probe", data=np.arange(4))
            ok = tuple(f["probe"].shape) == (4,)
        return ok, "h5py in-memory HDF5 round-trip OK" if ok else \
            "h5py round-trip returned unexpected shape"
    except Exception as exc:  # noqa: BLE001
        return False, f"HDF5 backend check failed: {exc!r}"


def report() -> bool:
    """Print the version table + HDF5 check; return True iff the env is ready."""
    rows, missing = check_imports()
    width = max(len(d) for d, _, _, _ in rows)
    print(f"§5 preflight — python {sys.version.split()[0]}")
    print("-" * 72)
    for dist, mod, ver, status in rows:
        print(f"  {dist:<{width}}  {ver:<14}  {status}")
    hdf5_ok, hdf5_msg = check_hdf5_backend()
    print("-" * 72)
    print(f"  HDF5 backend: {'OK' if hdf5_ok else 'FAIL'} — {hdf5_msg}")
    ready = not missing and hdf5_ok
    print("=" * 72)
    print("READY" if ready else f"NOT READY — missing: {missing or '[HDF5]'}")
    return ready


def assert_ready() -> None:
    """Raise ``SystemExit(2)`` with a clear message if the env is not ready.

    Called at the top of ``orchestrate.run_production`` so a missing dependency
    aborts in seconds, before any sampling — the antidote to the 2026-05-31
    "crash 5.7 h in on a missing import" failure.
    """
    if not report():
        raise SystemExit(2)


if __name__ == "__main__":
    raise SystemExit(0 if report() else 2)
