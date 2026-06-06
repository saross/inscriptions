#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""flip-preliminary-labels.py — clear the PRELIMINARY / amendment-gated labels.

OSF Amendment 02 lodged 2026-06-06 (Decision 36 gate cleared) and the
cross-sectional track was signed off 2026-06-05 (Decision 37). The Latin-frame
result artefacts in runs/2026-06-04-h3a-confirmatory/outputs/ therefore carry
stale "PRELIMINARY -- pending ..." status labels. This flips each to
CONFIRMATORY, citing the lodgement + sign-off.

Each replacement asserts the OLD string occurs EXACTLY ONCE in its file, so a
drifted source halts rather than silently over-replacing. Narrative/historical
records (decision-log, continuity, session-log, prereg-obligations audit) are
deliberately NOT touched — they are dated records of the state at writing time.

Author / Date: Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-06.
"""

from __future__ import annotations

import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent.parent.parent / "runs" / "2026-06-04-h3a-confirmatory" / "outputs"

# (filename, [(old, new), ...]). Each old must match exactly once.
EDITS: dict[str, list[tuple[str, str]]] = {
    "h3c-latin-results.json": [
        ('"status": "PRELIMINARY -- pending OSF Amendment 02 (Decision 36 amendment-gate)"',
         '"status": "CONFIRMATORY -- OSF Amendment 02 lodged 2026-06-06 (Decision 36 gate cleared); cross-sectional track signed off 2026-06-05 (Decision 37)"'),
    ],
    "sr1-latin-results.json": [
        ('"status": "PRELIMINARY -- pending OSF Amendment 02 (Decision 36 amendment-gate)"',
         '"status": "CONFIRMATORY -- OSF Amendment 02 lodged 2026-06-06 (Decision 36 gate cleared); cross-sectional track signed off 2026-06-05 (Decision 37)"'),
    ],
    "h3c-i-results-ad117-sensitivity.json": [
        ('"status": "PRELIMINARY --- pending sign-off; Latin frame pending OSF Amendment 02 (Decision 36 amendment-gate)"',
         '"status": "CONFIRMATORY --- cross-sectional track signed off 2026-06-05 (Decision 37); Latin frame OSF Amendment 02 lodged 2026-06-06 (Decision 36 gate cleared)"'),
        ('"status": "PRELIMINARY --- pending Shawn\'s sign-off"',
         '"status": "CONFIRMATORY --- signed off 2026-06-05 (Decision 37)"'),
        ('"status": "PRELIMINARY --- pending Shawn\'s sign-off AND pending OSF Amendment 02 (Decision 36 amendment-gate)"',
         '"status": "CONFIRMATORY --- signed off 2026-06-05 (Decision 37) AND OSF Amendment 02 lodged 2026-06-06 (Decision 36 gate cleared)"'),
    ],
    "h3c-i-results-oxrep-primary.json": [
        ('"status": "PRELIMINARY --- pending sign-off; Latin frame pending OSF Amendment 02 (Decision 36 amendment-gate)"',
         '"status": "CONFIRMATORY --- cross-sectional track signed off 2026-06-05 (Decision 37); Latin frame OSF Amendment 02 lodged 2026-06-06 (Decision 36 gate cleared)"'),
        ('"status": "PRELIMINARY --- pending Shawn\'s sign-off"',
         '"status": "CONFIRMATORY --- signed off 2026-06-05 (Decision 37)"'),
        ('"status": "PRELIMINARY --- pending Shawn\'s sign-off AND pending OSF Amendment 02 (Decision 36 amendment-gate)"',
         '"status": "CONFIRMATORY --- signed off 2026-06-05 (Decision 37) AND OSF Amendment 02 lodged 2026-06-06 (Decision 36 gate cleared)"'),
    ],
    "REPORT-latin-h3c-sr1.md": [
        ("# Latin-frame H3c + SR1 — REPORT (preliminary, pending OSF Amendment 02)",
         "# Latin-frame H3c + SR1 — REPORT (confirmatory; OSF Amendment 02 lodged 2026-06-06)"),
        ('**Status:** PRELIMINARY — pending **OSF Amendment 02**. Under Decision 36 the\n'
         'Latin-speaking-provinces frame is the new first-class hypothesis-testing frame,\n'
         'and it is **amendment-gated**: no Latin-primary confirmatory claim leaves the\n'
         'repository until Amendment 02 is lodged. Nothing here is "final".',
         '**Status:** CONFIRMATORY — **OSF Amendment 02 lodged 2026-06-06** (Decision 36\n'
         'gate cleared). Under Decision 36 the Latin-speaking-provinces frame is the new\n'
         'first-class hypothesis-testing frame; the cross-sectional track was signed off\n'
         '2026-06-05 (Decision 37). These Latin-primary results may now leave the\n'
         'repository as confirmatory.'),
        ('**Label:** all results above are **preliminary — pending OSF Amendment 02**\n'
         '(Decision 36 amendment-gate; the Latin frame is the new primary and is\n'
         'amendment-gated).',
         '**Label:** all results above are **confirmatory — OSF Amendment 02 lodged\n'
         '2026-06-06** (Decision 36 gate cleared; cross-sectional track signed off\n'
         '2026-06-05, Decision 37).'),
    ],
    "REPORT-h3c-i-capital-contrast.md": [
        ("# H3c(i) — provincial-capital residual contrast — REPORT (preliminary)",
         "# H3c(i) — provincial-capital residual contrast — REPORT (confirmatory)"),
        ("**Status:** PRELIMINARY — pending Shawn's sign-off. The **Latin frame** is additionally **pending OSF Amendment 02** (Decision 36 amendment-gate); nothing here is final.",
         "**Status:** CONFIRMATORY — cross-sectional track signed off 2026-06-05 (Decision 37); the **Latin frame**'s **OSF Amendment 02 lodged 2026-06-06** (Decision 36 gate cleared)."),
        ("- **Label:** preliminary — pending sign-off; Latin frame pending OSF Amendment 02.",
         "- **Label:** confirmatory — signed off 2026-06-05 (Decision 37); Latin frame's OSF Amendment 02 lodged 2026-06-06."),
    ],
}


def main() -> int:
    n_files = n_edits = 0
    for fname, pairs in EDITS.items():
        path = OUT / fname
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            count = text.count(old)
            if count != 1:
                sys.stderr.write(
                    f"ABORT: {fname}: expected exactly 1 match, found {count} for:\n  {old[:80]}...\n"
                )
                return 1
            text = text.replace(old, new)
            n_edits += 1
        path.write_text(text, encoding="utf-8")
        n_files += 1
        print(f"  {fname}: {len(pairs)} label(s) flipped")
    print(f"Done: {n_edits} labels flipped across {n_files} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
