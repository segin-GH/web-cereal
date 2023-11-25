function loadContent(page) {
  fetch(`${page}.html`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.text();
    })
    .then(html => {
      document.getElementById('content-area').innerHTML = html;
      // Attach event listener after content is loaded
      attachDropdownListener();
      if (page === 'usb') {
        getPortDataFromOatsAgent();
      }
    })
    .catch(error => {
      console.error('Error loading content:', error);
      document.getElementById('content-area').innerHTML = '<p>Error loading content.</p>';
    });
}

function attachDropdownListener() {
  document.getElementById('dropdownUSBPort').addEventListener('click', function () {
    var dropdownUSB = document.getElementById('dropdownUSB');
    dropdownUSB.classList.toggle('hidden');
  });

  // Event listeners for USB port selections
  var usbPortItems = document.querySelectorAll('#dropdownUSB li');
  usbPortItems.forEach(function (item) {
    item.addEventListener('click', function () {
      var selectedPort = this.textContent;
      var buttonUSBPort = document.getElementById('dropdownUSBPort');
      buttonUSBPort.textContent = selectedPort; // Update button text
      buttonUSBPort.appendChild(createDownArrow()); // Add the down arrow again
    });
  });

  document.getElementById('dropdownBaudRate').addEventListener('click', function () {
    var dropdown = document.getElementById('dropdownBaud');
    dropdown.classList.toggle('hidden');
  });

  var baudRateItems = document.querySelectorAll('#dropdownBaud li');
  baudRateItems.forEach(function (item) {
    item.addEventListener('click', function () {
      var selectedBaudRate = this.textContent;
      var buttonBaudRate = document.getElementById('dropdownBaudRate');
      buttonBaudRate.textContent = selectedBaudRate; // Update button text
      buttonBaudRate.appendChild(createDownArrow()); // Add the down arrow again
    });
  });

  function createDownArrow() {
    var svgNS = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("class", "ml-2 w-2 h-2");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("fill", "none");
    svg.setAttribute("viewBox", "0 0 10 6");

    var path = document.createElementNS(svgNS, "path");
    path.setAttribute("stroke", "currentColor");
    path.setAttribute("stroke-linecap", "round");
    path.setAttribute("stroke-linejoin", "round");
    path.setAttribute("stroke-width", "2");
    path.setAttribute("d", "m1 1 4 4 4-4");

    svg.appendChild(path);
    return svg;
  }

}

function getPortDataFromOatsAgent() {
  fetch('http://localhost:5000/usb')
    .then(response => response.json())
    .then(data => {
      console.log("Data from oatsAgent:\n\n", JSON.stringify(data, null, 2));

      // Get the dropdown menu element
      var dropdownMenu = document.getElementById('dropdownMenu');

      // Clear existing menu items
      dropdownMenu.innerHTML = '';

      // Add new menu items for each port
      data.ports.forEach(port => {
        // Extract port name, e.g., "USB0" from "/dev/ttyUSB0"
        var portName = port.port.match(/tty(USB\d+)/)[1];

        // Create new menu item
        var menuItem = document.createElement('a');
        menuItem.href = '#';
        menuItem.className = 'block p-2 hover:bg-clr-bg-thr';
        menuItem.textContent = portName;

        // Append new menu item to the dropdown
        dropdownMenu.appendChild(menuItem);
      });

    })
    .catch(error => console.error('Error:', error));
}


loadContent('usb');