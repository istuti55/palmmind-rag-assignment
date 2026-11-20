from app.services.embedding_service import generate_embeddings
from app.services.vector_store import create_collection, store_chunks, client, COLLECTION_NAME

# Sample text chunks
chunks = [
    "Python is a programming language.",
    "FastAPI is used to build APIs."
]

# Generate embeddings
embeddings = generate_embeddings(chunks)

# Create collection
create_collection()

# Store chunks and embeddings
store_chunks(
    chunks=chunks,
    embeddings=embeddings,
    filename="test.txt",
    chunking_strategy="fixed_size"
)

print("Chunks stored successfully!")

# Check how many points are stored
result = client.count(collection_name=COLLECTION_NAME)

print("Total stored points:", result.count)