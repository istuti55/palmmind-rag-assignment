
from app.services.embedding_service import generate_query_embedding
from app.services.vector_store import search_similar_chunks

question = "What is FastAPI?"

# Convert the question into an embedding
query_embedding = generate_query_embedding(question)

# Search Qdrant
results = search_similar_chunks(query_embedding, limit=3)

# Display results
print("Question:", question)
print("\nRelevant document chunks:")

for result in results:
    print("\nText:", result["text"])
    print("Filename:", result["filename"])
    print("Similarity score:", result["score"])
