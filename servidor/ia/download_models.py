"""Explicit provisioning; runtime never downloads weights."""
import argparse
import hashlib
import json
from pathlib import Path
from huggingface_hub import HfApi, snapshot_download
from transformers import AutoTokenizer
parser = argparse.ArgumentParser()
parser.add_argument('--translation', action='store_true')
parser.add_argument('--output', default='models/sos')
args = parser.parse_args()
repo = 'Helsinki-NLP/opus-mt-es-en' if args.translation else 'AventIQ-AI/Bert-Disaster-SOS-Message-Classifier'
if args.translation and args.output == 'models/sos':
    args.output = 'models/translation-es-en'
revision = HfApi().model_info(repo).sha
path = Path(snapshot_download(repo, revision=revision, local_dir=args.output,
    allow_patterns=['*.json', '*.safetensors', 'pytorch_model.bin', '*.spm', 'vocab.txt', '*.txt']))
if not args.translation and not (path/'vocab.txt').exists():
    AutoTokenizer.from_pretrained('bert-base-uncased').save_pretrained(path)
manifest = {'repository':repo, 'revision':revision, 'files':{}}
for file in path.iterdir():
    if file.is_file() and file.name != 'manifest.json':
        manifest['files'][file.name] = hashlib.file_digest(file.open('rb'), 'sha256').hexdigest()
(path/'manifest.json').write_text(json.dumps(manifest, indent=2))
print(f'Pesos disponibles en {path}; revisión {revision}.')
