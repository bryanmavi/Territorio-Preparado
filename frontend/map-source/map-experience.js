/* Original interaction layer for Territorio Preparado's archived inventory. */
function TerritoryMapTools({data,spaces,scope}) {
  const map=Rc();
  const [expanded,setExpanded]=F.useState(false);
    F.useEffect(()=>{
    const container=map.getContainer();
    const observer=new ResizeObserver(()=>map.invalidateSize({pan:false}));
    observer.observe(container);
    return()=>observer.disconnect();
  },[map]);
  function center(){
    const [commune,neighborhood]=scope.split('|');
    const features=neighborhood?data.neighborhoods.features.filter(f=>f.properties.name===neighborhood&&(!commune||f.properties.commune===commune)):commune&&commune!=='unassigned'?data.communes.features.filter(f=>f.properties.code===commune):[];
    const bounds=features.length?Yo.geoJSON({type:'FeatureCollection',features}).getBounds():spaces.length?Yo.latLngBounds(spaces.map(f=>[f.properties.coordinates[1],f.properties.coordinates[0]])):null;
    if(bounds?.isValid())map.fitBounds(bounds,{padding:[30,50],maxZoom:16});
  }
  function expand(){
    const wrap=map.getContainer().closest('.map-wrap');
    const next=!expanded;wrap.classList.toggle('map-expanded',next);setExpanded(next);
  }
  F.useEffect(()=>{
    const escape=event=>{if(event.key==='Escape'){map.getContainer().closest('.map-wrap').classList.remove('map-expanded');setExpanded(false)}};
    document.addEventListener('keydown',escape);
    return()=>{document.removeEventListener('keydown',escape);map.getContainer().closest('.map-wrap')?.classList.remove('map-expanded')};
  },[map]);
  return _.jsxs('div',{className:'territory-map-tools',ref:el=>{if(el){Yo.DomEvent.disableClickPropagation(el);Yo.DomEvent.disableScrollPropagation(el)}},children:[
    _.jsx('button',{type:'button',onClick:center,title:'Volver a encuadrar el sector consultado',children:'⌖ Centrar sector'}),
    _.jsx('button',{type:'button',onClick:expand,'aria-pressed':expanded,children:expanded?'↙ Reducir mapa':'↗ Ampliar mapa'}),
    _.jsx('p',{className:'map-tool-hint',children:'Acerca para ver las huellas · selecciona un lugar para consultar su ficha'})
  ]});
}
function TerritoryRecords({spaces,threat,select,scope}) {
  const map=Rc();
  const [view,setView]=F.useState(0);
  C_({moveend(){setView(v=>v+1)},zoomend(){setView(v=>v+1)}});
  const zoom=map.getZoom();
  const features=F.useMemo(()=>{
    const bounds=map.getBounds().pad(.15);
    const visible=spaces.filter(f=>bounds.contains([f.properties.coordinates[1],f.properties.coordinates[0]]));
    if(zoom>=15)return visible;
    const groups=new Map();
    visible.forEach(f=>{
      const pt=map.project([f.properties.coordinates[1],f.properties.coordinates[0]],zoom);
      const key=[Math.floor(pt.x/54),Math.floor(pt.y/54)].join(':');
      if(!groups.has(key))groups.set(key,[]);groups.get(key).push(f);
    });
    return [...groups].map(([id,members])=>{
      if(members.length===1)return {...members[0],geometry:{type:'Point',coordinates:members[0].properties.coordinates}};
      const coordinates=[0,0];members.forEach(f=>{coordinates[0]+=f.properties.coordinates[0]/members.length;coordinates[1]+=f.properties.coordinates[1]/members.length});
      return {type:'Feature',geometry:{type:'Point',coordinates},properties:{id,cluster:true,count:members.length,sourceKey:members.every(f=>f.properties.sourceKey==='sports')?'sports':members.every(f=>f.properties.sourceKey==='publicSpaces')?'publicSpaces':'mixed',crossed:members.filter(f=>f.properties[threat].length).length},members};
    });
  },[spaces,threat,view,zoom,map]);
  const color=f=>f.properties.cluster?(f.properties.sourceKey==='sports'?'#356dba':f.properties.sourceKey==='mixed'?'#24483e':'#177b68'):f.properties[threat].length?'#b45b32':f.properties.sourceKey==='sports'?'#356dba':'#177b68';
  return _.jsx(Su,{
    data:{type:'FeatureCollection',features},
    style:f=>({color:f.properties.cluster?'#fff':color(f),weight:2,fillColor:color(f),fillOpacity:f.properties.cluster?.95:.3}),
    pointToLayer:(f,latlng)=>Yo.circleMarker(latlng,{radius:f.properties.cluster?Math.min(22,12+Math.log2(f.properties.count)):7,color:'#fff',weight:2,fillColor:color(f),fillOpacity:.95}),
    onEachFeature:(f,layer)=>{
      if(f.properties.cluster){
        layer.bindTooltip(String(f.properties.count),{permanent:true,direction:'center',className:'territory-cluster-count'});

        layer.on('click',()=>{const bounds=Yo.latLngBounds(f.members.map(m=>[m.properties.coordinates[1],m.properties.coordinates[0]]));if(map.getZoom()<14)map.fitBounds(bounds,{padding:[45,70],maxZoom:15});else map.setView(layer.getLatLng(),15)});
      }else{
        const node=document.createElement('div');const title=document.createElement('strong');title.textContent=f.properties.name;node.append(title);
        const line=document.createElement('div');line.textContent=(f.properties.neighborhood||'Barrio sin asignar')+' · '+(f.properties[threat].length?'Con cruce de amenaza':'Sin cruce detectado');node.append(line);
        layer.bindTooltip(node,{className:'territory-place-tooltip'});layer.on('click',()=>select(spaces.find(s=>s.properties.id===f.properties.id)||f));
      }
    }
  },scope+'|'+threat+'|'+zoom+'|'+view+'|'+spaces.map(f=>f.properties.id).join(','));
}
function TerritoryQuickPlaces({spaces,selected,onSelect,query}) {
  const [open,setOpen]=F.useState(true);
  return _.jsxs('section',{className:'quick-places',children:[
    _.jsxs('button',{type:'button',className:'quick-places-heading','aria-expanded':open,onClick:()=>setOpen(!open),children:[_.jsx('span',{children:'Lugares del sector'}),_.jsx('span',{children:open?'−':'+'})]}),
    open&&_.jsxs('div',{children:[_.jsx('p',{className:'quick-places-note',children:query?'Coincidencias de tu búsqueda':'Selecciona un lugar para acercarte al mapa.'}),
      ...spaces.slice(0,6).map(f=>_.jsxs('button',{type:'button',className:'quick-place'+(selected?.properties.id===f.properties.id?' is-selected':''),onClick:()=>onSelect(f),children:[_.jsx('span',{className:'quick-place-dot '+(f.properties.sourceKey==='sports'?'sports':'public')}),_.jsxs('span',{children:[_.jsx('strong',{children:f.properties.name}),_.jsx('small',{children:f.properties.neighborhood||'Barrio por confirmar'})]}),_.jsx('span',{children:'↗'})]},f.properties.id)),
      !spaces.length&&_.jsx('p',{className:'quick-places-note',children:'Sin registros para estos filtros.'}),
      spaces.length>6&&_.jsxs('a',{className:'quick-places-all',href:'#map-inventory',children:['Consultar los ',new Intl.NumberFormat('es-CO').format(spaces.length),' registros ↓']})]})
  ]});
}
