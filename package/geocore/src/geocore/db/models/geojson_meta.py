from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Integer,
    Text,
    TIMESTAMP,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from geocore.database import Base


class GeoJSONMeta(Base):
    __tablename__ = "geojson_meta"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    file_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    table_name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    file_checksum: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    file_modified_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True,
    )

    imported_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("NOW()"),
    )

    feature_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        server_default=text("'success'"),
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
