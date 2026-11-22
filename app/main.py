import logging
import time

import requests
from fastapi import FastAPI, HTTPException, Query, Request
from pydantic import BaseModel, Field

from app.embed import embed_texts
from app.graph import resume_agent, start_agent
from app.llm import chat_with_matdarmitra
from app.rag import answer_question
from app.records import get_by_id, load_records
from app.smart_search import smart_search
from app.vectorstore import collection, search_documents

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("matdarmitra")

app = FastAPI(
    title="MatdarMitra API",
    description="ECI voter registration assistance API",
    version="1.0.0"
)
@app.middleware("http")
async def log_request_latency(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    latency_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "request=%s method=%s status=%s latency_ms=%.2f",
        request.url.path,
        request.method,
        response.status_code,
        latency_ms
    )

    response.headers["X-Response-Time-ms"] = f"{latency_ms:.2f}"

    return response

class AgentRequest(BaseModel):
    question: str | None = Field(default=None, max_length=1000)
    thread_id: str = Field(..., min_length=1, max_length=100)
    approved: bool | None = None


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    prompt_version: str = "1"


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


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


# 6. Chat with MatdarMitra

# 6. Chat with MatdarMitra
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        records = load_records()

        result = chat_with_matdarmitra(
            question=request.question,
            records=records,
            prompt_version=request.prompt_version
        )

        usage = result.get("usage", {})

        logger.info(
            "endpoint=/chat prompt_tokens=%s completion_tokens=%s "
            "total_tokens=%s",
            usage.get("prompt_tokens", 0),
            usage.get("completion_tokens", 0),
            usage.get("total_tokens", 0)
        )

        return result

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to Groq. Please try again."
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# 7. Semantic search using ChromaDB
@app.get("/search/semantic")
def semantic_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=3, ge=1, le=10)
):
    try:
        if collection.count() == 0:
            raise HTTPException(
                status_code=503,
                detail="Vector database is empty. Index documents first."
            )

        query_embedding = embed_texts(
            [q],
            task_type="RETRIEVAL_QUERY"
        )[0]

        results = search_documents(
            query_embedding,
            top_k=min(limit, collection.count())
        )

        matches = []

        for i in range(len(results["ids"][0])):
            matches.append({
                "chunk_id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

        return {
            "query": q,
            "results_count": len(matches),
            "results": matches
        }

    except HTTPException:
        raise

    except Exception as error:  # noqa: BLE001 - convert unexpected search failures to HTTP 500
        raise HTTPException(
            status_code=500,
            detail=f"Semantic search failed: {error!s}"
        )

# 8. RAG-based question answering
@app.post("/ask")
def ask(request: AskRequest):
    try:
        result = answer_question(
            question=request.question,
            top_k=3
        )

        usage = result.get("usage", {})

        logger.info(
            "endpoint=/ask prompt_tokens=%s completion_tokens=%s "
            "total_tokens=%s cache_hit=%s",
            usage.get("prompt_tokens", 0),
            usage.get("completion_tokens", 0),
            usage.get("total_tokens", 0),
            result.get("cache_hit", False)
        )

        return result

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to Groq or Gemini."
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    # Day 9: LangGraph Agent API
@app.post("/agent")
def agent_endpoint(request: AgentRequest):
    try:
        if request.approved is None:
            if not request.question or not request.question.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Question is required to start an agent."
                )

            result = start_agent(
                request.question,
                request.thread_id
            )
        else:
            result = resume_agent(
                request.thread_id,
                request.approved
            )

        if result.get("__interrupt__"):
            approval = result["__interrupt__"][0].value

            return {
                "status": "approval_required",
                "thread_id": request.thread_id,
                "approval_request": approval
            }

        return {
            "status": "completed",
            "thread_id": request.thread_id,
            "answer": result.get("answer", "")
        }

    except HTTPException:
        raise
    except Exception as error:  # noqa: BLE001 - return unexpected agent failures as HTTP 500
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )