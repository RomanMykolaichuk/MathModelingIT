"use strict";

(function (root, factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.MathModelingLab = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  const BASE_TASKS = [
    {task:"A",duration:4,preds:[]},
    {task:"B",duration:3,preds:[]},
    {task:"C",duration:5,preds:["A"]},
    {task:"D",duration:4,preds:["A"]},
    {task:"E",duration:6,preds:["B","C"]},
    {task:"F",duration:3,preds:["D"]},
    {task:"G",duration:2,preds:["E","F"]}
  ];

  const ALTERNATIVES = {
    A:{cost:82,time:18,reliability:.92,capacity:75,risk:.18},
    B:{cost:70,time:22,reliability:.88,capacity:90,risk:.25},
    C:{cost:92,time:15,reliability:.96,capacity:80,risk:.12},
    D:{cost:76,time:20,reliability:.90,capacity:85,risk:.20}
  };
  const TYPES={cost:"cost",time:"cost",reliability:"benefit",capacity:"benefit",risk:"cost"};
  const BASE_WEIGHTS={cost:.25,time:.20,reliability:.25,capacity:.20,risk:.10};

  function resourceValue(t, s0, rate, clampZero=true) {
    if (t < 0 || s0 < 0 || rate < 0) throw new Error("resource inputs must be non-negative");
    const value = s0 - rate*t;
    return clampZero ? Math.max(0,value) : value;
  }

  function depletionTime(s0, rate) {
    if (s0 < 0 || rate < 0) throw new Error("resource inputs must be non-negative");
    return rate === 0 ? Infinity : s0/rate;
  }

  function applyDelay(tasks, task, delay) {
    if (delay < 0) throw new Error("delay must be non-negative");
    if (!tasks.some(t=>t.task===task)) throw new Error("unknown task");
    return tasks.map(t=>({task:t.task,duration:t.duration+(t.task===task?delay:0),preds:t.preds.slice()}));
  }

  function cpm(tasks) {
    const by = Object.fromEntries(tasks.map(t => [t.task, t]));
    const order = tasks.map(t => t.task);
    if (new Set(order).size !== order.length) throw new Error("task identifiers must be unique");
    order.forEach(n=>{
      if (by[n].duration < 0) throw new Error("task duration must be non-negative");
      by[n].preds.forEach(p=>{ if (!by[p]) throw new Error("unknown predecessor"); });
    });

    const es={}, ef={}, best={}, bestPath={}, visiting=new Set(), visited=new Set(), topo=[];
    function visit(n){
      if (visiting.has(n)) throw new Error("project network must be a DAG");
      if (visited.has(n)) return;
      visiting.add(n);
      by[n].preds.forEach(visit);
      visiting.delete(n); visited.add(n); topo.push(n);
    }
    order.forEach(visit);

    topo.forEach(n => {
      const preds = by[n].preds;
      es[n] = preds.length ? Math.max(...preds.map(p => ef[p])) : 0;
      ef[n] = es[n] + by[n].duration;
      if (!preds.length) { best[n]=by[n].duration; bestPath[n]=[n]; }
      else {
        let p=preds[0];
        preds.forEach(x=>{ if (best[x]>best[p]) p=x; });
        best[n]=best[p]+by[n].duration;
        bestPath[n]=bestPath[p].concat([n]);
      }
    });

    const project=Math.max(...Object.values(ef),0);
    const succ=Object.fromEntries(order.map(n=>[n,[]]));
    order.forEach(n=>by[n].preds.forEach(p=>succ[p].push(n)));
    const ls={}, lf={};
    topo.slice().reverse().forEach(n=>{
      lf[n]=succ[n].length?Math.min(...succ[n].map(s=>ls[s])):project;
      ls[n]=lf[n]-by[n].duration;
    });
    const sinks=topo.filter(n=>!succ[n].length);
    let sink=sinks[0];
    sinks.forEach(n=>{ if (best[n]>best[sink]) sink=n; });

    return {
      duration:project,
      path:sink ? bestPath[sink] : [],
      rows:topo.map(n=>({
        task:n,duration:by[n].duration,ES:es[n],EF:ef[n],
        LS:ls[n],LF:lf[n],slack:ls[n]-es[n],
        critical:Math.abs(ls[n]-es[n])<1e-9
      }))
    };
  }

  function focusedWeights(reliabilityWeight) {
    if (reliabilityWeight < 0 || reliabilityWeight > 1) throw new Error("weight must be in [0,1]");
    const out={reliability:reliabilityWeight};
    const scale=(1-reliabilityWeight)/(1-BASE_WEIGHTS.reliability);
    Object.keys(BASE_WEIGHTS).forEach(k=>{
      if (k!=="reliability") out[k]=BASE_WEIGHTS[k]*scale;
    });
    return out;
  }

  function wsm(weights) {
    const keys=Object.keys(TYPES), names=Object.keys(ALTERNATIVES), norm={};
    keys.forEach(k=>{
      const vals=names.map(n=>ALTERNATIVES[n][k]), lo=Math.min(...vals), hi=Math.max(...vals);
      names.forEach(n=>{
        if (!norm[n]) norm[n]={};
        norm[n][k]=hi===lo?1:(TYPES[k]==="benefit"
          ?(ALTERNATIVES[n][k]-lo)/(hi-lo)
          :(hi-ALTERNATIVES[n][k])/(hi-lo));
      });
    });
    const scores={};
    names.forEach(n=>scores[n]=keys.reduce((s,k)=>s+norm[n][k]*weights[k],0));
    return scores;
  }

  function topsis(weights) {
    const keys=Object.keys(TYPES), names=Object.keys(ALTERNATIVES), weighted={};
    keys.forEach(k=>{
      const den=Math.sqrt(names.reduce((s,n)=>s+ALTERNATIVES[n][k]*ALTERNATIVES[n][k],0));
      names.forEach(n=>{
        if (!weighted[n]) weighted[n]={};
        weighted[n][k]=ALTERNATIVES[n][k]/den*weights[k];
      });
    });
    const best={}, worst={};
    keys.forEach(k=>{
      const vals=names.map(n=>weighted[n][k]);
      best[k]=TYPES[k]==="benefit"?Math.max(...vals):Math.min(...vals);
      worst[k]=TYPES[k]==="benefit"?Math.min(...vals):Math.max(...vals);
    });
    const scores={};
    names.forEach(n=>{
      const db=Math.sqrt(keys.reduce((s,k)=>s+Math.pow(weighted[n][k]-best[k],2),0));
      const dw=Math.sqrt(keys.reduce((s,k)=>s+Math.pow(weighted[n][k]-worst[k],2),0));
      scores[n]=(db+dw)===0?0.5:dw/(db+dw);
    });
    return scores;
  }

  function rank(scores) {
    return Object.entries(scores).sort((a,b)=>b[1]-a[1]);
  }

  return {
    BASE_TASKS, ALTERNATIVES, TYPES, BASE_WEIGHTS,
    resourceValue, depletionTime, applyDelay, cpm,
    focusedWeights, wsm, topsis, rank
  };
});
