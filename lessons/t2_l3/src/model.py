"""T2.L3 — nonlinear programming models.

Two complementary models are used:
1) An applied resource-allocation problem with diminishing returns.
2) A deliberately non-convex toy landscape for local-optimum demonstrations.
"""
from __future__ import annotations

from typing import Iterable
import numpy as np
from scipy.optimize import minimize


def applied_utility(x: float, y: float) -> float:
    """Utility of allocating resources x and y.

    The first two terms model diminishing returns.
    The geometric-mean term models a weak synergy between directions.
    """
    x = float(x)
    y = float(y)
    if x < 0 or y < 0:
        return float("-inf")
    return float(
        40.0 * (1.0 - np.exp(-0.05 * x))
        + 35.0 * (1.0 - np.exp(-0.04 * y))
        + 0.15 * np.sqrt(x * y)
    )


def solve_applied(total_resource: float = 100.0, start=(50.0, 50.0)) -> dict:
    """Maximize applied_utility subject to x+y <= total_resource and x,y >= 0."""
    total_resource = float(total_resource)
    if total_resource <= 0:
        raise ValueError("total_resource must be positive")
    start = np.asarray(start, dtype=float)
    if start.shape != (2,):
        raise ValueError("start must contain two values")
    if np.any(start < 0):
        raise ValueError("start must be non-negative")
    if start.sum() > total_resource:
        start = start * (total_resource / start.sum())

    constraints = [{"type": "ineq", "fun": lambda v: total_resource - v[0] - v[1]}]
    result = minimize(
        lambda v: -applied_utility(v[0], v[1]),
        start,
        method="SLSQP",
        bounds=[(0.0, total_resource), (0.0, total_resource)],
        constraints=constraints,
        options={"ftol": 1e-12, "maxiter": 1000},
    )
    x, y = result.x
    return {
        "success": bool(result.success),
        "message": str(result.message),
        "x": float(x),
        "y": float(y),
        "total_used": float(x + y),
        "resource_slack": float(total_resource - x - y),
        "objective": float(-result.fun),
        "iterations": int(result.nit),
    }


def verify_applied_solution(solution: dict, total_resource: float, tol: float = 1e-6) -> dict:
    """Independent feasibility checks for the applied problem."""
    x = float(solution["x"])
    y = float(solution["y"])
    checks = {
        "x_nonnegative": x >= -tol,
        "y_nonnegative": y >= -tol,
        "resource_constraint": x + y <= float(total_resource) + tol,
        "objective_finite": np.isfinite(float(solution["objective"])),
    }
    checks["all_passed"] = all(checks.values())
    return checks


def applied_sensitivity(resource_levels: Iterable[float], start=(50.0, 50.0)):
    """Solve the applied model for several resource limits."""
    rows = []
    for total in resource_levels:
        sol = solve_applied(float(total), start=start)
        rows.append({
            "total_resource": float(total),
            "x": sol["x"],
            "y": sol["y"],
            "objective": sol["objective"],
            "resource_slack": sol["resource_slack"],
        })
    return rows


def nonconvex_landscape(x: float, y: float) -> float:
    """A bounded, deliberately non-convex surface with several local maxima."""
    x = float(x)
    y = float(y)
    return float(np.sin(1.7 * x) * np.cos(1.3 * y) + 0.15 * x - 0.03 * (x * x + y * y))


def solve_nonconvex(start=(0.0, 0.0), bounds=((-4.0, 4.0), (-4.0, 4.0))) -> dict:
    """Local optimization of the non-convex landscape from one start point."""
    start = np.asarray(start, dtype=float)
    result = minimize(
        lambda v: -nonconvex_landscape(v[0], v[1]),
        start,
        method="L-BFGS-B",
        bounds=bounds,
    )
    x, y = result.x
    return {
        "success": bool(result.success),
        "x": float(x),
        "y": float(y),
        "objective": float(-result.fun),
        "iterations": int(result.nit),
    }


def multistart_nonconvex(starts) -> list[dict]:
    """Run the local solver from many start points and sort by objective."""
    rows = []
    for sx, sy in starts:
        sol = solve_nonconvex((sx, sy))
        rows.append({"start_x": float(sx), "start_y": float(sy), **sol})
    return sorted(rows, key=lambda r: r["objective"], reverse=True)


def grid_search_nonconvex(step: float = 0.05) -> dict:
    """Independent coarse grid search for global-optimum sanity checking."""
    if step <= 0:
        raise ValueError("step must be positive")
    xs = np.arange(-4.0, 4.0 + step / 2.0, step)
    ys = np.arange(-4.0, 4.0 + step / 2.0, step)
    best_value = float("-inf")
    best_x = best_y = None
    for x in xs:
        values = np.sin(1.7 * x) * np.cos(1.3 * ys) + 0.15 * x - 0.03 * (x * x + ys * ys)
        idx = int(np.argmax(values))
        if values[idx] > best_value:
            best_value = float(values[idx])
            best_x = float(x)
            best_y = float(ys[idx])
    return {"x": best_x, "y": best_y, "objective": best_value, "step": float(step)}
