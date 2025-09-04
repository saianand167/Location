# core_logic.py

from haversine import haversine, Unit
from typing import Dict, Any, Tuple # For older Python versions if needed

# In a real application, you would get this data from a database.
CLASS_LOCATIONS: Dict[str, Dict[str, Any]] = {
    "CS101": {
        "name": "Computer Science Building, Room 101",
        "lat": 16.7953091,
        "lon": 80.8228997
    },
    "PHY203": {
        "name": "Physics Hall, Room 203",
        "lat": 40.712776,
        "lon": -74.005974
    }
}

DEFAULT_RADIUS_METERS: int = 10 # The attendance radius is 100 meters

def verify_location(class_id: str, user_lat: float, user_lon: float) -> tuple[bool, float, dict]:
    """
    Verifies if a user's location is within a specified radius of a class location.
    """
    class_info = CLASS_LOCATIONS.get(class_id)

    if not class_info:
        raise ValueError(f"Class ID '{class_id}' not found.")

    class_location = (class_info["lat"], class_info["lon"])
    user_location = (user_lat, user_lon)

    distance = haversine(class_location, user_location, unit=Unit.METERS)
    is_in_range = distance <= DEFAULT_RADIUS_METERS

    return is_in_range, distance, class_info