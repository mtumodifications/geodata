# from .database import SessionLocal

from .seed_geojson import (
    insert_campus_locations,
    insert_campus_buildings,
    insert_parking_areas,
    insert_venues
)

from .config import DATA_DIR


def main():
    insert_campus_locations(
        f"{DATA_DIR}/geojson/campus/cork_campus_perimeter.geojson")
    insert_campus_buildings(
        f"{DATA_DIR}/geojson/buildings/cork_buildings.geojson")
    insert_parking_areas(
        f"{DATA_DIR}/geojson/transport/cork_parking_areas.geojson")

    insert_venues(
        f"{DATA_DIR}/geojson/venues/cork_main_building_floor_0.geojson"
    )
    insert_venues(
        f"{DATA_DIR}/geojson/venues/cork_main_building_floor_1.geojson"
    )


if __name__ == "__main__":
    main()
