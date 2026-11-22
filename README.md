[![MatdarMitra CI](https://github.com/siddhantparjane725/GEN-AI-EXAMATE-/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/siddhantparjane725/GEN-AI-EXAMATE-/actions/workflows/ci.yml)
# MatdarMitra — Day 1
# MatdarMitra 🇮🇳

### AI-Powered Voter Registration Assistant

MatdarMitra helps Indian citizens understand voter registration and electoral roll services through simple, guided assistance.

## Project Card

- **Product:** MatdarMitra
- **Domain:** Citizen Services
- **User:** First-time voters, students and citizens shifting residence.
- **Problem:** Citizens often struggle to identify the correct ECI form, required documents and qualifying dates.
- **Data Source:** Election Commission of India (ECI).
    ## Data Sources

        1. [ECI Download Forms]:(https://www.eci.gov.in/download-forms)
        2. [ECI Electoral Roll FAQ]:(https://www.eci.gov.in/Documents/Final-ER-FAQ.pdf)
        formate of data :PDF (forms, guidelines, FAQ) + HTML FAQ pages


# MatdarMitra — Day 2

Structured ECI voter-form and FAQ records for the MatdarMitra assistant.

## Dataset
- 6 form records: Forms 6, 6A, 6B, 7, 8 and a Form 12C summary.
- 14 FAQ records: eligibility, qualifying dates, Form 6 documents, online filing, correction, objection/deletion, NRI enrollment and revision schedule.
- Form records include `form_number`, `purpose`, `who_should_fill`, `documents_needed`, `submit_to`, and `source_url`. FAQ records also include `question` and `answer`.

## Run
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Windows CMD: .venv\Scripts\activate.bat
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m app.cli
```

## CLI
1. Print all records
2. Search by keyword
3. Count records by category
4. Get a record by ID (`FORM-6`, `FAQ-03`)
0. Exit

## Data quality note
Form 12C is included only as a summary from the ECI Citizen Service Portal, which describes it as a postal-ballot form for Kashmiri migrant electors. The Form 12C PDF was not among the uploaded files, so its exact documents and filing process are marked unverified. FAQ entries are concise summaries of the cited ECI pages. Verify current ECI instructions before acting.

## Official sources
- https://www.eci.gov.in/download-forms
- https://www.eci.gov.in/faq/en/how-to-register/
- https://www.eci.gov.in/faq/2/9
- https://voters.eci.gov.in/

## Day 3 – ECI Data Ingestion & Processing

### Objective
Collect official ECI forms and FAQ documents, extract relevant information, and convert it into structured JSON records.

### Tasks Completed
- Downloaded five ECI forms: Form 6, 6A, 6B, 7 and 8.
- Collected the official ECI Electoral Roll FAQ PDF.
- Implemented PDF text extraction using **PyPDF**.
- Created `app/ingest.py` to clean and process extracted data.
- Added error handling for missing files and malformed records.
- Generated structured records in `data/records.json`.

### Dataset Summary

| Record Type | Count |
|---|---:|
| ECI Forms | 5 |
| FAQs | 14 |
| **Total Records** | **19** |

### Key Files
- `app/ingest.py` – PDF extraction and data processing.
- `app/models.py` – Record dataclass.
- `data/raw/` – Original ECI PDF documents.
- `data/records.json` – Processed dataset.

### Technologies Used
Python, PyPDF, JSON, Regular Expressions.

**Outcome:** Successfully generated 19 structured MatdarMitra records from official ECI documents.


# Day 4 – FastAPI, Smart Search & Data Analysis

## Objective

Develop a FastAPI service for MatdarMitra, implement intelligent record searching using TF-IDF and cosine similarity, and explore the dataset using pandas.

## Tasks Completed

### S1 – FastAPI Service

Created `app/main.py` using FastAPI with the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks API health status |
| GET | `/records?limit=10` | Retrieves records with a specified limit |
| GET | `/records/{record_id}` | Retrieves a record by ID; returns 404 if missing |
| GET | `/search?q=keyword` | Searches records using smart search |
| POST | `/questions` | Accepts voter-related questions and returns relevant records |

### S2 – Data Analysis and Smart Search

**1. Data Exploration – `analysis/explore.py`**

Used pandas to analyze MatdarMitra records and print three facts:

- Total number of records.
- Distribution of records by type.
- Distribution of records by category.

**2. Smart Search – `app/smart_search.py`**

Implemented intelligent search using:

- TF-IDF (Term Frequency–Inverse Document Frequency) for text vectorization.
- Cosine Similarity for measuring query-to-record similarity.
- Ranking of records based on similarity scores.

Integrated smart search with the `/search` API endpoint.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pandas
- Scikit-learn
- TF-IDF
- Cosine Similarity

## How to Run

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Run data exploration

```bash
python -m analysis.explore
```

### 3. Start FastAPI server

```bash
python -m uvicorn app.main:app --reload
```

### 4. Open Swagger API documentation

http://127.0.0.1:8000/docs

## Day 4 Deliverables

- FastAPI application created.
- Five required API endpoints implemented.
- Pandas-based data exploration completed.
- TF-IDF and cosine similarity smart search implemented.
- Smart search integrated with FastAPI.
- API documentation available through Swagger UI.

## Week 1 Milestone

Day 4 completes the Week 1 development milestone for MatdarMitra.


**Project:** MatdarMitra – ECI Voter Registration Assistance System  
**Track:** GenAI Examate – Sanjivani SJ-19


**Project:** MatdarMitra – ECI Voter Registration Assistance System  
**Track:** GenAI Examate – Sanjivani SJ-19

---

## Day 5 – LLM Fundamentals & Checkpoint 1

### Objective
Understand how Large Language Models (LLMs) work, document real-world MatdarMitra user questions, and demonstrate the working FastAPI application.

### Tasks Completed

**1. LLM Documentation**
- Created `docs/how_llms_work.md`.
- Explained tokenization, embeddings, transformers, attention mechanisms and next-token prediction.
- Added an LLM workflow diagram using Mermaid.
- Documented how LLMs can support MatdarMitra.

**2. Real User Questions**
- Created `docs/user_questions.md`.
- Added 10 realistic voter registration questions.
- Included questions about Forms 6, 6A, 6B, 7 and 8.
- Identified a question about ward-wise BLO contact information that the current dataset cannot answer.

**3. Checkpoint 1 – FastAPI Demonstration**
- Successfully started the FastAPI server using Uvicorn.
- Verified API documentation through Swagger UI at `/docs`.
- Demonstrated the available API endpoints.
- Prepared an explanation of the `smart_search()` function using TF-IDF and cosine similarity.

### Key Files
- `docs/how_llms_work.md` – LLM concepts and workflow diagram.
- `docs/user_questions.md` – 10 MatdarMitra user questions.
- `app/main.py` – FastAPI application.
- `app/smart_search.py` – Intelligent record search.

### Technologies Used
Python, FastAPI, Uvicorn, TF-IDF, Cosine Similarity, Mermaid and Markdown.

### Outcome
Completed LLM fundamentals documentation, prepared 10 realistic user questions, and demonstrated the MatdarMitra FastAPI application as part of Checkpoint 1.

### Day 6 – LLM Integration with Groq
Objective
Integrate a Large Language Model (LLM) into MatdarMitra so users can ask voter-registration questions in natural language and receive answers grounded in the retrieved Election Commission of India (ECI) records.
Tasks Completed
- Created app/llm.py to handle the LLM integration.
- Configured Groq as the initial LLM provider.
- Integrated the POST /chat endpoint into the existing FastAPI application.
- Added environment-based configuration using .env and .env.example.
- Kept the actual API key in the local .env file; .env must not be committed to GitHub.
- Created the prompts/ directory with:
  - ## task_prompt_1.txt – form and information identification.
  - ##  task_prompt_2.txt – step-by-step procedural guidance.
- Configured /chat to return a JSON response with:
  - answer
  - confidence
  - follow_up
- Created eval/prompt_compare.md to document the comparison of the two task-prompt approaches using the 10 questions in docs/user_questions.md.
API Test
The POST /chat endpoint was tested successfully through FastAPI Swagger UI.

Example request:
{
  "question": "Which form should I use to correct my name spelling?",
  "prompt_version": "2"
}
Observed test: Groq returned a successful 200 OK response. MatdarMitra identified Form 8 for name-spelling correction and referenced FAQ-26 in the retrieved ECI context.
Prompt Design Comparison
- Prompt 1 focuses on identifying the relevant form, purpose, intended user, documents, and submission information from the retrieved records.
- Prompt 2 focuses on explaining a supported form or procedure in simple steps and asking a relevant follow-up question.
The prompt comparison document records the evaluation questions, criteria, prompt-design differences, available test evidence, and safety checks. Only observed test results should be described as live test evidence; do not claim unrecorded outputs or scores.
Day 6 Outcome
MatdarMitra now has a Groq-powered /chat endpoint connected to the existing TF-IDF retrieval workflow. The response format includes an answer, confidence value, and follow-up question. Answers must remain grounded in the available ECI records, and missing information such as verified ward-wise BLO contacts must not be invented.
Run the Application
Install dependencies if they are not already installed:
pip install -r requirements.txt
Set the local .env file in the project root:
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
Start FastAPI:
python -m uvicorn app.main:app --reload
Open the interactive API documentation:
http://127.0.0.1:8000/docs
Use POST /chat to test the Groq-powered


## Day 7 – Semantic Search and Vector Database

### Objective
Implement semantic search for MatdarMitra using Gemini embeddings and ChromaDB to retrieve relevant Election Commission of India (ECI) documents.

### 1. PDF Chunking
- Created `app/chunking.py`.
- Extracted text from 6 ECI PDF documents.
- Generated 34 text chunks.
- Preserved metadata for every chunk:
  - Chunk ID
  - Document title
  - Source PDF
  - Page number
  - Extracted text

### 2. Gemini Embeddings
- Created `app/embed.py`.
- Integrated Google's Gemini embedding model (`gemini-embedding-001`).
- Generated 768-dimensional embedding vectors.
- Successfully embedded all 34 chunks.
- Saved embeddings in `data/embedded_chunks.json`.

### 3. Semantic Search
- Created `app/semantic_search.py`.
- Implemented query embedding generation.
- Used cosine similarity to find relevant document chunks.
- Retrieved the top 3 matching results.
- Prepared a 10-question evaluation script.
- Saved search evaluation results in `eval/search_results.md`.

### 4. ChromaDB Vector Database
- Created `app/vectorstore.py`.
- Integrated persistent ChromaDB storage.
- Created collection: `matdarmitra_documents`.
- Indexed all 34 document chunks with their embeddings and metadata.
- Stored the database in `data/chroma_db/`.

### 5. FastAPI Integration
Added a new endpoint:

`GET /search/semantic?q=`

Features:
- Accepts natural-language questions.
- Generates Gemini query embeddings.
- Searches the ChromaDB collection.
- Returns matching document text, source, page number, chunk ID and distance.

### 6. API Testing

Tested the semantic search endpoint through FastAPI Swagger UI.

Example question:

`What documents are needed with Form 6?`

Verified results included:
- Form 6 – Page 2
- Form 6 – Page 1
- Form 6B – Page 1

The first two retrieved results contained relevant age-proof and residence-proof information.

### Day 7 Outcome

Successfully implemented a semantic retrieval pipeline that connects ECI PDF documents, Gemini embeddings, ChromaDB and FastAPI.

**Technologies Used:** Python, Google Gemini API, ChromaDB, FastAPI, Scikit-learn, Cosine Similarity, PyPDF.

## Day 8 – RAG Implementation and Evaluation

### 1. Retrieval-Augmented Generation (RAG)
- Created `app/rag.py`.
- Integrated ChromaDB semantic retrieval with the Groq LLM.
- Retrieved relevant ECI document chunks for user questions.
- Generated answers using retrieved context only.
- Added citations containing source PDF and page number.
- Added a fallback response when relevant information is unavailable.

### 2. FastAPI Integration
Added `POST /ask` to the MatdarMitra API.

The endpoint returns:
- Generated answer
- Confidence
- Follow-up question
- Source citations
- Retrieved chunk IDs

Q6 (ward-wise BLO details for Kopargaon) is handled with the required "I don't know" response.

### 3. Evaluation Dataset
- Created `eval/eval_set.json`.
- Added 15 evaluation questions.
- Included answerable and unanswerable questions.
- Marked expected source documents for evaluation.

### 4. Retrieval Configuration Comparison

| Configuration | Chunk Size | Top K | Source Hits | Hit Rate |
|---|---:|---:|---:|---:|
| Config A | 800 words | 3 | 14/14 | 100% |
| Config B | 800 words | 5 | 14/14 | 100% |

**Selected Configuration: Config A**

Both configurations achieved the same source hit rate. Config A was selected because it retrieves fewer chunks, reducing unnecessary context.

Note: This experiment compares top-k values while keeping chunk size fixed at 800 words.

### 5. Evaluation Script
- Created `eval/run_eval.py`.
- Executed both retrieval configurations.
- Saved results in `eval/eval_results.md`.

### Day 8 Outcome
Implemented a RAG-based question-answering system with source citations, a controlled fallback for unanswerable questions, and a two-configuration retrieval evaluation.


## Day 9 – AI Agent and LangGraph Integration

### Objective
Build an intelligent agent that selects the appropriate tool, retrieves voter information, calculates qualifying dates, and supports human approval before execution.

### Features Implemented

1. **Qualifying Date Calculator**
   - Calculates the 17th and 18th birthdays.
   - Determines the next ECI qualifying date.
   - Identifies potential advance-application eligibility.
   - Validates invalid and future dates.

2. **Handwritten Agent**
   - Implemented in `app/agent_loop.py`.
   - Routes date-related questions to the calculator.
   - Routes voter-information questions to the RAG system.
   - Requests DOB when it is missing.

3. **LangGraph Agent**
   - Implemented in `app/graph.py`.
   - Uses a StateGraph workflow.
   - Supports human approval and rejection.
   - Uses MemorySaver to retain workflow state between requests.

4. **FastAPI Integration**
   - Added `POST /agent`.
   - Supports approval requests and workflow resumption.
   - Exposes agent functionality through Swagger UI.

### Testing

Automated tests are available in the `tests/` directory.

- Date calculation and validation
- Agent tool selection
- RAG routing
- Human approval and rejection

Run tests:

```bash
python -m pytest tests/ -v
```

### Day 9 Architecture

```text
User Question
     |
     v
Tool Selection
     |
     v
Human Approval
     |
     +---- Rejected ----> Stop
     |
   Approved
     |
     v
Execute Selected Tool
     |
     +---- RAG Search
     |
     +---- Qualifying Date Calculator
     |
     v
Final Answer
```


## Day 10 – Streamlit Dashboard & Checkpoint 2

### Overview

Day 10 focuses on building a Streamlit-based user interface for MatdarMitra and connecting it with the FastAPI backend.

The dashboard allows users to ask voter-registration questions, receive source-based answers, provide feedback, and identify the appropriate voter-registration form through a three-question wizard.

### Features Implemented

**1. AI Assistant**
- Connected Streamlit with the FastAPI `/ask` endpoint.
- Accepts voter-registration questions.
- Displays AI-generated answers with source citations.
- Supports thumbs-up and thumbs-down feedback.

**2. Form Chooser Wizard**
- Uses three questions to understand the user's voter-registration situation.
- Recommends Form 6 for new voter enrolment.
- Recommends Form 8 for changes of residence or corrections.
- Displays a document checklist from the backend records.
- Provides preliminary guidance when no form is required.

**3. AI Agent**
- Connects with the `/agent` endpoint.
- Displays approval requests before tool execution.
- Supports approval and rejection of agent actions.

**4. About MatdarMitra**
- Displays the project overview.
- Documents the technologies and key capabilities.

### Technology Stack

- Python
- Streamlit
- FastAPI
- Retrieval-Augmented Generation (RAG)
- Gemini Embeddings
- ChromaDB
- Groq LLM
- LangGraph
- Requests

### How to Run

Start the FastAPI backend:

```bash
python -m uvicorn app.main:app --reload
```

Open another terminal and start the Streamlit application:

```bash
python -m streamlit run ui/app.py
```

Open the local URL displayed in the terminal.

### Application Screenshots

Add your actual screenshots in `docs/screenshots/`.

| Screenshot | File |
|---|---|
| AI Assistant | `ai-assistant.png` |
| Form Chooser Wizard | `form-wizard.png` |
| Main Dashboard | `dashboard.png` |

![Dashboard](docs/screenshots/dashboard.png)

![AI Assistant](docs/screenshots/ai-assistant.png)

![Form Chooser](docs/screenshots/form-wizard.png)

### Checkpoint 2

**Objective:** Demonstrate the MatdarMitra application through a working Streamlit interface connected to the FastAPI backend.

**Completion checklist:**
- [ ] Streamlit application runs successfully.
- [ ] AI Assistant returns answers with citations.
- [ ] Feedback is saved successfully.
- [ ] Form Chooser recommends the appropriate form.
- [ ] Document checklist is displayed.
- [ ] AI Agent approval and rejection work.
- [ ] Application screenshots added to README.
- [ ] Complete test suite passes.
- [ ] Live demo completed.
- [ ] Git tag `checkpoint-2` created and pushed.

# Day 11 – Testing, Code Quality and Docker Deployment

## Overview

Day 11 focused on improving the reliability, code quality and deployment of MatdarMitra. Automated testing was implemented using Pytest, code quality was checked using Ruff, and Docker was configured to run the FastAPI backend and Streamlit frontend together.

## S1 – Testing and Code Quality

### 1. Automated Testing with Pytest

Created and expanded the `tests/` directory to test important application functionality.

**Test coverage includes:**
- Agent loop functionality.
- LangGraph workflow and human approval process.
- Qualifying date calculator.
- API health endpoint.
- Records retrieval.
- Record search functionality.
- Individual record retrieval.
- RAG `/ask` endpoint using mocked retrieval and LLM responses.

### 2. Code Quality with Ruff

Used Ruff to identify and fix Python code quality issues.

Command:

```bash
python -m ruff check .
```

Ruff was used to check:
- Python coding standards.
- Unused imports.
- Code formatting issues.
- Common programming errors.

### 3. Run Tests

```bash
python -m pytest tests/ -v
```

Previously verified test result: **16 tests passed**.

## S2 – Docker Deployment

### 1. Docker Configuration

Created the following Docker configuration files:

| File | Purpose |
|---|---|
| `Dockerfile` | Builds the MatdarMitra application image |
| `.dockerignore` | Excludes unnecessary and sensitive files from the build context |
| `docker-compose.yml` | Runs the API and UI services together |

### 2. Docker Services

**API Service**
- Built using FastAPI.
- Runs on port `8000`.
- Provides backend APIs and application functionality.
- Includes a health check.

**UI Service**
- Built using Streamlit.
- Runs on port `8501`.
- Communicates with the API using Docker's internal service network.

**Vector Database**
- Uses ChromaDB for persistent vector storage.
- Stores database files in the mounted `data/chroma_db` directory.

### 3. Run MatdarMitra with Docker

Make sure Docker Desktop is running.

Build and start the application:

```bash
docker compose up --build
```

Check running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs -f
```

Stop the application:

```bash
docker compose down
```

### 4. Application URLs

| Service | URL |
|---|---|
| Streamlit UI | http://localhost:8501 |
| FastAPI Backend | http://localhost:8000 |
| Swagger API Documentation | http://localhost:8000/docs |

## Day 11 – Learning Outcomes

- Learned automated testing using Pytest.
- Understood how to mock external LLM and retrieval functions during testing.
- Improved Python code quality using Ruff.
- Learned how to create a Dockerfile.
- Understood Docker images and containers.
- Learned Docker Compose for managing multiple services.
- Connected a Streamlit frontend with a FastAPI backend inside Docker.
- Implemented persistent ChromaDB storage using Docker volumes.
- Successfully ran MatdarMitra using Docker Compose.

## Day 11 Deliverables

- `tests/` – Automated test cases.
- `Dockerfile` – Docker image configuration.
- `.dockerignore` – Docker build exclusions.
- `docker-compose.yml` – Multi-container application configuration.
- Updated `README.md` – Docker deployment instructions.

**Day 11 Goal:** Improve application reliability through automated testing and deploy the MatdarMitra API and UI using Docker Compose.

## Day 12 – CI/CD and Cloud Deployment

### S1: Continuous Integration

Implemented GitHub Actions to automate code quality and build validation.

- Integrated Ruff for Python linting.
- Integrated Pytest for automated testing.
- Added Docker image build verification.
- Configured CI to run on GitHub pushes and pull requests.
- Created a feature branch and merged the pull request after successful CI validation.

**Validation:**
- Ruff checks passed.
- All 16 tests passed locally.
- Docker image build passed.
- GitHub Actions workflow completed successfully.

### S2: Cloud Deployment

Successfully deployed MatdarMitra using Render.

**Live Application:**

https://matdarmitra-ui.onrender.com

**Backend API:**

https://matdarmitra-api.onrender.com

**API Health Check:**

https://matdarmitra-api.onrender.com/health

**Deployment Details:**
- Frontend: Streamlit
- Backend: FastAPI
- Containerization: Docker
- Cloud Platform: Render
- Database / Vector Store: ChromaDB

**Deployment Validation:**
- FastAPI backend deployed successfully.
- Public `/health` endpoint verified.
- Streamlit frontend deployed successfully.
- Frontend successfully connected to the backend.

### Day 12 Outcome
MatdarMitra now has an automated CI workflow and a publicly accessible frontend and backend deployment.