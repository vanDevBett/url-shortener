from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Link(Base):
    """A shortened link mapping a public code to a destination URL."""

    __tablename__ = "links"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    short_code: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    original_url: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
