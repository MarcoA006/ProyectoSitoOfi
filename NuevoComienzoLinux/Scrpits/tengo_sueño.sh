# Analizar la página de acceso denegado que aparece en TODAS las redirecciones
echo "=== ANALIZANDO ACCESO_DENEGADO.JSP ==="

curl -k "https://189.254.143.102/jsp/acceso_denegado.jsp" -o acceso_denegado_analysis.html

# Buscar información útil en la página de denegación
grep -i "mensaje\|error\|intento\|valid\|credencial\|usuario\|contrase" acceso_denegado_analysis.html

# Verificar si hay diferencias entre sesiones
curl -k -b "JSESSIONID=00000000000000000000000000000000" \
     "https://189.254.143.102/jsp/acceso_denegado.jsp" -o acceso_denegado_sesion.html

diff acceso_denegado_analysis.html acceso_denegado_sesion.html && echo "✅ Mismo contenido con sesión"
