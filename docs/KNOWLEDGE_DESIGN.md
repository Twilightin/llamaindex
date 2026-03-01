# Knowledge Base Design — Approved

> **Status:** Approved. This doc defines the structure the `/capture` skill generates.

---

## 1. Doc Types (Final — 4 types)

| # | Type | One-line purpose | Triggered when response contains... | Folder | Filename format |
|---|------|-----------------|--------------------------------------|--------|-----------------|
| 1 | **Decision** | Record *why* a choice was made | Comparison of options, trade-off reasoning, "we chose X because" | `docs/decisions/` | `YYYY-MM-DD-short-title.md` |
| 2 | **Runbook** | Record *how* to do a repeatable task | Step-by-step setup, commands, config instructions | `docs/runbooks/` | `short-title.md` |
| 3 | **Pattern** | Record *what works* as a reusable solution | Code snippet with explanation, "the right way to do X" | `docs/patterns/` | `short-title.md` |
| 4 | **Lesson** | Record *what broke* and *what to avoid* | Error + fix, warning, "don't do X", root cause analysis | `docs/lessons/` | `YYYY-MM-DD-short-title.md` |

**Note:** Postmortem and Anti-pattern are merged into **Lesson** — both are historical records from failure events, serving the same reader need: "what went wrong and what do I never do again."

---

## 2. Filename Convention

| Type | Date prefix? | Reason |
|------|:------------:|--------|
| Decision | Yes | Historical record — *when* a decision was made matters |
| Lesson | Yes | Tied to a specific event — correlates with git history |
| Runbook | No | Living reference — updated in place, date becomes stale noise |
| Pattern | No | Living reference — either valid or not, updated in place |

---

## 3. Templates

### Decision — `docs/decisions/YYYY-MM-DD-short-title.md`

```markdown
# [Why we chose X]

**Date:** YYYY-MM-DD

## Context
What problem were we solving? What constraints existed?

## Options Considered
- Option A — brief description
- Option B — brief description

## Decision
We chose **Option A**.

## Reasons
- Reason 1
- Reason 2

## Trade-offs Accepted
- What we gave up or accepted as a downside
```

---

### Runbook — `docs/runbooks/short-title.md`

```markdown
# [How to do X]

## Prerequisites
- What must already be true before starting

## Steps
1. Step one
2. Step two
   ```bash
   example command
   ```
3. Step three

## Verify It Worked
How to confirm the task succeeded.

## Notes
Edge cases, platform differences, or caveats.
```

---

### Pattern — `docs/patterns/short-title.md`

```markdown
# [The right way to do X]

## Context
When does this pattern apply?

## Pattern

```python
# The correct implementation
code_example_here()
```

## Why This Way
What makes this the preferred approach?

## When NOT to Use
Constraints or cases where this pattern breaks down.
```

---

### Lesson — `docs/lessons/YYYY-MM-DD-short-title.md`

```markdown
# [What broke / What to never do]

**Date:** YYYY-MM-DD

## What Happened
Symptom or the tempting bad pattern.

```python
# What went wrong or what NOT to do
bad_example()
```

## Why It's a Problem
Root cause or why the bad pattern fails.

## Fix / Do This Instead

```python
# Correct approach
good_example()
```

## Prevention
One-line rule to remember.
```

---

## 4. Hub File — `KNOWLEDGE.md` (root)

Auto-updated by `/capture` on every save. One line per entry.

```markdown
# Project Knowledge Base

## Decisions
- [Why we chose ChromaDB](docs/decisions/2026-03-01-why-chromadb.md)

## Runbooks
- [ChromaDB local setup](docs/runbooks/chromadb-setup.md)

## Patterns
- [Standard query engine pattern](docs/patterns/llamaindex-query-engine.md)

## Lessons
- [CollectionNotFoundError — missing --path flag](docs/lessons/2026-03-01-collection-not-found.md)
```

---

## 5. Skill Behaviour

1. User invokes `/capture`
2. Skill reads recent conversation, identifies the most valuable content
3. Classifies it into one of the 4 types
4. Fills in the correct template
5. **Always shows the user the proposed file path + full content for confirmation**
6. On approval: writes the file, then appends one line to `KNOWLEDGE.md`
