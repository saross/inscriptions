#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build-justification.py — assemble the OSF Amendment 02 justification.txt.

Mirrors the Amendment 01 apparatus: a hand-written concise statement (pasted
into the OSF "justification" field) followed by the FULL amendment reproduced as
plain text. The plain-text body is produced from the amendment markdown via
pandoc (markdown -> plain), with the YAML frontmatter flattened to visible
``key: value`` lines first (pandoc otherwise consumes YAML as metadata).

Usage: python build-justification.py
Writes: planning/osf-amendment-02-justification.txt

Author / Date: Claude Code (Opus 4.8, 1M context) on Shawn Ross's brief, 2026-06-06.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
MD = ROOT / "planning" / "osf-amendment-2026-06-06-latin-frame.md"
OUT = ROOT / "planning" / "osf-amendment-02-justification.txt"
PANDOC = Path("/opt/quarto/bin/tools/x86_64/pandoc")

CONCISE = """\
OSF JUSTIFICATION — Amendment 02: Latin-speaking provinces as the primary hypothesis-testing frame

[Paste everything below the divider into the OSF "justification" field. Plain text — the field does not render Markdown. Lodgement date: 2026-06-06. OSF does not permit new file uploads to a registration update, so the full amendment is LINKED (version-pinned at git tag osf-amendment-02-2026-06-06) and ALSO reproduced in plain text below, so the OSF record is self-contained. If the field rejects the length, delete the reproduced plain text and keep the concise statement + links — linking is OSF's own recommended method.]

==============================================================================

This is the second amendment to the project's preregistration (osf.io/uycs6, lodged 2026-05-20, embargoed). It is filed under the preregistration's own contingency rule, which requires substantive post-lodgement methodology changes to be lodged as an OSF amendment before implementation. It is a binding gate for the Latin frame only: Latin-speaking-province confirmatory claims (H3a, H3b, H3c, SR1) do not leave the project repository as confirmatory until this amendment is lodged. The empire-wide H3a result is within the original lodged preregistration's "all cities" text and is not gated by this amendment.

The amendment makes one change, with one bookkeeping reconciliation.

(1) Latin-speaking provinces become the primary hypothesis-testing frame. For the cross-sectional confirmatory analyses — H3a (the primary confirmatory result), H3b, H3c(i)/(ii), and SR1 — the primary unit set becomes the Latin-speaking provinces of LIRE v3.0 (Rome excluded), defined by the project's province-to-language classification. Empire-wide results are reported as secondary/context, with the coverage caveat stated. The rationale is dataset coverage: LIRE ("Latin Inscriptions of the Roman Empire") is approximately complete for the Latin-speaking western provinces but captures only a non-representative minority of epigraphic production in the Greek-speaking east, so an empire-wide frame mixes well-covered and poorly-covered provinces. The unit is Latin-speaking provinces, not Latin-only inscriptions, because the rationale is provincial coverage.

The change is coverage-driven, not result-driven, and we state the transparency point plainly: on the Latin frame the within-province population effect is stronger than empire-wide (f_within 0.480 versus 0.299). The reframe is nonetheless justified independently of that — (a) the coverage confound is a property of the dataset, true regardless of any result; (b) the preregistration's own "~815 cities" sampling figure was already the Latin-province filter (the realised empire-wide frame is 1,044 cities; the Latin frame is 817; the lodged "~815" is the Latin count), so the Latin frame was latent in the lodged document and the reframe corrects an under-specification; (c) the empire-wide results are retained and reported, not withdrawn; and (d) no model, estimand, decision rule, or threshold changes — the Latin verdict is read off the same machinery.

(2) Frame-count reconciliation (41 to 39). The lodged preregistration (section 2) states the Latin / Western-Empire subset covers 41 LIRE provinces (Rome excluded); the realised primary frame is 39 provinces / 817 cities. The difference is fully accounted for from evidence and changes no result: two provinces classify Latin but contribute zero Hanson-population-matched cities to the scaling frame (Italia, 1 inscription, redundant with the eleven Augustan regions; Alpes Graiae, 77 inscriptions but no Hanson-matched urban centre), and one is a 1:1 spelling normalisation to the dataset's field value (Lugdunensis to Lugudunensis). The province-to-language map is promoted to a first-class tracked artefact that defines the frame.

Full detail, the realised results on both frames, the reconciliation, the integrity points a reviewer can verify, and the provenance trail are in the full amendment — hosted version-pinned at git tag osf-amendment-02-2026-06-06, and reproduced in plain text below:
  PDF: https://github.com/saross/inscriptions/blob/osf-amendment-02-2026-06-06/planning/osf-amendment-2026-06-06-latin-frame.pdf
  Markdown: https://github.com/saross/inscriptions/blob/osf-amendment-02-2026-06-06/planning/osf-amendment-2026-06-06-latin-frame.md

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
        # markdown -> plain; --wrap=none keeps each paragraph as ONE line (no
        # hard mid-paragraph newlines) so the OSF justification field, which
        # soft-wraps, renders normal word wrap rather than ragged 90-col breaks.
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
