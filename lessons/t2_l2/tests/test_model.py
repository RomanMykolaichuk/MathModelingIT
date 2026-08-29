from pathlib import Path
import sys

import numpy as np
import pandas as pd
import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from model import check_solution, solve_transport_scipy, total_cost, validate_problem


def problem():
    costs = pd.DataFrame(
        [[4, 6, 8, 7], [5, 4, 3, 6], [9, 7, 4, 5]],
        index=["S1", "S2", "S3"],
        columns=["D1", "D2", "D3", "D4"],
        dtype=float,
    )
    supply = pd.Series([35, 50, 40], index=costs.index, dtype=float)
    demand = pd.Series([30, 25, 35, 35], index=costs.columns, dtype=float)
    return costs, supply, demand


def test_balanced_problem_is_valid():
    validate_problem(*problem())


def test_unbalanced_problem_is_rejected():
    costs, supply, demand = problem()
    demand = demand.copy()
    demand.loc["D4"] += 1
    with pytest.raises(ValueError):
        validate_problem(costs, supply, demand)


def test_baseline_optimum():
    costs, supply, demand = problem()
    result = solve_transport_scipy(costs, supply, demand)
    assert result.status == "Optimal"
    assert result.total_cost == pytest.approx(515.0)
    assert check_solution(result.plan, supply, demand)["feasible"]


def test_baseline_plan_expected_structure():
    costs, supply, demand = problem()
    result = solve_transport_scipy(costs, supply, demand)
    expected = np.array([[30, 5, 0, 0], [0, 20, 30, 0], [0, 0, 5, 35]], dtype=float)
    assert np.allclose(result.plan.to_numpy(), expected)


def test_forbidden_route_increases_cost():
    costs, supply, demand = problem()
    baseline = solve_transport_scipy(costs, supply, demand)
    closed = solve_transport_scipy(costs, supply, demand, forbidden_routes=[("S2", "D3")])
    assert closed.total_cost == pytest.approx(570.0)
    assert closed.total_cost > baseline.total_cost
    assert closed.plan.loc["S2", "D3"] == pytest.approx(0.0)


def test_total_cost_matches_solver_value():
    costs, supply, demand = problem()
    result = solve_transport_scipy(costs, supply, demand)
    assert total_cost(result.plan, costs) == pytest.approx(result.total_cost)
