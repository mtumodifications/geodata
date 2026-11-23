from sqlalchemy import DDL, event

from ..models.base import Base


create_get_building_rooms = DDL("""
CREATE OR REPLACE FUNCTION get_building_rooms(
    selected_floor INTEGER,
    selected_building_id VARCHAR(8)
)
RETURNS JSON
LANGUAGE SQL
STABLE
AS $$
    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', COALESCE(
            json_agg(
                json_build_object(
                    'type', 'Feature',
                    'id', r.id,
                    'properties', json_build_object(
                        'fid', r.fid,
                        'room_number', r.room_number,
                        'primary_function', r.primary_function,
                        'floor_level', r.level,
                        'building_id', r.building_id,
                        'building_name', b.building_name,
                        'building_section', b.building_section
                    ),
                    'geometry', ST_AsGeoJSON(r.geom)::json
                )
            ),
            '[]'::json
        )
    )
    FROM public.rooms r
    JOIN public.campus_buildings b
        ON b.id = r.building_id
    WHERE
        (selected_floor IS NULL OR r.level = selected_floor)
        AND r.building_id = selected_building_id;
$$;
""")

event.listen(
    Base.metadata,
    "after_create",
    create_get_building_rooms,
)
