import requests
from http.cookies import SimpleCookie

class SessionAnalyzer:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
        
    def analyze_session(self):
        """Analizar la sesión autenticada"""
        print("[+] Analizando sesión autenticada...")
        
        # Primero hacer login
        login_data = {
            'yAccion': 'login',
            'yUsuario': 'hnieto',
            'xUsuario': 'hnieto', 
            'xContrasena': 'utslp',
            'yIntentos': '1'
        }
        
        response = self.session.post(f"{self.target}/jsp/index.jsp", data=login_data)
        
        if response.status_code == 200:
            print("✅ Sesión obtenida")
            
            # Analizar cookies
            print("\n🍪 COOKIES DE SESIÓN:")
            for cookie in self.session.cookies:
                print(f"   {cookie.name} = {cookie.value}")
                if cookie.name == 'JSESSIONID':
                    print(f"      🔑 JSESSIONID: {cookie.value}")
            
            # Analizar headers de respuesta
            print("\n📋 HEADERS DE RESPUESTA:")
            for header, value in response.headers.items():
                if any(key in header.lower() for key in ['server', 'x-powered', 'set-cookie']):
                    print(f"   {header}: {value}")
            
            # Buscar tokens en la página
            import re
            tokens = re.findall(r'name="[^"]*token[^"]*" value="([^"]*)"', response.text)
            if tokens:
                print(f"\n🔐 TOKENS ENCONTRADOS: {tokens}")
            
            # Buscar información del usuario en la página
            if 'hnieto' in response.text:
                print("👤 Nombre de usuario encontrado en la página")
            
            return True
        else:
            print("❌ No se pudo obtener sesión")
            return False

# Ejecutar
analyzer = SessionAnalyzer("http://189.254.143.102")
analyzer.analyze_session()