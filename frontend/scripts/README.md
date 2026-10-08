# Mantenimiento del mapa de la demo

Esta copia contiene la aplicación compilada, sin el proyecto fuente original.

- `python3 frontend/scripts/improve_map.py`: aplica de forma reproducible las correcciones del mapa al bundle; conserva el original.
- `python3 frontend/scripts/verify_map_sources.py`: descarga las fuentes oficiales en `/tmp/territorio-current-sources`, compara geometrías y propiedades con los archivos originales y actualiza `frontend/dist/data/current-source-checks.json`.

Una consulta reciente no cambia la fecha de captura del inventario. Si se detectan cambios, deben regenerarse cruces, asignaciones territoriales y resúmenes antes de sustituir los derivados. Si la fuente no responde, se conserva la cartografía archivada con su fecha, sin afirmar que es actual.

Correcciones: listado completo de barrios oficiales; encuadre por límites y no solo por registros; límites y amenazas no interceptan selección; zoom de calles hasta 21 con nivel nativo 19; explicación de sectores sin inventario; enlace visible al estado de actualización.

## Explorador del mapa

`python3 frontend/scripts/improve_map_experience.py` aplica el diseño e interacciones propios de `frontend/map-source/` al bundle existente y copia su hoja de estilos. Conserva las correcciones de rutas de Pages y las demás secciones. Si se reconstruye el mapa con el script anterior, aplicar después este script y preparar las rutas de Pages.

El mapa agrupa espacialmente los registros visibles por celdas de 54 píxeles al alejarse; cada número cuenta registros, no predios únicos. Desde zoom 15 se muestran las geometrías del inventario. Los controles de espacios públicos y deportivos solo cambian la visibilidad del mapa, mientras los filtros territoriales y la búsqueda modifican el inventario consultado. Los datos y cruces de amenaza no cambian.

Comprobación en navegador: `MAP_URL=http://127.0.0.1:4173/ node frontend/map-source/browser-check.cjs` (requiere Playwright; `PLAYWRIGHT_MODULE` permite indicar su instalación). Comprueba agrupación, capas, selección, búsqueda, filtros, vista ampliada y móvil.
