from app.services.embedding_service import generate_query_embedding
from app.services.vector_store import search_hybrid_chunks
from app.services.llm_service import generate_answer
from app.services.redis_service import save_message, get_chat_history


def ask_question(question: str, session_id: str = "default") -> dict:
    if not question.strip():
        raise ValueError("Question cannot be empty")

    history = get_chat_history(session_id)
    conversation = "\n".join(history)

    search_query = conversation + "\nuser: " + question

    query_embedding = generate_query_embedding(search_query)

    results = search_hybrid_chunks(
        query_text=question,
        query_embedding=query_embedding,
        limit=3
    )

    if not results:
        return {
            "question": question,
            "answer": "No relevant information found in the documents.",
            "sources": []
        }

    context = "\n\n".join(
        result["text"] for result in results
    )

    prompt_question = f"""
    Previous conversation:
    {conversation}

    Current question:
    {question}

    Answer the current question using the document context.
    Consider the previous conversation when understanding the question.
    """

    answer = generate_answer(prompt_question, context)

    save_message(session_id, "user", question)
    save_message(session_id, "assistant", answer)

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "filename": result["filename"],
                "page": result["page"],
                "score": result["score"]
            }
            for result in results
        ]
    }