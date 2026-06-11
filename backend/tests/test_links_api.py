"""Tests for the links API endpoints."""

import httpx


async def test_create_link_endpoint(client: httpx.AsyncClient) -> None:
    response = await client.post("/links", json={"original_url": "https://example.com"})

    assert response.status_code == 201
    body = response.json()
    assert body["original_url"].startswith("https://example.com")
    assert body["short_code"]
