# js_vulnerability_scanner.py
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class JSVulnerabilityScanner:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        
    def scan_js_files(self):
        """Escanea archivos JavaScript en busca de vulnerabilidades"""
        print("=== ESCANEO DE VULNERABILIDADES EN JS ===")
        
        js_files = [
            "/javascript/utilities.js",
            "/javascript/scriptAnimaciones.js",
            "/javascript/jquery/jquery-1.5.1.min.js",
            "/javascript/jquery/jquery-ui-1.8.2.min.js"
        ]
        
        for js_file in js_files:
            print(f"\n[+] Analizando: {js_file}")
            url = f"{self.base_url}{js_file}"
            
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    content = response.text
                    
                    # Buscar vulnerabilidades específicas
                    self.find_hardcoded_credentials(content, js_file)
                    self.find_api_endpoints(content, js_file)
                    self.find_sql_queries(content, js_file)
                    self.find_config_data(content, js_file)
                    self.find_debug_functions(content, js_file)
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
    
    def find_hardcoded_credentials(self, content, filename):
        """Busca credenciales hardcodeadas"""
        print("  🔍 Buscando credenciales hardcodeadas...")
        
        patterns = {
            'passwords': r'password\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
            'users': r'username\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
            'api_keys': r'api[_-]?key\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
            'tokens': r'token\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"    ✅ {pattern_name.upper()} encontrado:")
                for match in matches:
                    if len(match) > 3:  # Filtrar valores muy cortos
                        print(f"      • {match}")
    
    def find_api_endpoints(self, content, filename):
        """Busca endpoints API"""
        print("  🔍 Buscando endpoints API...")
        
        patterns = [
            r'["\'](/[^"\']*ajax[^"\']*)["\']',
            r'["\'](/[^"\']*api[^"\']*)["\']',
            r'["\'](/[^"\']*json[^"\']*)["\']',
            r'["\'](/[^"\']*data[^"\']*)["\']',
            r'["\'](/[^"\']*get[^"\']*)["\']',
            r'["\'](/[^"\']*post[^"\']*)["\']'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                for match in matches:
                    if '..' not in match and 'http' not in match:
                        print(f"    ✅ Endpoint encontrado: {match}")
    
    def find_sql_queries(self, content, filename):
        """Busca consultas SQL"""
        print("  🔍 Buscando consultas SQL...")
        
        patterns = [
            r'SELECT.*FROM',
            r'INSERT INTO',
            r'UPDATE.*SET',
            r'DELETE FROM',
            r'WHERE.*='
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"    ✅ Consulta SQL encontrada:")
                for match in matches[:2]:  # Mostrar solo las primeras
                    print(f"      • {match[:100]}...")
    
    def find_config_data(self, content, filename):
        """Busca datos de configuración"""
        print("  🔍 Buscando datos de configuración...")
        
        patterns = {
            'database_urls': r'jdbc:mysql://([^\'"]+)',
            'hosts': r'host\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
            'ports': r'port\s*[:=]\s*[\'"]([^\'"]+)[\'"]',
            'database_names': r'database\s*[:=]\s*[\'"]([^\'"]+)[\'"]'
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"    ✅ {pattern_name.replace('_', ' ').title()}:")
                for match in matches:
                    print(f"      • {match}")
    
    def find_debug_functions(self, content, filename):
        """Busca funciones de debug"""
        print("  🔍 Buscando funciones de debug...")
        
        debug_patterns = [
            r'console\.log',
            r'alert\(',
            r'debugger',
            r'var_dump',
            r'print_r'
        ]
        
        for pattern in debug_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"    ⚠️  Función de debug encontrada: {pattern}")

# Ejecutar
if __name__ == "__main__":
    scanner = JSVulnerabilityScanner()
    scanner.scan_js_files()