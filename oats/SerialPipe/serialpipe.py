import serial
import time


class SerialPipe:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate)

    def send(self, data):
        self.ser.write(data.encode())
        self.ser.flush()  # Flush the buffer

    def receive(self, termination="/n"):
        data = self.ser.readline()
        return data.decode()


if __name__ == "__main__":
    port = "/dev/ttyUSB1"  # Change this to the correct port
    baudrate = 115200

    sp = SerialPipe(port, baudrate)

    try:
        while True:
            sp.send("Hello ESP32!")  # Send a message to ESP32
            time.sleep(1)  # Wait for a second
            data = sp.receive()
            if data:
                print(f"Received: {data}", end="")
    except KeyboardInterrupt:
        print("Program stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sp.ser.close()
