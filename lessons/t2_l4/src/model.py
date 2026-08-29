from __future__ import annotations
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
import networkx as nx


def parse_predecessors(value) -> List[str]:
    if pd.isna(value) or not str(value).strip():
        return []
    return [x.strip() for x in str(value).split(";") if x.strip()]


def build_graph(tasks: pd.DataFrame) -> nx.DiGraph:
    required = {"task", "duration", "predecessors"}
    missing = required - set(tasks.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if tasks["task"].duplicated().any():
        raise ValueError("Task identifiers must be unique")
    G = nx.DiGraph()
    for _, row in tasks.iterrows():
        duration = float(row["duration"])
        if duration < 0:
            raise ValueError("Task duration must be non-negative")
        G.add_node(str(row["task"]), duration=duration)
    for _, row in tasks.iterrows():
        task = str(row["task"])
        for pred in parse_predecessors(row["predecessors"]):
            if pred not in G:
                raise ValueError(f"Unknown predecessor: {pred}")
            G.add_edge(pred, task)
    if not nx.is_directed_acyclic_graph(G):
        raise ValueError("Project network must be a DAG")
    return G


def cpm_schedule(tasks: pd.DataFrame) -> Tuple[float, pd.DataFrame, List[str]]:
    G = build_graph(tasks)
    topo = list(nx.topological_sort(G))
    duration = {n: float(G.nodes[n]["duration"]) for n in topo}
    ES, EF = {}, {}
    for n in topo:
        predecessors = list(G.predecessors(n))
        ES[n] = max((EF[p] for p in predecessors), default=0.0)
        EF[n] = ES[n] + duration[n]
    project_duration = max(EF.values(), default=0.0)
    LS, LF = {}, {}
    for n in reversed(topo):
        successors = list(G.successors(n))
        LF[n] = min((LS[s] for s in successors), default=project_duration)
        LS[n] = LF[n] - duration[n]
    rows = []
    for n in topo:
        slack = LS[n] - ES[n]
        rows.append({
            "task": n, "duration": duration[n],
            "ES": ES[n], "EF": EF[n],
            "LS": LS[n], "LF": LF[n],
            "slack": slack,
            "critical": abs(slack) < 1e-9,
        })
    schedule = pd.DataFrame(rows)

    best_value, best_path = {}, {}
    for n in topo:
        preds = list(G.predecessors(n))
        if not preds:
            best_value[n] = duration[n]
            best_path[n] = [n]
        else:
            p = max(preds, key=lambda x: best_value[x])
            best_value[n] = best_value[p] + duration[n]
            best_path[n] = best_path[p] + [n]
    sinks = [n for n in topo if G.out_degree(n) == 0]
    sink = max(sinks, key=lambda x: best_value[x])
    return project_duration, schedule, best_path[sink]


def apply_delay(tasks: pd.DataFrame, task: str, delay: float) -> pd.DataFrame:
    if delay < 0:
        raise ValueError("Delay must be non-negative")
    if task not in set(tasks["task"]):
        raise ValueError(f"Unknown task: {task}")
    changed = tasks.copy()
    changed.loc[changed["task"] == task, "duration"] += float(delay)
    return changed


def pert_parameters(pert: pd.DataFrame) -> pd.DataFrame:
    required = {"task", "optimistic", "most_likely", "pessimistic"}
    missing = required - set(pert.columns)
    if missing:
        raise ValueError(f"Missing PERT columns: {sorted(missing)}")
    out = pert.copy()
    if not ((out["optimistic"] <= out["most_likely"]) &
            (out["most_likely"] <= out["pessimistic"]) &
            (out["optimistic"] >= 0)).all():
        raise ValueError("Require 0 <= optimistic <= most_likely <= pessimistic")
    out["pert_mean"] = (out["optimistic"] + 4*out["most_likely"] + out["pessimistic"]) / 6
    out["pert_variance"] = ((out["pessimistic"] - out["optimistic"]) / 6) ** 2
    return out


def beta_pert_sample(a: float, m: float, b: float, size: int, rng: np.random.Generator, lamb: float = 4.0) -> np.ndarray:
    if not (0 <= a <= m <= b):
        raise ValueError("Require 0 <= a <= m <= b")
    if size <= 0:
        raise ValueError("size must be positive")
    if b == a:
        return np.full(size, a, dtype=float)
    alpha = 1 + lamb * (m-a)/(b-a)
    beta = 1 + lamb * (b-m)/(b-a)
    return a + (b-a) * rng.beta(alpha, beta, size=size)


def monte_carlo_project(tasks: pd.DataFrame, pert: pd.DataFrame, n: int = 3000, seed: int = 2026) -> Tuple[pd.DataFrame, pd.DataFrame]:
    params = pert_parameters(pert)
    if set(params["task"]) != set(tasks["task"]):
        raise ValueError("PERT tasks must match project tasks")
    rng = np.random.default_rng(seed)
    samples: Dict[str, np.ndarray] = {}
    for _, r in params.iterrows():
        samples[str(r["task"])] = beta_pert_sample(
            float(r["optimistic"]), float(r["most_likely"]), float(r["pessimistic"]), n, rng
        )
    records = []
    for i in range(n):
        scenario = tasks.copy()
        scenario["duration"] = scenario["task"].map({t: samples[t][i] for t in samples})
        project_duration, _, critical_path = cpm_schedule(scenario)
        records.append({
            "simulation": i,
            "project_duration": project_duration,
            "critical_path": " -> ".join(critical_path),
        })
    results = pd.DataFrame(records)
    critical_freq = (
        results["critical_path"].value_counts(normalize=True)
        .rename_axis("critical_path").reset_index(name="frequency")
    )
    return results, critical_freq


def deadline_probability(simulation_results: pd.DataFrame, deadline: float) -> float:
    if deadline < 0:
        raise ValueError("deadline must be non-negative")
    return float((simulation_results["project_duration"] <= deadline).mean())
