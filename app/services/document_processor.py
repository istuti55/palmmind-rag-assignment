
import fitz
from pathlib import Path


def extract_text(filename: str, content: bytes) -> str:
    """
    Extract text from PDF or TXT files.
    """

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        pdf_document = fitz.open(
            stream=content,
            filetype="pdf"
        )

        extracted_text = ""

        for page in pdf_document:
            extracted_text += page.get_text()

        pdf_document.close()

        return extracted_text

    elif extension == ".txt":
        return content.decode("utf-8")

    else:
        raise ValueError("Unsupported file type")
