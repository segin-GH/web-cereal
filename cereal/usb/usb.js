import { attachDropdownListener } from '../utils.js';
import { SerialPort } from './serialPort.js';
import io from 'socket.io-client';

let tabSerialPorts = {
    "tab1": null,
};

export function attachUsbEventListeners() {
    attachDropdownListener('dropdownUSBPort', 'dropdownUSB');
    attachDropdownListener('dropdownBaudRate', 'dropdownBaud');
    attachDropdownListener('dropdownLineEnding', 'dropdownLineEnd');
}

// usb/usb.js

export function attachUsbEventListenersButton() {
    const button = document.getElementById('dropdownUSBPort');
    if (button) { // Check if the button exists
        button.addEventListener('click', fetchPortData);
    }
    const button2 = document.getElementById('dropdownBaudRate');
    if (button2) { // Check if the button exists
        button2.addEventListener('click', updateBaudRate);
    }
    const button3 = document.getElementById('dropdownLineEnding');
    if (button3) { // Check if the button exists
        button3.addEventListener('click', updateLineEnding);
    }

    const conButton = document.getElementById('connectButton');
    if (conButton) {
        conButton.addEventListener('click', handleConClick);
    } else {
        console.log("Connect button not found");
    }

    const closeButton = document.getElementById('clearButton');
    if (closeButton) {
        closeButton.addEventListener('click', handleCloseClick);
    } else {
        console.log("Close button not found");
    }
}

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

            // Assuming tab1 is always the current tab
            if (tabSerialPorts['tab1']) {
                tabSerialPorts['tab1'].changeBaudrate(baudRate);
            }

            console.log('Baud rate updated in tab1:', tabSerialPorts['tab1']);
        });

        baudRateDropdown.appendChild(listItem);
    });
}



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
            if (tabSerialPorts['tab1']) {
                tabSerialPorts['tab1'].setEndline(symbol);
            }

            console.log('Line ending updated in tab1:', tabSerialPorts['tab1']);
        });

        lineEndingDropdown.appendChild(listItem);
    });
}

let socket = null;

function setupWebSocket() {
    var socket = io.connect('ws://localhost:5000');

    socket.on('usb_data', function (data) {
        var outputDiv = document.getElementById('outputDiv');
        var outerDiv = outputDiv.parentElement;

        // Create a new div for each piece of data
        var newDataDiv = document.createElement('div');
        newDataDiv.innerHTML = data.data;
        outputDiv.appendChild(newDataDiv);

        var autoScrollToggle = document.getElementById('autoScroll'); // Get the toggle switch

        // Check if the outer div is going to overflow and if auto scroll is on
        if (outerDiv.scrollHeight > outerDiv.clientHeight && autoScrollToggle.checked) {
            // Add a small delay before scrolling the outerDiv
            outerDiv.scrollTop = outerDiv.scrollHeight;
        }
    });
}

// Function to handle connect button click
function handleConClick() {
    if (tabSerialPorts['tab1']) {
        tabSerialPorts['tab1'].serialConnect();
        setupWebSocket();  // Setup WebSocket connection
    }
}

// Function to handle close button click
function handleCloseClick() {
    if (tabSerialPorts['tab1']) {
        tabSerialPorts['tab1'].serialDisconnect();
    }
}