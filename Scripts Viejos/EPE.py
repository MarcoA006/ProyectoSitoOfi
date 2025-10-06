import socket
import requests

class PortScanner:
    def __init__(self, host):
        self.host = host.replace('http://', '').replace('https://', '').split('/')[0]
    
    def scan_ports(self):
        """Escanear puertos específicos de Tomcat"""
        ports = [80, 443, 8080, 8009, 8005, 8443, 8081, 8090, 8088, 8888]
        
        print(f"[+] Escaneando puertos en {self.host}...")
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.host, port))
                sock.close()
                
                if result == 0:
                    print(f"Puerto {port}: ABIERTO")
                    self.get_service_banner(port)
                else:
                    print(f"Puerto {port}: cerrado")
                    
            except Exception as e:
                print(f"Puerto {port}: error - {e}")
    
    def get_service_banner(self, port):
        """Obtener banner del servicio"""
        try:
            if port == 80 or port == 8080:
                response = requests.get(f"http://{self.host}:{port}", timeout=5)
                server = response.headers.get('Server', 'Desconocido')
                print(f"  Servidor: {server}")
                
        except Exception as e:
            print(f"  Error obteniendo banner: {e}")

# Escanear
scanner = PortScanner("189.254.143.102")
scanner.scan_ports()