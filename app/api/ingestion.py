
from typing import Literal

from fastapi import APIRouter, UploadFile, File, HTTPException, Form

from app.services.document_processor import extract_text
from app.services.chunking import (
    fixed_size_chunking,
    sentence_based_chunking
)

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
        extracted_text = extract_text(file.filename, content)

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read file: {str(error)}"
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the document"
        )

    if chunking_strategy == "fixed_size":
        chunks = fixed_size_chunking(extracted_text)

    else:
        chunks = sentence_based_chunking(extracted_text)

    return {
        "filename": file.filename,
        "message": "Document processed successfully",
        "chunking_strategy": chunking_strategy,
        "character_count": len(extracted_text),
        "chunk_count": len(chunks),
        "chunks": chunks
    }
