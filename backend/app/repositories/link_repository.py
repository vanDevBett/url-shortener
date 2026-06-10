from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.link import Link


class LinkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, *, original_url: str, short_code: str) -> Link:
        new_link = Link(original_url=original_url, short_code=short_code)
        self.session.add(new_link)
        await self.session.flush()
        await self.session.refresh(new_link)
        return new_link

    async def get_by_short_code(self, short_code: str) -> Link | None:
        stmt = select(Link).where(Link.short_code == short_code)
        result = await self.session.execute(stmt)
        link = result.scalar_one_or_none()
        return link
