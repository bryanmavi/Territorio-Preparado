"""Servidor local del demostrador. Solo datos sintéticos; no es un despliegue productivo."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse, json, os, sqlite3, time, urllib.request, urllib.error
ROOT = Path(__file__).resolve().parents[1]
STARTED = time.time()

def demo_records():
    base = [{'person_id': f'DEMO-{i:03}', 'household_id': f'H-{i%32:02}', 'source': 'Registro de albergue' if i%2 else 'Brigada territorial', 'water': True, 'shelter': i%4 != 0} for i in range(104)]
    return base + [dict(r, source='Junta comunitaria') for r in base[:24]]

def reconcile(records):
    people = {}; excluded = 0; conflicts = []
    for r in records:
        key = r.get('person_id')
        if not isinstance(key,str) or not key.startswith('DEMO-'):
            excluded += 1; continue
        if key in people and people[key].get('household_id') != r.get('household_id'):
            conflicts.append(key)
        people.setdefault(key,r)
    return {'reports': len(records), 'unique_people': len(people), 'duplicate_reports': len(records)-excluded-len(people), 'households': len({r.get('household_id') for r in people.values() if r.get('household_id')}), 'water_people': sum(bool(r.get('water')) for r in people.values()), 'shelter_people': sum(bool(r.get('shelter')) for r in people.values()), 'excluded': excluded, 'conflicts': sorted(set(conflicts)), 'dataset': 'sintético', 'method': 'Coincidencia exacta de identificador sintético; no fusión probabilística de identidades', 'counted_at': time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT/'frontend/dist'),**kw)
    def log_message(self,*a): pass
    def send_json(self,data,status=200):
        payload=json.dumps(data,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
    def do_GET(self):
        if self.path == '/api/status':
            return self.send_json({'server':'local', 'uptime_seconds':round(time.time()-STARTED), 'database':'SQLite local · datos sintéticos', 'inference':'Modelo local por configurar', 'commercial_ai_api':False, 'production_readiness':'demostrador'})
        return super().do_GET()
    def do_POST(self):
        # Same-origin browser calls only. No CORS, arbitrary imports, or arbitrary outbound URLs.
        origin=self.headers.get('Origin'); host=self.headers.get('Host','')
        if origin and origin not in ('http://'+host,'https://'+host):return self.send_json({'error':'Origen no permitido'},403)
        if self.path == '/api/demo/reconcile':
            result=reconcile(demo_records())
            with sqlite3.connect(self.server.db) as db:
                db.execute('CREATE TABLE IF NOT EXISTS runs (created TEXT, summary TEXT)')
                db.execute('INSERT INTO runs VALUES (?,?)',(result['counted_at'],json.dumps(result)))
            return self.send_json(result)
        if self.path == '/api/demo/analysis':
            model=os.getenv('TP_LOCAL_MODEL','')
            if not model:return self.send_json({'error':'Configura TP_LOCAL_MODEL y un modelo instalado en Ollama local. No se ha ejecutado IA.'},503)
            summary=reconcile(demo_records())
            prompt='Resume estos agregados sintéticos en español. No inventes cifras ni instrucciones de evacuación. Máximo 100 palabras. '+json.dumps(summary)
            body=json.dumps({'model':model,'prompt':prompt,'stream':False}).encode()
            try:
                req=urllib.request.Request('http://127.0.0.1:11434/api/generate',data=body,headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req,timeout=90) as response:data=json.load(response)
                return self.send_json({'model':model,'analysis':data['response'],'data_scope':'Solo agregados sintéticos','engine':'Ollama local'})
            except (OSError,ValueError,KeyError) as e:return self.send_json({'error':'El modelo local no está disponible. El conteo sigue funcionando.'},503)
        return self.send_json({'error':'Ruta no disponible'},404)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=4180);parser.add_argument('--db',default='/tmp/territorio-preparado-demo.sqlite');args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler);server.db=args.db
    print(f'Territorio Preparado: http://127.0.0.1:{args.port} · datos sintéticos',flush=True)
    server.serve_forever()
