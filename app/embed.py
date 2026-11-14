
"""Generate Gemini embeddings for MatdarMitra PDF chunks."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.chunking import load_all_chunks

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-embedding-001"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "embedded_chunks.json"

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)


def embed_texts(texts, task_type="RETRIEVAL_DOCUMENT"):
    response = client.models.embed_content(
        model=MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=768
        )
    )
    return [item.values for item in response.embeddings]


def embed_chunks(chunks, batch_size=5):
    embedded_chunks = []

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        texts = [chunk["text"] for chunk in batch]

        vectors = embed_texts(texts)

        for chunk, vector in zip(batch, vectors):
            embedded_chunks.append({
                **chunk,
                "embedding": vector
            })

        print(f"Embedded {len(embedded_chunks)}/{len(chunks)} chunks")

    return embedded_chunks


if __name__ == "__main__":
    chunks = load_all_chunks()
    results = embed_chunks(chunks)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False)

    print("\nEmbedding completed!")
    print("Total embedded chunks:", len(results))
    print("Vector dimensions:", len(results[0]["embedding"]))
    print("Saved to:", OUTPUT_PATH)
