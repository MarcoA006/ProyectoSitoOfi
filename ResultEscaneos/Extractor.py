#!/usr/bin/env python3
# analiza_reporte.py
# Uso: python3 analiza_reporte.py ReporteMaestro.txt
import re, sys, csv
from pathlib import Path

if len(sys.argv) < 2:
    print("Uso: python3 analiza_reporte.py ReporteMaestro.txt")
    sys.exit(1)

fpath = Path(sys.argv[1])
if not fpath.exists():
    print("No existe:", fpath)
    sys.exit(1)

txt = fpath.read_text(encoding='utf-8', errors='ignore')

# patrones
ips = set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', txt))
urls = set(re.findall(r'https?://[^\s\'"]+', txt))
emails = set(re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', txt))
jsession = set(re.findall(r'JSESSIONID[\'"]?\s*[:=]?\s*[\'"]?([A-Fa-f0-9]{16,})', txt))
paths = set(re.findall(r'/(?:[A-Za-z0-9_\-./]+/?)+', txt))

# filtrar paths comunes muy largos/ruido
interesting_paths = {p for p in paths if len(p) < 150 and (p.count('/')<=6 or any(k in p.lower() for k in ['manager','examples','docs','jsp','tomcat']))}

out = Path("reporte_extracted.csv")
with out.open("w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["type","value"])
    for i in sorted(ips):
        writer.writerow(["ip", i])
    for u in sorted(urls):
        writer.writerow(["url", u])
    for e in sorted(emails):
        writer.writerow(["email", e])
    for s in sorted(jsession):
        writer.writerow(["jsessionid", s])
    for p in sorted(interesting_paths):
        writer.writerow(["path", p])

print("Extracción completada. Resultados en:", out)
print(f"IPs: {len(ips)}, URLs: {len(urls)}, emails: {len(emails)}, paths interesantes: {len(interesting_paths)}")
