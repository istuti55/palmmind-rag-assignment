# Palm Mind AI – Conversational RAG System

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system with conversational memory and an AI-powered interview booking assistant.

Users can upload PDF and TXT documents, ask questions about their content, and interact with an interview booking assistant through REST APIs.

## Features

- PDF and TXT document ingestion
- Two chunking strategies:
  - Fixed-size chunking
  - Sentence-based chunking
- Text embeddings using Google Gemini
- Vector storage and semantic search using Qdrant
- Context-aware answers using Gemini LLM
- Conversational memory using Redis
- Interview booking through natural language
- Interview detail validation (name, email, date, and time)
- Booking persistence using PostgreSQL
- Document metadata storage
- REST APIs built with FastAPI

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| Google Gemini | LLM and embeddings |
| Qdrant | Vector database |
| Redis | Conversational memory |
| PostgreSQL | Persistent metadata and bookings |
| SQLAlchemy | Database ORM |
| PyMuPDF | PDF text extraction |
| Docker | Database and service containers |
| Pydantic | Data validation |

## Project Structure

```text
palmmind-rag-assignment/
│
├── app/
│   ├── api/
│   │   ├── chat.py
│   │   └── ingestion.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   ├── init_db.py
│   │   └── models.py
│   │
│   ├── services/
│   │   ├── booking_service.py
│   │   ├── chunking.py
│   │   ├── document_metadata_service.py
│   │   ├── document_processor.py
│   │   ├── embedding_service.py
│   │   ├── interview_service.py
│   │   ├── llm_service.py
│   │   ├── rag_service.py
│   │   ├── redis_service.py
│   │   └── vector_store.py
│   │
│   └── main.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/istuti55/palmmind-rag-assignment.git
cd palmmind-rag-assignment
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql+psycopg://raguser:ragpassword@localhost:5433/ragdb
```

Replace the Gemini API key placeholder with your own key.

**Never commit your `.env` file or expose your API key.**

### 5. Start the Docker services

Qdrant:

```bash
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

Redis:

```bash
docker run -d --name redis-docker -p 6380:6379 redis
```

PostgreSQL:

```bash
docker run -d --name postgres -e POSTGRES_USER=raguser -e POSTGRES_PASSWORD=ragpassword -e POSTGRES_DB=ragdb -p 5433:5432 -v postgres_data:/var/lib/postgresql/data postgres:17
```

If these containers already exist, start them with `docker start` instead of creating duplicates.

### 6. Initialize the database

```bash
python -m app.database.init_db
```

### 7. Run the application

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

### 1. Document Upload

**Endpoint:** `POST /api/documents/upload`

Upload a PDF or TXT document.

Form fields:

- `file`: PDF or TXT document
- `chunking_strategy`: `fixed_size` or `sentence_based`

The API extracts text, creates chunks, generates embeddings, stores vectors in Qdrant, and saves document metadata in PostgreSQL.

### 2. Conversational Chat

**Endpoint:** `POST /api/chat`

Example request:

```json
{
  "question": "What is Retrieval Augmented Generation?",
  "session_id": "candidate_001"
}
```

The API retrieves relevant document chunks, generates an answer using Gemini, and maintains conversation history using Redis.

The same endpoint also supports interview booking conversations.

Example booking request:

```json
{
  "question": "I want to book an interview.",
  "session_id": "candidate_001"
}
```

The assistant collects the candidate's name, email, interview date, and time before saving the booking in PostgreSQL.

## Testing

The project includes individual test scripts for components such as:

- Chunking
- Embeddings
- Qdrant
- Document retrieval
- Gemini LLM
- RAG
- Redis
- PostgreSQL
- Interview booking

Run individual tests using:

```bash
python test_chunking.py
python test_embeddings.py
python test_qdrant.py
python test_rag.py
python test_redis.py
python test_database.py
python test_booking.py
python test_interview.py
```

## Architecture

1. Documents are uploaded through the ingestion API.
2. Text is extracted and divided using the selected chunking strategy.
3. Gemini generates embeddings for the document chunks.
4. Qdrant stores the embeddings and associated text.
5. User questions are converted into query embeddings.
6. Relevant document chunks are retrieved from Qdrant.
7. Gemini generates answers using the retrieved context.
8. Redis maintains conversation history.
9. Interview booking information is validated and stored in PostgreSQL.

## Important Notes

- This project provides backend APIs; a separate frontend is not included.
- Docker must be running before starting the application.
- Valid Gemini API credentials are required.
- Redis, Qdrant, and PostgreSQL must be accessible using the configured ports.

## Author

Developed as a technical assignment for Palm Mind AI.