import logging
from typing import List

logger = logging.getLogger(__name__)

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except Exception:
    chromadb = None
    CHROMA_AVAILABLE = False


class ChromaClient:
    def __init__(self, url: str = "http://localhost:8001"):
        self.url = url
        self.client = None
        if CHROMA_AVAILABLE:
            try:
                self.client = chromadb.Client(Settings(chroma_api_impl="rest", chroma_server_host=url.replace('http://',''), chroma_server_http_port=8001))
                logger.info("Connected to ChromaDB at %s", url)
            except Exception:
                logger.exception("Failed to connect to ChromaDB")

    def upsert(self, collection_name: str, ids: List[str], embeddings: List[List[float]], metadatas: List[dict]):
        if not self.client:
            logger.warning("Chroma client not available; skipping upsert")
            return
        collection = self.client.get_or_create_collection(name=collection_name)
        collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)

    def query(self, collection_name: str, query_embedding: List[float], n_results: int = 5):
        if not self.client:
            logger.warning("Chroma client not available; returning empty results")
            return []
        collection = self.client.get_or_create_collection(name=collection_name)
        results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
        # results: dict with ids, distances, metadatas
        return results


chroma_client = ChromaClient()
