"""Linear resource-allocation model for T2.L1.

The module keeps mathematical logic separate from presentation and I/O.
"""

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True)
class AllocationProblem:
    names: tuple[str, ...]
    effectiveness: np.ndarray
    unit_cost: np.ndarray
    minimum: np.ndarray
    maximum: np.ndarray
    total_resource: float
    total_budget: float

    def __post_init__(self) -> None:
        arrays = (
            self.effectiveness,
            self.unit_cost,
            self.minimum,
            self.maximum,
        )
        n = len(self.names)
        if n == 0:
            raise ValueError("At least one direction is required.")
        if any(np.asarray(a).shape != (n,) for a in arrays):
            raise ValueError("All parameter vectors must match names length.")
        if np.any(np.asarray(self.minimum) < 0):
            raise ValueError("Minimum allocation cannot be negative.")
        if np.any(np.asarray(self.maximum) < np.asarray(self.minimum)):
            raise ValueError("Maximum must be >= minimum.")
        if self.total_resource < 0 or self.total_budget < 0:
            raise ValueError("Resource and budget must be non-negative.")


@dataclass(frozen=True)
class AllocationResult:
    allocation: np.ndarray
    objective: float
    resource_used: float
    budget_used: float
    success: bool
    message: str


def solve_allocation(problem: AllocationProblem) -> AllocationResult:
    """Maximize total effectiveness subject to resource, budget and bounds."""
    a_ub = np.vstack(
        [
            np.ones(len(problem.names), dtype=float),
            np.asarray(problem.unit_cost, dtype=float),
        ]
    )
    b_ub = np.array([problem.total_resource, problem.total_budget], dtype=float)
    bounds = list(zip(problem.minimum, problem.maximum))

    result = linprog(
        c=-np.asarray(problem.effectiveness, dtype=float),
        A_ub=a_ub,
        b_ub=b_ub,
        bounds=bounds,
        method="highs",
    )

    if not result.success:
        return AllocationResult(
            allocation=np.full(len(problem.names), np.nan),
            objective=float("nan"),
            resource_used=float("nan"),
            budget_used=float("nan"),
            success=False,
            message=result.message,
        )

    allocation = np.asarray(result.x, dtype=float)
    return AllocationResult(
        allocation=allocation,
        objective=float(problem.effectiveness @ allocation),
        resource_used=float(allocation.sum()),
        budget_used=float(problem.unit_cost @ allocation),
        success=True,
        message=result.message,
    )


def check_feasibility(
    problem: AllocationProblem,
    allocation: Iterable[float],
    atol: float = 1e-8,
) -> dict[str, bool]:
    """Check every constraint independently."""
    x = np.asarray(tuple(allocation), dtype=float)
    if x.shape != (len(problem.names),):
        raise ValueError("Allocation vector has wrong length.")

    checks = {
        "minimums": bool(np.all(x + atol >= problem.minimum)),
        "maximums": bool(np.all(x - atol <= problem.maximum)),
        "resource": bool(x.sum() <= problem.total_resource + atol),
        "budget": bool(problem.unit_cost @ x <= problem.total_budget + atol),
    }
    checks["all"] = all(checks.values())
    return checks


def objective_value(problem: AllocationProblem, allocation: Iterable[float]) -> float:
    """Return the value of the linear objective function."""
    x = np.asarray(tuple(allocation), dtype=float)
    if x.shape != (len(problem.names),):
        raise ValueError("Allocation vector has wrong length.")
    return float(problem.effectiveness @ x)


def baseline_problem() -> AllocationProblem:
    """Return the reproducible baseline used in the lesson."""
    return AllocationProblem(
        names=("A", "B", "C", "D"),
        effectiveness=np.array([8.0, 6.0, 9.0, 5.0]),
        unit_cost=np.array([3.0, 2.0, 4.0, 1.0]),
        minimum=np.array([10.0, 15.0, 10.0, 5.0]),
        maximum=np.array([40.0, 35.0, 30.0, 25.0]),
        total_resource=100.0,
        total_budget=250.0,
    )
