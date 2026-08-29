import math
from pathlib import Path
import sys

import numpy as np
import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from model import compare_rates, depletion_time, resource, simulate


def test_resource_known_values():
    result = resource([0, 5, 10], s0=100, rate=5)
    np.testing.assert_allclose(result, [100, 75, 50])


def test_physical_constraint_clamps_at_zero():
    result = resource([0, 10, 30], s0=100, rate=5, clamp_zero=True)
    np.testing.assert_allclose(result, [100, 50, 0])


def test_unclamped_model_exposes_model_domain_issue():
    result = resource([30], s0=100, rate=5, clamp_zero=False)
    np.testing.assert_allclose(result, [-50])


def test_zero_rate_has_infinite_depletion_time():
    assert math.isinf(depletion_time(100, 0))


def test_depletion_time_known_value():
    assert depletion_time(120, 8) == pytest.approx(15.0)


def test_negative_inputs_rejected():
    with pytest.raises(ValueError):
        resource([0, -1], s0=100, rate=5)
    with pytest.raises(ValueError):
        resource([0, 1], s0=-1, rate=5)
    with pytest.raises(ValueError):
        resource([0, 1], s0=100, rate=-5)


def test_simulate_returns_expected_columns_and_rows():
    df = simulate(range(3), s0=10, rate=2)
    assert list(df.columns) == ["time", "resource", "s0", "rate", "clamp_zero"]
    assert len(df) == 3


def test_compare_rates_contains_all_scenarios():
    df = compare_rates(range(2), s0=10, rates=[1, 2, 3])
    assert sorted(df["scenario_rate"].unique().tolist()) == [1.0, 2.0, 3.0]
