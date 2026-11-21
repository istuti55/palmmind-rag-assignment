
import pytest

from app.services.chunking import (
    fixed_size_chunking,
    sentence_based_chunking,
    chunk_pages
)


def test_fixed_size_chunking():
    text = "A" * 1000

    chunks = fixed_size_chunking(
        text,
        chunk_size=500,
        overlap=50
    )

    assert len(chunks) == 3
    assert len(chunks[0]) == 500
    assert len(chunks[1]) == 500
    assert len(chunks[2]) == 100


def test_fixed_size_invalid_chunk_size():
    with pytest.raises(ValueError):
        fixed_size_chunking("Hello world", chunk_size=0)


def test_fixed_size_invalid_overlap():
    with pytest.raises(ValueError):
        fixed_size_chunking("Hello world", chunk_size=100, overlap=100)


def test_sentence_based_chunking():
    text = "First sentence. Second sentence. Third sentence."

    chunks = sentence_based_chunking(
        text,
        max_chunk_size=30
    )

    assert len(chunks) == 2
    assert "First sentence." in chunks[0]
    assert "Second sentence." in chunks[1]
    assert "Third sentence." in chunks[1]


def test_sentence_based_chunking():
    text = "First sentence. Second sentence. Third sentence."

    chunks = sentence_based_chunking(
        text,
        max_chunk_size=30
    )

    assert len(chunks) == 3
    assert "First sentence." in chunks[0]
    assert "Second sentence." in chunks[1]
    assert "Third sentence." in chunks[2]


def test_chunk_pages_preserves_page_numbers():
    pages = [
        {
            "page": 1,
            "text": "First page content."
        },
        {
            "page": 2,
            "text": "Second page content."
        }
    ]

    chunks = chunk_pages(
        pages,
        strategy="sentence_based",
        chunk_size=100
    )

    assert len(chunks) == 2
    assert chunks[0]["page"] == 1
    assert chunks[1]["page"] == 2


def test_chunk_pages_invalid_strategy():
    pages = [
        {
            "page": 1,
            "text": "Test content."
        }
    ]

    with pytest.raises(ValueError, match="Unsupported chunking strategy"):
        chunk_pages(pages, strategy="invalid")
