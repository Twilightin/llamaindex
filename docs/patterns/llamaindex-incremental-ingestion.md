# The right way to do incremental document ingestion in LlamaIndex

## Context
When building a RAG system that loads files from disk into a ChromaDB vector store,
you need ingestion that:
- Skips unchanged files on re-run (no redundant embedding API calls)
- Automatically picks up new or modified files
- Works with multiple file types (PDF, TXT, MD, DOCX)

Use this pattern any time your documents live on disk and change over time.

## Pattern

```python
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.storage.docstore import SimpleDocumentStore

DATA_DIR     = Path(__file__).parent / "data"
PIPELINE_DIR = STORAGE_DIR / "pipeline"

def load_documents():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    reader = SimpleDirectoryReader(
        input_dir=str(DATA_DIR),
        recursive=True,
        filename_as_id=True,           # stable doc_id = file path; required for dedup
        required_exts=[".pdf", ".txt", ".md", ".docx"],
    )
    return reader.load_data()

def ingest_documents(vector_store) -> VectorStoreIndex:
    PIPELINE_DIR.mkdir(parents=True, exist_ok=True)
    pipeline_storage = str(PIPELINE_DIR)

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=64),
            Settings.embed_model,      # must be set in Settings before calling this
        ],
        vector_store=vector_store,
        docstore=SimpleDocumentStore(),
    )

    try:
        pipeline.load(pipeline_storage)   # restore hash cache from previous run
    except Exception:
        pass                              # first run — start fresh

    documents = load_documents()
    if documents:
        pipeline.run(documents=documents, show_progress=True)
        pipeline.persist(pipeline_storage)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
```

## Why This Way

- `filename_as_id=True` gives each file a stable `doc_id` (its full path). The pipeline uses this to track a `doc_id → content_hash` map and skips files that haven't changed.
- `pipeline.load()` / `pipeline.persist()` saves the hash cache between runs so deduplication works across restarts.
- `VectorStoreIndex.from_vector_store()` wraps the already-populated ChromaDB collection without re-embedding anything — instant startup.
- `SentenceSplitter(chunk_size=512, chunk_overlap=64)` is a conservative default: 512 tokens ≈ 380 words, 64-token overlap prevents context being cut at chunk boundaries.

## When NOT to Use

- If documents never change and you only ingest once, the simpler `VectorStoreIndex.from_documents()` is fine for a one-shot script.
- If you need metadata filtering (by date, source, author), extend `load_documents()` to attach metadata to each `Document` before passing to the pipeline.
- Do not call `VectorStoreIndex.from_documents()` on every startup — it re-embeds the entire corpus each time, wasting API calls and time.
