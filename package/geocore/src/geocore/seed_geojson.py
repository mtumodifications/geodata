import json

from pathlib import Path
from shapely.geometry import shape
from geoalchemy2.shape import from_shape
from sqlalchemy import func, select

from .database import engine, SessionLocal
from .models.campus_location import Base, CampusLocation
from .models.campus_building import CampusBuilding
from .models.parking_area import ParkingArea
from .models.venue import Venue


def insert_campus_locations(filepath: str):
    # Create the table if it doesn't exist
    Base.metadata.create_all(engine)

    # Read GeoJSON
    with open(filepath, "r", encoding="utf-8") as file:
        geojson = json.load(file)

    campus_name = geojson["campus"]
    campus_address = geojson["address"]

    with SessionLocal() as session:
        for feature in geojson["features"]:

            # Convert GeoJSON geometry to Shapely geometry
            shapely_geom = shape(feature["geometry"])

            # Convert Shapely geometry to GeoAlchemy geometry
            db_geom = from_shape(
                shapely_geom,
                srid=4326,
            )

            campus = CampusLocation(
                name=campus_name,
                address=campus_address,
                geom=db_geom,
            )

            session.add(campus)

        session.commit()


def insert_campus_buildings(filepath: str):
    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Read GeoJSON
    with open(filepath, "r", encoding="utf-8") as file:
        geojson = json.load(file)

    campus_name = geojson["campus"]

    with SessionLocal() as session:

        # Find the campus ID using its name
        campus = (
            session.query(CampusLocation)
            .filter(CampusLocation.name == campus_name)
            .first()
        )

        if campus is None:
            raise ValueError(
                f"Campus '{campus_name}' does not exist "
                "in campus_locations."
            )

        print(f"Importing buildings for: {campus.name}")

        imported_count = 0

        for feature in geojson["features"]:

            properties = feature["properties"]

            # Convert GeoJSON geometry to Shapely
            shapely_geom = shape(feature["geometry"])

            # Convert Shapely geometry to GeoAlchemy
            db_geom = from_shape(
                shapely_geom,
                srid=4326,
            )

            building = CampusBuilding(
                fid=properties.get("fid"),
                campus_id=campus.id,
                building_name=properties["Building_Name"],
                building_section=properties.get("Section_Name"),
                description=properties.get("Description"),
                floors=properties.get("Floors"),
                venue_count=properties.get("Venue_Count"),
                geom=db_geom,
            )

            session.add(building)
            imported_count += 1

        session.commit()

        print(
            f"Successfully imported {imported_count} "
            f"buildings for {campus.name}."
        )


def insert_parking_areas(filepath: str):
    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Read GeoJSON
    with open(filepath, "r", encoding="utf-8") as file:
        geojson = json.load(file)

    campus_name = geojson["campus"]

    with SessionLocal() as session:

        # Find the campus ID using its name
        campus = (
            session.query(CampusLocation)
            .filter(CampusLocation.name == campus_name)
            .first()
        )

        if campus is None:
            raise ValueError(
                f"Campus '{campus_name}' does not exist "
                "in campus_locations."
            )

        print(f"Importing parking areas for: {campus.name}")

        imported_count = 0

        for feature in geojson["features"]:

            properties = feature["properties"]

            # Convert GeoJSON geometry to Shapely
            shapely_geom = shape(feature["geometry"])

            # Convert Shapely geometry to GeoAlchemy
            db_geom = from_shape(
                shapely_geom,
                srid=4326,
            )

            parking_area = ParkingArea(
                fid=properties.get("fid"),
                campus_id=campus.id,
                label=properties["Parking_Name"],
                full_capacity=properties.get("Full_Capacity"),
                disabled_capacity=properties.get("Disabled_Capacity"),
                fee=properties.get("Fee"),
                fee_type=properties.get("Fee_Type"),
                is_paid=properties.get("Is_Paid"),
                is_reserved=properties.get("Is_Reserved"),
                is_disability_friendly=properties.get(
                    "Is_Disability_Friendly"),
                for_visitors=properties.get("For_Visitors"),
                has_barriers=properties.get("Has_Barrier"),
                geom=db_geom,
            )

            session.add(parking_area)
            imported_count += 1

        session.commit()

        print(
            f"Successfully imported {imported_count} "
            f"parking areas for {campus.name}."
        )


def insert_all_parking_areas(directory: str):
    files = Path(directory).glob("*_parking_areas.geojson")

    for filepath in files:
        print(f"\nProcessing: {filepath.name}")

        insert_parking_areas(str(filepath))


def insert_venues(filepath: str):
    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Read GeoJSON
    with open(filepath, "r", encoding="utf-8") as file:
        geojson = json.load(file)

    campus_name = geojson["campus"]
    building_name = geojson["building"]

    with SessionLocal() as session:

        # Find the campus
        campus = session.scalar(
            select(CampusLocation).where(
                CampusLocation.name == campus_name
            )
        )

        if campus is None:
            raise ValueError(f"Campus not found: {campus_name}")

        # Keep track of all buildings affected by this import
        affected_buildings = {}

        for feature in geojson["features"]:

            properties = feature["properties"]

            # Determine the building section
            block = properties.get("Block")
            section = properties.get("Section")

            if block is None and section is None:
                continue

            if block is not None:
                section_name = f"{block} Block"
            else:
                section_name = section

            # Find the corresponding building
            query = select(CampusBuilding).where(
                CampusBuilding.campus_id == campus.id,
                CampusBuilding.building_name == building_name,
                CampusBuilding.building_section == section_name,
            )

            building = session.scalar(query)

            if building is None:
                raise ValueError(
                    f"Could not find building '{building_name}' "
                    f"with section '{section_name}' "
                    f"in campus '{campus_name}'"
                )

            # Track this building
            affected_buildings[building.id] = building

            # Convert GeoJSON geometry
            shapely_geom = shape(feature["geometry"])

            # Convert to GeoAlchemy geometry
            db_geom = from_shape(
                shapely_geom,
                srid=4326,
            )

            fid = properties.get("fid")

            # Find existing venue
            venue = None

            if fid is not None:
                venue = session.scalar(
                    select(Venue).where(
                        Venue.building_id == building.id,
                        Venue.fid == fid,
                    )
                )

            # Create venue if it doesn't exist
            if venue is None:
                venue = Venue(
                    building_id=building.id,
                    fid=fid,
                )
                session.add(venue)

            # Populate/update venue properties
            venue.room_number = properties.get("Room_Number")

            venue.primary_function = properties.get(
                "Room_Primary_Function"
            )

            venue.description = properties.get("Description")

            venue.level = properties.get("Floor")

            venue.geom = db_geom

        # Flush pending inserts and updates before counting
        session.flush()

        # Recalculate mapped venues for every affected building
        for building in affected_buildings.values():

            mapped_venues = session.scalar(
                select(func.count(Venue.id)).where(
                    Venue.building_id == building.id
                )
            )

            building.mapped_venues = mapped_venues

            print(
                f"{building.building_name} - "
                f"{building.building_section}: "
                f"{mapped_venues} mapped venues"
            )

        session.commit()

        print(
            f"Successfully imported venues for {building_name}"
        )


def insert_all_campus_buildings(directory: str):
    files = Path(directory).glob("*_buildings.geojson")

    for filepath in files:
        print(f"\nProcessing: {filepath.name}")

        insert_campus_buildings(str(filepath))
