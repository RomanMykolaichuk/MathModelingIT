import math

from lessons.t1_l4.src.methods import (
    critical_path,
    linear_optimization,
    monte_carlo_risk,
    numerical_root,
    symbolic_roots,
    weighted_sum_decision,
)


def test_numerical_root_is_positive():
    root = numerical_root()
    assert root > 0


def test_numerical_root_satisfies_equation():
    root = numerical_root()
    value = 120 - 6 * root - 0.2 * root**2
    assert abs(value) < 1e-8


def test_symbolic_contains_positive_root_close_to_numerical():
    roots = [float(r.evalf()) for r in symbolic_roots()]
    positive = [r for r in roots if r > 0]
    assert len(positive) == 1
    assert math.isclose(positive[0], numerical_root(), rel_tol=1e-9)


def test_linear_optimization_is_feasible():
    result = linear_optimization()
    x1, x2 = result["x"]
    assert x1 >= 0 and x2 >= 0
    assert x1 + x2 <= 100 + 1e-9
    assert 3 * x1 + 2 * x2 <= 240 + 1e-9


def test_monte_carlo_is_reproducible():
    p1 = monte_carlo_risk(n_runs=2000, seed=2026)
    p2 = monte_carlo_risk(n_runs=2000, seed=2026)
    assert p1 == p2
    assert 0 <= p1 <= 1


def test_critical_path():
    path, length = critical_path()
    assert path == ["Start", "A", "C", "Finish"]
    assert length == 12.0


def test_weighted_sum_returns_ranking():
    df = weighted_sum_decision()
    assert list(df.columns).count("score") == 1
    assert len(df) == 3
    assert df.iloc[0]["score"] >= df.iloc[-1]["score"]
