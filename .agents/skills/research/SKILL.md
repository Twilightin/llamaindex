---
name: research
description: "Research and create an implementation plan for a LlamaIndex feature BEFORE writing any code. Invokes the llamaindex-researcher sub-agent to investigate the topic, produce a detailed plan file, and report back. Use this before starting any new feature or when unsure of the best LlamaIndex pattern to use."
disable-model-invocation: false
allowed-tools: Read, Write, Agent
---

# Research — Research First, Code Second

You have been asked to research and plan the following:

**Topic**: $ARGUMENTS

## Your Steps

1. **Check context.md** — read `.claude/task/context.md` to understand current project state and avoid duplicating existing plans.

2. **Delegate to llamaindex-researcher** — launch the `llamaindex-researcher` sub-agent with the topic above. It will:
   - Research the best LlamaIndex approach
   - Save a detailed implementation plan to `.claude/task/`
   - Update `context.md`
   - Return a concise summary

3. **Report to the user** — after the researcher completes, show the user:
   - The path to the plan file
   - The key findings (from the researcher's summary)
   - Confirm: "Ready to implement. Say 'go' when you want me to start coding."

## Important

Do NOT start writing any code until the user explicitly confirms. The plan must be reviewed first.
