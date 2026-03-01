# Project Context — Single Source of Truth

> All sub-agents MUST read this file before starting any work.
> After completing research or planning, sub-agents MUST update the "Progress Log" section below.

---

## Project Overview

**Name**: LlamaIndex Python Backend
**Goal**: Build a Python/LlamaIndex backend that uses OpenAI for RAG (Retrieval-Augmented Generation), agents, and structured data extraction.
**Stack**: Python 3.12, LlamaIndex, OpenAI API
**Virtualenv**: `backend/venv/`
**Entry point**: `backend/sample.py` (basic RAG demo — currently working)

## Key Architecture Decisions

- API keys loaded from `.env` via `python-dotenv` — never hardcoded
- LlamaIndex settings configured via `Settings.llm` and `Settings.embed_model` (global)
- Models: `gpt-4o-mini` for LLM, `text-embedding-3-small` for embeddings
- `.env` path resolved relative to `__file__` for portability

## Current Status

- [x] Python 3.12 virtualenv set up at `backend/venv/`
- [x] Core packages installed: `llama-index`, `openai`, `python-dotenv`
- [x] `backend/sample.py` — basic in-memory RAG demo running successfully
- [x] Persistent vector store (ChromaDB) set up at backend/storage/
- [ ] No document loader for real files yet
- [ ] No API server (FastAPI/Flask) yet

## Active Plans

- ChromaDB persistent vector store implemented — see `backend/sample.py`

---

## Progress Log

| Date | Agent | Action | Plan File |
|------|-------|--------|-----------|
| — | — | Initial context created | — |
| 2026-03-01 | main | Implemented ChromaDB persistent vector store | Plan in conversation |
