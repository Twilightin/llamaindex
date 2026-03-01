# Skill Evaluation Output — capture skill, eval-1-decision

## Classified Doc Type

**Decision**

The content compares two options (ChromaDB vs FAISS), explains the reasoning behind a choice, and documents accepted trade-offs. This is a textbook Decision.

---

## Proposed Filename and Folder Path

- **Folder:** `docs/decisions/`
- **Filename:** `2026-03-01-why-chromadb-over-faiss.md`
- **Full path:** `docs/decisions/2026-03-01-why-chromadb-over-faiss.md`

---

## Complete File Content (shown to user for confirmation)

```
📄 Proposed file: docs/decisions/2026-03-01-why-chromadb-over-faiss.md
Type: Decision

--- PREVIEW ---
# Why we chose ChromaDB over FAISS

**Date:** 2026-03-01

## Context
We needed a vector store for our LlamaIndex backend. The decision was between ChromaDB and FAISS — two commonly used options — and we needed one that would be easy to integrate, reliably persist data, and work well within the LlamaIndex ecosystem.

## Options Considered
- **ChromaDB** — a dedicated vector database with built-in persistent storage and a native LlamaIndex integration via `ChromaVectorStore`
- **FAISS** — a high-performance similarity search library from Meta that requires manual serialization for persistence and uses a wrapper for LlamaIndex integration

## Decision
We chose **ChromaDB**.

## Reasons
- ChromaDB provides persistent storage out of the box — no extra work needed to save and reload the index across restarts
- ChromaDB has a native LlamaIndex integration via `ChromaVectorStore`, making setup straightforward
- FAISS requires manual serialization using numpy, which is error-prone and adds maintenance overhead
- FAISS integration with LlamaIndex is via a wrapper, adding an extra layer of indirection

## Trade-offs Accepted
- ChromaDB requires a running server process, which adds operational complexity compared to FAISS's in-process library model
---

Save this file and update KNOWLEDGE.md? (yes / edit / skip)
```

---

## KNOWLEDGE.md Update

**Would update KNOWLEDGE.md:** Yes

**Line to add** (under the `## Decisions` section):

```
- [Why we chose ChromaDB over FAISS](docs/decisions/2026-03-01-why-chromadb-over-faiss.md)
```

If `KNOWLEDGE.md` does not yet exist at the project root, the skill would create it with all four section headings (`## Decisions`, `## Runbooks`, `## Patterns`, `## Lessons`) and then append this line under `## Decisions`.
