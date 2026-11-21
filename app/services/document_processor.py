
from pathlib import Path

import pymupdf


def extract_text_with_pages(filename: str, content: bytes) -> list[dict]:
    """
    Extract text from PDF or TXT files while preserving page numbers.
    """

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        pdf_document = pymupdf.open(stream=content, filetype="pdf")

        extracted_pages = []

        for page_number, page in enumerate(pdf_document, start=1):
            extracted_text = page.get_text()

            if extracted_text.strip():
                extracted_pages.append({
                    "page": page_number,
                    "text": extracted_text
                })

        pdf_document.close()

        return extracted_pages

    elif extension == ".txt":
        extracted_text = content.decode("utf-8")

        return [{
            "page": None,
            "text": extracted_text
        }]

    else:
        raise ValueError("Unsupported file type")
