from flask import Blueprint, jsonify, request
from app.services.usb.oats_usb import oats_usb
from app.utils.logger_conf import setup_logger
import json

logger = setup_logger(__name__)

bp = Blueprint('usb', __name__, url_prefix='/usb')


@bp.route('/usb_port', methods=['GET'])
def get_data():
    try:
        ports = oats_usb.get_port_data_for_client()
        return jsonify({'ports': ports})

    except Exception as e:
        logger.error(f'Error getting USB port data: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/usb_connect', methods=['POST'])
def usb_connect():
    try:
        request_data = request.get_json()
        logger.info(f'Received configuration request: {request_data}')
        data, uuid = oats_usb.process_connect_request(request_data)
        return jsonify({'data': data, 'uuid': uuid})
    except Exception as e:
        logger.error(f'Error processing USB configuration: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/usb_disconnect', methods=['POST'])
def usb_disconnect():
    try:
        request_data = request.get_json()
        logger.info(f'Received configuration request: {request_data}')
        data, uuid = oats_usb.process_disconnect_request(request_data)
        return jsonify({'data': data, 'uuid': uuid})
    except Exception as e:
        logger.error(f'Error processing USB configuration: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/user-departure', methods=['POST'])
def user_departure():
    data_bytes = request.get_data()
    if not data_bytes:
        return jsonify({"error": "No data received"}), 400

    try:
        request_data = json.loads(data_bytes.decode('utf-8'))
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON data"}), 400

    try:
        response_data, conf_id = oats_usb.process_disconnect_request(
            request_data)
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
