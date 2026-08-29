from __future__ import annotations

import numpy as np
import pandas as pd
import networkx as nx
from scipy.optimize import linprog, root_scalar
import sympy as sp


def numerical_root() -> float:
    f = lambda t: 120 - 6 * t - 0.2 * t**2
    result = root_scalar(f, bracket=[0, 30], method="brentq")
    return float(result.root)


def symbolic_roots():
    t = sp.symbols("t", real=True)
    return sp.solve(sp.Eq(120 - 6 * t - sp.Rational(1, 5) * t**2, 0), t)


def linear_optimization():
    # scipy.linprog minimizes, therefore maximize 8*x1+6*x2 by minimizing its negative.
    c = np.array([-8.0, -6.0])
    A_ub = np.array([[1.0, 1.0], [3.0, 2.0]])
    b_ub = np.array([100.0, 240.0])
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None), (0, None)], method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    return {
        "x": result.x,
        "objective": float(-result.fun),
        "resource_used": float(result.x.sum()),
        "budget_used": float(3 * result.x[0] + 2 * result.x[1]),
    }


def monte_carlo_risk(n_runs: int = 10000, seed: int = 2026, steps: int = 20,
                     mean: float = 6.0, std: float = 1.5, capacity: float = 120.0) -> float:
    rng = np.random.default_rng(seed)
    consumption = rng.normal(mean, std, size=(n_runs, steps))
    consumption = np.clip(consumption, 0.0, None)
    totals = consumption.sum(axis=1)
    return float(np.mean(totals > capacity))


def critical_path():
    g = nx.DiGraph()
    edges = [
        ("Start", "A", 3),
        ("Start", "B", 4),
        ("A", "C", 5),
        ("B", "C", 2),
        ("C", "Finish", 4),
    ]
    for u, v, duration in edges:
        g.add_edge(u, v, weight=duration)
    path = nx.algorithms.dag.dag_longest_path(g, weight="weight")
    length = nx.algorithms.dag.dag_longest_path_length(g, weight="weight")
    return path, float(length)


def weighted_sum_decision() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "alternative": ["A", "B", "C"],
            "cost": [80.0, 65.0, 95.0],
            "time": [7.0, 9.0, 5.0],
            "reliability": [0.90, 0.82, 0.96],
        }
    )
    weights = {"cost": 0.30, "time": 0.25, "reliability": 0.45}

    # Cost and time are cost criteria; reliability is a benefit criterion.
    df["cost_score"] = df["cost"].min() / df["cost"]
    df["time_score"] = df["time"].min() / df["time"]
    df["reliability_score"] = df["reliability"] / df["reliability"].max()
    df["score"] = (
        weights["cost"] * df["cost_score"]
        + weights["time"] * df["time_score"]
        + weights["reliability"] * df["reliability_score"]
    )
    return df.sort_values("score", ascending=False).reset_index(drop=True)
