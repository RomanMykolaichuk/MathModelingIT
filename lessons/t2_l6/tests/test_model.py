from pathlib import Path
import sys

import numpy as np
import pytest
import sympy as sp

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from model import (
    analytical_solution,
    cumulative_state,
    equilibrium,
    lambdified_solution,
    max_symbolic_numeric_error,
    symbolic_model,
    threshold_time,
)


def test_symbolic_residual_is_zero():
    assert symbolic_model()["residual"] == 0


def test_symbolic_equilibrium():
    model = symbolic_model()
    q = model["symbols"]["q"]
    k = model["symbols"]["k"]
    assert sp.simplify(model["equilibrium"] - q / k) == 0


def test_baseline_equilibrium():
    assert equilibrium(12.0, 0.1) == pytest.approx(120.0)


def test_baseline_state_t10():
    value = analytical_solution(10.0, 12.0, 0.1, 20.0)
    assert value == pytest.approx(83.2120558829, rel=1e-9)


def test_lambdify_matches_direct_evaluation():
    times = np.linspace(0, 10, 11)
    fn = lambdified_solution()
    direct = analytical_solution(times, 12.0, 0.1, 20.0)
    generated = fn(times, 12.0, 0.1, 20.0)
    assert np.allclose(direct, generated)


def test_symbolic_and_numerical_solutions_agree():
    times = np.linspace(0, 30, 121)
    assert max_symbolic_numeric_error(times, 12.0, 0.1, 20.0) < 1e-6


def test_cumulative_state_baseline():
    assert cumulative_state(10.0, 12.0, 0.1, 20.0) == pytest.approx(
        567.8794411714, rel=1e-9
    )


def test_threshold_time_baseline():
    assert threshold_time(80.0, 12.0, 0.1, 20.0) == pytest.approx(
        9.1629073187, rel=1e-9
    )


def test_invalid_parameters():
    with pytest.raises(ValueError):
        equilibrium(1.0, 0.0)
    with pytest.raises(ValueError):
        analytical_solution(-1.0, 12.0, 0.1, 20.0)
    with pytest.raises(ValueError):
        threshold_time(150.0, 12.0, 0.1, 20.0)
