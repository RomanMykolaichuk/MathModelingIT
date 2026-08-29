"""Config-driven experiment runner for T1.L3."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from .model import deterministic_response, simulate_observation
except ImportError:
    from model import deterministic_response, simulate_observation


def canonical_json(data: dict[str, Any]) -> str:
    """Return stable JSON representation used for hashing and reproducibility."""
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def config_hash(config: dict[str, Any]) -> str:
    """Return short deterministic SHA-256 hash of experiment configuration."""
    return hashlib.sha256(canonical_json(config).encode("utf-8")).hexdigest()[:12]


def load_config(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_config(config: dict[str, Any]) -> None:
    required = {"seed", "replications", "model"}
    missing = required - set(config)
    if missing:
        raise ValueError(f"Missing config keys: {sorted(missing)}")
    if int(config["replications"]) <= 0:
        raise ValueError("replications must be positive")
    if float(config["model"]["noise_sd"]) < 0:
        raise ValueError("noise_sd must be non-negative")


def run_experiment(config: dict[str, Any], scenarios: pd.DataFrame) -> pd.DataFrame:
    """Run all scenarios and return one row per stochastic replication."""
    validate_config(config)
    needed = {"scenario_id", "resource", "load"}
    missing = needed - set(scenarios.columns)
    if missing:
        raise ValueError(f"Missing scenario columns: {sorted(missing)}")

    rng = np.random.default_rng(int(config["seed"]))
    params = config["model"]
    rows: list[dict[str, Any]] = []

    for row in scenarios.itertuples(index=False):
        deterministic = float(
            deterministic_response(
                row.resource,
                row.load,
                baseline=params["baseline"],
                resource_gain=params["resource_gain"],
                load_penalty=params["load_penalty"],
            )
        )
        for replication in range(int(config["replications"])):
            observed = simulate_observation(
                row.resource,
                row.load,
                rng=rng,
                noise_sd=params["noise_sd"],
                baseline=params["baseline"],
                resource_gain=params["resource_gain"],
                load_penalty=params["load_penalty"],
            )
            rows.append(
                {
                    "scenario_id": row.scenario_id,
                    "resource": float(row.resource),
                    "load": float(row.load),
                    "replication": replication,
                    "deterministic_response": deterministic,
                    "observed_response": observed,
                }
            )
    return pd.DataFrame(rows)


def summarize_results(results: pd.DataFrame) -> pd.DataFrame:
    """Aggregate replications into interpretable scenario-level metrics."""
    return (
        results.groupby(["scenario_id", "resource", "load"], as_index=False)
        .agg(
            deterministic_response=("deterministic_response", "first"),
            mean_observed=("observed_response", "mean"),
            std_observed=("observed_response", "std"),
            p10=("observed_response", lambda x: x.quantile(0.10)),
            p90=("observed_response", lambda x: x.quantile(0.90)),
        )
    )


def build_metadata(config: dict[str, Any], scenarios: pd.DataFrame) -> dict[str, Any]:
    """Create deterministic metadata needed to identify the experiment."""
    return {
        "experiment_id": f"t1_l3_{config_hash(config)}",
        "config_hash": config_hash(config),
        "seed": int(config["seed"]),
        "replications": int(config["replications"]),
        "scenario_count": int(len(scenarios)),
        "model": config["model"],
        "workflow_note": "Results are reproducible for the same code, config, data and software environment.",
    }


def save_outputs(
    results: pd.DataFrame,
    summary: pd.DataFrame,
    metadata: dict[str, Any],
    output_dir: str | Path,
) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_dir / "results.csv", index=False)
    summary.to_csv(output_dir / "summary.csv", index=False)
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def run_from_files(config_path: str | Path, scenarios_path: str | Path, output_dir: str | Path):
    config = load_config(config_path)
    scenarios = pd.read_csv(scenarios_path)
    results = run_experiment(config, scenarios)
    summary = summarize_results(results)
    metadata = build_metadata(config, scenarios)
    save_outputs(results, summary, metadata, output_dir)
    return results, summary, metadata


def main() -> None:
    lesson_dir = Path(__file__).resolve().parents[1]
    _, summary, metadata = run_from_files(
        lesson_dir / "experiment_config.json",
        lesson_dir / "data" / "scenarios.csv",
        lesson_dir / "outputs",
    )
    print(summary.to_string(index=False))
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
