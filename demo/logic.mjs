// Deterministic browser-side adaptation of scripts/modules/*.py.
// Fictional portfolio records only. Never process real LinkedIn exports here.
export const samples=[
 {name:"Ava Example",company:"Example Labs",position:"Senior Product Manager",url:"example-product-lead"},
 {name:"Noah Example",company:"Example AI",position:"Machine Learning Engineer",url:"example-ml-engineer"},
 {name:"Mina Example",company:"Example Talent",position:"Technical Recruiter",url:"example-recruiter"},
 {name:"Omid Example",company:"Example Systems",position:"Backend Software Engineer",url:"example-software-engineer"},
 {name:"Sara Example",company:"Example Studio",position:"Founder",url:"example-founder"},
 {name:"Dara Example",company:"",position:"Data Analyst",url:""},
 {name:"Leila Example",company:"Example Product",position:"Product Owner",url:""},
 {name:"Roya Example",company:"",position:"Community Organizer",url:""}
];
export const categories=["Product","AI / Data","Developer","HR / Recruiter","Other"];
export const recommendations={Product:"Prioritize outreach","AI / Data":"Prioritize outreach",Developer:"Explore collaboration","HR / Recruiter":"Keep warm",Other:"Review manually"};
export const relevance={Product:5,Developer:4,"AI / Data":4,"HR / Recruiter":3,Other:1};
export function categorizeTitle(value){
 const title=String(value??"").trim().toLowerCase();
 if(["hr","recruiter","talent","people","human resources"].some(s=>title.includes(s)))return "HR / Recruiter";
 if(["machine learning","deep learning","data scientist","data analyst","data engineer","ai engineer","ml engineer","artificial intelligence"].some(s=>title.includes(s))||["ai ","ml ","data "].some(s=>title.startsWith(s)))return "AI / Data";
 if(["product manager","head of product","product owner","product lead","product"].some(s=>title.includes(s))||title==="pm")return "Product";
 if(["developer","engineer","cto","backend","frontend","fullstack","full stack","software","programmer"].some(s=>title.includes(s)))return "Developer";
 return "Other";
}
export function analyze(r){
 const category=categorizeTitle(r.position);
 const completeness=["company","position","url"].filter(key=>String(r[key]??"").trim()).length;
 const score=relevance[category]+completeness;
 return {...r,category,score,completeness,recommendation:recommendations[category],priority:score>=7?"High":score>=5?"Medium":"Low"};
}
export function filterSort(records,{query="",category="All",priority="All",sort="score"}={}){
 const q=query.trim().toLowerCase();
 return records.map(analyze).filter(r=>(category==="All"||r.category===category)&&(priority==="All"||r.priority===priority)&&[r.name,r.company,r.position,r.category].some(x=>x.toLowerCase().includes(q))).sort((a,b)=>sort==="name"?a.name.localeCompare(b.name):sort==="category"?a.category.localeCompare(b.category)||b.score-a.score:b.score-a.score||a.name.localeCompare(b.name));
}
