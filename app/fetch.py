from pathlib import Path
import requests

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
DOCUMENTS = {
    "Final-ER-FAQ.pdf": "https://www.eci.gov.in/Documents/Final-ER-FAQ.pdf",
    "Form-6.pdf": "https://voters.eci.gov.in/formspdf/Form_6_English.pdf",
    "Form-7.pdf": "https://voters.eci.gov.in/formspdf/Form_7_English.pdf",
    "Form-8.pdf": "https://voters.eci.gov.in/formspdf/Form_8_English.pdf",
}

def download_file(url, destination, timeout=30):
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "MatdarMitra-StudentProject/1.0"})
        response.raise_for_status()
        if not response.content.startswith(b"%PDF"):
            raise ValueError("Downloaded response is not a PDF")
        destination.write_bytes(response.content)
        print(f"[OK] {destination.name}: {len(response.content)} bytes")
        return True
    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] {url}")
    except requests.exceptions.HTTPError as exc:
        print(f"[HTTP ERROR] {url}: {exc}")
    except requests.exceptions.RequestException as exc:
        print(f"[NETWORK ERROR] {url}: {exc}")
    except (OSError, ValueError) as exc:
        print(f"[FILE/CONTENT ERROR] {destination}: {exc}")
    return False

def fetch_documents():
    downloaded = []
    for filename, url in DOCUMENTS.items():
        target = RAW_DIR / filename
        if download_file(url, target):
            downloaded.append(target)
    print(f"Downloaded {len(downloaded)} of {len(DOCUMENTS)} documents")
    return downloaded

if __name__ == "__main__":
    fetch_documents()
