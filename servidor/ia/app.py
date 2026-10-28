"""FastAPI application, served on the same origin as the existing prototype."""
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
import uuid

import httpx
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from langdetect import detect, DetectorFactory, LangDetectException
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from .engines import SOS, Damage, Unavailable, translate_local
DetectorFactory.seed = 0
ROOT = Path(__file__).resolve().parents[2]
app = FastAPI(title='Territorio Preparado · IA', version='1.0.0')
sos, damage = SOS(), Damage()
@app.middleware('http')
async def same_origin(request, call_next):
    origin = request.headers.get('origin')
    host = request.headers.get('host', '')
    if request.method == 'POST' and origin and origin not in ('http://'+host, 'https://'+host):
        return JSONResponse({'detail':'Origen no permitido', 'error':'Origen no permitido'}, status_code=403)
    response = await call_next(request)
    if request.method in ('GET', 'HEAD') and (request.url.path.endswith(('.html', '.js', '.css', '.json')) or request.url.path == '/'):
        response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response

@app.exception_handler(HTTPException)
async def api_error(request, exc):
    return JSONResponse({'detail':exc.detail, 'error':exc.detail}, status_code=exc.status_code)

slots = asyncio.Semaphore(1)
clients = set()
DB = Path(os.getenv('TP_AI_DB', '/tmp/territorio-preparado-ai.sqlite'))

def connection():
    db = sqlite3.connect(DB)
    db.execute('CREATE TABLE IF NOT EXISTS messages (id TEXT PRIMARY KEY, created TEXT, result TEXT)')
    return db

class TextRequest(BaseModel):
    text: str = Field(min_length=3, max_length=4000)
    language: str = Field(default='auto', pattern='^(auto|es|en)$')

@app.get('/api/v1/status')
def status():
    return {'sos_weights_present':sos.ready(), 'xview_runtime_configured':damage.ready(),
            'translation_configured':bool(os.getenv('DEEPL_AUTH_KEY')) or (Path(os.getenv('TP_TRANSLATION_MODEL','models/translation-es-en'))/'config.json').is_file(),
            'semantic_labels_configured':bool(os.getenv('TP_SOS_LABELS')),
            'human_review_required':True}

async def english(text, language):
    if language == 'en':
        return text, False
    if language != 'es':
        raise HTTPException(422, 'Solo español e inglés; especifica el idioma para mensajes cortos.')
    local_path = Path(os.getenv('TP_TRANSLATION_MODEL', 'models/translation-es-en'))
    if (local_path/'config.json').is_file():
        async with slots:
            try:
                return await run_in_threadpool(translate_local, text), True
            except (Unavailable, OSError) as exc:
                raise HTTPException(503, 'Traducción local no disponible.') from exc
    key = os.getenv('DEEPL_AUTH_KEY')
    if not key:
        raise HTTPException(503, 'Falta DEEPL_AUTH_KEY para traducir mensajes en español.')
    endpoint = 'https://api-free.deepl.com/v2/translate' if key.endswith(':fx') else 'https://api.deepl.com/v2/translate'
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(endpoint, headers={'Authorization':f'DeepL-Auth-Key {key}'},
                                         json={'text':[text], 'source_lang':'ES', 'target_lang':'EN'})
            response.raise_for_status()
            return response.json()['translations'][0]['text'], True
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as exc:
        raise HTTPException(503, 'Traducción no disponible; no se ejecutó clasificación.') from exc

@app.post('/api/v1/analyze-text')
async def analyze_text(body: TextRequest):
    if not body.text.strip():
        raise HTTPException(422, 'El mensaje está vacío.')
    language = body.language
    if language == 'auto':
        try:
            language = detect(body.text)
        except LangDetectException:
            raise HTTPException(422, 'No se pudo detectar el idioma; selecciona español o inglés.')
    text, translated = await english(body.text, language)
    async with slots:
        try:
            result = await run_in_threadpool(sos.predict, text)
        except Unavailable as exc:
            raise HTTPException(503, str(exc))
    result.update(id=str(uuid.uuid4()), original_text=body.text, analyzed_text=text,
                  language=language, translated=translated,
                  created=datetime.now(timezone.utc).isoformat())
    with connection() as db:
        db.execute('INSERT INTO messages VALUES (?,?,?)', (result['id'], result['created'], json.dumps(result)))
    for client in tuple(clients):
        try:
            await asyncio.wait_for(client.send_json(result), timeout=2)
        except Exception:
            clients.discard(client)
    return result

@app.get('/api/v1/messages')
def messages():
    with connection() as db:
        return [json.loads(row[0]) for row in db.execute('SELECT result FROM messages ORDER BY created DESC LIMIT 100')]

@app.websocket('/api/v1/messages/ws')
async def events(socket: WebSocket):
    origin = socket.headers.get('origin')
    if origin and origin not in ('http://'+socket.headers.get('host',''), 'https://'+socket.headers.get('host','')):
        await socket.close(code=1008)
        return
    await socket.accept()
    clients.add(socket)
    try:
        while True:
            await socket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        clients.discard(socket)

@app.post('/api/v1/analyze-damage')
async def analyze_damage(pre: UploadFile = File(...), post: UploadFile = File(...), bounds: str = Form(...)):
    try:
        bbox = json.loads(bounds)
        if (not isinstance(bbox,list) or len(bbox)!=4 or
            any(type(x) not in (int,float) for x in bbox) or
            not (-180 <= bbox[0] < bbox[2] <= 180 and -90 <= bbox[1] < bbox[3] <= 90)):
            raise ValueError()
    except (ValueError, TypeError):
        raise HTTPException(422, 'bounds debe ser [oeste,sur,este,norte] en WGS84.')
    contents = []
    for upload in (pre, post):
        content = await upload.read(12*1024*1024+1)
        await upload.close()
        if len(content) > 12*1024*1024:
            raise HTTPException(413, 'Cada imagen admite hasta 12 MB.')
        contents.append(content)
    async with slots:
        try:
            return await run_in_threadpool(damage.predict, *contents, bbox)
        except ValueError as exc:
            raise HTTPException(422, str(exc))
        except Unavailable as exc:
            raise HTTPException(503, str(exc))

# Preserve existing demo API behavior and static application.
from ..server import demo_records, reconcile
@app.get('/api/status')
def legacy_status():
    return {'server':'local', 'inference':'FastAPI · BERT / xView2', 'production_readiness':'piloto'}
@app.post('/api/demo/reconcile')
def legacy_reconcile():
    result = reconcile(demo_records())
    with sqlite3.connect(os.getenv('TP_LEGACY_DB', '/tmp/territorio-preparado-demo.sqlite')) as db:
        db.execute('CREATE TABLE IF NOT EXISTS runs (created TEXT, summary TEXT)')
        db.execute('INSERT INTO runs VALUES (?,?)', (result['counted_at'], json.dumps(result)))
    return result
@app.post('/api/demo/analysis')
def legacy_analysis():
    model = os.getenv('TP_LOCAL_MODEL', '')
    if not model:
        raise HTTPException(503, 'Configura TP_LOCAL_MODEL y Ollama local.')
    try:
        with httpx.Client(timeout=90) as client:
            response = client.post('http://127.0.0.1:11434/api/generate', json={
                'model':model, 'stream':False,
                'prompt':'Resume en español estos agregados sintéticos sin inventar cifras: '+json.dumps(reconcile(demo_records()))})
            response.raise_for_status()
            return {'model':model, 'analysis':response.json()['response'], 'data_scope':'Solo agregados sintéticos', 'engine':'Ollama local'}
    except (httpx.HTTPError, ValueError, KeyError):
        raise HTTPException(503, 'El modelo local no está disponible.')
app.mount('/', StaticFiles(directory=ROOT/'frontend/dist', html=True), name='frontend')
