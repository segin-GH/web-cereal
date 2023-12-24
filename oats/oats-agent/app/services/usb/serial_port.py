import serial.tools.list_ports
import serial
import time
import kthread
from app import socketio
from app.utils.logger_conf import setup_logger

logger = setup_logger(__name__)


class SerialPort:
    def __init__(self, port, baudrate=115200, endline='\n'):
        self.enabled = False
        self.port = port
        self.baudrate = baudrate
        self.endline = endline
        self.enabled_timestamp = False
        self.read_thread = None
        self.serial_conn = None
        logger.info(
            f"SerialPort initialized with port: {port}, baudrate: {baudrate}")

    def __del__(self):
        self.enabled = False
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.kill()
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        logger.info("SerialPort instance deleted")

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
        if self.serial_conn and self.serial_conn.is_open:
            data = str(data)
            try:
                self.serial_conn.write(data.encode())
            except serial.SerialException as e:
                logger.error(f"Serial exception during write: {e}")
            except Exception as e:
                logger.error(f"Unexpected error during write: {e}")

    def turn_on(self):
        # TODO handle the case when the port is not available
        self.serial_conn = serial.Serial(self.port, self.baudrate)
        self.enabled = True
        self.read_thread = kthread.KThread(
            target=self.read_data,)
        self.read_thread.start()

    def turn_off(self):
        self.enabled = False
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.join()
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()

    def close_serial(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()

    def read_data(self):
        while self.enabled:
            try:
                while self.serial_conn.in_waiting > 0:
                    reading = self.serial_conn.readline().decode().strip()
                    socketio.emit('usb_data', {'data': reading})
            except serial.SerialTimeoutException:
                logger.warning("Timeout occurred during read operation.")
            except serial.SerialException as e:
                logger.error(f"Serial exception during read: {e}")
                self.enabled = False
                self.close_serial()
            except UnicodeDecodeError:
                logger.warning(
                    "Decoding error occurred. Invalid byte sequence received.")
            except IOError as e:
                if e.errno == 5:
                    logger.error(
                        "I/O Error: Device might have been disconnected.")
                    socketio.emit('disconnect_request', {'data': 'disconnect'})
                    self.enabled = False
                    self.close_serial()
                else:
                    logger.error(f"IOError during read: {e}")
            except Exception as e:
                logger.error(f"Unexpected error during read: {e}")
                self.enabled = False
                self.close_serial()
            time.sleep(0.1)

    def get_conf_json(self):
        return {
            "port": self.port,
            "baudrate": self.baudrate,
            "endline": self.endline,
            "enabled": self.enabled,
        }


def get_available_ports():
    # List all available serial ports
    ports = serial.tools.list_ports.comports()

    # Check if there are any available ports
    if not ports:
        return {"ports": None}

    # Format the ports information to only include the port names
    data = {"ports": [{"port": port.device} for port in ports]}

    return data
