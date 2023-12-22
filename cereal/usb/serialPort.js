import io from 'socket.io-client';

export class SerialPort {
    constructor(port, baudrate = 115200, endline = '\n', dataCallback = null) {
        this.enabled = false;
        this.port = port;
        this.baudrate = baudrate;
        this.endline = endline;
        this.enabledTimeStamps = false;
        this.socket = null;
        this.dataCallback = dataCallback;

    }

    destroy() {
        this.enabled = false;
        this.port = null;
        this.baudrate = null;
        this.endline = null;
        this.enabledTimeStamps = false;
        this.socket = null;
        this.dataCallback = null;
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

    setCallbackForReceivedData(callback) {
        this.dataCallback = callback;
    }

    async serialConnect() {
        this.enabled = true;
        try {
            const response = await fetch('http://localhost:5000/usb/usb_conf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: this.getSeralPortConfigJSON(),
            });
            const data = await response.json();
            console.log('Success:', data);
        } catch (error) {
            console.error('Error in Serial Connect:', error);
            this.enabled = false;
        }
    }

    async serialDisconnect() {
        this.enabled = false;
        /* TODO disconnect from socket */
        try {
            const response = await fetch('http://localhost:5000/usb/usb_conf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: this.getSeralPortConfigJSON(),
            });
            const data = await response.json();
            console.log('Success:', data);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    connectSerialPipe() {
        if (this.socket) {
            return;
        }
        this.socket = io.connect('ws://localhost:5000');
        this.socket.on('usb_data', this.#onSerialPipeReceivedData.bind(this));
    }

    #onSerialPipeReceivedData(data) {
        if (this.dataCallback && this.socket && this.enabled) {
            this.dataCallback(data.data);
        } else {
            console.log("Data received through Serial Pipe:", data.data);
        }
    }

    sendData(data) {
        if (this.enabled && this.socket) {
            this.#sendDataThroughSerialPipe(data);
        } else {
            console.log("Serial port is not enabled");
        }
    }

    #sendDataThroughSerialPipe(data) {
        this.socket.emit('usb_data', { data: data });
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
