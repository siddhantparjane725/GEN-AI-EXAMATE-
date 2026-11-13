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
