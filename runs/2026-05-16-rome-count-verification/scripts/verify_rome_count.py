"""
Rome-count verification for preregistration-draft.md.

Reproduces the inscription counts cited in §1 of the preregistration:

    "Rome alone contributes 65,435 inscriptions to the filtered corpus:
     36.2 % of the 180,609-row total, or 46.5 % of the 140,575 inscriptions
     assigned to a Hanson-catalogued city. The Rome-excluded corpus is
     therefore 115,174 inscriptions."

Runs from the project root:
    .venv/bin/python runs/2026-05-16-rome-count-verification/scripts/verify_rome_count.py

The filter applied is identical to the preregistration's §1 specification:

    is_geotemporal := Latitude IS NOT NULL AND Longitude IS NOT NULL
                      AND not_before IS NOT NULL AND not_after IS NOT NULL
                      AND not_before <= not_after
    is_within_RE   := province IS NOT NULL
    envelope       := not_after >= -50 AND not_before <= 350
                      (overlap, not containment, with [50 BC, AD 350])

If the script's output diverges from the preregistration figures, treat the
preregistration figures as suspect — the parquet at `archive/data-2026-04-22/
LIRE_v3-0.parquet` is the source of truth.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
RUN_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = RUN_DIR.parent.parent
DATA_PATH = PROJECT_ROOT / "archive" / "data-2026-04-22" / "LIRE_v3-0.parquet"
OUT_DIR = RUN_DIR / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

ENVELOPE_MIN, ENVELOPE_MAX = -50, 350


def main() -> None:
    df = pd.read_parquet(DATA_PATH)
    pre_filter = len(df)

    is_geotemporal = (
        df["Latitude"].notna()
        & df["Longitude"].notna()
        & df["not_before"].notna()
        & df["not_after"].notna()
        & (df["not_before"] <= df["not_after"])
    )
    is_within_re = df["province"].notna()
    in_envelope = (df["not_after"] >= ENVELOPE_MIN) & (df["not_before"] <= ENVELOPE_MAX)

    filt = is_geotemporal & is_within_re & in_envelope
    sub = df.loc[filt]
    filtered_total = len(sub)

    rome = int((sub["urban_context_city"] == "Roma").sum())
    has_city = int(sub["urban_context_city"].notna().sum())
    rome_excluded = filtered_total - rome

    lines = [
        "# Rome-count verification — output",
        "",
        f"- Pre-filter rows: {pre_filter:,}",
        f"- Filtered corpus: {filtered_total:,}  (prereg states 180,609)",
        f"- Rome rows in filtered corpus: {rome:,}  (prereg states 65,435)",
        f"- Rome share of filtered corpus: {100 * rome / filtered_total:.3f} %  (prereg states 36.2 %)",
        f"- Rows with a Hanson-catalogued city assigned: {has_city:,}  (prereg states 140,575)",
        f"- Rome share of city-assigned subset: {100 * rome / has_city:.3f} %  (prereg states 46.5 %)",
        f"- Rome-excluded corpus: {rome_excluded:,}  (prereg states 115,174)",
        "",
        f"Source data: `{DATA_PATH.relative_to(PROJECT_ROOT)}`",
        f"Filter spec: preregistration-draft.md §1 (Dataset and corpus).",
    ]
    out_path = OUT_DIR / "verification.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWritten to: {out_path}")


if __name__ == "__main__":
    main()
