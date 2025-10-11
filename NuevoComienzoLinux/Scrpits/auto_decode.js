const fs = require('fs');

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

// Decodificar strings específicas encontradas en análisis previo
const testStrings = [
    ")HS(*39YUF?",
    "gYhCge*3y3H*Zd3#", 
    "other_encoded_strings_here"
];

console.log("=== DECODIFICACIÓN AUTOMÁTICA ===");
testStrings.forEach(str => {
    console.log(`"${str}" -> "${f(str)}"`);
});

// Buscar en el código patrones de conexión
const code = fs.readFileSync('utilities.js', 'utf8');
const connectionPatterns = [
    /['"](jdbc:[^'"]+)['"]/gi,
    /['"](mysql:[^'"]+)['"]/gi,
    /['"](password[^'"]+)['"]/gi,
    /['"](user[^'"]+)['"]/gi
];

connectionPatterns.forEach(pattern => {
    const matches = code.match(pattern);
    if (matches) {
        console.log(`\nPatrón encontrado (${pattern}):`);
        matches.slice(0, 5).forEach(match => console.log("  " + match));
    }
});
