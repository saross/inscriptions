# Provisioning — inscriptions compute environment

How to stand up a reproducible Python environment for this project on a fresh
host (or refresh an existing one), using [uv](https://docs.astral.sh/uv/) and the
committed `uv.lock`. The lock pins the exact stack that produced the §5 Layer-A
results; `uv sync --frozen` reproduces it bit-for-bit.

Last updated: 2026-06-02 (task #9 dependency hygiene — `chore/dep-hygiene-pymc6`).

## The pinned stack

The project standardises on the **pymc-6** stack (validated on zbook for the §5
Layer-A production run):

| package | version | note |
|---------|---------|------|
| python | 3.13.x | `requires-python = ">=3.13"` |
| pymc | 6.0.1 | |
| pytensor | **3.0.3** | pinned in `[tool.uv]`; a clean resolve floats to 3.0.4 |
| arviz | 1.1.0 | 1.x is a major refactor; netCDF I/O is now an optional extra |
| h5netcdf | 1.8.1 | netCDF backend — **must be declared** (see below) |
| h5py | 3.16.0 | HDF5 binding h5netcdf calls at runtime — also declared |
| scikit-learn | 1.8.0 | k-means trajectory clustering (the 2026-05-31 crash dep) |
| numpy / scipy / pandas / pyarrow | 2.4.4 / 1.17.1 / 3.0.2 / 24.0.0 | |

**Why h5netcdf + h5py are explicit dependencies.** arviz 1.x made the netCDF
backend an *optional extra*, and h5netcdf 1.8.1 declares only `numpy` +
`packaging` (the HDF5 library is the caller's choice). The §5 monolithic
posteriors are **HDF5-format `.nc`** files. Without both packages declared, a
clean `uv sync` produces an environment that imports fine but **cannot read the
project's own posteriors** — silently breaking Layer B. They are pinned so this
cannot regress.

**Why pytensor is pinned to 3.0.3.** That is the version that actually produced
the §5 results. A clean resolve of `pymc>=6.0.1` floats pytensor to 3.0.4; the
`[tool.uv] constraint-dependencies` pin keeps the locked environment a faithful
image of the validated run. Lift it only when deliberately upgrading and
re-validating.

## Prerequisites

1. **uv** on PATH (here it lives at `~/.local/bin/uv`, not in the
   non-interactive PATH — call it by full path in scripts).
2. **A C/C++ toolchain + Python development headers.** pytensor compiles C++ at
   runtime (NUTS sampling). It needs `g++`/`gcc` **and** `Python.h`. Two ways to
   satisfy the header requirement:

   - **Preferred:** let uv use a **uv-managed** CPython (`uv python install
     3.13`), which bundles the dev headers — no system `-dev` package needed.
   - **System Python:** install the headers, e.g. on Ubuntu
     `sudo apt install build-essential python3-dev`.

   > Imports succeed without the headers; only *sampling* fails (with
   > `fatal error: Python.h: No such file or directory`). So a host can pass
   > `--check-env` and still be unable to fit. amd-tower (2026-06-02) has `g++`
   > but lacks the Python 3.13 headers — fine for reading posteriors, not for
   > fitting.

## Provision (or refresh) the environment

From the repository root:

```bash
~/.local/bin/uv sync --frozen      # build .venv exactly from uv.lock
```

`--frozen` uses the lock as-is (no re-resolve), so every host gets the same
versions. Omit `--frozen` only when you intend to update the lock.

## Verify

```bash
# Full preflight: imports every runtime dep + checks the HDF5 backend.
.venv/bin/python runs/2026-05-30-s5-small-n-trajectories/code/preflight.py
# or, equivalently, via the orchestrator:
.venv/bin/python runs/2026-05-30-s5-small-n-trajectories/code/orchestrate.py --check-env
```

A `READY` line and exit code 0 mean the environment can import everything and do
HDF5 netCDF I/O. The §5 launch wrapper (`run-production.sh`) runs this preflight
automatically before any sampling; set `SKIP_PREFLIGHT=1` to bypass (e.g. to read
the dry-run plan on a host without the full stack).

## Host notes

- **zbook** — the reference host; already on the pinned stack. Ran the §5
  Layer-A production. Has the dev headers (fits compile).
- **sapphire** — the standing compute server, currently on the **older**
  pymc-5.28 / arviz-0.23 stack (it ran the recovery grids). Standardise it on
  pymc-6 by running `uv sync --frozen` **after the recovery grid finishes** —
  **never** while a grid is running (it would change site-packages under the
  live process). Until upgraded, sapphire's arviz 0.23 may not read the §5
  arviz-1.1 `.nc` posteriors, so Layer B should run on zbook (or a synced host)
  in the meantime.
- **amd-tower** — synced to the pinned stack; reads posteriors fine but cannot
  fit until Python 3.13 dev headers are installed (see Prerequisites).

## Resuming diagnostics without re-fitting

If the monolithic `.nc` posteriors + `subsample-recover-results.json` already
exist but Step-3 diagnostics need to be (re)run — e.g. after a Step-3 crash —
use the resume path instead of re-paying the ~5.7 h of fitting:

```bash
.venv/bin/python runs/2026-05-30-s5-small-n-trajectories/code/orchestrate.py \
    --resume-diagnostics \
    --out-base runs/2026-05-30-s5-small-n-trajectories/code/production
```

This loads Steps 1–2 from disk and only re-fits the few standalone
anchor/Pompeii cities (~15–25 min). It supersedes the one-off
`finish_diagnostics.py`.
