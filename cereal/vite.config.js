import { resolve } from 'path';
import { defineConfig } from 'vite';

export default defineConfig({
    build: {
        rollupOptions: {
            input: {
                main: resolve(__dirname, 'index.html'),
                usb: resolve(__dirname, 'usb/usb.html'),
                wifi: resolve(__dirname, 'wifi/wifi.html'),
                ble: resolve(__dirname, 'ble/ble.html'),
                mqtt: resolve(__dirname, 'mqtt/mqtt.html')
            }
        }
    }
});
