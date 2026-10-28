# IA para desastres · implementación de la guía PDF

Desde la raíz del repositorio:

```bash
python3 -m venv servidor/ia/.venv
servidor/ia/.venv/bin/python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
servidor/ia/.venv/bin/python -m pip install -r servidor/ia/requirements.txt
servidor/ia/.venv/bin/python servidor/ia/download_models.py
servidor/ia/.venv/bin/python -m uvicorn servidor.ia.app:app --host 127.0.0.1 --port 4180
```

Abrir http://127.0.0.1:4180/disaster-ai.html o entrar desde Centro de operaciones. OpenAPI: `/docs`. GitHub Pages solo sirve la interfaz; requiere este servidor para inferencias. El servidor anterior sigue disponible.

## BERT

`POST /api/v1/analyze-text` recibe `{"text":"We need water", "language":"en"}`. `language` admite `es`, `en` y `auto`. La detección de mensajes cortos puede fallar: el operador puede seleccionar el idioma. Español usa traducción local con Helsinki-NLP/opus-mt-es-en si está provisionada:

```bash
servidor/ia/.venv/bin/python servidor/ia/download_models.py --translation
```

`TP_TRANSLATION_MODEL` cambia su ruta. Si no está disponible, se puede configurar `DEEPL_AUTH_KEY` como alternativa; en ese caso el texto se envía a DeepL (incluye posibles datos personales). Sin ninguna opción devuelve 503. Con los pesos provisionados, ambos idiomas funcionan sin red. La traducción es automática y requiere revisión.

El repositorio original contiene **36 etiquetas genéricas** y clasificación multietiqueta. Se usa sigmoid con umbral 0.5; no softmax. No hay una correspondencia publicada y verificada entre los índices y categorías. Por ello se guardan puntuaciones y `priority=human_review`, sin atribuir una urgencia médica a las salidas. Para habilitar nombres, `TP_SOS_LABELS` apunta a un JSON `{ "0": "nombre verificado", ... "35": "nombre verificado" }`, solo tras verificar su procedencia. La validación de exactitud y de priorización con corpus español/inglés etiquetado sigue pendiente. El F1 declarado por el autor es 0.83; no es una métrica medida en Cali.

`TP_SOS_MODEL` cambia la ruta local (predeterminada `models/sos`). Descarga explícita, revisión y SHA256 registrados en `manifest.json`; inferencia usa `local_files_only=True` y float32 en CPU. El original y la traducción se guardan en SQLite (`TP_AI_DB`). `/api/v1/messages` devuelve los últimos 100; `/api/v1/messages/ws` avisa de nuevos resultados. Al no existir urgencias verificadas, la tabla usa orden cronológico.

## xView2

Opción local sin Docker (Conda instalado):

```bash
servidor/ia/.venv/bin/python servidor/ia/provision_xview.py
```

Prepara Python 3.7 y las dependencias fijadas en `requirements-xview.txt`, descarga los dos pesos oficiales y registra commit/hashes. `TP_XVIEW_SOURCE` y `TP_XVIEW_PYTHON` permiten rutas alternativas. `xview_runner.py` ejecuta localización con pesos oficiales sin grafo de gradientes, por bloques de 256 píxeles con 64 de contexto, extracción oficial de polígonos y la arquitectura de clasificación oficial con los pesos completos. Evita inicializar ResNet con pesos ImageNet que después se sobrescriben, conserva el escalado 1.4 y el redimensionado nearest del baseline, y procesa un edificio por lote para limitar memoria. La inferencia completa de 1024×1024 agotó la RAM del equipo; los bloques evitan ese fallo. Las predicciones pueden variar en los bordes de bloque respecto a la inferencia original y requieren validación específica. La CPU tarda más que una GPU. Esta opción no necesita Docker ni credenciales.

Opción contenedor (Dockerfiles suministrados, construcción no ejecutada en este equipo):

```bash
docker build -f deploy/ia/Dockerfile.xview -t territorio-xview:local .
TP_XVIEW_IMAGE=territorio-xview:local servidor/ia/.venv/bin/python -m uvicorn servidor.ia.app:app --host 127.0.0.1 --port 4180
```

Este contenedor incluye el mismo procesamiento por bloques del runner local y sus límites de validación.

El baseline original no es un modelo PyTorch de seis canales: localiza con SpaceNet/Chainer y clasifica con Keras/TensorFlow 1. Se conecta al contenedor oficial sin reemplazarlo por un detector arbitrario.

1. Instalar Docker en un servidor de inferencia.
2. Obtener y revisar https://github.com/DIUx-xView/xView2_baseline y sus pesos oficiales (localización y clasificación, release v1.0). Su Dockerfile antiguo no compila sin adaptar dependencias/sistema a TensorFlow 1; no se considera validado con Ubuntu actual. Registrar commit y hashes de pesos del contenedor que se valide.
3. Construir una imagen compatible con la interfaz oficial de `submission/run.sh`, guardando todos los pesos dentro de ella. Definir `TP_XVIEW_IMAGE` al nombre de esa imagen. El adaptador ejecuta `docker run --network=none`, con directorio temporal exclusivo, timeout y límite de recursos. No admite comandos ni nombres de imagen suministrados por el navegador.
4. Enviar dos PNG RGB alineados de 1024×1024 y sus límites geográficos compartidos. Multipart: `pre`, `post`, `bounds=[oeste,sur,este,norte]`. Los límites deben venir de metadatos geográficos verificados; no se estiman a partir del contenido visual. No se corrige registro geométrico automáticamente.
5. El contenedor devuelve máscara 0–4. Se vectorizan regiones contiguas y se exporta GeoJSON WGS84; regiones no equivalen necesariamente a edificios individuales. El visor pinta 1 verde, 2 amarillo, 3 naranja y 4 rojo. xBD para entrenamiento/evaluación requiere gestionar su acceso en https://xview2.org/dataset.

El endpoint devuelve 503 si falta el motor configurado o si falla la ejecución. Una prueba técnica con la imagen pública de ejemplo del repositorio no equivale a validar precisión con pares xBD ni a evaluar daños en Cali.

## Despliegue

`deploy/ia/Dockerfile` y `compose.yml` preparan el servicio CPU BERT con modelos montados de solo lectura y SQLite persistente. El runtime local xView2 se ejecuta desde el host; la alternativa Docker también requiere el host; Compose no monta el socket de Docker. No habilitar esa capacidad dentro del contenedor de la API sin diseñar un servicio aislado de inferencia.

`kubernetes.yaml` es una plantilla de una réplica con PVC externos. **No habilita escalado horizontal:** SQLite y WebSocket en memoria requieren migrar a PostgreSQL y un broker compartido (Redis) antes de añadir réplicas/HPA. No se ha desplegado a infraestructura externa. La API se ejecuta en loopback para piloto; acceso público requiere autenticación, TLS, controles de acceso, retención de mensajes y colas durables. Las teselas OSM requieren red; Leaflet se guarda localmente.

## Verificación

```bash
servidor/ia/.venv/bin/python -m unittest servidor.ia.test_ai -v
python3 -m unittest discover -s servidor -v
```

Las pruebas de integración aíslan la inferencia con dobles y comprueban persistencia, WebSocket, errores sin inferencia ficticia, validación y coordenadas GeoJSON. No miden precisión del modelo ni sustituyen la prueba del contenedor xView2 con pares xBD.

Fuentes: [BERT y métricas del autor](https://huggingface.co/AventIQ-AI/Bert-Disaster-SOS-Message-Classifier), [configuración de 36 etiquetas](https://huggingface.co/AventIQ-AI/Bert-Disaster-SOS-Message-Classifier/blob/main/config.json), [baseline y contrato de salida xView2](https://github.com/DIUx-xView/xView2_baseline).

## Resultado verificado el 16 de octubre de 2026

Pesos BERT y traducción instalados; inferencias reales en inglés y español verificadas. xView2 instalado en Python 3.7 y probado con los pesos originales: 74 polígonos clasificados y 51 regiones vectorizadas en el ejemplo público del repositorio. La prueba técnica usa la misma imagen en ambas entradas y límites artificiales; no demuestra precisión pre/post ni daño georreferenciado real. La prueba del navegador recorrió formulario → API → GeoJSON → mapa → descarga. Pasaron diez pruebas de integración y tres del servidor previo.

```bash
node frontend/tests/disaster-browser.cjs --damage
```

Este chequeo usa el servidor en el puerto 4181 y requiere Google Chrome, `frontend/tests/node_modules` y todos los pesos provisionados. Sin `--damage` verifica texto e interfaz. [Registro de versiones, hashes y alcance de pruebas](../../docs/evidence/ia-2026-10-16.json). Versiones instaladas registradas en `requirements-tested.txt` y `requirements-xview-tested.txt`; PyTorch CPU requiere el índice `https://download.pytorch.org/whl/cpu`.
