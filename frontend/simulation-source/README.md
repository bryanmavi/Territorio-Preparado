# Laboratorio de escenarios de Cali

Integración del ZIP `simulacion_ciudad_cali.zip` aportado por el equipo. Originales conservados en esta carpeta. Maqueta y escenarios permanecen autocontenidos, sin añadir dependencias CDN ni publicar a servicios externos.

## Generar

Desde la raíz del repositorio:

```bash
python3 frontend/scripts/improve_map.py
python3 frontend/scripts/integrate_simulation.py
node frontend/simulation-source/simulation-math.test.cjs
```

El primer comando restaura y aplica el parche de mapa sobre el bundle original; el segundo debe ejecutarse después para recuperar la pestaña de simulación. No hace falta repetir el primer comando si solo se cambia el laboratorio. La integración es idempotente y conserva las pestañas existentes.

## Verificar

Con el servidor de la demo en `127.0.0.1:4173`:

```bash
node frontend/simulation-source/browser-check.cjs
```

Recorre inundación/sismo/incendio, pausa y continuación, movimiento reducido, informe JSON, comparación, transferencia de candidato con su amenaza, navegación entre vistas y formato móvil sin descargas externas. Requiere Chrome instalado.

## Cambios

- Pestaña «06 Simular escenarios», con opción de vista a pantalla completa.
- Candidatos conectados por mensajes del mismo origen y validación de ID a la preparación existente. Incendio conserva su estado de verificación, no se transforma en inundación al entrar.
- Pausa, reinicio, duración visual, movimiento reducido y detalle de pantalla.
- Tres vistas de cámara, captura PNG, comparación de ejercicios en memoria e informe JSON.
- Capas drapeadas sobre el relieve; iluminación y materiales con mejor legibilidad; bounds y matrices de instancias actualizados.
- Solo se dibuja cuando cambia la escena, la cámara o el ejercicio; la pestaña oculta pausa la reproducción.
- Margen del incendio medido contra celdas cuadradas de 60 m: índice espacial contrastado en 4.000 puntos contra cálculo exhaustivo. Sigue siendo un parámetro supuesto, no una distancia segura.
- Inicio en 0 %, controles deshabilitados durante carga y aviso si WebGL o el decodificador fallan.

## Evidencia y límites

El ZIP contiene el producto compilado, no los scripts Blender ni la fuente React original referidos por su autor. La app principal también está compilada; se usan parches reproducibles hasta recuperar ese proyecto fuente. El laboratorio usa Three.js r180 directamente dentro de una vista aislada; no se monta un segundo renderer sobre el Canvas de React Three Fiber existente.

Las fuentes y conteos del ZIP se atribuyen a su documento `FUENTES_Y_METODO.md`; no se hizo una nueva descarga completa del catastro ni una verificación independiente de sus cifras. La licencia catastral sigue por verificar según el autor. Esta integración local no implica publicación ni certificación legal.

Inundación y sismo revelan categorías de capas, no dinámica hidráulica ni cálculo de daños estructurales. Incendio es un ejercicio de propagación reproducible con semilla fija, no un modelo calibrado del fuego. Conteos catastrales no son habitantes. Comparar amenazas diferentes no demuestra igualdad de impacto. Selección por coordenada/centro y área no verifica toda la superficie, acceso, disponibilidad ni autorización. El informe conserva estos límites.
