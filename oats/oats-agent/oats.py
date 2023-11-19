from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route("/usb", methods=["GET"])
def get_data():
    # data for serial port
    data = {
        "ports": [
            {
                "port": "/dev/ttyUSB0",
                "baudrate": 115200,
            },
            {
                "port": "/dev/ttyUSB1",
                "baudrate": 115200,
            },
            {
                "port": "/dev/ttyUSB2",
                "baudrate": 115200,
            },
        ]
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
