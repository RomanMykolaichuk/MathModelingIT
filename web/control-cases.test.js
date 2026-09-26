"use strict";
const fs = require("fs");
const path = require("path");
const E = require("./lab-engine.js");
const C = JSON.parse(fs.readFileSync(path.join(__dirname,"control-cases.json"),"utf8"));

function near(a,b,tol=1e-8) {
  if (Math.abs(a-b)>tol) throw new Error("expected "+b+", got "+a);
}
function same(a,b,label) {
  if (JSON.stringify(a)!==JSON.stringify(b)) throw new Error(label+": expected "+JSON.stringify(b)+", got "+JSON.stringify(a));
}

for (const key of ["baseline","scenario"]) {
  const c=C.resource[key];
  near(E.resourceValue(c.time,c.s0,c.rate,c.clamp_zero),c.expected_value);
  near(E.depletionTime(c.s0,c.rate),c.expected_depletion_time);
}

let r=E.cpm(E.BASE_TASKS);
near(r.duration,C.network.baseline.expected_duration);
same(r.path,C.network.baseline.expected_path,"baseline critical path");

for (const key of ["delay_c3","delay_d3"]) {
  const c=C.network[key];
  r=E.cpm(E.applyDelay(E.BASE_TASKS,c.task,c.delay));
  near(r.duration,c.expected_duration);
  if (c.expected_path) same(r.path,c.expected_path,key+" critical path");
}

for (const key of ["baseline","low_reliability"]) {
  const c=C.mcda[key], w=E.focusedWeights(c.reliability_weight);
  const wr=E.rank(E.wsm(w)), tr=E.rank(E.topsis(w));
  if (c.expected_wsm_ranking) same(wr.map(x=>x[0]),c.expected_wsm_ranking,"WSM ranking");
  if (c.expected_topsis_ranking) same(tr.map(x=>x[0]),c.expected_topsis_ranking,"TOPSIS ranking");
  if (c.expected_wsm_top && wr[0][0]!==c.expected_wsm_top) throw new Error("WSM top mismatch");
  if (c.expected_topsis_top && tr[0][0]!==c.expected_topsis_top) throw new Error("TOPSIS top mismatch");
  if (c.expected_wsm_c) near(Object.fromEntries(wr).C,c.expected_wsm_c,1e-9);
  if (c.expected_topsis_c) near(Object.fromEntries(tr).C,c.expected_topsis_c,1e-9);
}

console.log("Web control cases: PASS");
