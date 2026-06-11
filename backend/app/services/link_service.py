from app.core.base62 import encode_base62
from app.models.link import Link
from app.repositories.link_repository import LinkRepository


class LinkService:
    def __init__(self, link_repo: LinkRepository):
        self.link_repo = link_repo

    async def create_link(self, original_url: str) -> Link:
        next_id = await self.link_repo.reserve_next_id()
        short_code = encode_base62(next_id)
        new_link = await self.link_repo.create(
            link_id=next_id, original_url=original_url, short_code=short_code
        )
        return new_link

    async def get_link(self, short_code: str) -> Link | None:
        link = await self.link_repo.get_by_short_code(short_code=short_code)
        return link
