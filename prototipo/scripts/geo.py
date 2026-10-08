"""Utilidades geoespaciales mínimas en Python puro (sin geopandas)."""
import json


def cargar(ruta):
    return json.load(open(ruta, encoding="utf-8"))["features"]


def _anillos(geom):
    if geom is None:
        return []
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon":
        return geom["coordinates"]
    return []


def _en_anillo(x, y, anillo):
    dentro = False
    j = len(anillo) - 1
    for i in range(len(anillo)):
        xi, yi = anillo[i][:2]
        xj, yj = anillo[j][:2]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            dentro = not dentro
        j = i
    return dentro


def bbox(geom):
    xs, ys = [], []
    for poly in _anillos(geom):
        for p in poly[0]:
            xs.append(p[0]); ys.append(p[1])
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def punto_en(x, y, geom, caja=None):
    if caja and not (caja[0] <= x <= caja[2] and caja[1] <= y <= caja[3]):
        return False
    for poly in _anillos(geom):
        if _en_anillo(x, y, poly[0]) and not any(_en_anillo(x, y, h) for h in poly[1:]):
            return True
    return False


def centroide(geom):
    """Centroide aproximado: promedio de vértices del anillo exterior más grande, o el punto."""
    if geom["type"] == "Point":
        return geom["coordinates"][:2]
    if geom["type"] == "MultiPoint":
        return geom["coordinates"][0][:2]
    polys = _anillos(geom)
    if not polys:
        return None
    ext = max((p[0] for p in polys), key=len)
    return [sum(p[0] for p in ext) / len(ext), sum(p[1] for p in ext) / len(ext)]


class Indice:
    """Asigna puntos a polígonos (p. ej. comunas o barrios)."""

    def __init__(self, features, clave):
        self.items = [(f["properties"][clave], f["geometry"], bbox(f["geometry"]), f["properties"]) for f in features if f["geometry"]]

    def buscar(self, x, y):
        for k, g, c, props in self.items:
            if punto_en(x, y, g, c):
                return k, props
        return None, None
