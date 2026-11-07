
import json
import re
from pathlib import Path

from pypdf import PdfReader
from app.models import Record


# Project paths
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUTPUT = ROOT / "data" / "records.json"


# Five forms using your exact downloaded filenames
FORMS = {
    "6.pdf": (
        "6",
        "Application for inclusion of a name in the electoral roll as a new voter.",
        "Eligible Indian citizens applying for first-time inclusion at their ordinary residence.",
        "Recent photograph, age proof and residence proof as specified in Form 6.",
        "Relevant ERO/AERO or official ECI voter services portal.",
        "new_registration"
    ),
    "6a.pdf": (
        "6A",
        "Application for inclusion of an overseas elector in the electoral roll.",
        "Eligible Indian citizens residing outside India who have not acquired citizenship of another country.",
        "Recent photograph, relevant Indian passport pages and valid visa endorsement.",
        "ERO of the constituency corresponding to the Indian address in the passport.",
        "overseas_registration"
    ),
    "6b.pdf": (
        "6B",
        "Letter of information of Aadhaar number for electoral roll authentication.",
        "Electors already enrolled in the electoral roll who wish to provide Aadhaar information or declare that they cannot furnish Aadhaar.",
        "Aadhaar number or one accepted alternative document listed in Form 6B.",
        "Official ECI voter services portal or prescribed election registration channel.",
        "aadhaar_authentication"
    ),
    "7.pdf": (
        "7",
        "Application for objection to proposed inclusion or deletion of a name from an existing electoral roll.",
        "A person submitting an objection or permitted deletion request under applicable rules.",
        "Applicant and concerned elector details, reason, and relevant supporting evidence.",
        "Relevant Electoral Registration Officer (ERO).",
        "objection_deletion"
    ),
    "8.pdf": (
        "8",
        "Application for shifting residence, correction of electoral-roll entries, replacement EPIC, or marking PwD.",
        "An already registered elector requesting one of the services listed in Form 8.",
        "Address proof for shifting; documentary proof for correction; relevant EPIC/FIR evidence for replacement; disability details as applicable.",
        "Relevant ERO, including through the official ECI voter services portal.",
        "shifting_correction_epic"
    )
}


FORMS_URL = "https://www.eci.gov.in/download-forms"
FAQ_URL = "https://www.eci.gov.in/Documents/Final-ER-FAQ.pdf"


# Required 14 FAQ records
SELECTED_FAQ_IDS = {
    "FAQ-12",
    "FAQ-14",
    "FAQ-15",
    "FAQ-23",
    "FAQ-26",
    "FAQ-31",
    "FAQ-33",
    "FAQ-36",
    "FAQ-37",
    "FAQ-41",
    "FAQ-42",
    "FAQ-47",
    "FAQ-48",
    "FAQ-49"
}


# Extract text from PDF
def pdf_text(path):
    reader = PdfReader(str(path))

    return "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )


# Clean extracted text
def clean(value):
    return re.sub(r"\s+", " ", value).strip()


# Process five form PDFs
def process_forms():

    records = []

    for filename, fields in FORMS.items():

        try:
            path = RAW / filename

            if not path.exists():
                print(f"[SKIP] Missing {filename}")
                continue

            extracted_text = pdf_text(path)

            if not extracted_text.strip():
                raise ValueError("PDF contains no extractable text")

            number, purpose, who, docs, submit, category = fields

            record = Record(
                form_number=number,
                purpose=clean(purpose),
                who_should_fill=clean(who),
                documents_needed=clean(docs),
                submit_to=clean(submit),
                source_url=FORMS_URL,
                record_id=f"FORM-{number}",
                record_type="form",
                category=category
            )

            records.append(record.to_dict())
            print(f"[OK] Processed Form {number}: {filename}")

        except Exception as exc:
            print(f"[BAD ROW] {filename}: {exc}")

    return records


# Process FAQ PDF
def process_faq():

    records = []
    faq_path = RAW / "Final-ER-FAQ.pdf"

    try:
        if not faq_path.exists():
            print("[SKIP] Final-ER-FAQ.pdf not found")
            return records

        text = pdf_text(faq_path)

        if not text.strip():
            raise ValueError("FAQ PDF contains no extractable text")

        # Match numbered questions, their Ans sections, and the next question.
        pattern = re.compile(
            r"\bQ\s*\.?\s*(\d{1,3})\s*[.):\-]?\s*"
            r"(.*?)\s*"
            r"\bAns(?:wer)?\s*\.?\s*:?\s*"
            r"(.*?)"
            r"(?=\bQ\s*\.?\s*\d{1,3}\s*[.):\-]?|\Z)",
            re.IGNORECASE | re.DOTALL
        )

        for match in pattern.finditer(text):

            try:
                num, question, answer = match.groups()

                record_id = f"FAQ-{int(num):02d}"

                # Keep only the 14 required FAQs
                if record_id not in SELECTED_FAQ_IDS:
                    continue

                question = clean(question)
                answer = clean(answer)

                if not question or not answer:
                    raise ValueError("Empty question or answer")

                record = Record(
                    form_number="",
                    purpose=f"ECI FAQ: {question}",
                    who_should_fill="People seeking electoral-roll guidance.",
                    documents_needed="Refer to the relevant ECI form and official guidelines.",
                    submit_to="Relevant ERO/AERO or official ECI portal.",
                    source_url=FAQ_URL,
                    record_id=record_id,
                    record_type="faq",
                    question=question,
                    answer=answer,
                    category="eci_faq"
                )

                records.append(record.to_dict())
                print(f"[OK] Extracted {record_id}")

            except (ValueError, TypeError) as exc:
                print(f"[SKIP] Malformed FAQ row: {exc}")

        found_ids = {r["record_id"] for r in records}
        missing_ids = SELECTED_FAQ_IDS - found_ids

        if missing_ids:
            print("[WARNING] FAQ IDs not extracted:", sorted(missing_ids))

    except Exception as exc:
        print(f"[ERROR] FAQ extraction failed: {exc}")

    return records


# Main ingestion function
def ingest():

    print("\n========== MATDARMITRA INGESTION ==========\n")

    records = []

    print("\n[1] Processing ECI Forms...\n")
    records.extend(process_forms())

    print("\n[2] Processing selected ECI FAQs...\n")
    records.extend(process_faq())

    print("\n[3] Saving records...\n")

    try:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)

        OUTPUT.write_text(
            json.dumps(records, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

        form_count = sum(
            1 for r in records if r["record_type"] == "form"
        )

        faq_count = sum(
            1 for r in records if r["record_type"] == "faq"
        )

        print("\n========== COMPLETED ==========")
        print(f"Forms processed : {form_count}")
        print(f"FAQs extracted  : {faq_count}")
        print(f"Total records   : {len(records)}")
        print(f"\nSaved to: {OUTPUT}")

    except (OSError, TypeError, ValueError) as exc:
        print(f"[SAVE ERROR] {exc}")

    return records


if __name__ == "__main__":
    ingest()
