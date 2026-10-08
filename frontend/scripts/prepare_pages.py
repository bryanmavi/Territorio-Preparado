"""Prepare the compiled prototype for a GitHub Pages project URL."""
import argparse
from pathlib import Path
import re
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--base', default='/Territorio-Preparado/')
parser.add_argument('--output', default='_site')
args = parser.parse_args()
base = '/' + args.base.strip('/') + '/'
root = Path(__file__).resolve().parents[2]
out = root / args.output
if out.exists():
    raise SystemExit(f'Output already exists: {out}')
shutil.copytree(root / 'frontend/dist', out)
for path in out.rglob('*'):
    if path.suffix not in {'.html', '.js', '.css'}:
        continue
    content = path.read_text()
    content = re.sub(r'(["\x27`(=])/((?:assets|data|images)/|simulation(?:\.html|-method\.md))', lambda match: match[1] + base + match[2], content)
    # Vite's dependency preloader also constructs paths from the domain root.
    content = content.replace('return"/"+S', f'return"{base}"+S')
    path.write_text(content)
(out / '.nojekyll').touch()
print(f'Prepared {out} at {base}')
