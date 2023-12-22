import app.services.usb.serial_port as sp


class OatsUSB:
    def __init__(self):
        # a Dict to save the SerialInstance with tab id as key
        self.oats_usb_dict = {}

    def get_port(self):
        return sp.get_available_ports()

    def process_req(self, conf):
        conf_id = conf['id']
        if conf_id not in self.oats_usb_dict:
            # New SerialPort instance
            self.oats_usb_dict[conf_id] = sp.SerialPort(
                conf['port'], conf['baudrate'], conf['endline'])
        else:
            # Update existing SerialPort instance
            self.oats_usb_dict[conf_id].update_conf(
                conf['port'], conf['baudrate'], conf['endline'])

        # Handle enabling or disabling the serial port
        if conf['enabled']:
            self.oats_usb_dict[conf_id].turn_on()
        else:
            self.oats_usb_dict[conf_id].turn_off()

        return self.oats_usb_dict[conf_id].get_conf_json()


oats_usb = OatsUSB()
