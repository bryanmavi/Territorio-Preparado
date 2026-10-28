"""Python 3.7 runner for the official xView2 baseline (CPU, no training).
Keeps the upstream architecture/weights and preprocessing; avoids downloading
ImageNet initialization that is overwritten by the complete checkpoint.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--source', required=True)
parser.add_argument('--pre', required=True)
parser.add_argument('--post', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args()
source = Path(args.source).resolve()
output = Path(args.output).resolve()
work = output.parent
os.environ.setdefault('OMP_NUM_THREADS', '2')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '2')
os.environ.setdefault('TF_NUM_INTRAOP_THREADS', '2')
os.environ.setdefault('TF_NUM_INTEROP_THREADS', '1')
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def run(script, arguments, cwd):
    subprocess.run([sys.executable, str(script)] + [str(x) for x in arguments], cwd=str(cwd), check=True)

polygons = work/'polygons.json'
run(Path(__file__).with_name('xview_localize.py').resolve(), ['--source', source, '--input', Path(args.pre).resolve(), '--output', polygons], source)
with polygons.open() as file:
    localized = json.load(file)
classes = work/'classes.json'
if localized['features']['xy']:
    crops = work/'crops'
    crops.mkdir()
    csv_path = work/'crops.csv'
    run(source/'model/process_data_inference.py', ['--input_img', Path(args.post).resolve(),
        '--label_path', polygons, '--output_dir', crops, '--output_csv', csv_path], source/'model')
    import numpy as np
    import pandas as pd
    import keras
    import tensorflow as tf
    from PIL import Image
    # Bound TF threads and disable GPUs explicitly.
    config = tf.ConfigProto(intra_op_parallelism_threads=2, inter_op_parallelism_threads=1,
                            device_count={'GPU':0})
    keras.backend.set_session(tf.Session(config=config))
    code = (source/'model/model.py').read_text()
    if "weights = 'imagenet'" not in code:
        raise RuntimeError('Unexpected upstream architecture source')
    namespace = {}
    exec(compile(code.replace("weights = 'imagenet'", 'weights = None'),
                 str(source/'model/model.py'), 'exec'), namespace)
    model = namespace['generate_xBD_baseline_model']()
    model.load_weights(str(source/'weights/classification.hdf5'))
    frame = pd.read_csv(str(csv_path))
    labels = ['no-damage','minor-damage','major-damage','destroyed']
    results = {}
    for name in frame['uuid']:
        with Image.open(str(crops/name)) as image:
            image = image.convert('RGB').resize((128,128), Image.NEAREST)
            batch = np.asarray(image, dtype=np.float32)[None] * 1.4
        predicted = model.predict_on_batch(batch)[0]
        results[Path(name).stem] = labels[int(np.argmax(predicted))]
    classes.write_text(json.dumps(results))
else:
    classes.write_text('{}')
combined = work/'combined.json'
run(source/'utils/combine_jsons.py', ['--polys',polygons,'--classes',classes,'--output',combined], source)
run(source/'utils/inference_image_output.py', ['--input',combined,'--output',output], source)
