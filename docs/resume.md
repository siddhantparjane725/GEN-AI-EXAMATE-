# MatdarMitra — Resume Highlights

- Built **MatdarMitra**, an AI-powered voter-registration assistance application using **FastAPI, Streamlit, Python, Gemini embeddings, ChromaDB, Groq, and LangGraph**, grounding responses in Election Commission of India (ECI) documents.
- Implemented a **RAG pipeline** with PDF chunking, semantic retrieval, source/page citations, and controlled fallback responses; indexed **34 ECI document chunks** and recorded **14/14 source hits** in the documented retrieval evaluation.
- Improved reliability with **Pytest (18 tests passing), Ruff, GitHub Actions CI, Docker, and Render deployment**; added request-latency and token-usage logging, input limits, and an in-memory response cache (300-second TTL, 128-entry capacity).

**Project links**
- Live UI: https://matdarmitra-ui.onrender.com
- API: https://matdarmitra-api.onrender.com/docs
- GitHub: https://github.com/siddhantparjane725/GEN-AI-EXAMATE-

*Accuracy note: the 14/14 figure is a retrieval source-hit result on the documented evaluation set, not a claim of 100% generated-answer accuracy.*
