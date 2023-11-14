import serial
import serial.tools.list_ports
import json


class SerialPipe:
    def __init__(self):
        self.ser = None

    def get_ports_info(self):
        # Get a list of available serial ports
        ports = serial.tools.list_ports.comports()
        # Create a JSON object with the number of ports and their names
        ports_info = {
            "number_of_ports": len(ports),
            "port_names": [port.device for port in ports],
        }
        return json.dumps(ports_info, indent=4)  # Return the JSON object as a string


if __name__ == "__main__":
    sp = SerialPipe()
    print(sp.get_ports_info())
