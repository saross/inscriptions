# Agents used in this run

## Proposer — data-profile-scout

- **Canonical definition:** `~/personal-assistant/agents/data-profile-scout.md`.
- **Repo + commit at time of use:** `saross/personal-assistant`; commit recorded here after the agent-definition commits on 2026-04-23 (will be filled in before launch).
- **Execution vehicle for this run:** `general-purpose` agent (Agent tool, `subagent_type=general-purpose`). The named `data-profile-scout` agent was defined today and is not yet in this session's routing table; inlining the full methodology in the invocation brief gives equivalent behaviour for one-shot use. Future sessions will invoke the named agent directly.
- **Brief:** `./briefs/data-profile-scout-brief.md` — inlines the methodology from the canonical definition plus this run's specific inputs.

## Verifier — data-profile-verifier

- **Canonical definition:** `~/personal-assistant/agents/data-profile-verifier.md`.
- **Repo + commit at time of use:** `saross/personal-assistant`; commit recorded here after the agent-definition commits on 2026-04-23 (will be filled in before launch).
- **Execution vehicle for this run:** `general-purpose` agent, same reason as the proposer.
- **Brief:** `./briefs/data-profile-verifier-brief.md`.
- **Dispatch pattern:** serial. Launch proposer → await completion → launch verifier against proposer output. No nested sub-agent spawning (follows the lit-scout case-study "main-conversation chaining" pattern rather than the unrealisable "sub-agent dispatches verifier" pattern).

## Auxiliary tools invoked via Skill

- `/review-implementation` on the design (spec + both agent definitions) before launch.
- `/improve-prompt` on each brief before launch.

## What is NOT in use

- No worktrees — the run reads a read-only parquet and writes to `outputs/`; no branch-level isolation needed.
- No external paid APIs — `/phase-gate` does not fire.
- No Zotero or Zenodo writes.
