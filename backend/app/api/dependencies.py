from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.repositories.link_repository import LinkRepository
from app.services.link_service import LinkService


def get_link_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LinkService:
    return LinkService(LinkRepository(session))
