
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client import models
from uuid import uuid4

load_dotenv()

# Connect to Qdrant using environment variables
client = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333")
)

# Collection name
COLLECTION_NAME = "documents"


def create_collection() -> None:
    """
    Create the Qdrant collection and its BM25 text index.
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

    # Check whether the text index already exists.
    collection_info = client.get_collection(COLLECTION_NAME)

    if "text" not in collection_info.payload_schema:
        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="text",
            field_schema=models.TextIndexParams(
                type="text",
                tokenizer="word",
                min_token_len=2,
                max_token_len=40,
                lowercase=True,
                scoring=True
            ),
            wait=True
        )


def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    filename: str,
    chunking_strategy: str,
    pages: list[int | None] | None = None
) -> None:

    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks and embeddings must match")

    if pages is not None and len(chunks) != len(pages):
        raise ValueError("Number of chunks and page numbers must match")

    points = []

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point = PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "filename": filename,
                "chunk_index": index,
                "chunking_strategy": chunking_strategy,
                "page": pages[index] if pages is not None else None
            }
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


def search_similar_chunks(
    query_embedding: list[float],
    limit: int = 3
) -> list[dict]:

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        with_payload=True
    )

    return [
        {
            "text": point.payload["text"],
            "filename": point.payload["filename"],
            "page": point.payload.get("page"),
            "score": point.score
        }
        for point in results.points
    ]


def search_hybrid_chunks(
    query_text: str,
    query_embedding: list[float],
    limit: int = 3
) -> list[dict]:
    """
    Combine semantic search and BM25 keyword search
    using Reciprocal Rank Fusion (RRF).
    """

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        prefetch=[
            models.Prefetch(
                query=query_embedding,
                limit=10
            ),
            models.Prefetch(
                query=models.TextQuery(text=query_text),
                using="text",
                limit=10
            )
        ],
        query=models.FusionQuery(
            fusion=models.Fusion.RRF
        ),
        limit=limit,
        with_payload=True
    )

    return [
        {
            "text": point.payload["text"],
            "filename": point.payload["filename"],
            "page": point.payload.get("page"),
            "score": point.score
        }
        for point in results.points
    ]
