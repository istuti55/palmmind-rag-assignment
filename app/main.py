
from fastapi import FastAPI
from app.api.ingestion import router as ingestion_router

app = FastAPI(
    title="Palm Mind RAG API",
    description="Document Ingestion and Conversational RAG System",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Palm Mind RAG API is running successfully!"
    }


app.include_router(
    ingestion_router,
    prefix="/api/documents",
    tags=["Document Ingestion"]
)
