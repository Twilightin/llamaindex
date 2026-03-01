"""
LlamaIndex + OpenAI sample — RAG with persistent ChromaDB vector store
and file-based document loading with incremental ingestion.

Usage:
    source backend/venv/bin/activate
    python backend/sample.py

Drop files into backend/data/ (PDF, TXT, MD, DOCX) before running.
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

STORAGE_DIR     = Path(__file__).parent / "storage"
CHROMA_DIR      = STORAGE_DIR / "chroma"
DATA_DIR        = Path(__file__).parent / "data"
PIPELINE_DIR    = STORAGE_DIR / "pipeline"
COLLECTION_NAME = "llamaindex_docs"
CHUNK_SIZE      = 512
CHUNK_OVERLAP   = 64


def load_documents() -> list:
    """Load all supported files from backend/data/ using SimpleDirectoryReader.

    filename_as_id=True gives each document a stable doc_id based on its
    file path — required for incremental ingestion deduplication.
    Supported: .pdf, .txt, .md, .docx
    """
    reader = SimpleDirectoryReader(
        input_dir=str(DATA_DIR),
        recursive=True,
        filename_as_id=True,
        required_exts=[".pdf", ".txt", ".md", ".docx"],
    )
    return reader.load_data()


def ingest_documents(vector_store: ChromaVectorStore) -> VectorStoreIndex:
    """Ingest documents from backend/data/ into ChromaDB.

    On first run: processes and embeds every file.
    On subsequent runs: skips files whose content hash has not changed,
    re-embeds only modified or new files.
    """
    if Settings.embed_model is None:
        raise RuntimeError("Settings.embed_model must be set before calling ingest_documents()")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PIPELINE_DIR.mkdir(parents=True, exist_ok=True)

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP),
            Settings.embed_model,
        ],
        vector_store=vector_store,
        docstore=SimpleDocumentStore(),
    )

    try:
        pipeline.load(PIPELINE_DIR)
        print("Loaded existing pipeline cache from storage.")
    except (FileNotFoundError, ValueError):
        print("No existing pipeline cache found — starting fresh.")

    documents = load_documents()
    if not documents:
        print(f"Warning: No documents found in {DATA_DIR}. Add files and re-run.")
    else:
        print(f"Processing {len(documents)} document(s) from {DATA_DIR} ...")
        pipeline.run(documents=documents, show_progress=True)
        pipeline.persist(PIPELINE_DIR)
        print("Pipeline state persisted.")

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )


def get_or_create_index() -> VectorStoreIndex:
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
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
