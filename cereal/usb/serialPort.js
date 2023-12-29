import io from 'socket.io-client';


export class SerialPort {
    constructor(port, baudrate = 115200, endline = '\n', dataCallback = null, id = null) {
        this.enabled = false;
        this.port = port;
        this.baudrate = baudrate;
        this.endline = endline;
        this.enabledTimeStamps = false;
        this.socket = null;
        this.dataCallback = dataCallback;
        this.id = id; // id for the tab, only required for multiple tabs
        this.socketType = null;

    }

    destroy() {
        this.enabled = false;
        this.port = null;
        this.baudrate = null;
        this.endline = null;
        this.enabledTimeStamps = false;
        this.socket = null;
        this.dataCallback = null;
        this.id = null;
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

    setID(id) {
        this.id = id;
    }

    unsetID() {
        this.id = null;
    }

    getID() {
        return this.id;
    }

    async serialConnect() {
        this.enabled = true;
        try {
            const response = await fetch(`${import.meta.env.VITE_FETCH_BASE_URL}/usb/usb_connect`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: this.getSerialPortConfigJSON(),
            });
            const recvData = await response.json();
            console.log('Success:', recvData);
            alert('Connected to ' + recvData.data.port);
            console.log('ID:', recvData.uuid);
            this.id = recvData.uuid;
            this.updateSerialPortConfig(recvData.data);
            this.connectSerialPipe();
        } catch (error) {
            console.error('Error in Serial Connect:', error);
            this.enabled = false;
        }
    }

    async serialDisconnect() {
        if (this.getID() < 0) {
            console.error('No device id set for disconnect');
            return;
        }
        this.enabled = false;
        try {
            console.log('Disconnecting from ' + this.port + ' with id ' + this.id);
            const response = await fetch(`${import.meta.env.VITE_FETCH_BASE_URL}/usb/usb_disconnect`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: this.getSerialPortConfigJSON(),
            });
            const recvData = await response.json();
            alert('Disconnected from ' + recvData.data.port);
            console.log('Success:', recvData);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    connectSerialPipe() {
        if (this.socket) {
            return;
        }

        this.socket = io(`${import.meta.env.VITE_FETCH_BASE_URL}`, {
            withCredentials: true,
            extraHeaders: {
                "my-custom-header": "abcd"
            }
        });
        this.socketType = 'tab_' + this.id;
        console.log('Connecting to ' + this.socketType);
        this.socket.on(this.socketType, this.#onSerialPipeReceivedData.bind(this));
        this.socket.on('disconnect_request', this.#onSerialPipeDisconnectRequest.bind(this));
    }

    #onSerialPipeReceivedData(data) {
        if (this.dataCallback && this.socket && this.enabled) {
            this.dataCallback(data.data);
        } else {
            console.log("Data received through Serial Pipe:", data.data);
        }
    }

    #onSerialPipeDisconnectRequest() {
        this.enabled = false;
        alert("Lost Device " + this.port);
        this.socket.disconnect();
        this.socket = null;
        sendUserDeparture();
    }

    sendUserDeparture() {
        const data = JSON.stringify({ id: this.socketType });
        navigator.sendBeacon(`${import.meta.env.VITE_FETCH_BASE_URL}/usb/user-departure`, data);
    }

    sendData(data) {
        if (this.enabled && this.socket) {
            this.#sendDataThroughSerialPipe(data);
        } else {
            console.log("Serial port is not enabled");
        }
    }

    #sendDataThroughSerialPipe(data) {
        this.socket.emit(this.socketType, { data: data });
    }


    getSerialPortConfigJSON() {
        return JSON.stringify({
            id: this.id,
            enabled: this.enabled,
            port: this.port,
            baudrate: this.baudrate,
            endline: this.endline,
            enabledTimeStamps: this.enabledTimeStamps,
        });
    }

    updateSerialPortConfig(configData) {
        this.port = configData.port;
        this.baudrate = configData.baudrate;
        this.endline = configData.endline;
    }
}
