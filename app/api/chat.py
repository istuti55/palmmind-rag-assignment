
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag_service import ask_question
from app.services.interview_service import process_interview_message

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        # First, check whether the message is about interview booking
        booking_result = process_interview_message(
            session_id=request.session_id,
            message=request.question
        )

        # If it is a booking conversation, return its response
        if booking_result["booking_intent"]:
            return booking_result

        # Otherwise, process it using the RAG system
        return ask_question(
            request.question,
            session_id=request.session_id
        )

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
