"""Local model inference. Never substitutes heuristics for missing weights."""
import io
import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import threading

class Unavailable(RuntimeError):
    pass

class SOS:
    def __init__(self):
        self.path = Path(os.getenv('TP_SOS_MODEL', 'models/sos'))
        self.lock = threading.Lock()
        self.model = None

    def ready(self):
        return (self.path / 'config.json').is_file()

    def predict(self, text):
        if not self.ready():
            raise Unavailable('Faltan pesos BERT locales. Ejecuta download_models.py.')
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        with self.lock:
            if self.model is None:
                self.tokenizer = AutoTokenizer.from_pretrained(self.path, local_files_only=True)
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    self.path, local_files_only=True).float().eval()
            tokens = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=128)
            with torch.inference_mode():
                probabilities = torch.sigmoid(self.model(**tokens).logits)[0].tolist()
        # Upstream publishes LABEL_0..LABEL_35; do not invent a semantic mapping.
        mapping_path = os.getenv('TP_SOS_LABELS')
        mapping = json.loads(Path(mapping_path).read_text()) if mapping_path else {}
        if mapping and set(mapping) != {str(i) for i in range(len(probabilities))}:
            raise Unavailable('El mapa de etiquetas debe cubrir todas las salidas del modelo.')
        scores = [{'label': mapping.get(str(i), f'LABEL_{i}'), 'score': round(p, 6)}
                  for i, p in enumerate(probabilities)]
        return {'scores': scores, 'selected': [s for s in scores if s['score'] >= .5],
                'model': 'AventIQ-AI/Bert-Disaster-SOS-Message-Classifier',
                'semantic_labels_verified': bool(mapping),
                'priority': 'human_review', 'threshold': .5,
                'limitation': 'Revisión humana requerida. Las categorías no equivalen a una escala clínica de urgencia.'}

class Damage:
    """Official xView2 weights via isolated local runner or submission container."""
    def __init__(self):
        self.image = os.getenv('TP_XVIEW_IMAGE', '')
        self.work = Path(os.getenv('TP_XVIEW_WORK', '/tmp/tp-xview'))
        self.lock = threading.Lock()
        self.source = Path(os.getenv('TP_XVIEW_SOURCE', 'models/xview2/source')).resolve()
        self.python = Path(os.getenv('TP_XVIEW_PYTHON', 'models/xview2/runtime/bin/python')).resolve()

    def ready(self):
        return bool(self.image and shutil.which('docker')) or (
            self.python.is_file() and all((self.source/'weights'/name).is_file()
                for name in ('localization.h5','classification.hdf5','mean.npy')))


    def predict(self, pre, post, bounds):
        if not self.ready():
            raise Unavailable('Faltan runtime y pesos xView2 locales; configura TP_XVIEW_PYTHON/TP_XVIEW_SOURCE o TP_XVIEW_IMAGE.')
        import numpy as np
        from PIL import Image
        from rasterio.features import shapes
        from rasterio.transform import from_bounds
        images = []
        for content in (pre, post):
            try:
                image = Image.open(io.BytesIO(content))
                if image.size != (1024, 1024):
                    raise ValueError('El baseline requiere imágenes PNG RGB de 1024 × 1024, alineadas.')
                image.load()
                images.append(image.convert('RGB'))
            except (OSError, Image.DecompressionBombError) as exc:
                raise ValueError('Imagen inválida.') from exc
        self.work.mkdir(parents=True, exist_ok=True)
        with self.lock, tempfile.TemporaryDirectory(dir=self.work) as directory:
            root = Path(directory)
            root.chmod(0o755)
            (root/'input').mkdir()
            (root/'output').mkdir(mode=0o777)
            (root/'output').chmod(0o777)
            for image, name in zip(images, ('pre', 'post')):
                image.save(root/'input'/f'event_{name}_disaster.png')
            # Host and container paths must match when API itself runs in Docker.
            command = ['docker', 'run', '--rm', '--network=none', '--memory=6g',
                       '--cpus=2', '-v', f'{root}/input:/submission:ro',
                       '-v', f'{root}/output:/output', self.image,
                       '/submission/event_pre_disaster.png', '/submission/event_post_disaster.png',
                       '/output/localization.png', '/output/damage.png']
            if not self.image:
                command = [str(self.python), str(Path(__file__).with_name('xview_runner.py')),
                    '--source', str(self.source), '--pre', str(root/'input/event_pre_disaster.png'),
                    '--post', str(root/'input/event_post_disaster.png'), '--output', str(root/'output/damage.png')]
            try:
                subprocess.run(command, check=True, capture_output=True, timeout=600)
            except (subprocess.SubprocessError, OSError) as exc:
                logging.getLogger(__name__).error('xView2 failed: %s', str(getattr(exc, 'stderr', b''))[-3000:])
                raise Unavailable('Falló el motor xView2; verifica imagen, pesos y runtime.') from exc
            output = root/'output/damage.png'
            if not output.is_file():
                raise Unavailable('xView2 no generó la máscara esperada.')
            mask = np.array(Image.open(output))
            result = mask_to_geojson(mask, bounds, shapes, from_bounds)
            result['metadata']['localization_mode'] = 'container-configured' if self.image else 'tiled-cpu-256-context64'
            result['metadata']['tiling_requires_validation'] = True
            return result

def mask_to_geojson(mask, bounds, shapes=None, from_bounds=None):
    import numpy as np
    if shapes is None:
        from rasterio.features import shapes
        from rasterio.transform import from_bounds
    if mask.ndim != 2 or not np.isin(mask, [0, 1, 2, 3, 4]).all():
        raise Unavailable('Máscara xView2 inválida.')
    names = {1:'no-damage', 2:'minor-damage', 3:'major-damage', 4:'destroyed'}
    transform = from_bounds(*bounds, mask.shape[1], mask.shape[0])
    features = [{'type':'Feature', 'geometry':geometry,
                 'properties':{'damage':names[int(value)], 'damage_class':int(value),
                               'review_required':True}}
                for geometry, value in shapes(mask.astype('uint8'), mask=mask > 0, transform=transform)]
    return {'type':'FeatureCollection', 'features':features,
            'metadata':{'model':'DIUx-xView/xView2_baseline', 'bounds':bounds,
                        'limitation':'Regiones de píxeles contiguos; no identifica edificios individuales contiguos. Georreferencia proporcionada por el operador.'}}

def translate_local(text):
    import torch
    from transformers import MarianMTModel, MarianTokenizer
    path = Path(os.getenv('TP_TRANSLATION_MODEL', 'models/translation-es-en'))
    if not (path/'config.json').is_file():
        raise Unavailable('Falta modelo local de traducción español-inglés.')
    tokenizer = MarianTokenizer.from_pretrained(path, local_files_only=True)
    model = MarianMTModel.from_pretrained(path, local_files_only=True).eval()
    tokens = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    with torch.inference_mode():
        output = model.generate(**tokens, max_new_tokens=512)
    return tokenizer.decode(output[0], skip_special_tokens=True)
