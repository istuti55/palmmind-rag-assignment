
from app.services.embedding_service import generate_query_embedding
from app.services.vector_store import search_similar_chunks
from app.services.llm_service import generate_answer
from app.services.redis_service import save_message, get_chat_history


def ask_question(question: str, session_id: str = "default") -> dict:
    """
    Answer questions using RAG and maintain conversation history.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty")

    # 1. Get previous conversation history from Redis
    history = get_chat_history(session_id)

    # 2. Combine history with the current question
    conversation = "\n".join(history)
    search_query = conversation + "\nuser: " + question

    # 3. Generate embedding for the search query
    query_embedding = generate_query_embedding(search_query)

    # 4. Retrieve relevant chunks from Qdrant
    results = search_similar_chunks(query_embedding, limit=3)

    if not results:
        return {
            "question": question,
            "answer": "No relevant information found in the documents.",
            "sources": []
        }

    # 5. Prepare document context
    context = "\n\n".join(
        result["text"] for result in results
    )

    # 6. Include conversation history in the LLM prompt
    prompt_question = f"""
    Previous conversation:
    {conversation}

    Current question:
    {question}

    Answer the current question using the document context.
    Consider the previous conversation when understanding the question.
    """

    # 7. Generate answer using Gemini
    answer = generate_answer(prompt_question, context)

    # 8. Save the new messages in Redis
    save_message(session_id, "user", question)
    save_message(session_id, "assistant", answer)

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
