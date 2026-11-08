
"""TF-IDF based smart search for MatdarMitra."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def record_text(record):
    """Combine useful record fields into searchable text."""
    fields = [
        record.get("form_number", ""),
        record.get("purpose", ""),
        record.get("who_should_fill", ""),
        record.get("documents_needed", ""),
        record.get("submit_to", ""),
        record.get("question", ""),
        record.get("answer", ""),
        record.get("category", "")
    ]

    return " ".join(str(field) for field in fields if field)


def smart_search(records, query, limit=5):
    """Rank records according to TF-IDF cosine similarity."""

    query = query.strip()

    if not query or not records:
        return []

    documents = [record_text(record) for record in records]

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        document_vectors = vectorizer.fit_transform(documents)
        query_vector = vectorizer.transform([query])

        similarities = cosine_similarity(
            query_vector,
            document_vectors
        ).flatten()

        ranked_indices = similarities.argsort()[::-1]

        results = []

        for index in ranked_indices:
            score = float(similarities[index])

            if score <= 0:
                continue

            result = records[index].copy()
            result["similarity_score"] = round(score, 4)
            results.append(result)

            if len(results) >= limit:
                break

        return results

    except ValueError:
        return []
