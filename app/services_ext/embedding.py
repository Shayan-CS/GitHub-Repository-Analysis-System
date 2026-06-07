import logging
from typing import List
import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingClient:
    def __init__(self):
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Loaded sentence-transformers model")
        except Exception:
            self.model = None
            logger.warning("sentence-transformers not available, using fallback embeddings")

    def embed_text(self, texts: List[str]) -> List[List[float]]:
        if self.model:
            vectors = self.model.encode(texts, show_progress_bar=False)
            return [v.tolist() for v in vectors]
        # fallback: deterministic numeric embedding via hash
        out = []
        for t in texts:
            h = abs(hash(t)) % (10 ** 8)
            vec = np.random.RandomState(h).randn(384).tolist()
            out.append(vec)
        return out

    def embed_query(self, query: str) -> List[float]:
        return self.embed_text([query])[0]

embedding_client = EmbeddingClient()
