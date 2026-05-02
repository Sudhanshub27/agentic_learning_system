import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_progress_mastery_endpoint(client: AsyncClient):
    """Test the mock mastery endpoint."""
    response = await client.get("/api/progress/mastery/test_user_123")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user_123"
    assert "overall_mastery" in data

@pytest.mark.asyncio
async def test_progress_retention_endpoint(client: AsyncClient):
    """Test the ML retention warnings endpoint."""
    response = await client.get("/api/progress/retention/test_user_123")
    assert response.status_code == 200
    data = response.json()
    assert "warnings" in data
    
# We do not test the /api/learning/start endpoint here because it calls the LLMs extensively
# and would make the test suite very slow and flaky due to API rate limits/costs. 
# In a real setup, we would mock the `llm_service.generate` method.
