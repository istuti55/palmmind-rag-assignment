
from app.services.rag_service import ask_question

question = "What is FastAPI?"

result = ask_question(question)

print("Question:", result["question"])
print("\nAnswer:", result["answer"])

print("\nSources:")
for source in result["sources"]:
    print(source)
