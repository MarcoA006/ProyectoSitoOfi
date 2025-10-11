#!/usr/bin/env python3
import requests
import urllib3
urllib3.disable_warnings()

def analyze_login_structure():
    target = "https://189.254.143.102/jsp/menu.jsp"
    
    print("=== ANALIZANDO ESTRUCTURA REAL DEL LOGIN ===")
    
    # Primero obtener la página sin enviar datos
    session = requests.Session()
    r = session.get(target, verify=False)
    
    print(f"Status Code (GET): {r.status_code}")
    print(f"Tamaño: {len(r.text)}")
    print(f"URL: {r.url}")
    
    # Buscar formularios en la página
    if '<form' in r.text:
        forms = r.text.split('<form')
        for i, form in enumerate(forms[1:], 1):
            print(f"\n--- Formulario {i} ---")
            form_lines = form.split('>')[0:10]
            for line in form_lines:
                if 'name=' in line or 'id=' in line or 'action=' in line:
                    print(f"  {line.strip()}")
    
    # Buscar campos de entrada específicos
    input_fields = []
    for line in r.text.split('\n'):
        if 'input' in line.lower() and 'name=' in line.lower():
            input_fields.append(line.strip())
    
    if input_fields:
        print(f"\nCampos de entrada encontrados ({len(input_fields)}):")
        for field in input_fields[:5]:
            print(f"  {field}")
    
    # Guardar la página para análisis manual
    with open('login_page_analysis.html', 'w', encoding='utf-8') as f:
        f.write(r.text)
    
    print(f"\n✅ Página guardada en: login_page_analysis.html")

if __name__ == "__main__":
    analyze_login_structure()
