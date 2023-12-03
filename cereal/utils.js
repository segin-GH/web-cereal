// utils.js
export function createDownArrow() {
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

export function toggleDropdown(dropdownId) {
    var dropdown = document.getElementById(dropdownId);
    if (dropdown) {
        dropdown.classList.toggle('hidden');
    }
}

export function attachDropdownListener(dropdownButtonId, dropdownContentId) {
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

function updateDropdownSelection(dropdownButton, selectedValue) {
    dropdownButton.textContent = selectedValue;
    dropdownButton.appendChild(createDownArrow());
}
