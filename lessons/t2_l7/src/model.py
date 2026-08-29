"""Research-grade computational modeling utilities for T2.L7.

The lesson uses a simple first-order dynamic resource model

    dS/dt = q - k S

with analytical solution

    S(t) = q/k + (S0 - q/k) exp(-k t)

to demonstrate the full research workflow:
synthetic observations -> calibration -> verification -> scenario experiment
-> uncertainty analysis -> research conclusion.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares


@dataclass(frozen=True)
class DynamicParams:
    s0: float
    q: float
    k: float

    def validate(self) -> None:
        if self.s0 < 0:
            raise ValueError("s0 must be non-negative")
        if self.q <= 0:
            raise ValueError("q must be positive")
        if self.k <= 0:
            raise ValueError("k must be positive")


def analytical_trajectory(
    times: Iterable[float] | np.ndarray,
    *,
    s0: float,
    q: float,
    k: float,
) -> np.ndarray:
    params = DynamicParams(s0=s0, q=q, k=k)
    params.validate()
    t = np.asarray(times, dtype=float)
    if np.any(t < 0):
        raise ValueError("times must be non-negative")
    equilibrium = q / k
    return equilibrium + (s0 - equilibrium) * np.exp(-k * t)


def numerical_trajectory(
    times: Iterable[float] | np.ndarray,
    *,
    s0: float,
    q: float,
    k: float,
) -> np.ndarray:
    params = DynamicParams(s0=s0, q=q, k=k)
    params.validate()
    t = np.asarray(times, dtype=float)
    if t.ndim != 1 or len(t) == 0:
        raise ValueError("times must be a non-empty one-dimensional sequence")
    if np.any(t < 0) or np.any(np.diff(t) < 0):
        raise ValueError("times must be sorted and non-negative")

    def rhs(_t: float, y: np.ndarray) -> list[float]:
        return [q - k * y[0]]

    sol = solve_ivp(
        rhs,
        (float(t[0]), float(t[-1])),
        [s0],
        t_eval=t,
        rtol=1e-10,
        atol=1e-12,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[0]


def calibrate_parameters(
    times: Iterable[float] | np.ndarray,
    observations: Iterable[float] | np.ndarray,
    *,
    s0: float,
    initial_q: float = 10.0,
    initial_k: float = 0.08,
) -> dict[str, float]:
    t = np.asarray(times, dtype=float)
    y = np.asarray(observations, dtype=float)
    if t.shape != y.shape or t.ndim != 1 or len(t) < 3:
        raise ValueError("times and observations must be one-dimensional and have equal length >= 3")
    if np.any(t < 0):
        raise ValueError("times must be non-negative")
    if s0 < 0 or initial_q <= 0 or initial_k <= 0:
        raise ValueError("invalid initial parameters")

    def residuals(theta: np.ndarray) -> np.ndarray:
        q, k = theta
        return analytical_trajectory(t, s0=s0, q=q, k=k) - y

    result = least_squares(
        residuals,
        x0=np.array([initial_q, initial_k], dtype=float),
        bounds=([1e-8, 1e-8], [1e3, 10.0]),
    )
    if not result.success:
        raise RuntimeError(result.message)

    q_hat, k_hat = (float(result.x[0]), float(result.x[1]))
    fitted = analytical_trajectory(t, s0=s0, q=q_hat, k=k_hat)
    residual = y - fitted
    rmse = float(np.sqrt(np.mean(residual**2)))
    return {
        "q": q_hat,
        "k": k_hat,
        "equilibrium": float(q_hat / k_hat),
        "rmse": rmse,
        "cost": float(result.cost),
    }


def time_to_threshold(*, s0: float, q: float, k: float, threshold: float) -> float:
    params = DynamicParams(s0=s0, q=q, k=k)
    params.validate()
    equilibrium = q / k
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    if math.isclose(threshold, s0, rel_tol=0.0, abs_tol=1e-12):
        return 0.0
    lo, hi = sorted((s0, equilibrium))
    if threshold < lo or threshold > hi or math.isclose(s0, equilibrium):
        return math.inf
    ratio = (threshold - equilibrium) / (s0 - equilibrium)
    if ratio <= 0:
        return math.inf
    return float(-math.log(ratio) / k)


def scenario_batch(
    q_values: Iterable[float],
    *,
    s0: float,
    k: float,
    horizon: float,
    threshold: float,
) -> pd.DataFrame:
    rows: list[dict[str, float]] = []
    for q in q_values:
        q = float(q)
        DynamicParams(s0=s0, q=q, k=k).validate()
        s_horizon = float(analytical_trajectory([horizon], s0=s0, q=q, k=k)[0])
        rows.append(
            {
                "q": q,
                "k": float(k),
                "equilibrium": float(q / k),
                "s_horizon": s_horizon,
                "time_to_threshold": time_to_threshold(
                    s0=s0, q=q, k=k, threshold=threshold
                ),
            }
        )
    return pd.DataFrame(rows)


def bootstrap_calibration(
    times: Iterable[float] | np.ndarray,
    observations: Iterable[float] | np.ndarray,
    *,
    s0: float,
    threshold: float,
    horizon: float,
    n_boot: int = 500,
    seed: int = 2026,
) -> pd.DataFrame:
    if n_boot <= 0:
        raise ValueError("n_boot must be positive")
    t = np.asarray(times, dtype=float)
    y = np.asarray(observations, dtype=float)
    fit = calibrate_parameters(t, y, s0=s0)
    fitted = analytical_trajectory(t, s0=s0, q=fit["q"], k=fit["k"])
    residuals = y - fitted
    rng = np.random.default_rng(seed)

    rows: list[dict[str, float]] = []
    for i in range(n_boot):
        sampled = rng.choice(residuals, size=len(residuals), replace=True)
        synthetic = fitted + sampled
        bfit = calibrate_parameters(
            t,
            synthetic,
            s0=s0,
            initial_q=fit["q"],
            initial_k=fit["k"],
        )
        q_hat = bfit["q"]
        k_hat = bfit["k"]
        rows.append(
            {
                "replication": i,
                "q": q_hat,
                "k": k_hat,
                "equilibrium": q_hat / k_hat,
                "time_to_threshold": time_to_threshold(
                    s0=s0, q=q_hat, k=k_hat, threshold=threshold
                ),
                "s_horizon": float(
                    analytical_trajectory([horizon], s0=s0, q=q_hat, k=k_hat)[0]
                ),
            }
        )
    return pd.DataFrame(rows)


def quantile_summary(df: pd.DataFrame, column: str) -> dict[str, float]:
    if column not in df.columns:
        raise ValueError(f"missing column: {column}")
    values = pd.to_numeric(df[column], errors="coerce").dropna().to_numpy(dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        raise ValueError("no finite values")
    q025, q50, q975 = np.quantile(values, [0.025, 0.5, 0.975])
    return {
        "mean": float(np.mean(values)),
        "median": float(q50),
        "p2_5": float(q025),
        "p97_5": float(q975),
    }


def experiment_hash(payload: dict) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]
