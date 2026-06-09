"""Tests for the Link database model."""

from sqlalchemy import create_engine, inspect

from app.core.db import Base
from app.models.link import Link  # noqa: F401  # registers the model on Base


def test_links_table_has_expected_shape() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    insp = inspect(engine)

    assert "links" in insp.get_table_names()

    columns = {c["name"]: c for c in insp.get_columns("links")}
    assert {"id", "short_code", "original_url", "created_at"} <= set(columns)
    assert columns["short_code"]["nullable"] is False
    assert columns["original_url"]["nullable"] is False

    indexes = insp.get_indexes("links")
    unique = {tuple(ix["column_names"]) for ix in indexes if ix["unique"]}
    assert ("short_code",) in unique
