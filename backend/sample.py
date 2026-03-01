"""
LlamaIndex + OpenAI sample — basic RAG (Retrieval-Augmented Generation)

Usage:
    source backend/venv/bin/activate
    python backend/sample.py
"""

from pathlib import Path

from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


def main() -> None:
    # Configure LlamaIndex to use OpenAI
    Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.1)
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

    # Sample documents (replace with real data loaders later)
    documents = [
        Document(text="LlamaIndex is a data framework for LLM applications."),
        Document(text="It supports RAG, agents, and structured data extraction."),
        Document(text="You can load PDFs, web pages, databases, and more."),
    ]

    # Build vector index from documents
    index = VectorStoreIndex.from_documents(documents)

    # Create query engine
    query_engine = index.as_query_engine()

    # Run a query
    question = "What is LlamaIndex used for?"
    response = query_engine.query(question)

    print(f"Q: {question}")
    print(f"A: {response}")


if __name__ == "__main__":
    main()
