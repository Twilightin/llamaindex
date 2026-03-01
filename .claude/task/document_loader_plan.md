# Document Loader Implementation Plan

**Date**: 2026-03-01
**Status**: Ready for implementation
**Target file**: `backend/sample.py` (refactor) + new `backend/data/` directory

---

## 1. Summary

This plan replaces the hardcoded `get_documents()` stub in `backend/sample.py` with a real file-based document loader using `SimpleDirectoryReader`. It also introduces incremental ingestion via `IngestionPipeline` + `SimpleDocumentStore` so that re-running the script only processes new or changed files, not the entire corpus.

### Why this approach

- `SimpleDirectoryReader` is the standard LlamaIndex solution, lives in `llama_index.core` (no extra package needed beyond the file-type extras), and handles PDF, TXT, Markdown, and DOCX out of the box with the right backend libraries installed.
- `IngestionPipeline` with a `SimpleDocumentStore` provides content-hash-based deduplication. It automatically skips unchanged documents and re-embeds only modified ones, making it safe to call on every startup.
- `filename_as_id=True` on `SimpleDirectoryReader` gives each document a stable, deterministic `doc_id` (the full file path string), which is the key that the docstore uses to detect duplicates.
- This integrates cleanly with the existing `ChromaVectorStore` + `StorageContext` pattern already in the codebase.

---

## 2. New packages to install

Run these with the virtualenv active (`source backend/venv/bin/activate`):

```bash
# File reader integration (DocxReader, PDFReader, MarkdownReader, etc.)
pip install llama-index-readers-file

# PDF support — PDFReader internally does: import pypdf
pip install pypdf

# DOCX support — DocxReader internally does: import docx2txt
pip install docx2txt

# SentenceSplitter lives in llama-index-core (already installed).
# No extra package needed for chunking.
```

Optional (only if PyMuPDF-based PDF reading is preferred over pypdf):
```bash
pip install pymupdf   # enables PyMuPDFReader, faster and better layout
```

The `llama-index-readers-file` package (latest: 0.5.6 as of 2025-12-24) is a separate integration package. `SimpleDirectoryReader` inside `llama_index.core` automatically delegates to the readers in this package when the right extensions are encountered.

---

## 3. Folder structure

```
backend/
  data/                  <- NEW: drop files here; git-ignored
    .gitkeep             <- ensures the folder is committed but content is not
  storage/
    chroma/              <- existing ChromaDB persistent store
    index_store.json     <- existing LlamaIndex docstore metadata
    pipeline/            <- NEW: IngestionPipeline cache + docstore persistence
  sample.py              <- MODIFIED
```

Add to `.gitignore` (if not already there):
```
backend/data/*
!backend/data/.gitkeep
```

---

## 4. Exact imports for the new code

```python
# Already present in sample.py — keep these:
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# NEW imports to add:
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.storage.docstore import SimpleDocumentStore
```

Note: `Document`, `load_index_from_storage` can be removed once the new loader pattern replaces `get_documents()`.

---

## 5. Step-by-step implementation

### Step 1 — Create the data directory

```bash
mkdir -p backend/data
touch backend/data/.gitkeep
```

Place test files there (e.g., a `.txt`, a `.pdf`, a `.md`) before running.

### Step 2 — Add the DATA_DIR and PIPELINE_DIR path constants

In `backend/sample.py`, after the existing path constants:

```python
DATA_DIR     = Path(__file__).parent / "data"
PIPELINE_DIR = STORAGE_DIR / "pipeline"
```

### Step 3 — Replace get_documents() with load_documents()

Remove the old `get_documents()` function entirely. Replace with:

```python
def load_documents():
    """Load all files from backend/data/ using SimpleDirectoryReader.

    filename_as_id=True gives each document a stable doc_id based on its
    full file path — required for incremental ingestion deduplication.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    reader = SimpleDirectoryReader(
        input_dir=str(DATA_DIR),
        recursive=True,
        filename_as_id=True,    # critical for deduplication
        required_exts=[".pdf", ".txt", ".md", ".docx"],  # whitelist
    )
    return reader.load_data()
```

Supported extensions and their backing libraries:
- `.txt`, `.md`  — handled natively, no extra package
- `.pdf`         — uses `pypdf` (must be installed)
- `.docx`        — uses `docx2txt` (must be installed)

### Step 4 — Replace get_or_create_index() with ingest_documents()

The new function uses `IngestionPipeline` with:
1. A `SentenceSplitter` for chunking
2. The existing `ChromaVectorStore` as the destination
3. A `SimpleDocumentStore` for hash-based deduplication

```python
def ingest_documents(vector_store: ChromaVectorStore) -> VectorStoreIndex:
    """Ingest documents from backend/data/ into ChromaDB.

    On first run: processes and embeds every file.
    On subsequent runs: skips files whose content hash has not changed,
    re-embeds only modified or new files.
    """
    PIPELINE_DIR.mkdir(parents=True, exist_ok=True)
    pipeline_storage = str(PIPELINE_DIR)

    # Restore persisted pipeline state (docstore + cache) if it exists
    docstore = SimpleDocumentStore()
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(
                chunk_size=512,      # see chunking notes below
                chunk_overlap=64,
            ),
            Settings.embed_model,    # uses the globally configured embedder
        ],
        vector_store=vector_store,
        docstore=docstore,
    )

    # Load persisted pipeline state (skip-list + cache) between runs
    try:
        pipeline.load(pipeline_storage)
        print("Loaded existing pipeline cache from storage.")
    except Exception:
        print("No existing pipeline cache found — starting fresh.")

    documents = load_documents()
    if not documents:
        print(f"Warning: No documents found in {DATA_DIR}. Add files and re-run.")
    else:
        print(f"Processing {len(documents)} document(s) from {DATA_DIR} ...")
        pipeline.run(documents=documents, show_progress=True)
        pipeline.persist(pipeline_storage)
        print("Pipeline state persisted.")

    # Build a VectorStoreIndex view over the populated ChromaDB collection
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )
```

### Step 5 — Update get_or_create_index() to call ingest_documents()

Simplify the existing `get_or_create_index()` to:

```python
def get_or_create_index() -> VectorStoreIndex:
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    chroma_collection = chroma_client.get_or_create_collection("llamaindex_docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    return ingest_documents(vector_store)
```

The old `index_store_path.exists()` branch logic is no longer needed because `IngestionPipeline` manages its own persistence and deduplication.

### Step 6 — Chunking configuration rationale

`SentenceSplitter(chunk_size=512, chunk_overlap=64)` is a conservative default:

- `chunk_size=512` tokens. LlamaIndex default is 1024 but 512 works better for `text-embedding-3-small` (768-dim model) and keeps retrieved context focused. Increase to 1024 if your documents are long-form narrative prose.
- `chunk_overlap=64` tokens (~12.5% overlap). Prevents context being cut off at chunk boundaries.
- `SentenceSplitter` respects sentence boundaries, avoiding mid-sentence cuts that degrade embedding quality.

Units: LlamaIndex chunk_size is measured in tokens (using the model's tokenizer). For `text-embedding-3-small`, 512 tokens is roughly 380 words.

To set chunking globally (affects all parsers), you can alternatively use:
```python
Settings.chunk_size = 512
Settings.chunk_overlap = 64
```

---

## 6. Complete refactored sample.py

Below is the full file after all changes, for reference during implementation:

```python
"""
LlamaIndex + OpenAI sample — RAG with persistent ChromaDB vector store
and file-based document loading with incremental ingestion.

Usage:
    source backend/venv/bin/activate
    python backend/sample.py
"""

from pathlib import Path

import chromadb
from dotenv import load_dotenv
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

STORAGE_DIR  = Path(__file__).parent / "storage"
CHROMA_DIR   = STORAGE_DIR / "chroma"
DATA_DIR     = Path(__file__).parent / "data"
PIPELINE_DIR = STORAGE_DIR / "pipeline"


def load_documents():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    reader = SimpleDirectoryReader(
        input_dir=str(DATA_DIR),
        recursive=True,
        filename_as_id=True,
        required_exts=[".pdf", ".txt", ".md", ".docx"],
    )
    return reader.load_data()


def ingest_documents(vector_store: ChromaVectorStore) -> VectorStoreIndex:
    PIPELINE_DIR.mkdir(parents=True, exist_ok=True)
    pipeline_storage = str(PIPELINE_DIR)

    docstore = SimpleDocumentStore()
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=64),
            Settings.embed_model,
        ],
        vector_store=vector_store,
        docstore=docstore,
    )

    try:
        pipeline.load(pipeline_storage)
        print("Loaded existing pipeline cache from storage.")
    except Exception:
        print("No existing pipeline cache found — starting fresh.")

    documents = load_documents()
    if not documents:
        print(f"Warning: No documents found in {DATA_DIR}. Add files and re-run.")
    else:
        print(f"Processing {len(documents)} document(s)...")
        pipeline.run(documents=documents, show_progress=True)
        pipeline.persist(pipeline_storage)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )


def get_or_create_index() -> VectorStoreIndex:
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    chroma_collection = chroma_client.get_or_create_collection("llamaindex_docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    return ingest_documents(vector_store)


def main() -> None:
    Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.1)
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

    index = get_or_create_index()
    query_engine = index.as_query_engine()

    question = "What is LlamaIndex used for?"
    response = query_engine.query(question)

    print(f"Q: {question}")
    print(f"A: {response}")


if __name__ == "__main__":
    main()
```

---

## 7. Integration notes

### Settings must be configured before ingest_documents() is called

`ingest_documents()` uses `Settings.embed_model` directly inside the pipeline transformations list. The `Settings.llm` and `Settings.embed_model` assignments in `main()` must happen before `get_or_create_index()` is called. The existing code already does this correctly.

### Existing ChromaDB data

The `get_or_create_collection("llamaindex_docs")` call is unchanged, so data already stored in ChromaDB from the old hardcoded documents will remain. On first run with the new code, the pipeline will add new documents alongside the old embeddings. To start clean, delete `backend/storage/` before running.

### The pipeline.load() call is safe even on first run

`pipeline.load()` is wrapped in a `try/except` block. If `PIPELINE_DIR` is empty or does not contain a valid cache file, the exception is caught and ingestion proceeds fresh.

### VectorStoreIndex.from_vector_store() vs from_documents()

The old code used `VectorStoreIndex.from_documents()` which re-embeds everything each call. The new code uses `VectorStoreIndex.from_vector_store()` which simply wraps the already-populated ChromaDB collection — no re-embedding, instant startup once data is loaded.

---

## 8. Gotchas and version-specific issues

### Gotcha 1: Settings.embed_model must be set before IngestionPipeline runs

If `Settings.embed_model` is `None` when `pipeline.run()` is called, LlamaIndex will raise a configuration error. Always configure Settings in `main()` before calling `get_or_create_index()`.

### Gotcha 2: pypdf vs PyMuPDF

`PDFReader` from `llama-index-readers-file` uses `pypdf` by default. `pypdf` handles most standard PDFs well but may struggle with scanned/image-based PDFs (which need OCR). If PDFs have complex layouts or are scanned, consider `PyMuPDFReader` instead:

```python
from llama_index.readers.file import PyMuPDFReader
pip install pymupdf
```

Use `file_extractor={".pdf": PyMuPDFReader()}` in `SimpleDirectoryReader` to override.

### Gotcha 3: SimpleDirectoryReader raises ValueError if data dir is empty

If `DATA_DIR` exists but contains no files matching `required_exts`, `load_data()` returns an empty list (no error). However if `DATA_DIR` does not exist and `mkdir` fails, it will error. The `DATA_DIR.mkdir(parents=True, exist_ok=True)` call in `load_documents()` prevents this.

### Gotcha 4: filename_as_id generates OS-specific paths as doc_id

On macOS/Linux, `doc_id` will be something like `/Users/you/project/backend/data/report.pdf`. This is stable within one machine but will differ across machines (e.g., in Docker). For portability, consider using relative paths as doc_id — but for local development this is not a concern.

### Gotcha 5: chunk_size units are tokens, not characters

LlamaIndex chunk_size counts tokens (via tiktoken for OpenAI models). A 512-token chunk is roughly 380-400 English words. Do not confuse this with character count.

### Gotcha 6: IngestionPipeline.load() compatibility

`pipeline.persist()` and `pipeline.load()` were introduced in LlamaIndex 0.10. Since the project is on 0.14.x, these methods are available. The pipeline stores its state in a `docstore.json` and `cache.json` within the specified directory.

### Gotcha 7: required_exts filter

`required_exts` must include the leading dot: `[".pdf", ".txt"]` not `["pdf", "txt"]`. Wrong values silently result in zero documents loaded.

---

## 9. Verification

### Quick test after implementation

1. Install packages:
   ```bash
   source backend/venv/bin/activate
   pip install llama-index-readers-file pypdf docx2txt
   ```

2. Add a test file:
   ```bash
   echo "FastAPI is a modern Python web framework for building APIs." > backend/data/test.txt
   ```

3. Run:
   ```bash
   python backend/sample.py
   ```
   Expected output:
   ```
   No existing pipeline cache found — starting fresh.
   Processing 1 document(s)...
   Pipeline state persisted.
   Q: What is LlamaIndex used for?
   A: <answer from the text file>
   ```

4. Run again (incremental check):
   ```bash
   python backend/sample.py
   ```
   Expected output:
   ```
   Loaded existing pipeline cache from storage.
   Processing 1 document(s)...
   Pipeline state persisted.
   Q: What is LlamaIndex used for?
   A: <same answer>
   ```
   The second run should complete significantly faster because the document hash is unchanged and embeddings are skipped.

5. PDF test:
   ```bash
   # Place any PDF in backend/data/
   cp ~/Downloads/some_document.pdf backend/data/
   python backend/sample.py
   ```
   Should show "Processing 2 document(s)..." on the second run with the PDF added.

6. Inspect what was indexed:
   ```python
   print(index.ref_doc_info)  # shows doc_id -> node mapping
   ```
