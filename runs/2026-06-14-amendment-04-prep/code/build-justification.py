#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build-justification.py — assemble the OSF Amendment 04 justification.txt.

Mirrors the Amendment 01/02/03 apparatus: a hand-written concise statement (pasted
into the OSF "justification" field) followed by the FULL amendment reproduced as
plain text. The plain-text body is produced from the amendment markdown via pandoc
(gfm -> plain), with the YAML frontmatter flattened to visible ``key: value`` lines
first (pandoc otherwise consumes YAML as metadata).

The anticipated lodgement date / git tag below is 2026-06-14 /
osf-amendment-04-2026-06-14. CONFIRM at lodgement and update the date + tag in the
concise statement (and the summary-addendum) if the actual lodgement differs.

Usage: python build-justification.py
Writes: planning/osf-amendment-04-justification.txt

Author / Date: Claude Code (Fable 5) on Shawn Ross's brief, 2026-06-14.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
MD = ROOT / "planning" / "osf-amendment-2026-06-14-cross-classified-remediation.md"
OUT = ROOT / "planning" / "osf-amendment-04-justification.txt"
PANDOC = Path("/opt/quarto/bin/tools/x86_64/pandoc")

CONCISE = """\
OSF JUSTIFICATION — Amendment 04: Cross-classified time x alignment remediation for the convention-fraction identifiability limit (reverses the shared convention basis)

[Paste everything below the divider into the OSF "justification" field. Plain text — the field does not render Markdown. Anticipated lodgement date: 2026-06-14 — CONFIRM at lodgement and update the date + git tag here and in the summary-addendum if it differs. OSF does not permit new file uploads to a registration update, so the full amendment is LINKED (version-pinned at git tag osf-amendment-04-2026-06-14) and ALSO reproduced in plain text below, so the OSF record is self-contained. If the field rejects the length, delete the reproduced plain text and keep the concise statement + links — linking is OSF's own recommended method.]

==============================================================================

This is the fourth amendment to the project's preregistration (osf.io/uycs6, lodged 2026-05-20, embargoed), filed under the preregistration's own contingency rule, which requires substantive post-lodgement methodology changes to be lodged as an OSF amendment before implementation. It concerns only the H2.1 temporal deconvolution-mixture; the cross-sectional track (H3a, H3c, SR1; Amendments 01 and 02, on date-window counts) is untouched. It reverses one element of Amendment 03 — the shared, unit-independent convention basis — while retaining the rest of Amendment 03 (the grid-quantisation reframe and the reclassification of reigns as genuine-but-aoristic).

The amendment replaces the convention/genuine deconvolution with a cross-classified time x alignment model. The motivation is a structural identifiability limit, diagnosed after the H2.1 production run, that the lodged shared-basis design could not avoid.

The problem. Amendment 03 modelled editorial-convention dating with a single broad calendar-slab template shared across all analytical units. After the production fit, a diagnostic showed this under-identifies the convention fraction (alpha) for temporally-concentrated units — predominantly frontier and military provinces (Britannia, Moesia inferior, Pannonia inferior, and others) whose conventional dating clusters in the same narrow window (their Roman occupation period, roughly AD 100-300) as their genuine inscribing activity. When the convention and genuine components overlap in time, the temporal distribution alone cannot separate them: the smooth genuine component absorbs the period-concentrated convention mass and alpha collapses (Moesia inferior returned alpha approximately 0.05 when about 60 percent of its dating is conventionally grid-aligned). This is a textbook weak-separation identifiability failure — the mixing weight is only weakly identified and the likelihood can be confidently wrong (Feller, Greif, Ho, Miratrix and Pillai 2016), and a prior over a partially-identified region is never updated by the data (Gustafson 2010), which is why an informed-alpha prior, considered first, was refuted on its own prototype.

The remedy. The canonical fix is to bring an informative covariate into the likelihood — the concomitant-variable / latent-class-with-covariate tradition (identification theory in Huang and Bandeen-Roche 2004; the archaeological archetype is the OxCal two-component outlier mixture, Bronk Ramsey 2009). The covariate is grid-alignment: whether an inscription's date sits on the round-number calendar grid (a "1st-2nd century" bracket is grid-aligned; a precise "AD 117-138" is not). The cross-classified model splits each unit's inscriptions into a grid-aligned subset and a non-aligned subset and models the two temporal sub-distributions jointly, sharing the latent quantities (alpha, the convention shape, the genuine shape, and the alignment rates). Alpha is then identified by the contrast between the two subsets — the aligned subset is convention-enriched, the non-aligned subset genuine-enriched — not by the temporal-shape match alone. This is, in collapsed form, the exact likelihood of the per-inscription generative process; the shared-basis fit was a composite-likelihood approximation whose cost was a measured systematic over-attribution.

Three connected specifications:

(1) The deconvolution is the cross-classified time x alignment model (per unit: a binomial for the aligned count and two multinomials for the aligned- and non-aligned-subset summed-probability analyses, all sharing the latents). The temporal block — the Dirichlet convention weighting and the non-centred random-walk genuine shape — is byte-identical to the recovery-validated H2.1 model; only the likelihood structure (the alignment split plus the classification term) is new.

(2) The convention shape is a fixed, a-priori, corpus-wide round-endpoint slab library, identical for every unit — the direct production analogue of the fixed slab library that the recovery grid validated, sized to the real corpus. Being fixed and unit-independent it carries no per-unit contamination channel; being deterministic boxes it carries no mass contamination. This is what makes reversing Amendment 03's shared basis safe: the classification term supplies the over-attribution control that the shared basis was adopted to provide, so a flexible convention shape no longer over-attributes.

(3) The alignment rates (theta) are calibrated, then re-derived. The plug-in calibration over-stated the genuine-alignment rate because it was fit using the under-attributing shared-basis alphas; re-derived from the corrected estimates — and corroborated by an independent joint fit and a prior-sensitivity sweep — the genuine-alignment rate falls from about 0.155 to about 0.025 and is adopted as the production prior.

What does NOT change: the mixture likelihood's temporal block (the Dirichlet convention weighting, the non-centred random-walk genuine shape, the Beta(1,1) alpha prior); the envelope (50 BC to AD 350, 5-year bins); the largest-remainder multinomial observation model; year-precise dates (genuine); the cross-sectional track; and Amendment 03's grid-quantisation reframe and reigns-as-genuine reclassification (this amendment changes how convention is identified, not what convention is).

Validation. Because the likelihood structure changes, the model was recovery-validated on synthetic data with known answers before the production refit. A 300-cell by 100-replicate recovery grid (zero failed cells) shows, against the shared-basis design: the near-uniform +0.06 to +0.08 over-attribution bias of the shared/estimated basis is eliminated (the do-no-harm identifiable-cell median bias falls to 0.021, and the bias surface is flat across the whole parameter plane); the confounded cells are pulled to truth (median bias 0.009, against a shared-basis baseline of 0.362 — roughly a 40-fold reduction); and convergence improves to 96 percent of cells. A production refit of the 29 analytical units then confirms the diagnostic prediction on the real data: all ten flagged frontier units rise to sensible mid-range convention fractions tracking an independent classification-implied estimate (Moesia inferior 0.05 to 0.70, Britannia 0.00 to 0.45, Pannonia inferior 0.15 to 0.68, and so on), while the well-identified controls are unchanged (Pompeii remains about 0, correctly; the aggregates move negligibly). A theta-prior sensitivity sweep (four priors over the 29 units) shows the per-unit convention fractions are stable to the theta assumption for 27 of 29 units; only the two most temporally-confounded units carry a residual theta-sensitivity, and they move within the disclosed two-bound range.

H3b — the project's pre-specified exploratory deviation-detection analysis — is not a confirmatory family (Decision 15). The post-hoc restriction of H3b to "identifiable units" is replaced by propagating the cross-classified deconvolution's posterior uncertainty into the deviation test, so a unit whose convention/genuine split is weakly identified receives a wider, more conservative result rather than a hard exclusion; the lodged Phase-1 reachability (power) gate is unchanged, the coverage caveat is carried, and the two most theta-sensitive units (Moesia inferior and Britannia) carry a soft reliability annotation. The implementation (the H2.1 hand-off emitting the genuine-SPA posterior rather than only its median, and the draw-wise envelope test) is part of finalising the H3b analysis, not pre-specified by this amendment.

Full detail — the model, the recovery-grid verdict, the production refit, the theta robustness work, the literature warrant, and the provenance trail — is in the full amendment, hosted version-pinned at git tag osf-amendment-04-2026-06-14, and reproduced in plain text below:
  PDF: https://github.com/saross/inscriptions/blob/osf-amendment-04-2026-06-14/planning/osf-amendment-2026-06-14-cross-classified-remediation.pdf
  Markdown: https://github.com/saross/inscriptions/blob/osf-amendment-04-2026-06-14/planning/osf-amendment-2026-06-14-cross-classified-remediation.md

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
