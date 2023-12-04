// SerialPort.js

export class SerialPort {
    constructor(port, baudrate=115200, endline = '\n') {
        this.port = port;
        this.baudrate = baudrate;
        this.endline = endline;
        // Add other properties as needed
    }

    changeBaudrate(newBaudrate) {
        this.baudrate = newBaudrate;
        // Additional logic for changing baudrate
    }

    setEndline(newEndline) {
        this.endline = newEndline;
        // Additional logic for setting endline
    }

    // Add other methods as needed
}
