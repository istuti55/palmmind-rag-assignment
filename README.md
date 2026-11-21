# Palm Mind AI – Conversational RAG System

A document-based Conversational Retrieval-Augmented Generation (RAG) system built with FastAPI, Google Gemini, Qdrant, Redis, and PostgreSQL.

The system allows users to upload PDF and TXT documents, ask questions about their content, receive context-aware answers with source references, and interact with an AI-powered interview booking assistant.

## Features

### Document Ingestion
- PDF and TXT document upload
- PDF text extraction with page number preservation
- Two configurable chunking strategies:
  - Fixed-size chunking with overlap
  - Sentence-based chunking
- Document metadata persistence in PostgreSQL

### Retrieval-Augmented Generation
- Text embeddings using Google Gemini
- Vector storage and retrieval using Qdrant
- Hybrid search combining semantic vector search and BM25 full-text search
- BM25 scoring enabled for Qdrant full-text search
- Reciprocal Rank Fusion (RRF) for combining retrieval results
- Context-aware answer generation using Gemini
- Page-level source citations for PDF documents
- Conversational memory using Redis
- Custom RAG pipeline without a pre-built RetrievalQAChain

### AI-Powered Interview Booking
- Natural-language interview booking conversations
- Automatic extraction of booking details using Gemini
- Collection of candidate name, email, interview date, and time
- Email, date, and time validation
- Prevention of repeated bookings within a completed session
- Booking persistence using PostgreSQL
- Redis-based session booking state with a 30-day expiry

### Evaluation and Testing
- RAG evaluation script with a manually curated evaluation dataset
- Answer and source accuracy evaluation
- Precision@3 and Recall@3 metrics
- 23 automated tests using pytest

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| Google Gemini | LLM and text embeddings |
| Qdrant | Vector database and hybrid retrieval |
| Redis | Conversational memory and session state |
| PostgreSQL | Document metadata and booking persistence |
| SQLAlchemy | Database ORM |
| PyMuPDF | PDF text extraction |
| Pydantic | Data validation |
| Docker | Running supporting services |
| Pytest | Automated testing |

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
├── tests/
│   ├── test_chunking.py
│   ├── test_document_processor.py
│   ├── test_rag_service.py
│   └── test_interview_service.py
│
├── evaluate_rag.py
├── evaluation_dataset.json
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

The requirements file is located in the project root.

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key

DATABASE_URL=postgresql+psycopg://raguser:ragpassword@localhost:5433/ragdb

QDRANT_URL=http://localhost:6333

REDIS_HOST=localhost
REDIS_PORT=6380
```

Replace the Gemini API key placeholder with your own API key. Adjust database credentials if you use different PostgreSQL settings.

**Important:** Never commit your `.env` file or expose API credentials.

### 5. Start supporting services

Make sure Docker Desktop is running.

**Qdrant**

```bash
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

**Redis**

The application uses port `6380` on the host, mapped to Redis's default container port `6379`.

```bash
docker run -d --name redis-docker -p 6380:6379 redis
```

**PostgreSQL**

```bash
docker run -d --name postgres -e POSTGRES_USER=raguser -e POSTGRES_PASSWORD=ragpassword -e POSTGRES_DB=ragdb -p 5433:5432 -v postgres_data:/var/lib/postgresql/data postgres:17
```

If the containers already exist, start them using:

```bash
docker start qdrant redis-docker postgres
```

Ensure the `.env` connection settings match the ports and credentials used by your containers.

### 6. Initialize the database

```bash
python -m app.database.init_db
```

### 7. Run the application

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Endpoints

### 1. Document Upload

**Endpoint:** `POST /api/documents/upload`

Upload a PDF or TXT document.

Form fields:

- `file`: PDF or TXT document
- `chunking_strategy`: `fixed_size` or `sentence_based`

Processing workflow:

1. Extract text from the uploaded document.
2. Preserve PDF page information.
3. Divide the extracted text into chunks using the selected strategy.
4. Generate embeddings using Gemini.
5. Store vectors and chunk information in Qdrant.
6. Save document metadata in PostgreSQL.

### 2. Conversational Chat

**Endpoint:** `POST /api/chat`

Example request:

```json
{
  "question": "What is Retrieval Augmented Generation?",
  "session_id": "candidate_001"
}
```

Processing workflow:

1. Retrieve conversation history from Redis.
2. Generate a query embedding.
3. Retrieve relevant document chunks using hybrid search.
4. Combine semantic and BM25 retrieval results using RRF.
5. Provide retrieved context to Gemini.
6. Generate a context-aware answer.
7. Return the answer with source information.
8. Save conversation messages in Redis.

### 3. Interview Booking

The conversational chat endpoint also supports interview booking.

Example request:

```json
{
  "question": "I want to book an interview.",
  "session_id": "candidate_001"
}
```

The assistant collects the candidate's:

- Name
- Email
- Interview date
- Interview time

Gemini extracts booking details from the conversation. The application validates the information before saving the booking in PostgreSQL.

Redis stores the completed booking ID for each session with a 30-day expiry, preventing repeated bookings within that session.

## Testing

The project includes 23 automated tests implemented using pytest.

The complete test suite currently passes all 23 tests.

Run the complete test suite:

```bash
python -m pytest -v
```

### Test Coverage

| Test file | Tests |
|---|---:|
| `test_chunking.py` | 6 |
| `test_document_processor.py` | 4 |
| `test_rag_service.py` | 4 |
| `test_interview_service.py` | 9 |
| **Total** | **23** |

The tests cover:

- Fixed-size and sentence-based chunking
- Chunk size and overlap validation
- PDF and TXT extraction
- PDF page number preservation
- Unsupported file types
- Empty question handling
- RAG retrieval and answer generation
- Conversation history handling
- Interview booking validation
- Duplicate booking prevention within a session
- Successful booking flow

Service-level tests use mocked dependencies where appropriate, avoiding unnecessary calls to external services.

## RAG Evaluation

The project includes a basic RAG evaluation pipeline using:

- `evaluate_rag.py`
- `evaluation_dataset.json`

The evaluation dataset contains manually curated questions, expected answers, and expected source information.

The evaluation script measures:

- Answer accuracy
- Source accuracy
- Correct abstentions for unanswerable questions
- Precision@3
- Recall@3

The evaluation provides a small benchmark for checking retrieval and answer-generation behavior. Results should be interpreted in the context of the limited, manually curated dataset.

## System Architecture

### Document Ingestion Flow

1. User uploads a PDF or TXT document.
2. FastAPI receives the document.
3. PyMuPDF or text decoding extracts the content.
4. The selected chunking strategy divides the content.
5. Gemini generates embeddings.
6. Qdrant stores the vectors and associated chunk payloads.
7. PostgreSQL stores document metadata.

### Conversational RAG Flow

1. User submits a question.
2. Redis provides previous conversation history.
3. Gemini generates a query embedding.
4. Qdrant performs semantic and BM25 retrieval.
5. Reciprocal Rank Fusion combines the retrieval results.
6. Relevant chunks are passed to Gemini as context.
7. Gemini generates the answer.
8. Source information is returned with the response.
9. Redis stores the conversation history.

### Interview Booking Flow

1. User expresses interview booking intent.
2. Gemini extracts booking details from the conversation.
3. The application checks for missing information.
4. Email, date, and time are validated.
5. Valid booking information is saved in PostgreSQL.
6. Redis stores the completed booking state for the session.
7. The assistant returns the booking confirmation.

## Important Notes

- This project provides backend REST APIs; a separate frontend is not included.
- Docker must be running before starting the application.
- A valid Gemini API key is required.
- Qdrant, Redis, and PostgreSQL must be accessible using the configured connection settings.
- The RAG evaluation dataset is a small manually curated benchmark and does not represent comprehensive real-world evaluation.

## Author

Developed as a technical assignment for Palm Mind AI.

GitHub: https://github.com/istuti55
