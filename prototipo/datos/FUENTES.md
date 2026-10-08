# Fuentes de los datos

Todos los archivos de `raw/` se descargaron el **25 de septiembre de 2026** de las URL que aparecen abajo. La versión para máquinas (para Sheets) está en `fuentes.csv`. Las URL WFS devuelven la capa completa en GeoJSON (EPSG:4326), así que para actualizar un archivo basta con volver a descargarlo desde su URL.

**Atribución obligatoria (CC BY / CC BY-SA):** "Fuente: Alcaldía de Santiago de Cali - DAPM / IDESC, datos.cali.gov.co". Los derivados de `procesados/` se publican con **CC BY-SA 4.0**. Para los daños del sismo: "© Copernicus EMS EMSR916", "© ICube-SERTIT 2026 / International Charter", "Microsoft AI for Good / Airbus, vía HDX".


## IDESC: servicio WFS de la Alcaldía de Cali

### Comunas de Santiago de Cali (Acuerdo 0636 de 2026)
- **Archivo:** `raw/idesc/pdt_dpa_comunas.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://www.datos.gov.co/dataset/Comunas-de-Santiago-de-Cali/dx2g-2mhm
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=dapm:pdt_dpa_comunas&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY
- **Nota:** Servicio WFS de la IDESC, capa dapm:pdt_dpa_comunas

### Barrios y sectores de Santiago de Cali
- **Archivo:** `raw/idesc/pdt_dpa_barrios_sectores.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://datos.cali.gov.co/dataset/servicio-wms-barrios-de-cali
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=dapm:pdt_dpa_barrios_sectores&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY
- **Nota:** Servicio WFS de la IDESC, capa dapm:pdt_dpa_barrios_sectores

### EPOU - Espacio Público Efectivo
- **Archivo:** `raw/idesc/epou_epu_espacio_publico_efectivo.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://datos.cali.gov.co/dataset/epou-espacio-publico-efectivo
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=dapm:epou_epu_espacio_publico_efectivo&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa dapm:epou_epu_espacio_publico_efectivo

### Escenarios deportivos (puntos)
- **Archivo:** `raw/idesc/escenarios_deportivos.geojson`
- **Entidad:** Secretaría del Deporte y la Recreación
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=deporte_recreacion:escenarios_deportivos&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa deporte_recreacion:escenarios_deportivos

### POT - Equipamientos de deporte
- **Archivo:** `raw/idesc/eqp_uba_deporte.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=pot_2014:eqp_uba_deporte&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa pot_2014:eqp_uba_deporte

### POT - Equipamientos de educación
- **Archivo:** `raw/idesc/eqp_uco_educacion.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=pot_2014:eqp_uco_educacion&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa pot_2014:eqp_uco_educacion

### POT - Equipamientos de salud
- **Archivo:** `raw/idesc/eqp_uco_salud.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://datos.cali.gov.co/dataset/pot-salud
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=pot_2014:eqp_uco_salud&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa pot_2014:eqp_uco_salud

### Establecimientos educativos
- **Archivo:** `raw/idesc/esf_establecimiento_educativo.geojson`
- **Entidad:** Secretaría de Educación
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=educacion:esf_establecimiento_educativo&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa educacion:esf_establecimiento_educativo

### Microzonificación sísmica de Cali
- **Archivo:** `raw/idesc/mc_microzonificacion_sismica.geojson`
- **Entidad:** DAPM / IDESC
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=idesc:mc_microzonificacion_sismica&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa idesc:mc_microzonificacion_sismica

### Zonas susceptibles a licuación
- **Archivo:** `raw/idesc/mc_susceptible_licuacion.geojson`
- **Entidad:** DAPM / IDESC
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=idesc:mc_susceptible_licuacion&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa idesc:mc_susceptible_licuacion

### POT - Efectos sísmicos (licuación y corrimiento lateral)
- **Archivo:** `raw/idesc/amb_ari_efectos_sismicos.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://datos.cali.gov.co/dataset/efectos-sismicos
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=pot_2014:amb_ari_efectos_sismicos&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa pot_2014:amb_ari_efectos_sismicos

### POT - Inundación fluvial
- **Archivo:** `raw/idesc/amb_ari_inundacion_fluvial.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://datos.cali.gov.co/dataset/inundacion-fluvial
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=pot_2014:amb_ari_inundacion_fluvial&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa pot_2014:amb_ari_inundacion_fluvial

### POT - Inundación pluvial
- **Archivo:** `raw/idesc/amb_ari_inundacion_pluvial.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://datos.cali.gov.co/dataset/inundacion-pluvial
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=pot_2014:amb_ari_inundacion_pluvial&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa pot_2014:amb_ari_inundacion_pluvial

### POT - Zonas de desbordamiento Tr 50 años
- **Archivo:** `raw/idesc/amb_ari_amenaza_desborde_creciente.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://datos.cali.gov.co/dataset/zonas-de-desbordamiento-con-periodos-de-retorno-de-50-anos
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=pot_2014:amb_ari_amenaza_desborde_creciente&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa pot_2014:amb_ari_amenaza_desborde_creciente

### POT - Diques (incluye Jarillón del río Cauca)
- **Archivo:** `raw/idesc/amb_ari_diques.geojson`
- **Entidad:** DAPM
- **Página de la fuente:** https://datos.cali.gov.co/dataset/diques
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=pot_2014:amb_ari_diques&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa pot_2014:amb_ari_diques

### Amenaza no mitigable por inundación (río Cauca y tributarios)
- **Archivo:** `raw/idesc/emc_amb_ari_amenaza_no_mitigable_inundacion.geojson`
- **Entidad:** DAPM - Expediente municipal
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=expediente_municipal:emc_amb_ari_amenaza_no_mitigable_inundacion&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa expediente_municipal:emc_amb_ari_amenaza_no_mitigable_inundacion

### IPS y capacidad instalada (REPS)
- **Archivo:** `raw/idesc/ads_ips_capacidad_reps.geojson`
- **Entidad:** Secretaría de Salud Pública
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=salud:ads_ips_capacidad_reps&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa salud:ads_ips_capacidad_reps

### Organismos de acción comunal (JAC)
- **Archivo:** `raw/idesc/pfp_ivc_organismos_accion_comunal.geojson`
- **Entidad:** Secretaría de Desarrollo Territorial y Participación Ciudadana
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=desarrollo_territorial_pc:pfp_ivc_organismos_accion_comunal&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa desarrollo_territorial_pc:pfp_ivc_organismos_accion_comunal

### Barrios precarios (PMIH)
- **Archivo:** `raw/idesc/pmih_barrios_precarios.geojson`
- **Entidad:** Secretaría de Vivienda Social y Hábitat
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=vivienda:pmih_barrios_precarios&outputFormat=application/json&srsName=EPSG:4326
- **Licencia:** CC BY-SA
- **Nota:** Servicio WFS de la IDESC, capa vivienda:pmih_barrios_precarios


## Datos Abiertos Cali (CKAN)

### Escenarios Deportivos de Santiago de Cali (atributos)
- **Archivo:** `raw/cali_abiertos/escenarios_deportivos.csv`
- **Entidad:** Secretaría del Deporte y la Recreación
- **Página de la fuente:** https://datos.cali.gov.co/dataset/escenarios-deportivos-de-santiago-de-cali
- **Descarga:** https://datos.cali.gov.co/dataset/bcd91741-d1e7-4fd6-be0e-87a428cab94b/resource/de4a23e6-2440-47ec-bdc1-cac61c5f2ad8/download/escenarios-deportivos.csv
- **Licencia:** CC BY-SA
- **Nota:** Codificación latin1, separador ;

### Ubicación de organismos de socorro y de la Secretaría de Gestión del Riesgo 2024
- **Archivo:** `raw/cali_abiertos/organismos_socorro.csv`
- **Entidad:** Secretaría de Gestión del Riesgo
- **Página de la fuente:** https://datos.cali.gov.co/dataset/ubicacion-organismos-de-socorro-y-secretaria-de-gestion-de-riesgo-2024
- **Descarga:** https://datos.cali.gov.co/dataset/02c6222a-136d-41f1-9c62-efd580a5afcb/resource/0950db10-b61d-4bc8-ad2f-7be7868fad32/download/dato_7_ubicaciones_organismos_socorro.csv
- **Licencia:** CC BY
- **Nota:** Separador |

### Intervenciones del Plan Jarillón: demoliciones y liberación de áreas, 2014-2024
- **Archivo:** `raw/cali_abiertos/plan_jarillon_intervenciones.csv`
- **Entidad:** Secretaría de Gestión del Riesgo
- **Página de la fuente:** https://datos.cali.gov.co/dataset/casas-demolidas-en-el-jarillon-de-cali-durante-el-periodo-2014-al-2024
- **Descarga:** https://datos.cali.gov.co/dataset/d643f5a3-edd3-449f-8c8f-0006d62e76e9/resource/f1bfcae7-89d2-4784-8bdf-0d3a1c5abf3b/download/dato_4_intervenciones_plan_jarillon.csv
- **Licencia:** CC BY-SA
- **Nota:** Separador |

### Proyecciones de población de Cali por comuna y corregimiento 2006-2020
- **Archivo:** `raw/cali_abiertos/poblacion_comuna_2006_2020.csv`
- **Entidad:** DAPM
- **Página de la fuente:** https://datos.cali.gov.co/dataset/proyecciones-de-poblacion-de-cali-por-comuna-y-corregimiento-2006-2020
- **Descarga:** https://datos.cali.gov.co/dataset/8fb07a43-4033-437e-8db0-e1474937ecae/resource/63f3e50e-0452-49cf-993d-08dfc2842cb4/download/proyecciones_de_poblaci_n_de_cali_por_comuna_y_corregimiento__2006-2020.csv
- **Licencia:** CC BY-SA
- **Nota:** Desactualizada: última proyección 2020

### Estratificación socioeconómica urbana por comunas, 2015
- **Archivo:** `raw/cali_abiertos/estrato_moda_comuna_2015.csv`
- **Entidad:** DAPM
- **Página de la fuente:** https://datos.cali.gov.co/dataset/estratificacion-socioeconomica-urbana-por-comunas-en-cali-ano-2015
- **Descarga:** https://datos.cali.gov.co/dataset/89db273a-dcd0-459c-b995-621dbf1f94c9/resource/88f7450b-59d7-42f5-aaa3-010dbca9976b/download/estratificaci_n_socioecon_mica_urbana_por_comunas_en_cali_a_o_2015.csv
- **Licencia:** CC BY-SA


## Sismo del 10 de agosto de 2026

### Copernicus EMS EMSR916 - AOI01 Northern Cali, evaluación de daños (GRA v2)
- **Archivo:** `raw/sismo/EMSR916_AOI01_GRA_PRODUCT_v2.zip`
- **Entidad:** Copernicus Emergency Management Service (UE)
- **Página de la fuente:** https://rapidmapping.emergency.copernicus.eu/EMSR916/
- **Descarga:** https://rapidmapping.emergency.copernicus.eu/backend/EMSR916/AOI01/GRA_PRODUCT/EMSR916_AOI01_GRA_PRODUCT_v2.zip
- **Licencia:** Copernicus: uso libre con atribución
- **Nota:** Fotointerpretación; incluye un mapa en PDF

### Copernicus EMS EMSR916 - AOI03 Cali Center, evaluación de daños (GRA v1)
- **Archivo:** `raw/sismo/EMSR916_AOI03_GRA_PRODUCT_v1.zip`
- **Entidad:** Copernicus Emergency Management Service (UE)
- **Página de la fuente:** https://rapidmapping.emergency.copernicus.eu/EMSR916/
- **Descarga:** https://rapidmapping.emergency.copernicus.eu/backend/EMSR916/AOI03/GRA_PRODUCT/EMSR916_AOI03_GRA_PRODUCT_v1.zip
- **Licencia:** Copernicus: uso libre con atribución
- **Nota:** Fotointerpretación; incluye un mapa en PDF

### Daños ICube-SERTIT / International Charter, AOI07 Cali (filtrado a Cali)
- **Archivo:** `raw/sismo/sertit_danos.csv`
- **Entidad:** ICube-SERTIT (Univ. de Estrasburgo), vía monitor-terremoto-colombia
- **Página de la fuente:** https://sertit.unistra.fr/cartographie-rapide/cartoaction/845/
- **Descarga:** https://raw.githubusercontent.com/18orkidea/monitor-terremoto-colombia/HEAD/data/dumps/sertit_danos.csv
- **Licencia:** Fuente primaria: atribución a ICube-SERTIT; el repositorio intermedio no declara licencia
- **Nota:** Vectores originales: data/documentos/sertit/CHARTER_CALL1202_ID1048_AOI07_COLOMBIA_CALI_IMPACTMAP_20260810_SCALE7500_A1_ICube-SERTIT_en_vectors.zip en https://github.com/18orkidea/monitor-terremoto-colombia

### Daños detectados por modelo de IA sobre huellas de edificios (filtrado a Cali)
- **Archivo:** `raw/sismo/msft_danos.csv`
- **Entidad:** Microsoft AI for Good + Airbus, publicado en HDX; vía monitor-terremoto-colombia
- **Página de la fuente:** https://data.humdata.org/dataset/98e2bb4b-e2b9-4178-bf47-826883ca08cc
- **Descarga:** https://raw.githubusercontent.com/18orkidea/monitor-terremoto-colombia/HEAD/data/dumps/msft_danos.csv
- **Licencia:** HDX (verificar la licencia del dataset)
- **Nota:** Fuente original: airbus_8-10_cali_hdx_building_footprints_with_predictions_validated.gpkg en HDX

### Índice de recursos de Microsoft/Airbus en HDX
- **Archivo:** `raw/sismo/msft_recursos.csv`
- **Entidad:** Microsoft AI for Good, vía monitor-terremoto-colombia
- **Página de la fuente:** https://data.humdata.org/dataset/98e2bb4b-e2b9-4178-bf47-826883ca08cc
- **Descarga:** https://raw.githubusercontent.com/18orkidea/monitor-terremoto-colombia/HEAD/data/dumps/msft_recursos.csv
- **Licencia:** HDX (verificar)
- **Nota:** Trae la URL de descarga directa de cada archivo en HDX

### Sedes educativas con estado físico tras el sismo (filtrado a Cali, cod_mun 76001)
- **Archivo:** `raw/sismo/men_sedes.csv`
- **Entidad:** Ministerio de Educación Nacional (SISE), vía monitor-terremoto-colombia
- **Página de la fuente:** https://mineducacion.maps.arcgis.com/apps/dashboards/5e47f09f3b374396a5b3be15e8e96192
- **Descarga:** https://raw.githubusercontent.com/18orkidea/monitor-terremoto-colombia/HEAD/data/dumps/men_sedes.csv
- **Licencia:** Información pública del MEN
- **Nota:** Reporte administrativo de las secretarías de educación, no una evaluación estructural

### IPS con daños según los SitRep 1-6 de la OPS (filtrado a Cali)
- **Archivo:** `raw/sismo/ops_salud_ips.csv`
- **Entidad:** Organización Panamericana de la Salud, vía monitor-terremoto-colombia
- **Página de la fuente:** https://github.com/18orkidea/monitor-terremoto-colombia/tree/HEAD/data/documentos/ops_salud
- **Descarga:** https://raw.githubusercontent.com/18orkidea/monitor-terremoto-colombia/HEAD/data/dumps/ops_salud_ips.csv
- **Licencia:** Información pública de la OPS
- **Nota:** Filas repetidas por SitRep

### Cruce Copernicus vs. prensa y reportes por AOI
- **Archivo:** `raw/sismo/crosscheck.csv`
- **Entidad:** datosdelterremoto.org
- **Página de la fuente:** https://datosdelterremoto.org/municipio/cali/
- **Descarga:** https://datosdelterremoto.org/data/public/crosscheck.csv
- **Licencia:** Sin licencia declarada


## Consultados sin guardar o sin descarga directa

### RUD - Registro Único de Damnificados, serie diaria por municipio
- **Archivo:** `(no guardado) rud.json`
- **Entidad:** UNGRD, capturado por datosdelterremoto.org
- **Página de la fuente:** https://rud.gestiondelriesgo.gov.co/
- **Descarga:** https://datosdelterremoto.org/data/public/rud.json
- **Licencia:** Información pública
- **Nota:** Cali: 45.138 familias, 97.337 personas, 879 viviendas destruidas y 16.357 averiadas (corte al 17-sep-2026)

### Monitor del terremoto: AOIs, exposición y activaciones
- **Archivo:** `(no guardado) monitor.json`
- **Entidad:** datosdelterremoto.org
- **Página de la fuente:** https://datosdelterremoto.org/
- **Descarga:** https://datosdelterremoto.org/data/public/monitor.json
- **Licencia:** Sin licencia declarada

### Nivel instantáneo de ríos (IDEAM)
- **Archivo:** `(consulta) IDEAM nivel instantáneo`
- **Entidad:** IDEAM, en datos.gov.co
- **Página de la fuente:** https://www.datos.gov.co/resource/bdmn-sqnh
- **Descarga:** https://www.datos.gov.co/resource/bdmn-sqnh.json
- **Licencia:** Datos abiertos
- **Nota:** En Cali solo trae la estación La Vorágine; no incluye Juanchito

### Nivel del río Cauca en Juanchito, informes diarios GEOCVC
- **Archivo:** `(consulta) CVC Juanchito`
- **Entidad:** CVC
- **Página de la fuente:** https://portal-hidroclimatologico.cvc.gov.co/
- **Licencia:** Pública
- **Nota:** No tiene API: se copia a mano

### Capacidades del servicio WFS de la IDESC (lista de capas)
- **Archivo:** `(consulta) catálogo IDESC`
- **Entidad:** IDESC
- **Página de la fuente:** https://idesc.cali.gov.co
- **Descarga:** https://ws-idesc.cali.gov.co/geoserver/ows?service=WFS&version=1.0.0&request=GetCapabilities
- **Licencia:** 
- **Nota:** Sirve para descubrir más capas

### API CKAN de Datos Abiertos Cali
- **Archivo:** `(consulta) API del portal`
- **Entidad:** Alcaldía de Cali
- **Página de la fuente:** https://datos.cali.gov.co
- **Descarga:** https://datos.cali.gov.co/api/3/action/package_search?q=
- **Licencia:** 
- **Nota:** Búsqueda de datasets


## Portales y referencias de contexto
- Datos Abiertos Cali: https://datos.cali.gov.co
- Geoportal IDESC: https://idesc.cali.gov.co · Guía del geovisor: https://idesc.cali.gov.co/download/guias/guia_manejo_geovisor_idesc.pdf
- Datos Abiertos Colombia: https://www.datos.gov.co
- Copernicus EMSR916: https://rapidmapping.emergency.copernicus.eu/EMSR916/
- International Charter / SERTIT: https://sertit.unistra.fr/cartographie-rapide/cartoaction/845/
- UNITAR-UNOSAT, producto 4250: http://unosat.org/products/4250
- Observatorio datosdelterremoto.org (Cali): https://datosdelterremoto.org/municipio/cali/ · RUD: https://datosdelterremoto.org/rud.html
- Repositorio del observatorio: https://github.com/18orkidea/monitor-terremoto-colombia
- RUD de la UNGRD: https://rud.gestiondelriesgo.gov.co/
- Tablero del MEN (sedes afectadas): https://mineducacion.maps.arcgis.com/apps/dashboards/5e47f09f3b374396a5b3be15e8e96192
- Repositorio oficial del terremoto (Alcaldía): https://www.cali.gov.co/gobierno/publicaciones/193607/terremoto-de-cali-repositorio-oficial-de-informacion/
- Balance de la Alcaldía del 23 de septiembre (El País): https://www.elpais.com.co/cali/alcaldia-de-cali-entrega-balance-de-gestion-tras-el-sismo-mas-de-3400-edificaciones-evaluadas-y-45000-familias-damnificadas-2338.html
- Cifras del sismo (Semana): https://www.semana.com/nacion/cali/articulo/sismo-en-cali-revelan-nuevas-cifras-de-damnificados-heridos-y-edificaciones-afectadas/202634/
- Sectores más afectados (El País): https://www.elpais.com.co/cali/cali-antes-y-despues-del-terremoto-asi-cambiaron-los-sectores-mas-afectados-desgarradoras-imagenes-1636.html
- Balance inicial (Infobae): https://www.infobae.com/colombia/2026/08/11/mas-de-130-muertos-570-heridos-viviendas-y-vias-danadas-y-aeropuertos-cerrados-las-dramaticas-cifras-que-deja-hasta-ahora-el-terremoto-en-colombia/
- Portal hidroclimatológico de la CVC: https://portal-hidroclimatologico.cvc.gov.co/
- El río Cauca superó su caudal histórico en Juanchito (CVC): https://www.cvc.gov.co/carousel/2781-en-juanchito-el-rio-cauca-supero-su-maximo-caudal-historico


## Maqueta y escenarios suministrados por el equipo (8 de octubre de 2026)

Archivo aportado: `/home/ijoan/proyectos/simulacion_ciudad_cali.zip`. Original preservado: `frontend/simulation-source/simulacion_ciudad_cali.html`; método y URLs declaradas por el autor: `frontend/simulation-source/FUENTES_Y_METODO.md`. Se integran geometría/relieve y agregados catastrales, sin nombres ni identificadores de predios. No se efectuó una nueva descarga completa ni certificación de los datos del ZIP.

- Catastro: `catastro:cat_bas_manzanas` y `catastro:cat_bas_construcciones`, página https://idesc.cali.gov.co ; descarga declarada mediante WFS https://ws-idesc.cali.gov.co/geoserver/wfs?service=WFS&version=2.0.0&request=GetFeature&outputFormat=application/json&srsName=EPSG:4326&typeNames=catastro:cat_bas_manzanas . Licencia no declarada: por verificar según autor.
- Ríos y cobertura: `pot_2014:bcs_hid_rios` y `pot_2014:amb_eep_aeie_cobertura_boscosa`, WFS del mismo servidor; origen y licencia atribuidos al documento del ZIP. Cobertura boscosa no equivale a amenaza oficial de incendio.
- Relieve: https://registry.opendata.aws/terrain-tiles/ ; teselas https://s3.amazonaws.com/elevation-tiles-prod/terrarium/13/{x}/{y}.png ; atribución por origen: https://github.com/tilezen/joerd/blob/master/docs/attribution.md . Registro oficial consultado el 08/10/2026; no se redescargaron teselas.
- Capas de amenaza y daños: reutilizadas por el autor a partir del catálogo existente; la geometría del ejercicio no reemplaza evaluación técnica.
