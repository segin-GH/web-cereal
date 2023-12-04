import serial
import time


class SerialPort:
    def __init__(self, port, baudrate, endline='\n'):
        self.enabled = False
        self.port = port
        self.baudrate = baudrate
        self.endline = endline
        self.enabled_timestamp = False

    def change_baudrate(self, new_baudrate):
        self.baudrate = new_baudrate
        # Add code to reconfigure the actual serial port

    def set_endline(self, new_endline):
        self.endline = new_endline
        # Add code to handle endline character in serial communication
