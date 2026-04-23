# Verdict — LIRE v3.0 descriptive profile (2026-04-23)

## Verdict: **PASS**

All 223 claims enumerated in `claims.jsonl` reproduce within the tolerances specified in the verifier brief (exact match for counts and rankings; ±0.1 pp for percentages; ±0.5 % relative for chi-square and p-values; ±0.1 % relative for mean/median/stddev). Independent adversarial spot-checks against the source parquet — using a distinct numpy-frequency-dictionary code path rather than the scout's pandas-boolean code path — also reproduce exactly for the unexpected-pattern diagnostic (granularity histogram + broad date-range histogram), the two load-bearing artefact checks (midpoint-inflation at AD 50/150/250/350 and editorial-spikes at the seven `not_before` and seven `not_after` boundary years), and random per-subset details at dataset (`inscr_process` null rate = 93.8683 %), province (`Roma` count = 65,457), and urban-area (`Cirta` count = 1,020) levels.

No numerical corrections are required. The six judgement calls the proposer recorded in `decisions.md` are semantic, not numerical: the verifier confirms each of them reproduces the claimed figure and, for Decision 4, independently confirms the proposer's overlap-vs-containment interpretation — all 182,853 rows have date intervals that overlap 50 BC – AD 350, so the reported "34,562 temporal outliers" figure is correct under the scout's stated literal-endpoint semantics and 0 under an overlap interpretation. See `corrections.md` §"Semantic dependencies" for per-claim notes.

One minor documentation issue worth flagging (not a numerical correction): claims c0213–c0214 describe the `other_round_values` bucket as "10, 20, 30, ..., 500" (implying every multiple of 10), but the scout's source code hardcodes a discrete set `{10, 20, 30, 40, 60, 70, 75, 80, 90, 125, 150, 175, 250, 300, 400, 500}`. The reported count (3,971) is correct relative to the code, and the description should be updated to enumerate the actual set so future verifiers and readers are not misled.

## Files

- `/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/outputs/corrections.md`
- `/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/outputs/verdict.md` (this file)
- `/home/shawn/Code/inscriptions/runs/2026-04-23-descriptive-stats/outputs/verifier.log`
