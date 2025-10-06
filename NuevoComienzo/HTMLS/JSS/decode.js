// decode_extended.js
function f(D) {
    var p = "aRfguQwJvbc#h l)[W2jkm/op?N!rVisGq=@tB3O4CdeF9n0U(HI_6X]KLM>,DE.-Pxyz15YZ<78AST";
    var l = "gJvbUWc#,Dh5w*sGq=@tB[!39nO4CuYdeF0a]Kl)iQxZ<7yf2jkSTrVm/oR-Pp?NI_6XLM>E.z18A(H";
    var F = D.split("").reverse();
    var E = "";
    for(cont = 0; cont < F.length; cont++) {
        for(cont2 = 0; cont2 < l.length; cont2++) {
            if(l[cont2] == F[cont]) {
                E = E + "" + p[cont2];
                break;
            }
        }
    }
    return E;
}

// Decodifica más strings importantes
console.log("Backdoor strings:");
console.log("1:", f(")HS(*39YUF?")); // Equipo SITO
console.log("2:", f("gYhCge*3y3H*Zd3#")); // Jose Tono Garcia
console.log("3:", f("3]hZX3C_*Zx*CZxYo*PC3xgss3CCgdZp"));
console.log("4:", f("LZCY[gJ*gCdS"));
console.log("5:", f("LYyUR*hI3tygU#"));
console.log("6:", f("9(*sZXygp"));
