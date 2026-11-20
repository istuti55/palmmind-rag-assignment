from app.services.chunking import (
    fixed_size_chunking,
    sentence_based_chunking
)

text = """
Python is a programming language.
FastAPI is used to build APIs.
RAG helps AI answer questions using documents.
"""

print("Fixed Size Chunking:")
fixed_chunks = fixed_size_chunking(text, chunk_size=50, overlap=10)

for chunk in fixed_chunks:
    print(chunk)

print("\nSentence Based Chunking:")
sentence_chunks = sentence_based_chunking(text, max_chunk_size=60)

for chunk in sentence_chunks:
    print(chunk)