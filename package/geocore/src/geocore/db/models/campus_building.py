import secrets

from sqlalchemy import (
    String,
    Integer,
    Text,
    ForeignKey,
    Index,
    DDL,
    event,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from typing import TYPE_CHECKING

from .base import Base


class CampusBuilding(Base):
    __tablename__ = "campus_buildings"

    id: Mapped[str] = mapped_column(
        String(8),
        primary_key=True,
        default=lambda: secrets.token_hex(4),
    )

    fid: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    campus_id: Mapped[str | None] = mapped_column(
        String(8),
        ForeignKey("campus_loc.id", ondelete="RESTRICT"),
        nullable=True,
    )

    building_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    building_section: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    floors: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    room_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        default=0,
    )

    mapped_rooms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    geom: Mapped[object | None] = mapped_column(
        Geometry("POLYGON", srid=4326),
        nullable=True,
    )

    # many buildings belong to one campus
    campus: Mapped["CampusLoc | None"] = relationship(
        "CampusLoc",
        back_populates="buildings",
    )
    
    # one building has many rooms
    rooms: Mapped[list["Room"]] = relationship(
        "Room",
        back_populates="building",
    )

    __table_args__ = (
        Index(
            "campus_buildings_geom_idx",
            "geom",
            postgresql_using="gist",
        ),
        UniqueConstraint(
            "campus_id",
            "fid",
            name="uq_campus_buildings_campus_fid",
        ),
    )


# Enable Row Level Security
event.listen(
    CampusBuilding.__table__,
    "after_create",
    DDL(
        "ALTER TABLE campus_buildings ENABLE ROW LEVEL SECURITY"
    ),
)

# Public SELECT policy
event.listen(
    CampusBuilding.__table__,
    "after_create",
    DDL("""
        CREATE POLICY "Public can view campus buildings"
        ON campus_buildings
        FOR SELECT
        USING (true)
    """),
)
