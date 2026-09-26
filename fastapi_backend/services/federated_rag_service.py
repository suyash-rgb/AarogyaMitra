# services/federated_rag_service.py / app/services/federated_rag_service.py
from typing import List, Dict, Optional
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastembed import TextEmbedding
import logging

logger = logging.getLogger(__name__)

class FederatedRAGService:
    _instance: Optional["FederatedRAGService"] = None
    _client: Optional[QdrantClient] = None
    _embed_model: Optional[TextEmbedding] = None

    def __init__(self, storage_path: Optional[str] = None):
        if storage_path is None:
            base_dir = Path(__file__).resolve().parent.parent.parent
            storage_path = str(base_dir / "data" / "qdrant_storage")
        
        self.storage_path = storage_path

    @property
    def client(self) -> QdrantClient:
        if self._client is None:
            self._client = QdrantClient(path=self.storage_path)
        return self._client

    @property
    def embed_model(self) -> TextEmbedding:
        if self._embed_model is None:
            self._embed_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        return self._embed_model

    def retrieve(
        self,
        query: str,
        collection_name: str,
        user_state: Optional[str] = "ALL",
        limit: int = 4
    ) -> List[Dict]:
        query_vector = list(self.embed_model.embed([query]))[0].tolist()

        # Dynamic State Partitioning: Central baseline ('ALL') + Specific state ('HR', etc.)
        state_code_filter = (user_state or "ALL").upper().strip()
        state_filter = models.Filter(
            should=[
                models.FieldCondition(
                    key="metadata.state_code",
                    match=models.MatchValue(value="ALL")
                ),
                models.FieldCondition(
                    key="metadata.state_code",
                    match=models.MatchValue(value=state_code_filter)
                )
            ]
        )

        try:
            search_result = self.client.query_points(
                collection_name=collection_name,
                query=query_vector,
                query_filter=state_filter,
                limit=limit
            ).points

            return [
                {
                    "text": p.payload.get("text", ""),
                    "source": p.payload.get("metadata", {}).get("source_file", ""),
                    "scheme": p.payload.get("metadata", {}).get("scheme_name", ""),
                    "jurisdiction": p.payload.get("metadata", {}).get("jurisdiction_level", "CENTRAL"),
                    "state": p.payload.get("metadata", {}).get("state_code", "ALL"),
                    "score": round(p.score, 4)
                }
                for p in search_result
            ]
        except Exception as e:
            logger.error(f"Error querying Qdrant collection '{collection_name}': {e}", exc_info=True)
            return []

federated_rag_service = FederatedRAGService()
