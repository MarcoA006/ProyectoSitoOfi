import requests
import socket

class PortServiceAnalyzer:
    def __init__(self, host):
        self.host = host.replace('http://', '').replace('https://', '').split('/')[0]
    
    def analyze_services(self):
        """Analizar servicios en puertos abiertos"""
        print("[+] Analizando servicios...")
        
        ports = [80, 443, 8080, 8009, 8005, 8443]
        
        for port in ports:
            try:
                # Verificar si el puerto está abierto
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((self.host, port))
                sock.close()
                
                if result == 0:
                    print(f"\n📡 Puerto {port}: ABIERTO")
                    self.get_service_info(port)
                    
            except Exception as e:
                print(f"Error en puerto {port}: {e}")
    
    def get_service_info(self, port):
        """Obtener información del servicio"""
        try:
            if port == 80:
                response = requests.get(f"http://{self.host}:{port}", timeout=5)
                print(f"   Service: HTTP")
                print(f"   Server: {response.headers.get('Server', 'Unknown')}")
                print(f"   Title: {self.extract_title(response.text)}")
                
            elif port == 443:
                response = requests.get(f"https://{self.host}:{port}", timeout=5, verify=False)
                print(f"   Service: HTTPS")
                print(f"   Server: {response.headers.get('Server', 'Unknown')}")
                
            elif port == 8080:
                response = requests.get(f"http://{self.host}:{port}", timeout=5)
                print(f"   Service: HTTP (Alternate)")
                print(f"   Server: {response.headers.get('Server', 'Unknown')}")
                
            elif port == 8009:
                print(f"   Service: AJP (Apache JServ Protocol)")
                print(f"   Usado para comunicación entre Apache y Tomcat")
                
            elif port == 8005:
                print(f"   Service: Tomcat Shutdown Port")
                print(f"   ⚠️  Puerto de shutdown de Tomcat")
                
        except Exception as e:
            print(f"   Error obteniendo info: {e}")
    
    def extract_title(self, html):
        """Extraer título de HTML"""
        import re
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        return title_match.group(1) if title_match else "No title"

# Ejecutar
analyzer = PortServiceAnalyzer("189.254.143.102")
analyzer.analyze_services()