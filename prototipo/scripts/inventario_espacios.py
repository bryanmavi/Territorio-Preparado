"""Inventario de espacios públicos de Cali con su exposición real a cada amenaza.

Base: EPOU - Espacio Público Efectivo (DAPM/IDESC, 1.970 parques, zonas verdes, plazas).
Le cruza: inundación fluvial y pluvial del POT, microzonificación sísmica, licuación,
distancia al dique del río Cauca (Jarillón), daños reales del sismo del 10-ago-2026,
IPS y organismos de socorro cercanos, y el índice de afectación de su comuna.

Salida: prototipo/datos/procesados/inventario_espacios_cali.csv
"""
import csv, math, os, re, sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from geo import cargar, Indice, bbox, punto_en

BASE = os.path.join(os.path.dirname(__file__), "..", "datos")
RAW, OUT = os.path.join(BASE, "raw"), os.path.join(BASE, "procesados")


def metros(lat1, lon1, lat2, lon2):
    x = math.radians(lon2 - lon1) * math.cos(math.radians((lat1 + lat2) / 2))
    y = math.radians(lat2 - lat1)
    return 6371000 * math.hypot(x, y)


class Rejilla:
    """Índice espacial simple para buscar puntos cercanos (celdas de ~1,1 km)."""

    def __init__(self, puntos, celda=0.01):
        self.c, self.g = celda, defaultdict(list)
        for p in puntos:
            self.g[(int(p[0] / celda), int(p[1] / celda))].append(p)

    def cerca(self, lat, lon, radio_m):
        k = math.ceil(radio_m / 1100) + 1
        i, j = int(lat / self.c), int(lon / self.c)
        for a in range(i - k, i + k + 1):
            for b in range(j - k, j + k + 1):
                for p in self.g.get((a, b), []):
                    d = metros(lat, lon, p[0], p[1])
                    if d <= radio_m:
                        yield d, p

    def mas_cercano(self, lat, lon, radio_max=8000):
        return min(self.cerca(lat, lon, radio_max), default=(None, None), key=lambda t: t[0])


def capa_poligonos(nombre, campo):
    return [(f["properties"][campo], f["geometry"], bbox(f["geometry"])) for f in cargar(f"{RAW}/idesc/{nombre}.geojson") if f["geometry"]]


def primera(capa, lat, lon, orden=None):
    hits = [k for k, g, c in capa if punto_en(lon, lat, g, c)]
    if orden and hits:
        hits.sort(key=lambda h: orden.get(h, 9))
    return hits[0] if hits else ""


def nivel_inund(t):
    if not t:
        return "Sin amenaza"
    for n in ("no mitigable", "Alta", "Media", "Baja", "Torrenciales"):
        if n in t:
            return {"no mitigable": "No mitigable", "Torrenciales": "Avenida torrencial"}.get(n, n)
    return t


ORDEN = {}
fluvial = capa_poligonos("amb_ari_inundacion_fluvial", "tipo_amena")
pluvial = capa_poligonos("amb_ari_inundacion_pluvial", "tipo_amena")
cauca = capa_poligonos("emc_amb_ari_amenaza_no_mitigable_inundacion", "amenaza_in")
micro = [(f["properties"], f["geometry"], bbox(f["geometry"])) for f in cargar(f"{RAW}/idesc/mc_microzonificacion_sismica.geojson")]
efectos = capa_poligonos("amb_ari_efectos_sismicos", "tipo")
prio = {"no mitigable": 0, "Alta": 1, "Media": 2, "Torrenciales": 3, "Baja": 4}
orden = lambda capa: {k: min((v for n, v in prio.items() if n in k), default=9) for k, _, _ in capa}

# Vértices del dique del río Cauca (Jarillón)
dique = []
for f in cargar(f"{RAW}/idesc/amb_ari_diques.geojson"):
    if f["properties"]["nombre"] == "Río Cauca":
        g = f["geometry"]
        lineas = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
        for l in lineas:
            for i in range(len(l) - 1):  # densificar cada ~50 m
                (x1, y1), (x2, y2) = l[i][:2], l[i + 1][:2]
                n = max(1, int(metros(y1, x1, y2, x2) / 50))
                dique += [(y1 + (y2 - y1) * t / n, x1 + (x2 - x1) * t / n) for t in range(n)]
dique_r = Rejilla(dique, 0.02)

danos = [(float(r["lat"]), float(r["lon"]), r["fuente"], r["grado"]) for r in csv.DictReader(open(f"{OUT}/danos_puntos_cali.csv", encoding="utf-8"))]
danos_r = Rejilla(danos)

ips = {}
for f in cargar(f"{RAW}/idesc/ads_ips_capacidad_reps.geojson"):
    if f["geometry"]:
        x, y = f["geometry"]["coordinates"][:2]
        ips.setdefault(f["properties"]["nombre_ips"], (y, x, f["properties"]["nombre_ips"]))
ips_r = Rejilla(list(ips.values()))

socorro = []
for r in csv.DictReader(open(f"{RAW}/cali_abiertos/organismos_socorro.csv", encoding="latin1"), delimiter="|"):
    m = re.findall(r"-?\d+\.\d+", r["Localizacion"])
    if len(m) == 2:
        socorro.append((float(m[0]), float(m[1]), f"{r['Organismo']} {r['Sede']}".strip()))
socorro_r = Rejilla(socorro)

afect = {r["comuna"]: float(r["indice_afectacion"]) for r in csv.DictReader(open(f"{OUT}/afectacion_por_comuna.csv", encoding="utf-8"))}

filas = []
for f in cargar(f"{RAW}/idesc/epou_epu_espacio_publico_efectivo.geojson"):
    p = f["properties"]
    lat, lon = p["epelatitud"], p["epelongit"]
    if lat is None or lon is None:
        continue
    fl = primera(fluvial, lat, lon, orden(fluvial))
    pl = primera(pluvial, lat, lon, orden(pluvial))
    mz = next((pp for pp, g, c in micro if punto_en(lon, lat, g, c)), None)
    ef = primera(efectos, lat, lon)
    d_dique, _ = dique_r.mas_cercano(lat, lon, 20000)
    cerca = list(danos_r.cerca(lat, lon, 500))
    d_ips, ip = ips_r.mas_cercano(lat, lon)
    d_soc, so = socorro_r.mas_cercano(lat, lon, 15000)
    filas.append({
        "id": p["epecodep"] and f"{p['epecodep']}-{p['gid']}",
        "tipo": p["epepotele"], "subtipo": p["epepottip"], "escala": p["epepotesc"],
        "comuna": p["epeidcomuna"], "barrio_cod": p["epeidbarrio"], "barrio": p["epebarrio"],
        "lat": round(lat, 6), "lon": round(lon, 6),
        "area_m2": round(p["shape_area"]),
        "estado_cualitativo": p["epecualit"], "grado_cercania": p["epegracer"],
        "inund_fluvial": nivel_inund(fl), "inund_pluvial": nivel_inund(pl),
        "zona_inund_rio_cauca": "Sí" if primera(cauca, lat, lon) == "Amenaza inundación río Cauca" else "No",
        "dist_dique_cauca_m": round(d_dique) if d_dique is not None else "",
        "micro_sismica_zona": (mz or {}).get("label") or "",
        "micro_sismica_Aa": (mz or {}).get("am_etc") or "",
        "licuacion": "Sí" if (mz and mz.get("sucep_licu")) or "licuacion" in ef else "No",
        "corrimiento_lateral": "Sí" if "Corrimiento" in ef else "No",
        "danos_sismo_500m": len(cerca),
        "danos_graves_500m": sum(1 for _, d in cerca if d[3] in ("Destroyed", "Damaged", "Colapso parcial")),
        "ips_cercana": ip[2] if ip else "", "dist_ips_m": round(d_ips) if d_ips else "",
        "socorro_cercano": so[2] if so else "", "dist_socorro_m": round(d_soc) if d_soc else "",
        "indice_afectacion_comuna": afect.get(p["epeidcomuna"], 0),
        "street_view": p["epestrview"],
    })

with open(f"{OUT}/inventario_espacios_cali.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
    w.writeheader(); w.writerows(filas)

from collections import Counter
print(len(filas), "espacios")
for k in ("inund_fluvial", "zona_inund_rio_cauca", "micro_sismica_zona", "licuacion", "corrimiento_lateral"):
    print(k, Counter(r[k] for r in filas).most_common())
print("a <500 m del dique:", sum(1 for r in filas if r["dist_dique_cauca_m"] != "" and r["dist_dique_cauca_m"] < 500))
print("con daños graves a <500 m:", sum(1 for r in filas if r["danos_graves_500m"]))
