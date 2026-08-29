"""Scenario runner for T2.L3."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from model import (
    solve_applied,
    verify_applied_solution,
    applied_sensitivity,
    multistart_nonconvex,
    grid_search_nonconvex,
)


def run(output_dir: str | Path = "../outputs"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    baseline = solve_applied(total_resource=100.0, start=(50.0, 50.0))
    checks = verify_applied_solution(baseline, 100.0)

    sensitivity = pd.DataFrame(applied_sensitivity([60, 80, 100, 120]))
    sensitivity.to_csv(output_dir / "applied_sensitivity.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(sensitivity["total_resource"], sensitivity["objective"], marker="o")
    ax.set_title("Нелінійна віддача від збільшення ресурсу")
    ax.set_xlabel("Доступний ресурс")
    ax.set_ylabel("Оптимальне значення цільової функції")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "applied_sensitivity.png", dpi=160)
    plt.close(fig)

    starts = [(-3, -3), (-3, 2), (0, 0), (2, 2), (3, -2), (4, 4)]
    multi = pd.DataFrame(multistart_nonconvex(starts))
    multi.to_csv(output_dir / "nonconvex_multistart.csv", index=False)
    grid = grid_search_nonconvex(step=0.05)
    pd.DataFrame([grid]).to_csv(output_dir / "nonconvex_grid_check.csv", index=False)

    xs = np.linspace(-4, 4, 240)
    ys = np.linspace(-4, 4, 240)
    X, Y = np.meshgrid(xs, ys)
    Z = np.sin(1.7 * X) * np.cos(1.3 * Y) + 0.15 * X - 0.03 * (X * X + Y * Y)
    fig, ax = plt.subplots(figsize=(7, 5))
    cs = ax.contourf(X, Y, Z, levels=25)
    ax.scatter(multi["x"], multi["y"], s=35, label="local optima from starts")
    ax.scatter([grid["x"]], [grid["y"]], marker="*", s=140, label="grid-search best")
    ax.set_title("Non-convex landscape: multi-start vs grid search")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    fig.colorbar(cs, ax=ax, label="objective")
    fig.tight_layout()
    fig.savefig(output_dir / "nonconvex_contours.png", dpi=160)
    plt.close(fig)

    return baseline, checks, sensitivity, multi, grid


if __name__ == "__main__":
    baseline, checks, sensitivity, multi, grid = run()
    print("Baseline:", baseline)
    print("Verification:", checks)
    print("\nSensitivity:\n", sensitivity)
    print("\nTop multi-start solutions:\n", multi.head())
    print("\nGrid check:", grid)
