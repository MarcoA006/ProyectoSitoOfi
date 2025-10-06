import requests
import urllib3
from xml.etree import ElementTree

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ServerInfoAnalyzer:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"

    def analyze_server_headers(self):
        """Analiza headers del servidor"""
        print("[*] Analizando headers del servidor...")
        
        try:
            response = requests.get(self.base_url, verify=False, timeout=5)
            
            server_info = {
                "Server": response.headers.get("Server", "No info"),
                "X-Powered-By": response.headers.get("X-Powered-By", "No info"),
                "X-AspNet-Version": response.headers.get("X-AspNet-Version", "No info"),
                "Set-Cookie": response.headers.get("Set-Cookie", "No cookies")
            }
            
            print("[+] Información del servidor:")
            for key, value in server_info.items():
                print(f"    {key}: {value}")
                
        except Exception as e:
            print(f"[-] Error analizando headers: {e}")

    def check_tomcat_manager_status(self):
        """Verifica estado del manager"""
        print("\n[*] Verificando estado del Tomcat Manager...")
        
        manager_urls = [
            f"{self.base_url}/manager/status",
            f"{self.base_url}/manager/jmxproxy",
            f"{self.base_url}/manager/list"
        ]
        
        for url in manager_urls:
            try:
                response = requests.get(url, verify=False, timeout=5)
                if response.status_code == 401:
                    print(f"[+] Manager protegido: {url}")
                elif response.status_code == 200:
                    print(f"[!] Manager accesible: {url}")
                else:
                    print(f"[-] Manager {url}: {response.status_code}")
            except:
                pass

# Ejecutar análisis
analyzer = ServerInfoAnalyzer("189.254.143.102")
analyzer.analyze_server_headers()
analyzer.check_tomcat_manager_status()