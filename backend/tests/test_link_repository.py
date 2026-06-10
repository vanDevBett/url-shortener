"""Tests for the LinkRepository against a real PostgreSQL database."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.link_repository import LinkRepository


async def test_create_assigns_id_and_persists(session: AsyncSession) -> None:
    repo = LinkRepository(session)
    link = await repo.create(original_url="https://example.com", short_code="abc123")
    assert link.id is not None
    assert link.short_code == "abc123"
    assert link.created_at is not None


async def test_get_by_short_code_returns_link(session: AsyncSession) -> None:
    repo = LinkRepository(session)
    await repo.create(original_url="https://example.com", short_code="xyz789")
    found = await repo.get_by_short_code("xyz789")
    assert found is not None
    assert found.original_url == "https://example.com"


async def test_get_by_short_code_missing_returns_none(session: AsyncSession) -> None:
    repo = LinkRepository(session)
    assert await repo.get_by_short_code("missing") is None
