from qdrant_client import QdrantClient, models
from bayesrag.config import QDRANT_HOST, QDRANT_COLLECTION
from bayesrag.embedder  import get_embedding
# from bayesrag import logger
from loguru import logger
qclient = QdrantClient(url=QDRANT_HOST)

class VectorDB:
    def __init__(self,collection_name):
        self.collection_name = collection_name

    def create_db(self):
        if qclient.collection_exists(collection_name=self.collection_name):
            logger.debug(f"Vector DB already exists: {self.collection_name}")
        else:
            qclient.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
            )
            logger.info(f"Vector DB successfully created: {self.collection_name}")

    def upsert_embeddings(self,chunks,):
        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk.page_content)
            qclient.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=i, vector=embedding, payload={"data": chunk.page_content, "metadata": chunk.metadata}
                    ),
                ],
            )
        logger.info("Embeddings created successfully")
