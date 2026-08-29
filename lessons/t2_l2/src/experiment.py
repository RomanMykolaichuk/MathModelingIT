"""Reproducible scenario experiment for T2.L2."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
LESSON = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from model import check_solution, long_plan, solve_transport_pulp, solve_transport_scipy


def load_problem():
    costs = pd.read_csv(LESSON / "data" / "costs.csv", index_col="supplier")
    supply_df = pd.read_csv(LESSON / "data" / "supply.csv")
    demand_df = pd.read_csv(LESSON / "data" / "demand.csv")
    supply = supply_df.set_index("supplier")["supply"].astype(float)
    demand = demand_df.set_index("consumer")["demand"].astype(float)
    return costs.astype(float), supply, demand


def run_scenarios():
    costs, supply, demand = load_problem()

    scenarios = []

    def record(name, c, s, d, forbidden=None):
        result = solve_transport_pulp(c, s, d, forbidden_routes=forbidden)
        verification = check_solution(result.plan, s, d)
        scenarios.append(
            {
                "scenario": name,
                "total_cost": result.total_cost,
                "feasible": verification["feasible"],
            }
        )
        return result

    baseline = record("baseline", costs, supply, demand)

    scipy_baseline = solve_transport_scipy(costs, supply, demand)
    if abs(scipy_baseline.total_cost - baseline.total_cost) > 1e-6:
        raise RuntimeError("PuLP and SciPy disagree on the baseline optimum.")

    record("close_S2_D3", costs, supply, demand, forbidden=[("S2", "D3")])

    shock = costs.copy()
    shock.loc["S2", "D3"] += 4
    record("cost_S2_D3_plus4", shock, supply, demand)

    d4_cost = costs.copy()
    d4_cost["D4"] += 2
    record("all_routes_to_D4_plus2", d4_cost, supply, demand)

    shifted_supply = supply.copy()
    shifted_supply.loc["S1"] -= 10
    shifted_supply.loc["S3"] += 10
    record("supply_shift_S1_to_S3", costs, shifted_supply, demand)

    return baseline, pd.DataFrame(scenarios)


def save_outputs():
    output_dir = LESSON / "outputs"
    output_dir.mkdir(exist_ok=True)

    costs, _, _ = load_problem()
    baseline, scenarios = run_scenarios()

    baseline.plan.to_csv(output_dir / "baseline_plan.csv")
    long_plan(baseline.plan, costs).to_csv(output_dir / "baseline_routes.csv", index=False)
    scenarios.to_csv(output_dir / "scenario_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4))
    image = ax.imshow(baseline.plan.to_numpy(dtype=float), aspect="auto")
    ax.set_xticks(range(len(baseline.plan.columns)), baseline.plan.columns)
    ax.set_yticks(range(len(baseline.plan.index)), baseline.plan.index)
    ax.set_xlabel("Пункт потреби")
    ax.set_ylabel("Джерело")
    ax.set_title("Оптимальний транспортний план")
    for i in range(baseline.plan.shape[0]):
        for j in range(baseline.plan.shape[1]):
            ax.text(j, i, f"{baseline.plan.iloc[i, j]:.0f}", ha="center", va="center")
    fig.colorbar(image, ax=ax, label="Обсяг перевезення")
    fig.tight_layout()
    fig.savefig(output_dir / "baseline_plan_heatmap.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(scenarios["scenario"], scenarios["total_cost"])
    ax.set_ylabel("Загальні витрати")
    ax.set_title("Вартість транспортного плану за сценаріями")
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(output_dir / "scenario_costs.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    save_outputs()
