"""Reproducible computational experiment for T1.L1."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from model import compare_rates, depletion_time, simulate


def run_experiment(output_dir: str | Path | None = None) -> dict[str, object]:
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / "outputs"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    times = range(0, 21)
    base = simulate(times, s0=120, rate=8)
    economy = simulate(times, s0=120, rate=5)

    comparison = pd.concat(
        [
            base.assign(scenario="base"),
            economy.assign(scenario="economy"),
        ],
        ignore_index=True,
    )
    comparison.to_csv(output_dir / "scenario_comparison.csv", index=False)

    sensitivity = compare_rates(times, s0=120, rates=[4, 6, 8, 10, 12])
    sensitivity.to_csv(output_dir / "rate_sensitivity.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    for name, group in comparison.groupby("scenario"):
        ax.plot(group["time"], group["resource"], marker="o", label=name)
    ax.set_title("Зміна запасу ресурсу в часі")
    ax.set_xlabel("Час, умовні одиниці")
    ax.set_ylabel("Залишок ресурсу, умовні одиниці")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "scenario_comparison.png", dpi=160)
    plt.close(fig)

    summary = {
        "base_depletion_time": depletion_time(120, 8),
        "economy_depletion_time": depletion_time(120, 5),
        "base_resource_t10": float(base.loc[base["time"] == 10, "resource"].iloc[0]),
        "economy_resource_t10": float(economy.loc[economy["time"] == 10, "resource"].iloc[0]),
    }
    pd.DataFrame([summary]).to_csv(output_dir / "summary.csv", index=False)
    return summary


if __name__ == "__main__":
    summary = run_experiment()
    for key, value in summary.items():
        print(f"{key}: {value}")
