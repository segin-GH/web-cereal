
/**
 * Main JavaScript file for handling page content loading and interactive elements.
 * Includes functions for loading HTML content, attaching event listeners, and handling dropdowns.
 */

// Function to load HTML content into a specified element
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
      attachEventListeners();
    })
    .catch(error => {
      console.error('Error loading content:', error);
      document.getElementById('content-area').innerHTML = '<p>Error loading content.</p>';
    });
}

// Function to attach event listeners to various elements
function attachEventListeners() {
  attachDropdownListener('dropdownUSBPort', 'dropdownUSB');
  attachDropdownListener('dropdownBaudRate', 'dropdownBaud');
  attachDropdownListener('dropdownLineEnding', 'dropdownLineEnd');
}

// Generic function to attach a listener to a dropdown
function attachDropdownListener(dropdownButtonId, dropdownContentId) {
  var dropdownButton = document.getElementById(dropdownButtonId);
  if (dropdownButton) {
    dropdownButton.addEventListener('click', function () {
      toggleDropdown(dropdownContentId);
    });

    var dropdownItems = document.querySelectorAll(`#${dropdownContentId} li`);
    dropdownItems.forEach(item => {
      item.addEventListener('click', function () {
        updateDropdownSelection(dropdownButton, this.textContent);
        toggleDropdown(dropdownContentId);
      });
    });
  }
}

// Function to update the dropdown selection display
function updateDropdownSelection(dropdownButton, selectedValue) {
  dropdownButton.textContent = selectedValue;
  dropdownButton.appendChild(createDownArrow());
}

// Function to create a down arrow SVG element
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

// Function to toggle dropdown visibility
function toggleDropdown(dropdownId) {
  var dropdown = document.getElementById(dropdownId);
  if (dropdown) {
    dropdown.classList.toggle('hidden');
  }
}

// Initial content loading
loadContent('usb');