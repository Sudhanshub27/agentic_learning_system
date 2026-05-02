"""
Tests for health check endpoints.
Verifies the FastAPI app starts and responds correctly.
"""

import pytest


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test that the root endpoint returns app info."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "Agentic Learning System" in data["name"]


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test that the health endpoint reports healthy status."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "llm_providers" in data
    assert "ollama" in data["llm_providers"]
