import requests
from bs4 import BeautifulSoup
import re
import urllib3

# Desactivar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def analyze_script_content(script_url):
    """Analiza el contenido de un script externo"""
    try:
        response = requests.get(script_url, verify=False, timeout=10)
        content = response.text
        
        # Buscar patrones interesantes
        patterns = {
            'URLs': r'https?://[^\s<>"{}|\\^`\[\]]+',
            'IPs': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'Emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'Tokens': r'[A-Za-z0-9]{32,}',
            'API Keys': r'api[_-]?key[=:][A-Za-z0-9]+',
            'Passwords': r'password[=:][^&\s]+'
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"  [!] {pattern_name} encontrados: {matches[:3]}")  # Mostrar solo los primeros 3
                
    except Exception as e:
        print(f"  [-] Error analizando script: {e}")

def analyze_inline_script(content, script_num):
    """Analiza scripts inline"""
    try:
        if content and len(content) > 10:
            # Buscar variables interesantes
            interesting_vars = re.findall(r'var\s+(\w+)\s*=', content)
            if interesting_vars:
                print(f"  [Script {script_num}] Variables: {interesting_vars[:5]}")  # Mostrar solo 5 variables
            
            # Buscar funciones
            functions = re.findall(r'function\s+(\w+)\s*\(', content)
            if functions:
                print(f"  [Script {script_num}] Funciones: {functions[:5]}")
            
            # Buscar endpoints API
            endpoints = re.findall(r'fetch\([\'"]([^\'"]+)[\'"]\)|\.ajax\([^}]*url[\s:]*[\'"]([^\'"]+)[\'"]', content)
            if endpoints:
                print(f"  [Script {script_num}] Endpoints: {endpoints[:3]}")
                
    except Exception as e:
        print(f"  [-] Error en script inline: {e}")

def analyze_javascript(url):
    """Analiza archivos JavaScript en busca de información sensible"""
    try:
        response = requests.get(url, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar scripts
        scripts = soup.find_all('script')
        print(f"[*] Encontrados {len(scripts)} scripts en {url}")
        
        for i, script in enumerate(scripts):
            if script.get('src'):
                script_url = script['src']
                if not script_url.startswith('http'):
                    # Construir URL completa
                    base_url = '/'.join(url.split('/')[:3])
                    if script_url.startswith('/'):
                        script_url = f"{base_url}{script_url}"
                    else:
                        script_url = f"{base_url}/{script_url}"
                
                print(f"[*] Analizando script externo: {script_url}")
                analyze_script_content(script_url)
            else:
                # Script inline
                if script.string:
                    print(f"[*] Analizando script inline #{i+1}")
                    analyze_inline_script(script.string, i+1)
                    
    except Exception as e:
        print(f"[-] Error analizando la página: {e}")

def search_sensitive_info_in_js(url):
    """Búsqueda más profunda de información sensible"""
    try:
        response = requests.get(url, verify=False, timeout=10)
        
        # Patrones para información sensible
        sensitive_patterns = {
            'Claves API': r'api[_-]?key["\']?\\s*[:=]\\s*["\']?([A-Za-z0-9]{20,40})["\']?',
            'Tokens': r'["\']?token["\']?\\s*[:=]\\s*["\']?([A-Za-z0-9]{32,})["\']?',
            'Contraseñas': r'["\']?password["\']?\\s*[:=]\\s*["\']?([^"\'\\s]+)["\']?',
            'Usuarios': r'["\']?username["\']?\\s*[:=]\\s*["\']?([^"\'\\s]+)["\']?',
            'Correos': r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b',
            'IPs': r'\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b',
            'URLs internas': r'["\']/(api|admin|login|config|database)[^"\'\\s]*["\']'
        }
        
        print(f"[*] Buscando información sensible en: {url}")
        
        for pattern_name, pattern in sensitive_patterns.items():
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            if matches:
                print(f"[!] {pattern_name} encontrados:")
                for match in matches[:5]:  # Mostrar solo los primeros 5
                    print(f"    - {match}")
                    
    except Exception as e:
        print(f"[-] Error en búsqueda sensible: {e}")

# Función principal mejorada
def main():
    target_ip = "189.254.143.102"
    base_url = f"http://{target_ip}"
    
    print("=== ANÁLISIS DE JAVASCRIPT ===")
    
    # Análisis básico
    analyze_javascript(base_url)
    
    print("\n=== BÚSQUEDA DE INFORMACIÓN SENSIBLE ===")
    
    # Búsqueda de información sensible
    search_sensitive_info_in_js(base_url)
    
    # Probar también el manager si es accesible
    manager_url = f"{base_url}/manager"
    print(f"\n[*] Probando manager: {manager_url}")
    analyze_javascript(manager_url)

if __name__ == "__main__":
    main()