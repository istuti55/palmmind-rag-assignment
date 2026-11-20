
from fastapi import FastAPI
from app.api.ingestion import router as ingestion_router
from app.api.chat import router as chat_router

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
app.include_router(
    chat_router,
    prefix="/api",
    tags=["Chat"]
)