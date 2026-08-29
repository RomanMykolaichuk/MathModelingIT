import numpy as np
import pandas as pd
import pytest

from lessons.t1_l3.src.model import deterministic_response, simulate_observation
from lessons.t1_l3.src.experiment import (
    build_metadata,
    config_hash,
    run_experiment,
    summarize_results,
)


CONFIG = {
    "seed": 2026,
    "replications": 20,
    "model": {
        "baseline": 20.0,
        "resource_gain": 1.8,
        "load_penalty": 1.2,
        "noise_sd": 4.0,
    },
}
SCENARIOS = pd.DataFrame(
    [
        {"scenario_id": "baseline", "resource": 40, "load": 50},
        {"scenario_id": "high", "resource": 50, "load": 50},
    ]
)


def test_deterministic_response_known_value():
    assert deterministic_response(40, 50) == pytest.approx(32.0)


def test_deterministic_response_clipped_at_zero():
    assert deterministic_response(0, 100) == pytest.approx(0.0)


def test_negative_inputs_rejected():
    with pytest.raises(ValueError):
        deterministic_response(-1, 10)


def test_reproducible_observation_with_same_seed():
    rng1 = np.random.default_rng(2026)
    rng2 = np.random.default_rng(2026)
    a = simulate_observation(40, 50, rng=rng1)
    b = simulate_observation(40, 50, rng=rng2)
    assert a == pytest.approx(b)


def test_run_experiment_row_count():
    results = run_experiment(CONFIG, SCENARIOS)
    assert len(results) == 40


def test_run_experiment_reproducible():
    a = run_experiment(CONFIG, SCENARIOS)
    b = run_experiment(CONFIG, SCENARIOS)
    pd.testing.assert_frame_equal(a, b)


def test_summary_contains_all_scenarios():
    results = run_experiment(CONFIG, SCENARIOS)
    summary = summarize_results(results)
    assert set(summary["scenario_id"]) == {"baseline", "high"}


def test_config_hash_is_stable_to_key_order():
    config2 = {
        "replications": 20,
        "model": CONFIG["model"],
        "seed": 2026,
    }
    assert config_hash(CONFIG) == config_hash(config2)


def test_metadata_identifies_experiment():
    metadata = build_metadata(CONFIG, SCENARIOS)
    assert metadata["experiment_id"].startswith("t1_l3_")
    assert metadata["seed"] == 2026
    assert metadata["scenario_count"] == 2
