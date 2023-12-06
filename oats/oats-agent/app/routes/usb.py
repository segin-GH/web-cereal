# app/routes/usb.py
from flask import Blueprint, jsonify, request

bp = Blueprint('usb', __name__, url_prefix='/usb')


@bp.route('/port', methods=['GET'])
def get_data():
    # Data for serial port
    data = {
        "ports": [
            {"port": "/dev/ttyUSB0", "baudrate": 115200},
            {"port": "/dev/ttyUSB1", "baudrate": 115200},
            {"port": "/dev/ttyUSB2", "baudrate": 115200},
        ]
    }
    return jsonify(data)


@bp.route('/conf', methods=['POST'])
def usb_conf():
    # Get JSON data sent from the client
    request_data = request.get_json()

    # You can process the data here based on your needs
    # For example, you might want to check 'action' field and perform corresponding actions
    action = request_data.get('action', '')
    data = request_data.get('data', {})

    # Add your logic here to handle 'connect' and 'disconnect' actions
    if action == 'connect':
        # Handle connect action
        print(data)
        pass  # Replace with your code
    elif action == 'disconnect':
        # Handle disconnect action
        print(data)
        pass  # Replace with your code

    # Respond back to the client
    response = {"status": "success", "message": f"Action '{action}' processed"}
    return jsonify(response)
