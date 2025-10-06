#!/usr/bin/env python3
import socket

def test_ajp_connection(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((host, port))
        print(f"[+] Conexión AJP exitosa a {host}:{port}")
        
        # Enviar ping AJP básico
        ping_data = b'\x12\x34\x00\x01\x0a'
        sock.send(ping_data)
        
        response = sock.recv(1024)
        print(f"[+] Respuesta recibida: {response.hex()}")
        
        sock.close()
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

# Probar conexión
test_ajp_connection("189.254.143.102", 8009)