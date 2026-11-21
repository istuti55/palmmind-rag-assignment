
import pytest
import pymupdf

from app.services.document_processor import extract_text_with_pages


def test_extract_txt_file():
    content = b"Hello, this is a test document."

    result = extract_text_with_pages("sample.txt", content)

    assert len(result) == 1
    assert result[0]["page"] is None
    assert result[0]["text"] == "Hello, this is a test document."


def test_extract_pdf_with_page_numbers():
    pdf = pymupdf.open()

    page1 = pdf.new_page()
    page1.insert_text((50, 50), "Sick Leave Policy")

    page2 = pdf.new_page()
    page2.insert_text((50, 50), "Annual Leave Policy")

    pdf_bytes = pdf.tobytes()
    pdf.close()

    result = extract_text_with_pages("sample.pdf", pdf_bytes)

    assert len(result) == 2
    assert result[0]["page"] == 1
    assert "Sick Leave Policy" in result[0]["text"]
    assert result[1]["page"] == 2
    assert "Annual Leave Policy" in result[1]["text"]


def test_skip_empty_pdf_pages():
    pdf = pymupdf.open()

    page1 = pdf.new_page()
    page1.insert_text((50, 50), "Page with content")

    pdf.new_page()  # Empty page

    pdf_bytes = pdf.tobytes()
    pdf.close()

    result = extract_text_with_pages("sample.pdf", pdf_bytes)

    assert len(result) == 1
    assert result[0]["page"] == 1


def test_unsupported_file_type():
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_text_with_pages("sample.docx", b"some content")
