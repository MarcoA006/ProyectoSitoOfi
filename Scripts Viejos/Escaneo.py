import requests
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib3
import sys

# Desactivar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TomcatScanner:
    def __init__(self, target_ip, target_url):
        self.target_ip = target_ip
        self.target_url = target_url
        self.common_ports = [80, 443, 8080, 8009, 8443, 8005, 8000, 8888, 9090]
        self.tomcat_paths = [
            "/manager/html",
            "/manager/status",
            "/manager/jmxproxy",
            "/host-manager/html",
            "/docs/",
            "/examples/",
            "/admin/",
            "/webdav/",
            "/cgi-bin/",
            "/servlets-examples/",
            "/jsp-examples/",
            "/tomcat-docs/",
            "/ROOT/",
            "/web-console/",
            "/invoker/JMXInvokerServlet"
        ]
        
        # Usuarios y contraseñas comunes de Tomcat
        self.credentials = [
            ("admin", "admin"),
            ("tomcat", "tomcat"),
            ("admin", "tomcat"),
            ("admin", ""),
            ("tomcat", ""),
            ("admin", "password"),
            ("root", "root"),
            ("admin", "123456")
        ]

    def scan_port(self, port):
        """Escanea un puerto específico"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.target_ip, port))
            sock.close()
            if result == 0:
                print(f"[+] Puerto {port} abierto")
                return port
        except Exception as e:
            pass
        return None

    def scan_ports(self):
        """Escanea puertos comunes"""
        print("[*] Escaneando puertos...")
        open_ports = []
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(self.scan_port, self.common_ports)
            open_ports = [port for port in results if port is not None]
        
        return open_ports

    def check_tomcat_paths(self, base_url):
        """Verifica rutas comunes de Tomcat"""
        print(f"[*] Verificando rutas en {base_url}")
        found_paths = []
        
        for path in self.tomcat_paths:
            try:
                url = f"{base_url}{path}"
                response = requests.get(url, timeout=5, verify=False)
                
                if response.status_code == 200:
                    print(f"[+] Ruta encontrada: {url}")
                    found_paths.append(url)
                elif response.status_code == 401:
                    print(f"[!] Ruta protegida: {url} (Requiere autenticación)")
                    found_paths.append(f"{url} [PROTEGIDA]")
                elif response.status_code == 403:
                    print(f"[!] Acceso prohibido: {url}")
                    
            except requests.RequestException:
                pass
        
        return found_paths

    def brute_force_manager(self, base_url):
        """Intenta autenticarse en el Manager"""
        print("[*] Probando credenciales en Tomcat Manager...")
        
        for username, password in self.credentials:
            try:
                session = requests.Session()
                auth = (username, password)
                response = session.get(f"{base_url}/manager/html", auth=auth, timeout=5, verify=False)
                
                if response.status_code == 200 and "Tomcat Web Application Manager" in response.text:
                    print(f"[+] ¡Credenciales válidas encontradas! {username}:{password}")
                    return username, password, session
                else:
                    print(f"[-] Falló: {username}:{password}")
                    
            except requests.RequestException:
                pass
        
        return None, None, None

    def check_vulnerabilities(self, base_url, session=None):
        """Verifica vulnerabilidades comunes"""
        print("[*] Verificando vulnerabilidades...")
        
        # Verificar si examples está habilitado
        try:
            response = requests.get(f"{base_url}/examples/", timeout=5, verify=False)
            if response.status_code == 200:
                print("[!] ¡Cuidado! Directorio /examples/ está accesible")
        except:
            pass
        
        # Verificar si docs está habilitado
        try:
            response = requests.get(f"{base_url}/docs/", timeout=5, verify=False)
            if response.status_code == 200:
                print("[!] ¡Cuidado! Directorio /docs/ está accesible")
        except:
            pass

    def scan_web_applications(self, session, base_url):
        """Escanea aplicaciones web desplegadas"""
        if session:
            try:
                response = session.get(f"{base_url}/manager/html", verify=False)
                if response.status_code == 200:
                    # Buscar aplicaciones en la página del manager
                    if "web application list" in response.text.lower():
                        print("[+] Aplicaciones web encontradas en el manager")
                        # Aquí podrías parsear el HTML para extraer las aplicaciones
            except:
                pass

    def run_scan(self):
        """Ejecuta el escaneo completo"""
        print(f"[*] Iniciando escaneo de {self.target_ip}")
        
        # Escanear puertos
        open_ports = self.scan_ports()
        
        # Probar diferentes URLs base
        base_urls = []
        for port in open_ports:
            if port == 443:
                base_urls.append(f"https://{self.target_ip}:{port}")
            else:
                base_urls.append(f"http://{self.target_ip}:{port}")
        
        # También probar sin puerto para el caso de puerto 80
        base_urls.append(f"http://{self.target_ip}")
        
        for base_url in base_urls:
            print(f"\n[*] Probando {base_url}")
            
            # Verificar rutas
            self.check_tomcat_paths(base_url)
            
            # Intentar brute force
            username, password, session = self.brute_force_manager(base_url)
            
            # Verificar vulnerabilidades
            self.check_vulnerabilities(base_url, session)
            
            # Escanear aplicaciones si tenemos sesión
            if session:
                self.scan_web_applications(session, base_url)

# Uso del script
if __name__ == "__main__":
    # Tu servidor
    target_ip = "189.254.143.102"
    target_url = "http://189.254.143.102/manager"
    
    scanner = TomcatScanner(target_ip, target_url)
    scanner.run_scan()