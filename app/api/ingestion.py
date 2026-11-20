
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_processor import extract_text

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    if not file.filename.lower().endswith((".pdf", ".txt")):
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

    return {
        "filename": file.filename,
        "message": "Text extracted successfully",
        "extracted_text": extracted_text,
        "character_count": len(extracted_text)
    }
