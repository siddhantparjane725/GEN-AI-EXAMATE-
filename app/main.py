
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.records import load_records, get_by_id
from app.smart_search import smart_search

app = FastAPI(
    title="MatdarMitra API",
    description="ECI voter registration assistance API",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)


def get_records():
    try:
        return load_records()
    except (OSError, ValueError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to load records: {exc}"
        )


# Homepage
@app.get("/")
def home():
    return {
        "message": "Welcome to MatdarMitra API",
        "docs": "/docs",
        "status": "running"
    }


# 1. Health check
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MatdarMitra API"
    }


# 2. Get all records with limit
@app.get("/records")
def list_records(limit: int = Query(default=10, ge=1, le=100)):
    records = get_records()

    return {
        "total_records": len(records),
        "returned_records": min(limit, len(records)),
        "records": records[:limit]
    }


# 3. Get record by ID
@app.get("/records/{record_id}")
def record_details(record_id: str):
    records = get_records()
    record = get_by_id(records, record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Record not found"
        )

    return record


# 4. Smart search
@app.get("/search")
def search_records(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=5, ge=1, le=20)
):
    records = get_records()
    results = smart_search(records, q, limit)

    return {
        "query": q,
        "results_count": len(results),
        "results": results
    }


# 5. Ask a question
@app.post("/questions")
def ask_question(request: QuestionRequest):
    records = get_records()

    results = smart_search(
        records,
        request.question,
        limit=5
    )

    return {
        "question": request.question,
        "answer": (
            "Here are the most relevant ECI records for your question."
            if results
            else "No relevant records found. Please try another question."
        ),
        "results": results
    }
