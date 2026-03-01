"""
LlamaIndex + OpenAI sample — RAG with persistent ChromaDB vector store

Usage:
    source backend/venv/bin/activate
    python backend/sample.py
"""

from pathlib import Path

import chromadb
from dotenv import load_dotenv
from llama_index.core import (
    Document,
    Settings,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

STORAGE_DIR = Path(__file__).parent / "storage"
CHROMA_DIR = STORAGE_DIR / "chroma"


def get_documents() -> list[Document]:
    return [
        Document(text="LlamaIndex is a data framework for LLM applications."),
        Document(text="It supports RAG, agents, and structured data extraction."),
        Document(text="You can load PDFs, web pages, databases, and more."),
    ]


def get_or_create_index() -> VectorStoreIndex:
    chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    chroma_collection = chroma_client.get_or_create_collection("llamaindex_docs")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    index_store_path = STORAGE_DIR / "index_store.json"

    if index_store_path.exists():
        print("Loading existing index from storage...")
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
            persist_dir=str(STORAGE_DIR),
        )
        return load_index_from_storage(storage_context)
    else:
        print("Creating new index and persisting to storage...")
        STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            get_documents(), storage_context=storage_context
        )
        storage_context.persist(persist_dir=str(STORAGE_DIR))
        return index


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
