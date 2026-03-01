# AI Assistant Instructions

This file defines how the AI assistant should behave in this repository.
It covers three workflows: knowledge capture, git commits, and code review.

---

## 1. Knowledge Capture

**Trigger:** When the user says "save this", "capture this", "document this", "remember this", "write this down", or wants to preserve a useful answer, solution, pattern, or decision from the chat.

Classify the content into exactly ONE of 5 doc types, then show a preview and ask for confirmation before writing anything.

### Doc Types

| Type | Use when content... | Folder | Filename |
|------|---------------------|--------|----------|
| **Decision** | Compares options, explains trade-offs, records why something was chosen | `docs/decisions/` | `YYYY-MM-DD-kebab-title.md` |
| **Runbook** | Gives step-by-step instructions to set up or operate something | `docs/runbooks/` | `kebab-title.md` |
| **Pattern** | Shows the correct/preferred way to write code for a recurring problem | `docs/patterns/` | `kebab-title.md` |
| **Lesson** | Debugs an error, warns about a gotcha, identifies a root cause, "don't do X" | `docs/lessons/` | `YYYY-MM-DD-kebab-title.md` |
| **Command** | Explains a shell/bash command the user doesn't recognise | `docs/commands/` | `kebab-command-name.md` |

**Date prefix rule:** Decision and Lesson filenames get a `YYYY-MM-DD-` prefix (historical records). Runbook, Pattern, and Command do not (living references).

### Templates

**Decision**
```markdown
# Why we chose [X]
**Date:** YYYY-MM-DD
## Context
## Options Considered
- **Option A** — description
- **Option B** — description
## Decision
We chose **Option A**.
## Reasons
## Trade-offs Accepted
```

**Runbook**
```markdown
# How to [do X]
## Prerequisites
## Steps
1. Step one
2. Step two
   ```bash
   command here
   ```
## Verify It Worked
## Notes
```

**Pattern**
```markdown
# The right way to [do X]
## Context
## Pattern
```python
correct_code_here()
```
## Why This Way
## When NOT to Use
```

**Lesson**
```markdown
# [What broke / What to never do]
**Date:** YYYY-MM-DD
## What Happened
```python
# bad example
```
## Why It's a Problem
## Fix / Do This Instead
```python
# correct approach
```
## Prevention
One-line rule.
```

**Command**
```markdown
# `command` — what it does in one line
## Full command
```bash
exact command here
```
## What it does
Plain English. No jargon.
## Breaking it down
| Part | Meaning |
|------|---------|
| `cmd` | base program |
| `-flag` | what this flag does |
## Danger level
Safe / Caution / Destructive
## When to use it
## When NOT to use it
```

### Save Workflow

1. Identify the most valuable insight in the recent response
2. Classify into exactly one doc type
3. Fill the template with real content (no placeholder text)
4. Show the user:
   ```
   📄 Proposed file: docs/patterns/example.md
   Type: Pattern
   --- PREVIEW ---
   [full file content]
   ---
   Save this file and update KNOWLEDGE.md? (yes / edit / skip)
   ```
5. On approval: create folder if needed, write the file, append one line to `KNOWLEDGE.md` at the project root

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
## Commands
- [Title](docs/commands/title.md)
```
If `KNOWLEDGE.md` doesn't exist, create it with all 5 section headings first.

---

## 2. Git Commits

**Trigger:** When the user says "commit", "commit this", or asks to create a git commit.

### Commit message format

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

### Commit types

| Type | Use |
|------|-----|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no logic change |
| `refactor` | Refactoring, no feature/bug change |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `build` | Build system or dependency changes |
| `ci` | CI configuration changes |
| `chore` | Other maintenance |
| `revert` | Reverting a commit |

### Audience

Commit messages are written for **project managers with limited technical background**. Write in Japanese.

- For functional changes: explain what changed in plain language, use bullet points for each change area
- For minor changes (config, docs, style): keep it to 1–2 lines
- Always clarify what changed (what) and why (why)
- Start with a verb: 「〜を修正」「〜を追加」「〜を改善」
- Keep the subject line under 72 characters

### Workflow

1. Run `git status --porcelain` and `git diff` to understand changes
2. Stage relevant files (never commit `.env`, credentials, or secrets)
3. Determine type and scope from the diff
4. Write the commit message in Japanese following the format above
5. Run `git commit -m "..."` using a heredoc for multi-line messages

### Safety rules

- Never modify git config
- Never use `--force`, `--hard reset`, or `--no-verify` unless explicitly requested
- Never force-push to main/master
- If a pre-commit hook fails, fix the issue and create a NEW commit — do not amend

---

## 3. Code Review

**Trigger:** When the user says "review my code", "review this", or asks for a code review.

### Severity levels

| Level | Name | Action |
|-------|------|--------|
| **P0** | Critical — security vulnerability, data loss, correctness bug | Must fix before merge |
| **P1** | High — logic error, significant SOLID violation, performance regression | Should fix before merge |
| **P2** | Medium — code smell, maintainability concern | Fix in this PR or follow-up |
| **P3** | Low — style, naming, minor suggestion | Optional |

### Review workflow

1. Run `git diff` to scope the changes
2. Check for SOLID violations:
   - **SRP**: Does this module have one reason to change?
   - **OCP**: Can new behaviour be added without editing existing code?
   - **LSP**: Can subclasses be substituted without callers noticing?
   - **ISP**: Do all implementers use all interface methods?
   - **DIP**: Is high-level logic coupled to concrete implementations?
3. Check for security risks: injection, path traversal, secret leakage, unbounded loops, missing auth checks, race conditions (TOCTOU)
4. Check for code quality issues: swallowed exceptions (bare `except Exception`), N+1 queries, missing null/empty checks, magic numbers
5. Identify removal candidates: unused code, dead branches, redundant logic

### Output format

```markdown
## Code Review Summary
**Files reviewed**: X files, Y lines changed
**Overall assessment**: APPROVE / REQUEST_CHANGES / COMMENT

## Findings

### P0 - Critical
(none or list)

### P1 - High
1. **[file:line]** Title
   - Issue description
   - Suggested fix

### P2 - Medium
### P3 - Low

## Removal/Iteration Plan
(if applicable)
```

After findings, always ask:

```
I found X issues (P0: _, P1: _, P2: _, P3: _).

How would you like to proceed?
1. Fix all
2. Fix P0/P1 only
3. Fix specific items
4. No changes needed
```

**Do NOT implement fixes until the user explicitly confirms.**
