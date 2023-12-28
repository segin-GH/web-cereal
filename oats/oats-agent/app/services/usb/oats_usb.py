from app import socketio
import app.services.usb.serial_port as sp
from app.utils.logger_conf import setup_logger
from app.utils.socket_wrap import SocketWrap as sw

logger = setup_logger(__name__)


class OatsUSB:
    def __init__(self):
        self.oats_usb_dict = {}
        self.oats_uid = 0
        logger.debug("OatsUSB instance.")

    def oats_get_uuid(self):
        self.oats_uid += 1
        return str(self.oats_uid)

    def get_port_data_for_client(self):
        ports = sp.get_available_ports()
        logger.info(f"Available ports: {ports}")
        return ports

    def process_connect_request(self, request):
        conf_id = request['id']
        if (conf_id == None):
            conf_id = self.oats_get_uuid()

        logger.info(f"Processing connect request for id: {conf_id}")
        if conf_id not in self.oats_usb_dict:
            # Create a new SerialPort instance and assign a socket wrap
            self.oats_usb_dict[conf_id] = sp.SerialPort(
                request['port'], request['baudrate'], request['endline'])
            logger.info(f"Created new SerialPort for id: {conf_id}")
            self.oats_usb_dict[conf_id].socket_wrap = sw(
                socketio, (f"tab_{conf_id}"))
            self.oats_usb_dict[conf_id].socket_wrap.on_event(
                self.oats_usb_dict[conf_id].write_data)
        else:
            self.oats_usb_dict[conf_id].update_conf(
                request['port'], request['baudrate'], request['endline'])
            logger.info(f"Updated SerialPort for id: {conf_id}")

        self.oats_usb_dict[conf_id].turn_on()
        logger.info(f"Enabled SerialPort for id: {conf_id}")
        return self.oats_usb_dict[conf_id].get_conf_json(), conf_id

    def process_disconnect_request(self, request_data):
        try:
            conf_id = request_data['id']
            conf_id = conf_id[4:]
        except KeyError:
            logger.error("Request data does not contain 'id'")
            raise ValueError("Invalid request data: 'id' not found")

        if conf_id not in self.oats_usb_dict:
            logger.warning(f"ID {conf_id} not found in oats_usb_dict")
            raise KeyError(f"ID {conf_id} not found")

        usb_device = self.oats_usb_dict[conf_id]
        usb_device.turn_off()

        del self.oats_usb_dict[conf_id]

        logger.info(f"Disabled SerialPort for id: {conf_id}")
        return usb_device.get_conf_json(), conf_id


oats_usb = OatsUSB()
