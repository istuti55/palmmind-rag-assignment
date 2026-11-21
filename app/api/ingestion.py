
from typing import Literal

from fastapi import APIRouter, UploadFile, File, HTTPException, Form

from app.services.document_processor import extract_text_with_pages
from app.services.chunking import chunk_pages
from app.services.embedding_service import generate_embeddings
from app.services.vector_store import create_collection, store_chunks
from app.services.document_metadata_service import save_document_metadata

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    chunking_strategy: Literal["fixed_size", "sentence_based"] = Form("fixed_size")
):
    if not file.filename or not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed"
        )

    content = await file.read()

    try:
        pages = extract_text_with_pages(file.filename, content)
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read file: {str(error)}"
        )

    extracted_text = "\n".join(page["text"] for page in pages)

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the document"
        )

    chunks_with_pages = chunk_pages(
        pages=pages,
        strategy=chunking_strategy
    )

    chunks = [item["text"] for item in chunks_with_pages]
    page_numbers = [item["page"] for item in chunks_with_pages]

    embeddings = generate_embeddings(chunks)

    create_collection()

    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename,
        chunking_strategy=chunking_strategy,
        pages=page_numbers
    )

    metadata = save_document_metadata(
        filename=file.filename,
        file_type=file.filename.rsplit(".", 1)[-1].lower(),
        chunking_strategy=chunking_strategy,
        character_count=len(extracted_text),
        chunk_count=len(chunks)
    )

    return {
        "filename": file.filename,
        "message": "Document processed successfully",
        "chunking_strategy": chunking_strategy,
        "character_count": len(extracted_text),
        "chunk_count": len(chunks),
        "storage": "Embeddings successfully stored in Qdrant",
        "document_metadata": metadata,
        "chunks": chunks_with_pages
    }
