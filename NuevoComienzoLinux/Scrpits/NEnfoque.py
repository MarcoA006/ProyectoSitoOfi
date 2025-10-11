#!/usr/bin/env python3
import requests
import urllib3
urllib3.disable_warnings()

def analyze_jsp_access():
    target = "https://189.254.143.102"
    
    # Probar acceso a JSPs específicos con la sesión
    jsps_to_test = [
        "/jsp/index.jsp",
        "/jsp/login.jsp", 
        "/jsp/menu.jsp",
        "/jsp/admin/",
        "/jsp/administracion/",
        "/examples/jsp/",
        "/examples/jsp/jsp2/",
        "/examples/jsp/snp/"
    ]
    
    session = requests.Session()
    session.cookies.set('JSESSIONID', '00000000000000000000000000000000')
    session.verify = False
    
    print("=== ANALIZANDO ACCESO A JSPs ===")
    
    for jsp in jsps_to_test:
        try:
            r = session.get(f"{target}{jsp}", timeout=5)
            print(f"{jsp}: {r.status_code}")
            
            if r.status_code == 200:
                # Buscar formularios o enlaces interesantes
                if 'form' in r.text.lower() or 'action=' in r.text.lower():
                    print(f"   📝 FORMULARIO ENCONTRADO")
                if 'password' in r.text.lower() or 'login' in r.text.lower():
                    print(f"   🔐 PÁGINA DE LOGIN")
                    
        except Exception as e:
            print(f"{jsp}: Error - {str(e)[:50]}")

if __name__ == "__main__":
    analyze_jsp_access()
