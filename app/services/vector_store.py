from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from uuid import uuid4
from qdrant_client.models import PointStruct


# Connect to Qdrant
client = QdrantClient(url="http://localhost:6333")


# Collection name
COLLECTION_NAME = "documents"


def create_collection() -> None:
    """
    Create a collection in Qdrant to store document embeddings.
    """
    collections = client.get_collections().collections

    collection_exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections
    )

    if not collection_exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )

def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    filename: str,
    chunking_strategy: str
) -> None:
    """
    Store document chunks and their embeddings in Qdrant.
    """

    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks and embeddings must match")

    points = []

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point = PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "filename": filename,
                "chunk_index": index,
                "chunking_strategy": chunking_strategy
            }
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )