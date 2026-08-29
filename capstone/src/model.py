from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.optimize import least_squares, minimize


@dataclass(frozen=True)
class DynamicParams:
    q: float
    k: float
    s0: float = 20.0

    def validate(self) -> None:
        if self.q <= 0:
            raise ValueError("q must be positive")
        if self.k <= 0:
            raise ValueError("k must be positive")
        if self.s0 < 0:
            raise ValueError("s0 must be non-negative")


@dataclass(frozen=True)
class InterventionConfig:
    q_gain: float = 0.35
    k_reduction: float = 0.30
    cost_u: float = 60.0
    cost_v: float = 80.0
    budget: float = 70.0
    horizon: float = 12.0

    def validate(self) -> None:
        if not 0 <= self.q_gain:
            raise ValueError("q_gain must be non-negative")
        if not 0 <= self.k_reduction < 1:
            raise ValueError("k_reduction must be in [0, 1)")
        if self.cost_u <= 0 or self.cost_v <= 0:
            raise ValueError("intervention costs must be positive")
        if self.budget < 0:
            raise ValueError("budget must be non-negative")
        if self.horizon <= 0:
            raise ValueError("horizon must be positive")


def state_trajectory(t: Iterable[float] | np.ndarray, params: DynamicParams) -> np.ndarray:
    params.validate()
    t = np.asarray(t, dtype=float)
    if np.any(t < 0):
        raise ValueError("time must be non-negative")
    equilibrium = params.q / params.k
    return equilibrium + (params.s0 - equilibrium) * np.exp(-params.k * t)


def fit_parameters(t: Iterable[float], y: Iterable[float], s0: float = 20.0) -> dict:
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    if t.ndim != 1 or y.ndim != 1 or len(t) != len(y) or len(t) < 3:
        raise ValueError("t and y must be 1D arrays of equal length >= 3")
    if np.any(t < 0) or np.any(~np.isfinite(y)):
        raise ValueError("invalid observations")

    def residuals(p: np.ndarray) -> np.ndarray:
        pred = state_trajectory(t, DynamicParams(float(p[0]), float(p[1]), s0))
        return pred - y

    result = least_squares(
        residuals,
        x0=np.array([10.0, 0.08]),
        bounds=(np.array([0.1, 0.001]), np.array([50.0, 1.0])),
    )
    q_hat, k_hat = map(float, result.x)
    residual = residuals(result.x)
    rmse = float(np.sqrt(np.mean(residual**2)))
    return {
        "params": DynamicParams(q_hat, k_hat, s0),
        "rmse": rmse,
        "residuals": residual,
        "success": bool(result.success),
        "message": result.message,
    }


def effective_params(
    params: DynamicParams,
    u: float,
    v: float,
    config: InterventionConfig,
) -> DynamicParams:
    params.validate()
    config.validate()
    if not (0 <= u <= 1 and 0 <= v <= 1):
        raise ValueError("u and v must be in [0, 1]")
    q_eff = params.q * (1.0 + config.q_gain * u)
    k_eff = params.k * (1.0 - config.k_reduction * v)
    return DynamicParams(q_eff, k_eff, params.s0)


def intervention_cost(u: float, v: float, config: InterventionConfig) -> float:
    return float(config.cost_u * u + config.cost_v * v)


def terminal_state(params: DynamicParams, u: float, v: float, config: InterventionConfig) -> float:
    eff = effective_params(params, u, v, config)
    return float(state_trajectory([config.horizon], eff)[0])


def optimize_intervention(params: DynamicParams, config: InterventionConfig) -> dict:
    params.validate()
    config.validate()

    def objective(z: np.ndarray) -> float:
        return -terminal_state(params, float(z[0]), float(z[1]), config)

    constraints = [{
        "type": "ineq",
        "fun": lambda z: config.budget - intervention_cost(float(z[0]), float(z[1]), config),
    }]
    result = minimize(
        objective,
        x0=np.array([0.4, 0.4]),
        bounds=[(0.0, 1.0), (0.0, 1.0)],
        constraints=constraints,
        method="SLSQP",
        options={"ftol": 1e-9, "maxiter": 500},
    )
    u, v = map(float, result.x)
    cost = intervention_cost(u, v, config)
    feasible = (
        -1e-7 <= u <= 1 + 1e-7
        and -1e-7 <= v <= 1 + 1e-7
        and cost <= config.budget + 1e-6
    )
    return {
        "u": u,
        "v": v,
        "cost": cost,
        "terminal_state": -float(result.fun),
        "success": bool(result.success),
        "feasible": bool(feasible),
        "message": result.message,
    }


def grid_verify(
    params: DynamicParams,
    config: InterventionConfig,
    resolution: int = 151,
) -> dict:
    if resolution < 11:
        raise ValueError("resolution must be >= 11")
    best = {"u": 0.0, "v": 0.0, "cost": 0.0, "terminal_state": terminal_state(params, 0, 0, config)}
    grid = np.linspace(0.0, 1.0, resolution)
    for u in grid:
        for v in grid:
            cost = intervention_cost(float(u), float(v), config)
            if cost <= config.budget + 1e-12:
                value = terminal_state(params, float(u), float(v), config)
                if value > best["terminal_state"]:
                    best = {"u": float(u), "v": float(v), "cost": float(cost), "terminal_state": float(value)}
    return best


def budget_sensitivity(
    params: DynamicParams,
    config: InterventionConfig,
    budgets: Iterable[float],
) -> pd.DataFrame:
    rows = []
    for budget in budgets:
        cfg = InterventionConfig(
            q_gain=config.q_gain,
            k_reduction=config.k_reduction,
            cost_u=config.cost_u,
            cost_v=config.cost_v,
            budget=float(budget),
            horizon=config.horizon,
        )
        result = optimize_intervention(params, cfg)
        rows.append({"budget": float(budget), **{k: result[k] for k in ["u", "v", "cost", "terminal_state", "feasible"]}})
    return pd.DataFrame(rows)


def bootstrap_optimized_outcomes(
    t: Iterable[float],
    y: Iterable[float],
    config: InterventionConfig,
    n_boot: int = 200,
    seed: int = 2026,
    s0: float = 20.0,
) -> pd.DataFrame:
    if n_boot < 20:
        raise ValueError("n_boot must be >= 20")
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    base_fit = fit_parameters(t, y, s0=s0)
    params = base_fit["params"]
    fitted = state_trajectory(t, params)
    residuals = y - fitted
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n_boot):
        sampled_residuals = rng.choice(residuals, size=len(residuals), replace=True)
        y_boot = fitted + sampled_residuals
        fit = fit_parameters(t, y_boot, s0=s0)
        opt = optimize_intervention(fit["params"], config)
        rows.append({
            "replicate": i,
            "q_hat": fit["params"].q,
            "k_hat": fit["params"].k,
            "rmse": fit["rmse"],
            "u": opt["u"],
            "v": opt["v"],
            "terminal_state": opt["terminal_state"],
        })
    return pd.DataFrame(rows)
