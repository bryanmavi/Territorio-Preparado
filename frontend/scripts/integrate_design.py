#!/usr/bin/env python3
"""Apply the shared visual system after rebuilding any static app entry."""
from pathlib import Path
import shutil
import re
frontend = Path(__file__).resolve().parents[1]
dist = frontend / 'dist'
source = frontend / 'design-source'
for name in ('app-theme.css', 'app-theme.js', 'equipo.jpeg'):
    shutil.copy2(source / name, dist / 'assets' / name)
for name in ('index.html', 'operations.html', 'disaster-ai.html', 'simulation.html'):
    path = dist / name
    text = path.read_text()
    text = re.sub(r'<link[^>]*href="\./assets/navbar-photo.css"[^>]*>', '', text)
    text = re.sub(r'<script[^>]*src="\./assets/navbar-photo.js"[^>]*></script>', '', text)
    if './assets/app-theme.css' not in text:
        text = text.replace('</head>', '<link rel="stylesheet" href="./assets/app-theme.css"></head>')
    if name == 'index.html' and './assets/app-theme.js' not in text:
        text = text.replace('</body>', '<script src="./assets/app-theme.js"></script></body>')
    path.write_text(text)
print('Shared design applied to all four app entries.')
