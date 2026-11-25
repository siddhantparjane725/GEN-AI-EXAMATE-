# MatdarMitra Interview Preparation

## 60-Second Pitch

MatdarMitra is an AI-powered voter-registration assistant that helps people understand Election Commission of India procedures, identify relevant forms, and find supporting information. The application uses a Streamlit frontend and a FastAPI backend. Its retrieval-augmented generation pipeline chunks ECI documents, creates Gemini embeddings, searches them with ChromaDB, and uses Groq to generate answers grounded in retrieved passages, with citations and a fallback when the documents do not support an answer. LangGraph coordinates the agent's multi-step tools and approval flow. I also added input validation, latency and token-usage logging, and a bounded response cache. In the documented retrieval evaluation, the system found a source for all 14 test questions; that measures retrieval, not answer accuracy. The project is deployed on Render, and its latest recorded checks are 18 passing tests and passing Ruff checks.

## Core Technical Questions

1. What is RAG?
RAG stands for Retrieval-Augmented Generation. It retrieves relevant information from a knowledge base and
gives that context to a language model to generate an answer. This helps MatdarMitra answer questions using
its reference documents.
2. Why did you use ChromaDB?
ChromaDB stores vector embeddings and supports similarity search. It helps retrieve document chunks that are
semantically related to a user's question, even when the wording is different.
3. Why did you use Gemini embeddings?
Gemini embeddings convert text into numerical vectors. These vectors represent text meaning and help find
relevant document chunks for a user's question.
4. Why did you use Groq?
Groq provides API access to a language model. In MatdarMitra, the model uses retrieved context to generate a
clear response.
5. What is LangGraph?
LangGraph is a framework for building multi-step AI workflows. We use it to coordinate the agent's steps,
including tool use and decision-making.
6. What happens if the answer is not available in your documents?
The system should return a safe fallback instead of guessing. This is important because incorrect
voter-registration information could mislead citizens.
7. How did you test your project?
We used pytest for automated tests and Ruff for code-quality checks. The latest confirmed result in the project
notes was 18 tests passed and Ruff checks passed. Show the current terminal output during the demo.
8. What is the difference between a normal chatbot and a RAG chatbot?
A normal chatbot generates answers using its model knowledge and the conversation. A RAG chatbot first
searches a knowledge base for relevant information, then uses that information to help generate an answer.
9. What is FastAPI used for?
FastAPI is used to build the backend API. It connects the frontend to the project's search, chat, RAG and agent
functionality, and provides interactive API documentation.
10. What are the limitations of MatdarMitra?
Answer quality depends on the quality and freshness of official source documents. The deployed application also
depends on internet connectivity and availability of its cloud AI services.

## Hardest-Problem Story: RAG Response Caching

11. Tell us about the hardest problem you solved.
The hardest problem was reducing repeated RAG work without returning the wrong answer or letting cached data grow without bounds. Repeated questions could trigger retrieval and another language-model call, adding latency and using provider tokens. I added a cache keyed by the normalized question and retrieval setting, with a 300-second expiry and a 128-entry limit. Cache hits return a copy of the stored result and report zero new LLM tokens. I verified the behavior with a test that calls the same question twice: the first call is a miss, the second is a hit, and retrieval and generation each run only once. The cache is process-local, so it resets on restart; the test verifies cache behavior, not a real-world latency improvement.

12. How does your cache work?
The cache uses Python's OrderedDict. It keeps responses for up to 300 seconds, stores at most 128 entries,
uses a normalized question and top_k as the cache key, and removes expired or older entries when needed. The
cache is in memory, so it resets when the application process restarts.
13. How did you measure or verify the improvement?
I wrote an automated pytest test. It sends the same question twice and checks that the first response is a cache
miss and the second is a cache hit. It also verifies that retrieval and the LLM are called only once, and that the
cache-hit response reports zero new LLM tokens. This verifies cache behavior; it is not a real-world latency
benchmark.