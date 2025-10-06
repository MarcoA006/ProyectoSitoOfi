import os
from bs4 import BeautifulSoup
import re

class ResponseAnalyzer:
    def __init__(self):
        self.responses_dir = "."

    def analyze_all_responses(self):
        """Analiza todas las respuestas HTML guardadas"""
        print("[*] Analizando respuestas guardadas...")
        
        html_files = [f for f in os.listdir(self.responses_dir) if f.endswith('.html')]
        
        for file in html_files:
            print(f"\n[+] Analizando: {file}")
            
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # Buscar información sensible
                self.search_sensitive_info(content, file)
                
                # Buscar diferencias entre respuestas
                if "mysql_info" in file:
                    self.analyze_mysql_response(content, file)
                    
            except Exception as e:
                print(f"    [-] Error analizando {file}: {e}")

    def search_sensitive_info(self, content, filename):
        """Busca información sensible en el contenido"""
        patterns = {
            'Emails': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'Database Keywords': r'\b(mysql|database|schema|table|user|password)\b',
            'SQL Keywords': r'\b(SELECT|INSERT|UPDATE|DELETE|UNION|FROM|WHERE)\b',
            'IP Addresses': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'File Paths': r'[cC]:\\[^\\]+\\[^\\]+|/[^/]+/[^/]+',
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                unique_matches = list(set(matches))
                print(f"    [!] {pattern_name} encontrados: {unique_matches[:3]}")

    def analyze_mysql_response(self, content, filename):
        """Analiza respuestas de MySQL específicamente"""
        print("    [MySQL] Buscando datos inyectados...")
        
        # Buscar datos que parezcan resultados de consultas
        suspicious_data = re.findall(r'<[^>]*>([A-Za-z0-9_]{3,20})</[^>]*>', content)
        
        # Filtrar datos normales vs inyectados
        normal_texts = ['Solicita', 'Ficha', 'Admisión', 'admin', 'UNION', 'SELECT']
        injected_data = [data for data in suspicious_data if data not in normal_texts]
        
        if injected_data:
            print(f"    [!] Posibles datos inyectados: {list(set(injected_data))[:5]}")

# Analizar respuestas
print("=== ANÁLISIS DE RESPUESTAS GUARDADAS ===")
analyzer = ResponseAnalyzer()
analyzer.analyze_all_responses()