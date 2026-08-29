from pathlib import Path
import sys

import numpy as np
import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from model import (
    ResourceModelParams,
    deterministic_stock,
    deterministic_exhaustion_time,
    discrete_stock_path,
    exhaustion_step,
    monte_carlo_exhaustion_times,
    stochastic_consumption,
    stochastic_stock_path,
    summarize_exhaustion,
)


def test_deterministic_stock_known_values():
    t = np.array([0, 5, 20, 25])
    result = deterministic_stock(t, 120, 6)
    assert np.allclose(result, [120, 90, 0, 0])


def test_deterministic_exhaustion_time():
    assert deterministic_exhaustion_time(120, 6) == pytest.approx(20.0)
    assert deterministic_exhaustion_time(120, 0) == float("inf")


def test_discrete_stock_path():
    stock = discrete_stock_path(20, [5, 7, 10])
    assert np.allclose(stock, [20, 15, 8, 0])


def test_stochastic_consumption_reproducible():
    a = stochastic_consumption(8, 6, 1.5, seed=123)
    b = stochastic_consumption(8, 6, 1.5, seed=123)
    assert np.allclose(a, b)
    assert np.all(a >= 0)


def test_stochastic_stock_path_shapes():
    params = ResourceModelParams(initial_stock=50, mean_consumption=5, std_consumption=1, horizon=10)
    stock, consumption = stochastic_stock_path(params, seed=1)
    assert len(stock) == 11
    assert len(consumption) == 10
    assert np.all(stock >= 0)


def test_exhaustion_step():
    assert exhaustion_step([10, 5, 0, 0]) == 2
    assert exhaustion_step([10, 5, 1]) is None


def test_monte_carlo_reproducible_and_valid():
    params = ResourceModelParams(initial_stock=120, mean_consumption=6, std_consumption=1.5, horizon=30)
    a = monte_carlo_exhaustion_times(params, n_runs=200, seed=2026)
    b = monte_carlo_exhaustion_times(params, n_runs=200, seed=2026)
    assert np.allclose(a, b, equal_nan=True)
    finite = a[np.isfinite(a)]
    assert np.all((finite >= 1) & (finite <= 30))


def test_summary_probability_range():
    summary = summarize_exhaustion([20, 21, np.nan, 19])
    assert summary["probability_exhausted"] == pytest.approx(0.75)
    assert summary["median_exhaustion_step"] == pytest.approx(20.0)
