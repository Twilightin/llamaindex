# Skill Execution Output — eval-3-lesson

## Classified Doc Type

**Lesson**

The content debugs a specific error (CollectionNotFoundError), identifies a root cause (missing --path flag), warns about a bad pattern (calling `chroma run` without `--path`), and provides a fix. This matches the Lesson type exactly: "Debugs an error, warns about a gotcha, identifies a root cause, says 'don't do X'."

---

## Proposed Filename and Folder Path

- **Folder:** `docs/lessons/`
- **Filename:** `2026-03-01-chroma-run-requires-path-flag.md`
- **Full path:** `docs/lessons/2026-03-01-chroma-run-requires-path-flag.md`

(Lessons get a date prefix because they are historical records.)

---

## Complete File Content (shown for confirmation)

```
Proposed file: docs/lessons/2026-03-01-chroma-run-requires-path-flag.md
Type: Lesson

--- PREVIEW ---
# Never start ChromaDB without the --path flag

**Date:** 2026-03-01

## What Happened

`CollectionNotFoundError` was thrown after the ChromaDB server restarted. The root cause was that `chroma run` was called without the `--path` flag, so ChromaDB started in in-memory mode. Any collections created in a previous session were lost on restart.

```bash
# What NOT to do
chroma run
```

## Why It's a Problem

Without `--path`, ChromaDB runs entirely in memory. No data is persisted to disk. When the server restarts — for any reason — all collections and their embeddings are silently lost. The `CollectionNotFoundError` at query time is the symptom, but the real failure happened at startup.

## Fix / Do This Instead

Always provide the `--path` flag pointing to a directory on disk when starting the ChromaDB server:

```bash
# Correct approach — data is persisted across restarts
chroma run --path ./chroma_db
```

Create the `./chroma_db` directory before first use if it does not already exist. Use the same path consistently across all environments (local dev, CI, production) to avoid environment-specific surprises.

## Prevention

One-line rule: never start Chroma without `--path` in any environment.
---

Save this file and update KNOWLEDGE.md? (yes / edit / skip)
```

---

## KNOWLEDGE.md Update

**Would update KNOWLEDGE.md:** Yes

**Line to add** (under the `## Lessons` section):

```
- [Never start ChromaDB without the --path flag](docs/lessons/2026-03-01-chroma-run-requires-path-flag.md)
```

If `KNOWLEDGE.md` does not exist at the project root, the skill would create it with all four section headings (Decisions, Runbooks, Patterns, Lessons) and then append this line under `## Lessons`.
