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
<<<<<<< HEAD
=======

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