"""Reproducible mini-research experiment for T2.L7."""

from __future__ import annotations

import json
from pathlib import Path
import platform
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from model import (
    analytical_trajectory,
    bootstrap_calibration,
    calibrate_parameters,
    experiment_hash,
    numerical_trajectory,
    quantile_summary,
    scenario_batch,
    time_to_threshold,
)

HERE = Path(__file__).resolve().parent
LESSON_DIR = HERE.parent
DATA_DIR = LESSON_DIR / "data"
OUTPUT_DIR = LESSON_DIR / "outputs"


def run(output_dir: Path | None = None) -> dict[str, float | str]:
    output_dir = Path(output_dir) if output_dir else OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    config = json.loads((LESSON_DIR / "experiment_config.json").read_text(encoding="utf-8"))
    observations = pd.read_csv(DATA_DIR / "synthetic_observations.csv")
    t = observations["time"].to_numpy(dtype=float)
    y = observations["observed_s"].to_numpy(dtype=float)

    s0 = float(config["s0"])
    threshold = float(config["threshold"])
    horizon = float(config["horizon"])
    fit = calibrate_parameters(t, y, s0=s0)

    fitted = analytical_trajectory(t, s0=s0, q=fit["q"], k=fit["k"])
    numerical = numerical_trajectory(t, s0=s0, q=fit["q"], k=fit["k"])
    max_verification_error = float(np.max(np.abs(fitted - numerical)))

    q_values = [fit["q"] * float(m) for m in config["q_multipliers"]]
    scenarios = scenario_batch(q_values, s0=s0, k=fit["k"], horizon=horizon, threshold=threshold)
    scenarios.insert(0, "q_multiplier", config["q_multipliers"])
    scenarios.to_csv(output_dir / "scenario_results.csv", index=False)

    bootstrap = bootstrap_calibration(
        t,
        y,
        s0=s0,
        threshold=threshold,
        horizon=horizon,
        n_boot=int(config["bootstrap_replications"]),
        seed=int(config["seed"]),
    )
    bootstrap.to_csv(output_dir / "bootstrap_predictions.csv", index=False)

    threshold_summary = quantile_summary(bootstrap, "time_to_threshold")
    horizon_summary = quantile_summary(bootstrap, "s_horizon")

    calibration = pd.DataFrame([
        {
            **fit,
            "time_to_threshold": time_to_threshold(s0=s0, q=fit["q"], k=fit["k"], threshold=threshold),
            "s_horizon": float(analytical_trajectory([horizon], s0=s0, q=fit["q"], k=fit["k"])[0]),
            "analytical_vs_solve_ivp_max_abs_error": max_verification_error,
        }
    ])
    calibration.to_csv(output_dir / "calibration_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    dense_t = np.linspace(0, horizon, 300)
    ax.scatter(t, y, label="Synthetic observations")
    ax.plot(dense_t, analytical_trajectory(dense_t, s0=s0, q=fit["q"], k=fit["k"]), label="Calibrated analytical model")
    ax.set_xlabel("Time")
    ax.set_ylabel("State S(t)")
    ax.set_title("T2.L7 — calibration of the research model")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "calibration_fit.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(scenarios["q_multiplier"], scenarios["time_to_threshold"], marker="o")
    ax.set_xlabel("q multiplier")
    ax.set_ylabel("Time to threshold")
    ax.set_title("Sensitivity to the replenishment parameter q")
    fig.tight_layout()
    fig.savefig(output_dir / "sensitivity.png", dpi=160)
    plt.close(fig)

    finite_threshold = bootstrap["time_to_threshold"].replace([np.inf, -np.inf], np.nan).dropna()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(finite_threshold, bins=25)
    ax.set_xlabel("Time to threshold")
    ax.set_ylabel("Frequency")
    ax.set_title("Bootstrap uncertainty of the research prediction")
    fig.tight_layout()
    fig.savefig(output_dir / "bootstrap_threshold.png", dpi=160)
    plt.close(fig)

    hash_payload = {
        "config": config,
        "data": observations.round(8).to_dict(orient="records"),
        "model": "dS/dt=q-kS",
    }
    exp_hash = experiment_hash(hash_payload)
    metadata = {
        "experiment_id": f"t2_l7_{exp_hash}",
        "model": "dS/dt = q - kS",
        "config": config,
        "calibrated_parameters": fit,
        "threshold_uncertainty": threshold_summary,
        "horizon_uncertainty": horizon_summary,
        "verification": {"analytical_vs_solve_ivp_max_abs_error": max_verification_error},
        "environment": {"python": sys.version.split()[0], "platform": platform.platform()},
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "experiment_id": metadata["experiment_id"],
        "q_hat": fit["q"],
        "k_hat": fit["k"],
        "rmse": fit["rmse"],
        "time_to_threshold": float(calibration.iloc[0]["time_to_threshold"]),
        "s_horizon": float(calibration.iloc[0]["s_horizon"]),
        "threshold_ci_low": threshold_summary["p2_5"],
        "threshold_ci_high": threshold_summary["p97_5"],
        "max_verification_error": max_verification_error,
    }
    pd.DataFrame([summary]).to_csv(output_dir / "summary.csv", index=False)
    return summary


if __name__ == "__main__":
    result = run()
    for key, value in result.items():
        print(f"{key}: {value}")
