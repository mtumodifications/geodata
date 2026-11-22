import argparse

from .seed_geojson import (
    insert_campus_locations,
    insert_campus_buildings,
    insert_parking_areas,
    insert_rooms,
)

from .config import DATA_DIR


def seed():
    insert_campus_locations(
        f"{DATA_DIR}/geojson/campus/cork_campus_perimeter.geojson"
    )
    insert_campus_buildings(
        f"{DATA_DIR}/geojson/buildings/cork_buildings.geojson"
    )
    insert_parking_areas(
        f"{DATA_DIR}/geojson/transport/cork_parking_areas.geojson"
    )

    insert_rooms(
        f"{DATA_DIR}/geojson/venues/cork_main_building_floor_0.geojson"
    )
    insert_rooms(
        f"{DATA_DIR}/geojson/venues/cork_main_building_floor_1.geojson"
    )


def cli():
    parser = argparse.ArgumentParser(
        prog="geocore",
        description="Geocore management CLI",
    )

    parser.add_argument(
        "--seed",
        action="store_true",
        help="Seed geospatial data into the database",
    )

    args = parser.parse_args()

    if args.seed:
        seed()
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
