"""Apply the original map experience to the compiled app, preserving prior fixes."""
from pathlib import Path
root = Path(__file__).resolve().parents[1]
p = root / 'dist/assets/index-B2wY6ZdK.js'
s = p.read_text()
def change(old,new):
    global s
    if s.count(old)!=1: raise RuntimeError('Map anchor changed: '+old[:100])
    s=s.replace(old,new,1)
if 'function TerritoryRecords(' not in s:
    change(':territoryData.communes.features;let bounds=',':[];let bounds=')
    change('function P_(', (root/'map-source/map-experience.js').read_text()+'\nfunction P_(')
    change('showStreets:at,scope:j}){return','showStreets:at,scope:j,showPublic:showPublic,showSports:showSports}){const visibleSpaces=F.useMemo(()=>N.filter(f=>f.properties.sourceKey==="sports"?showSports:showPublic),[N,showPublic,showSports]);return')
    start=s.index('_.jsx(Su,{data:{type:"FeatureCollection",features:N},style:')
    end=s.index(',y&&_.jsx(R_',start)
    s=s[:start]+'_.jsx(TerritoryRecords,{spaces:visibleSpaces,threat:O,select:p,scope:j})'+s[end:]
    change('_.jsx(q_,{spaces:N,selected:y,scope:j,data:S})','_.jsx(q_,{spaces:N,selected:y,scope:j,data:S}),_.jsx(TerritoryMapTools,{data:S,spaces:N,scope:j})')
    change('function Q_(){const[S,N]', 'function Q_(){const [showPublic,setShowPublic]=F.useState(true),[showSports,setShowSports]=F.useState(true);const[S,N]')
    change('showStreets:ii,scope:$t}', 'showStreets:ii,scope:$t,showPublic:showPublic,showSports:showSports}')
    change('_.jsx("h3",{children:"Capas del mapa"}),', '_.jsx("h3",{children:"Capas del mapa"}),_.jsxs("label",{children:[_.jsx("input",{type:"checkbox",checked:showPublic,onChange:e=>setShowPublic(e.target.checked)}),_.jsx("i",{className:"layer-dot public"}),"Espacios públicos",_.jsx("span",{className:"layer-count",children:fa(Rt.filter(f=>f.properties.sourceKey==="publicSpaces").length)})]}),_.jsxs("label",{children:[_.jsx("input",{type:"checkbox",checked:showSports,onChange:e=>setShowSports(e.target.checked)}),_.jsx("i",{className:"layer-dot sports"}),"Escenarios deportivos",_.jsx("span",{className:"layer-count",children:fa(Rt.filter(f=>f.properties.sourceKey==="sports").length)})]}),')
    change('"Calles (OpenStreetMap) · requiere internet"','"Mapa de calles · OpenStreetMap"')
    change('_.jsxs("p",{className:"small-note",children:["Cartografía oficial archivada;', '_.jsx(TerritoryQuickPlaces,{spaces:Rt,selected:Ft,onSelect:D,query:lt}),_.jsxs("p",{className:"small-note",children:["Cartografía oficial archivada;')
    change('className:"inventory",children:', 'className:"inventory",id:"map-inventory",children:')
    change('children:"Una red por conocer"', 'children:"Explorador de Cali"') if 'children:"Una red por conocer"' in s else None
    change(':"Una red por conocer")', ':"Explorador de Cali")')
    p.write_text(s)
else:
    start=s.index('/* Original interaction layer')
    end=s.index('function P_(', start)
    s=s[:start]+(root/'map-source/map-experience.js').read_text()+'\n'+s[end:]
    p.write_text(s)
html=root/'dist/index.html'
h=html.read_text()
if 'map-experience.css' not in h:
    h=h.replace('</head>','<link rel="stylesheet" href="./assets/map-experience.css"></head>')
html.write_text(h)
(root/'dist/assets/map-experience.css').write_text((root/'map-source/map-experience.css').read_text())
print('Map experience applied')
