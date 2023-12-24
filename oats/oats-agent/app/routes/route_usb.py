import logging
from app import socketio
from flask import Blueprint, jsonify, request
from app.services.usb.oats_usb import oats_usb

# Assuming logging is configured externally
logger = logging.getLogger(__name__)

bp = Blueprint('usb', __name__, url_prefix='/usb')


@socketio.on('usb_data')
def handle_message(message):
    logger.info(f'Received USB data: {message}')
    try:
        oats_usb.send_data_to_serial(message)
        logger.info('Data sent successfully')
    except Exception as e:
        logger.error(f'Error sending data: {e}', exc_info=True)


@bp.route('/usb_port', methods=['GET'])
def get_data():
    try:
        data = oats_usb.get_port_data_for_client()
        logger.info(f'USB port data: {data}')
        return jsonify(data)
    except Exception as e:
        logger.error(f'Error getting USB port data: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500


@bp.route('/usb_conf', methods=['POST'])
def usb_conf():
    try:
        request_data = request.get_json()
        logger.info(f'Received configuration request: {request_data}')
        data = oats_usb.process_req_from_client(request_data)
        return jsonify(data)
    except Exception as e:
        logger.error(f'Error processing USB configuration: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500
