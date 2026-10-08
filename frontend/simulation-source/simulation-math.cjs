/* Spatial checks for the educational fire grid. Units: local metres. */
function createFireMask(cells, margin, cellSize = 60) {
  if (!Number.isFinite(margin) || margin < 0 || !Number.isFinite(cellSize) || cellSize <= 0) throw new Error('Margen o celda inválidos');
  const half = cellSize / 2;
  const bucketSize = Math.max(cellSize, margin + half);
  const buckets = new Map();
  for (const [x,y] of cells) {
    const key = `${Math.floor(x/bucketSize)},${Math.floor(y/bucketSize)}`;
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key).push([x,y]);
  }
  return (x,y) => {
    const bx=Math.floor(x/bucketSize), by=Math.floor(y/bucketSize);
    for(let i=-1;i<=1;i++) for(let j=-1;j<=1;j++) {
      for(const [cx,cy] of buckets.get(`${bx+i},${by+j}`)||[]) {
        const dx=Math.max(Math.abs(x-cx)-half,0),dy=Math.max(Math.abs(y-cy)-half,0);
        if(dx*dx+dy*dy<=margin*margin) return true;
      }
    }
    return false;
  };
}
if(typeof module!=='undefined')module.exports={createFireMask};
