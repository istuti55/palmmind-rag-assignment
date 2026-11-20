from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


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