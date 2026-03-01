---
name: capture
description: "Saves valuable insights from the current conversation into structured .md files. Use this skill whenever the user says 'save this', 'capture this', 'save to knowledge base', '/capture', 'remember this', 'document this', 'write this down', or wants to preserve a useful answer, solution, pattern, or decision from the chat. Even if the user just says 'save' or 'keep this', trigger this skill. The skill classifies the content into one of 4 doc types (Decision, Runbook, Pattern, Lesson), applies the correct template, asks for confirmation, writes the file, and updates KNOWLEDGE.md at the project root."
allowed-tools: Read, Write, Edit, Bash
---

# Capture — Knowledge Base Writer

You save valuable insights from the conversation into structured `.md` files so nothing important gets lost in chat history.

## Step 1 — Identify the content

Read the recent conversation. Find the most valuable insight in the **last AI response** (or the section the user is pointing to). Extract and summarize it — do not copy-paste raw chat text. The goal is a clean, standalone document a future reader can understand without the chat context.

## Step 2 — Classify into exactly one doc type

Pick the ONE type that best fits the content's primary purpose:

| Type | Classify when the content... | Folder | Filename |
|------|------------------------------|--------|----------|
| **Decision** | Compares options, explains trade-offs, records why something was chosen | `docs/decisions/` | `YYYY-MM-DD-kebab-title.md` |
| **Runbook** | Gives step-by-step instructions to set up or operate something | `docs/runbooks/` | `kebab-title.md` |
| **Pattern** | Shows the correct/preferred way to write code for a recurring problem | `docs/patterns/` | `kebab-title.md` |
| **Lesson** | Debugs an error, warns about a gotcha, identifies a root cause, says "don't do X" | `docs/lessons/` | `YYYY-MM-DD-kebab-title.md` |

**Date prefix rule:** Decision and Lesson get today's date prefix (they are historical records). Runbook and Pattern do not (they are living references, updated in place).

If the content genuinely spans two types, pick the one that serves a future reader better. If you truly cannot classify it, ask the user.

## Step 3 — Fill in the template

Use the exact template for the classified type. Fill every section with real content — do not leave placeholder text.

### Decision template
```markdown
# Why we chose [X]

**Date:** YYYY-MM-DD

## Context
What problem were we solving? What constraints existed?

## Options Considered
- **Option A** — brief description
- **Option B** — brief description

## Decision
We chose **Option A**.

## Reasons
- Reason 1
- Reason 2

## Trade-offs Accepted
- What we gave up or accepted as a downside
```

### Runbook template
```markdown
# How to [do X]

## Prerequisites
- What must already be true before starting

## Steps
1. Step one
2. Step two
   ```bash
   command here
   ```
3. Step three

## Verify It Worked
How to confirm the task succeeded.

## Notes
Edge cases, platform differences, or caveats.
```

### Pattern template
```markdown
# The right way to [do X]

## Context
When does this pattern apply?

## Pattern
```python
# correct implementation
code_here()
```

## Why This Way
What makes this the preferred approach over alternatives?

## When NOT to Use
Constraints or cases where this pattern breaks down.
```

### Lesson template
```markdown
# [What broke / What to never do]

**Date:** YYYY-MM-DD

## What Happened
Symptom observed, or the tempting bad pattern.

```python
# What went wrong or what NOT to do
bad_example()
```

## Why It's a Problem
Root cause, or why the bad pattern fails.

## Fix / Do This Instead

```python
# Correct approach
good_example()
```

## Prevention
One-line rule to remember going forward.
```

## Step 4 — Show the user for confirmation

Present the proposed output clearly before writing anything:

```
📄 Proposed file: docs/decisions/2026-03-01-why-chromadb.md
Type: Decision

--- PREVIEW ---
[full file content here]
---

Save this file and update KNOWLEDGE.md? (yes / edit / skip)
```

Wait for explicit user approval. Never write without confirmation.

## Step 5 — Write the file and update KNOWLEDGE.md

On approval:

1. Create the target folder if it doesn't exist
2. Write the `.md` file
3. Update `KNOWLEDGE.md` at the **project root**:
   - If `KNOWLEDGE.md` doesn't exist, create it with all 4 section headings
   - Append exactly one line under the correct section heading

### KNOWLEDGE.md structure
```markdown
# Project Knowledge Base

## Decisions
- [Title](docs/decisions/YYYY-MM-DD-title.md)

## Runbooks
- [Title](docs/runbooks/title.md)

## Patterns
- [Title](docs/patterns/title.md)

## Lessons
- [Title](docs/lessons/YYYY-MM-DD-title.md)
```

Confirm to the user: "Saved to `<path>` and added to `KNOWLEDGE.md`."

## Edge cases

- **User points at a specific part of the chat:** Use that section, not the whole response.
- **Content fits no type:** Ask the user: "This looks like [X] — should I save it as a [Lesson] or a different type?"
- **File already exists with the same name:** Read the existing file, merge the new content in, don't overwrite blindly.
- **User says "edit" at confirmation:** Ask what they want to change, update the preview, confirm again.
