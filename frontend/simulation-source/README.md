# Simulación de Cali — versión 3

Versión suministrada en `simulacion_ciudad_cali_v3.zip`, integrada el 8 de octubre de 2026.

- `simulacion_ciudad_cali.html`: original v3, conservado sin modificaciones.
- `LEEME.txt` y `FUENTES_Y_METODO.md`: instrucciones y método aportados con v3.
- `python3 frontend/scripts/integrate_simulation.py`: genera `frontend/dist/simulation.html` con enlaces de regreso, fuentes y mejoras de presentación.
- GitHub Pages adapta las rutas mediante `frontend/scripts/prepare_pages.py`.

Los archivos `enhancements.js`, `simulation-math.cjs`, `simulation-math.test.cjs` y `browser-check.cjs` pertenecen a la integración anterior; no se aplican ni validan los modelos de v3. Los controles y modelos actuales son los incluidos en el HTML suministrado.

La integración aplica `rendering.css`, ajusta la iluminación y la niebla de la maqueta y añade un selector de calidad visual (ligera, equilibrada y alta). El original v3 y los modelos de cálculo se conservan sin modificaciones.
