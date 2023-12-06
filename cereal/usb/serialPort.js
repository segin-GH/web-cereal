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

    async serialConnect() {
        this.enabled = true;
        let json = this.getSeralPortConfigJSON();
        console.log(json);

        try {
            // Send POST request to localhost with action type
            const response = await fetch('http://localhost:5000/usb/conf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action: 'connect', data: json }),
            });
            const data = await response.json();
            console.log('Success:', data);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async serialDisconnect() {
        this.enabled = false;
        let json = this.getSeralPortConfigJSON();
        console.log(json);

        try {
            // Send POST request to localhost with action type
            const response = await fetch('http://localhost:5000/usb/conf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action: 'disconnect', data: json }),
            });
            const data = await response.json();
            console.log('Success:', data);
        } catch (error) {
            console.error('Error:', error);
        }
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
