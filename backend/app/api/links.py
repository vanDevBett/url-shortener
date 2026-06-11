from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_link_service
from app.schemas.link import LinkCreate, LinkRead
from app.services.link_service import LinkService

router = APIRouter()


@router.post("/links", response_model=LinkRead, status_code=status.HTTP_201_CREATED)
async def create_link(
    payload: LinkCreate, service: Annotated[LinkService, Depends(get_link_service)]
) -> LinkRead:
    link = await service.create_link(str(payload.original_url))
    return LinkRead.model_validate(link)
