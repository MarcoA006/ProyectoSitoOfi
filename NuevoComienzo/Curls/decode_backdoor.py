import re

# Las cadenas de codificación del backdoor
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

# Probar con algunas cadenas codificadas del backdoor
test_strings = [
    ")HS(*39YUF?",
    "gYhCge*3y3H*Zd3#",
    "3]hZX3C_*Zx*CZxYo*PC3xgss3CCgdZp",
    "whygJ9(*I*9dsXyxa*I*-D!z9(*sZXygp-Dz*HQ(S*I*fMf@*]wbYCX93h"
]

print("=== DECODIFICACIÓN DEL BACKDOOR ===")
for encoded in test_strings:
    try:
        decoded = decode(encoded)
        print(f"Codificado: {encoded}")
        print(f"Decodificado: {decoded}")
        print("---")
    except Exception as e:
        print(f"Error decodificando {encoded}: {e}")
