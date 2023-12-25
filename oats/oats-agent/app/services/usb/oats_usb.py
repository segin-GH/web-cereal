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
            self.oats_usb_dict[conf_id].socket_wrap = sw(socketio, 'usb_data')
            self.oats_usb_dict[conf_id].socket_wrap.on_event(
                self.oats_usb_dict[conf_id].write_data)
        else:
            self.oats_usb_dict[conf_id].update_conf(
                request['port'], request['baudrate'], request['endline'])
            logger.info(f"Updated SerialPort for id: {conf_id}")

        self.oats_usb_dict[conf_id].turn_on()
        logger.info(f"Enabled SerialPort for id: {conf_id}")
        return self.oats_usb_dict[conf_id].get_conf_json(), conf_id

    def process_disconnect_request(self, request):
        conf_id = request['id']
        if conf_id not in self.oats_usb_dict:
            return None, None

        self.oats_usb_dict[conf_id].turn_off()
        logger.info(f"Disabled SerialPort for id: {conf_id}")
        return self.oats_usb_dict[conf_id].get_conf_json(), conf_id


oats_usb = OatsUSB()
