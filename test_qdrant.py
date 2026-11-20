from app.services.vector_store import create_collection, client

create_collection()

collections = client.get_collections().collections

print("Qdrant connected successfully!")

for collection in collections:
    print("Collection:", collection.name)