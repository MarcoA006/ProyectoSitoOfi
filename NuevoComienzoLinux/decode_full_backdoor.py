import re

p = "aRfguQwJvbc#h l)[W2jkm/op?N!rVisGq=@tB3O4CdeF9n0U(HI_6X]KLM>,DE.-Pxyz15YZ<78AST"
l = "gJvbUWc#,Dh5w*sGq=@tB[!39nO4CuYdeF0a]Kl)iQxZ<7yf2jkSTrVm/oR-Pp?NI_6XLM>E.z18A(H"

def decode(encoded):
    reversed_str = encoded[::-1]
    decoded = ""
    for char in reversed_str:
        if char in l:
            index = l.index(char)
            decoded += p[index]
        else:
            decoded += char
    return decoded

# Cadenas adicionales críticas del backdoor
critical_strings = [
    "9]]w",  # URL del servidor
    "by9N3y3]!rf7@!fl8b[Y!dUNBhgwdZbg[YNfl8b[Y!!",  # Posible URL/credencial
    "by9NCgCdY!ll8@!>fib[Y!dUNBhgwdZbg[YN>fib[Y!!",
    "by9N3tygUt!ii8>!@l8b[Y!dUNBhgwdZbg[YN@l8b[Y!!", 
    "by9NsZXygx!18rM!@M8b[Y!dUNBhgwdZbg[YN@M8b[Y!!",
    "whygJ9(*I*9dsXyxa*I*-D!z9(*sZXygp-Dz*HQ(S*I*fMf@*]wbYCX93h"  # Mensaje copyright
]

print("=== DECODIFICACIÓN COMPLETA DEL BACKDOOR ===")
for encoded in critical_strings:
    try:
        decoded = decode(encoded)
        print(f"Codificado: {encoded}")
        print(f"Decodificado: {decoded}")
        print("---")
    except Exception as e:
        print(f"Error: {e}")

# Buscar patrones de URLs y credenciales
print("=== BUSCANDO PATRONES ===")
for encoded in critical_strings:
    decoded = decode(encoded)
    if "http" in decoded.lower() or "www" in decoded.lower() or "@" in decoded:
        print(f"POSIBLE URL/EMAIL: {decoded}")
    if "pass" in decoded.lower() or "user" in decoded.lower() or "admin" in decoded.lower():
        print(f"POSIBLE CREDENCIAL: {decoded}")
