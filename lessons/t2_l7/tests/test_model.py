from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
import pytest

LESSON_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = LESSON_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from model import (
    DynamicParams,
    analytical_trajectory,
    bootstrap_calibration,
    calibrate_parameters,
    experiment_hash,
    numerical_trajectory,
    quantile_summary,
    scenario_batch,
    time_to_threshold,
)


def load_data():
    df = pd.read_csv(LESSON_DIR / "data" / "synthetic_observations.csv")
    return df["time"].to_numpy(float), df["observed_s"].to_numpy(float)


def test_initial_condition():
    value = analytical_trajectory([0.0], s0=20.0, q=12.0, k=0.1)[0]
    assert value == pytest.approx(20.0)


def test_analytical_matches_numerical():
    t = np.linspace(0, 20, 21)
    a = analytical_trajectory(t, s0=20.0, q=12.0, k=0.1)
    n = numerical_trajectory(t, s0=20.0, q=12.0, k=0.1)
    assert np.max(np.abs(a - n)) < 1e-6


def test_calibration_recovers_synthetic_parameters():
    t, y = load_data()
    fit = calibrate_parameters(t, y, s0=20.0)
    assert fit["q"] == pytest.approx(12.0, rel=0.03)
    assert fit["k"] == pytest.approx(0.10, rel=0.03)
    assert fit["rmse"] < 2.0


def test_threshold_time_baseline():
    value = time_to_threshold(s0=20.0, q=12.0, k=0.1, threshold=80.0)
    assert value == pytest.approx(9.1629, rel=1e-4)


def test_scenario_batch_has_expected_direction():
    df = scenario_batch([10.0, 12.0, 14.0], s0=20.0, k=0.1, horizon=20.0, threshold=80.0)
    assert list(df.columns) == ["q", "k", "equilibrium", "s_horizon", "time_to_threshold"]
    assert df["s_horizon"].is_monotonic_increasing
    assert df["time_to_threshold"].is_monotonic_decreasing


def test_bootstrap_is_reproducible():
    t, y = load_data()
    a = bootstrap_calibration(t, y, s0=20.0, threshold=80.0, horizon=20.0, n_boot=50, seed=2026)
    b = bootstrap_calibration(t, y, s0=20.0, threshold=80.0, horizon=20.0, n_boot=50, seed=2026)
    pd.testing.assert_frame_equal(a, b)


def test_bootstrap_interval_is_finite_and_contains_point_estimate():
    t, y = load_data()
    fit = calibrate_parameters(t, y, s0=20.0)
    point = time_to_threshold(s0=20.0, q=fit["q"], k=fit["k"], threshold=80.0)
    boot = bootstrap_calibration(t, y, s0=20.0, threshold=80.0, horizon=20.0, n_boot=150, seed=2026)
    summary = quantile_summary(boot, "time_to_threshold")
    assert np.isfinite(summary["p2_5"])
    assert np.isfinite(summary["p97_5"])
    assert summary["p2_5"] < point < summary["p97_5"]


def test_experiment_hash_is_deterministic():
    payload = {"b": 2, "a": 1}
    assert experiment_hash(payload) == experiment_hash({"a": 1, "b": 2})


def test_invalid_parameters_are_rejected():
    with pytest.raises(ValueError):
        DynamicParams(s0=20.0, q=0.0, k=0.1).validate()
    with pytest.raises(ValueError):
        analytical_trajectory([0, 1], s0=20.0, q=12.0, k=-0.1)
    with pytest.raises(ValueError):
        time_to_threshold(s0=20.0, q=12.0, k=0.1, threshold=-1.0)
