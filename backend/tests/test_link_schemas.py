"""Tests for the Link API schemas."""

import pytest
from pydantic import ValidationError

from app.schemas.link import LinkCreate, LinkRead


def test_link_create_accepts_valid_url() -> None:
    payload = LinkCreate.model_validate({"original_url": "https://example.com"})
    assert str(payload.original_url).startswith("https://example.com")


def test_link_create_rejects_invalid_url() -> None:
    with pytest.raises(ValidationError):
        LinkCreate.model_validate({"original_url": "not-a-url"})


def test_link_read_builds_from_object_attributes() -> None:
    class DummyLink:
        short_code = "abc123"
        original_url = "https://example.com"

    read = LinkRead.model_validate(DummyLink())
    assert read.short_code == "abc123"
    assert read.original_url == "https://example.com"
