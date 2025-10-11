# Analizar EXACTAMENTE qué está pasando en las redirecciones
echo "=== ANÁLISIS DETALLADO DE REDIRECCIONES ==="

curl -k -v -L -b "JSESSIONID=00000000000000000000000000000000" \
     -d "usuario=test&contrasena=test" \
     "https://189.254.143.102/jsp/menu.jsp" 2>&1 | \
     grep -i "location\|set-cookie\|http/\|usuario\|contrase"

# Probar con diferentes user-agents (simular navegador real)
curl -k -v -L -A "Mozilla/5.0 (Windows NT 5.1; rv:10.0) Gecko/20100101 Firefox/10.0" \
     -b "JSESSIONID=00000000000000000000000000000000" \
     -d "usuario=jose&contrasena=garcia" \
     "https://189.254.143.102/jsp/menu.jsp" 2>&1 | \
     grep -i "location\|http/"
