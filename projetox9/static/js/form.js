"use strict"

document.addEventListener("DOMContentLoaded", function(ev) {
    var CPFs = document.getElementsByClassName("CPF");
    for (var i=0; i<CPFs.length;++i){
        CPFs[i].addEventListener('input', function(ev) {
            var content = ev.target.value.replace(/\./g,"").replace(/-/g,"");
            ev.target.value = format_CPF(content);
        });
    }
});
