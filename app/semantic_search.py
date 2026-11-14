
"""Semantic search for MatdarMitra."""

import json
from pathlib import Path

from sklearn.metrics.pairwise import cosine_similarity

from app.embed import embed_texts

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "embedded_chunks.json"

QUESTIONS = [
    "What documents are needed with Form 6?",
    "Which form is used to correct name spelling?",
    "Who can object to someone's name in the voter list?",
    "What are the eligibility requirements for a new voter?",
    "How can the name of a deceased person be removed?",
    "Who is the BLO for ward 5 in Kopargaon?",
    "How can an NRI register as a voter?",
    "Is Aadhaar mandatory for voter registration?",
    "Which form is used after shifting to a new address?",
    "Can I submit a voter registration form online or physically?"
]


def load_embeddings():
    with DATA_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def search_chunks(question, chunks, top_k=3):
    query_vector = embed_texts(
        [question],
        task_type="RETRIEVAL_QUERY"
    )[0]

    document_vectors = [chunk["embedding"] for chunk in chunks]

    scores = cosine_similarity(
        [query_vector],
        document_vectors
    )[0]

    results = sorted(
        zip(scores, chunks),
        key=lambda item: item[0],
        reverse=True
    )

    return results[:top_k]


def main():
    chunks = load_embeddings()
    output = ["# MatdarMitra Semantic Search Results\n"]

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {number}: {question}")

        results = search_chunks(question, chunks)

        output.append(f"\n## Question {number}: {question}\n")

        for rank, (score, chunk) in enumerate(results, start=1):
            print(
                f"{rank}. {chunk['source']} | "
                f"Page {chunk['page']} | Score: {score:.4f}"
            )

            output.append(
                f"- **Rank {rank}** | Score: {score:.4f}\n"
                f"  - Source: {chunk['source']}\n"
                f"  - Page: {chunk['page']}\n"
                f"  - Chunk ID: {chunk['chunk_id']}\n"
                f"  - Text: {chunk['text'][:300]}...\n"
            )

    eval_dir = Path(__file__).resolve().parents[1] / "eval"
    eval_dir.mkdir(exist_ok=True)

    output_path = eval_dir / "search_results.md"
    output_path.write_text("\n".join(output), encoding="utf-8")

    print("\nSemantic search completed!")
    print("Results saved to:", output_path)


if __name__ == "__main__":
    main()
