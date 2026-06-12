"""Tests for the links API endpoints."""

import httpx


async def test_create_link_endpoint(client: httpx.AsyncClient) -> None:
    response = await client.post("/links", json={"original_url": "https://example.com"})

    assert response.status_code == 201
    body = response.json()
    assert body["original_url"].startswith("https://example.com")
    assert body["short_code"]


async def test_redirect_returns_307_to_original(client: httpx.AsyncClient) -> None:
    created = await client.post("/links", json={"original_url": "https://example.com"})
    short_code = created.json()["short_code"]

    response = await client.get(f"/{short_code}")

    assert response.status_code == 307
    assert response.headers["location"].startswith("https://example.com")


async def test_redirect_unknown_code_returns_404(client: httpx.AsyncClient) -> None:
    response = await client.get("/doesnotexist")
    assert response.status_code == 404


async def test_health_still_works(client: httpx.AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
