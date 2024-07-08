from qdrant_client import QdrantClient, models
from bayesrag.config import QDRANT_HOST, QDRANT_COLLECTION
from bayesrag.embedder  import get_embedding
# from bayesrag import logger

qclient = QdrantClient(url=QDRANT_HOST)

def create_db(collection_name=QDRANT_COLLECTION):
    if qclient.collection_exists(collection_name=collection_name):
        print(f"Vector DB already exists: {collection_name}")
    else:
        qclient.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
        )
        print(f"Vector DB successfully created: {collection_name}")

def upsert_embeddings(chunks):
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk.page_content)
        qclient.upsert(
            collection_name=QDRANT_COLLECTION,
            points=[
                models.PointStruct(
                    id=i, vector=embedding, payload={"data": chunk.page_content, "metadata": chunk.metadata}
                ),
            ],
        )
    print("Embeddings created successfully")
