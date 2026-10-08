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

---

## 6. Versión realista (8 de octubre, tarde)

Entregable independiente: `entregables/simulacion-ciudad/` (un solo HTML que se abre con doble clic; ver su `LEEME.txt`). Se arma con `node entregables/simulacion-ciudad/construir.mjs`.

### 6.1 Edificio por edificio (catastro)
- **Huellas:** `catastro:cat_bas_construcciones` con geometría, solo `npisos`, `shape_area` y `the_geom` (`raw/ciudad3d/bajar_edificios.sh`; sin NPN, predio ni códigos prediales). 713.863 registros, sin duplicados entre páginas.
- **Proceso:** `prototipo/scripts/edificios3d.py` simplifica cada huella (Douglas-Peucker, 0,35 m) y la guarda por teselas de 1 km en un binario con coordenadas cada 0,2 m (17,9 MB → 9,7 MB comprimido). Quedan **634.239 edificios**. Se omiten **79.624** construcciones menores de 4 m² (mediana de 2,8 m²: casetas y tanques). **271.940** no tienen dato de pisos (43 %) y se dibujan de 1 piso.
- **En pantalla:** cerca de la cámara se dibujan los edificios reales (huella × pisos × 3 m) con fachadas, ventanas y techos procedurales (ilustrativos); lejos, la volumetría por manzana. Las vías salen de una máscara de manzanas cada 8 m.

### 6.2 Topografía: curvas de nivel oficiales
- **Fuente:** `pot_2014:bcs_curvas_nivel` (IDESC): 3.523 curvas **cada 10 m**, con su cota. Se descartan las cotas 0 y 500, que no existen en Cali. Se usaron 3.516.
- **Método** (`prototipo/scripts/topografia.py`): las curvas se dibujan en una grilla de 20 m y el espacio entre ellas se llena con **interpolación armónica** (ecuación de Laplace, de la malla gruesa a la fina, solo con numpy). La superficie pasa exactamente por las curvas y no inventa picos.
- **Resultado:** el SRTM sale en promedio **8,8 m más alto** que las curvas (p5 −31 m, p95 +4 m), porque el radar mide copas de árboles y techos. Fuera de la cobertura de las curvas (la franja oriental, al otro lado del Cauca) se usa el SRTM corregido en **−3,3 m**, que es la diferencia mediana en el valle. Las curvas cubren el 66 % de la caja.
- **Consultado y descartado:** el modelo de elevación municipal `raster:dem_modelo_elevacion_digital` existe en el WMS de la IDESC, pero el WCS no lo publica, así que solo se obtiene como imagen y no con valores de altura.

### 6.3 Sismo con magnitud a elección
- **Intensidad:** Allen, Wald y Worden (2012), *Intensity attenuation for active crustal regions*, J. Seismology 16:409-433, versión con distancia hipocentral. Los coeficientes se tomaron del código de OpenQuake (Fundación GEM, clase `AllenEtAl2012Rhypo`): c0 = 2,085; c1 = 1,428; c2 = −1,402; c4 = 0,078; m1 = −0,209; m2 = 2,042. Fuente del código: https://github.com/gem/oq-engine/blob/master/openquake/hazardlib/gsim/allen_2012_ipe.py
- **Daño por edificio:** método macrosísmico de Lagomarsino y Giovinazzi (2006): μD = 2,5·[1 + tanh((I + 6,25·V − 13,1)/Q)], con grados 0-5 de la escala EMS-98 y distribución binomial. Vulnerabilidad **supuesta por pisos**: 1-2 pisos, clase B (V = 0,74); 3-5 pisos, clase C (0,58); 6 o más, clase D (0,42). Q = 2,3 (2,6 en la clase D). Valores **(verificar)** con el artículo original.
- **Ajustes:** suelo blando (zonas de licuación o corrimiento) +0,5 grados (supuesto). Los sismos profundos (50 km o más) llevan **+0,7 grados**, calibrados para que el sismo real dé intensidad VI en el centro de Cali. La ecuación es para sismos corticales y con el sismo real daba V; el SGC reportó intensidades de hasta VII.
- **Sismo real de referencia:** solución del SGC, 4,99° N y −76,29° O, 103 km de profundidad, Mw 7,4 (San José del Palmar, Chocó). El USGS da 4,844° N, −76,242° O y 108-110 km. Queda a 172 km del centro de Cali (201 km hasta el hipocentro).
- **Validación con lo ocurrido:** con el sismo real, el modelo estima **834 edificaciones con daño muy grave o colapso**, y la UNGRD reportó **879 viviendas destruidas** en Cali (corte del 17-sep). En daño moderado o importante **sobrestima**: 74.328 contra 16.357 averiadas. Las cifras no son del todo comparables (viviendas frente a edificaciones), pero la escala del daño grave coincide.
- **Pruebas:** `maqueta3d/scripts/sismo.test.mjs` (4).

### 6.4 Inundación: corrección
- El polígono «Área prioritaria para estudio» (30 km²) no es un nivel de amenaza y ya **no se inunda** en la simulación. Antes se contaba como amenaza alta.
- Las zonas de amenaza «mitigable» están protegidas por obras como el jarillón: la simulación muestra qué pasaría si esas protecciones fallan.
- Profundidad representativa de cada rango del POT: baja 0,3 m, media 0,7 m y alta 1,5 m. Resultado: **221.830** edificaciones en zona de inundación (170.848 alta, 26.845 media y 24.137 baja).

### 6.5 Direcciones de los edificios
- **Fuente:** `dapm:pdt_nmc_nomenclatura_domiciliaria` (IDESC), **692.389** direcciones, con corte del 3-sep-2026. Solo se descargan la dirección, el barrio y la comuna; ni NPN, ni predio, ni ningún otro identificador. Esta capa exige `sortBy` para paginar.
- **Asignación:** dirección más cercana a 30 m o menos del centro de cada edificio: **91 %** de los edificios (574.637). Al hacer clic en un edificio o en un cono de daño se ven la dirección, el barrio, los pisos, la huella y el resultado del escenario, con la advertencia de que es una estimación y no una evaluación.

### 6.6 APIs externas (claves fuera del repositorio)
- **NASA FIRMS:** focos de calor de los últimos 5 días (el máximo por consulta es 5; con 10 responde «Invalid day range»). Al armar el archivo hubo **1 foco** en la caja (6-oct, VIIRS SNPP, sureste). Se ofrece como punto de inicio del ejercicio de incendio.
- **Mapillary:** foto de calle más cercana a 70 m o menos de cada espacio candidato: **1.088 de 1.442** tienen foto (311 de 2024 en adelante). La caja de búsqueda debe ser pequeña: con 1 km responde «Please reduce the amount of data». El HTML solo trae el enlace público, no el token.
- **Nominatim (OpenStreetMap):** no respondió desde el servidor (respuesta vacía). Se ubicó con la nomenclatura y el inventario.

### 6.7 Albergues: reales frente a sugeridos

**Albergues reales tras el sismo** (curados el 8-oct; `prototipo/scripts/albergues_direcciones.py`):

| Lugar | Tipo | Ubicación | Fuente |
|---|---|---|---|
| Coliseo de Hockey Miguel Calero (Canchas Panamericanas), Cl 9 con Kr 37A/39 | Oficial: 146 cupos, unas 60 familias | Inventario IDESC | [Alcaldía 12-ago](https://www.cali.gov.co/boletines/publicaciones/193628/alcaldia-de-cali-refuerza-la-atencion-integral-a-familias-afectadas-por-el-sismo-mediante-la-disposicion-de-albergues-temporales/), [RCN](https://newsroom.rcnradio.com/colombia/cali-estos-son-los-centros-de-acopio-y-albergues-habilitados-tras-el-terremoto-de-7-4-en-colombia-conoce-que-ayudas-se-necesitan), [El País](https://www.elpais.com.co/cali/terremoto-en-cali-estos-son-los-lugares-habilitados-para-recibir-a-los-damnificados-1038.html) |
| Diamante de Béisbol, Kr 39 con Cl 9 | Oficial (anunciado el 11-ago) | Inventario IDESC | El País, RCN |
| Unidad Deportiva Jaime Aparicio | Albergue, acopio y descanso de rescatistas | Aproximada (complejo) | El País |
| Escuela Nacional del Deporte, Cl 9 # 34-01 | Centro de acopio | Nomenclatura domiciliaria | RCN |
| Plazoleta Jairo Varela, Av 2N # 10N-1 | Centro de acopio | Aproximada (sin placa propia) | RCN |
| Chiminango I, Chiminango II, Calimio Norte (sector Ramalí) | Autogestionados: 336 hogares (1.046 personas) al 18-ago | Aproximada (centro del barrio) | [Defensoría](https://www.defensoria.gov.co/web/guest/-/defensoria-pide-atencion-urgente-para-336-familias-en-albergues-de-cali?redirect=%2F), [AFP](https://albertonews.com/internacionales/la-lluvia-amenaza-los-albergues-improvisados-de-cali-no-tenemos-a-donde-ir/) |
| Altos de Santa Elena | Autogestionado (carpas) | Aproximada (centro del barrio) | Alcaldía, [Occidente](https://occidente.co/cali/albergues-de-cali-tras-sismo-control-subsidios-arriendo/) |
| Iglesia Reyes y Sacerdotes | Familias de Altos de Santa Elena | Sin ubicación publicada | Alcaldía |

Cifras generales: Cali tuvo unos 12 albergues (2 oficiales y 10 autogestionados) y **más de 2.800 personas** a los diez días del sismo ([Minuto30](https://www.minuto30.com/terremoto-damnificados-albergues-cali/1716443/)); 194 personas en los institucionales a la semana ([El País](https://www.elpais.com.co/cali/confirman-que-194-personas-siguen-en-albergues-tras-terremoto-en-cali-alcaldia-evalua-edificaciones-afectadas-1759.html)).

**Hallazgos del cruce con las capas oficiales:**
- **Chiminango I, Chiminango II y Calimio Norte quedaron en zonas de amenaza de inundación** (alta y media, protegidas por el jarillón) **y de licuación o corrimiento.** En otro sismo con réplicas o con lluvias fuertes serían de los lugares menos seguros para un albergue. Coincide con la alerta de la Defensoría.
- **Altos de Santa Elena** está en una ladera con **38,6 % de pendiente** (modelo de curvas), no apta para carpas.
- Los dos albergues oficiales (hockey y diamante) están en terreno plano (0,5-1,5 %) y fuera de las zonas de amenaza.

**Idoneidad de un espacio** (`maqueta3d/src/albergues.ts`, con 3 pruebas): puntaje de 0 a 100 con cinco criterios y pesos a la vista:
- **Demanda (35 %):** edificaciones afectadas a menos de 1,5 km, frente al percentil 90 del caso.
- **Capacidad (20 %):** 45 m² por persona, cifra de las normas Esfera para asentamientos tipo campamento **(verificar)**.
- **Seguridad (20 %):** se descartan los espacios que cruzan la amenaza; en el sismo se castigan los que tienen colapsos estimados a unos 100 m, y en el incendio los que están a menos de 1 km del área quemada.
- **Pendiente (15 %):** ideal hasta 2 %, no apta desde 8 % (supuesto).
- **Salud (10 %):** IPS del REPS y equipamientos de salud de la IDESC.

La dotación usa las reglas del proyecto: kit de 20 personas, 1 baño por cada 20 y 15 L por persona al día.

**Todos los casos** (7: inundación; sismo real; sismos hipotéticos bajo Cali de Mw 6,5 y 7,0; incendio desde Cristo Rey, Tres Cruces y Pichindé): los espacios que más se repiten entre los 10 mejores son los Parques **Torres de Comfandi** (comuna 5), **Ciudad de Los Álamos** (comuna 2) y **Olímpico** (comuna 10), cada uno en 3 de los 7 casos. Son los primeros candidatos para preparar con anticipación.

### 6.8 Albergue armado y realidad aumentada
- **En la maqueta:** «Ver albergue montado» arma el sitio con los **kits del proyecto** (`maqueta3d/src/data/site.ts`): cubierta de 10 × 7 m a 3 m de altura con 5 particiones de 2 × 2 × 2 m (20 personas por kit), baños de 1,2 × 1,2 × 2,3 m, tanques, módulos de NNA y de salud de 5 × 3,5 × 2,5 m y registro de 4 × 3 m. La disposición es ilustrativa.
- **Realidad aumentada:** «Realidad aumentada» exporta un módulo de 100 personas a GLB y lo abre en `model-viewer` 4.3.1 (Google, desde jsDelivr; necesita internet). En Android con ARCore (WebXR) o en iPhone (Quick Look), el modelo se pone a escala real sobre el piso a través de la cámara. Abierto en el sitio, se ve el albergue en su lugar real.
