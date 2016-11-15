"use strict"
document.addEventListener("DOMContentLoaded", function(ev) {
    document.getElementsByClassName("CPF")[0].addEventListener('input', function(ev) {
        ev.target.value = format_CPF(ev.target.value);
    });

    document.getElementsByTagName("form")[0].addEventListener('submit', function(ev) {
        var list = ["CPF", "password"];
        for (var i in list)
            if (document.getElementById(list[i]).value === "")
                ev.preventDefault();
    });
});
