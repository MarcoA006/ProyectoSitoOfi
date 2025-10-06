import requests
from urllib.parse import urljoin

class RealPathEnumerator:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
    
    def enumerate_real_paths(self):
        """Enumerar rutas que realmente existen"""
        print("=== ENUMERACIÓN DE RUTAS REALES ===")
        
        # Rutas basadas en lo que sabemos que existe
        known_paths = [
            '/jsp/index.jsp',
            '/jsp/cerrar_sesion.jsp',
            '/jsp/escolar/proceso_admision/proceso_interesado.jsp',
            '/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp',
            '/jsp/escolar/muestra_bachillerato_ajax.jsp',
            '/examples/jsp/include/include.jsp',
            '/examples/jsp/cal/cal2.jsp',
            '/examples/jsp/snp/snoop.jsp'
        ]
        
        print("[+] Verificando rutas conocidas...")
        for path in known_paths:
            try:
                response = self.session.get(urljoin(self.target, path))
                print(f"   {path:60} -> HTTP {response.status_code} - {len(response.text)} bytes")
            except Exception as e:
                print(f"   {path:60} -> Error: {e}")
        
        # Buscar patrones comunes
        print("\n[+] Buscando patrones comunes...")
        patterns = [
            '/jsp/{}/index.jsp',
            '/jsp/{}/{}.jsp',
            '/{}/index.jsp',
            '/{}.jsp'
        ]
        
        common_names = ['admin', 'login', 'logout', 'user', 'users', 'config', 
                       'database', 'report', 'reports', 'panel', 'dashboard']
        
        for pattern in patterns:
            for name in common_names:
                path = pattern.format(name)
                try:
                    response = self.session.head(urljoin(self.target, path), timeout=3)
                    if response.status_code == 200:
                        print(f"   ✅ ENCONTRADO: {path}")
                except:
                    pass

# Ejecutar
enumerator = RealPathEnumerator("http://189.254.143.102")
enumerator.enumerate_real_paths()