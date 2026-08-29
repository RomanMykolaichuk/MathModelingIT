"""Reproducible computational experiments for T2.L1."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from model import AllocationProblem, baseline_problem, check_feasibility, solve_allocation


def problem_with(
    base: AllocationProblem,
    *,
    total_resource: float | None = None,
    total_budget: float | None = None,
    effectiveness: np.ndarray | None = None,
) -> AllocationProblem:
    return AllocationProblem(
        names=base.names,
        effectiveness=base.effectiveness if effectiveness is None else np.asarray(effectiveness, dtype=float),
        unit_cost=base.unit_cost,
        minimum=base.minimum,
        maximum=base.maximum,
        total_resource=base.total_resource if total_resource is None else total_resource,
        total_budget=base.total_budget if total_budget is None else total_budget,
    )


def run_scenarios() -> pd.DataFrame:
    base = baseline_problem()
    scenarios = [
        ("baseline", base),
        ("resource_minus_10", problem_with(base, total_resource=90.0)),
        ("resource_plus_10", problem_with(base, total_resource=110.0)),
        ("budget_minus_20", problem_with(base, total_budget=230.0)),
        ("budget_plus_20", problem_with(base, total_budget=270.0)),
        ("direction_c_priority", problem_with(base, effectiveness=np.array([8.0, 6.0, 11.0, 5.0]))),
    ]

    rows: list[dict[str, float | str | bool]] = []
    for scenario_name, problem in scenarios:
        result = solve_allocation(problem)
        row: dict[str, float | str | bool] = {
            "scenario": scenario_name,
            "success": result.success,
            "objective": result.objective,
            "resource_used": result.resource_used,
            "budget_used": result.budget_used,
        }
        if result.success:
            for name, value in zip(problem.names, result.allocation):
                row[f"x_{name}"] = value
            row["feasible"] = check_feasibility(problem, result.allocation)["all"]
        else:
            for name in problem.names:
                row[f"x_{name}"] = np.nan
            row["feasible"] = False
        rows.append(row)

    return pd.DataFrame(rows)


def run_budget_sensitivity(start: float = 210.0, stop: float = 290.0, step: float = 10.0) -> pd.DataFrame:
    base = baseline_problem()
    rows = []
    for budget in np.arange(start, stop + step, step):
        problem = problem_with(base, total_budget=float(budget))
        result = solve_allocation(problem)
        rows.append(
            {
                "budget": float(budget),
                "success": result.success,
                "objective": result.objective,
                "resource_used": result.resource_used,
                "budget_used": result.budget_used,
            }
        )
    return pd.DataFrame(rows)


def save_outputs(output_dir: str | Path) -> tuple[Path, Path, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    scenarios = run_scenarios()
    sensitivity = run_budget_sensitivity()

    scenarios_path = output_dir / "scenario_results.csv"
    sensitivity_path = output_dir / "budget_sensitivity.csv"
    figure_path = output_dir / "budget_sensitivity.png"

    scenarios.to_csv(scenarios_path, index=False)
    sensitivity.to_csv(sensitivity_path, index=False)

    valid = sensitivity[sensitivity["success"]]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(valid["budget"], valid["objective"], marker="o")
    ax.set_title("Чутливість оптимального результату до бюджету")
    ax.set_xlabel("Доступний бюджет")
    ax.set_ylabel("Значення цільової функції")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(figure_path, dpi=160)
    plt.close(fig)

    return scenarios_path, sensitivity_path, figure_path


if __name__ == "__main__":
    paths = save_outputs(Path(__file__).resolve().parents[1] / "outputs")
    for path in paths:
        print(path)
