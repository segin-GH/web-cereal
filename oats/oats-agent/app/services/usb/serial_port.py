import serial
import time
import kthread
from app import socketio


class SerialPort:
    def __init__(self, port, baudrate=115200, endline='\n'):
        self.enabled = False
        self.port = port
        self.baudrate = baudrate
        self.endline = endline
        self.enabled_timestamp = False
        self.read_thread = None

    def __del__(self):
        self.enabled = False
        if self.read_thread.is_alive() and self.read_thread is not None:
            self.read_thread.kill()
        # Add code to close the serial port

    def update_conf(self, port, baudrate=115200, endline='\n'):
        self.port = port
        self.baudrate = baudrate
        self.endline = endline

    def set_port(self, new_port):
        self.port = new_port

    def set_baudrate(self, new_baudrate):
        self.baudrate = new_baudrate

    def set_endline(self, new_endline):
        self.endline = new_endline

    def write_data(self, data):
        pass

    def turn_on(self):
        self.enabled = True
        # Create and start a thread for reading data
        self.read_thread = kthread.KThread(
            target=self.read_data,)
        self.read_thread.start()

    def turn_off(self):
        self.enabled = False
        # Kill the thread
        if self.read_thread.is_alive() and self.read_thread is not None:
            self.read_thread.kill()

    def read_data(self):
        while self.enabled:
            reading = time.time()
            time.sleep(0.1)
            socketio.emit('usb_data', {'data': reading})

    def get_conf_json(self):
        return {
            "port": self.port,
            "baudrate": self.baudrate,
            "endline": self.endline,
            "enabled": self.enabled,
        }


def get_available_ports():

    data = {
        "ports": [
            {"port": "/dev/ttyUSB0", "baudrate": 115200},
            {"port": "/dev/ttyUSB1", "baudrate": 115200},
            {"port": "/dev/ttyUSB3", "baudrate": 115200},
        ]
    }

    return data
