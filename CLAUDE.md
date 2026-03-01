# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python/LlamaIndex backend project. Currently in early setup — the virtualenv exists but no packages are installed yet and no source files have been written.

## Environment

- Python 3.12 virtualenv at `backend/venv/`
- OpenAI API key stored in `.env` (root level, gitignored)

Activate the virtualenv:
```bash
source backend/venv/bin/activate
```

Install packages into the venv (do not use system Python):
```bash
pip install <package>
```

## Environment Variables

`.env` is gitignored. Required variables:
- `OPENAI_API_KEY` — OpenAI API key for LlamaIndex

## Git Workflow

Commits use [Conventional Commits](https://www.conventionalcommits.org/) format and are written in Japanese, targeting a PM audience with limited technical background. See `.agents/skills/git-commit/SKILL.md` for the full commit message guidelines.

Use the `/git-commit` skill to create commits.
