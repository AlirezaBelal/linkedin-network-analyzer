'use strict';
const LIMITS={bytes:2097152,rows:2000,columns:32,field:2048};
const categories=['HR / Recruiter','AI / Data','Product','Developer','Other'];
const categoryPoints={Product:5,Developer:4,'AI / Data':4,'HR / Recruiter':3,Other:1};
const recommendations={Product:'Prioritize outreach','AI / Data':'Prioritize outreach',Developer:'Explore collaboration','HR / Recruiter':'Keep warm',Other:'Review manually'};
const rules=[['HR / Recruiter',['hr','recruiter','talent','people','human resources']],['AI / Data',['machine learning','deep learning','data scientist','data analyst','data engineer','ai engineer','ml engineer','artificial intelligence']],['Product',['product manager','head of product','product owner','product lead','product']],['Developer',['developer','engineer','cto','backend','frontend','fullstack','full stack','software','programmer']]];
const sample=[['Ava','Senior Product Manager','Example Labs','ava'],['Noah','Machine Learning Engineer','Example AI',''],['Mina','Technical Recruiter','Example Talent','mina'],['Omid','Backend Software Engineer','Example Systems','omid'],['Sara','Community Founder','Example Studio','']].map(([name,Position,Company,url])=>({'First Name':name,'Last Name':'Example',Position,Company,URL:url?'https://example.invalid/'+url:''}));
const pythonWhitespace=/[\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+/gu;
const pythonTrim=new RegExp('^'+pythonWhitespace.source+'|'+pythonWhitespace.source+'$','gu');
function trimValue(value){return String(value??'').replace(pythonTrim,'');}
function normalizeTitle(value){return trimValue(value).toLowerCase().replace(pythonWhitespace,' ');}
function hasValue(value){return String(value??'').replace(pythonWhitespace,'').length>0;}
function classify(value){const title=normalizeTitle(value);for(const [category,terms] of rules){for(const term of terms)if(new RegExp('(^|[^\\p{L}\\p{N}_])'+term+'($|[^\\p{L}\\p{N}_])','u').test(title))return {category,matched:term};if(category==='AI / Data'&&/^(ai|ml|data)(?: |$)/.test(title))return {category,matched:title.split(' ')[0]+' prefix'};if(category==='Product'&&title==='pm')return {category,matched:'pm'};}return {category:'Other',matched:'No supported keyword'};}
function categorizeTitle(value){return classify(value).category;}
function analyze(records){return records.map(r=>{const match=classify(r.Position),completeness=['Company','Position','URL'].filter(k=>hasValue(r[k])).length,score=categoryPoints[match.category]+completeness;return {...r,...match,completeness,score,priority:score>=7?'High':score>=5?'Medium':'Low',recommendation:recommendations[match.category]};});}
function parseCSV(text){
 if(new TextEncoder().encode(text).length>LIMITS.bytes)throw Error('File exceeds 2 MiB. Use the Python CLI for larger exports.');
 if(text.includes('\0'))throw Error('NUL characters are not supported. Save a UTF-8 CSV.');
 const lines=text.replace(/^\uFEFF/,'').split(/\r\n|\n|\r/);let start=0;
 for(let i=0;i<Math.min(12,lines.length);i++)if(lines[i].split(',').some(s=>trimValue(trimValue(s).replace(/^"|"$/g,''))==='Position')){start=i;break;}
 text=lines.slice(start).join('\n');let rows=[],row=[],field='',quoted=false,closed=false,atStart=true;
 function cell(){row.push(field);field='';closed=false;atStart=true;if(row.length>LIMITS.columns)throw Error('At most 32 columns are supported.');}
 function line(){cell();if(row.some(v=>hasValue(v)))rows.push(row);row=[];if(rows.length>LIMITS.rows+1)throw Error('At most 2,000 records are supported.');}
 for(let i=0;i<text.length;i++){const c=text[i];if(quoted){if(c==='"'){if(text[i+1]==='"'){field+='"';i++;}else{quoted=false;closed=true;}}else field+=c;}else if(c===',')cell();else if(c==='\n')line();else if(c==='"'&&atStart){quoted=true;atStart=false;}else{if(closed||c==='"')throw Error('Malformed CSV quoting. Use comma-separated UTF-8 CSV.');field+=c;atStart=false;}if(field.length>LIMITS.field)throw Error('A field exceeds 2,048 characters. Use the CLI.');}
 if(quoted)throw Error('Unclosed CSV quote. Correct the CSV and retry.');if(field||row.length||closed)line();
 const headers=(rows.shift()||[]).map(s=>trimValue(s));if(!headers.length||headers.some(s=>!s)||new Set(headers).size!==headers.length)throw Error('Column names must be non-empty and unique.');
 if(!headers.includes('Position'))throw Error('A case-sensitive Position column is required.');if(!rows.length)throw Error('No records found. Include at least one data row.');
 return {headers,records:rows.map(values=>{if(values.length!==headers.length)throw Error('Inconsistent row width. Every row must match the header.');const r=Object.create(null);headers.forEach((k,i)=>r[k]=values[i]);return r;})};
}
function filterRecords(rows,{query='',category='all',priority='all'}={}){return rows.filter(r=>['First Name','Last Name','Position','Company'].map(k=>r[k]||'').join(' ').toLowerCase().includes(query.trim().toLowerCase())&&(category==='all'||r.category===category)&&(priority==='all'||r.priority===priority));}
function safeCell(value){let s=String(value??'');if(/^[\s\u0000-\u001f]*[=+@-]/u.test(s)||/^[\t\r\n]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"';}
function exportCSV(rows){return '\uFEFF'+[['First Name','Last Name','Position','Company','Category','Action Recommendation','Priority Score','Priority','Score Basis'],...rows.map(r=>[r['First Name'],r['Last Name'],r.Position,r.Company,r.category,r.recommendation,r.score,r.priority,categoryPoints[r.category]+' relevance + '+r.completeness+' completeness; human review required'])].map(row=>row.map(safeCell).join(',')).join('\r\n');}
if(typeof module!=='undefined')module.exports={LIMITS,categories,categoryPoints,recommendations,rules,sample,classify,categorizeTitle,analyze,parseCSV,filterRecords,safeCell,exportCSV};
if(typeof document!=='undefined'){
 const $=id=>document.getElementById(id);let rows=analyze(sample),mode='sample',page=0,operation=0;
 function el(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
 for(const value of categories){const o=el('option',value);o.value=value;$('category').append(o);}
 function visible(){return filterRecords(rows,{query:$('search').value,category:$('category').value,priority:$('priority').value});}
 function reset(){for(const id of ['search','category','priority'])$(id).value=id==='search'?'':'all';page=0;}
 function render(){
  const filtered=visible();$('records').replaceChildren();$('dataset-label').textContent=mode==='sample'?'Fictional sample · 5 invented records':'Local CSV · selected data stays in this tab';
  $('result-count').textContent=filtered.length.toLocaleString('en-US')+' of '+rows.length.toLocaleString('en-US')+' records';$('total-count').textContent=rows.length.toLocaleString('en-US');$('review-count').textContent=rows.filter(r=>r.category==='Other').length.toLocaleString('en-US');
  for(const r of filtered.slice(page*20,(page+1)*20)){
   const tr=el('tr'),person=el('td');person.append(el('strong',[r['First Name'],r['Last Name']].filter(Boolean).join(' ')||'Unnamed record'),el('span',r.Position||'No position','sub'),el('span',r.Company||'No company','sub'));
   const group=el('td');group.append(el('span',r.category,'badge'));const rec=el('td');rec.append(el('span',r.recommendation),el('span','Human review required','sub'));
   const score=el('td');score.append(el('strong',r.score+' / 8','score'),el('span',r.priority+' priority','sub'));
   const basis=el('td'),details=el('details');details.append(el('summary','Explain score'));const list=el('ul');for(const text of ['Rule: '+r.matched+'.','Precedence: HR → AI / Data → Product → Developer.','Category relevance: '+categoryPoints[r.category]+'.','Completeness: '+r.completeness+' / 3 (Company, Position, URL).','No engagement or relationship data is used.'])list.append(el('li',text));details.append(list);basis.append(details);tr.append(person,group,rec,score,basis);$('records').append(tr);
  }
  $('empty').hidden=filtered.length>0;$('export').disabled=!filtered.length;$('prev').disabled=page===0;$('next').disabled=(page+1)*20>=filtered.length;$('page-count').textContent=filtered.length?'Page '+(page+1)+' of '+Math.ceil(filtered.length/20):'No results';
  $('distribution').replaceChildren();for(const c of categories){const count=filtered.filter(r=>r.category===c).length,item=el('li'),label=el('div');label.append(el('span',c),el('strong',String(count)));const meter=el('meter');meter.min=0;meter.max=Math.max(filtered.length,1);meter.value=count;meter.setAttribute('aria-label',c+' records in filtered view');item.append(label,meter);$('distribution').append(item);}
 }
 for(const id of ['search','category','priority'])$(id).addEventListener('input',()=>{page=0;render();});
 for(const id of ['reset','empty-reset'])$(id).addEventListener('click',()=>{reset();render();$('search').focus();});
 for(const [id,delta] of [['prev',-1],['next',1]])$(id).addEventListener('click',()=>{page+=delta;render();$('results-heading').focus();});
 $('consent').addEventListener('change',()=>{$('local-file').disabled=!$('consent').checked;});
 function restore(){operation++;rows=analyze(sample);mode='sample';$('local-file').value='';$('local-file').disabled=true;$('consent').checked=false;$('file-error').hidden=true;$('file-state').textContent='Local data cleared. Fictional sample restored.';reset();render();}
 $('restore').addEventListener('click',restore);
 $('local-file').addEventListener('change',async()=>{
  const token=++operation,file=$('local-file').files[0];if(!file)return;$('file-error').hidden=true;$('file-state').textContent='Reading and analyzing locally…';$('local-file').disabled=true;
  try{if(file.size>LIMITS.bytes)throw Error('File exceeds 2 MiB. Use the Python CLI.');const bytes=await file.arrayBuffer();if(token!==operation)return;let text;try{text=new TextDecoder('utf-8',{fatal:true}).decode(bytes);}catch{throw Error('Invalid UTF-8. Save the CSV as UTF-8 and retry.');}rows=analyze(parseCSV(text).records);mode='local';reset();render();$('file-state').textContent='Local analysis ready. No file or records were transmitted.';}
  catch(e){$('file-error').textContent=e instanceof Error&&/^(File exceeds|At most|NUL|Malformed|Unclosed|Column names|A case-sensitive|No records|Inconsistent|A field|Invalid UTF-8)/.test(e.message)?e.message:'Could not read this file. Select a valid UTF-8 CSV.';$('file-error').hidden=false;$('file-error').focus();$('file-state').textContent='Previous dataset retained. Correct the file or restore the sample.';}
  finally{if(token===operation){$('local-file').value='';$('local-file').disabled=!$('consent').checked;}}
 });
 $('export').addEventListener('click',()=>{const url=URL.createObjectURL(new Blob([exportCSV(visible())],{type:'text/csv;charset=utf-8'})),a=el('a');a.href=url;a.download='network-atlas-review.csv';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);$('file-state').textContent='Filtered review CSV saved locally. Keep private reports outside shared folders.';});
 for(const b of document.querySelectorAll('[data-copy]'))b.addEventListener('click',async()=>{try{await navigator.clipboard.writeText($(b.dataset.copy).textContent);$('copy-state').textContent='Command copied.';}catch{$('copy-state').textContent='Clipboard unavailable. Select and copy the command manually.';}});
 window.addEventListener('pagehide',()=>{operation++;rows=[];$('records').replaceChildren();$('search').value='';$('local-file').value='';});
 window.addEventListener('pageshow',e=>{if(e.persisted)restore();});render();
}

