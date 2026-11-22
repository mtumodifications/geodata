
import secrets

from sqlalchemy import (
    String,
    Integer,
    Text,
    ForeignKey,
    Index,
    DDL,
    event,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry

from .base import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(
        String(8),
        primary_key=True,
        default=lambda: secrets.token_hex(4),
    )

    fid: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    building_id: Mapped[str] = mapped_column(
        String(8),
        ForeignKey("campus_buildings.id", ondelete="RESTRICT"),
        nullable=False,
    )

    room_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    primary_function: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    geom: Mapped[object | None] = mapped_column(
        Geometry("POLYGON", srid=4326),
        nullable=True,
    )

    building: Mapped["CampusBuilding"] = relationship(
        "CampusBuilding",
        back_populates="rooms",
    )

    __table_args__ = (
        Index(
            "rooms_geom_idx",
            "geom",
            postgresql_using="gist",
        ),
        Index(
            "uq_rooms_building_room_number",
            "building_id",
            "room_number",
            unique=True,
            postgresql_where=(
                (room_number.is_not(None))
                & (room_number != "VOID")
            ),
        ),
        UniqueConstraint(
            "building_id",
            "fid",
            name="uq_rooms_building_fid",
        ),
    )


event.listen(
    Room.__table__,
    "after_create",
    DDL(
        "ALTER TABLE rooms ENABLE ROW LEVEL SECURITY"
    ),
)

event.listen(
    Room.__table__,
    "after_create",
    DDL("""
        CREATE POLICY "Public can view rooms"
        ON rooms
        FOR SELECT
        USING (true)
    """),
)
