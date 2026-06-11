from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from app.api.dependencies import get_link_service
from app.schemas.link import LinkCreate, LinkRead
from app.services.link_service import LinkService

router = APIRouter()

LinkServiceDep = Annotated[LinkService, Depends(get_link_service)]


@router.post("/links", response_model=LinkRead, status_code=status.HTTP_201_CREATED)
async def create_link(payload: LinkCreate, service: LinkServiceDep) -> LinkRead:
    link = await service.create_link(str(payload.original_url))
    return LinkRead.model_validate(link)


@router.get("/{short_code}", response_class=RedirectResponse)
async def get_by_code(short_code: str, service: LinkServiceDep) -> RedirectResponse:
    link = await service.get_link(short_code)
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=link.original_url, status_code=307)
