# Probar diferentes endpoints del manager con la sesión
JSESSION="00000000000000000000000000000000"
TARGET="https://189.254.143.102"

echo "=== TESTING MANAGER ENDPOINTS ==="

curl -k -b "JSESSIONID=$JSESSION" "$TARGET/manager/html" > manager_test.html
echo "Manager HTML: $? (0=éxito)"

curl -k -b "JSESSIONID=$JSESSION" "$TARGET/manager/list" > manager_list.txt
echo "Manager List: $? (0=éxito)"

curl -k -b "JSESSIONID=$JSESSION" "$TARGET/manager/status" > manager_status.txt
echo "Manager Status: $? (0=éxito)"

# Verificar respuestas
for file in manager_*.txt manager_*.html; do
    if [[ -s "$file" ]]; then
        echo "--- $file tiene contenido ---"
        head -5 "$file"
    fi
done
