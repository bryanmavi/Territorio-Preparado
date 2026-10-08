const assert=require('node:assert/strict');
const {createFireMask}=require('./simulation-math.cjs');
const mask=createFireMask([[0,0]],300,60);
assert.equal(mask(330,0),true);assert.equal(mask(330.01,0),false);
assert.equal(mask(300,300),false); // Former neighbour buckets over-excluded this point.
assert.equal(mask(30,30),true);assert.equal(createFireMask([],300)(0,0),false);
assert.equal(createFireMask([[0,0]],0)(30,30),true);assert.equal(createFireMask([[0,0]],0)(31,0),false);
assert.throws(()=>createFireMask([],NaN));
// Compare the index against a brute-force distance to every square cell.
const cells=Array.from({length:300},(_,i)=>[(i*197)%3000-1500,(i*311)%4000-2000]);
for(const radius of [0,100,300,1000]){
 const fast=createFireMask(cells,radius);
 for(let i=0;i<1000;i++){
  const x=(i*331)%5000-2500,y=(i*797)%6000-3000;
  const expected=cells.some(([cx,cy])=>Math.max(Math.abs(x-cx)-30,0)**2+Math.max(Math.abs(y-cy)-30,0)**2<=radius**2);
  assert.equal(fast(x,y),expected,`radius=${radius} point=${x},${y}`);
 }
}
console.log('Distancias y máscara: 4.000 casos contrastados con cálculo exhaustivo.');
