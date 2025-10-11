const fs = require('fs');

// La función de desofuscación del backdoor
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

// Leer el archivo completo del backdoor
const backdoorContent = fs.readFileSync('utilities.js', 'utf8');

// Extraer TODAS las cadenas ofuscadas
const encodedStrings = backdoorContent.match(/'[^']+'|"[^"]+"/g) || [];

console.log("=== ANÁLISIS COMPLETO DEL BACKDOOR ===");
console.log(`Se encontraron ${encodedStrings.length} cadenas potencialmente ofuscadas\n`);

// Probar desofuscación en todas las cadenas
encodedStrings.forEach((str, index) => {
    const cleanStr = str.replace(/['"]/g, '');
    
    // Solo probar con cadenas que parecen ofuscadas (sin espacios, caracteres especiales)
    if (cleanStr.length > 5 && !cleanStr.includes(' ') && /[^a-zA-Z0-9]/.test(cleanStr)) {
        try {
            const decoded = f(cleanStr);
            if (decoded && decoded.length > 3) {
                console.log(`Cadena ${index}: "${cleanStr}"`);
                console.log(`Decodificado: "${decoded}"`);
                
                // Buscar patrones específicos
                if (decoded.includes('password') || decoded.includes('user') || decoded.includes('login')) {
                    console.log('🔑 POSIBLE CREDENCIAL ENCONTRADA!');
                }
                if (decoded.includes('jdbc') || decoded.includes('database')) {
                    console.log('🗄️  POSIBLE CONFIGURACIÓN DE BD!');
                }
                console.log('---');
            }
        } catch (e) {
            // Ignorar errores de desofuscación
        }
    }
});

// Buscar específicamente patrones de conexión a BD
console.log("=== BUSCANDO CONFIGURACIÓN DE BASE DE DATOS ===");
const dbPatterns = [
    /jdbc:([^'"]+)/gi,
    /mysql:([^'"]+)/gi, 
    /database=([^'"]+)/gi,
    /password=([^'"]+)/gi,
    /username=([^'"]+)/gi
];

dbPatterns.forEach(pattern => {
    const matches = backdoorContent.match(pattern);
    if (matches) {
        console.log(`Patrón ${pattern}:`, matches.slice(0, 3));
    }
});
