---
priority: 1
scope: in-stream
title: "Continuity message — end of 2026-04-23 session"
audience: "next CC instance picking up the project"
---

# Continuity — inscriptions project, end of 2026-04-23

## Who you're picking up

CC on the inscriptions project (`~/Code/inscriptions`) with Shawn Ross (archaeologist + ancient historian, Macquarie; co-author Adela Sobotková at Aarhus SDAM). Today's session ran ~14 hours across two calendar days — substantial. Git should be clean on entry; verify with `git status` and `git log --oneline -10`.

## Working-relationship register — read this first

Shawn has explicitly set up a trusted-colleague / critical-friend register, not helpful-assistant. Concretely:

- **Lab-not-dev-team** mental model. He's PI; main-thread CC is senior analyst / RSE; agents are specialist consultants for discrete tasks. Peer review + Adela are critical friends outside the thread.
- **Critical-friend on statistics is a standing rule** (in `~/personal-assistant/data/scratchpad.md`). For every statistical choice — his or yours — run four checks: is there (a) a more appropriate test for the data structure, (b) a more powerful / robust alternative, (c) a more current best-practice approach, (d) do the method's assumptions actually hold? If yes to any, surface before executing. Applies to your own proposals too.
- **Context-management is not defensive.** 50-75 % is the operating band. Don't pre-empt by truncating; don't skip skill invocations to save tokens. Shawn /reflect-and-exits around 50 %, gets aggressive at 75 %.
- **Pre-launch review for phase / block implementations.** Spec the block together before launching agents. Don't auto-execute large blocks without his sign-off.
- **Invoke skills fully.** We cut the `/improve-prompt` corner today once; avoid. If a skill is the right tool, invoke the Skill tool and work through the protocol.
- **Commit before each pipeline stage** (from scratchpad). Research-record preservation matters.
- **Push back when warranted.** Explicit standing invitation.
- **Sapphire for compute.** Any bootstrap sweeps, permutation tests, or CPU-intensive work runs on sapphire via SSH (`~/Code/inscriptions` on sapphire cloned and synced; `.venv` there has all deps). Workdir is `~/Code/inscriptions`, not `~/inscriptions` — typo caused an agent stall today.

## Where the research is — two sentences

We profiled LIRE v3.0 (182,853 × 63; Rome = 35.8 %; zero negative date ranges; massive century-midpoint inflation at 22–41× but on `mid` values, not on aoristic-weighted SPAs). Main SPA paper architecture is set in Decision 7 (deconvolution-mixture primary + thresholded robustness in body + stratification in appendix + baorista comparative in appendix); Saturday 2026-04-25 is a feasibility doc to Adela; Friday is a min-thresholds simulation draft; paper sprint runs three weeks after Saturday.

## Immediate timeline

- **Thursday 2026-04-24**: OSF preregistration draft for min-thresholds simulation (evening work Shawn wants to do together). Deconvolution-mixture pilot on one province. Extended editorial-spikes test on 14 boundary years per Obs 11 hypothesis (AD 68, 69, 96, 117, 138, 161, 180 + existing 7; Hanson 2021 PDF check for letter-count claim.
- **Friday 2026-04-25**: min-thresholds simulation + draft to Adela.
- **Saturday 2026-04-26**: feasibility doc + paper skeleton to Adela (1-page analysis plan + 4–6 pages detail).
- **Sunday 2026-04-27 or Monday 2026-04-28**: baorista install on sapphire (R + NIMBLE + C++). Pilot on LIRE subset.
- **Sunday 2026-05-03** (end of Week 1 of paper sprint): **scope-commitment checkpoint** — commit single paper vs methods/results split per Decision 7 criteria. No later.

## Artefacts that matter — priority order

- `planning/decision-log.md` — 7 ADRs. Decision 7 is the paper architecture (deconvolution primary + robustness + scope-commitment path).
- `planning/future-studies.md` — FS-0 (methods/results split contingency), FS-1 (Aeneas-partition paper), FS-2 (deconvolution mixture, elevated to main paper).
- `planning/backlog-2026-04-22.md` — timeline, immediately-actionable, preliminary signals to watch for.
- `planning/ai-contributions.md` — log of substantive AI intellectual contributions (Shawn's research-record practice). New entries here when you propose something non-trivial that shapes research direction. Two entries today.
- `planning/memos/2026-04-23-reflect-multi-invocation.md` — `/reflect` safety option (a) endorsed; subsequent-invocation cue convention.
- `planning/bibliography-2026-04-22.md` + `bibliography-aeneas-2026-04-23.md` + `inscriptions-spa.bib` + `inscriptions-aeneas.bib` — verified bibliographies.
- `docs/notes/reflections/working-notes.md` — 11 numbered observations. Obs 10 and 11 are `[PATTERN]` tagged (computational-sibling seeding; editorial-convention hierarchy hypothesis).
- `docs/notes/reflections/reasoning-log.md` — narrative in-stream; session texture.
- `docs/notes/reflections/abductive-reasoning.md` — Entry 1 on lit-scout verifier zero-correction surprise (belief revision about Guard-A's load-bearing role).
- `runs/2026-04-23-descriptive-stats/` — complete run record: spec, briefs, seed, code, outputs (1,305 claims, verifier PARTIAL 1303/1330 pass), decisions.
- `planning/paper-outlines/aeneas-partition.md` — follow-up paper outline.

## Things I'm watching for (Shawn's "keep eyes open" request)

1. **Deconvolution-mixture pilot quality** (Thursday). Clean first-attempt → methodology compact → single paper. Tuning required → grows → split candidate.
2. **baorista install cost** (Sun / Mon). Non-trivial → may need to downgrade from "run properly" to "citation with rationale."
3. **Obs 11 hypothesis test** (Thursday). Prediction: AD 96 and AD 180 dip (near rounds); AD 138 and AD 161 spike (far from rounds); AD 68, 69, 117 mid-range. If holds, informs `convention_SPA` shape in the mixture (hierarchical weighted attractors, not uniform century slabs).
4. **Aeneas-partition outline depth**. If it grows during drafting into a full paper independently, confirms FS-1 as Paper B; main paper stays single.
5. **Field convention on methods-first vs combined structure** (opportunistic quick check). How did Timpson / Crema structure their Neolithic SPD papers? Informs default scope.

## Open known-unknowns

- **Hanson 2021 letter-count claim unverified** (Obs 8). PDF check before any draft cites Hanson 2021 as the letter-count source.
- **AD 2230 placeholder values** in LIRE `not_after` column. Action: Shawn reports to LIRE / SDAM team. He may have reported AD 2230 before; confirm before nagging.
- **May 2026 conference details** — venue, date, abstract deadline, format all TBC.
- **Effect-size targets for min-thresholds** — (a) 50 % sustained over ≥50 y (headline for Adela); (b) doubling over ≥25 y; (c) 20 % over ≥25 y bracket. Run all three; (a) primary.

## Failure modes observed today — avoid

- **Path typo in agent briefs.** Sapphire workdir is `~/Code/inscriptions`. A typo (`~/inscriptions`) caused an agent to stall on failed `cd`.
- **pgrep self-match on polling loops.** `pgrep -f "python3.*verify.py"` matches its own invoking shell command because the regex pattern appears in its command line. Use `pgrep -f "[.]venv/bin/python3.*verify.py"` (bracket-escaped) OR `kill -0 <specific_pid>` OR capture the PID via `pgrep ... -o` once and check that specific PID.
- **Agent stalling on inline script streaming.** When composing a long Python script, an agent streamed it as chat text; watchdog killed it at 600s. Fix: put script content in Write tool's `content` parameter; do not paste as chat text. Make this explicit in agent briefs.
- **Monitor loops tripping on stale files.** A verifier-completion monitor keyed on `verifier.log` existence fired immediately because a stale file from a previous run was present. Prefer file-mtime checks or fresh-run markers over existence checks.

## Session texture worth remembering

Manager-mode experiment held for most of the day. Two places where critical-friend push-back materially improved outcomes: (i) when Shawn invited push-back on my four-co-equal-methods plan, I revised to one-primary-plus-robustness (Decision 7) and the paper architecture got crisper; (ii) when Shawn asked "can Aeneas re-date inscriptions," I reframed to variance-not-mean partitioning and we landed on a novel methodology sidestepping training-data circularity. Both in `ai-contributions.md`.

The "more methods isn't more rigour" lesson is worth internalising: fewer chosen methods with better-stated rationale reads stronger than a smorgasbord of approaches.

The editorial-hierarchy hypothesis (Obs 11) emerged from Shawn's sharp observation that the AD 235 peak contradicts the AD 97 dip — good example of his pattern-recognition pushing the methodology harder than the aggregate results did.

Shawn publishes ~2 articles/year in Q1 journals. Rigour bar is non-negotiable; quality > speed; honest uncertainty > performed confidence.

## If context feels cold

Start: `docs/notes/reflections/reasoning-log.md` Entry 1 (today's texture) + `planning/decision-log.md` (scan the 7 ADRs, especially Decision 7) + `planning/backlog-2026-04-22.md` §§0-3b (timeline and immediately-actionable). Skip the full run outputs unless you need specific numbers.

Verifier verdict: PARTIAL, 1303/1330 pass, 27 major (not critical), method-as-implemented all pass. Don't re-run; it's done.
