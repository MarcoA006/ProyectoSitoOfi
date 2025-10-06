import requests
import sys
import urllib3
from urllib.parse import urljoin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AccessVerifier:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.verify = False
    
    def verify_login_effectiveness(self):
        """Verificar si el login realmente nos da acceso"""
        print("=== VERIFICACIÓN DE ACCESO REAL ===")
        
        # Primero hacer login
        login_data = {
            'yAccion': 'login',
            'yUsuario': 'hnieto',
            'xUsuario': 'hnieto',
            'xContrasena': 'utslp', 
            'yIntentos': '1'
        }
        
        print("[1] Intentando login...")
        response = self.session.post(f"{self.target}/jsp/index.jsp", data=login_data)
        
        # Verificar indicadores reales de login
        login_indicators = [
            'cerrar_sesion.jsp' in response.text,
            'Bienvenido' in response.text,
            'Bienvenida' in response.text,
            'Menu' in response.text,
            'Menú' in response.text,
            'hnieto' in response.text,
            'Cerrar Sesión' in response.text,
            'Logout' in response.text
        ]
        
        if any(login_indicators):
            print("✅ Posible login exitoso")
            print(f"   Indicadores encontrados: {sum(login_indicators)}/8")
        else:
            print("❌ Login probablemente fallido")
            print("   La página retorna después del login:")
            print(f"   Tamaño: {len(response.text)} bytes")
            print(f"   Contiene 'error': {'error' in response.text.lower()}")
            print(f"   Contiene 'invalid': {'invalid' in response.text.lower()}")
            return False
        
        # Verificar acceso a páginas específicas
        print("\n[2] Verificando acceso a páginas conocidas...")
        test_pages = [
            '/jsp/index.jsp',
            '/jsp/cerrar_sesion.jsp',
            '/jsp/escolar/proceso_admision/proceso_interesado.jsp'
        ]
        
        for page in test_pages:
            try:
                response = self.session.get(urljoin(self.target, page))
                print(f"   {page}: HTTP {response.status_code} - {len(response.text)} bytes")
            except Exception as e:
                print(f"   {page}: Error - {e}")
        
        return True
    
    def test_functional_access(self):
        """Probar funcionalidades específicas"""
        print("\n[3] Probando funcionalidades...")
        
        # Probar el proceso de admisión que sabemos existe
        proceso_url = f"{self.target}/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=N"
        try:
            response = self.session.get(proceso_url)
            if response.status_code == 200:
                print("✅ Proceso de admisión accesible")
                
                # Buscar formularios funcionales
                if '<form' in response.text:
                    forms_count = response.text.count('<form')
                    print(f"   Formularios en la página: {forms_count}")
                    
                    # Extraer campos del formulario principal
                    import re
                    hidden_fields = re.findall(r'<input[^>]*type="hidden"[^>]*name="([^"]*)"[^>]*value="([^"]*)"', response.text)
                    if hidden_fields:
                        print("   Campos ocultos encontrados:")
                        for name, value in hidden_fields[:5]:  # Mostrar primeros 5
                            print(f"      {name} = {value}")
            else:
                print("❌ Proceso de admisión no accesible")
                
        except Exception as e:
            print(f"❌ Error probando proceso de admisión: {e}")
    
    def check_ajax_endpoints(self):
        """Verificar endpoints AJAX con sesión"""
        print("\n[4] Probando endpoints AJAX...")
        
        ajax_endpoints = [
            '/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato=1',
            '/jsp/escolar/muestra_bachillerato_ajax.jsp?xCveBachillerato=1'
        ]
        
        for endpoint in ajax_endpoints:
            try:
                response = self.session.get(urljoin(self.target, endpoint))
                if response.status_code == 200:
                    print(f"✅ {endpoint}: Accesible")
                    if len(response.text) > 0:
                        print(f"   Respuesta: {response.text[:100]}...")
                else:
                    print(f"❌ {endpoint}: HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ {endpoint}: Error - {e}")

# Ejecutar
verifier = AccessVerifier("http://189.254.143.102")
if verifier.verify_login_effectiveness():
    verifier.test_functional_access()
    verifier.check_ajax_endpoints()