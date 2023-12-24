import app.services.usb.serial_port as sp
from app.utils.logger_conf import setup_logger

logger = setup_logger(__name__)


class OatsUSB:
    def __init__(self):
        self.oats_usb_dict = {}
        logger.debug("OatsUSB instance.")

    def get_port(self):
        ports = sp.get_available_ports()
        logger.info(f"Available ports: {ports}")
        return ports

    def process_req(self, conf):
        conf_id = conf['id']
        logger.info(f"Processing request for id: {conf_id}")
        if conf_id not in self.oats_usb_dict:
            logger.info(f"Creating new SerialPort instance for id: {conf_id}")
            self.oats_usb_dict[conf_id] = sp.SerialPort(
                conf['port'], conf['baudrate'], conf['endline'])
        else:
            logger.info(
                f"Updating existing SerialPort instance for id: {conf_id}")
            self.oats_usb_dict[conf_id].update_conf(
                conf['port'], conf['baudrate'], conf['endline'])

        if conf['enabled']:
            logger.info(f"Enabling SerialPort for id: {conf_id}")
            self.oats_usb_dict[conf_id].turn_on()
        else:
            logger.info(f"Disabling SerialPort for id: {conf_id}")
            self.oats_usb_dict[conf_id].turn_off()

        conf_json = self.oats_usb_dict[conf_id].get_conf_json()
        logger.debug(f"Configuration for id {conf_id}:\n {conf_json}")
        return conf_json

    def send_data(self, data):
        if 'tab1' in self.oats_usb_dict:
            self.oats_usb_dict['tab1'].write_data(data)
        else:
            logger.warning(
                "Attempted to send data to serial, but 'tab1' is not in oats_usb_dict")


oats_usb = OatsUSB()
