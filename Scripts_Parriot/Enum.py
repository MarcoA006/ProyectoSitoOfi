#!/usr/bin/env python3
import requests

target = "https://189.254.143.102"
subdomains = [
    "sito", "sitoma", "sita", "misito", "admin", "sistema", 
    "aplicaciones", "plataforma", "web", "app", "portal",
    "intranet", "interno", "secure", "auth", "login",
    "manager", "tomcat", "test", "dev", "staging"
]

for sub in subdomains:
    host = f"{sub}.utslp.edu.mx"
    headers = {"Host": host}
    
    try:
        response = requests.get(target, headers=headers, verify=False, timeout=5)
        print(f"[+] {host} - Status: {response.status_code} - Length: {len(response.text)}")
        
        if response.status_code != 200 or len(response.text) != 16038:
            print(f"    [DIFERENTE] ¡Posible subdominio válido!")
            with open(f"subdomain_{sub}.html", "w") as f:
                f.write(response.text)
    except Exception as e:
        print(f"[-] {host} - Error: {e}")