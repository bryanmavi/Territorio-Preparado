"""Contrasta las geometrías y propiedades archivadas con los WFS oficiales."""
import concurrent.futures,datetime,hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'dist/data'
manifest=json.loads((ROOT/'manifest.json').read_text())
old=json.loads((ROOT/'source-checks.json').read_text())
def verify(source):
 try:
  with urllib.request.urlopen(source['download'],timeout=45) as response: raw=response.read()
  data=json.loads(raw)
  if data.get('type')!='FeatureCollection':raise ValueError('Respuesta no GeoJSON')
  folder=Path('/tmp/territorio-current-sources');folder.mkdir(exist_ok=True)
  (folder/(source['key']+'.json')).write_bytes(raw)
  # El hash del manifiesto se refiere al archivo archivado; el ID WFS cambia.
  canonical=[{'geometry':f['geometry'],'properties':f['properties']} for f in data['features']]
  canonical.sort(key=lambda x:json.dumps(x,sort_keys=True))
  archived=Path(__file__).resolve().parents[2]/'prototipo/datos/raw/idesc'/(source['name']+'.geojson')
  same=None
  if archived.exists():
   snapshot=json.loads(archived.read_text())
   normalized=[{'geometry':f['geometry'],'properties':f['properties']} for f in snapshot['features']]
   normalized.sort(key=lambda x:json.dumps(x,sort_keys=True))
   same=normalized==canonical
  digest=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  return {'key':source['key'],'url':source['download'],'consultedOn':datetime.date.today().isoformat(),'snapshotCount':source['count'],'remoteCount':len(canonical),'contentDigest':digest,'sameGeometryAndProperties':same,'status':'Sin cambios respecto al archivo original' if same else 'Cambio detectado; requiere regenerar derivados' if same is False else 'Descarga verificada; falta archivo original para comparar'}
 except Exception as e:return {'key':source['key'],'url':source['download'],'consultedOn':datetime.date.today().isoformat(),'status':'No verificable: '+str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(verify,manifest['sources']))
(ROOT/'current-source-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
for r in results:print(r['key'],r.get('remoteCount'),r['status'])
