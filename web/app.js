"use strict";

const $ = (id) => document.getElementById(id);
const qsa = (sel) => Array.from(document.querySelectorAll(sel));
const fmt = (x, digits=2) => Number.isFinite(x) ? Number(x).toFixed(digits).replace(/\.00$/, "") : "∞";

function downloadJson(filename, data) {
  const blob = new Blob([JSON.stringify(data, null, 2)], {type: "application/json"});
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function lineSvg(series, horizon, yMin, yMax) {
  const w = 760, h = 310, p = 42;
  const X = (t) => p + (t / horizon) * (w - 2*p);
  const Y = (v) => h - p - ((v - yMin) / (yMax - yMin || 1)) * (h - 2*p);
  const path = (pts) => pts.map((d,i) => (i ? "L" : "M") + X(d.t).toFixed(1) + " " + Y(d.v).toFixed(1)).join(" ");
  const zeroY = Y(0);
  return '<svg viewBox="0 0 '+w+' '+h+'" role="img">'+
    '<line class="axis" x1="'+p+'" y1="'+(h-p)+'" x2="'+(w-p)+'" y2="'+(h-p)+'"></line>'+
    '<line class="axis" x1="'+p+'" y1="'+p+'" x2="'+p+'" y2="'+(h-p)+'"></line>'+
    (yMin < 0 && yMax > 0 ? '<line class="zero-line" x1="'+p+'" y1="'+zeroY+'" x2="'+(w-p)+'" y2="'+zeroY+'"></line>' : '')+
    '<path class="line-a" d="'+path(series[0])+'"></path>'+
    '<path class="line-b" d="'+path(series[1])+'"></path>'+
    '<text class="axis-label" x="'+(w-p-20)+'" y="'+(h-12)+'">t</text>'+
    '<text class="axis-label" x="8" y="'+(p+5)+'">S(t)</text>'+
    '<text class="legend" x="'+(p+10)+'" y="24">v₁</text>'+
    '<text class="legend" x="'+(p+55)+'" y="24">v₂</text>'+
    '</svg>';
}

let resourceState = {};
function renderResource() {
  const s0 = +$("resource-s0").value;
  const a = +$("resource-rate-a").value;
  const b = +$("resource-rate-b").value;
  const horizon = +$("resource-horizon").value;
  const clamp = $("resource-clamp").checked;
  $("resource-s0-out").textContent = s0;
  $("resource-rate-a-out").textContent = a;
  $("resource-rate-b-out").textContent = b;
  $("resource-horizon-out").textContent = horizon;

  const value = (t, rate) => {
    const v = s0 - rate*t;
    return clamp ? Math.max(0, v) : v;
  };
  const points = 60;
  const sa = [], sb = [];
  for (let i=0;i<=points;i++) {
    const t = horizon*i/points;
    sa.push({t:t, v:value(t,a)});
    sb.push({t:t, v:value(t,b)});
  }
  const all = sa.concat(sb).map(d => d.v);
  const yMin = Math.min(0, ...all);
  const yMax = Math.max(s0, ...all, 1);
  $("resource-chart").innerHTML = lineSvg([sa,sb], horizon, yMin, yMax);

  const ta = a === 0 ? Infinity : s0/a;
  const tb = b === 0 ? Infinity : s0/b;
  $("resource-ta").textContent = fmt(ta);
  $("resource-tb").textContent = fmt(tb);
  $("resource-delta").textContent = Number.isFinite(ta) && Number.isFinite(tb) ? fmt(tb-ta) : "—";

  const invalid = !clamp && (s0-a*horizon < 0 || s0-b*horizon < 0);
  const insight = $("resource-insight");
  if (invalid) {
    insight.className = "insight warning";
    insight.textContent = "Ви зламали фізичну інтерпретацію: лінійна формула продовжує давати від’ємний запас. Потрібне обмеження або інша модель.";
  } else if (a === b) {
    insight.className = "insight";
    insight.textContent = "Сценарії збігаються: без зміни параметра модель не створює нового дослідницького контрасту.";
  } else {
    insight.className = "insight";
    insight.textContent = b < a ? "Менша стала витрата збільшує час до вичерпання. Це наслідок структури S(t)=S₀-vt, а не універсальний закон для реальних систем." : "Більша стала витрата скорочує час до вичерпання. Перевірте, чи припущення про сталу інтенсивність справді обґрунтоване.";
  }
  resourceState = {s0:s0, rate_baseline:a, rate_scenario:b, horizon:horizon, clamp_zero:clamp, depletion_baseline:ta, depletion_scenario:tb, prediction:$("resource-prediction").value};
}

const baseTasks = [
  {task:"A",duration:4,preds:[]},
  {task:"B",duration:3,preds:[]},
  {task:"C",duration:5,preds:["A"]},
  {task:"D",duration:4,preds:["A"]},
  {task:"E",duration:6,preds:["B","C"]},
  {task:"F",duration:3,preds:["D"]},
  {task:"G",duration:2,preds:["E","F"]}
];

function cpm(tasks) {
  const by = Object.fromEntries(tasks.map(t => [t.task, t]));
  const order = tasks.map(t => t.task);
  const es={}, ef={}, best={}, bestPath={};
  order.forEach(n => {
    const preds = by[n].preds;
    es[n] = preds.length ? Math.max(...preds.map(p => ef[p])) : 0;
    ef[n] = es[n] + by[n].duration;
    if (!preds.length) { best[n]=by[n].duration; bestPath[n]=[n]; }
    else {
      let p = preds[0];
      preds.forEach(x => { if (best[x] > best[p]) p=x; });
      best[n] = best[p] + by[n].duration;
      bestPath[n] = bestPath[p].concat([n]);
    }
  });
  const project = Math.max(...Object.values(ef));
  const succ={};
  order.forEach(n => succ[n]=[]);
  order.forEach(n => by[n].preds.forEach(p => succ[p].push(n)));
  const ls={}, lf={};
  order.slice().reverse().forEach(n => {
    lf[n] = succ[n].length ? Math.min(...succ[n].map(s => ls[s])) : project;
    ls[n] = lf[n] - by[n].duration;
  });
  const sinks = order.filter(n => !succ[n].length);
  let sink = sinks[0];
  sinks.forEach(n => { if (best[n] > best[sink]) sink=n; });
  return {
    duration: project,
    path: bestPath[sink],
    rows: order.map(n => ({task:n,duration:by[n].duration,ES:es[n],EF:ef[n],LS:ls[n],LF:lf[n],slack:ls[n]-es[n],critical:Math.abs(ls[n]-es[n])<1e-9}))
  };
}

function networkSvg(result) {
  const pos={A:[90,75],B:[90,225],C:[270,55],D:[270,165],E:[470,90],F:[470,210],G:[665,145]};
  const edges=[];
  baseTasks.forEach(t => t.preds.forEach(p => edges.push([p,t.task])));
  const criticalEdges = new Set(result.path.slice(1).map((n,i) => result.path[i]+"-"+n));
  let out='<svg viewBox="0 0 760 290" role="img"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#49657e"></path></marker></defs>';
  edges.forEach(e => {
    const a=pos[e[0]], b=pos[e[1]], cls=criticalEdges.has(e[0]+"-"+e[1]) ? "network-edge critical" : "network-edge";
    out += '<line class="'+cls+'" x1="'+(a[0]+24)+'" y1="'+a[1]+'" x2="'+(b[0]-24)+'" y2="'+b[1]+'"></line>';
  });
  result.rows.forEach(r => {
    const p=pos[r.task], cls=r.critical ? "network-node critical" : "network-node";
    out += '<circle class="'+cls+'" cx="'+p[0]+'" cy="'+p[1]+'" r="24"></circle><text class="network-label" x="'+p[0]+'" y="'+p[1]+'">'+r.task+'</text>';
  });
  return out+"</svg>";
}

let networkState = {};
function renderNetwork() {
  const task=$("delay-task").value, delay=+$("delay-value").value;
  $("delay-out").textContent = "+"+delay;
  const tasks=baseTasks.map(t => ({task:t.task,duration:t.duration+(t.task===task?delay:0),preds:t.preds.slice()}));
  const result=cpm(tasks);
  $("project-duration").textContent=fmt(result.duration);
  $("critical-path").textContent=result.path.join(" → ");
  $("network-svg").innerHTML=networkSvg(result);

  const gantt=$("gantt");
  gantt.innerHTML="";
  result.rows.forEach(r => {
    const row=document.createElement("div"); row.className="gantt-row";
    const left=(r.ES/result.duration)*100, width=(r.duration/result.duration)*100;
    row.innerHTML='<strong>'+r.task+'</strong><div class="gantt-track"><div class="gantt-bar '+(r.critical?"critical":"")+'" style="left:'+left+'%;width:'+width+'%"></div></div><span>sl '+fmt(r.slack)+'</span>';
    gantt.appendChild(row);
  });

  const baseline=cpm(baseTasks).duration;
  const affected=result.duration>baseline+1e-9;
  $("network-insight").textContent = delay===0 ? "Baseline: 17 одиниць, критичний шлях A → C → E → G. Оберіть роботу та додайте затримку." :
    affected ? "Затримка вийшла за доступний резерв і збільшила строк проєкту на "+fmt(result.duration-baseline)+"." :
    "Затримка поглинута резервом: локальна зміна ще не змінила загальний строк проєкту.";
  networkState={delayed_task:task,delay:delay,project_duration:result.duration,critical_path:result.path,schedule:result.rows};
}

const alternatives = {
  A:{cost:82,time:18,reliability:.92,capacity:75,risk:.18},
  B:{cost:70,time:22,reliability:.88,capacity:90,risk:.25},
  C:{cost:92,time:15,reliability:.96,capacity:80,risk:.12},
  D:{cost:76,time:20,reliability:.90,capacity:85,risk:.20}
};
const types={cost:"cost",time:"cost",reliability:"benefit",capacity:"benefit",risk:"cost"};
const baseWeights={cost:.25,time:.20,reliability:.25,capacity:.20,risk:.10};

function focusedWeights(rel) {
  const out={reliability:rel};
  const scale=(1-rel)/(1-baseWeights.reliability);
  Object.keys(baseWeights).forEach(k => { if (k!=="reliability") out[k]=baseWeights[k]*scale; });
  return out;
}
function wsm(weights) {
  const keys=Object.keys(types), names=Object.keys(alternatives);
  const norm={};
  keys.forEach(k => {
    const vals=names.map(n => alternatives[n][k]), lo=Math.min(...vals), hi=Math.max(...vals);
    names.forEach(n => {
      if (!norm[n]) norm[n]={};
      norm[n][k]=hi===lo?1:(types[k]==="benefit"?(alternatives[n][k]-lo)/(hi-lo):(hi-alternatives[n][k])/(hi-lo));
    });
  });
  const scores={};
  names.forEach(n => scores[n]=keys.reduce((s,k)=>s+norm[n][k]*weights[k],0));
  return scores;
}
function topsis(weights) {
  const keys=Object.keys(types), names=Object.keys(alternatives), weighted={};
  keys.forEach(k => {
    const den=Math.sqrt(names.reduce((s,n)=>s+alternatives[n][k]*alternatives[n][k],0));
    names.forEach(n => {
      if (!weighted[n]) weighted[n]={};
      weighted[n][k]=alternatives[n][k]/den*weights[k];
    });
  });
  const best={}, worst={};
  keys.forEach(k => {
    const vals=names.map(n=>weighted[n][k]);
    best[k]=types[k]==="benefit"?Math.max(...vals):Math.min(...vals);
    worst[k]=types[k]==="benefit"?Math.min(...vals):Math.max(...vals);
  });
  const scores={};
  names.forEach(n => {
    const db=Math.sqrt(keys.reduce((s,k)=>s+Math.pow(weighted[n][k]-best[k],2),0));
    const dw=Math.sqrt(keys.reduce((s,k)=>s+Math.pow(weighted[n][k]-worst[k],2),0));
    scores[n]=(db+dw)===0?.5:dw/(db+dw);
  });
  return scores;
}
function rank(scores) { return Object.entries(scores).sort((a,b)=>b[1]-a[1]); }

let mcdaState={};
function renderMcda() {
  const rel=+$("reliability-weight").value;
  $("reliability-out").textContent=rel.toFixed(2);
  const weights=focusedWeights(rel), a=rank(wsm(weights)), b=rank(topsis(weights));
  $("weights-view").innerHTML=Object.entries(weights).map(x=>'<div class="weight-row"><span>'+x[0]+'</span><strong>'+x[1].toFixed(3)+'</strong></div>').join("");
  $("wsm-ranking").innerHTML=a.map(x=>'<li>'+x[0]+' · '+x[1].toFixed(3)+'</li>').join("");
  $("topsis-ranking").innerHTML=b.map(x=>'<li>'+x[0]+' · '+x[1].toFixed(3)+'</li>').join("");

  const bars=$("mcda-bars"); bars.innerHTML="";
  a.forEach(x => {
    const row=document.createElement("div"); row.className="bar-row";
    row.innerHTML='<strong>WSM '+x[0]+'</strong><div class="bar-track"><div class="bar-fill" style="width:'+(x[1]*100)+'%"></div></div><span>'+x[1].toFixed(3)+'</span>';
    bars.appendChild(row);
  });

  let wsmWinners=new Set(), topWinners=new Set();
  for (let x=.10;x<=.4501;x+=.01) {
    const ww=focusedWeights(x);
    wsmWinners.add(rank(wsm(ww))[0][0]);
    topWinners.add(rank(topsis(ww))[0][0]);
  }
  const disagree=a[0][0]!==b[0][0];
  $("mcda-insight").textContent=(disagree ? "Методи не погоджуються щодо лідера за поточних ваг. " : "Методи мають спільного лідера за поточних ваг. ")+
    "У діапазоні reliability 0.10–0.45 лідери WSM: "+Array.from(wsmWinners).join(", ")+"; TOPSIS: "+Array.from(topWinners).join(", ")+". Це і є перевірка стійкості, а не пошук «абсолютно найкращої» альтернативи.";
  mcdaState={reliability_weight:rel,weights:weights,wsm:a,topsis:b,wsm_winners_in_range:Array.from(wsmWinners),topsis_winners_in_range:Array.from(topWinners)};
}

["resource-s0","resource-rate-a","resource-rate-b","resource-horizon","resource-clamp","resource-prediction"].forEach(id => $(id).addEventListener("input",renderResource));
["delay-task","delay-value"].forEach(id => $(id).addEventListener("input",renderNetwork));
$("reliability-weight").addEventListener("input",renderMcda);

qsa("[data-export]").forEach(btn => btn.addEventListener("click",() => {
  const kind=btn.dataset.export;
  const data=kind==="resource"?resourceState:kind==="network"?networkState:mcdaState;
  downloadJson("mathmodelingit-"+kind+".json",{lab:kind,exported_at:new Date().toISOString(),result:data});
}));

qsa("[data-progress]").forEach(box => {
  const key="mmi-progress-"+box.dataset.progress;
  box.checked=localStorage.getItem(key)==="1";
  box.addEventListener("change",()=>localStorage.setItem(key,box.checked?"1":"0"));
});

const passportIds=["p-question","p-variables","p-assumptions","p-data","p-verification","p-limits"];
function passportData() { return Object.fromEntries(passportIds.map(id => [id.replace("p-",""),$(id).value])); }
function loadPassport() {
  try {
    const data=JSON.parse(localStorage.getItem("mmi-passport")||"{}");
    passportIds.forEach(id => { const k=id.replace("p-",""); if (data[k]) $(id).value=data[k]; });
  } catch (_) {}
}
$("passport-save").addEventListener("click",() => {
  localStorage.setItem("mmi-passport",JSON.stringify(passportData()));
  $("passport-status").textContent="Збережено у цьому браузері.";
});
$("passport-export").addEventListener("click",() => downloadJson("mathmodelingit-model-passport.json",{exported_at:new Date().toISOString(),passport:passportData()}));

loadPassport();
renderResource();
renderNetwork();
renderMcda();
