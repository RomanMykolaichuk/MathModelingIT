"use strict";

const E = globalThis.MathModelingLab;
const CATALOG = globalThis.MathModelingCatalog || [];
const $ = (id) => document.getElementById(id);
const qsa = (sel) => Array.from(document.querySelectorAll(sel));
const fmt = (x, digits=2) => Number.isFinite(x) ? Number(x).toFixed(digits).replace(/\.00$/, "") : "∞";

function downloadJson(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], {type:"application/json"});
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function lineSvg(series, horizon, yMin, yMax) {
  const w=760, h=310, p=42;
  const X=t=>p+(t/horizon)*(w-2*p);
  const Y=v=>h-p-((v-yMin)/(yMax-yMin||1))*(h-2*p);
  const path=pts=>pts.map((d,i)=>(i?"L":"M")+X(d.t).toFixed(1)+" "+Y(d.v).toFixed(1)).join(" ");
  const zeroY=Y(0);
  return '<svg viewBox="0 0 '+w+' '+h+'" role="img">'+
    '<line class="axis" x1="'+p+'" y1="'+(h-p)+'" x2="'+(w-p)+'" y2="'+(h-p)+'"></line>'+
    '<line class="axis" x1="'+p+'" y1="'+p+'" x2="'+p+'" y2="'+(h-p)+'"></line>'+
    (yMin<0&&yMax>0?'<line class="zero-line" x1="'+p+'" y1="'+zeroY+'" x2="'+(w-p)+'" y2="'+zeroY+'"></line>':'')+
    '<path class="line-a" d="'+path(series[0])+'"></path>'+
    '<path class="line-b" d="'+path(series[1])+'"></path>'+
    '<text class="axis-label" x="'+(w-p-20)+'" y="'+(h-12)+'">t</text>'+
    '<text class="axis-label" x="8" y="'+(p+5)+'">S(t)</text>'+
    '<text class="legend" x="'+(p+10)+'" y="24">v₁</text>'+
    '<text class="legend" x="'+(p+55)+'" y="24">v₂</text>'+
    '</svg>';
}

function networkSvg(result) {
  const pos={A:[90,75],B:[90,225],C:[270,55],D:[270,165],E:[470,90],F:[470,210],G:[665,145]};
  const edges=[];
  E.BASE_TASKS.forEach(t=>t.preds.forEach(p=>edges.push([p,t.task])));
  const criticalEdges=new Set(result.path.slice(1).map((n,i)=>result.path[i]+"-"+n));
  let out='<svg viewBox="0 0 760 290" role="img"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#49657e"></path></marker></defs>';
  edges.forEach(edge=>{
    const p1=pos[edge[0]], p2=pos[edge[1]];
    const cls=criticalEdges.has(edge[0]+"-"+edge[1])?"network-edge critical":"network-edge";
    out+='<line class="'+cls+'" x1="'+(p1[0]+24)+'" y1="'+p1[1]+'" x2="'+(p2[0]-24)+'" y2="'+p2[1]+'"></line>';
  });
  result.rows.forEach(row=>{
    const p=pos[row.task], cls=row.critical?"network-node critical":"network-node";
    out+='<circle class="'+cls+'" cx="'+p[0]+'" cy="'+p[1]+'" r="24"></circle><text class="network-label" x="'+p[0]+'" y="'+p[1]+'">'+row.task+'</text>';
  });
  return out+"</svg>";
}

function renderCatalog() {
  const root=$("course-catalog");
  root.innerHTML="";
  CATALOG.forEach(item=>{
    const card=document.createElement("article");
    card.className="panel catalog-card";
    const source="https://github.com/RomanMykolaichuk/MathModelingIT/tree/main/lessons/"+item.id;
    const status=item.status==="interactive"?"інтерактивна лабораторія":"Python package";
    card.innerHTML=
      '<span class="catalog-code">'+item.code+'</span>'+
      '<span class="catalog-status '+item.status+'">'+status+'</span>'+
      '<h3>'+item.title+'</h3>'+
      '<p><strong>Challenge:</strong> '+item.challenge+'</p>'+
      '<p class="instructor-only"><strong>Transfer:</strong> '+item.transfer+'</p>'+
      '<div class="catalog-actions">'+
      (item.status==="interactive"?'<a class="primary" href="'+item.anchor+'">Відкрити Lab</a>':'')+
      (item.notesUrl?'<a href="'+item.notesUrl+'" target="_blank" rel="noopener noreferrer">Конспект ↗</a>':'')+
      (item.theoryUrl?'<a href="'+item.theoryUrl+'" target="_blank" rel="noopener noreferrer">Теорія ↗</a>':'')+
      (item.instructionPdf?'<a href="'+item.instructionPdf+'" target="_blank" rel="noopener noreferrer">PDF-інструкція ↗</a>':'')+
      '<a href="'+source+'" target="_blank" rel="noopener">Python package</a>'+
      '</div>';
    root.appendChild(card);
  });
}

function setMode(mode) {
  const normalized=mode==="instructor"?"instructor":"student";
  document.body.dataset.mode=normalized;
  localStorage.setItem("mmi-mode",normalized);
  qsa("[data-mode-button]").forEach(btn=>btn.classList.toggle("active",btn.dataset.modeButton===normalized));
}

let resourceState={};
function renderResource() {
  const s0=+$("resource-s0").value;
  const rateA=+$("resource-rate-a").value;
  const rateB=+$("resource-rate-b").value;
  const horizon=+$("resource-horizon").value;
  const clamp=$("resource-clamp").checked;
  $("resource-s0-out").textContent=s0;
  $("resource-rate-a-out").textContent=rateA;
  $("resource-rate-b-out").textContent=rateB;
  $("resource-horizon-out").textContent=horizon;

  const sa=[], sb=[], points=60;
  for(let i=0;i<=points;i++){
    const t=horizon*i/points;
    sa.push({t,v:E.resourceValue(t,s0,rateA,clamp)});
    sb.push({t,v:E.resourceValue(t,s0,rateB,clamp)});
  }
  const all=sa.concat(sb).map(d=>d.v);
  $("resource-chart").innerHTML=lineSvg([sa,sb],horizon,Math.min(0,...all),Math.max(s0,...all,1));

  const ta=E.depletionTime(s0,rateA), tb=E.depletionTime(s0,rateB);
  $("resource-ta").textContent=fmt(ta);
  $("resource-tb").textContent=fmt(tb);
  $("resource-delta").textContent=Number.isFinite(ta)&&Number.isFinite(tb)?fmt(tb-ta):"—";

  const invalid=!clamp&&(E.resourceValue(horizon,s0,rateA,false)<0||E.resourceValue(horizon,s0,rateB,false)<0);
  const insight=$("resource-insight");
  if(invalid){
    insight.className="insight warning";
    insight.textContent="Математичний вираз продовжує працювати, але фізична інтерпретація зламана: запас став від’ємним.";
  } else if(rateA===rateB){
    insight.className="insight";
    insight.textContent="Сценарії збігаються. Без зміни параметра немає дослідницького контрасту.";
  } else {
    insight.className="insight";
    insight.textContent=rateB<rateA
      ?"Менша стала витрата збільшує час до вичерпання. Це висновок саме цієї структури моделі."
      :"Більша стала витрата скорочує час до вичерпання. Перевірте обґрунтованість припущення про сталу інтенсивність.";
  }

  resourceState={
    s0,rate_baseline:rateA,rate_scenario:rateB,horizon,clamp_zero:clamp,
    depletion_baseline:ta,depletion_scenario:tb,
    reflection:reflectionFor("resource")
  };
}

let networkState={};
function renderNetwork() {
  const task=$("delay-task").value, delay=+$("delay-value").value;
  $("delay-out").textContent="+"+delay;
  const result=E.cpm(E.applyDelay(E.BASE_TASKS,task,delay));
  $("project-duration").textContent=fmt(result.duration);
  $("critical-path").textContent=result.path.join(" → ");
  $("network-svg").innerHTML=networkSvg(result);

  const gantt=$("gantt");
  gantt.innerHTML="";
  result.rows.forEach(row=>{
    const el=document.createElement("div");
    el.className="gantt-row";
    const left=(row.ES/result.duration)*100, width=(row.duration/result.duration)*100;
    el.innerHTML='<strong>'+row.task+'</strong><div class="gantt-track"><div class="gantt-bar '+(row.critical?"critical":"")+'" style="left:'+left+'%;width:'+width+'%"></div></div><span>sl '+fmt(row.slack)+'</span>';
    gantt.appendChild(el);
  });

  const baseline=E.cpm(E.BASE_TASKS).duration;
  const affected=result.duration>baseline+1e-9;
  $("network-insight").textContent=delay===0
    ?"Baseline: 17 одиниць, критичний шлях A → C → E → G."
    :affected
      ?"Затримка вийшла за доступний резерв і збільшила строк проєкту на "+fmt(result.duration-baseline)+"."
      :"Затримка поглинута резервом: локальна зміна не змінила загальний строк.";

  networkState={
    delayed_task:task,delay,project_duration:result.duration,
    critical_path:result.path,schedule:result.rows,
    reflection:reflectionFor("network")
  };
}

let mcdaState={};
function renderMcda() {
  const rel=+$("reliability-weight").value;
  $("reliability-out").textContent=rel.toFixed(2);
  const weights=E.focusedWeights(rel);
  const wsm=E.rank(E.wsm(weights)), topsis=E.rank(E.topsis(weights));

  $("weights-view").innerHTML=Object.entries(weights)
    .map(([k,v])=>'<div class="weight-row"><span>'+k+'</span><strong>'+v.toFixed(3)+'</strong></div>').join("");
  $("wsm-ranking").innerHTML=wsm.map(x=>'<li>'+x[0]+' · '+x[1].toFixed(3)+'</li>').join("");
  $("topsis-ranking").innerHTML=topsis.map(x=>'<li>'+x[0]+' · '+x[1].toFixed(3)+'</li>').join("");

  const bars=$("mcda-bars");
  bars.innerHTML="";
  wsm.forEach(([name,score])=>{
    const row=document.createElement("div");
    row.className="bar-row";
    row.innerHTML='<strong>WSM '+name+'</strong><div class="bar-track"><div class="bar-fill" style="width:'+(score*100)+'%"></div></div><span>'+score.toFixed(3)+'</span>';
    bars.appendChild(row);
  });

  const wsmWinners=new Set(), topsisWinners=new Set();
  for(let x=.10;x<=.4501;x+=.01){
    const w=E.focusedWeights(x);
    wsmWinners.add(E.rank(E.wsm(w))[0][0]);
    topsisWinners.add(E.rank(E.topsis(w))[0][0]);
  }
  const disagree=wsm[0][0]!==topsis[0][0];
  $("mcda-insight").textContent=(disagree?"Методи не погоджуються щодо лідера. ":"Методи мають спільного лідера. ")+
    "У діапазоні reliability 0.10–0.45 WSM дає лідерів "+Array.from(wsmWinners).join(", ")+
    ", TOPSIS — "+Array.from(topsisWinners).join(", ")+". Висновок має бути умовним.";

  mcdaState={
    reliability_weight:rel,weights,wsm,topsis,
    wsm_winners_in_range:Array.from(wsmWinners),
    topsis_winners_in_range:Array.from(topsisWinners),
    reflection:reflectionFor("mcda")
  };
}

function reflectionFor(prefix) {
  const out={};
  qsa('[id^="'+prefix+'-"][data-reflection]').forEach(el=>{
    out[el.id.replace(prefix+"-","")]=el.value;
  });
  return out;
}

function setupReflections() {
  qsa("[data-reflection]").forEach(el=>{
    const key="mmi-reflection-"+el.id;
    el.value=localStorage.getItem(key)||"";
    el.addEventListener("input",()=>{
      localStorage.setItem(key,el.value);
      if(el.id.startsWith("resource-")) renderResource();
      if(el.id.startsWith("network-")) renderNetwork();
      if(el.id.startsWith("mcda-")) renderMcda();
    });
  });
}

function setupProgress() {
  qsa("[data-progress]").forEach(box=>{
    const key="mmi-progress-"+box.dataset.progress;
    box.checked=localStorage.getItem(key)==="1";
    box.addEventListener("change",()=>localStorage.setItem(key,box.checked?"1":"0"));
  });
}

const passportIds=[
  "p-question","p-variables","p-assumptions","p-data","p-method",
  "p-verification","p-uncertainty","p-limits","p-conclusion"
];
function passportData() {
  return Object.fromEntries(passportIds.map(id=>[id.replace("p-",""),$(id).value]));
}
function loadPassport() {
  try {
    const data=JSON.parse(localStorage.getItem("mmi-passport")||"{}");
    passportIds.forEach(id=>{
      const key=id.replace("p-","");
      if(data[key]) $(id).value=data[key];
    });
  } catch (_) {}
}
function courseProgress() {
  return {
    mode:document.body.dataset.mode,
    completed:Object.fromEntries(qsa("[data-progress]").map(box=>[box.dataset.progress,box.checked])),
    reflections:{
      resource:reflectionFor("resource"),
      network:reflectionFor("network"),
      mcda:reflectionFor("mcda")
    },
    passport:passportData()
  };
}

qsa("[data-mode-button]").forEach(btn=>btn.addEventListener("click",()=>setMode(btn.dataset.modeButton)));

["resource-s0","resource-rate-a","resource-rate-b","resource-horizon","resource-clamp"]
  .forEach(id=>$(id).addEventListener("input",renderResource));
["delay-task","delay-value"].forEach(id=>$(id).addEventListener("input",renderNetwork));
$("reliability-weight").addEventListener("input",renderMcda);

qsa("[data-export]").forEach(btn=>btn.addEventListener("click",()=>{
  const kind=btn.dataset.export;
  const data=kind==="resource"?resourceState:kind==="network"?networkState:mcdaState;
  downloadJson("mathmodelingit-"+kind+".json",{lab:kind,exported_at:new Date().toISOString(),result:data});
}));

$("passport-save").addEventListener("click",()=>{
  localStorage.setItem("mmi-passport",JSON.stringify(passportData()));
  $("passport-status").textContent="Збережено у цьому браузері.";
});
$("passport-export").addEventListener("click",()=>downloadJson(
  "mathmodelingit-model-passport.json",
  {exported_at:new Date().toISOString(),passport:passportData()}
));
$("progress-export").addEventListener("click",()=>downloadJson(
  "mathmodelingit-course-progress.json",
  {exported_at:new Date().toISOString(),progress:courseProgress()}
));

renderCatalog();
setMode(localStorage.getItem("mmi-mode")||"student");
setupReflections();
setupProgress();
loadPassport();
renderResource();
renderNetwork();
renderMcda();
