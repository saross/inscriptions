# Verifier verdict — PARTIAL

Of 83 claims, 81 pass, 2 partial, 0 fail, 0 unverifiable.

All numerical claims reproduce exactly or within tolerance against an independent re-derivation from `LIRE_v3-0.parquet`. The two PARTIAL entries are both **source_method-string misdescriptions** on the group-count claims for `province` and `urban-area`: the recorded `source_method` says `df.groupby([...]).ngroups` (default `dropna=True`, which would yield 65 and 1,045), but the numeric values 66 and 1,046 require `dropna=False` (counting null as a group). The visible top-N tables in `profile-urban-area.md` already display `<null>` as a 40,944-row group, so the analytic choice is consistent with the visible report. Only the `source_method` string in `claims.jsonl` is misdescribed; numerically the report is internally consistent.

Per current driver policy (2026-05-22) PARTIAL is flagged but not auto-iterated.

Notes on verification scope:
- Dataset size 182,853 rows — well under the 1M-row threshold; verified on full data, no sampling.
- Independent code path: re-loaded parquet with pandas, recomputed each primitive from scratch; did not consume `tables/*.csv`.
- All chi² statistics and p-values reproduce within 0.5% relative.
- All count, rate, and threshold-qualifying claims reproduce exactly.
- `claims.jsonl` is present and well-formed (83 lines, all valid JSON).
