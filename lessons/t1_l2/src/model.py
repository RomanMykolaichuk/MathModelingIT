from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np


@dataclass(frozen=True)
class ResourceModelParams:
    initial_stock: float = 120.0
    mean_consumption: float = 6.0
    std_consumption: float = 1.5
    horizon: int = 24

    def validate(self) -> None:
        if self.initial_stock < 0:
            raise ValueError("initial_stock must be non-negative")
        if self.mean_consumption < 0:
            raise ValueError("mean_consumption must be non-negative")
        if self.std_consumption < 0:
            raise ValueError("std_consumption must be non-negative")
        if self.horizon < 0:
            raise ValueError("horizon must be non-negative")


def deterministic_stock(t: float | np.ndarray, initial_stock: float, rate: float, clip: bool = True):
    """Continuous deterministic model S(t) = S0 - v*t."""
    if initial_stock < 0 or rate < 0:
        raise ValueError("initial_stock and rate must be non-negative")
    result = initial_stock - rate * np.asarray(t, dtype=float)
    if clip:
        result = np.maximum(result, 0.0)
    if np.ndim(t) == 0:
        return float(result)
    return result


def deterministic_exhaustion_time(initial_stock: float, rate: float) -> float:
    if initial_stock < 0 or rate < 0:
        raise ValueError("initial_stock and rate must be non-negative")
    if rate == 0:
        return float("inf")
    return initial_stock / rate


def stochastic_consumption(
    n_steps: int,
    mean: float,
    std: float,
    seed: int | None = None,
) -> np.ndarray:
    if n_steps < 0:
        raise ValueError("n_steps must be non-negative")
    if mean < 0 or std < 0:
        raise ValueError("mean and std must be non-negative")
    rng = np.random.default_rng(seed)
    draws = rng.normal(loc=mean, scale=std, size=n_steps)
    return np.maximum(draws, 0.0)


def discrete_stock_path(
    initial_stock: float,
    consumptions: Sequence[float] | np.ndarray,
) -> np.ndarray:
    """Discrete dynamic model: S[k+1] = max(0, S[k] - C[k])."""
    if initial_stock < 0:
        raise ValueError("initial_stock must be non-negative")
    c = np.asarray(consumptions, dtype=float)
    if np.any(c < 0):
        raise ValueError("consumptions must be non-negative")

    stock = np.empty(len(c) + 1, dtype=float)
    stock[0] = initial_stock
    for k, value in enumerate(c):
        stock[k + 1] = max(0.0, stock[k] - float(value))
    return stock


def stochastic_stock_path(
    params: ResourceModelParams,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    params.validate()
    c = stochastic_consumption(
        n_steps=params.horizon,
        mean=params.mean_consumption,
        std=params.std_consumption,
        seed=seed,
    )
    s = discrete_stock_path(params.initial_stock, c)
    return s, c


def exhaustion_step(stock_path: Sequence[float] | np.ndarray) -> int | None:
    """Return first index k where stock reaches zero; None if not exhausted."""
    s = np.asarray(stock_path, dtype=float)
    idx = np.where(s <= 0)[0]
    return int(idx[0]) if len(idx) else None


def monte_carlo_exhaustion_times(
    params: ResourceModelParams,
    n_runs: int = 1000,
    seed: int = 42,
) -> np.ndarray:
    """Estimate distribution of exhaustion step. NaN = not exhausted within horizon."""
    params.validate()
    if n_runs <= 0:
        raise ValueError("n_runs must be positive")

    rng = np.random.default_rng(seed)
    times = np.full(n_runs, np.nan, dtype=float)

    for i in range(n_runs):
        run_seed = int(rng.integers(0, 2**32 - 1))
        stock, _ = stochastic_stock_path(params, seed=run_seed)
        step = exhaustion_step(stock)
        if step is not None:
            times[i] = float(step)
    return times


def summarize_exhaustion(times: Sequence[float] | np.ndarray) -> dict[str, float]:
    t = np.asarray(times, dtype=float)
    finite = t[np.isfinite(t)]
    probability = float(len(finite) / len(t)) if len(t) else float("nan")
    if len(finite) == 0:
        return {
            "probability_exhausted": probability,
            "mean_exhaustion_step": float("nan"),
            "median_exhaustion_step": float("nan"),
        }
    return {
        "probability_exhausted": probability,
        "mean_exhaustion_step": float(np.mean(finite)),
        "median_exhaustion_step": float(np.median(finite)),
    }
