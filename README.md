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
