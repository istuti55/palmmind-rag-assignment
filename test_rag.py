
from app.services.rag_service import ask_question
from app.services.redis_service import redis_client

# Clear old test conversation
redis_client.delete("chat:rag_test")

session_id = "rag_test"

# First question
print("QUESTION 1: What is FastAPI?")
result1 = ask_question("What is FastAPI?", session_id)
print("ANSWER 1:", result1["answer"])

# Follow-up question
print("\nQUESTION 2: What is it used for?")
result2 = ask_question("What is it used for?", session_id)
print("ANSWER 2:", result2["answer"])
