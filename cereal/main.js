import { initializeTerminal } from './terminalSetup.js';

// initializeTerminal()

export function toggleControlCenterType(type) {
  if (type === 1) {
    console.log("term selected");
    document.getElementById('plot-ctrl').classList.add('hidden');
    document.getElementById('term-ctrl').classList.remove('hidden');

    // Change button colors
    document.getElementById('butt-term').classList.remove('bg-bg3');
    document.getElementById('butt-term').classList.add('bg-acc');
    document.getElementById('butt-plot').classList.remove('bg-acc');
    document.getElementById('butt-plot').classList.add('bg-bg3');
  } else {
    console.log("plot selected");
    document.getElementById('plot-ctrl').classList.remove('hidden');
    document.getElementById('term-ctrl').classList.add('hidden');

    // Change button colors
    document.getElementById('butt-plot').classList.remove('bg-bg3');
    document.getElementById('butt-plot').classList.add('bg-acc');
    document.getElementById('butt-term').classList.remove('bg-acc');
    document.getElementById('butt-term').classList.add('bg-bg3');
  }
}

// Wait until the DOM is fully loaded before attaching event listeners
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("butt-term").addEventListener("click", () => toggleControlCenterType(1));
  document.getElementById("butt-plot").addEventListener("click", () => toggleControlCenterType(2));
});
