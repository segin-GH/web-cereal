# TODO: get number of ports from the system and send it to the client

import kthread
import time
from app import socketio
from flask import Blueprint, jsonify, request
from app.services.usb.oats_usb import oats_usb

bp = Blueprint('usb', __name__, url_prefix='/usb')


@socketio.on('usb_data')
def handle_message(message):
    oats_usb.send_data(message)


@bp.route('/usb_port', methods=['GET'])
def get_data():
    data = oats_usb.get_port()
    return jsonify(data)


@bp.route('/usb_conf', methods=['POST'])
def usb_conf():
    data = oats_usb.process_req(request.get_json())
    return jsonify(data)
