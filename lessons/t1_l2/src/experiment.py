from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LESSON_DIR = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from model import (
    ResourceModelParams,
    deterministic_stock,
    deterministic_exhaustion_time,
    monte_carlo_exhaustion_times,
    stochastic_stock_path,
    summarize_exhaustion,
)


def run_experiment(output_dir: Path | None = None) -> dict[str, object]:
    output_dir = output_dir or (LESSON_DIR / "outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    params = ResourceModelParams(
        initial_stock=120.0,
        mean_consumption=6.0,
        std_consumption=1.5,
        horizon=21,
    )

    time = np.arange(params.horizon + 1)
    deterministic = deterministic_stock(
        time, params.initial_stock, params.mean_consumption
    )

    stock_seed_7, consumption_seed_7 = stochastic_stock_path(params, seed=7)
    stock_seed_21, consumption_seed_21 = stochastic_stock_path(params, seed=21)

    times = monte_carlo_exhaustion_times(params, n_runs=3000, seed=2026)
    summary = summarize_exhaustion(times)

    paths = pd.DataFrame({
        "step": time,
        "deterministic": deterministic,
        "stochastic_seed_7": stock_seed_7,
        "stochastic_seed_21": stock_seed_21,
    })
    paths.to_csv(output_dir / "model_paths.csv", index=False)

    mc = pd.DataFrame({"exhaustion_step": times})
    mc.to_csv(output_dir / "monte_carlo_exhaustion.csv", index=False)

    summary_df = pd.DataFrame([{
        "deterministic_exhaustion_time": deterministic_exhaustion_time(
            params.initial_stock, params.mean_consumption
        ),
        **summary,
    }])
    summary_df.to_csv(output_dir / "summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(time, deterministic, label="Deterministic")
    ax.plot(time, stock_seed_7, label="Stochastic seed=7")
    ax.plot(time, stock_seed_21, label="Stochastic seed=21")
    ax.set_title("Deterministic and stochastic resource models")
    ax.set_xlabel("Discrete step")
    ax.set_ylabel("Remaining stock")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "model_paths.png", dpi=180)
    plt.close(fig)

    finite = times[np.isfinite(times)]
    if len(finite):
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.hist(finite, bins=np.arange(finite.min() - 0.5, finite.max() + 1.5, 1))
        ax.set_title("Monte Carlo distribution of exhaustion step")
        ax.set_xlabel("Exhaustion step")
        ax.set_ylabel("Number of runs")
        fig.tight_layout()
        fig.savefig(output_dir / "exhaustion_histogram.png", dpi=180)
        plt.close(fig)

    return {
        "params": params,
        "paths": paths,
        "summary": summary_df.iloc[0].to_dict(),
    }


if __name__ == "__main__":
    result = run_experiment()
    print(result["summary"])
