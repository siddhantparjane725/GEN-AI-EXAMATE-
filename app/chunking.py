
"""Extract and split ECI PDF documents into metadata-rich chunks."""

from pathlib import Path
from pypdf import PdfReader


DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def split_text(text, chunk_size=CHUNK_SIZE,
               overlap=CHUNK_OVERLAP):
    """Split text into chunks with overlapping context."""

    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def process_pdf(pdf_path):
    """Extract page text and create metadata-rich chunks."""

    reader = PdfReader(str(pdf_path))
    title = reader.metadata.title if reader.metadata else None
    title = title or pdf_path.stem.replace("-", " ")

    all_chunks = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        for index, chunk in enumerate(split_text(text), start=1):
            all_chunks.append({
                "chunk_id": (
                    f"{pdf_path.stem}-p{page_number}-c{index}"
                ),
                "title": title,
                "source": pdf_path.name,
                "page": page_number,
                "text": chunk
            })

    return all_chunks


def load_all_chunks():
    """Process every PDF in data/raw."""

    chunks = []

    for pdf_path in sorted(DATA_DIR.glob("*.pdf")):
        print(f"Processing: {pdf_path.name}")
        chunks.extend(process_pdf(pdf_path))

    return chunks


if __name__ == "__main__":
    chunks = load_all_chunks()

    print("\nChunking completed!")
    print("Total chunks:", len(chunks))

    if chunks:
        print("\nFirst chunk:")
        print(chunks[0])
