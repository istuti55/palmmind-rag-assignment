
from fastapi import FastAPI

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
