from pydantic import BaseModel, ConfigDict, HttpUrl


class LinkCreate(BaseModel):
    original_url: HttpUrl


class LinkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    short_code: str
    original_url: str
