import secrets

from sqlalchemy import (
    String,
    Integer,
    Numeric,
    Boolean,
    ForeignKey,
    Index,
    DDL,
    event,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .campus_loc import CampusLoc


class ParkingArea(Base):
    __tablename__ = "parking_areas"

    id: Mapped[str] = mapped_column(
        String(8),
        primary_key=True,
        default=lambda: secrets.token_hex(4),
    )

    fid: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        unique=True,
    )

    campus_id: Mapped[str | None] = mapped_column(
        String(8),
        ForeignKey("campus_loc.id", ondelete="RESTRICT"),
        nullable=True,
    )

    label: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        unique=True,
    )

    full_capacity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    disabled_capacity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    fee: Mapped[float | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )

    fee_type: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    is_paid: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    is_reserved: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    is_disability_friendly: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    for_visitors: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    has_barriers: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
    )

    geom: Mapped[object | None] = mapped_column(
        Geometry("POLYGON", srid=4326),
        nullable=True,
    )

    # Many parking areas belong to one campus
    campus: Mapped["CampusLoc | None"] = relationship(
        "CampusLoc",
        back_populates="parking_areas",
    )

    __table_args__ = (
        Index(
            "parking_areas_geom_idx",
            "geom",
            postgresql_using="gist",
        ),
        UniqueConstraint(
            "campus_id",
            "fid",
            name="uq_parking_areas_campus_fid"
        )
    )


# Enable Row Level Security
event.listen(
    ParkingArea.__table__,
    "after_create",
    DDL(
        "ALTER TABLE parking_areas ENABLE ROW LEVEL SECURITY"
    ),
)

# Public SELECT policy
event.listen(
    ParkingArea.__table__,
    "after_create",
    DDL("""
        CREATE POLICY "Public can view parking areas"
        ON parking_areas
        FOR SELECT
        USING (true)
    """),
)
