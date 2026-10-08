"""Parche reproducible de la demo compilada; conserva el bundle original."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'dist/assets/index-B2wY6ZdK.js'; backup=root/'scripts/index-B2wY6ZdK.original.js'
if not backup.exists():backup.write_bytes(p.read_bytes())
s=backup.read_text()
def change(old,new):
 global s
 if old not in s:raise RuntimeError('No se encontró bloque: '+old[:100])
 s=s.replace(old,new,1)
change('mi=F.useMemo(()=>[...new Set(Mt.filter(b=>!H||(H==="unassigned"?!b.properties.commune:b.properties.commune===H)).map(b=>b.properties.neighborhood).filter(b=>!!b))].sort((b,G)=>b.localeCompare(G,"es")),[S,H])','mi=F.useMemo(()=>[...new Set([...(S?.neighborhoods.features??[]).filter(b=>!H||(H==="unassigned"?!b.properties.commune:b.properties.commune===H)).map(b=>b.properties.name),...Mt.filter(b=>!H||(H==="unassigned"?!b.properties.commune:b.properties.commune===H)).map(b=>b.properties.neighborhood)].filter(Boolean))].sort((b,G)=>b.localeCompare(G,"es")),[S,H])')
change('function q_({spaces:S,selected:N,scope:y})','function q_({spaces:S,selected:N,scope:y,data:territoryData})')
change('S.length&&p.fitBounds(Yo.latLngBounds(S.map(O=>[O.properties.coordinates[1],O.properties.coordinates[0]])),{paddingTopLeft:[35,35],paddingBottomRight:[35,130],maxZoom:15,animate:!1})','(()=>{const [commune,neighborhood]=y.split("|");let features=neighborhood?territoryData.neighborhoods.features.filter(f=>f.properties.name===neighborhood&&(!commune||f.properties.commune===commune)):commune&&commune!=="unassigned"?territoryData.communes.features.filter(f=>f.properties.code===commune):territoryData.communes.features;let bounds=features.length?Yo.geoJSON({type:"FeatureCollection",features}).getBounds():S.length?Yo.latLngBounds(S.map(O=>[O.properties.coordinates[1],O.properties.coordinates[0]])):null;if(bounds?.isValid())p.fitBounds(bounds,{paddingTopLeft:[35,35],paddingBottomRight:[35,130],maxZoom:16,animate:!1});p.invalidateSize()})()')
change('_.jsx(q_,{spaces:N,selected:y,scope:j})','_.jsx(q_,{spaces:N,selected:y,scope:j,data:S})')
change('data:S.communes,style:','data:S.communes,interactive:!1,style:')
change('data:S.neighborhoods,style:','data:S.neighborhoods,interactive:!1,style:')
change('data:S[O],style:','data:S[O],interactive:!1,style:')
change('No hay registros para estos filtros.','Este sector no tiene espacios en el inventario seleccionado. Puedes explorar sus calles y límites; limpia los filtros para consultar otros registros.')
change('Explora los espacios de Cali por comuna y barrio, consulta las amenazas cartografiadas y revisa qué falta por confirmar.','Explora todos los barrios cartografiados de Cali, incluso donde no hay espacios inventariados. Las calles se consultan en OpenStreetMap; los espacios y amenazas se contrastan con las fuentes oficiales.')
change('Corte de los archivos:','Fecha del inventario archivado:')
# Base más tolerante a zoom alto y errores transitorios, sin cambiar de proveedor.
change('url:"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",eventHandlers:{tileerror:()=>N(!0)}','url:"https://tile.openstreetmap.org/{z}/{x}/{y}.png",maxNativeZoom:19,maxZoom:21,keepBuffer:4,eventHandlers:{tileerror:()=>N(!0),load:()=>N(!1)}')
change('className:"territory-map","aria-label"','maxZoom:21,className:"territory-map","aria-label"')
change('_.jsx("p",{className:"small-note",children:"Los sectores corresponden', '_.jsxs("p",{className:"small-note",children:["Cartografía oficial archivada; consulta de fuentes: 08/10/2026. ",_.jsx("a",{href:"/data/current-source-checks.json",target:"_blank",rel:"noopener",children:"Ver estado de actualización"})]}),_.jsx("p",{className:"small-note",children:"Los sectores corresponden')
p.write_text(s)
print('Mapa corregido; original conservado en scripts.')
