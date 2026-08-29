"""Core model for T1.L3: reproducible computational modeling workflow."""

from __future__ import annotations
import numpy as np


def deterministic_response(
    resource: float | np.ndarray,
    load: float | np.ndarray,
    *,
    baseline: float = 20.0,
    resource_gain: float = 1.8,
    load_penalty: float = 1.2,
) -> np.ndarray:
    """Compute deterministic system response and clip it at zero."""
    resource_arr = np.asarray(resource, dtype=float)
    load_arr = np.asarray(load, dtype=float)
    if np.any(resource_arr < 0) or np.any(load_arr < 0):
        raise ValueError("resource and load must be non-negative")
    value = baseline + resource_gain * resource_arr - load_penalty * load_arr
    return np.maximum(value, 0.0)


def simulate_observation(
    resource: float,
    load: float,
    *,
    rng: np.random.Generator,
    noise_sd: float = 4.0,
    baseline: float = 20.0,
    resource_gain: float = 1.8,
    load_penalty: float = 1.2,
) -> float:
    """Generate one stochastic observation around the deterministic response."""
    if noise_sd < 0:
        raise ValueError("noise_sd must be non-negative")
    mu = float(
        deterministic_response(
            resource,
            load,
            baseline=baseline,
            resource_gain=resource_gain,
            load_penalty=load_penalty,
        )
    )
    return max(0.0, float(rng.normal(mu, noise_sd)))
