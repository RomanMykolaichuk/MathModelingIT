import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from model import (  # noqa: E402
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


def observations():
    df = pd.read_csv(ROOT / "data" / "observations.csv")
    return df["time"].to_numpy(float), df["observed_state"].to_numpy(float)


def test_trajectory_starts_at_s0():
    p = DynamicParams(12, 0.1, 20)
    assert state_trajectory([0], p)[0] == pytest.approx(20)


def test_fit_is_close_to_generating_region():
    t, y = observations()
    fit = fit_parameters(t, y, s0=20)
    assert fit["success"]
    assert 11.0 < fit["params"].q < 13.5
    assert 0.085 < fit["params"].k < 0.12
    assert fit["rmse"] < 2.5


def test_optimization_is_feasible_and_improves_baseline():
    t, y = observations()
    p = fit_parameters(t, y, s0=20)["params"]
    cfg = InterventionConfig()
    opt = optimize_intervention(p, cfg)
    assert opt["success"] and opt["feasible"]
    assert opt["cost"] <= cfg.budget + 1e-6
    assert opt["terminal_state"] > terminal_state(p, 0, 0, cfg)


def test_optimizer_agrees_with_grid_search():
    t, y = observations()
    p = fit_parameters(t, y, s0=20)["params"]
    cfg = InterventionConfig()
    opt = optimize_intervention(p, cfg)
    grid = grid_verify(p, cfg, resolution=101)
    assert abs(opt["terminal_state"] - grid["terminal_state"]) < 0.25


def test_budget_sensitivity_is_non_decreasing():
    t, y = observations()
    p = fit_parameters(t, y, s0=20)["params"]
    df = budget_sensitivity(p, InterventionConfig(), [40, 55, 70, 85])
    diffs = np.diff(df["terminal_state"].to_numpy())
    assert np.all(diffs >= -1e-7)


def test_bootstrap_is_reproducible():
    t, y = observations()
    cfg = InterventionConfig()
    a = bootstrap_optimized_outcomes(t, y, cfg, n_boot=30, seed=2026)
    b = bootstrap_optimized_outcomes(t, y, cfg, n_boot=30, seed=2026)
    pd.testing.assert_frame_equal(a, b)


def test_bootstrap_has_finite_results():
    t, y = observations()
    df = bootstrap_optimized_outcomes(t, y, InterventionConfig(), n_boot=30, seed=7)
    assert np.isfinite(df[["q_hat", "k_hat", "terminal_state"]].to_numpy()).all()


def test_invalid_parameters_raise():
    with pytest.raises(ValueError):
        state_trajectory([0, 1], DynamicParams(0, 0.1, 20))


def test_invalid_grid_resolution_raises():
    with pytest.raises(ValueError):
        grid_verify(DynamicParams(12, 0.1, 20), InterventionConfig(), resolution=5)
