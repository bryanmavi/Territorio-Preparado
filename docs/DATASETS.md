# Datos reales para Cali Activa (alcance: Santiago de Cali)

**Actualizado al 25 de septiembre de 2026.** Decisión del equipo: **el prototipo usa datos reales y públicos de Cali, no simulados.** Solo el IoT del kit de PVC sigue simulado, y así se marca en la demo.

**Todas las URL de descarga, las páginas de origen y las licencias de cada archivo están en [`prototipo/datos/FUENTES.md`](../prototipo/datos/FUENTES.md)** (y en `fuentes.csv`).

Los datos están en `prototipo/datos/raw/` (fuentes originales) y `prototipo/datos/procesados/` (cruces). Los scripts, en Python puro y sin dependencias, están en `prototipo/scripts/`:

```bash
python3 prototipo/scripts/afectacion_por_comuna.py   # daños del sismo → comuna y barrio
python3 prototipo/scripts/inventario_espacios.py     # 1.970 espacios × amenazas
python3 prototipo/scripts/resumen_comunas.py         # tabla multiamenaza por comuna
```

## 1. Zonas más afectadas por el sismo del 10 de agosto de 2026 (M7.4)

**Cifras oficiales de Cali:**
- RUD de la UNGRD con corte al 17 de septiembre: 45.138 familias (97.337 personas), 879 viviendas destruidas y 16.357 averiadas.
- Balance de la Alcaldía al 23 de septiembre: 3.403 edificaciones evaluadas (1.078 con sticker rojo, 1.272 amarillo y 1.053 verde), 333 personas en alojamientos temporales y 154 fallecidos (repositorio oficial, corte del 8 de septiembre).

**Por comuna.** Hay 1.090 puntos de daño georreferenciados y cruzados con las comunas del Acuerdo 0636 de 2026:

| # | Comuna | Destruidos | Dañados | Sedes educativas afectadas | Índice* | Barrios más golpeados |
|---|---|---|---|---|---|---|
| 1 | **19** | 7 | 26 | 6 | 170 | Nueva Tequendama, Tequendama, Cuarto de Legua–Guadalupe, El Refugio (edificios Cantabria, Ana Pilar, Vanessa en Los Cámbulos) |
| 2 | **20** | – | – | 1 | 53 | Siloé, Brisas de Mayo, Belén, Lleras Camargo (ladera, estrato 1) |
| 3 | **2** | – | – | 0 | 37 | Altos de Menga, Santa Mónica, La Flora |
| 4 | **13** | – | – | 5 | 35,5 | Laguna del Pondaje, El Poblado II, Los Lagos |
| 5 | **9** | 4 | 5 | 6 | 34 | Barrio Obrero, Sucre, Guayaquil, Bretaña |
| 6 | 1 | – | – | 7 | 29 | Terrón Colorado, Vista Hermosa |
| 7 | 6 | 0 | 2 | 0 | 28 | Floralia, Paso del Comercio, Calimio |
| 8 | 3 | 4 | 1 | 1 | 25,5 | San Juan Bosco, Santa Rosa, San Pascual |
| 9 | 10 | 1 | 2 | 10 | 22,5 | Olímpico (apartahotel Molino Rojo), Cristóbal Colón, Pasoancho |

\* El índice pondera el grado de daño: destruido = 3, dañado = 2, posible = 1, sede educativa con reporte = 1 y detección del modelo de IA = 0,5. Es una **medida relativa**, no una cifra oficial.

> **Sesgo de cobertura, hay que decirlo en el pitch:** los satélites solo cubrieron algunas zonas. Copernicus mapeó el norte y el centro (AOI01 y AOI03), SERTIT el sur (AOI07, por eso la comuna 19 pesa tanto) y el modelo de Microsoft y Airbus solo su área válida. Una comuna sin puntos **no significa que no tuvo daño**. Falta el RUD por barrio (ver la sección 4).

## 2. Lo que dicen los datos: Cali tiene dos mapas de riesgo distintos

Cruce de los 1.970 espacios públicos con el POT (`procesados/resumen_comunas_multiamenaza.csv`):

- **Occidente y sur (comunas 1, 3, 9, 17, 18, 19 y 20):** allí se concentró el **daño sísmico real**. Sus espacios **no tienen amenaza de inundación ni son licuables**, así que son **aptos como albergue ante un sismo**. Ejemplos: 31 espacios de más de 5.000 m² en la comuna 19 (La Cascada, 23.094 m²; Nueva Tequendama, 22.532 m²) y 11 en la comuna 3 (loma de San Antonio, 36.782 m²).
- **Oriente, sobre el Jarillón (comunas 6, 7, 13, 14 y 21):** entre el 55 y el 92 % de los espacios tiene **amenaza alta de inundación** y entre el 92 y el 100 % está en **suelo licuable** (zona sísmica 6). En la comuna 15, el 19 % tiene amenaza alta y el 100 % es licuable. Además, 185 espacios quedan a menos de 500 m del dique del río Cauca. Allí **ningún espacio grande sirve de albergue** ni ante sismo ni ante inundación. Su papel es de **amortiguación**, o de punto de agua durante una sequía.
- **Validación del hallazgo de la Defensoría:** los parques de **Chiminangos I y II** y de **Calimio**, donde hay albergues autogestionados, tienen amenaza **alta** de inundación y suelo **licuable**. Los parques de Urbanización Calimio están a **entre 72 y 152 m del dique**. Es decir, la gente huyó del sismo hacia el lugar de mayor riesgo de inundación.
- **Déficit:** comunas como la 9 (0,71 m² de espacio público por habitante), la 12 (0,88), la 8 (1,01) y la 13 (1,04) tienen muy poco espacio. La comuna 17 tiene 8,89 m² y la 22 tiene 60,16.

**Consecuencia para el producto:** la misma pregunta ("¿dónde alojo a 300 personas?") tiene respuestas opuestas según la amenaza. Esto ya **no es una suposición: lo demuestran los datos oficiales**.

## 3. Catálogo: lo que ya tenemos (todo público)

| Dataset | Fuente | Registros en Cali | Licencia | Uso en el prototipo |
|---|---|---|---|---|
| Espacio público efectivo (EPOU) | DAPM / IDESC (WFS) | 1.970 parques, zonas verdes y plazas, con área, estado y Street View | CC BY-SA | **Base de la ficha de cada espacio** |
| Escenarios deportivos, puntos | Secretaría de Deporte / IDESC | 1.021 | CC BY-SA | Coliseos y canchas cubiertas (albergue) |
| Escenarios deportivos, atributos | datos.cali.gov.co | 617 | CC BY-SA | Equipamiento (piscinas, canchas, etc.) |
| Comunas y barrios (Acuerdo 0636 de 2026) | IDESC | 22 comunas, 342 barrios | CC BY | Unidad de análisis |
| Inundación fluvial y pluvial del POT | DAPM / IDESC | 423 y 227 polígonos | CC BY-SA | Aptitud ante inundación |
| Amenaza no mitigable por el río Cauca | Expediente municipal / IDESC | 3 | CC BY-SA | Exclusión dura |
| Diques (Jarillón del río Cauca) | POT / IDESC | 11 tramos | CC BY-SA | Distancia al dique |
| Microzonificación sísmica y licuación | IDESC | 16 zonas (Aa, suelos) | CC BY-SA | Aptitud ante sismo |
| Daños por fotointerpretación satelital | Copernicus EMS **EMSR916** (AOI01 y AOI03) | 21 edificios | Copernicus, libre con atribución | Daño real |
| Daños por fotointerpretación satelital | ICube-SERTIT / International Charter (AOI07 Cali) | 94 edificios | Libre con atribución | Daño real |
| Daños detectados por modelo de IA | Microsoft AI for Good + Airbus (HDX) | 887 huellas | HDX (verificar la licencia) | Daño estimado (pesa menos) |
| Sedes educativas con afectación | MEN, SISE | 897 sedes, 101 con reporte | Pública | Daño y sedes que no deben ser albergue |
| IPS con daños | OPS, SitRep 1–6 | 10 IPS (HUV con colapso parcial, Clínica Nuestra evacuada) | Pública | Red de salud disponible |
| IPS y capacidad instalada (REPS) | Secretaría de Salud / IDESC | 1.062 registros | CC BY-SA | Punto de salud más cercano |
| Organismos de socorro | Secretaría de Gestión del Riesgo | Estaciones de bomberos, Cruz Roja, Defensa Civil | CC BY | Quién responde y a qué distancia |
| Organismos de acción comunal (JAC) | IDESC | 182 | CC BY-SA | Contacto comunitario (IRL) |
| Barrios precarios (PMIH) | Secretaría de Vivienda / IDESC | 71 | CC BY-SA | Vulnerabilidad |
| Intervenciones del Plan Jarillón | datos.cali.gov.co | Demoliciones por AHDI, 2014–2024 | CC BY-SA | Contexto del Jarillón |
| Población por comuna, proyección 2020 | DAPM | 22 comunas | CC BY-SA | Personas por m² (**desactualizada**) |
| Estrato moda por comuna, 2015 | DAPM | 22 comunas | CC BY-SA | Vulnerabilidad |
| RUD municipal | UNGRD (vía datosdelterremoto.org) | Total de Cali | Pública | Magnitud |

Los datos intermedios provienen del observatorio [datosdelterremoto.org](https://datosdelterremoto.org/municipio/cali/) ([código](https://github.com/18orkidea/monitor-terremoto-colombia)). El repositorio no declara licencia, así que **en el pitch se cita la fuente primaria** (Copernicus, SERTIT, HDX, MEN, OPS).

## 4. Lo que necesitamos y no es abierto (hay que pedirlo o capturarlo)

| Dato que falta | Para qué | Quién lo tiene | Cómo conseguirlo |
|---|---|---|---|
| **RUD por comuna o barrio**, agregado y sin datos personales | Quitar el sesgo satelital; medir la demanda real de alojamiento | Secretaría de Gestión del Riesgo de Cali / UNGRD | Derecho de petición (Ley 1755 de 2015) invocando la Ley 1712 de 2014, **solo agregados** (Ley 1581) |
| **3.403 evaluaciones de edificaciones** (rojo, amarillo, verde) por barrio | Mapa real del daño; saber dónde hace falta alojamiento | Secretaría de Gestión del Riesgo / DAGRD | Igual que la anterior |
| Alojamientos temporales activos y su ocupación | Estado actual (333 personas) | Alcaldía de Cali; Defensoría (autogestionados) | Repositorio oficial y comunicado de la Defensoría; geocodificar a mano los 4 oficiales (Miguel Calero, Diamante de Béisbol, CIDES Los Pinos, Coliseo Metropolitano Norte) |
| Nivel del río Cauca en **Juanchito**, en tiempo real | Disparar el escenario de inundación | CVC ([portal hidroclimatológico](https://portal-hidroclimatologico.cvc.gov.co/)); IDEAM | La CVC publica un informe diario sin API: copiarlo a mano o hacer scraping para la demo. El dataset abierto del IDEAM (`bdmn-sqnh` en datos.gov.co) solo trae la estación La Vorágine en Cali |
| Aforo, baños, agua y energía de coliseos y escenarios | Calcular brechas según la norma Esfera | Secretaría del Deporte / Indervalle | Petición, o capturarlo con el formulario de Cali Lista (esa es la propuesta de Pablo) |
| Población por comuna para 2026 | La que tenemos es una proyección a 2020 | DANE (proyecciones post CNPV 2018), Cali Cómo Vamos | Descargar del DANE; mientras tanto, usar la de 2020 y aclararlo |
| Redes de EMCALI (tomas de agua, hidrantes, tanques) | Papel de punto de agua ante sequía | EMCALI | No es abierta: se deja como adecuación recomendada |
| Pronóstico de El Niño y racionamiento | Escenario de sequía | IDEAM, UNGRD, EMCALI | Boletines públicos |

## 5. Filtro legal de los datos

- **Ley 1581 de 2012:** no usamos ni pedimos datos personales. Se retiraron los reportes ciudadanos de ChatMap porque traen fotos de personas. Del RUD solo se piden **agregados**.
- **Licencias CC BY-SA** de los datos del DAPM: los derivados (`procesados/`) también deben publicarse con **CC BY-SA 4.0 y atribución** a la Alcaldía de Cali (DAPM/IDESC).
- **Ley 1523 de 2012:** los datos oficiales del POT y del RUD son la base, pero **el sistema recomienda y la autoridad decide**. El índice de afectación es relativo y no reemplaza la EDAN ni el RUD.
- **Ley 1712 de 2014 (transparencia):** la información que se pide es pública clasificable. Hay que pedir agregados para no chocar con la reserva de datos personales.
