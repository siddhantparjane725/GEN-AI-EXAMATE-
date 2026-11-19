
from fastapi.testclient import TestClient

import app.main as main_module
import app.rag as rag_module
from app.main import app

client = TestClient(app)


SAMPLE_RECORDS = [
    {
        "record_id": "form-6",
        "form_number": "6",
        "purpose": "New voter enrolment",
        "who_should_fill": "Eligible first-time voters",
        "documents_needed": "Age proof; Address proof",
        "submit_to": "Electoral Registration Officer",
        "category": "form",
    },
    {
        "record_id": "form-8",
        "form_number": "8",
        "purpose": "Correction of voter details",
        "who_should_fill": "Existing registered voters",
        "documents_needed": "Supporting documents",
        "submit_to": "Electoral Registration Officer",
        "category": "form",
    },
]


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_records_endpoint(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "get_records",
        lambda: SAMPLE_RECORDS,
    )

    response = client.get("/records?limit=1")

    assert response.status_code == 200
    assert response.json()["total_records"] == 2
    assert response.json()["returned_records"] == 1
    assert len(response.json()["records"]) == 1


def test_record_by_id(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "get_records",
        lambda: SAMPLE_RECORDS,
    )

    response = client.get("/records/form-6")

    assert response.status_code == 200
    assert response.json()["form_number"] == "6"


def test_search_endpoint(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "get_records",
        lambda: SAMPLE_RECORDS,
    )

    response = client.get("/search?q=new voter enrolment")

    assert response.status_code == 200
    assert response.json()["results_count"] >= 1
    assert response.json()["results"][0]["form_number"] == "6"


def test_ask_endpoint_with_fake_llm(monkeypatch):
    fake_chunks = [
        {
            "chunk_id": "chunk-001",
            "text": "Form 6 is used for new voter enrolment.",
            "metadata": {
                "source": "6.pdf",
                "page": 1,
            },
            "distance": 0.15,
        }
    ]

    def fake_retrieve(question, top_k=3):
        return fake_chunks

    def fake_llm(system_prompt, user_prompt):
        assert "new voter" in user_prompt.lower()

        return {
            "answer": "Form 6 is used for new voter enrolment.",
            "confidence": 0.95,
            "follow_up": "Would you like to know the required documents?",
        }

    monkeypatch.setattr(
        rag_module,
        "retrieve_chunks",
        fake_retrieve,
    )
    monkeypatch.setattr(
        rag_module,
        "call_groq",
        fake_llm,
    )

    response = client.post(
        "/ask",
        json={"question": "Which form is used for new voter enrolment?"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "Form 6" in data["answer"]
    assert data["confidence"] == 0.95
    assert len(data["citations"]) == 1
    assert data["citations"][0]["source"] == "6.pdf"
