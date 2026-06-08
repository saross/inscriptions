#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build-justification.py — assemble the OSF Amendment 03 justification.txt.

Mirrors the Amendment 01/02 apparatus: a hand-written concise statement (pasted
into the OSF "justification" field) followed by the FULL amendment reproduced as
plain text. The plain-text body is produced from the amendment markdown via
pandoc (markdown -> plain), with the YAML frontmatter flattened to visible
``key: value`` lines first (pandoc otherwise consumes YAML as metadata).

The anticipated lodgement date / git tag below is 2026-06-08 /
osf-amendment-03-2026-06-08. CONFIRM at lodgement and update the date + tag in
the concise statement (and the summary-addendum) if the actual lodgement differs.

Usage: python build-justification.py
Writes: planning/osf-amendment-03-justification.txt

Author / Date: Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-08.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
MD = ROOT / "planning" / "osf-amendment-2026-06-07-convention-basis.md"
OUT = ROOT / "planning" / "osf-amendment-03-justification.txt"
PANDOC = Path("/opt/quarto/bin/tools/x86_64/pandoc")

CONCISE = """\
OSF JUSTIFICATION — Amendment 03: The editorial-convention component of the temporal mixture is an empirical calendar-slab basis (grid-quantisation reframe; no reign tier)

[Paste everything below the divider into the OSF "justification" field. Plain text — the field does not render Markdown. Lodgement date: 2026-06-08. OSF does not permit new file uploads to a registration update, so the full amendment is LINKED (version-pinned at git tag osf-amendment-03-2026-06-08) and ALSO reproduced in plain text below, so the OSF record is self-contained. If the field rejects the length, delete the reproduced plain text and keep the concise statement + links — linking is OSF's own recommended method.]

==============================================================================

This is the third amendment to the project's preregistration (osf.io/uycs6, lodged 2026-05-20, embargoed). It is filed under the preregistration's own contingency rule, which requires substantive post-lodgement methodology changes to be lodged as an OSF amendment before implementation. It is a binding gate for the H2.1 temporal deconvolution-mixture only: the production mixture fit must not run until this amendment is lodged. It is independent of Amendments 01 and 02, which govern the cross-sectional track (H3a, H3c, SR1) on date-window counts and are untouched here.

The amendment redefines the mixture's editorial-convention component (p_conv) and reframes what the "convention" artefact is. There are four linked changes, all flowing from one empirical finding and one conceptual correction.

(1) The convention component becomes an empirical three-tier calendar-slab basis, with NO reign tier. The lodged design typed convention as reign/dynasty slabs plus round-period brackets. A full template-dictionary scan of the corpus (the exact-match dating-interval frequency distribution) showed that curated basis to be empirically inadequate: multi-century calendar slabs are about 31 percent of the convention pool and were absent from the curated tiers, while reign intervals are only about 2.7 percent. The convention component is rebuilt as the frequency-weighted aoristic distribution of the corpus's actual calendar-slab templates, grouped into three structural tiers by interval width — sub-century, century, multi-century — built per frame (empire and Latin), with no reign tier.

(2) Reigns, dynasties, and datable events are reclassified as genuine-but-aoristic, not convention. The lodged document placed reign-dated inscriptions in the convention component; the family classifier and the historical-anchor principle place them out of it. A reign or datable event is genuine chronological information with a wide but real interval (for example Marcus Aurelius, AD 161 to 180); it is not a calendar-rounding artefact. A small curated historical-anchor interval list defines these, drawn from the corpus's own datable-event intervals.

(3) The "convention" artefact is reframed as grid-quantisation of genuine-but-coarse evidence, not absence of information. The lodged framing treated round-period datings as carrying approximately no chronological signal (a midpoint spike; "round period approximately equals no information"). The corrected framing: every recorded interval reflects genuine but coarse knowledge that the editorial tradition has snapped onto the BC/AD calendar lattice. The artefact the method removes is that grid-snapping — the per-inscription distortion and the cross-item boundary pile-ups — not an absence of signal. The observable discriminator is grid-alignment, a proxy for the dating criterion that LIRE's raw_dating field does not preserve.

(4) Decadal and quarter-century brackets ride as a reported sensitivity band, not a hard class. These fine brackets (about 4 to 5 percent of the corpus) are grid-snapped (convention side) but low-distortion (fine grid), so they are added back as a robustness band rather than forced into a binary classification.

What does NOT change: the mixture likelihood and the F1/F3 structural fixes (build_model_f1_f3), the learned three-tier Dirichlet structure, the envelope (50 BC to AD 350, 5-year bins), the largest-remainder multinomial observation model, the cross-sectional track, and year-precise dates (which remain genuine).

The change is gated on a fresh recovery re-validation, because the validated recovery of the earlier basis (Grid A) does not transfer to a multi-century-bearing basis: a long flat envelope-edge plateau is a priori confusable with genuine quiescence. The re-validation re-generated synthetics from the new empirical basis and ran a stress-triage first (the alpha = 0.95, multi-century, peaked-genuine corner) then a full 450-cell grid, scored under the Amendment-01 section A5.5.1 criterion (convergence and shape binding; alpha-coverage a shape-conditioned diagnostic; operating envelope alpha <= 0.70). Both passed. The full grid clean-passes 96.4 percent of in-envelope cells against the 90 percent bar; the feared multi-century plateau-confusion failure mode is absent (the multi-century tier is not a systematic failure, and alpha is recovered essentially unbiased, mean signed bias +0.005); and alpha-recovery precision (95 percent limits of agreement [-0.12, +0.13], shape-conditioned from about +/-0.09 for smooth/flat shapes to about +/-0.18 for multimodal shapes) is within the +/-0.18 envelope Amendment 01 established for Grid A.

Full detail — the basis construction, the template-dictionary evidence, the recovery re-validation REPORT, the novelty positioning, and the provenance trail — is in the full amendment, hosted version-pinned at git tag osf-amendment-03-2026-06-08, and reproduced in plain text below:
  PDF: https://github.com/saross/inscriptions/blob/osf-amendment-03-2026-06-08/planning/osf-amendment-2026-06-07-convention-basis.pdf
  Markdown: https://github.com/saross/inscriptions/blob/osf-amendment-03-2026-06-08/planning/osf-amendment-2026-06-07-convention-basis.md

==============================================================================
FULL AMENDMENT (reproduced in plain text from the Markdown source)
==============================================================================

"""


def split_frontmatter(md_text: str) -> tuple[list[str], str]:
    lines = md_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], md_text
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx], "\n".join(lines[idx + 1:])
    return [], md_text


def render_frontmatter_plain(fm_lines: list[str]) -> str:
    out = []
    for line in fm_lines:
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            out.append(line.strip())
            continue
        out.append(f"{key.strip()}: {value.strip().strip(chr(34)).strip(chr(39))}")
    return "\n".join(out) + "\n\n------------------------------------------------------------------------\n\n"


def main() -> None:
    if not PANDOC.exists():
        sys.exit(f"pandoc not found at {PANDOC}")
    md_text = MD.read_text(encoding="utf-8")
    fm, body = split_frontmatter(md_text)

    with tempfile.TemporaryDirectory() as tmp:
        build_md = Path(tmp) / "body.md"
        build_md.write_text(body, encoding="utf-8")
        res = subprocess.run(
            [str(PANDOC), str(build_md), "-f", "gfm", "-t", "plain",
             "--wrap=none", "-o", "-"],
            capture_output=True, text=True,
        )
        if res.returncode != 0:
            sys.stderr.write(res.stderr)
            sys.exit(f"pandoc failed (exit {res.returncode})")
        body_plain = res.stdout

    OUT.write_text(CONCISE + render_frontmatter_plain(fm) + body_plain, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
