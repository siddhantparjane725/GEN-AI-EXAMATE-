
"""Persistent ChromaDB vector store for MatdarMitra."""

import json
from pathlib import Path

import chromadb

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "embedded_chunks.json"
DB_PATH = BASE_DIR / "data" / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

collection = client.get_or_create_collection(
    name="matdarmitra_documents",
    metadata={"hnsw:space": "cosine"}
)


def index_chunks():
    with DATA_PATH.open(encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        print("No chunks found.")
        return

    collection.upsert(
        ids=[chunk["chunk_id"] for chunk in chunks],
        embeddings=[chunk["embedding"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {
                "title": chunk["title"],
                "source": chunk["source"],
                "page": chunk["page"]
            }
            for chunk in chunks
        ]
    )

    print("ChromaDB indexing completed!")
    print("Total indexed chunks:", collection.count())


def search_documents(query_vector, top_k=3):
    return collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )


if __name__ == "__main__":
    index_chunks()
