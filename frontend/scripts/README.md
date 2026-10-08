# Mantenimiento del mapa de la demo

Esta copia contiene la aplicación compilada, sin el proyecto fuente original.

- `python3 frontend/scripts/improve_map.py`: aplica de forma reproducible las correcciones del mapa al bundle; conserva el original.
- `python3 frontend/scripts/verify_map_sources.py`: descarga las fuentes oficiales en `/tmp/territorio-current-sources`, compara geometrías y propiedades con los archivos originales y actualiza `frontend/dist/data/current-source-checks.json`.

Una consulta reciente no cambia la fecha de captura del inventario. Si se detectan cambios, deben regenerarse cruces, asignaciones territoriales y resúmenes antes de sustituir los derivados. Si la fuente no responde, se conserva la cartografía archivada con su fecha, sin afirmar que es actual.

Correcciones: listado completo de barrios oficiales; encuadre por límites y no solo por registros; límites y amenazas no interceptan selección; zoom de calles hasta 21 con nivel nativo 19; explicación de sectores sin inventario; enlace visible al estado de actualización.
