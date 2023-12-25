import app.services.usb.serial_port as sp
from app.utils.logger_conf import setup_logger

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
        if conf_id == 'tab1':  # TODO"tab1", really? ever heard of meaningful names?
            conf_id = self.oats_get_uuid()

        logger.info(f"Processing connect request for id: {conf_id}")
        if conf_id not in self.oats_usb_dict:
            self.oats_usb_dict[conf_id] = sp.SerialPort(
                request['port'], request['baudrate'], request['endline'])
            logger.info(f"Created new SerialPort for id: {conf_id}")
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
            # Nice error handling
            raise ValueError(
                "Trying to disconnect a non-existent connection. Good job.")

        self.oats_usb_dict[conf_id].turn_off()
        logger.info(f"Disabled SerialPort for id: {conf_id}")
        return self.oats_usb_dict[conf_id].get_conf_json(), conf_id

    def send_data_to_serial(self, data, id="1"):
        if id in self.oats_usb_dict:
            self.oats_usb_dict[id].write_data(data)
        else:
            logger.warning(
                "Attempted to send data to serial, but 'tab1' is not in oats_usb_dict")


oats_usb = OatsUSB()
