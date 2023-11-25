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
    var dropdown = document.getElementById('dropdownUSB');
    dropdown.classList.toggle('hidden');
  });
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