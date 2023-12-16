# app/routes/usb.py
import kthread
from flask import Blueprint, jsonify, request
from app import socketio
import time

from flask import Blueprint, jsonify, request

bp = Blueprint('usb', __name__, url_prefix='/usb')

# ... other code ...

usb_read_thread = None


@socketio.on('usb_data')
def handle_usb_data(data):
    print(str(data))


def read_from_usb_port():
    while True:
        reading = time.time()
        time.sleep(0.1)
        socketio.emit('usb_data', {'data': reading})


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
    global usb_read_thread

    request_data = request.get_json()
    action = request_data.get('action', '')

    if action == 'connect':
        if usb_read_thread is None or not usb_read_thread.is_alive():
            usb_read_thread = kthread.KThread(target=read_from_usb_port)
            usb_read_thread.start()
        response = {"status": "success", "message": "USB Reading Started"}
    elif action == 'disconnect':
        if usb_read_thread is not None:
            usb_read_thread.terminate()
        response = {"status": "success", "message": "USB Reading Stopped"}
    else:
        response = {"status": "error", "message": f"Unknown action '{action}'"}

    return jsonify(response)
