# Memo — /reflect multi-invocation safety

**Date:** 2026-04-23 (written overnight; for morning review)
**Source:** overnight Explore agent + my synthesis
**Status:** no action required before you're ready; pick an option when rested

---

## Agent's diagnosis

The `/reflect` skill is **soft-unsafe for multiple same-day
invocations**. All five files append unconditionally with date-only
headers, no timestamp granularity, no de-duplication. Run `/reflect`
at 14:00 and again at 22:00 and both entries date to `2026-04-22`,
distinguishable only by ordinal position in the file.

The agent identified five specific failure modes. The one that
actually matters: `abductive-reasoning.md` has a conditional "scope"
trigger currently evaluated at *session* level, not at *delta-since-
last-reflection* level — so a second invocation can force a duplicate
entry on the same observation.

Full agent output preserved in the task-result transcript at
`/tmp/claude-1000/-home-shawn-Code-inscriptions/91b1783e-e099-49c8-826e-d37026ca716b/tasks/a9f8bbeba94b6b516.output`.

## My take — the failure surface is narrower than the analysis suggests

Per-file, sorted by actual risk:

- **`working-notes.md`** — numbered, monotonic. Multiple-per-day
  entries are fine; date-sharing is cosmetic at worst. Non-issue.
- **`session-log.md`** — two entries per day is two session-chunks,
  not a duplicate. Fine with a time-of-day marker. Low risk.
- **`session-reflection.md`** — two narratives from different
  prompts is plausibly valuable (prompt rotation is already a
  designed feature). Low risk.
- **`abductive-reasoning.md`** — **real risk.** Requires disciplined
  re-evaluation of the conditional trigger on each invocation.
- **`reasoning-log.md`** — already append-only by design and written
  in-stream by me anyway. Untouched by the risk.

So the agent's five-file failure-surface framing overstates the
problem. The actual live risk is one file (abductive-reasoning) plus
a cosmetic issue on the others.

## Three options

**(a) Lightest — convention only.**
Prompt-level rule: multiple same-day invocations add a time-of-day
to their headers (`## 2026-04-22 14:00 — ...`). On
abductive-reasoning, interpret the trigger as *"since last
reflection"* not *"this session overall."* No skill edit needed.

**(b) Agent's recommendation — manual checkpoint file.**
Add a `session-checkpoint.md` to the reflections directory for
mid-session captures. End-of-session `/reflect` touches only the
standard five; checkpoints live separately. Minimal skill edit (a
note in `SKILL.md`).

**(c) Harder — refactor `/reflect` to support `--checkpoint` mode.**
Proper API extension. More work, more risk of breaking existing
usage across your projects. Likely over-engineered for the need.

## Recommendation

**(a)** for this week. Try it at your next sign-off point. If the
convention holds in practice, formalise it in `SKILL.md` as a
documented pattern. If it feels fragile — promote to (b). Skip (c)
unless multi-invocation becomes a frequent workflow across multiple
projects.

The one concrete discipline: when you re-invoke `/reflect`
mid-session or end-of-day after a prior same-day run, tell me
explicitly that it's a re-invocation — that's the cue for me to (i)
add a time-of-day to the header, (ii) re-evaluate the
abductive-reasoning condition against "since last reflection," not
"this session," and (iii) skip `working-notes` if no new
observations accrued since the last entry.

That's the minimum viable discipline. If we hold it for a week and
the log stays clean, we document the pattern. If it drifts, we
promote to option (b).
