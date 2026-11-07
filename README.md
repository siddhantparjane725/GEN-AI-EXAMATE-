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
