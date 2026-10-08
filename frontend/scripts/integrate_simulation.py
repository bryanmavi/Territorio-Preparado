"""Integrate the supplied v3 simulation without applying legacy v1 patches."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
source = root / 'simulation-source'
out = root / 'dist'
html = (source / 'simulacion_ciudad_cali.html').read_text()
marker = '<p class="marca">Territorio Preparado · RETO-01 Cali Activa</p>'
assert marker in html
html = html.replace(marker, marker + '<p style="margin:4px 0;font-size:12px"><a href="./">← Volver a Territorio Preparado</a> · Simulación v3 · <a href="./simulation-method.md" target="_blank" rel="noopener">Fuentes y método</a></p>', 1)
# Keep the supplied source intact; rendering changes are reproducible here.
html = html.replace('</head>', '<style>' + (source / 'rendering.css').read_text() + '</style></head>', 1)
html = html.replace('<p class="ayuda">', '<div class="render-tools"><label for="render-quality">Calidad visual</label><select id="render-quality"><option value="low">Ligera</option><option value="balanced" selected>Equilibrada</option><option value="high">Alta</option></select></div><p class="ayuda">', 1)
def patch(old, new):
    global html
    assert html.count(old) == 1, f'Rendering anchor changed: {old}'
    html = html.replace(old, new, 1)
patch('$n.toneMappingExposure=1.05', '$n.toneMappingExposure=1.0')
patch('cn.background=new pe("#d9e7f2");cn.fog=new to("#d9e7f2",9e3,42e3);cn.add(new yo("#f2f7ff","#b9ad8f",1.5))', 'cn.background=new pe("#e4eeef");cn.fog=new to("#e4eeef",14e3,48e3);cn.add(new yo("#eaf4ff","#a49c80",1.15))')
patch('var fm=new vs("#fff6e8",2.6)', 'var fm=new vs("#fff4df",2.15)')
patch('cn.add(fm);var Yn=', 'cn.add(fm);var fillLight=new vs("#d7eaff",.55);fillLight.position.set(4200,2800,-5000);cn.add(fillLight);var Yn=')
patch('Go.prepend($n.domElement);', """Go.prepend($n.domElement);
var qualityControl=document.getElementById('render-quality');
function applyRenderQuality(){
  var quality=qualityControl.value;
  $n.setPixelRatio(quality==='low'?1:Math.min(window.devicePixelRatio||1,quality==='high'?2:1.5));
}
qualityControl.addEventListener('change',applyRenderQuality);
window.addEventListener('resize',applyRenderQuality);
applyRenderQuality();""")
(out / 'simulation.html').write_text(html)
(out / 'simulation-method.md').write_text((source / 'FUENTES_Y_METODO.md').read_text())
print('Simulation v3 integrated')
