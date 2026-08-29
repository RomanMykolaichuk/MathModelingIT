from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from model import (
    DynamicParams,
    InterventionConfig,
    bootstrap_optimized_outcomes,
    budget_sensitivity,
    fit_parameters,
    grid_verify,
    optimize_intervention,
    state_trajectory,
    terminal_state,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_experiment(root: Path | None = None) -> dict:
    root = Path(root or Path(__file__).resolve().parents[1])
    config_path = root / "experiment_config.json"
    data_path = root / "data" / "observations.csv"
    out = root / "outputs"
    out.mkdir(parents=True, exist_ok=True)

    cfg_raw = load_config(config_path)
    obs = pd.read_csv(data_path)
    t = obs["time"].to_numpy(float)
    y = obs["observed_state"].to_numpy(float)

    fit = fit_parameters(t, y, s0=float(cfg_raw["model"]["s0"]))
    params = fit["params"]
    ic = InterventionConfig(**cfg_raw["intervention"])

    optimum = optimize_intervention(params, ic)
    grid = grid_verify(params, ic, resolution=int(cfg_raw["verification"]["grid_resolution"]))
    baseline_terminal = terminal_state(params, 0.0, 0.0, ic)

    budgets = cfg_raw["sensitivity"]["budgets"]
    sensitivity = budget_sensitivity(params, ic, budgets)
    sensitivity.to_csv(out / "budget_sensitivity.csv", index=False)

    boot = bootstrap_optimized_outcomes(
        t,
        y,
        ic,
        n_boot=int(cfg_raw["uncertainty"]["n_boot"]),
        seed=int(cfg_raw["uncertainty"]["seed"]),
        s0=float(cfg_raw["model"]["s0"]),
    )
    boot.to_csv(out / "bootstrap_results.csv", index=False)

    q_ci = np.quantile(boot["q_hat"], [0.025, 0.975]).tolist()
    k_ci = np.quantile(boot["k_hat"], [0.025, 0.975]).tolist()
    terminal_ci = np.quantile(boot["terminal_state"], [0.025, 0.975]).tolist()

    t_dense = np.linspace(float(t.min()), max(float(t.max()), ic.horizon), 300)
    fitted_curve = state_trajectory(t_dense, params)
    effective = DynamicParams(
        q=params.q * (1 + ic.q_gain * optimum["u"]),
        k=params.k * (1 - ic.k_reduction * optimum["v"]),
        s0=params.s0,
    )
    optimized_curve = state_trajectory(t_dense, effective)

    plt.figure(figsize=(8, 5))
    plt.scatter(t, y, label="synthetic observations")
    plt.plot(t_dense, fitted_curve, label="calibrated baseline")
    plt.plot(t_dense, optimized_curve, label="optimized intervention")
    plt.xlabel("time")
    plt.ylabel("state")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "trajectory_comparison.png", dpi=160)
    plt.close()

    plt.figure(figsize=(7, 4))
    plt.plot(sensitivity["budget"], sensitivity["terminal_state"], marker="o")
    plt.xlabel("budget")
    plt.ylabel("optimized terminal state")
    plt.tight_layout()
    plt.savefig(out / "budget_sensitivity.png", dpi=160)
    plt.close()

    summary = {
        "q_hat": params.q,
        "k_hat": params.k,
        "rmse": fit["rmse"],
        "baseline_terminal_state": baseline_terminal,
        "optimal_u": optimum["u"],
        "optimal_v": optimum["v"],
        "optimal_cost": optimum["cost"],
        "optimal_terminal_state": optimum["terminal_state"],
        "grid_terminal_state": grid["terminal_state"],
        "optimizer_grid_gap": optimum["terminal_state"] - grid["terminal_state"],
        "q_ci95": q_ci,
        "k_ci95": k_ci,
        "optimized_terminal_ci95": terminal_ci,
    }
    pd.DataFrame([summary]).to_json(out / "summary.json", orient="records", indent=2, force_ascii=False)

    fingerprint = hashlib.sha256(
        (_sha256(config_path) + _sha256(data_path) + _sha256(root / "src" / "model.py")).encode("utf-8")
    ).hexdigest()[:12]
    metadata = {
        "experiment_id": f"capstone_{fingerprint}",
        "config_sha256": _sha256(config_path),
        "data_sha256": _sha256(data_path),
        "model_sha256": _sha256(root / "src" / "model.py"),
        "seed": int(cfg_raw["uncertainty"]["seed"]),
        "n_boot": int(cfg_raw["uncertainty"]["n_boot"]),
        "outputs": [
            "summary.json",
            "budget_sensitivity.csv",
            "bootstrap_results.csv",
            "trajectory_comparison.png",
            "budget_sensitivity.png",
        ],
    }
    (out / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"summary": summary, "metadata": metadata, "optimum": optimum, "grid": grid}


if __name__ == "__main__":
    result = run_experiment()
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    print(result["metadata"]["experiment_id"])
