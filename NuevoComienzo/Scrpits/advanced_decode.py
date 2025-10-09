#!/usr/bin/env python3
import re
import base64
import binascii

def analyze_backdoor(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    
    print("=== ANÁLISIS AVANZADO DEL BACKDOOR ===")
    
    # Buscar patrones Base64
    base64_patterns = re.findall(b'[A-Za-z0-9+/]{20,}={0,2}', content)
    for pattern in base64_patterns[:10]:  # Mostrar solo primeros 10
        try:
            decoded = base64.b64decode(pattern).decode('utf-8', errors='ignore')
            if len(decoded) > 3 and any(c.isalpha() for c in decoded):
                print(f"Base64: {pattern.decode()} -> {decoded}")
        except:
            pass
    
    # Buscar patrones Hex
    hex_patterns = re.findall(b'(?:\\\\x[0-9a-f]{2})+', content)
    for pattern in hex_patterns[:10]:
        try:
            hex_str = pattern.replace(b'\\\\x', b'')
            decoded = binascii.unhexlify(hex_str).decode('utf-8', errors='ignore')
            if len(decoded) > 3:
                print(f"Hex: {pattern.decode()} -> {decoded}")
        except:
            pass
    
    # Buscar URLs ocultas
    url_patterns = re.findall(b'https?://[^\\s"\\']+', content)
    for url in url_patterns:
        print(f"URL encontrada: {url.decode()}")
    
    # Buscar rutas de archivos
    path_patterns = re.findall(b'/[a-zA-Z0-9_/\\.-]+\\.(?:jsp|html|xml|properties|conf)', content)
    for path in set(path_patterns):  # Remover duplicados
        print(f"Ruta encontrada: {path.decode()}")

if __name__ == "__main__":
    analyze_backdoor('backdoor_analysis.js')
