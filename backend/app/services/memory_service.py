import logging
import uuid
from typing import List, Dict, Any

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from app.config import settings

logger = logging.getLogger(__name__)

class MemoryService:
    """
    Service for interacting with ChromaDB to store and retrieve long-term memory (session summaries).
    """
    def __init__(self):
        # We use local persistent storage
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        
        # Use default lightweight local embeddings (all-MiniLM-L6-v2)
        # This keeps the system completely free and offline for memory retrieval.
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        self.collection = self.client.get_or_create_collection(
            name="learning_sessions",
            embedding_function=self.embedding_fn
        )
        logger.info(f"MemoryService initialized. DB path: {settings.chroma_persist_dir}")

    async def store_session(self, user_id: str, subject: str, summary: str) -> None:
        """
        Stores a session summary into the vector database.
        """
        doc_id = str(uuid.uuid4())
        
        logger.info(f"Storing session memory for User {user_id} - Subject: {subject}")
        self.collection.add(
            documents=[summary],
            metadatas=[{"user_id": user_id, "subject": subject}],
            ids=[doc_id]
        )

    async def recall_history(self, user_id: str, query: str, n_results: int = 2) -> str:
        """
        Retrieves the most relevant past session summaries for a user based on semantic search.
        """
        logger.info(f"Recalling memory for User {user_id} with query: {query}")
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"user_id": user_id}
        )
        
        if not results["documents"] or len(results["documents"][0]) == 0:
            return "No historical memory found for this user/topic."
            
        # Combine the retrieved documents into a single context string
        context = "\n\n---\n\n".join(results["documents"][0])
        return context

memory_service = MemoryService()
