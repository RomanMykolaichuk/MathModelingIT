"""Transportation model for T2.L2.

Primary teaching backend: PuLP.
Independent verification backend: SciPy HiGHS.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class TransportResult:
    status: str
    total_cost: float
    plan: pd.DataFrame


def validate_problem(
    costs: pd.DataFrame,
    supply: pd.Series,
    demand: pd.Series,
    *,
    atol: float = 1e-9,
) -> None:
    """Validate dimensions, labels, non-negativity and balance."""
    if costs.empty:
        raise ValueError("Cost matrix must not be empty.")
    if list(costs.index) != list(supply.index):
        raise ValueError("Cost-matrix rows must match supply labels and order.")
    if list(costs.columns) != list(demand.index):
        raise ValueError("Cost-matrix columns must match demand labels and order.")
    if (costs.to_numpy(dtype=float) < 0).any():
        raise ValueError("Transportation costs must be non-negative.")
    if (supply.to_numpy(dtype=float) < 0).any() or (demand.to_numpy(dtype=float) < 0).any():
        raise ValueError("Supply and demand must be non-negative.")
    if not np.isclose(float(supply.sum()), float(demand.sum()), atol=atol):
        raise ValueError(
            f"Problem is unbalanced: total supply={float(supply.sum())}, "
            f"total demand={float(demand.sum())}."
        )


def total_cost(plan: pd.DataFrame, costs: pd.DataFrame) -> float:
    """Return sum_ij x_ij * c_ij."""
    return float((plan * costs).to_numpy(dtype=float).sum())


def check_solution(
    plan: pd.DataFrame,
    supply: pd.Series,
    demand: pd.Series,
    *,
    atol: float = 1e-7,
) -> dict:
    """Independently verify non-negativity and row/column balances."""
    plan = plan.astype(float)
    supply_residual = plan.sum(axis=1) - supply
    demand_residual = plan.sum(axis=0) - demand
    nonnegative = bool((plan.to_numpy() >= -atol).all())
    supply_ok = bool((supply_residual.abs() <= atol).all())
    demand_ok = bool((demand_residual.abs() <= atol).all())
    return {
        "feasible": nonnegative and supply_ok and demand_ok,
        "nonnegative": nonnegative,
        "supply_ok": supply_ok,
        "demand_ok": demand_ok,
        "max_supply_residual": float(supply_residual.abs().max()),
        "max_demand_residual": float(demand_residual.abs().max()),
    }


def solve_transport_pulp(
    costs: pd.DataFrame,
    supply: pd.Series,
    demand: pd.Series,
    *,
    forbidden_routes: Iterable[tuple[str, str]] | None = None,
) -> TransportResult:
    """Solve the balanced transportation problem with PuLP/CBC."""
    validate_problem(costs, supply, demand)

    try:
        import pulp
    except ImportError as exc:
        raise RuntimeError(
            "PuLP is required for solve_transport_pulp(). Install dependencies "
            "with: pip install -r requirements.txt"
        ) from exc

    forbidden = set(forbidden_routes or [])
    suppliers = list(costs.index)
    consumers = list(costs.columns)

    problem = pulp.LpProblem("transportation_problem", pulp.LpMinimize)
    x = {
        (i, j): pulp.LpVariable(f"x_{i}_{j}", lowBound=0)
        for i in suppliers
        for j in consumers
    }

    problem += pulp.lpSum(float(costs.loc[i, j]) * x[i, j] for i in suppliers for j in consumers)

    for i in suppliers:
        problem += pulp.lpSum(x[i, j] for j in consumers) == float(supply.loc[i]), f"supply_{i}"

    for j in consumers:
        problem += pulp.lpSum(x[i, j] for i in suppliers) == float(demand.loc[j]), f"demand_{j}"

    for i, j in forbidden:
        if i not in suppliers or j not in consumers:
            raise ValueError(f"Unknown forbidden route: {(i, j)}")
        problem += x[i, j] == 0, f"forbidden_{i}_{j}"

    problem.solve(pulp.PULP_CBC_CMD(msg=False))
    status = pulp.LpStatus[problem.status]
    if status != "Optimal":
        raise RuntimeError(f"Solver did not find an optimal solution: {status}")

    plan = pd.DataFrame(
        [[float(pulp.value(x[i, j])) for j in consumers] for i in suppliers],
        index=suppliers,
        columns=consumers,
    )
    return TransportResult(status=status, total_cost=total_cost(plan, costs), plan=plan)


def solve_transport_scipy(
    costs: pd.DataFrame,
    supply: pd.Series,
    demand: pd.Series,
    *,
    forbidden_routes: Iterable[tuple[str, str]] | None = None,
) -> TransportResult:
    """Solve the same LP independently with scipy.optimize.linprog."""
    validate_problem(costs, supply, demand)
    from scipy.optimize import linprog

    suppliers = list(costs.index)
    consumers = list(costs.columns)
    m, n = costs.shape
    c = costs.to_numpy(dtype=float).ravel()

    A_eq = []
    b_eq = []
    for i in range(m):
        row = np.zeros(m * n)
        row[i * n : (i + 1) * n] = 1.0
        A_eq.append(row)
        b_eq.append(float(supply.iloc[i]))

    for j in range(n):
        row = np.zeros(m * n)
        row[j::n] = 1.0
        A_eq.append(row)
        b_eq.append(float(demand.iloc[j]))

    forbidden = set(forbidden_routes or [])
    bounds = []
    for i in suppliers:
        for j in consumers:
            if (i, j) in forbidden:
                bounds.append((0.0, 0.0))
            else:
                bounds.append((0.0, None))

    result = linprog(
        c,
        A_eq=np.asarray(A_eq),
        b_eq=np.asarray(b_eq),
        bounds=bounds,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"SciPy solver failed: {result.message}")

    plan = pd.DataFrame(
        result.x.reshape(m, n),
        index=suppliers,
        columns=consumers,
    )
    return TransportResult(
        status="Optimal",
        total_cost=float(result.fun),
        plan=plan,
    )


def long_plan(plan: pd.DataFrame, costs: pd.DataFrame) -> pd.DataFrame:
    """Convert matrix plan to a tidy route table."""
    rows = []
    for supplier in plan.index:
        for consumer in plan.columns:
            quantity = float(plan.loc[supplier, consumer])
            if quantity > 1e-9:
                unit_cost = float(costs.loc[supplier, consumer])
                rows.append(
                    {
                        "supplier": supplier,
                        "consumer": consumer,
                        "quantity": quantity,
                        "unit_cost": unit_cost,
                        "route_cost": quantity * unit_cost,
                    }
                )
    return pd.DataFrame(rows)
