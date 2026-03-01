# `git status -sb && echo "---" && git diff --stat HEAD~1` — show repo status and what changed in the last commit

## Full command
```bash
git status -sb && echo "---" && git diff --stat HEAD~1
```

## What it does
Shows two things at once: (1) which files are currently modified or untracked in your working folder, and (2) a summary of what files changed in the most recent commit — how many lines were added or removed per file.

## Breaking it down

| Part | Meaning |
|------|---------|
| `git status` | lists files that have been changed, added, or deleted |
| `-s` | "short" — compact one-line-per-file output instead of the long default |
| `-b` | also show which branch you're on and whether it's ahead/behind the remote |
| `&&` | only run the next command if the previous one succeeded |
| `echo "---"` | prints a separator line so the two outputs are easy to tell apart |
| `git diff` | shows differences between two points in history |
| `--stat` | summary mode — shows filenames + lines added/removed, not the full line-by-line diff |
| `HEAD~1` | "one commit before the current one" — so this shows what the last commit changed |

## Danger level
- **Safe** — read-only, changes nothing

## When to use it
Before writing a commit message — gives you a quick picture of both what's uncommitted right now and what the previous commit contained, so you can write an accurate message.

## When NOT to use it
If you want to see the actual line-by-line content of changes (not just the summary), use `git diff HEAD~1` without `--stat`.
