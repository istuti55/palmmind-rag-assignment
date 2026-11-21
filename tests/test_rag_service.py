
import pytest

from app.services import rag_service


def test_empty_question():
    with pytest.raises(ValueError, match="Question cannot be empty"):
        rag_service.ask_question("   ")


def test_no_relevant_documents(monkeypatch):
    monkeypatch.setattr(
        rag_service,
        "get_chat_history",
        lambda session_id: []
    )

    monkeypatch.setattr(
        rag_service,
        "generate_query_embedding",
        lambda query: [0.1, 0.2, 0.3]
    )

    monkeypatch.setattr(
        rag_service,
        "search_hybrid_chunks",
        lambda **kwargs: []
    )

    result = rag_service.ask_question(
        "What is the maternity leave policy?",
        session_id="test_session"
    )

    assert result["question"] == "What is the maternity leave policy?"
    assert result["answer"] == "No relevant information found in the documents."
    assert result["sources"] == []


def test_rag_generates_answer_and_returns_sources(monkeypatch):
    saved_messages = []

    monkeypatch.setattr(
        rag_service,
        "get_chat_history",
        lambda session_id: []
    )

    monkeypatch.setattr(
        rag_service,
        "generate_query_embedding",
        lambda query: [0.1, 0.2, 0.3]
    )

    monkeypatch.setattr(
        rag_service,
        "search_hybrid_chunks",
        lambda **kwargs: [
            {
                "text": "Employees receive 12 days of paid sick leave.",
                "filename": "hr_policy.pdf",
                "page": 2,
                "score": 0.95
            }
        ]
    )

    monkeypatch.setattr(
        rag_service,
        "generate_answer",
        lambda question, context: "Employees receive 12 days of paid sick leave."
    )

    monkeypatch.setattr(
        rag_service,
        "save_message",
        lambda session_id, role, message:
            saved_messages.append((session_id, role, message))
    )

    result = rag_service.ask_question(
        "How many sick leave days are provided?",
        session_id="test_session"
    )

    assert "12 days" in result["answer"]
    assert len(result["sources"]) == 1
    assert result["sources"][0]["filename"] == "hr_policy.pdf"
    assert result["sources"][0]["page"] == 2
    assert result["sources"][0]["score"] == 0.95

    assert len(saved_messages) == 2
    assert saved_messages[0][1] == "user"
    assert saved_messages[1][1] == "assistant"


def test_conversation_history_is_used(monkeypatch):
    captured_query = {}

    monkeypatch.setattr(
        rag_service,
        "get_chat_history",
        lambda session_id: [
            "user: How many sick leave days?",
            "assistant: Employees receive 12 days."
        ]
    )

    def fake_embedding(query):
        captured_query["query"] = query
        return [0.1, 0.2, 0.3]

    monkeypatch.setattr(
        rag_service,
        "generate_query_embedding",
        fake_embedding
    )

    monkeypatch.setattr(
        rag_service,
        "search_hybrid_chunks",
        lambda **kwargs: []
    )

    rag_service.ask_question(
        "What about annual leave?",
        session_id="test_session"
    )

    assert "How many sick leave days?" in captured_query["query"]
    assert "What about annual leave?" in captured_query["query"]
