"""Tests for the LinkService."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base62 import encode_base62
from app.repositories.link_repository import LinkRepository
from app.services.link_service import LinkService


async def test_create_link_generates_code_from_id(session: AsyncSession) -> None:
    service = LinkService(LinkRepository(session))
    link = await service.create_link("https://example.com")

    assert link.id is not None
    assert link.original_url == "https://example.com"
    assert link.short_code == encode_base62(link.id)


async def test_create_link_codes_are_unique(session: AsyncSession) -> None:
    service = LinkService(LinkRepository(session))
    first = await service.create_link("https://a.com")
    second = await service.create_link("https://b.com")

    assert first.short_code != second.short_code
