// SerialPort.js

export class SerialPort {
    constructor(port, baudrate = 115200, endline = '\n') {
        this.enabled = false;
        this.port = port;
        this.baudrate = baudrate;
        this.endline = endline;
        this.enabledTimeStamps = false;
    }

    changeBaudrate(newBaudrate) {
        this.baudrate = newBaudrate;
    }

    setEndline(newEndline) {
        this.endline = newEndline;
    }

    enableTimeStamps() {
        this.enabledTimeStamps = true;
    }

    disableTimeStamps() {
        this.enabledTimeStamps = false;
    }

    serialConnect() {
        this.enabled = true;
        let json = this.getSeralPortConfigJSON();
        console.log(json);
    }

    serialDisconnect() {
        this.enabled = false;
        let json = this.getSeralPortConfigJSON();
        console.log(json);
    }

    getSeralPortConfigJSON() {
        return JSON.stringify({
            enabled: this.enabled,
            port: this.port,
            baudrate: this.baudrate,
            endline: this.endline,
            enabledTimeStamps: this.enabledTimeStamps,
        });
    }

}
