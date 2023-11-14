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
    })
    .catch(error => {
      console.error('Error loading content:', error);
      document.getElementById('content-area').innerHTML = '<p>Error loading content.</p>';
    });
}

function attachDropdownListener() {
  const dropdownButton = document.getElementById('dropdownButton');
  if (dropdownButton) {
    dropdownButton.addEventListener('click', function () {
      console.log("Dropdown button clicked");
      document.getElementById('dropdownMenu').classList.toggle('hidden');
    });
  } else {
    console.warn('Dropdown button not found');
  }
}

loadContent('usb');
