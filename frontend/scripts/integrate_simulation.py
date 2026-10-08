"""Integrate the supplied v3 simulation without applying legacy v1 patches."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
source = root / 'simulation-source'
out = root / 'dist'
html = (source / 'simulacion_ciudad_cali.html').read_text()
marker = '<p class="marca">Territorio Preparado · RETO-01 Cali Activa</p>'
assert marker in html
html = html.replace(marker, marker + '<p style="margin:4px 0;font-size:12px"><a href="./">← Volver a Territorio Preparado</a> · Simulación v3 · <a href="./simulation-method.md" target="_blank" rel="noopener">Fuentes y método</a></p>', 1)
(out / 'simulation.html').write_text(html)
(out / 'simulation-method.md').write_text((source / 'FUENTES_Y_METODO.md').read_text())
print('Simulation v3 integrated')
