// main.js
import { attachUsbEventListeners, attachUsbEventListenersButton } from './usb/usb.js';
import './style.css';

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

      if (page === './usb/usb') {
        attachUsbEventListeners();
        attachUsbEventListenersButton();
      }
    })
    .catch(error => {
      console.error('Error loading content:', error);
      document.getElementById('content-area').innerHTML = '<p>Error loading content.</p>';
    });
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', event => {
      event.preventDefault();
      const page = item.getAttribute('data-page');
      loadContent(page);
    });
  });
});

// Initial content loading
loadContent('./usb/usb');