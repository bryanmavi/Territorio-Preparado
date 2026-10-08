from pathlib import Path
import re
root=Path(__file__).resolve().parents[1];src=root/'simulation-source';out=root/'dist'
s=(src/'simulacion_ciudad_cali.html').read_text()
def change(old,new):
 global s
 if old not in s:raise RuntimeError('Bloque no encontrado: '+old[:110])
 s=s.replace(old,new,1)
# Scope is explicitly educational and labels do not imply a present incident.
change('Simulación de escenarios en Santiago de Cali','Laboratorio de escenarios · Cali')
change('<h2>Cuadro de simulación</h2>','<p class="exercise-pill">SIMULACRO · DATOS Y SUPUESTOS VISIBLES</p><h2>Explora, compara y prepara</h2><p id="phase-exercise" role="status">Preparación</p>')
change('<button type="button" id="simular" class="primario">▶ Simular</button>','<button type="button" id="simular" class="primario" disabled>▶ Simular</button><button type="button" id="pause-exercise" disabled>Pausar</button><button type="button" id="reset-exercise" disabled>Reiniciar</button>')
change('<fieldset id="opciones-incendio" hidden>','''<div class="exercise-settings"><label>Duración visual <select id="duration-exercise"><option value="8000">8 segundos</option><option value="16000" selected>16 segundos</option><option value="30000">30 segundos</option></select></label><label><input type="checkbox" id="reduce-motion"> Reducir movimiento</label><label>Detalle de pantalla <select id="render-quality"><option value="standard">Normal</option><option value="low">Ligero</option></select></label></div><p id="exercise-status" role="status">Cargando datos y escena…</p><fieldset id="opciones-incendio" hidden>''')
change('<p class="ayuda">','<div class="camera-toolbar" role="group" aria-label="Vistas de cámara"><button data-view="overview">Ciudad completa</button><button data-view="top">Desde arriba</button><button data-view="hills">Laderas</button><button id="capture-exercise">Capturar vista</button></div><p class="ayuda">')
change('<h3>Sitios sugeridos para acopio</h3>','''<div class="exercise-comparison"><h3>Comparar ejercicios</h3><p id="comparison-exercise">Guarda un escenario completo como base y cambia las condiciones para compararlo.</p><div class="fila"><button id="save-exercise" disabled>Guardar base</button><button id="export-exercise" disabled>Descargar informe JSON</button></div></div><h3>Candidatos de acopio para revisión</h3>''')
change('</style>','''
.exercise-pill{color:#226a58;font-size:10px;font-weight:700;letter-spacing:.09em}.exercise-settings{display:grid;gap:9px;padding:12px;background:#f0f5ee;border-radius:10px;font-size:12px}.exercise-settings label{display:flex;align-items:center;gap:8px}.exercise-settings select{margin-left:auto;padding:5px;border:1px solid var(--borde);border-radius:5px}.camera-toolbar{position:absolute;top:12px;left:12px;display:flex;flex-wrap:wrap;gap:5px;z-index:1;max-width:calc(100% - 24px)}.camera-toolbar button{background:#ffffffed;font-size:11px;box-shadow:0 2px 5px #153b3914}.ayuda{top:54px}.exercise-comparison{background:#f4f6ee;border:1px solid var(--borde);border-radius:10px;padding:12px;margin:14px 0}.exercise-comparison h3{margin:0}.exercise-comparison p,#exercise-status,#phase-exercise{font-size:12px;line-height:1.5;color:var(--suave)}#phase-exercise{font-weight:700;color:var(--verde)}button:disabled{opacity:.5;cursor:wait}.cabecera{background:#153b39;color:#fafaf4}.cabecera .marca{color:#bbdf99}.cabecera .aviso{color:#d3e0d6}.diseno{grid-template-columns:minmax(0,1fr) 420px}.resumen{background:#e9f1e4}.acciones{gap:6px;flex-wrap:wrap}.acciones button{color:#fff;background:#245d50}.visor{background:#cfdae2}.cargando{background:#e8eee5}.etiqueta{padding:3px 7px;background:#153b39ed;color:#fff;border-color:#a4cb8e}.etiqueta span{color:#d9e7d0}.cuadro{scrollbar-width:thin}.nota{line-height:1.5}body{height:100vh}a{color:#205c51}#r-manzanas,#r-construcciones{font-size:18px}input[type=range]{accent-color:#205c51}
@media(max-width:760px){body{height:auto}.diseno{grid-template-columns:1fr}.visor{height:60vh;min-height:390px}.cuadro{overflow:visible}.cabecera{align-items:flex-start}.cabecera h1{font-size:19px}.camera-toolbar button{font-size:10px}.ayuda{top:82px;max-width:85%}.leyenda{font-size:10px}}
</style>''')
# False flat patches previously floated/cut through hills: drape every vertex.
old='return o.rotateX(-Math.PI/2),o.translate(0,Dh(Ft.relieve,r[0][0],r[0][1])+4,0),o'
new='o.rotateX(-Math.PI/2);let positions=o.getAttribute("position");for(let index=0;index<positions.count;index++)positions.setY(index,Dh(Ft.relieve,positions.getX(index),-positions.getZ(index))+7);positions.needsUpdate=true;o.computeVertexNormals();o.computeBoundingSphere();return o'
change(old,new)
# Replace the coarse neighbouring-cell exclusion with metric distance to burned grid cells.
start=s.index('function Nh(s,e){');end=s.index('function wf(',start)
math=(src/'simulation-math.cjs').read_text().split("if(typeof module")[0]
s=s[:start]+math+'function Nh(s,e){return createFireMask(s,e,60)}'+s[end:]
change('if(e==="inundacion"){let o=t<.3333333333333333?3:t<.6666666666666666?2:1;', 'if(e==="inundacion"){let o=t===0?4:t<.3333333333333333?3:t<.6666666666666666?2:1;')
change('r=t<1/3?3:t<2/3?2:1;', 'r=t===0?4:t<1/3?3:t<2/3?2:1;')
change('let a=e==="incendio"?Ef(Ft,Mi,i):[]','let a=e==="incendio"&&t>0?Ef(Ft,Mi,i):[]')
change('pn.count=t,pn.instanceColor','pn.count=ut.avance===0?0:t,pn.instanceColor')
# Rendering and bounds, explicitly using Three r180 already bundled by the author.
change('new kr("#f4f9ff","#b8ad92",1.4)','new kr("#eef4ff","#79856b",.85)')
change('new zi("#ffffff",2.3)','new zi("#fff3dc",1.8)')
change('An.toneMappingExposure=1.1','An.toneMappingExposure=.98')
change('0:new xe("#e3dfd3"),1:new xe("#9fbd88"),2:new xe("#c9d3a8")','0:new xe("#d5d0bc"),1:new xe("#628464"),2:new xe("#a4b486")')
change('n.count=s.length,wn.add(n),n','n.count=s.length,n.instanceMatrix.needsUpdate=true,n.instanceColor&&(n.instanceColor.needsUpdate=true),n.computeBoundingSphere(),wn.add(n),n')
change('let e=gt("acopios");','lastCandidates=s||[];let e=gt("acopios");')
change('Hy(c),Oy.forEach','lastFlags=c;Hy(c),Oy.forEach')
change('d.append(f,_,m),c.append(l,h,u,d),e.append(c)','let prepare=document.createElement("button");prepare.type="button";prepare.textContent="Preparar intervención";prepare.addEventListener("click",()=>{if(window.parent!==window){window.parent.postMessage({type:"territorio:prepare-candidate",id:a.id,scenario:ut.escenario},location.origin)}else{status("Abre este laboratorio desde la app para preparar el candidato.")}});d.append(f,prepare,_,m),c.append(l,h,u,d),e.append(c)')
# Do not frame constructions as people/demand, and use a deterministic ID tie-breaker.
change('o.demanda-r.demanda||(o.s.properties.areaM2??0)-(r.s.properties.areaM2??0)','o.demanda-r.demanda||(o.s.properties.areaM2??0)-(r.s.properties.areaM2??0)||r.s.properties.id.localeCompare(o.s.properties.id)')
change('Si','Si') if False else None
change('Zs=null,ut.escenario=s.dataset.escenario,ut.avance=1,$f(),ri(!0)','stopPlayback();ut.escenario=s.dataset.escenario;ut.avance=0;$f();ri(!0);status("Escenario listo. Pulsa Simular o recorre el avance.")')
change('if(Hh)return ut.avance=1,ri();Zs=performance.now()','startPlayback()')
change('Zs=null,ut.avance=Number(s.target.value),ri()','stopPlayback();ut.avance=Number(s.target.value);ri()')
change('ut.ignicion=fc(Ft,zh[kn.value]),vc(),ri(!0)','stopPlayback();ut.ignicion=fc(Ft,zh[kn.value]);vc();ri(!0)')
change('ut.viento=Number(s.target.value),vc(),ri(!0)','stopPlayback();ut.viento=Number(s.target.value);vc();ri(!0)')
change('ut.margen=Number(s.target.value),gt("margen-valor").textContent=`${ut.margen} m`,ri()','stopPlayback();ut.margen=Number(s.target.value);gt("margen-valor").textContent=`${ut.margen} m`;ri()')
change('if(Hh){si.target.copy(t),Hn.position.copy(n);return}','if(reducedMotion){si.target.copy(t);Hn.position.copy(n);dirty=true;return}')
# Initial camera includes whole city, and controls guarded until mesh decoder finishes.
change('escenario:"inundacion",avance:1','escenario:"inundacion",avance:0')
change('gt("cargando").hidden=!0','gt("cargando").hidden=!0;ready=true;setView("overview");document.querySelectorAll("[data-escenario],#simular,#pause-exercise,#reset-exercise,#save-exercise,#export-exercise,#avance,#inicio,#viento,#margen").forEach(el=>el.disabled=false);status("Maqueta lista. Elige un escenario y comienza el ejercicio.")')
change('var Bh=new hc,','''document.querySelectorAll("[data-escenario],#avance,#inicio,#viento,#margen").forEach(el=>el.disabled=true);
'''+(src/'enhancements.js').read_text()+'\nvar Bh=new hc,')
# Idle frames skip both WebGL and DOM label rendering; camera damping still invalidates.
start=s.index('An.setAnimationLoop(s=>{');end=s.index('});})();',start)+3
s=s[:start]+'''An.setAnimationLoop(time=>{
 if(document.hidden)return;
 if(Zs!==null){ut.avance=Math.min(1,(performance.now()-Zs)/playbackDuration);if(ut.avance===1){Zs=null;status("Ejercicio completo. Revisa los candidatos y sus verificaciones pendientes.")}if(pn)ri();}
 if(_c){_c(performance.now());dirty=true}
 const controlsChanged=si.update();
 const shaking=Zs!==null&&ut.escenario==="sismo"&&!reducedMotion&&ut.avance>0&&ut.avance<.4;
 let displacement=shaking?12*(1-ut.avance/.4):0;
 const x=Math.sin(time*.038)*displacement,z=Math.cos(time*.031)*displacement;
 if(ro.position.x!==x||ro.position.z!==z){ro.position.set(x,0,z);dirty=true;}
 if(time-lastRender<33)return;
 if(dirty||controlsChanged||shaking){An.render(wn,Hn);yc.render(wn,Hn);lastRender=time;dirty=false;}
});'''+s[end:]
change('en la zona del escenario','en la capa o ejercicio · no son personas')
change('Acopio sugerido','Candidato por verificar')
# Store only supplied source claims; no new legal assertions.
change('No es un pronóstico','No es un pronóstico') if False else None
change('CC BY-SA. Relieve:','licencia según fuente; catastro por verificar. Relieve:')
change('</details>','<p><strong>Mejoras integradas:</strong> margen de incendio medido desde celdas de 60 m; capas adaptadas al relieve; controles de pausa y comparación. El centro de una manzana o un espacio no acredita la condición de toda su superficie. Informe del ejercicio, no alerta vigente.</p><p><a href="/simulation-method.md" target="_blank" rel="noopener">Consultar fuentes y método aportados</a></p></details>')
s=s.replace('<script>','<script>window.addEventListener("error",()=>{const node=document.getElementById("cargando");if(node&&!node.hidden)node.textContent="No se pudo iniciar la escena 3D. Comprueba que WebGL esté habilitado o vuelve al mapa principal.";});window.addEventListener("unhandledrejection",()=>{const node=document.getElementById("cargando");if(node&&!node.hidden)node.textContent="No se pudo completar la carga 3D. Recarga el laboratorio o usa el mapa principal.";});</script><script>',1)
(out/'simulation.html').write_text(s)
(out/'simulation-method.md').write_text((src/'FUENTES_Y_METODO.md').read_text()+"\n\n## Integración en Territorio Preparado\nPausa, reinicio, duración visual, modo sin movimiento, vistas, captura, comparación e informe JSON. El incendio usa distancia en metros a celdas cuadradas de 60 m (margen supuesto), no vecindad gruesa de buckets. Capas ajustadas a altura del relieve. Las construcciones cercanas son registros catastrales, no conteos de personas. La licencia de catastro permanece sin verificar según el autor; integración local autorizada por el equipo, sin nueva publicación externa.\n")
# Integrate with the existing React shell, preserving every existing tab and map fix.
p=out/'assets/index-B2wY6ZdK.js';main=p.read_text()
if 'territorio:prepare-candidate' not in main:
 main=main.replace('function Q_(){','function CitySimulation(){return _.jsxs("section",{className:"simulation-integration",children:[_.jsx("iframe",{src:"/simulation.html",title:"Laboratorio de escenarios de Cali",style:{width:"100%",height:"min(1000px,85vh)",minHeight:"720px",border:"1px solid #d8e0d7",borderRadius:"16px"}}),_.jsx("p",{className:"small-note",children:_.jsx("a",{href:"/simulation.html",target:"_blank",rel:"noopener",children:"Abrir laboratorio a pantalla completa ↗"})})]})}function Q_(){',1)
 marker='const Mt=S?.spaces.features??[]'
 effect='F.useEffect(()=>{if(!S)return;const listener=event=>{if(event.origin!==location.origin||event.data?.type!=="territorio:prepare-candidate")return;const frame=document.querySelector("iframe[title=\\"Laboratorio de escenarios de Cali\\"]");if(!frame||event.source!==frame.contentWindow)return;const candidate=S.spaces.features.find(f=>f.properties.id===event.data.id);if(!candidate)return;dt(event.data.scenario==="sismo"?"seismic":"flood");bt(candidate);Y("plan");};window.addEventListener("message",listener);return()=>window.removeEventListener("message",listener)},[S]);'
 if marker not in main:raise RuntimeError('No se encontró estado principal')
 main=main.replace(marker,effect+marker,1)
 marker='_.jsx("a",{href:"/data/sectores.csv",download:!0'
 main=main.replace(marker,'_.jsx("button",{className:O==="simulation"?"active":"",onClick:()=>Y("simulation"),children:"06 Simular escenarios"}),'+marker,1)
 main=main.replace('O==="kit"?_.jsx(Y_,{}):y?', 'O==="simulation"?_.jsx(CitySimulation,{}):O==="kit"?_.jsx(Y_,{}):y?',1)
 p.write_text(main)
main=p.read_text()
if 'planFromSimulation' not in main:
 main=main.replace('[ii,jt]=F.useState(!0);F.useEffect','[ii,jt]=F.useState(!0);const [planScenario,setPlanScenario]=F.useState("flood"),[planFromSimulation,setPlanFromSimulation]=F.useState(!1);F.useEffect',1)
 main=main.replace('dt(event.data.scenario==="sismo"?"seismic":"flood");bt(candidate);Y("plan");','setPlanScenario(event.data.scenario==="sismo"?"earthquake":event.data.scenario==="incendio"?"wildfire":"flood");setPlanFromSimulation(!0);bt(candidate);Y("plan");',1)
 main=main.replace('onClick:()=>Y("plan")','onClick:()=>{setPlanFromSimulation(!1);setPlanScenario(pt==="seismic"?"earthquake":"flood");Y("plan")}',2)
 main=main.replace('data:S,origin:Ft,scope:P,scopeLabel:','data:S,origin:Ft,initialThreat:planScenario,scope:planFromSimulation?S.spaces.features:P,scopeLabel:',1)
 main=main.replace('scopeLabel:[H===','scopeLabel:planFromSimulation?"Todo Cali · candidato del simulacro":[H===',1)
 p.write_text(main)
intervention=out/'assets/Intervention-OeJ7xSVO.js';code=intervention.read_text()
if 'initialThreat:initialThreat' not in code:
 code=code.replace('scopeLabel:n,onMap:u}){const[r,o]=h.useState("flood")','scopeLabel:n,onMap:u,initialThreat:initialThreat="flood"}){const[r,o]=h.useState(initialThreat)',1)
 intervention.write_text(code)
print('Laboratorio mejorado e integrado')

# Keep the simulation entry as a direct link in the main navigation.
p=out/'assets/index-B2wY6ZdK.js'
main=p.read_text()
main=main.replace('_.jsx("button",{className:O==="simulation"?"active":"",onClick:()=>Y("simulation"),children:"06 Simular escenarios"})','_.jsxs("a",{href:"/simulation.html",children:["06 ",_.jsx("span",{children:"Simulación"})]})',1)
p.write_text(main)

# Render the direct navigation entry as a visible button matching the tabs.
main=p.read_text()
main=main.replace('_.jsxs("a",{href:"/simulation.html",children:["06 ",_.jsx("span",{children:"Simulación"})]})','_.jsxs("button",{type:"button",className:"simulation-direct-button",onClick:()=>{window.location.href="/simulation.html"},children:["06 ",_.jsx("span",{children:"Simulación"})]})',1)
p.write_text(main)
