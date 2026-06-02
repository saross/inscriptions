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
h5netcdf + h5py pair (the HDF5 backend behind ``InferenceData.to_netcdf`` /
``arviz.from_netcdf`` via xarray — the monolithic posteriors are HDF5 ``.nc``).

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
    """Verify the real netCDF write path works, not merely that h5py imports.

    arviz 1.x writes/reads ``.nc`` by delegating to xarray, which delegates to
    the h5netcdf engine, which calls h5py. Importing h5py is not sufficient: the
    binding to the underlying HDF5 C library, the h5netcdf<->h5py pairing, or
    xarray's engine resolution can each break independently. Exercise the actual
    substrate — an xarray Dataset round-tripped through the ``h5netcdf`` engine
    to a temporary ``.nc`` and back — which is the path that fails when the
    backend is missing or mismatched (the failure class this module exists for).
    """
    import os
    import tempfile

    try:
        import numpy as np
        import xarray as xr

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "preflight-probe.nc")
            xr.Dataset({"probe": ("a", np.arange(4))}).to_netcdf(
                path, engine="h5netcdf")
            with xr.open_dataset(path, engine="h5netcdf") as back:
                ok = int(back["probe"].sum()) == 6
        return ok, ("xarray->h5netcdf->h5py .nc round-trip OK" if ok else
                    "netCDF round-trip returned unexpected data")
    except Exception as exc:  # noqa: BLE001
        return False, f"HDF5 backend check failed: {exc!r}"


def report() -> bool:
    """Print the version table + HDF5 check; return True iff the env is ready."""
    rows, missing = check_imports()
    width = max((len(d) for d, _, _, _ in rows), default=0)
    print(f"§5 preflight — python {sys.version.split()[0]}")
    print("-" * 72)
    for dist, mod, ver, status in rows:
        print(f"  {dist:<{width}}  {ver:<14}  {status}")
    hdf5_ok, hdf5_msg = check_hdf5_backend()
    print("-" * 72)
    print(f"  HDF5 backend: {'OK' if hdf5_ok else 'FAIL'} — {hdf5_msg}")
    ready = not missing and hdf5_ok
    print("=" * 72)
    if ready:
        print("READY")
    else:
        problems = list(missing) + ([] if hdf5_ok else ["HDF5-backend"])
        print(f"NOT READY — problems: {problems}")
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
