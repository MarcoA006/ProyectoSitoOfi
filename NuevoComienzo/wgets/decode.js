const fs = require('fs');
const code = fs.readFileSync('backdoor_analysis.js', 'utf8');

// Buscar y decodificar patrones comunes
console.log("=== BUSCANDO PATRONES CODIFICADOS ===");

// Buscar Base64
const base64Regex = /['"]([A-Za-z0-9+/]{20,}={0,2})['"]/g;
let match;
while ((match = base64Regex.exec(code)) !== null) {
    try {
        const decoded = Buffer.from(match[1], 'base64').toString();
        if (decoded.length > 5 && /[a-zA-Z]/.test(decoded)) {
            console.log(`Base64: ${match[1]} -> ${decoded}`);
        }
    } catch (e) {}
}

// Buscar Hex
const hexRegex = /(\\\\x[0-9a-f]{2}){5,}/g;
const hexMatches = code.match(hexRegex);
if (hexMatches) {
    hexMatches.forEach(hexStr => {
        const cleanHex = hexStr.replace(/\\\\x/g, '');
        try {
            const decoded = Buffer.from(cleanHex, 'hex').toString();
            console.log(`Hex: ${hexStr} -> ${decoded}`);
        } catch (e) {}
    });
}

// Buscar Unicode escapes
const unicodeRegex = /(\\\\u[0-9a-f]{4}){3,}/g;
const unicodeMatches = code.match(unicodeRegex);
if (unicodeMatches) {
    unicodeMatches.forEach(unicodeStr => {
        try {
            const decoded = unicodeStr.replace(/\\\\u/g, '')
                .match(/.{4}/g)
                .map(hex => String.fromCharCode(parseInt(hex, 16)))
                .join('');
            console.log(`Unicode: ${unicodeStr} -> ${decoded}`);
        } catch (e) {}
    });
}
