import socketio
import serial.tools.list_ports
import serial
import time
import kthread
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
        self.com_port = None
        self.socket_wrap = None
        logger.info(
            f"SerialPort initialized with port: {port}, baudrate: {baudrate}")

    def __del__(self):
        self.enabled = False
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.kill()
        if self.com_port and self.com_port.is_open:
            self.com_port.close()
        if self.socket_wrap:
            self.socket_wrap.turn_off()
        logger.info("SerialPort instance deleted")

    def destroy(self):
        self.enabled = False
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.kill()
        if self.com_port and self.com_port.is_open:
            self.com_port.close()
        if self.socket_wrap:
            self.socket_wrap.turn_off()
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
        if self.com_port and self.com_port.is_open:
            data = str(data)
            try:
                self.com_port.write(data.encode())
            except serial.SerialException as e:
                logger.error(f"Serial exception during write: {e}")
            except Exception as e:
                logger.error(f"Unexpected error during write: {e}")

    def turn_on(self):
        if self.com_port and self.com_port.is_open:
            logger.warning("Serial port is already open.")
            self.com_port.close()

        try:
            self.com_port = serial.Serial(self.port, self.baudrate)
            self.enabled = True
        except serial.SerialException as e:
            logger.error(f"Failed to open serial port: {e}")
            self.enabled = False
            return

        # Now this check will not raise an AttributeError
        if not self.read_thread or not self.read_thread.is_alive():
            self.read_thread = kthread.KThread(target=self.read_data)
            self.read_thread.start()
            logger.info("Started the read thread.")
        else:
            logger.info("Read thread is already running.")

    def turn_off(self):
        self.enabled = False
        if self.read_thread and self.read_thread.is_alive():
            self.read_thread.join()
        if self.com_port and self.com_port.is_open:
            self.com_port.close()

    def close_serial(self):
        if self.com_port and self.com_port.is_open:
            self.com_port.close()

    def read_data(self):
        while self.enabled and self.com_port and self.com_port.is_open:
            try:
                while self.com_port.in_waiting > 0:
                    # TODO not able to exit gracefully when the device is disconnected
                    reading = self.com_port.readline().decode().strip()
                    self.socket_wrap.emit_data({'data': reading})
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
                    # TODO: socket wrap for disconnect
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


class PortManager:
    def __init__(self):
        self.used_ports = set()

    def get_ports(self):
        """
        List all available serial ports that are not in use (according to the internal record) and return them in a dictionary.
        If no available ports are found, return None.
        """
        ports = serial.tools.list_ports.comports()
        available_ports = [
            {"port": port.device} for port in ports if port.device not in self.used_ports
        ]
        return {"ports": available_ports} if available_ports else {"ports": None}

    def mark_port_as_used(self, port):
        """
        Mark the given port as used.
        """
        if port not in self.used_ports:
            self.used_ports.add(port)
        else:
            logger.warning(f"Attempted to use an already used port: {port}")

    def mark_port_as_unused(self, port):
        """
        Mark the given port as unused.
        """
        if port in self.used_ports:
            self.used_ports.remove(port)
        else:
            # Consider logging this as a warning or informational message
            logger.warning(f"Attempted to free an unused port: {port}")
