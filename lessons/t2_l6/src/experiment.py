"""Reproducible experiment for T2.L6."""

from __future__ import annotations

from pathlib import Path
import json

import numpy as np
import pandas as pd

from model import (
    analytical_solution,
    cumulative_state,
    equilibrium,
    lambdified_solution,
    max_symbolic_numeric_error,
    numerical_solution,
    symbolic_model,
    threshold_time,
)


BASELINE = {"q": 12.0, "k": 0.10, "s0": 20.0}
HORIZON = 30.0
TARGET = 80.0


def run_experiment(output_dir: str | Path | None = None):
    times = np.linspace(0.0, HORIZON, 121)
    p = BASELINE.copy()

    analytical = analytical_solution(times, **p)
    numerical = numerical_solution(times, **p)
    lambdified = lambdified_solution()(times, p["q"], p["k"], p["s0"])

    comparison = pd.DataFrame(
        {
            "time": times,
            "analytical": analytical,
            "lambdified": lambdified,
            "solve_ivp": numerical,
            "abs_error": np.abs(analytical - numerical),
        }
    )

    k_values = [0.05, 0.08, 0.10, 0.12, 0.15]
    sensitivity = pd.DataFrame(
        [
            {
                "k": k,
                "equilibrium": equilibrium(p["q"], k),
                "state_t10": analytical_solution(10.0, p["q"], k, p["s0"]),
            }
            for k in k_values
        ]
    )

    symbolic = symbolic_model()
    summary = {
        "baseline": p,
        "equilibrium": equilibrium(p["q"], p["k"]),
        "state_t10": analytical_solution(10.0, **p),
        "cumulative_0_10": cumulative_state(10.0, **p),
        "threshold": TARGET,
        "threshold_time": threshold_time(TARGET, **p),
        "max_symbolic_numeric_error": max_symbolic_numeric_error(times, **p),
        "symbolic_residual": str(symbolic["residual"]),
        "symbolic_equilibrium": str(symbolic["equilibrium"]),
        "symbolic_solution": str(symbolic["solution"]),
        "symbolic_cumulative": str(symbolic["cumulative"]),
        "sensitivity_dSeq_dq": str(symbolic["sensitivity_q"]),
        "sensitivity_dSeq_dk": str(symbolic["sensitivity_k"]),
    }

    if output_dir is not None:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        comparison.to_csv(out / "comparison.csv", index=False)
        sensitivity.to_csv(out / "sensitivity.csv", index=False)
        (out / "summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    return comparison, sensitivity, summary


if __name__ == "__main__":
    here = Path(__file__).resolve().parents[1]
    comparison, sensitivity, summary = run_experiment(here / "outputs")
    print(pd.Series(summary))
    print("\nSensitivity:")
    print(sensitivity.to_string(index=False))
