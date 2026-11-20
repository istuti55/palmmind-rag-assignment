
from app.services.llm_service import generate_answer

question = "What is FastAPI?"

context = """
FastAPI is a Python framework used to build APIs.
It helps developers create APIs.
"""

answer = generate_answer(question, context)

print("Question:", question)
print("Answer:", answer)
