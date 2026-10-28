# Territorio Preparado

Prototipo territorial para preparar espacios y coordinar ayudas ante emergencias en Cali.

Equipo: William Ortiz, Herlin Echeverry, Pablo Arango y Bryan Martinez Villamarin.

## Documento actualizado

- [Documento PDF](Territorio_Preparado_Actualizado.pdf)
- [Documento editable Word](Territorio_Preparado_Actualizado.docx)
- [Documento fuente](Territorio_Preparado_Actualizado.md)

## Ejecutar el prototipo

Desde la raíz del repositorio, con Python 3 instalado:

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory frontend/dist
```

Abrir http://127.0.0.1:4173/ y usar **06 Simulación** para acceder al laboratorio.

La entrega contiene la app compilada; no requiere instalar Node para ejecutarla. Los fuentes originales y la configuración de compilación React no están disponibles en esta copia. Los scripts de mantenimiento se conservan en `frontend/scripts` y el laboratorio en `frontend/simulation-source`.

Los escenarios son ejercicios de preparación; sus límites y fuentes aparecen en la interfaz y en `frontend/dist/simulation-method.md`.

## GitHub Pages

Dirección pública: https://bryanmavi.github.io/Territorio-Preparado/

Un administrador debe seleccionar **Settings → Pages → Build and deployment → Source → GitHub Actions**. El workflow `.github/workflows/pages.yml` publica `frontend/dist` cada vez que se actualiza `main`. El script `frontend/scripts/prepare_pages.py` adapta rutas de datos, imágenes, módulos y simulación al prefijo del repositorio, conservando la ejecución local original.

## Simulación v3

Actualizada el 8 de octubre de 2026 con el paquete suministrado `simulacion_ciudad_cali_v3.zip`. Incluye las pestañas Simulación y Albergues y nuevos controles de escenarios. El original y sus fuentes se conservan en `frontend/simulation-source`.

La raíz incluye un acceso a `frontend/dist/` para funcionar también si Pages publica la rama `main` directamente. Las rutas de la aplicación son relativas y los módulos diferidos comparten la misma instancia de React; no añadir parámetros de versión al módulo principal en `index.html`.

## IA para desastres · BERT SOS y xView2

La aplicación incorpora **07 Centro de operaciones** y el [visor de IA para desastres](https://bryanmavi.github.io/Territorio-Preparado/disaster-ai.html).

- **BERT SOS:** clasificación multietiqueta de mensajes, traducción local español–inglés y persistencia en SQLite. Las salidas requieren revisión humana; no se ha verificado la correspondencia semántica de las 36 etiquetas.
- **xView2:** adaptador de los pesos oficiales para imágenes antes/después y exportación GeoJSON. Requiere provisionar su runtime; las pruebas técnicas no constituyen validación de precisión.
- **GitHub Pages:** publica la interfaz y el demostrador de conteo sintético. No ejecuta Python ni aloja inferencias; la interfaz indica cuando el servidor de IA no está disponible.

Para ejecutar las inferencias, sigue [instalación, modelos y pruebas](servidor/ia/README.md). Con el entorno y los pesos instalados:

```bash
servidor/ia/.venv/bin/python -m uvicorn servidor.ia.app:app --host 127.0.0.1 --port 4180
```

Abre http://127.0.0.1:4180/disaster-ai.html. El puerto 4173 sirve únicamente la aplicación estática. Los pesos, entornos virtuales, bases de datos y archivos de instrucciones para asistentes no forman parte de esta publicación.

[Arquitectura del servidor propio](docs/SERVIDOR_PROPIO_IA_Y_VIGILANCIA.md) · [registro técnico anterior de modelos y pruebas](docs/evidence/ia-2026-10-16.json).
