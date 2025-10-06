#!/bin/bash
DOMAIN="sito.utslp.edu.mx"

echo "[+] Starting Tomcat Audit for $DOMAIN"
echo "[+] Date: $(date)"

echo "[1] Port Scanning"
nmap -p 80,443,8000,8005,8009,8080,8443 -sV $DOMAIN

echo "[2] Directory Enumeration"
gobuster dir -u https://$DOMAIN/ -w /usr/share/wordlists/dirb/common.txt -x jsp,html -t 20 -o directories.txt

echo "[3] Tomcat Manager Enumeration"
curl -k "https://$DOMAIN/manager/status" 2>/dev/null | head -50

echo "[4] Configuration Files Check"
for file in "web.xml" "context.xml" "tomcat-users.xml" "server.xml"; do
    echo "Checking: $file"
    curl -k "https://$DOMAIN/$file" 2>/dev/null | head -5
done

echo "[5] JavaScript Analysis"
wget -q -O - https://$DOMAIN/javascript/utilities.js 2>/dev/null | grep -i "password\|user" | head -10

echo "[+] Audit Complete"
