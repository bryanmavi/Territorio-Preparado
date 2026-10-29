#!/usr/bin/env python3
"""Apply the shared visual system after rebuilding any static app entry."""
from pathlib import Path
import shutil
import re
import hashlib
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
    # Content versions prevent browsers from retaining the previous visual rules.
    for asset in ('app-theme.css', 'app-theme.js'):
        version = hashlib.sha256((source / asset).read_bytes()).hexdigest()[:12]
        text = re.sub(r'(\./assets/' + re.escape(asset) + r')(?:\?v=[a-f0-9]+)?', lambda m: m[1] + '?v=' + version, text)
    if name != 'index.html':
        # Add a mobile photograph and clear, semantic return links in static headers.
        header = re.search(r'<header\b[^>]*>.*?</header>', text, re.S)
        if header:
            markup = header.group(0)
            def style_return(match):
                attrs, label = match.groups()
                if ('←' in label or 'Volver' in label) and 'tp-back' not in attrs:
                    return '<a class="tp-back"' + attrs + '>' + label + '</a>'
                return match.group(0)
            markup = re.sub(r'<a([^>]*)>(.*?)</a>', style_return, markup, flags=re.S)
            if 'tp-header-photo' not in markup:
                markup = markup.replace('</header>', '<img class="tp-header-photo" src="./assets/equipo.jpeg" width="1600" height="900" alt="Equipo de Territorio Preparado trabajando en la simulación de Cali"></header>')
            text = text[:header.start()] + markup + text[header.end():]
    if name == 'operations.html' and 'tp-internal-hero' not in text:
        intro = re.search(r'<main>(<div class="intro">.*?</div></div>)', text, re.S)
        if intro:
            hero = intro[1].replace('class="intro"', 'class="intro tp-internal-hero"', 1)
            text = text[:intro.start(1)] + text[intro.end(1):]
            text = text.replace('</header>', hero + '</header>', 1)
    path.write_text(text)
print('Shared design applied to all four app entries.')
