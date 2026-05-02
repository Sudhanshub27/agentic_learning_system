import pytest
import chromadb
from app.services.memory_service import MemoryService
from app.config import settings

@pytest.mark.asyncio
async def test_memory_service_store_and_recall():
    """Verify that we can store a session in ChromaDB and retrieve it."""
    
    # Use an in-memory client for testing
    test_service = MemoryService()
    test_service.client = chromadb.EphemeralClient()
    test_service.collection = test_service.client.get_or_create_collection("test_sessions")
    
    user_id = "test_user_123"
    subject = "Python Programming"
    summary = "User struggled with decorators but finally understood closures. Mastery score reached 0.8."
    
    # Store
    await test_service.store_session(user_id, subject, summary)
    
    # Recall
    recalled = await test_service.recall_history(user_id, "How did the user do with decorators?")
    
    assert "decorators" in recalled
    assert "0.8" in recalled
    
@pytest.mark.asyncio
async def test_memory_service_empty_recall():
    test_service = MemoryService()
    test_service.client = chromadb.EphemeralClient()
    test_service.collection = test_service.client.get_or_create_collection("test_sessions")
    
    # Recall for unknown user
    recalled = await test_service.recall_history("unknown_user", "How did the user do?")
    assert "No historical memory found" in recalled
