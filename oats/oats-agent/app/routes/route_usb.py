from flask import Blueprint, jsonify, request
from app.services.usb.oats_usb import oats_usb
from app.utils.logger_conf import setup_logger

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
def handle_user_departure():
    try:
        # Extract the data sent from the client
        data = request.get_json()
        logger.info(f'Received user departure: ' + str(data))
        user_id = data['userId']

        logger.info(f'User with ID {user_id} is departing')
        # TODO: Handle user departure here clean up the data structures
        # TODO: clean serial port and the id from the oats_usb_dict
        return jsonify({'message': 'User departure handled successfully'})

    except Exception as e:
        logger.error(f'Error handling user departure: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500
