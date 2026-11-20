
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Check file extension
    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed"
        )

    # Read uploaded file
    content = await file.read()

    return {
        "filename": file.filename,
        "message": "File uploaded successfully",
        "file_size": len(content)
    }
