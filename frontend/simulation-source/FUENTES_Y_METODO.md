# Maqueta 3D de Cali: cómo se hizo y de dónde salió cada dato

**Fecha de consulta y descarga:** 8 de octubre de 2026.
**Para qué sirve:** es la base de la simulación de los tres escenarios (sismo, inundación e incendio forestal) y de la propuesta de sitios para acopios.
**Qué no es:** no es un gemelo digital certificado ni un estudio de amenaza. La volumetría es por manzana, no edificio por edificio, y la simulación muestra las capas oficiales, no las reemplaza.

Este documento registra **todos los sitios consultados**: los que se usaron y los que se descartaron, con la razón. Así cualquiera puede repetir el proceso y verificar cada cifra.

---

## 1. Fuentes usadas

### 1.1 Catastro de Cali: construcciones (IDESC)
- **Capa:** `catastro:cat_bas_construcciones`, servicio WFS de la IDESC.
- **Descubierta en:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&request=GetCapabilities
- **Descarga (8 páginas de 100.000):** `https://ws-idesc.cali.gov.co/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&outputFormat=application/json&srsName=EPSG:4326&typeNames=catastro:cat_bas_construcciones&propertyName=sector,comuna,barrio,manzana,npisos,shape_area&startIndex=0&count=100000`
- **Registros:** 713.863 construcciones (`numberMatched`), sin duplicados entre páginas.
- **Campos usados:** solo códigos de manzana (`sector`, `comuna`, `barrio`, `manzana`), `npisos` y `shape_area`. **No se descargaron** la geometría, el número predial nacional (`npn`) ni los códigos de predio. Así se cumple el principio de minimización (Ley 1581 de 2012): no hay datos que permitan identificar un predio ni a su dueño.
- **Calidad del dato de pisos:** 289.064 construcciones tienen `npisos = 0` y 6 tienen `-1` (sin dato). En la maqueta cuentan como 1 piso y el número queda registrado. El máximo en catastro es 25 pisos; en la volumetría por manzana el promedio más alto es 20.
- **Licencia:** el WFS no la declara y la capa no aparece en datos.cali.gov.co (búsqueda en https://datos.cali.gov.co/api/3/action/package_search?q=construcciones). **(verificar con la Subdirección de Catastro antes de publicar)**. El repositorio es privado.

### 1.2 Catastro de Cali: manzanas (IDESC)
- **Capa:** `catastro:cat_bas_manzanas`.
- **Descarga:** `https://ws-idesc.cali.gov.co/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&outputFormat=application/json&srsName=EPSG:4326&typeNames=catastro:cat_bas_manzanas`
- **Registros:** 15.743 manzanas. 174 claves (`sector`+`comuna`+`barrio`+`manzana`) se repiten; su conteo se suma una sola vez.
- **Cruce:** 711.509 de 713.863 construcciones (99,7 %) encuentran su manzana.
- **Filtro:** se excluyen las manzanas rurales (`tipo_avalu = 00`) y las de más de 10 ha (campus y zonas industriales), porque como bloque macizo cubrían los cerros. Quedan **14.179 polígonos** con **693.468 construcciones**; 270.095 de ellas no tienen dato de pisos.
- **Licencia:** igual que 1.1 **(verificar)**.

### 1.3 Ríos (POT 2014, IDESC)
- **Capa:** `pot_2014:bcs_hid_rios`, 12 polígonos. Se recortan al área de la maqueta, porque el Cauca se extiende cerca de 200 km; quedan 10.
- **Descarga:** `https://ws-idesc.cali.gov.co/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&outputFormat=application/json&srsName=EPSG:4326&typeNames=pot_2014:bcs_hid_rios`
- **Licencia:** CC BY-SA, como las demás capas del POT en datos.cali.gov.co.

### 1.4 Cobertura boscosa (POT 2014, IDESC)
- **Capa:** `pot_2014:amb_eep_aeie_cobertura_boscosa`, 429 polígonos. Descargada para el escenario de incendio forestal.
- **Ojo:** cobertura boscosa **no es** amenaza de incendio. Sirve para ubicar dónde hay vegetación, nada más.

### 1.5 Relieve: Terrain Tiles (AWS Open Data)
- **Registro:** https://registry.opendata.aws/terrain-tiles/
- **Teselas:** `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/13/{x}/{y}.png`, 36 teselas de zoom 13 (x 2351–2356, y 4015–4020). No requiere clave.
- **Formato:** PNG Terrarium, altura = R×256 + G + B/256 − 32.768 m.
- **Origen de los datos para Colombia:** SRTM de la NASA, con resolución de unos 30 m. La atribución obligatoria está en https://github.com/tilezen/joerd/blob/master/docs/attribution.md
- **Resultado:** grilla de 408 × 388 celdas de 60 m (24,4 × 23,2 km), con alturas de 929 a 3.110 m.

### 1.6 Capas que ya tenía la app (25 de septiembre)
Inundación (`flood.json`), licuación y corrimiento (`seismic.json`) y espacios públicos (`spaces.json`). Su origen está en `prototipo/datos/FUENTES.md`.

---

## 2. Fuentes consultadas y descartadas

| Fuente | Qué se probó | Resultado | Por qué se descartó |
|---|---|---|---|
| OpenStreetMap, Overpass API (`overpass-api.de`, `overpass.private.coffee`, `overpass.kumi.systems`) | Contar edificios en la caja de Cali | Servidores saturados o con error | No respondió. Además, el catastro es más completo |
| Overture Maps, edificios, versión `2026-09-23.1` (`s3://overturemaps-us-west-2`, consultado con DuckDB) | Contar edificios en la caja de Cali | **39.733** edificios: 17.601 de Microsoft, 12.417 de Google Open Buildings y 9.715 de OSM. Solo 742 con altura y 3.551 con pisos | Cubre cerca del 6 % de lo que tiene el catastro (713.863) |
| Capa ArcGIS «amenaza forestal» de Bomberos (consulta del 25-sep, ver `docs/DATASETS.md`) | Metadatos | Sin procedencia oficial ni licencia | No se usa geometría |
| Google Street View y Google Photorealistic 3D Tiles | Revisión de condiciones de uso | Ver sección 4 | Los términos de Google Maps Platform prohíben crear datos derivados de su contenido |

---

## 3. Cómo se construyó (reproducible)

1. **Descarga:** `prototipo/datos/raw/ciudad3d/bajar.sh` (catastro, ríos y cobertura boscosa) más las teselas de relieve.
2. **Preparación:** `python3 prototipo/scripts/ciudad3d.py`, en Python con numpy, sin GDAL. Proyecta todo a metros locales con origen en lon −76,53 y lat 3,42, decodifica el relieve, calcula los pisos promedio de cada manzana (ponderados por área construida) y simplifica los polígonos (Douglas-Peucker, 1,5 m). Genera `prototipo/datos/procesados/ciudad3d/ciudad.json`.
3. **Modelo 3D:** `blender -b --python maqueta3d/scripts/blender/ciudad.py` (Blender 4.0.2, tarda unos 4 s). Arma el terreno (158.304 vértices), extruye cada manzana a pisos × 3 m sobre el relieve (249.594 vértices) y agrega los ríos. Guarda `cali.blend` y un GLB sin comprimir de 33 MB en `prototipo/datos/procesados/ciudad3d/`.
4. **Compresión:** el Blender de Ubuntu no trae Draco, así que se comprime con glTF-Transform (`npx @gltf-transform/cli@4 draco … --quantize-position 16 --quantize-texcoord 16 --quantize-normal 10`). Resultado: `maqueta3d/public/ciudad/cali.glb` de **1,65 MB**. Cada manzana lleva su índice en la coordenada UV para que la app la coloree.
5. **Revisión en Blender:** con **MCP for Blender** (addon 1.8, instalado con `uvx mcp-for-blender install-addon`) se abre `cali.blend` en el Blender del equipo y se revisa visualmente desde Claude.
6. **Simulación y acopios:** en la app web (React Three Fiber, la misma base de Three.js de la web de Universal Group), sobre el GLB y las capas oficiales. Ver sección 5.

**Herramientas:** Blender 4.0.2, MCP for Blender 1.8, glTF-Transform 4 (por `npx`), Python 3.12 con numpy y DuckDB 1.5.6 (solo para la prueba de Overture, con `uv run --with duckdb`; no quedó instalado).

**Herramientas especializadas que se evaluaron y no hicieron falta:** BlenderGIS y Blender-OSM (blosm) importan edificios de OpenStreetMap y relieve dentro de Blender. Aquí no aportan, porque OSM tiene muy pocos edificios de Cali (sección 2) y el catastro oficial es más completo. Además, BlenderGIS pide una clave de OpenTopography para el relieve SRTM. El flujo con scripts propios es reproducible con un solo comando.

---

## 4. Servicios de Google: qué se puede y qué no

- **Abrir Street View de un sitio:** ya funciona sin clave con los enlaces oficiales de Google Maps URLs (`src/googleMaps.ts`).
- **Ver Street View dentro de la app:** requiere una clave de Google Cloud con la *Maps Embed API* habilitada. Ese uso no tiene costo, pero Google exige una cuenta de facturación activa.
- **Edificios fotorrealistas de Google (Photorealistic 3D Tiles, Map Tiles API):** requiere clave y facturación (hay un cupo gratuito mensual), mostrar el logo y la atribución de Google, y no guardar el contenido. Hay que verificar si Cali tiene cobertura. Serviría solo como **capa visual**.
- **"Mapear la ciudad" con Street View:** **no está permitido.** Los términos de Google Maps Platform prohíben extraer contenido de Google Maps o crear contenido a partir de él, por ejemplo calcando edificios o derivando datos de sus imágenes. Por eso el mapeo se hizo con el catastro oficial y no con Google.

---

## 5. Simulación y propuesta de acopios (pestaña 07 de la app)

Archivos: `maqueta3d/src/CiudadSim.tsx` (vista 3D) y `maqueta3d/src/ciudadSim.ts` (lógica, con pruebas en `scripts/ciudad-sim.test.mjs`). Los datos livianos salen de `prototipo/scripts/ciudad3d.py` hacia `maqueta3d/public/ciudad/escenarios.json`: el cruce oficial por manzana, la máscara de vegetación y los puntos de daño.

| Escenario | Qué se muestra | Fuente | Qué **no** es |
|---|---|---|---|
| **Inundación** | Manzanas cuyo centro cae en una zona de amenaza: **5.357**. La animación revela primero la amenaza alta (incluye no mitigable, avenidas torrenciales y río Cauca), luego la media y por último la baja | POT 2014 fluvial y pluvial y expediente municipal (IDESC), las mismas capas de `flood.json` | No es un modelo hidráulico ni muestra el avance real del agua |
| **Sismo** | Manzanas en zonas de licuación o corrimiento: **7.855**. También los **1.090 puntos de daño** observados tras el sismo del 10-ago-2026 | Licuación y efectos sísmicos (IDESC). Daños: Copernicus EMSR916, ICube-SERTIT, Microsoft/Airbus (modelo de IA) y MEN | La vibración es solo visual; no calcula daño por edificio |
| **Incendio forestal** | Propagación sobre **40.488 celdas** de 60 m con cobertura boscosa oficial y **38.441 celdas** de ladera no urbana por encima de 1.050 m (pastos y rastrojo). Estas últimas son un **supuesto** porque no hay capa oficial. Si el punto de inicio no cae en una celda combustible, se mueve a la más cercana (hasta 600 m). Avanza más rápido ladera arriba y a favor del viento, con azar de semilla fija (siempre da el mismo resultado). Se puede elegir el punto de inicio y el viento | Cobertura boscosa POT 2014 (IDESC) y relieve | **Es un ejercicio.** No hay capa oficial de amenaza por incendio y no es un modelo de comportamiento del fuego (FARSITE o Rothermel). El margen alrededor del área quemada (300 m por defecto) es un supuesto que se puede ajustar, no una distancia segura |

**Cómo se eligen los sitios de acopio:**
1. Se toman los espacios públicos y escenarios deportivos del inventario (`spaces.json`) con al menos **1.000 m²**. Ese umbral es un supuesto del ejercicio.
2. **Inundación y sismo:** se aplica la misma regla de la pestaña 03 (`eligibility` en `planning.ts`). Se descarta todo espacio que cruce la capa oficial.
3. **Incendio:** se descarta todo espacio dentro del área quemada o de su margen supuesto.
4. Los sitios se ordenan por **demanda cercana**: construcciones de manzanas afectadas a menos de 1,5 km. Se eligen 8, **separados al menos 1 km entre sí** para no sugerir tres parques del mismo barrio. Cada uno trae su enlace a Street View (sin clave) y el botón *Preparar intervención*.
5. Es una **preselección para revisar en sitio**. No confirma disponibilidad, estado estructural ni autorización: la activación la registra una persona autorizada (Ley 1523 de 2012, «recomienda, no decide»).

**Puntos de inicio del incendio:** Cristo Rey (−76,5652; 3,4357), Cerro de las Tres Cruces (−76,5485; 3,4655) y Pichindé (−76,6155; 3,4405). Son coordenadas **aproximadas (verificar)**, puestas a mano para el ejercicio. Pichindé tiene antecedentes de incendio forestal según la Alcaldía (ver `src/fire.ts`).
