from sqlalchemy import select, func
from sqlalchemy.orm import Session


def get_building_rooms(
    db: Session,
    building_id: str,
    floor: int | None = None,
):
    stmt = select(
        func.get_building_rooms(
            floor,
            building_id,
        )
    )

    result = db.execute(stmt).scalar_one()

    return result
