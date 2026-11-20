
from app.services.embedding_service import generate_query_embedding

question = "What is FastAPI?"

embedding = generate_query_embedding(question)

print("Question:", question)
print("Embedding dimensions:", len(embedding))
print("First 5 values:", embedding[:5])
