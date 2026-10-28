const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
try{const page=await browser.newPage({viewport:{width:1280,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:4181/operations.html');await page.getByRole('link',{name:/Abrir IA/}).click();
await page.locator('#engine-status').filter({hasText:'sos_weights_present'}).waitFor();
await page.selectOption('#locale','en');assert.equal(await page.locator('h1').textContent(),'Disaster AI');
await page.selectOption('#sos-language','en');await page.fill('#sos-text','There was an earthquake and we need water and medical help.');
await page.locator('#sos-form button').click();await page.locator('#sos-result').filter({hasText:'semantic_labels_verified'}).waitFor({timeout:90000});
assert.match(await page.locator('#sos-result').textContent(),/human_review/);await page.locator('#message-list tr').first().waitFor();
await page.selectOption('#sos-language','es');await page.fill('#sos-text','Necesitamos agua y ayuda médica después del terremoto.');
await page.locator('#sos-form button').click();await page.locator('#sos-result').filter({hasText:'We need water'}).waitFor({timeout:90000});
if(process.argv.includes('--damage')){
// Technical smoke only: identical public example on both inputs and artificial bounds.
// This is not a pre/post accuracy evaluation or a georeferenced damage assessment.
const image=require('node:path').resolve('models/xview2/source/overlay_output_to_image/santa-rosa-wildfire_00000007_post_disaster.png');
await page.locator('input[name=pre]').setInputFiles(image);await page.locator('input[name=post]').setInputFiles(image);
await page.fill('input[name=bounds]','[0,0,1,1]');
const response=page.waitForResponse(r=>r.url().endsWith('/api/v1/analyze-damage'),{timeout:180000});
await page.locator('#damage-form button').click();const result=await response;
assert.equal(result.status(),200);const data=await result.json();assert.ok(data.features.length>0);
await page.locator('#download').waitFor();assert.ok(await page.locator('#damage-map path').count()>0);
console.log('PASS: real xView2 upload, GeoJSON, map overlay and download; regions:',data.features.length);
}
await page.setViewportSize({width:390,height:844});assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
assert.deepEqual(errors,[]);console.log('PASS: navigation, English interface, real local BERT in English and Spanish, stored message, mobile layout, no browser errors');
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exit(1)});
