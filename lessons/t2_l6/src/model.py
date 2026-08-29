"""Symbolic and numerical models for T2.L6.

Baseline dynamic model:
    dS/dt = q - k*S,  k > 0

where
    S(t) - state variable,
    q    - constant inflow,
    k    - proportional loss coefficient.
"""

from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


def symbolic_model():
    """Build the symbolic model and derive its main analytical results."""
    t = sp.symbols("t", nonnegative=True, real=True)
    q = sp.symbols("q", positive=True, real=True)
    k = sp.symbols("k", positive=True, real=True)
    s0 = sp.symbols("S0", nonnegative=True, real=True)
    S = sp.Function("S")

    ode = sp.Eq(sp.diff(S(t), t), q - k * S(t))
    equilibrium = sp.solve(sp.Eq(q - k * sp.Symbol("S_eq"), 0), sp.Symbol("S_eq"))[0]
    solution = sp.simplify(equilibrium + (s0 - equilibrium) * sp.exp(-k * t))
    residual = sp.simplify(sp.diff(solution, t) - (q - k * solution))
    cumulative = sp.simplify(sp.integrate(solution, (t, 0, t)))
    sensitivity_q = sp.simplify(sp.diff(equilibrium, q))
    sensitivity_k = sp.simplify(sp.diff(equilibrium, k))

    return {
        "symbols": {"t": t, "q": q, "k": k, "S0": s0},
        "ode": ode,
        "equilibrium": equilibrium,
        "solution": solution,
        "residual": residual,
        "cumulative": cumulative,
        "sensitivity_q": sensitivity_q,
        "sensitivity_k": sensitivity_k,
    }


def equilibrium(q: float, k: float) -> float:
    """Return S* = q/k."""
    if q < 0:
        raise ValueError("q must be non-negative")
    if k <= 0:
        raise ValueError("k must be positive")
    return float(q / k)


def analytical_solution(t, q: float, k: float, s0: float):
    """Evaluate the closed-form solution using NumPy."""
    if q < 0:
        raise ValueError("q must be non-negative")
    if k <= 0:
        raise ValueError("k must be positive")
    if s0 < 0:
        raise ValueError("s0 must be non-negative")
    arr = np.asarray(t, dtype=float)
    if np.any(arr < 0):
        raise ValueError("time must be non-negative")
    seq = q / k
    values = seq + (s0 - seq) * np.exp(-k * arr)
    if np.ndim(t) == 0:
        return float(values)
    return values


def lambdified_solution():
    """Return a NumPy-ready function generated from the SymPy expression."""
    symbolic = symbolic_model()
    s = symbolic["symbols"]
    return sp.lambdify(
        (s["t"], s["q"], s["k"], s["S0"]),
        symbolic["solution"],
        modules="numpy",
    )


def numerical_solution(times, q: float, k: float, s0: float):
    """Solve the ODE numerically with SciPy solve_ivp."""
    if q < 0:
        raise ValueError("q must be non-negative")
    if k <= 0:
        raise ValueError("k must be positive")
    if s0 < 0:
        raise ValueError("s0 must be non-negative")

    t_eval = np.asarray(times, dtype=float)
    if t_eval.ndim != 1 or t_eval.size < 2:
        raise ValueError("times must be a 1-D array with at least two points")
    if np.any(t_eval < 0) or np.any(np.diff(t_eval) <= 0):
        raise ValueError("times must be strictly increasing and non-negative")

    def rhs(_t, y):
        return [q - k * y[0]]

    result = solve_ivp(
        rhs,
        (float(t_eval[0]), float(t_eval[-1])),
        [float(s0)],
        t_eval=t_eval,
        rtol=1e-10,
        atol=1e-12,
    )
    if not result.success:
        raise RuntimeError(result.message)
    return result.y[0]


def cumulative_state(horizon: float, q: float, k: float, s0: float) -> float:
    """Evaluate integral_0^T S(t) dt from the analytical expression."""
    if horizon < 0:
        raise ValueError("horizon must be non-negative")
    if q < 0 or s0 < 0 or k <= 0:
        raise ValueError("invalid model parameters")
    seq = q / k
    return float(seq * horizon + (s0 - seq) * (1 - np.exp(-k * horizon)) / k)


def threshold_time(target: float, q: float, k: float, s0: float) -> float:
    """Return first t >= 0 when the monotone trajectory reaches target."""
    if target < 0:
        raise ValueError("target must be non-negative")
    seq = equilibrium(q, k)
    lo, hi = sorted((s0, seq))
    if target < lo - 1e-12 or target > hi + 1e-12:
        raise ValueError("target must lie between initial state and equilibrium")
    if np.isclose(target, s0):
        return 0.0
    if np.isclose(target, seq):
        return float("inf")
    ratio = (target - seq) / (s0 - seq)
    return float(-np.log(ratio) / k)


def max_symbolic_numeric_error(times, q: float, k: float, s0: float) -> float:
    """Compare analytical and solve_ivp trajectories."""
    a = analytical_solution(times, q=q, k=k, s0=s0)
    n = numerical_solution(times, q=q, k=k, s0=s0)
    return float(np.max(np.abs(a - n)))
