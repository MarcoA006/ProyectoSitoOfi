# ajax_data_extractor.py
import requests
import urllib3
import json
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AjaxDataExtractor:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        self.session.cookies.set('JSESSIONID', '3B0DDD39CD0068BB30ED28B8C75B2A38')
        
    def extract_all_bachilleratos(self):
        """Extrae todos los bachilleratos disponibles"""
        print("=== EXTRACCIÓN DE DATOS VÍA AJAX ===")
        
        endpoint = "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"
        
        print("[+] Extrayendo datos de bachilleratos...")
        
        bachilleratos = []
        
        # Probar un rango de IDs
        for i in range(1, 50):
            url = f"{self.base_url}{endpoint}?xCveBachillerato={i}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                content = response.text.strip()
                if content and "¬" in content:
                    parts = content.split("¬")
                    bachilleratos.append({
                        'id': parts[0],
                        'nombre': parts[1]
                    })
                    print(f"  ✅ {parts[0]} - {parts[1]}")
                elif content and content != "1¬INSTITUTO OCTAVIO PAZ":
                    print(f"  ⚠️  Respuesta diferente: '{content}'")
        
        # Guardar datos extraídos
        if bachilleratos:
            with open('bachilleratos_extracted.json', 'w', encoding='utf-8') as f:
                json.dump(bachilleratos, f, indent=2, ensure_ascii=False)
            print(f"💾 Guardados {len(bachilleratos)} bachilleratos en bachilleratos_extracted.json")
        
        return bachilleratos
    
    def find_other_ajax_endpoints(self):
        """Busca otros endpoints AJAX en la aplicación"""
        print("\n[+] Buscando otros endpoints AJAX...")
        
        # Obtener página principal para buscar llamadas AJAX
        main_url = f"{self.base_url}/jsp/escolar/proceso_admision/proceso_interesado.jsp"
        response = self.session.get(main_url)
        
        # Buscar patrones de URLs AJAX en el JavaScript
        ajax_patterns = [
            r'["\'](/[^"\']*ajax[^"\']*)["\']',
            r'["\'](/[^"\']*json[^"\']*)["\']',
            r'["\'](/[^"\']*data[^"\']*)["\']',
            r'["\'](/[^"\']*load[^"\']*)["\']',
            r'["\'](/[^"\']*get[^"\']*)["\']'
        ]
        
        for pattern in ajax_patterns:
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            if matches:
                for match in matches:
                    if '..' not in match and 'http' not in match:
                        print(f"  🔍 Posible endpoint AJAX: {match}")
                        
                        # Probar el endpoint
                        url = f"{self.base_url}{match}"
                        test_response = self.session.get(url)
                        if test_response.status_code == 200:
                            print(f"    ✅ Accesible - Tamaño: {len(test_response.text)} bytes")

# Ejecutar
if __name__ == "__main__":
    extractor = AjaxDataExtractor()
    extractor.extract_all_bachilleratos()
    extractor.find_other_ajax_endpoints()