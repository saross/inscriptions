# Archive-search crash: diagnosis and safe-design recommendation

**Date:** 2026-06-21
**Author:** Claude (infra diagnosis session)
**Status:** Diagnosis + design recommendation. **NOT an implementation.** Hand this
to the infra session that will build the "search the archives" skill/agent.

> **RESOLVED 2026-06-21** — built in the personal-assistant repo. The §4 safety
> invariants (a–d) were all implemented; two recommendations changed on contact
> with the wider infrastructure:
>
> 1. **Index backend: PostgreSQL, not standalone SQLite FTS5.** This machine
>    already runs a `claude_memories` Postgres DB with `pg_trgm` + `pgvector` and
>    a synced `sessions` table; a fresh SQLite index would have duplicated that
>    query layer. Built a `session_chunks` table (per-turn prose, GENERATED
>    tsvector GIN + trigram) instead — integrated with the memory MCP. 470
>    sessions / 44,639 chunks indexed.
> 2. **Engine: pure-Python line scanner, not `rg -z`.** `rg` and `grep` on this
>    machine are shell *functions* routing to the Claude Code executable, not
>    standalone binaries — the §5 stopgap could not have run from a script, and
>    that harness ripgrep was itself the OOM-killed process in R1. The safe
>    fallback (`search-archives-safe.sh` → `_scan_archives.py`) keeps every §4
>    limit (nice/ionice/timeout/cgroup/flock) but does the scan in Python.
>
> Implemented: `scripts/{search-archives-safe.sh,_scan_archives.py,
> index-session-content.py,search-sessions.py}`, the `search_sessions` MCP tool,
> and the `/search-sessions` skill. See
> `personal-assistant/global-claude-md/infrastructure-reference.md`
> ("Searching past sessions — the escalation ladder").

> **Safety note for whoever reads this next:** the pattern diagnosed below crashed
> the machine once (mouse froze, all fans to maximum, hard lockup). The dangerous
> command was **not re-run** to produce this document — every number here was
> confirmed with metadata-only commands (`ls -la`, `du -sh`, `gzip -l`, `nproc`,
> `free -h`). Do not reproduce the crash to "verify" it.

---

## 1. Summary verdict

The crash was **not** caused by decompressed data size — the whole corpus is tiny
(~115 MB compressed, ~290 MB decompressed, against 22 GB free RAM). It was caused
by **running a line-oriented regex (`grep -oiE` with large bounded quantifiers) over
a single multi-megabyte "line"**: a prior `tr '\n' ' '` collapsed each ~25 MB JSONL
transcript into one ~25 MB line, and `grep -o` on one giant line scans and backtracks
roughly quadratically while buffering the whole line, pinning a CPU core per pipeline.
That pathology was then **multiplied by ~5 such pipelines left running concurrently in
the background**, racing the harness's own `ugrep`/`ripgrep` search hook, with **no
resource limits of any kind** — saturating all 16 cores (fans), driving memory
pressure into swap (mouse freeze), and ending in OOM/lockup.

**The single most important "never do this":** **never collapse newlines (`tr '\n' ' '`)
before feeding text to `grep`/`sed`/`awk`.** Line-oriented tools assume short lines;
a multi-megabyte line turns a linear scan into a pathological one. Keep the data
line-oriented and let the tool stream it.

---

## 2. Evidence

### Machine envelope (confirmed this session, metadata-only)

| Fact | Value | Source command |
|------|-------|----------------|
| CPU cores | **16** | `nproc` and `grep -c processor /proc/cpuinfo` |
| Total RAM | **30 GiB** | `free -h` |
| Free RAM at diagnosis | **22 GiB free / 24 GiB available** | `free -h` |
| Swap | **8.0 GiB total, 3.6 GiB already in use** | `free -h` |

Note the swap line: 3.6 GiB was *already* on swap at a quiet moment. Under the
concurrent-pipeline load, swap thrash is the most likely proximate cause of the
mouse freeze (interactive/UI pages get evicted under memory pressure).

### Corpus envelope (confirmed this session, metadata-only)

| Fact | Value | Source command |
|------|-------|----------------|
| Archive dir | `~/cc-archives/inscriptions/` | — |
| Session directories | **30** | `ls -d .../*/ \| wc -l` |
| `session.jsonl.gz` files | **30** | `ls .../*/session.jsonl.gz \| wc -l` |
| Total compressed | **115 MB** | `du -sh` |
| Largest compressed file | **14,998,990 B (~15 MB)** | `ls -la` |
| Largest decompressed | **24,910,932 B (~25 MB)**, ratio 39.8% | `gzip -l` (reads gzip trailer only) |
| Index present | `~/cc-archives/CATALOG.json`, **643,235 B**, schema 1.2, 503 total sessions | `ls -la` + JSON read |

Decompressed total ≈ 115 MB ÷ 0.40 ≈ **~290 MB** — under 1.3% of free RAM. **Raw size
was never the problem.** The largest single file decompresses to ~25 MB; after
`tr '\n' ' '` that became one **~25 MB line**, which is the toxic input.

### The crash commands (the suspects)

1. **Background pile-up of shell loops** — roughly five launched concurrently (the
   harness auto-backgrounded each; the operator relaunched more when old ones looked
   stuck), each of the form:

   ```bash
   for f in */session.jsonl.gz; do
     zcat "$f" | grep -oiE ".{0,140}rom[ae].{0,200}" | grep -iE "<keywords>"
   done
   ```

2. **The worst variant — newline collapse before grep:**

   ```bash
   zcat "$f" | tr '\n' ' ' | grep -oiE ".{0,120}rom[ae].{0,180}"
   ```

   This turns each ~25 MB JSONL file into **one ~25 MB line**, then runs `grep -oiE`
   with large bounded quantifiers (`.{0,120}` … `.{0,180}`) against that single line.

3. **Racing the harness's own search hook** — a `ugrep`/`ripgrep` background process
   (seen in a bash snapshot as `exec -a ugrep … ugrep -G …`) was running the
   harness's file-search and was observed OOM-**`Killed`**.

4. **No limits anywhere** — no `nice`, no `ionice`, no `ulimit`, no `timeout`, no
   concurrency cap, no cgroup.

### The safe-vs-crash contrast (the key clue)

A **later pure-Python scan** that iterated the decompressed stream **line by line**
(never collapsing newlines, bounded per-line regex, a single process) **completed
fine, no crash.** Same data, same machine. The only things that changed:
**line-oriented (not one giant line)**, **memory bounded to one line at a time**, and
**a single process instead of ~5 stacked**. That isolates the cause to the
*newline-collapse + giant-line regex + concurrency* combination, not the data volume.

---

## 3. Root cause and contributing factors, ranked

### Root cause (the pathology)

**R0. `grep -oiE` with large bounded quantifiers over a single multi-megabyte line.**
Line-oriented tools (`grep`, `sed`, `awk`) read and buffer a whole *line* at a time
and assume lines are short. After `tr '\n' ' '`, the "line" is ~25 MB. `grep -o`
must, for that one line, repeatedly try to match and emit *every* non-overlapping
occurrence; with bounded-but-large quantifiers (`.{0,120}…rom[ae]….{0,180}`) the
regex engine does substantial scanning/backtracking at many start positions across a
25-million-character string. Cost grows far worse than linearly in line length, so a
single pipeline pins one core near 100% and holds the whole line resident. This is the
pathology; everything else multiplies it.

> Distinction to carry into design: **R0 is a per-invocation pathology** — it would hurt
> even run once, sequentially. It is a *different* problem from R1/R2 below, which are
> about *how many* such invocations ran and the absence of guardrails. The fix for R0 is
> "stay line-oriented"; the fix for R1/R2 is "cap concurrency and impose limits". You
> need **both**.

### Contributing factors (amplifiers), ranked

**R1. Concurrency / background pile-up (primary amplifier).** ~5 pathological
pipelines running at once, plus the harness's own `ugrep` hook, saturated all 16
cores → fans to maximum. Each pipeline also held a ~25 MB line (plus `grep -o`
match buffers) resident; stacked, they pushed the working set past comfortable
limits and into **swap thrash** (3.6 GiB was already on swap), which is what froze
the cursor. One of the competing processes (`ugrep`) was OOM-**`Killed`**, confirming
genuine memory pressure, not just CPU.

**R2. No resource limits at all.** No `nice`/`ionice` meant the search competed on
equal footing with the interactive desktop for CPU and I/O. No `timeout` meant a
pipeline that *looked* stuck (because R0 made it genuinely slow, not hung) was never
killed — instead the operator launched *more*, compounding R1. No concurrency cap and
no cgroup meant nothing bounded the aggregate.

**R3. Operator feedback loop.** Because R0 made each pipeline slow and the harness
auto-backgrounded it silently, the pipelines *looked* hung. The natural response —
relaunch — was exactly wrong: it stacked load (→ R1). A correct design must make
progress visible and must **not** silently background long scans.

**R4. Decompressed size — explicitly NOT a primary factor.** ~290 MB decompressed
total vs 22 GB free. Memory exhaustion came from *many* multi-MB line buffers under
concurrency plus swap that was already partly consumed — not from the corpus being
large. Do not "fix" this by adding RAM; fix the pathology and the concurrency.

---

## 4. Safe-search design recommendations (prioritised)

For the infra session building the "search the archives" skill/agent. Ordered by
impact; (a)–(c) are non-negotiable invariants, (d) is the belt-and-braces wrapper,
(e) is the real fix.

### (a) NEVER collapse newlines before a line-oriented tool — invariant

No `tr '\n' ' '`, ever, upstream of `grep`/`sed`/`awk`/`rg`. JSONL is one JSON object
per line; keep it that way. If "context across lines" is wanted, get it from
line-oriented context flags (`rg -A/-B/-C`) or by parsing JSON, **never** by
flattening the file into one line. This single rule would have prevented the crash.

### (b) Use a gzip-native, line-oriented, memory-bounded tool — invariant

Replace the hand-rolled `zcat | tr | grep` with one of:

- **`rg -z`** (ripgrep) — decompresses gzip natively, streams line-by-line, bounded
  memory, fast, with `-A/-B/-C` for context and `--max-columns`/`-M` to defuse any
  accidental long line. **Preferred.**
- **`zgrep`** — line-oriented gzip grep; fine for simple patterns, slower than `rg`.

Both stay line-oriented and stream, so R0 cannot recur even on a pathological file.
Add **`-M 2000` (`--max-columns`)** as a defence-in-depth cap so that *if* some
transcript ever contains a genuinely long line, ripgrep truncates the display rather
than chewing on it.

### (c) Strictly sequential, or a hard concurrency cap of 1–2 — invariant

- Run searches **sequentially** by default (one file or one `rg` invocation at a time;
  `rg` already parallelises internally across files, so you usually want exactly **one**
  `rg` process over the whole tree, not a shell `for` loop spawning many).
- **Never background a search and relaunch it.** If the skill runs anything async, it
  must (i) cap concurrency at 1–2, (ii) track the running job, and (iii) refuse to
  start a second job while one is live. The background pile-up (R1/R3) was the primary
  amplifier; design it out.

### (d) Wrap every run in resource limits — belt and braces

Even with (a)–(c), wrap the search so a mistake cannot take the machine down:

- **`nice -n 19 ionice -c3 …`** — make the search yield CPU and I/O to the desktop, so
  a runaway degrades search speed, not interactivity.
- **`timeout 120 …`** — kill anything that overruns, so "looks stuck" becomes "is
  dead" instead of inviting a relaunch.
- **`systemd-run --user --scope -p MemoryMax=… -p CPUQuota=… …`** — a per-run cgroup
  that hard-caps memory and CPU. **This project already uses `systemd-run` cgroup caps
  for sapphire compute** — reuse that exact pattern here; do not invent a new one.
  Suggested starting caps for a corpus this small: `MemoryMax=2G`, `CPUQuota=400%`
  (≈4 of 16 cores), tighten after measuring. With these, even the original crash
  command would have been OOM-killed in its own scope **without touching the rest of
  the machine.**

A single composed wrapper is the goal, e.g. conceptually:
`systemd-run --user --scope -p MemoryMax=2G -p CPUQuota=400% nice -n 19 ionice -c3 timeout 120 rg -z …`

### (e) The real fix — search an index, not the raw `.gz` each time

Searching 30 gzipped transcripts on every query is wasteful and is what put us next to
the cliff. Build a **one-time content index** of the extracted user/assistant text and
search *that*:

- **What exists already:** `~/cc-archives/CATALOG.json` (schema 1.2, 503 sessions). It
  indexes **session-level metadata only** — `id`, `title`, `directory`, `started_at`,
  `duration_minutes`, `tags`, `purpose`, `subagent_count`, `subagent_cost_usd`. It does
  **NOT** contain transcript text, so it cannot answer a content query like "Rome near
  suggestion-keywords." Use it for *navigation* (which sessions/projects to scope to),
  not content search.
- **What to build:** a content index, extracted **once** per archived session by
  parsing the JSONL line-by-line (never collapsing newlines) and pulling the text
  fields of user/assistant turns. Two good options:
  - **SQLite FTS5** — a `sessions_fts(session_id, role, turn_idx, text)` virtual table.
    Gives ranked full-text queries, phrase/NEAR operators (ideal for "rom* NEAR
    keyword"), and millisecond lookups with no per-query decompression. **Preferred.**
  - **Flat plaintext sidecars** — one `*.txt` of extracted turns per session, then a
    single `rg` over the `.txt` tree. Simpler, still memory-bounded, but no ranking/NEAR.
- **Incremental maintenance:** index a session once at archive time (or lazily on first
  search, keyed on the `.gz` mtime/size), so steady-state search never decompresses
  anything. Store the index under `~/cc-archives/` next to `CATALOG.json`.
- The extractor is the *one* place gzip is read, and it must be line-oriented and run
  under the (d) wrapper.

---

## 5. Safe interim recipe (stopgap — paste today)

> **STOPGAP ONLY.** Use this until the indexed skill from §4(e) exists. It is bounded,
> sequential, and resource-capped. It does **not** collapse newlines and does **not**
> background anything.

```bash
# One ripgrep process over the whole archive tree. Gzip-native, line-oriented,
# memory-bounded. nice+ionice yield to the desktop; timeout kills overruns;
# -M caps any pathological long line; -i case-insensitive; -C2 gives context.
# Run it in the FOREGROUND and wait for it; do NOT relaunch if it seems slow.

nice -n 19 ionice -c3 timeout 120 \
  rg -z -i -M 2000 -C2 \
     -e 'rom[ae]' \
     ~/cc-archives/inscriptions/

# To AND-filter for suggestion keywords, pipe ONE rg into a second line-oriented
# rg (still no tr, still streaming, still bounded):
nice -n 19 ionice -c3 timeout 120 \
  rg -z -i -M 2000 -C2 -e 'rom[ae]' ~/cc-archives/inscriptions/ \
  | rg -i -e 'suggest|recommend|propose|<your-keywords>'
```

Optional hard cgroup cap (reuses the project's existing sapphire `systemd-run` pattern;
even a mistake stays inside the scope):

```bash
systemd-run --user --scope -p MemoryMax=2G -p CPUQuota=400% \
  nice -n 19 ionice -c3 timeout 120 \
  rg -z -i -M 2000 -C2 -e 'rom[ae]' ~/cc-archives/inscriptions/
```

**Do NOT:** use `tr '\n' ' '`; use `grep -o` with large bounded quantifiers on
unbounded lines; run more than one search at a time; background a search and relaunch
it; or run any of this without `nice`/`timeout`.

---

## Appendix — confirmed numbers (all metadata-only)

- `nproc` → 16; `grep -c processor /proc/cpuinfo` → 16
- `free -h` → Mem 30Gi total / 22Gi free / 24Gi available; Swap 8.0Gi total / 3.6Gi used
- `du -sh ~/cc-archives/inscriptions/` → 115M
- largest `session.jsonl.gz` → 14,998,990 B; `gzip -l` → 24,910,932 B uncompressed (39.8%)
- 30 session directories, 30 `session.jsonl.gz` files
- `~/cc-archives/CATALOG.json` → 643,235 B, schema 1.2, total_sessions 503;
  per-session fields are metadata only (no transcript text)
