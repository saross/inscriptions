# Invocation brief: data-profile-verifier → LIRE v3.0 comprehensive profile (2026-04-23, revised)

You are acting as **data-profile-verifier** per the canonical methodology at `~/personal-assistant/agents/data-profile-verifier.md` (the updated definition including stochastic-claim verification). The canonical definition is authoritative; this brief provides run-specific inputs.

## Your role

Adversarial re-check of the `data-profile-scout` comprehensive-mode report. Fresh context, assume nothing, re-compute from the source dataset. Find problems, don't rubber-stamp. The comprehensive-mode claim surface expands substantially (bootstrap CIs, MC permutation p-values, Cliff's delta effect sizes, diversity indices, correlation matrix entries) — every one needs verification.

## Inputs

- `claims_file` (primary input): `runs/2026-04-23-descriptive-stats/outputs/claims.jsonl` (expect ≥ 150 claims; comprehensive mode expands beyond the first run's 223).
- `profile_report_dir`: `runs/2026-04-23-descriptive-stats/outputs/` on sapphire (`~/Code/inscriptions/runs/...`).
- `dataset_path`: `archive/data-2026-04-22/LIRE_v3-0.parquet` (relative to sapphire workdir).
- `remote_exec`: `{host: sapphire, workdir: ~/Code/inscriptions, venv_python: .venv/bin/python3}`.
- `output_dir`: `runs/2026-04-23-descriptive-stats/outputs/` on sapphire (write alongside proposer, do not overwrite).
- `bootstrap_resamples`: 10 000.
- `permutation_resamples`: 10 000.

## Your job

1. **Iterate over `claims.jsonl`.** This is the primary input; one line per claim with fields `{claim_id, category, description, value, units, source_method, source_file}`. Re-compute each from the source parquet using your own code path.
2. **If `claims.jsonl` is missing or malformed**, fall back to parsing the markdown reports (`summary.md`, `profile-*.md`, `artefacts.md`, `comprehensive.md`, `distribution-shape.md`, `temporal-coverage.md`, `categorical-distributions.md`, `concentration.md`, `text-statistics.md`, `correlations.md`, `null-cooccurrence.md`, `drill-downs/*`, `sensitivity-sweep.md`). Flag the missing claims file in `verdict.md` — that's an output-contract failure even if numerical claims reproduce.
3. **For stochastic claims** (`category in {permutation_pvalue, corrected_pvalue, ci_lower, ci_upper}`): re-run the procedure with a **different random seed**, same number of resamples, same data. Apply the stochastic-claim tolerance (±1 pp on p-values, ±5 % relative on CI bounds).
4. **For deterministic claims** (counts, rates, summary stats, rank-based effect sizes like Cliff's delta, diversity indices like Shannon entropy): reproduce exactly within the standard tolerances.
5. **Spot-check at least one random per-subset detail for each subset level** (dataset, province, urban-area, province × urban-area) independently sampled from the claims iteration.
6. **Re-run the unexpected-pattern diagnostic independently** in both views (granularity histogram + broad date-range histogram). If your result contradicts the scout's, flag.
7. **Re-run at least two MC permutation tests** independently — one from `midpoint-inflation`, one from `editorial-spikes`. Check that the scout's reported null model (two-stage: uniform `not_before` across envelope, observed `date_range` marginal) was actually what was implemented, not just what was described.
8. **Re-run at least one drill-down per-year test** independently, particularly the AD 97 neighbourhood where the scout reports a dip. This is where interpretation rides on the test methodology — high-stakes for verifier scrutiny.

## Tolerances

See canonical definition (`data-profile-verifier.md`) for the full table. Summary:

- Counts, top-k rankings: exact (±0).
- Rates, proportions: ±0.1 pp.
- Summary stats: ±0.1 %.
- Stochastic claims (p-values, CI bounds): ±1 pp / ±5 % relative after re-run with different seed.
- Rank-based effect sizes, diversity indices: ±0.001 absolute.

## Output

Write to `output_dir`:

- `corrections.md` — per-claim: `claim_id` / description / scout value / your value / match / notes.
- `verdict.md` — one paragraph rendering PASS / PARTIAL / FAIL.
- `verifier.log`.

Response to caller (≤ 300 words): verdict, count of corrections, severity summary, file paths.

## Adversarial discipline

- Re-compute from the parquet using your own code path; do NOT consume the scout's CSVs.
- For stochastic procedures, use a DIFFERENT seed. Same seed would merely re-produce the scout's numerical output, not verify the methodology.
- Verify the **method as described** against the **method as implemented**. Check the scout's script at `runs/2026-04-23-descriptive-stats/code/profile.py` for each stochastic procedure; does the code actually do the two-stage null? Does it actually apply Holm-Bonferroni? A misdescribed method passes deterministic-numerical verification but produces interpretively wrong claims.
- Common failure modes specific to comprehensive mode:
  - Null model implemented as simple uniform-on-mid (observed mid vs uniform expected) or chi-square-vs-uniform rather than **aoristic-probability null** (for each row, weight 1/date_range within interval; expected at year Y = Σ weights; null resampling redraws mid uniformly within each row's interval). The aoristic framing is the one required by the canonical methodology; a chi-square-vs-uniform implementation is a common accidental simplification that tests the wrong null.
  - Multiple-comparison correction applied across the wrong family (e.g., all tests pooled rather than per-family), or Westfall-Young implemented without the joint permutation distribution (just applied to marginal p-values, which reduces it to something no better than Holm).
  - Assumption-check entries in `decisions.md` missing for inferential claims — each claim with `category in {permutation_pvalue, corrected_pvalue, ci_lower, ci_upper, effect_size, correlation}` should have a corresponding assumption-check entry. Flag claims that lack one.
  - Bootstrap CIs computed on transformed data but reported in original units (or vice versa).
  - Diversity indices computed on grouped data rather than per-group.
  - Spearman correlation computed on rank-tie data with wrong tie-handling.

## Failure modes to avoid (verifier-specific)

- **No rubber-stamping** — independent code path, not consumption of scout outputs.
- **No same-seed reproduction** of stochastic procedures — verifies nothing.
- **No trusting the described method** — check the code.
