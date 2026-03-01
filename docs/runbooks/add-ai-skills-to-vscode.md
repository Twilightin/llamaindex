# How to add AI skills to VS Code

## Prerequisites
- VS Code installed
- GitHub Copilot extension installed, OR Claude Code installed

## Steps

### Option A — Claude Code users (VS Code terminal)

```bash
claude install https://github.com/Twilightin/ai-skills/tree/main/skills/capture
claude install https://github.com/Twilightin/ai-skills/tree/main/skills/code-review-expert
claude install https://github.com/Twilightin/ai-skills/tree/main/skills/git-commit
```

### Option B — GitHub Copilot, per project

Run once in the VS Code terminal inside any project:

```bash
mkdir -p .github && curl -o .github/copilot-instructions.md \
  https://raw.githubusercontent.com/Twilightin/ai-skills/main/.github/copilot-instructions.md
```

Copilot picks it up immediately — no restart needed.

### Option C — GitHub Copilot, global (all projects)

Open VS Code User Settings JSON (`Cmd+Shift+P` → "Open User Settings JSON") and add:

```json
"github.copilot.chat.codeGeneration.instructions": [
  {
    "url": "https://raw.githubusercontent.com/Twilightin/ai-skills/main/.github/copilot-instructions.md"
  }
]
```

This applies all skills to every project on the device automatically.

## Verify It Worked

- **Claude Code:** type `/capture` or "review my code" — the skill should trigger
- **Copilot:** open Copilot Chat, ask "review my code" — it should follow the P0/P1/P2/P3 format

## Notes
- Option C (global) is the recommended approach for a shared team device
- The skills repo is at `https://github.com/Twilightin/ai-skills`
- Copilot users do not need Claude installed at all
