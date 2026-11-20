
from app.services.embedding_service import generate_query_embedding
from app.services.vector_store import search_similar_chunks
from app.services.llm_service import generate_answer


def ask_question(question: str) -> dict:
    """
    Answer a question using document retrieval and Gemini.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty")

    # 1. Convert the question into an embedding
    query_embedding = generate_query_embedding(question)

    # 2. Retrieve relevant chunks from Qdrant
    results = search_similar_chunks(query_embedding, limit=3)

    if not results:
        return {
            "question": question,
            "answer": "No relevant information found in the documents.",
            "sources": []
        }

    # 3. Combine retrieved chunks into context
    context = "\n\n".join(
        result["text"] for result in results
    )

    # 4. Generate an answer using Gemini
    answer = generate_answer(question, context)

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "filename": result["filename"],
                "score": result["score"]
            }
            for result in results
        ]
    }
