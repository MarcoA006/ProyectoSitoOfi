import requests
import re
import sys
from urllib.parse import urljoin, urlparse
import urllib3

# Desactivar warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SITOEnumerator:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.found_endpoints = []
    
    def enumerate_application(self):
        """Enumerar toda la aplicación SITO"""
        print("=== ENUMERACIÓN DETALLADA APLICACIÓN SITO ===")
        print(f"Objetivo: {self.target}\n")
        
        try:
            # 1. Obtener página principal
            print("[1] Analizando página principal...")
            main_page = self.session.get(f"{self.target}/jsp/index.jsp", timeout=10, verify=False)
            
            if main_page.status_code == 200:
                print(f"✅ Página principal accesible: {len(main_page.text)} bytes")
                self.analyze_main_page(main_page.text)
            else:
                print(f"❌ No se puede acceder a la página principal: HTTP {main_page.status_code}")
                # Intentar con la raíz
                main_page = self.session.get(self.target, timeout=10, verify=False)
                if main_page.status_code == 200:
                    print(f"✅ Página raíz accesible: {len(main_page.text)} bytes")
                    self.analyze_main_page(main_page.text)
            
            # 2. Buscar archivos comunes
            print("\n[2] Buscando archivos y directorios comunes...")
            self.find_common_files()
            
            # 3. Enumerar rutas JSP
            print("\n[3] Enumerando rutas JSP...")
            self.enumerate_jsp_paths()
            
            # 4. Analizar JavaScript
            print("\n[4] Analizando archivos JavaScript...")
            self.analyze_javascript_files()
            
            # 5. Buscar parámetros ocultos
            print("\n[5] Buscando parámetros ocultos...")
            self.find_hidden_parameters()
            
            # 6. Generar reporte
            self.generate_report()
            
        except Exception as e:
            print(f"❌ Error durante la enumeración: {e}")
    
    def analyze_main_page(self, html_content):
        """Analizar la página principal"""
        # Extraer todos los enlaces
        links = re.findall(r'href=[\'"]([^\'"]*)[\'"]', html_content, re.IGNORECASE)
        scripts = re.findall(r'src=[\'"]([^\'"]*)[\'"]', html_content, re.IGNORECASE)
        forms = re.findall(r'<form[^>]*>', html_content, re.IGNORECASE)
        
        print(f"📎 Enlaces encontrados: {len(links)}")
        print(f"📜 Scripts encontrados: {len(scripts)}")
        print(f"📋 Formularios encontrados: {len(forms)}")
        
        # Filtrar y mostrar enlaces interesantes
        interesting_links = []
        for link in links:
            if any(x in link.lower() for x in ['.jsp', 'admin', 'config', 'login', 'database', 'ajax']):
                interesting_links.append(link)
        
        if interesting_links:
            print("\n🔍 Enlaces interesantes:")
            for link in interesting_links[:10]:  # Mostrar solo los primeros 10
                print(f"   {link}")
        
        # Guardar enlaces para posterior análisis
        self.found_endpoints.extend(interesting_links)
        
        # Analizar formularios
        if forms:
            print("\n📋 Formularios encontrados:")
            for form in forms[:3]:  # Mostrar primeros 3 formularios
                # Extraer acción del formulario
                action_match = re.search(r'action=[\'"]([^\'"]*)[\'"]', form, re.IGNORECASE)
                action = action_match.group(1) if action_match else 'N/A'
                print(f"   Action: {action}")
                
                # Extraer campos ocultos
                hidden_fields = re.findall(r'<input[^>]*type=[\'"]hidden[\'"][^>]*>', form, re.IGNORECASE)
                for field in hidden_fields:
                    name_match = re.search(r'name=[\'"]([^\'"]*)[\'"]', field)
                    value_match = re.search(r'value=[\'"]([^\'"]*)[\'"]', field)
                    if name_match:
                        name = name_match.group(1)
                        value = value_match.group(1) if value_match else 'N/A'
                        print(f"     Campo oculto: {name} = {value}")
    
    def find_common_files(self):
        """Buscar archivos y directorios comunes"""
        common_paths = [
            # Archivos de configuración
            '/WEB-INF/web.xml', '/META-INF/context.xml',
            '/config.xml', '/configuration.xml',
            
            # Directorios importantes
            '/admin/', '/administrator/', '/webadmin/',
            '/config/', '/database/', '/db/',
            '/backup/', '/logs/', '/temp/',
            
            # Archivos de datos
            '/data.sql', '/database.sql', '/backup.sql',
            '/users.xml', '/config.ini', '.env',
            
            # Rutas de la aplicación SITO
            '/jsp/admin/', '/jsp/config/', '/jsp/database/',
            '/jsp/reports/', '/jsp/export/'
        ]
        
        found_files = []
        
        for path in common_paths:
            try:
                url = urljoin(self.target, path)
                response = self.session.head(url, timeout=5, verify=False)
                
                if response.status_code == 200:
                    found_files.append(path)
                    print(f"✅ Archivo/directorio encontrado: {path}")
                    
                # Para algunos paths, hacer GET para verificar contenido
                elif response.status_code in [403, 401]:
                    print(f"⚠️  Acceso restringido: {path} (HTTP {response.status_code})")
                    
            except Exception as e:
                continue
        
        return found_files
    
    def enumerate_jsp_paths(self):
        """Enumerar rutas JSP específicas"""
        jsp_paths = [
            '/jsp/login.jsp', '/jsp/logout.jsp', '/jsp/register.jsp',
            '/jsp/admin/index.jsp', '/jsp/admin/users.jsp',
            '/jsp/admin/config.jsp', '/jsp/admin/database.jsp',
            '/jsp/escolar/proceso_admision/proceso_interesado.jsp',
            '/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp',
            '/jsp/escolar/muestra_bachillerato_ajax.jsp',
            '/jsp/cerrar_sesion.jsp', '/jsp/menu_principal.jsp',
            '/jsp/error.jsp', '/jsp/404.jsp'
        ]
        
        accessible_jsp = []
        
        for jsp_path in jsp_paths:
            try:
                url = urljoin(self.target, jsp_path)
                response = self.session.get(url, timeout=5, verify=False)
                
                if response.status_code == 200:
                    accessible_jsp.append(jsp_path)
                    print(f"✅ JSP accesible: {jsp_path} ({len(response.text)} bytes)")
                    
                    # Verificar si es la página de login o admin
                    if 'login' in jsp_path.lower() and any(x in response.text.lower() for x in ['password', 'usuario', 'user']):
                        print("   🔐 Posible página de login")
                    
                    elif 'admin' in jsp_path.lower():
                        print("   ⚠️  Página administrativa")
                        
                elif response.status_code == 403:
                    print(f"🔒 JSP protegido: {jsp_path}")
                    
            except Exception as e:
                print(f"❌ Error accediendo a {jsp_path}: {e}")
        
        return accessible_jsp
    
    def analyze_javascript_files(self):
        """Analizar archivos JavaScript en busca de información sensible"""
        js_paths = [
            '/javascript/utilities.js',
            '/js/main.js', '/js/app.js', '/js/config.js',
            '/javascript/jquery/jquery-1.5.1.min.js',
            '/javascript/jquery/jquery-ui-1.8.2.min.js',
            '/javascript/scriptAnimaciones.js'
        ]
        
        for js_path in js_paths:
            try:
                url = urljoin(self.target, js_path)
                response = self.session.get(url, timeout=5, verify=False)
                
                if response.status_code == 200:
                    print(f"\n📜 Analizando: {js_path}")
                    self.scan_js_for_secrets(response.text, js_path)
                    
            except Exception as e:
                continue
    
    def scan_js_for_secrets(self, js_content, filename):
        """Buscar información sensible en JavaScript"""
        patterns = {
            'URLs de API': r'["\'](https?://[^"\']+\.(php|jsp|do|action)[^"\']*)["\']',
            'Endpoints AJAX': r'["\'](/[^"\']*ajax[^"\']*)["\']',
            'Credenciales de BD': r'(user|username|pass|password|database|host|port)[\s:=]+["\']([^"\']+)["\']',
            'Tokens': r'(token|key|secret)[\s:=]+["\']([A-Za-z0-9]{10,})["\']',
            'Emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'IPs': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'Configuraciones': r'(url|host|port|database)[\s:=]+["\']([^"\']+)["\']'
        }
        
        found_items = {}
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, js_content, re.IGNORECASE)
            if matches:
                found_items[pattern_name] = matches
                print(f"   🔍 {pattern_name}:")
                for match in matches[:2]:  # Mostrar solo 2 resultados
                    if isinstance(match, tuple):
                        print(f"      {match}")
                    else:
                        print(f"      {match}")
        
        if found_items:
            # Guardar análisis
            with open(f"js_analysis_{filename.replace('/', '_')}.txt", 'w', encoding='utf-8') as f:
                f.write(f"Análisis de: {filename}\n")
                for pattern_name, matches in found_items.items():
                    f.write(f"\n{pattern_name}:\n")
                    for match in matches:
                        f.write(f"  {match}\n")
    
    def find_hidden_parameters(self):
        """Buscar parámetros ocultos en formularios JSP"""
        print("\n[5] Buscando parámetros ocultos en formularios...")
        
        jsp_pages = [
            '/jsp/index.jsp',
            '/jsp/escolar/proceso_admision/proceso_interesado.jsp'
        ]
        
        for jsp_page in jsp_pages:
            try:
                url = urljoin(self.target, jsp_page)
                response = self.session.get(url, timeout=8, verify=False)
                
                if response.status_code == 200:
                    # Buscar todos los inputs hidden
                    hidden_inputs = re.findall(r'<input[^>]*type=[\'"]hidden[\'"][^>]*>', response.text, re.IGNORECASE)
                    
                    if hidden_inputs:
                        print(f"\n📋 Parámetros ocultos en {jsp_page}:")
                        for input_tag in hidden_inputs:
                            name_match = re.search(r'name=[\'"]([^\'"]*)[\'"]', input_tag)
                            value_match = re.search(r'value=[\'"]([^\'"]*)[\'"]', input_tag)
                            
                            if name_match:
                                name = name_match.group(1)
                                value = value_match.group(1) if value_match else 'N/A'
                                print(f"   🔒 {name} = {value}")
                
            except Exception as e:
                print(f"❌ Error analizando {jsp_page}: {e}")
    
    def generate_report(self):
        """Generar reporte final"""
        print("\n" + "="*60)
        print("REPORTE FINAL DE ENUMERACIÓN")
        print("="*60)
        
        # Aquí iría un resumen de todo lo encontrado
        print("\n✅ Enumeración completada")
        print("📊 Revisa los archivos guardados para más detalles")

def main():
    if len(sys.argv) != 2:
        print("Uso: python sito_enumerator.py http://189.254.143.102")
        sys.exit(1)
    
    target = sys.argv[1]
    enumerator = SITOEnumerator(target)
    enumerator.enumerate_application()

if __name__ == "__main__":
    main()