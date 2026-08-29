import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from model import AllocationProblem, baseline_problem, check_feasibility, objective_value, solve_allocation


def test_baseline_solution_is_reproducible():
    problem = baseline_problem()
    result = solve_allocation(problem)
    assert result.success
    np.testing.assert_allclose(result.allocation, [40.0, 17.5, 17.5, 25.0], atol=1e-7)
    assert result.objective == pytest.approx(707.5)
    assert result.resource_used == pytest.approx(100.0)
    assert result.budget_used == pytest.approx(250.0)


def test_baseline_solution_is_feasible():
    problem = baseline_problem()
    result = solve_allocation(problem)
    assert check_feasibility(problem, result.allocation)["all"]


def test_manual_candidate_has_lower_objective():
    problem = baseline_problem()
    candidate = [25.0, 25.0, 25.0, 25.0]
    assert check_feasibility(problem, candidate)["all"]
    assert objective_value(problem, candidate) < solve_allocation(problem).objective


def test_infeasible_budget_is_reported():
    p = baseline_problem()
    impossible = AllocationProblem(
        names=p.names,
        effectiveness=p.effectiveness,
        unit_cost=p.unit_cost,
        minimum=p.minimum,
        maximum=p.maximum,
        total_resource=p.total_resource,
        total_budget=60.0,
    )
    result = solve_allocation(impossible)
    assert not result.success


def test_wrong_vector_length_fails():
    with pytest.raises(ValueError):
        check_feasibility(baseline_problem(), [1.0, 2.0])


def test_invalid_bounds_fail():
    with pytest.raises(ValueError):
        AllocationProblem(
            names=("A",),
            effectiveness=np.array([1.0]),
            unit_cost=np.array([1.0]),
            minimum=np.array([2.0]),
            maximum=np.array([1.0]),
            total_resource=10.0,
            total_budget=10.0,
        )
