import {chromium} from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const out=process.env.QA_OUTPUT||'qa-evidence',url=process.env.PRODUCT_URL||'http://127.0.0.1:8765/';
await mkdir(out,{recursive:true});const browser=await chromium.launch();const reports=[];
const fixture='First Name,Last Name,Position,Company,URL,Email Address\n"<img src=x onerror=alert(1)>",Example,Product Manager,"=2+2",https://example.invalid/private,synthetic@example.invalid\nSample,Example,Director,NA,,\n';
async function select(page,buffer){await page.locator('#consent').check();const chooser=page.waitForEvent('filechooser');await page.locator('#local-file').click();await(await chooser).setFiles({name:'fictional.csv',mimeType:'text/csv',buffer:Buffer.from(buffer)});}
async function scan(page,name){const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();await writeFile(out+'/'+name+'-accessibility.json',JSON.stringify(result,null,2));assert.deepEqual(result.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})),[]);}
try{for(const width of [320,375,390,768,1024,1440,1920]){
 const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce',acceptDownloads:true});const page=await context.newPage();const errors=[],requests=[],bad=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('request',r=>requests.push({url:r.url(),method:r.method()}));page.on('response',r=>{if(r.status()>=400)bad.push(r.status()+' '+r.url());});
 await page.goto(url,{waitUntil:'networkidle'});assert.equal(await page.locator('#records tr').count(),5);assert(await page.locator('#local-file').isDisabled());
 await page.keyboard.press('Tab');assert(await page.evaluate(()=>document.activeElement!==document.body&&getComputedStyle(document.activeElement).outlineStyle!=='none'),'focus');
 assert.equal(await page.locator('h1').count(),1);assert(await page.locator('h1').evaluate(e=>parseFloat(getComputedStyle(e).fontSize)<=60));
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow');assert(await page.locator('img').evaluateAll(xs=>xs.every(x=>x.complete&&x.naturalWidth)),'assets');
 for(const a of await page.locator('a[href^="#"]').all()){assert(await page.locator(await a.getAttribute('href')).count());}
 await page.screenshot({path:out+'/product-'+width+'.png',fullPage:true});
 if(width===1440){await page.locator('#workspace').scrollIntoViewIfNeeded();await page.screenshot({path:out+'/portfolio-preview.png'});}
 await page.locator('#search').fill('Ava');await page.locator('#category').selectOption('Product');await page.locator('#priority').selectOption('High');assert.equal(await page.locator('#records tr').count(),1);
 await page.locator('summary').first().focus();await page.keyboard.press('Enter');assert(await page.locator('details').first().getAttribute('open')!==null);assert.match(await page.locator('details').first().textContent(),/Category relevance: 5/);
 await page.locator('#search').fill('no-such-person');assert(await page.locator('#empty').isVisible());assert(await page.locator('#export').isDisabled());await page.locator('#empty-reset').click();assert.equal(await page.locator('#records tr').count(),5);
 await scan(page,'sample-'+width);
 await select(page,fixture);await page.waitForFunction(()=>document.querySelector('#dataset-label').textContent.startsWith('Local CSV'));assert.equal(await page.locator('#records tr').count(),2);assert.equal(await page.locator('#records img').count(),0);assert.equal(await page.locator('#records a').count(),0);assert.match(await page.locator('#records').textContent(),/<img src=x/);assert.match(await page.locator('#records').textContent(),/Other/);
 await scan(page,'import-'+width);
 const dl=page.waitForEvent('download');await page.locator('#export').click();const download=await dl;await download.saveAs(out+'/synthetic-review-'+width+'.csv');const csv=await readFile(out+'/synthetic-review-'+width+'.csv','utf8');assert.match(csv,/'=2\+2/);assert.doesNotMatch(csv,/private|synthetic@example|Email Address|URL/);
 for(const [data,message] of [['Position,Position\nA,B','unique'],['Position,Company\nA','width'],['Position\n"broken','quote'],['Position\n'+ 'x'.repeat(2049),'2,048'],[Buffer.from([255]),'UTF-8'],['x'.repeat(2097153),'2 MiB']]){
  await select(page,data);await page.locator('#file-error').waitFor({state:'visible'});assert.match(await page.locator('#file-error').textContent(),new RegExp(message));assert.equal(await page.locator('#records tr').count(),2);
 }
 await page.locator('#restore').click();assert.equal(await page.locator('#records tr').count(),5);assert(await page.locator('#local-file').isDisabled());assert(!await page.locator('#consent').isChecked());assert.doesNotMatch(await page.locator('#records').textContent(),/<img src=x/);
 const memoryBefore=await page.evaluate(()=>performance.memory?.usedJSHeapSize||null),started=Date.now();
 await select(page,'First Name,Position,Company,URL\n'+Array.from({length:2000},()=> 'Example,Backend Engineer,'+'x'.repeat(1000)+',\n').join(''));
 await page.waitForFunction(()=>document.querySelector('#total-count').textContent==='2,000');const milliseconds=Date.now()-started,memoryAfter=await page.evaluate(()=>performance.memory?.usedJSHeapSize||null);assert(milliseconds<10000,'2,000-row input performance');assert.equal(await page.locator('#records tr').count(),20);await page.locator('#next').click();assert.match(await page.locator('#page-count').textContent(),/Page 2 of 100/);
 await page.locator('#restore').click();await page.reload();assert.equal(await page.locator('#records tr').count(),5);
 assert(await page.evaluate(()=>!localStorage.length&&!sessionStorage.length));assert.deepEqual(await page.evaluate(()=>indexedDB.databases()),[]);assert.deepEqual(await context.cookies(),[]);
 const external=requests.filter(r=>!r.url.startsWith(new URL(url).origin));assert.deepEqual(external,[]);assert(requests.every(r=>r.method==='GET'));assert.deepEqual(errors,[]);assert.deepEqual(bad,[]);
 reports.push({width,url,overflow:'passed',sample:'passed',filters:'passed',keyboard:'passed',filePicker:'passed',escaping:'passed',download:'passed',errors:[],unexpectedRequests:[],maxInput:{rows:2000,milliseconds,memoryBefore,memoryAfter,memoryNote:'Chromium heap estimates, not a certification'},reset:'passed'});await context.close();
}}finally{await writeFile(out+'/results.json',JSON.stringify(reports,null,2));await browser.close();}

