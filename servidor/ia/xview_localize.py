"""Memory-bounded localization using original Chainer weights and polygonizer.
256px cores with 64px context. Tiling can change predictions near seams;
validate separately from the original whole-image baseline.
"""
import argparse
import importlib.util
from pathlib import Path
import sys
import gc
import numpy as np
from PIL import Image
import chainer
parser=argparse.ArgumentParser()
for name in ('source','input','output'):
    parser.add_argument('--'+name,required=True)
args=parser.parse_args()
source=Path(args.source).resolve()
sys.path.insert(0,str(source/'spacenet/src/models'))
spec=importlib.util.spec_from_file_location('upstream_localize',str(source/'spacenet/inference/inference.py'))
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
chainer.global_config.enable_backprop=False
model=module.Model(str(source/'weights/localization.h5'),np.load(str(source/'weights/mean.npy')))
image=np.array(Image.open(args.input).convert('RGB'))
h,w,_=image.shape
core,halo=256,64
padded=np.pad(image,((halo,halo),(halo,halo),(0,0)),mode='symmetric')
scores=np.zeros((2,h,w),dtype=np.float32)
for y in range(0,h,core):
    for x in range(0,w,core):
        tile=padded[y:y+core+2*halo,x:x+core+2*halo]
        result=model.apply_segmentation(tile)
        height,width=min(core,h-y),min(core,w-x)
        scores[:,y:y+height,x:x+width]=result[:,halo:halo+height,halo:halo+width]
        del result
        gc.collect()
module.inference(image,scores,args.output)
