# login_page_analysis.py
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def analyze_login_page():
    """Analiza la página de login real para entender su comportamiento"""
    print("=== ANÁLISIS DE PÁGINA DE LOGIN ===")
    
    base_url = "https://189.254.143.102"
    session = requests.Session()
    session.verify = False
    
    login_url = f"{base_url}/jsp/index.jsp"
    
    # Obtener la página de login
    response = session.get(login_url)
    print(f"📄 Página de login: Status {response.status_code}, Tamaño {len(response.text)} bytes")
    
    # Analizar el formulario de login
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')
    
    print(f"📋 Formularios encontrados: {len(forms)}")
    
    for i, form in enumerate(forms):
        print(f"\n--- Formulario {i+1} ---")
        print(f"Action: {form.get('action', 'No action')}")
        print(f"Method: {form.get('method', 'GET')}")
        
        # Encontrar todos los inputs
        inputs = form.find_all('input')
        print("Inputs encontrados:")
        for input_tag in inputs:
            name = input_tag.get('name', 'sin nombre')
            input_type = input_tag.get('type', 'text')
            value = input_tag.get('value', '')
            print(f"  📝 {name} (type: {input_type}, value: '{value}')")
    
    # Buscar mensajes de error o información
    if "error" in response.text.lower():
        print("🔍 Mensajes de error encontrados en la página")
    
    if "contraseña" in response.text.lower() or "password" in response.text.lower():
        print("🔍 Referencias a contraseña encontradas")
    
    # Verificar si hay algún mensaje de estado de login
    if "sesión" in response.text.lower() or "session" in response.text.lower():
        print("🔍 Referencias a sesión encontradas")

def test_login_behavior():
    """Prueba el comportamiento del login con credenciales incorrectas"""
    print("\n=== COMPORTAMIENTO DE LOGIN ===")
    
    base_url = "https://189.254.143.102"
    session = requests.Session()
    session.verify = False
    
    login_url = f"{base_url}/jsp/index.jsp"
    
    # Credenciales incorrectas para ver el comportamiento
    login_data = {
        "yAccion": "login",
        "yUsuario": "usuario_inexistente",
        "xUsuario": "usuario_inexistente", 
        "xContrasena": "contraseña_incorrecta",
        "yIntentos": "1"
    }
    
    response = session.post(login_url, data=login_data)
    print(f"📊 Respuesta a credenciales incorrectas:")
    print(f"   Status: {response.status_code}")
    print(f"   Tamaño: {len(response.text)} bytes")
    
    # Buscar mensajes de error específicos
    if "incorrecto" in response.text.lower() or "inválido" in response.text.lower():
        print("   ✅ Mensaje de error de login detectado")
    else:
        print("   ❌ No se detectó mensaje de error específico")
    
    # Comparar con la página de login normal
    normal_response = session.get(login_url)
    if len(response.text) == len(normal_response.text):
        print("   ⚠️  Mismo tamaño que página de login (posible redirección al login)")
    else:
        print("   🔍 Tamaño diferente (posible página de error o éxito)")

if __name__ == "__main__":
    analyze_login_page()
    test_login_behavior()