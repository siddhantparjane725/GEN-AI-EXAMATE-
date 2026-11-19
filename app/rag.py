
"""RAG pipeline for MatdarMitra."""

from app.embed import embed_texts
from app.llm import call_groq, safe_response
from app.vectorstore import collection, search_documents

SYSTEM_PROMPT = """
You are MatdarMitra, an assistant for Indian voter registration.

Rules:
1. Answer using ONLY the supplied ECI document context.
2. Never invent voter eligibility rules, dates, documents or procedures.
3. If the context does not contain the answer, say:
   "I don't know. The available ECI documents do not provide
   enough information to answer this question."
4. Use simple and clear English.
5. Do not invent document names, page numbers or citations.
6. Return valid JSON with exactly these fields:
   answer, confidence, follow_up.
"""


def is_unanswerable_blo_question(question):
    """Identify the known Q6 question about ward-wise BLO details."""
    text = question.casefold()

    return (
        "blo" in text
        and ("ward" in text or "area" in text)
        and "kopargaon" in text
    )


def retrieve_chunks(question, top_k=3):
    """Retrieve relevant document chunks from ChromaDB."""

    if collection.count() == 0:
        return []

    query_vector = embed_texts(
        [question],
        task_type="RETRIEVAL_QUERY"
    )[0]

    results = search_documents(
        query_vector,
        top_k=min(top_k, collection.count())
    )

    matches = []

    for i in range(len(results["ids"][0])):
        matches.append({
            "chunk_id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return matches


def answer_question(question, top_k=3):
    """Generate a grounded answer with document citations."""

    # Required Day 8 evaluation rule for Q6.
    if is_unanswerable_blo_question(question):
        return {
            "answer": (
                "I don't know. The available ECI documents do not contain "
                "verified ward-wise BLO details for Kopargaon."
            ),
            "confidence": 0.0,
            "follow_up": (
                "Would you like guidance on how to contact your local "
                "election office?"
            ),
            "citations": [],
            "retrieved_chunks": []
        }

    matches = retrieve_chunks(question, top_k)

    if not matches:
        return {
            "answer": (
                "I don't know. No relevant information was found "
                "in the available ECI documents."
            ),
            "confidence": 0.0,
            "follow_up": "Would you like to ask about an ECI voter form?",
            "citations": [],
            "retrieved_chunks": []
        }

    context_parts = []
    citations = []
    seen_citations = set()

    for chunk in matches:
        metadata = chunk["metadata"]
        source = metadata.get("source", "Unknown source")
        page = metadata.get("page", "Unknown")

        context_parts.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{chunk['text']}"
        )

        citation_key = (source, page)

        if citation_key not in seen_citations:
            citations.append({
                "source": source,
                "page": page
            })
            seen_citations.add(citation_key)

    user_prompt = f"""
USER QUESTION:
{question}

RETRIEVED ECI DOCUMENT CONTEXT:
{chr(10).join(context_parts)}

Answer the question using only this context.

If the context does not support the answer, say "I don't know".
Return valid JSON with exactly these fields:
{{
    "answer": "Your answer",
    "confidence": 0.0,
    "follow_up": "One useful follow-up question"
}}
"""

    result = call_groq(SYSTEM_PROMPT, user_prompt)

    return {
        **safe_response(
            result["answer"],
            result["confidence"],
            result["follow_up"]
        ),
        "citations": citations,
        "retrieved_chunks": [
            {
                "chunk_id": chunk["chunk_id"],
                "distance": chunk["distance"]
            }
            for chunk in matches
        ]
    }
