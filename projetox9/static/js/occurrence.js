"use strict"

document.addEventListener("DOMContentLoaded", function(ev) {
    flatpickr(".flatpickr", {
        enableTime: true,
        dateFormat: "d/m/Y H:i",
        allowInput: true,
        defaultDate: new Date(),
        time_24hr: true
    });
});
