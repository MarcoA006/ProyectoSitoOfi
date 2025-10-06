import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class JSPIndexExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def analyze_index_jsp(self):
        """Analiza /jsp/index.jsp encontrado"""
        print("[*] Analizando /jsp/index.jsp...")
        
        try:
            url = f"{self.base_url}/jsp/index.jsp"
            response = self.session.get(url, timeout=10)
            
            print(f"[+] Status: {response.status_code}")
            print(f"[+] Tamaño: {len(response.text)} bytes")
            
            # Buscar redirecciones o contenido interesante
            if response.status_code == 200:
                if "login" in response.text.lower():
                    print("[!] Parece ser una página de login")
                if "bienvenido" in response.text.lower():
                    print("[!] Parece ser una página de dashboard")
                
                # Guardar para análisis
                with open("index_jsp_analysis.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                print("[+] Página guardada en index_jsp_analysis.html")
            
            # Verificar si es la página principal real
            main_page_response = self.session.get(self.base_url, timeout=5)
            if response.text == main_page_response.text:
                print("[!] /jsp/index.jsp es la página principal")
            else:
                print("[+] /jsp/index.jsp es diferente de la página principal")
                
        except Exception as e:
            print(f"[-] Error analizando index.jsp: {e}")

    def discover_admin_pages(self):
        """Descubre páginas de administración"""
        print("\n[*] Buscando páginas de administración...")
        
        admin_paths = [
            "/jsp/admin/", "/jsp/administracion/", "/jsp/manager/",
            "/jsp/system/", "/jsp/config/", "/jsp/database/",
            "/jsp/reports/", "/jsp/backup/", "/jsp/users/",
            "/admin/", "/administrator/", "/manager/", "/webadmin/"
        ]
        
        for path in admin_paths:
            try:
                url = f"{self.base_url}{path}"
                response = self.session.get(url, timeout=3)
                
                if response.status_code == 200:
                    print(f"[!] ¡Página de admin encontrada: {path}")
                elif response.status_code == 403:
                    print(f"[+] Acceso prohibido: {path}")
                elif response.status_code == 301 or response.status_code == 302:
                    print(f"[+] Redirección: {path}")
                    
            except:
                pass

    def brute_force_jsp_directories(self):
        """Fuerza bruta de directorios JSP"""
        print("\n[*] Fuerza bruta de directorios JSP...")
        
        jsp_dirs = [
            "escolar", "admin", "usuario", "config", "system",
            "reportes", "consultas", "mantenimiento", "seguridad",
            "academico", "financiero", "biblioteca", "laboratorio"
        ]
        
        for directory in jsp_dirs:
            # Probar diferentes patrones
            patterns = [
                f"/jsp/{directory}/",
                f"/jsp/{directory}/index.jsp",
                f"/{directory}/",
                f"/{directory}/index.jsp"
            ]
            
            for pattern in patterns:
                try:
                    url = f"{self.base_url}{pattern}"
                    response = self.session.get(url, timeout=3)
                    
                    if response.status_code == 200:
                        print(f"[!] ¡Directorio encontrado: {pattern}")
                    elif response.status_code == 403:
                        print(f"[+] Acceso denegado: {pattern}")
                        
                except:
                    pass

# Ejecutar análisis JSP
jsp_exploiter = JSPIndexExploiter("189.254.143.102")
jsp_exploiter.analyze_index_jsp()
jsp_exploiter.discover_admin_pages()
jsp_exploiter.brute_force_jsp_directories()