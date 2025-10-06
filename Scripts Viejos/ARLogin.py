import requests
import re

class LoginResponseAnalyzer:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
    
    def analyze_login_response(self):
        """Analizar detalladamente la respuesta del login"""
        print("=== ANÁLISIS DETALLADO DEL LOGIN ===")
        
        # Hacer login y capturar la respuesta completa
        login_data = {
            'yAccion': 'login',
            'yUsuario': 'hnieto',
            'xUsuario': 'hnieto',
            'xContrasena': 'utslp',
            'yIntentos': '1'
        }
        
        response = self.session.post(f"{self.target}/jsp/index.jsp", data=login_data)
        
        print(f"Estado HTTP: {response.status_code}")
        print(f"Tamaño respuesta: {len(response.text)} bytes")
        print(f"URL final: {response.url}")
        
        # Guardar respuesta para análisis
        with open('login_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("✅ Respuesta guardada en login_response.html")
        
        # Análisis detallado del contenido
        self.analyze_content(response.text)
    
    def analyze_content(self, html):
        """Analizar el contenido HTML de la respuesta"""
        print("\n[ANÁLISIS DEL CONTENIDO]")
        
        # Buscar mensajes de error
        error_patterns = [
            r'error[^>]*>([^<]+)<',
            r'alert[^>]*>([^<]+)<', 
            r'mensaje[^>]*>([^<]+)<',
            r'invalid[^>]*>([^<]+)<',
            r'incorrect[^>]*>([^<]+)<',
            r'fallo[^>]*>([^<]+)<'
        ]
        
        errors_found = []
        for pattern in error_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                errors_found.extend(matches)
        
        if errors_found:
            print("❌ MENSAJES DE ERROR ENCONTRADOS:")
            for error in errors_found[:3]:  # Mostrar primeros 3
                print(f"   - {error}")
        else:
            print("✅ No se encontraron mensajes de error evidentes")
        
        # Buscar indicadores de éxito
        success_indicators = [
            'bienvenido', 'welcome', 'éxito', 'success', 'correcto',
            'menu', 'menú', 'dashboard', 'panel', 'administración'
        ]
        
        success_found = []
        for indicator in success_indicators:
            if indicator in html.lower():
                success_found.append(indicator)
        
        if success_found:
            print("✅ INDICADORES DE ÉXITO:")
            for indicator in success_found:
                print(f"   - {indicator}")
        else:
            print("❌ No se encontraron indicadores de éxito claros")
        
        # Analizar redirecciones
        redirects = re.findall(r'window\.location[^=]*=[\'"]([^\'"]+)[\'"]', html)
        if redirects:
            print("🔀 REDIRECCIONES JAVASCRIPT:")
            for redirect in redirects:
                print(f"   - {redirect}")
        
        # Buscar enlaces después del login
        links = re.findall(r'href=[\'"]([^\'"]*)[\'"]', html)
        interesting_links = [link for link in links if any(x in link for x in ['.jsp', 'admin', 'menu', 'panel'])]
        
        if interesting_links:
            print("🔗 ENLACES INTERESANTES:")
            for link in interesting_links[:5]:
                print(f"   - {link}")

# Ejecutar
analyzer = LoginResponseAnalyzer("http://189.254.143.102")
analyzer.analyze_login_response()