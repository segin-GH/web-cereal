from app import socketio
import app.services.usb.serial_port as sp
from app.utils.logger_conf import setup_logger
from app.utils.socket_wrap import SocketWrap as sw


logger = setup_logger(__name__)


class OatsUSB:
    def __init__(self):
        self.oats_usb_dict = {}
        self.oats_uid = 0
        self.port_manager = sp.PortManager()
        logger.debug("OatsUSB instance.")

    def oats_get_uuid(self):
        self.oats_uid += 1
        return str(self.oats_uid)

    def get_port_data_for_client(self):
        ports = self.port_manager.get_ports()
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
            self.port_manager.mark_port_as_used(request['port'])
            logger.info(f"Created new SerialPort for id: {conf_id}")
            self.oats_usb_dict[conf_id].socket_wrap = sw(
                socketio, (f"tab_{conf_id}"))
            self.oats_usb_dict[conf_id].socket_wrap.on_event(
                self.oats_usb_dict[conf_id].write_data)
        else:
            self.oats_usb_dict[conf_id].update_conf(
                request['port'], request['baudrate'], request['endline'])
            self.port_manager.mark_port_as_used(request['port'])
            logger.info(f"Updated SerialPort for id: {conf_id}")

        self.oats_usb_dict[conf_id].turn_on()
        logger.info(f"Enabled SerialPort for id: {conf_id}")
        return self.oats_usb_dict[conf_id].get_conf_json(), conf_id

    def process_disconnect_request(self, request):
        conf_id = request['id']
        if conf_id not in self.oats_usb_dict:
            logger.warning(f"ID {conf_id} not found in oats_usb_dict")
            return None, None

        logger.info(f"Processing disconnect request for id: {conf_id}")
        self.port_manager.mark_port_as_unused(
            self.oats_usb_dict[conf_id].port)
        self.oats_usb_dict[conf_id].turn_off()
        self.oats_usb_dict[conf_id].destroy()
        logger.info(f"Disabled SerialPort for id: {conf_id}")
        return self.oats_usb_dict[conf_id].get_conf_json(), conf_id

    def process_departure_request(self, request_data):
        try:
            conf_id = request_data['id']
            conf_id = conf_id[4:]
        except KeyError:
            logger.error("Request data does not contain 'id'")
            raise ValueError("Invalid request data: 'id' not found")

        if conf_id not in self.oats_usb_dict:
            logger.warning(f"ID {conf_id} not found in oats_usb_dict")
            raise KeyError(f"ID {conf_id} not found")

        self.port_manager.mark_port_as_unused(
            self.oats_usb_dict[conf_id].port)
        self.oats_usb_dict[conf_id].turn_off()
        del self.oats_usb_dict[conf_id]
        logger.info(f"Disabled SerialPort for id: {conf_id}")
        return {"status": "OK"}, conf_id


oats_usb = OatsUSB()
