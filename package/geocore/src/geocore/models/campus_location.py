import secrets

from sqlalchemy import String, event, DDL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry

from .base import Base


class CampusLocation(Base):
    __tablename__ = "campus_locations"

    id: Mapped[str] = mapped_column(
        String(8),
        primary_key=True,
        default=lambda: secrets.token_hex(4),
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    geom: Mapped[object] = mapped_column(
        Geometry("POLYGON", srid=4326),
        nullable=False,
    )


# Enable Row Level Security after table creation
event.listen(
    CampusLocation.__table__,
    "after_create",
    DDL("ALTER TABLE campus_locations ENABLE ROW LEVEL SECURITY"),


)

# Create SELECT policy
event.listen(
    CampusLocation.__table__,
    "after_create",
    DDL("""
    CREATE POLICY "Public can view campus locations"
    ON campus_locations
    FOR SELECT
    USING (true)
"""),
)
