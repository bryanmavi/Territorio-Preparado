"""Cruza los daños reales del sismo del 10-ago-2026 con las comunas y barrios de Cali.

Salidas en prototipo/datos/procesados/:
  danos_puntos_cali.csv      cada edificio o sede con daño, con su comuna y barrio
  afectacion_por_comuna.csv  resumen e índice de afectación por comuna
"""
import csv, json, zipfile, os, sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from geo import cargar, Indice

BASE = os.path.join(os.path.dirname(__file__), "..", "datos")
RAW, OUT = os.path.join(BASE, "raw"), os.path.join(BASE, "procesados")
os.makedirs(OUT, exist_ok=True)

comunas = Indice(cargar(f"{RAW}/idesc/pdt_dpa_comunas.geojson"), "comcodigo")
barrios = Indice(cargar(f"{RAW}/idesc/pdt_dpa_barrios_sectores.geojson"), "barcodigo")

puntos = []  # fuente, grado, tipo, nombre, lat, lon


def add(fuente, grado, tipo, nombre, lat, lon):
    try:
        lat, lon = float(lat), float(lon)
    except (TypeError, ValueError):
        return
    puntos.append(dict(fuente=fuente, grado=grado, tipo=tipo, nombre=nombre, lat=lat, lon=lon))


# 1. Copernicus EMSR916 (fotointerpretación)
for z in ["EMSR916_AOI01_GRA_PRODUCT_v2.zip", "EMSR916_AOI03_GRA_PRODUCT_v1.zip"]:
    zf = zipfile.ZipFile(f"{RAW}/sismo/{z}")
    for n in zf.namelist():
        if "builtUpP" in n and n.endswith(".json"):
            for f in json.loads(zf.read(n))["features"]:
                x, y = f["geometry"]["coordinates"][:2]
                p = f["properties"]
                add("Copernicus EMSR916", p["damage_gra"], p["simplified"], p.get("name", ""), y, x)

# 2. ICube-SERTIT / Charter (fotointerpretación)
for r in csv.DictReader(open(f"{RAW}/sismo/sertit_danos.csv", encoding="utf-8")):
    if r["municipio"].lower() == "cali" and r["dano"] != "Not Applicable":
        add("ICube-SERTIT", r["dano"], r["tipo"], "", r["lat"], r["lon"])

# 3. Microsoft AI for Good + Airbus (modelo sobre huellas de edificios)
for r in csv.DictReader(open(f"{RAW}/sismo/msft_danos.csv", encoding="utf-8")):
    if r["municipio"].lower() == "cali" and r["dano"] == "1":
        add("Microsoft/Airbus (modelo IA)", "Damaged (modelo)", "Building", "", r["lat"], r["lon"])

# 4. Sedes educativas con afectación reportada (MEN, SISE)
for r in csv.DictReader(open(f"{RAW}/sismo/men_sedes.csv", encoding="utf-8")):
    if r["cod_mun"] == "76001" and r["estado_fisico"] not in ("No aporta información", ""):
        add("MEN sedes educativas", r["estado_fisico"], "Educational", r["nombre_sede"], r["lat"], r["lon"])

for p in puntos:
    c, _ = comunas.buscar(p["lon"], p["lat"])
    b, bp = barrios.buscar(p["lon"], p["lat"])
    p["comuna"] = c or "fuera_urbano"
    p["barrio_cod"] = b or ""
    p["barrio"] = bp["barnombre"] if bp else ""

with open(f"{OUT}/danos_puntos_cali.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(puntos[0].keys()))
    w.writeheader(); w.writerows(puntos)

# Peso por grado de daño (fotointerpretación Copernicus/SERTIT; el modelo IA pesa menos)
PESO = {"Destroyed": 3, "Colapso parcial": 3, "Riesgo inminente de colapso": 3,
        "Damaged": 2, "Possibly damaged": 1, "Damaged (modelo)": 0.5,
        "Reporta afectación sin definir el impacto": 1}

agg = defaultdict(Counter)
top_barrios = defaultdict(Counter)
for p in puntos:
    a = agg[p["comuna"]]
    a[p["fuente"]] += 1
    a[f"grado:{p['grado']}"] += 1
    a["indice"] += PESO.get(p["grado"], 1)
    if p["barrio"]:
        top_barrios[p["comuna"]][p["barrio"]] += PESO.get(p["grado"], 1)

fuentes = sorted({p["fuente"] for p in puntos})
filas = []
for c, a in agg.items():
    filas.append({
        "comuna": c,
        **{f: a[f] for f in fuentes},
        "destruidos": a["grado:Destroyed"] + a["grado:Colapso parcial"],
        "danados": a["grado:Damaged"],
        "posibles": a["grado:Possibly damaged"],
        "indice_afectacion": round(a["indice"], 1),
        "barrios_mas_afectados": "; ".join(b for b, _ in top_barrios[c].most_common(4)),
    })
filas.sort(key=lambda r: -r["indice_afectacion"])
with open(f"{OUT}/afectacion_por_comuna.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
    w.writeheader(); w.writerows(filas)

print(f"{len(puntos)} puntos de daño en Cali")
for r in filas:
    print(r)
