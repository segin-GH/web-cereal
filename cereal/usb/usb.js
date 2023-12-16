/* TODO: the send button gets stuck if there is serial instance */
/* TODO: timestamp how will u update the config ?  */

import { attachDropdownListener } from '../utils.js';
import { SerialPort } from './serialPort.js';

let tabSerialPorts = {
    "tab1": null,
};

var socket = null;

// Function to attach event listeners to the USB tab
export function attachUsbEventListeners() {
    attachDropdownListener('dropdownUSBPort', 'dropdownUSB');
    attachDropdownListener('dropdownBaudRate', 'dropdownBaud');
    attachDropdownListener('dropdownLineEnding', 'dropdownLineEnd');
}

// Function to attach event listeners to the USB tab
export function attachUsbEventListenersButton() {
    const button = document.getElementById('dropdownUSBPort');
    button?.addEventListener('click', fetchPortData);

    const button2 = document.getElementById('dropdownBaudRate');
    button2?.addEventListener('click', updateBaudRate);

    const button3 = document.getElementById('dropdownLineEnding');
    button3?.addEventListener('click', updateLineEnding);

    const conButton = document.getElementById('connectButton');
    conButton?.addEventListener('click', handleConClick);

    const closeButton = document.getElementById('clearButton');
    closeButton?.addEventListener('click', handleCloseClick);

    setupInputHandlers();

}

// Function to fetch the list of available USB ports
function fetchPortData() {
    fetch('http://localhost:5000/usb/port')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => updateDropdownPort(data.ports))
        .catch(error => console.error('Error fetching data:', error));
}

// Function to update the USB port dropdown
function updateDropdownPort(ports) {
    const dropdown = document.querySelector('#dropdownUSB ul');
    dropdown.innerHTML = '';

    ports.forEach(port => {
        const listItem = document.createElement('li');
        listItem.className = 'block px-4 py-2 hover:bg-clr-prim hover:text-white';
        listItem.textContent = port.port;

        listItem.addEventListener('click', function () {
            document.getElementById('dropdownUSBPortText').textContent = port.port;

            // Check if a SerialPort instance already exists for tab1
            if (tabSerialPorts['tab1']) {
                // Update the existing instance's port
                tabSerialPorts['tab1'].port = port.port;
            } else {
                // Create a new SerialPort instance with default or existing baudrate and endline
                tabSerialPorts['tab1'] = new SerialPort(port.port);
            }
            console.log('Current state of tab1:', tabSerialPorts['tab1']);

        });

        dropdown.appendChild(listItem);
    });
}

// Function to update the baud rate dropdown
function updateBaudRate() {
    const baudRateDropdown = document.getElementById('dropdownBaud');
    baudRateDropdown.innerHTML = ''; // Clear existing options

    // Define your baud rate options
    const baudRates = [1200, 9600, 115200, 921600];

    baudRates.forEach(baudRate => {
        const listItem = document.createElement('li');
        listItem.className = 'block px-4 py-2 hover:bg-clr-prim hover:text-white border-none'; // Add the 'border-none' class

        listItem.textContent = baudRate;

        listItem.addEventListener('click', function () {
            document.getElementById('dropdownBaudRateText').textContent = baudRate;

            // Assuming tab1 is always the current tab]
            tabSerialPorts['tab1']?.changeBaudrate(baudRate);
            console.log('Baud rate updated in tab1:', tabSerialPorts['tab1']);
        });

        baudRateDropdown.appendChild(listItem);
    });
}


// Function to update the line ending dropdown
function updateLineEnding() {
    const lineEndingDropdown = document.getElementById('dropdownLineEnd');
    lineEndingDropdown.innerHTML = ''; // Clear existing options

    // Define your line ending options and their names
    const lineEndings = {
        '\n': 'New Line',
        '\r': 'Carriage Return',
        '\r\n': 'Both NL & CR',
        '': 'None' // Added 'None' option
    };

    Object.entries(lineEndings).forEach(([symbol, name]) => {
        const listItem = document.createElement('li');
        listItem.className = 'block px-4 py-2 hover:bg-clr-prim hover:text-white border-none';

        listItem.textContent = name; // Set the name as the list item's text

        listItem.addEventListener('click', function () {
            // Update the button's text to the name of the selected line ending
            const textSpan = document.getElementById('dropDownLineEnding');
            textSpan.textContent = name;

            // Assuming tab1 is always the current tab
            tabSerialPorts['tab1']?.setEndline(symbol);
            console.log('Line ending updated in tab1:', tabSerialPorts['tab1']);
        });

        lineEndingDropdown.appendChild(listItem);
    });
}


// Function to handle received data from serial pipe
function serialPortReceiveCallback(data) {
    // Create a new div with the received data
    var newDataDiv = document.createElement('div');
    newDataDiv.innerHTML = data;

    // Append the new div to the output div
    var outputDiv = document.getElementById('outputDiv');
    outputDiv.appendChild(newDataDiv);

    // Auto-scroll if enabled
    var autoScrollToggle = document.getElementById('autoScroll');
    if (autoScrollToggle && autoScrollToggle.checked) {
        outputDiv.scrollTop = outputDiv.scrollHeight;
    }
}

// Function to handle connect button click
function handleConClick() {
    if (tabSerialPorts['tab1'] && !tabSerialPorts['tab1'].enabled) {
        tabSerialPorts['tab1'].serialConnect();
        tabSerialPorts['tab1'].setCallbackForReceivedData(serialPortReceiveCallback);
        tabSerialPorts['tab1'].connectSerialPipe();
    }
}

// Function to handle close button click
function handleCloseClick() {
    if (tabSerialPorts['tab1']?.enabled) {
        tabSerialPorts['tab1'].serialDisconnect();
    }
}

// Function to handle input box and send button
function setupInputHandlers() {
    const inputBox = document.getElementById('inputBox');
    const sendButton = document.getElementById('sendButton');

    const processInput = () => {
        if (!tabSerialPorts['tab1']?.enabled) {
            return;
        }
        var inputData = { data: inputBox.value };
        if (inputData.data === '' || inputData.data === null) {
            return;
        }
        serialPortReceiveCallback(inputData.data);
        tabSerialPorts['tab1']?.sendData(inputData);
        inputBox.value = '';
    };

    if (inputBox) {
        inputBox.addEventListener('keydown', function (event) {
            if (event.key === 'Enter') {
                sendButton.style.backgroundColor = '#6366f1';
                processInput();

                setTimeout(() => {
                    sendButton.style.backgroundColor = '';
                }, 90);
            }
        });
    } else {
        console.log("Input box not found");
    }

    sendButton?.addEventListener('mousedown', processInput);
}
