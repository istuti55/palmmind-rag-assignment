
from app.database.db import SessionLocal
from app.database.models import Document


def save_document_metadata(
    filename: str,
    file_type: str,
    chunking_strategy: str,
    character_count: int,
    chunk_count: int
) -> dict:
    db = SessionLocal()

    try:
        document = Document(
            filename=filename,
            file_type=file_type,
            chunking_strategy=chunking_strategy,
            character_count=character_count,
            chunk_count=chunk_count
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return {
            "id": document.id,
            "filename": document.filename,
            "file_type": document.file_type,
            "chunking_strategy": document.chunking_strategy,
            "character_count": document.character_count,
            "chunk_count": document.chunk_count
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
