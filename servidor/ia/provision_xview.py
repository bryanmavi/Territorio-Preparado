"""Provision official xView2 in a private Python 3.7 conda environment."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--conda', default=shutil.which('conda'))
args = parser.parse_args()
if not args.conda:
    parser.error('Conda no encontrado; indicar --conda /ruta/a/conda')
root = Path(__file__).resolve().parents[2]
source = root/'models/xview2/source'
runtime = root/'models/xview2/runtime'
commit = '821d9f8b9201ee7952aef13b073c9fd38ce11d4b'
if not source.exists():
    subprocess.run(['git','clone','https://github.com/DIUx-xView/xView2_baseline.git',str(source)],check=True)
subprocess.run(['git','checkout',commit],cwd=source,check=True)
if not (runtime/'bin/python').exists():
    subprocess.run([args.conda,'create','--prefix',str(runtime),'python=3.7','pip','-y'],check=True)
subprocess.run([str(runtime/'bin/python'),'-m','pip','install','-r',str(Path(__file__).with_name('requirements-xview.txt'))],check=True)
files = {}
for name in ('localization.h5','classification.hdf5'):
    path = source/'weights'/name
    if not path.exists():
        url = 'https://github.com/DIUx-xView/xView2_baseline/releases/download/v1.0/'+name
        temporary = path.with_suffix('.download')
        urllib.request.urlretrieve(url,temporary)
        temporary.replace(path)
    with path.open('rb') as stream:
        files[name] = hashlib.file_digest(stream,'sha256').hexdigest()
manifest = {'source_commit':commit,'release':'v1.0','weights_sha256':files}
(root/'models/xview2/manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
