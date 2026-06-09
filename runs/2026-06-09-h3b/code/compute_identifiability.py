#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compute_identifiability.py — derive the H3b identifiable-unit split.

The confirmatory H3b set is restricted to units whose H2.1 editorial-convention
correction is *reliable*. Per the prereg note
``planning/prereg-note-2026-06-09-alpha-identifiability.md`` (lines 53, 70–72) and
the H3b brief, the **operative flag** is the gap between a unit's grid-alignment
family-mass fraction and its fitted convention weight ``α``::

    gap = f1f3_family_mass_fraction − alpha_median
    identifiable  ⇔  gap < GAP_THRESHOLD   (GAP_THRESHOLD = 0.20)

A *large* positive gap means the shared-basis fit *under-attributed* convention
(α collapsed) for a temporally-concentrated unit, so its ``corrected_genuine_spa``
still carries convention masquerading as genuine — unreliable as an H3b input.

This module reads the 28 H2.1 production unit JSONs and emits the split. It also
reports the *alternative* basis-swing flag from the committed
``identifiability-table.json`` so the criterion conflict (spec OQ-2) is visible.

Author: Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-09.
UK/Australian English; Oxford comma.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path

PROJECT_ROOT = Path("/home/shawn/Code/inscriptions")
PROD_DIR = (
    PROJECT_ROOT / "runs" / "2026-06-07-h2.1-launch-prep"
    / "outputs" / "production"
)
UNITS_DIR = PROD_DIR / "units"
SWING_TABLE = PROD_DIR / "identifiability-table.json"

# The operative gap flag (prereg note line 53; brief). Units with a smaller gap
# are identifiable (convention/genuine split trusted).
GAP_THRESHOLD: float = 0.20


@dataclass
class UnitIdentifiability:
    """One unit's identifiability summary under the gap criterion."""

    name: str
    unit_index: int
    n_eff: int
    f1f3_family_mass_fraction: float
    alpha_median: float
    gap: float
    identifiable_gap: bool
    final_tier: str
    # The alternative basis-swing flag (from identifiability-table.json), if found.
    swing: float | None = None
    identifiable_swing: bool | None = None


def _load_swing_map() -> dict[str, dict]:
    """Map unit name → swing-table record (the alternative criterion)."""
    if not SWING_TABLE.exists():
        return {}
    rows = json.loads(SWING_TABLE.read_text(encoding="utf-8"))
    return {r["name"]: r for r in rows}


def compute_split() -> list[UnitIdentifiability]:
    """Read all unit JSONs and compute the gap-based identifiability split.

    Returns
    -------
    list[UnitIdentifiability]
        One record per H2.1 production unit, in unit-index order.
    """
    swing_map = _load_swing_map()
    records: list[UnitIdentifiability] = []
    for path in sorted(UNITS_DIR.glob("unit-*.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        f1f3 = float(d["f1f3_family_mass_fraction"])
        alpha = float(d["alpha_median"])
        gap = f1f3 - alpha
        sw = swing_map.get(d["name"])
        records.append(
            UnitIdentifiability(
                name=d["name"],
                unit_index=int(d["unit_index"]),
                n_eff=int(d["n_eff"]),
                f1f3_family_mass_fraction=f1f3,
                alpha_median=alpha,
                gap=gap,
                identifiable_gap=bool(gap < GAP_THRESHOLD),
                final_tier=str(d.get("final_tier", "?")),
                swing=(float(sw["swing"]) if sw else None),
                identifiable_swing=(bool(sw["identifiable"]) if sw else None),
            )
        )
    records.sort(key=lambda r: r.unit_index)
    return records


def identifiable_names(records: list[UnitIdentifiability]) -> list[str]:
    """Names of the gap-identifiable (confirmatory-eligible) units."""
    return [r.name for r in records if r.identifiable_gap]


def flagged_names(records: list[UnitIdentifiability]) -> list[str]:
    """Names of the gap-flagged (exploratory-only) units."""
    return [r.name for r in records if not r.identifiable_gap]


def main() -> None:
    """Print the split and write a machine-readable copy next to outputs."""
    records = compute_split()
    ident = [r for r in records if r.identifiable_gap]
    flagged = [r for r in records if not r.identifiable_gap]

    print(f"Gap criterion: identifiable ⇔ (f1f3 − α) < {GAP_THRESHOLD}")
    print(f"\nIDENTIFIABLE — {len(ident)} units (confirmatory-eligible):")
    for r in sorted(ident, key=lambda x: -x.n_eff):
        print(f"  {r.name:35s} N={r.n_eff:6d} gap={r.gap:+.3f}")
    print(f"\nFLAGGED under-identified — {len(flagged)} units (exploratory only):")
    for r in sorted(flagged, key=lambda x: -x.gap):
        print(f"  {r.name:35s} N={r.n_eff:6d} gap={r.gap:+.3f}")

    out = PROJECT_ROOT / "runs" / "2026-06-09-h3b" / "outputs" / "identifiability-split.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps([asdict(r) for r in records], indent=2),
        encoding="utf-8",
    )
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
