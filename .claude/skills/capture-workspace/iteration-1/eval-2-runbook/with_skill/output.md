# Capture Skill Evaluation — eval-2-runbook (with_skill)

## Classification

**Doc Type:** Runbook

**Reasoning:** The content provides step-by-step instructions to set up and operate ChromaDB locally. It walks through installation, starting a server, connecting a client, and verifying the setup. This is a living operational reference — not a historical decision, not a code pattern, and not a warning about a bug. Runbook is the clear match.

---

## Proposed Filename and Folder Path

**Folder:** `docs/runbooks/`
**Filename:** `setup-chromadb-locally.md`
**Full path:** `docs/runbooks/setup-chromadb-locally.md`

No date prefix — Runbooks are living references, not historical records.

---

## Complete File Content (shown for confirmation)

```
Proposed file: docs/runbooks/setup-chromadb-locally.md
Type: Runbook

--- PREVIEW ---
# How to Set Up ChromaDB Locally

## Prerequisites
- Python environment with `pip` available
- Port 8000 free on localhost
- A directory where ChromaDB data will persist (e.g., `./chroma_db`)

## Steps

1. Install the ChromaDB package:
   ```bash
   pip install chromadb
   ```

2. Start the ChromaDB server, specifying a persistent storage path:
   ```bash
   chroma run --path ./chroma_db
   ```
   This starts the server on port 8000. The `--path` flag is required — without it, data will not persist between server restarts.

3. Connect to the running server from your Python code:
   ```python
   import chromadb

   client = chromadb.HttpClient(host="localhost", port=8000)
   ```

## Verify It Worked

Call `client.heartbeat()` — it should return a timestamp, confirming the server is reachable and healthy:

```python
print(client.heartbeat())  # e.g., 1709298000000000000
```

## Notes

- Always pass `--path ./chroma_db` (or another directory of your choice) when starting the server. Omitting `--path` causes ChromaDB to store data in memory only, and all collections and embeddings are lost on restart.
- The default port is 8000. If you need a different port, pass `--port <number>` to `chroma run` and update `chromadb.HttpClient(port=<number>)` accordingly.
- This setup uses ChromaDB in client-server mode. For quick scripts or tests you can also use `chromadb.Client()` (in-memory, no server needed), but data will not persist.
---

Save this file and update KNOWLEDGE.md? (yes / edit / skip)
```

---

## KNOWLEDGE.md Update

**Would update KNOWLEDGE.md:** Yes

**Section to append under:** `## Runbooks`

**Line to add:**
```
- [How to Set Up ChromaDB Locally](docs/runbooks/setup-chromadb-locally.md)
```

If `KNOWLEDGE.md` does not exist at the project root, the skill would create it with all four section headings (`## Decisions`, `## Runbooks`, `## Patterns`, `## Lessons`) and then append the line above under `## Runbooks`.
