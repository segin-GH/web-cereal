// vite.config.js
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        usb: resolve(__dirname, 'usb/index.html'),
        ble: resolve(__dirname, 'ble/index.html'),
        wifi: resolve(__dirname, 'wifi/index.html'),
        mqtt: resolve(__dirname, 'mqtt/index.html'),
      },
    },
  },
})
