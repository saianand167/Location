# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from core_logic import verify_location # Import your core logic function

app = Flask(__name__)
# CORS is needed to allow a web browser (frontend) to send requests to your backend
CORS(app)

@app.route('/verify-attendance', methods=['POST'])
def handle_verify_attendance():
    """
    This is the API endpoint that the frontend application will call.
    It expects a JSON payload with 'class_id', 'latitude', and 'longitude'.
    """
    # 1. Get the data from the incoming request
    data = request.json
    class_id = data.get('class_id')
    user_lat = data.get('latitude')
    user_lon = data.get('longitude')

    # 2. Basic validation: ensure all required data is present
    if not all([class_id, user_lat, user_lon]):
        return jsonify({"status": "error", "message": "Missing class_id, latitude, or longitude."}), 400

    try:
        # 3. Call your core logic function to do the work
        is_in_range, distance, class_info = verify_location(class_id, user_lat, user_lon)

        # 4. Based on the result, build a response to send back to the user
        if is_in_range:
            # THIS IS WHERE YOU WILL LATER ADD THE FACE RECOGNITION STEP
            print(f"SUCCESS: User is within range for class '{class_id}'. Distance: {distance:.2f}m.")
            return jsonify({
                "status": "success",
                "message": f"Location verified. You are {distance:.2f} meters from the class.",
                "action": "proceed_with_face_scan"
            })
        else:
            print(f"FAILURE: User is NOT within range for class '{class_id}'. Distance: {distance:.2f}m.")
            return jsonify({
                "status": "failure",
                "message": f"Attendance denied. You are {distance:.2f} meters away from the class location.",
                 "action": "show_error_on_screen"
            })

    except ValueError as e:
        # This handles cases where the class_id does not exist
        return jsonify({"status": "error", "message": str(e)}), 404

# This makes the server run when you execute the script
if __name__ == '__main__':
    # host='0.0.0.0' makes it accessible from other devices on the same network
    app.run(host='0.0.0.0', port=5000, debug=True)