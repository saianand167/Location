# core_logic.py

from haversine import haversine, Unit

# In a real application, you would get this data from a database.
# For now, we will use a Python dictionary as a placeholder.
CLASS_LOCATIONS = {
    "CS101": {
        "name": "Computer Science Building, Room 101",
        "lat": 16.791913,
        "lon": 80.822386
    },
    "PHY203": {
        "name": "Physics Hall, Room 203",
        "lat": 40.712776,
        "lon": -74.005974 # A location in a different city for testing
    }
}

DEFAULT_RADIUS_METERS = 100 # The attendance radius is 100 meters

def verify_location(class_id: str, user_lat: float, user_lon: float) -> (bool, float, dict):
    """
    Verifies if a user's location is within a specified radius of a class location.

    Args:
        class_id (str): The identifier for the class (e.g., "CS101").
        user_lat (float): The latitude of the user's device.
        user_lon (float): The longitude of the user's device.

    Returns:
        tuple: A tuple containing:
            - bool: True if the user is within the radius, False otherwise.
            - float: The calculated distance in meters.
            - dict: The details of the class location.
    """
    class_info = CLASS_LOCATIONS.get(class_id)

    # Check if the class_id is valid
    if not class_info:
        raise ValueError(f"Class ID '{class_id}' not found.")

    class_location = (class_info["lat"], class_info["lon"])
    user_location = (user_lat, user_lon)

    # Calculate the distance between the two points in meters
    distance = haversine(class_location, user_location, unit=Unit.METERS)

    is_in_range = distance <= DEFAULT_RADIUS_METERS

    return is_in_range, distance, class_info

# This part allows you to test the file directly
if __name__ == "__main__":
    # --- TEST CASE 1: User is INSIDE the allowed range ---
    print("--- Testing Scenario 1: User is inside range ---")
    in_range, dist, info = verify_location("CS101", user_lat=17.41292, user_lon=78.44004)
    print(f"Class: {info['name']}")
    print(f"Distance from class: {dist:.2f} meters.")
    print(f"Is user within {DEFAULT_RADIUS_METERS}m radius? {'Yes' if in_range else 'No'}")
    print("-" * 20)

    # --- TEST CASE 2: User is OUTSIDE the allowed range ---
    print("--- Testing Scenario 2: User is outside range ---")
    in_range, dist, info = verify_location("CS101", user_lat=34.055120, user_lon=-118.247510)
    print(f"Class: {info['name']}")
    print(f"Distance from class: {dist:.2f} meters.")
    print(f"Is user within {DEFAULT_RADIUS_METERS}m radius? {'Yes' if in_range else 'No'}")
    print("-" * 20)