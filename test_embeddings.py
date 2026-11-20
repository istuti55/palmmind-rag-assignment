
from app.services.embedding_service import generate_embeddings

texts = [
    "Python is a programming language.",
    "FastAPI is used to build APIs."
]

embeddings = generate_embeddings(texts)

print("Number of embeddings:", len(embeddings))
print("Dimensions of first embedding:", len(embeddings[0]))
print("First embedding:", embeddings[0][:5])
