#!/usr/bin/env python3
"""Build a lodgement-grade PDF from the OSF amendment markdown.

The amendment markdown carries a YAML frontmatter block (title, status,
lodged-version, gate, dates, ...). Pandoc's markdown reader silently consumes
leading YAML as *metadata* — only ``title`` survives into the rendered output —
so this script first transforms the frontmatter into a visible key/value header
block, then runs Pandoc with the project's house flags.

House flags (reconstructed from the lodged supplementary build, commit a2e40fd):
  * ``-f markdown+autolink_bare_uris`` — emit ``\\url{}`` for bare URIs so xurl
    can act on them (without this, bibliography URLs come through as unbreakable
    plain text and overflow the right margin).
  * ``xurl`` via ``--include-in-header`` — let ``\\url`` break at any character.
  * ``--pdf-engine=xelatex`` with 0.8in margins.

Usage::

    python scripts/build-amendment-pdf.py \
        wiki/prereg/osf-amendment-2026-05-29-two-measure-framework.md

The output PDF is written alongside the input (``.md`` -> ``.pdf``). The PDF is a
build artefact, not committed source; regenerate it whenever the markdown changes.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

# Quarto bundles the pandoc binary the supplementary PDF was built with (3.6.3);
# it is not on PATH, so reference it explicitly.
PANDOC = Path("/opt/quarto/bin/tools/x86_64/pandoc")

# LaTeX preamble injected via --include-in-header. xurl loosens \url line-breaking
# (for bibliography/frontmatter URLs); the 0.78 mono scale matches the lodged
# supplementary and shrinks long inline-code paths (e.g. the 72-char
# runs/.../REPORT.md token) enough to wrap onto their own line; emergencystretch +
# sloppy mop up the remainder. Together these zero out the overfull \hbox warnings.
HEADER_TEX = r"""
\usepackage{xurl}
\setmonofont[Scale=0.78]{Latin Modern Mono}
\setlength{\emergencystretch}{3em}
\sloppy
"""


def split_frontmatter(md_text: str) -> tuple[list[str], str]:
    """Split a leading YAML frontmatter block from the markdown body.

    Args:
        md_text: Full markdown source, possibly starting with a ``---`` fenced
            YAML block.

    Returns:
        A ``(frontmatter_lines, body)`` tuple. ``frontmatter_lines`` is the list
        of raw ``key: value`` lines (empty if there is no frontmatter); ``body``
        is the markdown after the closing ``---``.
    """
    lines = md_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], md_text
    # Find the closing fence (the next line that is exactly '---').
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx], "\n".join(lines[idx + 1 :])
    # Unterminated frontmatter: treat the whole file as body to avoid data loss.
    return [], md_text


def render_frontmatter(frontmatter_lines: list[str]) -> str:
    """Render raw frontmatter lines as a visible bold key/value markdown block.

    Each top-level ``key: value`` pair becomes ``**key:** value`` on its own line
    (with a hard line break), so none of the lodgement metadata is dropped from
    the PDF. Surrounding quotes on values are stripped for readability.

    Args:
        frontmatter_lines: Raw lines from between the ``---`` fences.

    Returns:
        A markdown string (possibly empty) ending with a horizontal rule.
    """
    rendered: list[str] = []
    for line in frontmatter_lines:
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            # Continuation / non key:value line — keep verbatim.
            rendered.append(line.strip() + "  ")
            continue
        value = value.strip().strip('"').strip("'")
        rendered.append(f"**{key.strip()}:** {value}  ")
    if not rendered:
        return ""
    return "\n".join(rendered) + "\n\n---\n\n"


def extract_title(frontmatter_lines: list[str], fallback: str) -> str:
    """Return the ``title`` value from the frontmatter, else ``fallback``.

    Lets one builder serve every amendment: the PDF metadata title is taken from
    the markdown's own ``title:`` field rather than hard-coded per amendment.
    """
    for line in frontmatter_lines:
        key, sep, value = line.partition(":")
        if sep and key.strip() == "title":
            return value.strip().strip('"').strip("'")
    return fallback


def build_pdf(md_path: Path, title: str | None = None) -> Path:
    """Transform frontmatter and invoke Pandoc to produce the PDF.

    Args:
        md_path: Path to the amendment markdown file.
        title: Override for the PDF metadata title. If ``None``, the title is
            taken from the markdown frontmatter's ``title:`` field, falling back
            to the Amendment 01 string for backward compatibility.

    Returns:
        The path to the generated PDF.

    Raises:
        SystemExit: If Pandoc is unavailable or the build fails.
    """
    if not PANDOC.exists():
        sys.exit(f"pandoc not found at {PANDOC}")

    md_text = md_path.read_text(encoding="utf-8")
    frontmatter_lines, body = split_frontmatter(md_text)
    if title is None:
        title = extract_title(
            frontmatter_lines, "OSF Amendment 01 — Two-measure framework"
        )
    transformed = render_frontmatter(frontmatter_lines) + body

    pdf_path = md_path.with_suffix(".pdf")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        build_md = tmp_dir / "build.md"
        header_tex = tmp_dir / "header.tex"
        build_md.write_text(transformed, encoding="utf-8")
        header_tex.write_text(HEADER_TEX, encoding="utf-8")

        cmd = [
            str(PANDOC),
            str(build_md),
            "-f",
            "markdown+autolink_bare_uris",
            "--pdf-engine=xelatex",
            "-V",
            "geometry:margin=0.8in",
            "-V",
            "colorlinks=true",
            "-V",
            "linkcolor=blue",
            "-V",
            "urlcolor=blue",
            f"--include-in-header={header_tex}",
            "--metadata",
            f"title={title}",
            "-o",
            str(pdf_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            sys.stderr.write(result.stdout)
            sys.stderr.write(result.stderr)
            sys.exit(f"pandoc build failed (exit {result.returncode})")

    return pdf_path


def main() -> None:
    """Parse arguments and build the amendment PDF."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path, help="Path to the amendment .md file")
    parser.add_argument(
        "--title", default=None,
        help="PDF metadata title (default: the markdown's own title: frontmatter).",
    )
    args = parser.parse_args()

    md_path: Path = args.markdown
    if not md_path.exists():
        sys.exit(f"markdown not found: {md_path}")

    pdf_path = build_pdf(md_path, title=args.title)
    print(f"Built {pdf_path} ({pdf_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
