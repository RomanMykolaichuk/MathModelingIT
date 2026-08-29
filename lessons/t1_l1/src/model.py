"""Core mathematical model for T1.L1.

The lesson uses a simple resource-depletion model to demonstrate how the same
real-world situation is represented verbally, mathematically, algorithmically,
and programmatically.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ResourceModelParams:
    """Parameters of the linear resource model."""

    s0: float
    rate: float
    clamp_zero: bool = True

    def validate(self) -> None:
        if self.s0 < 0:
            raise ValueError("s0 must be non-negative.")
        if self.rate < 0:
            raise ValueError("rate must be non-negative.")


def resource(
    t: float | Iterable[float] | np.ndarray,
    s0: float,
    rate: float,
    clamp_zero: bool = True,
) -> np.ndarray:
    """Return remaining resource S(t) = S0 - rate*t.

    If clamp_zero=True, negative values are replaced by zero to respect the
    physical constraint that a resource reserve cannot be negative.
    """
    params = ResourceModelParams(s0=s0, rate=rate, clamp_zero=clamp_zero)
    params.validate()

    t_arr = np.asarray(t, dtype=float)
    if np.any(t_arr < 0):
        raise ValueError("Time values must be non-negative.")

    values = s0 - rate * t_arr
    if clamp_zero:
        values = np.maximum(values, 0.0)
    return values


def depletion_time(s0: float, rate: float) -> float:
    """Return theoretical time until depletion; infinity when rate == 0."""
    params = ResourceModelParams(s0=s0, rate=rate)
    params.validate()
    if rate == 0:
        return math.inf
    return s0 / rate


def simulate(
    times: Iterable[float] | np.ndarray,
    s0: float,
    rate: float,
    clamp_zero: bool = True,
) -> pd.DataFrame:
    """Run the model for a sequence of time values and return a tidy table."""
    t_arr = np.asarray(list(times), dtype=float)
    values = resource(t_arr, s0=s0, rate=rate, clamp_zero=clamp_zero)
    return pd.DataFrame(
        {
            "time": t_arr,
            "resource": values,
            "s0": float(s0),
            "rate": float(rate),
            "clamp_zero": bool(clamp_zero),
        }
    )


def compare_rates(
    times: Iterable[float] | np.ndarray,
    s0: float,
    rates: Iterable[float],
    clamp_zero: bool = True,
) -> pd.DataFrame:
    """Run the same model for several consumption rates."""
    frames = []
    for rate in rates:
        df = simulate(times, s0=s0, rate=float(rate), clamp_zero=clamp_zero)
        df["scenario_rate"] = float(rate)
        frames.append(df)

    if not frames:
        return pd.DataFrame(
            columns=["time", "resource", "s0", "rate", "clamp_zero", "scenario_rate"]
        )
    return pd.concat(frames, ignore_index=True)
