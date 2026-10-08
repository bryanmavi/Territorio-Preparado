"""Resumen multiamenaza por comuna: población, espacio público, exposición y daño real del sismo.

Salida: prototipo/datos/procesados/resumen_comunas_multiamenaza.csv
"""
import csv, os
from collections import defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..", "datos")
RAW, OUT = os.path.join(BASE, "raw"), os.path.join(BASE, "procesados")

pob = {}
for r in csv.DictReader(open(f"{RAW}/cali_abiertos/poblacion_comuna_2006_2020.csv", encoding="latin1")):
    d = list(r.values())[0]
    if d.startswith("Comuna "):
        pob[f"{int(d.split()[1]):02d}"] = int(r["2020"])

estrato = {}
for r in csv.DictReader(open(f"{RAW}/cali_abiertos/estrato_moda_comuna_2015.csv", encoding="latin1")):
    if r["Comuna"].isdigit():
        estrato[f"{int(r['Comuna']):02d}"] = r["Estrato moda"]

afect = {r["comuna"]: r for r in csv.DictReader(open(f"{OUT}/afectacion_por_comuna.csv", encoding="utf-8"))}

esp = defaultdict(list)
for r in csv.DictReader(open(f"{OUT}/inventario_espacios_cali.csv", encoding="utf-8")):
    esp[r["comuna"]].append(r)

filas = []
for c in sorted(pob):
    e = esp.get(c, [])
    area = sum(int(x["area_m2"]) for x in e)
    grandes = [x for x in e if int(x["area_m2"]) >= 2000]
    a = afect.get(c, {})
    filas.append({
        "comuna": c,
        "poblacion_2020": pob[c],
        "estrato_moda": estrato.get(c, ""),
        "espacios_publicos": len(e),
        "espacios_>=2000m2": len(grandes),
        "ep_m2_por_hab": round(area / pob[c], 2),
        "pct_ep_inund_alta_o_no_mitigable": round(100 * sum(x["inund_fluvial"] in ("Alta", "No mitigable") for x in e) / len(e)) if e else "",
        "espacios_<500m_dique_cauca": sum(1 for x in e if x["dist_dique_cauca_m"] and int(x["dist_dique_cauca_m"]) < 500),
        "pct_ep_licuacion": round(100 * sum(x["licuacion"] == "Sí" for x in e) / len(e)) if e else "",
        "zona_sismica_dominante": max({x["micro_sismica_zona"] for x in e} - {""}, key=lambda z: sum(x["micro_sismica_zona"] == z for x in e), default=""),
        "edificios_destruidos_sismo": a.get("destruidos", 0),
        "edificios_danados_sismo": a.get("danados", 0),
        "sedes_educativas_afectadas": a.get("MEN sedes educativas", 0),
        "indice_afectacion_sismo": a.get("indice_afectacion", 0),
        "barrios_mas_afectados": a.get("barrios_mas_afectados", ""),
    })

with open(f"{OUT}/resumen_comunas_multiamenaza.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
    w.writeheader(); w.writerows(filas)
for f in filas:
    print(f)
