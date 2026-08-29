from pathlib import Path
import sys

HERE = Path(__file__).resolve()
SRC = HERE.parents[1] / "src"
sys.path.insert(0, str(SRC))

from model import (
    applied_utility,
    solve_applied,
    verify_applied_solution,
    applied_sensitivity,
    solve_nonconvex,
    multistart_nonconvex,
    grid_search_nonconvex,
)


def test_applied_utility_increases_initially():
    assert applied_utility(20, 20) > applied_utility(10, 10)


def test_baseline_solution_expected_region():
    sol = solve_applied(100, (50, 50))
    assert sol["success"]
    assert abs(sol["x"] - 48.6593) < 0.05
    assert abs(sol["y"] - 51.3407) < 0.05
    assert abs(sol["objective"] - 74.49685) < 1e-3


def test_baseline_uses_resource():
    sol = solve_applied(100, (50, 50))
    assert abs(sol["total_used"] - 100.0) < 1e-5


def test_verification_passes():
    sol = solve_applied(100, (50, 50))
    checks = verify_applied_solution(sol, 100)
    assert checks["all_passed"]


def test_sensitivity_objective_non_decreasing():
    rows = applied_sensitivity([60, 80, 100, 120])
    values = [r["objective"] for r in rows]
    assert values == sorted(values)


def test_nonconvex_start_points_can_reach_different_local_optima():
    a = solve_nonconvex((0, 0))
    b = solve_nonconvex((2, 2))
    assert abs(a["objective"] - b["objective"]) > 0.05


def test_multistart_best_matches_known_region():
    rows = multistart_nonconvex([(-3,-3), (-3,2), (0,0), (2,2), (3,-2), (4,4)])
    best = rows[0]
    assert best["objective"] > 1.11
    assert abs(best["x"] - 0.956) < 0.03
    assert abs(best["y"]) < 0.03


def test_grid_search_agrees_with_multistart_best():
    rows = multistart_nonconvex([(-3,-3), (-3,2), (0,0), (2,2), (3,-2), (4,4)])
    grid = grid_search_nonconvex(step=0.05)
    assert abs(rows[0]["objective"] - grid["objective"]) < 0.01


def test_grid_step_validation():
    try:
        grid_search_nonconvex(0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
