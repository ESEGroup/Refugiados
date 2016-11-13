"use strict"
var format_CPF = function(CPF) {
    CPF = CPF.replace(/[a-zA-z]*/g,"");
    return CPF.slice(0,3) + (CPF.length > 3 ? "." + CPF.slice(3,6) + (CPF.length > 6 ? "." + CPF.slice(6, 9) + (CPF.length > 9 ? "-" + CPF.slice(9,11) : "") : "") : "");
}
