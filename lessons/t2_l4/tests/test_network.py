import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from model import (
    build_graph, cpm_schedule, apply_delay, pert_parameters,
    beta_pert_sample, monte_carlo_project, deadline_probability
)

TASKS = pd.read_csv(ROOT / "data" / "tasks.csv")
PERT = pd.read_csv(ROOT / "data" / "pert.csv")


def test_baseline_project_duration_and_path():
    duration, schedule, path = cpm_schedule(TASKS)
    assert duration == pytest.approx(17.0)
    assert path == ["A","C","E","G"]


def test_baseline_slacks():
    _, schedule, _ = cpm_schedule(TASKS)
    s = schedule.set_index("task")
    assert s.loc["B","slack"] == pytest.approx(6.0)
    assert s.loc["D","slack"] == pytest.approx(4.0)
    assert s.loc["F","slack"] == pytest.approx(4.0)
    assert set(s[s["critical"]].index) == {"A","C","E","G"}


def test_delay_on_critical_task_extends_project():
    delayed = apply_delay(TASKS, "C", 3)
    duration, _, path = cpm_schedule(delayed)
    assert duration == pytest.approx(20.0)
    assert path == ["A","C","E","G"]


def test_delay_within_noncritical_slack_does_not_extend_project():
    delayed = apply_delay(TASKS, "D", 3)
    duration, _, _ = cpm_schedule(delayed)
    assert duration == pytest.approx(17.0)


def test_cycle_is_rejected():
    bad = TASKS.copy()
    bad.loc[bad["task"]=="A","predecessors"] = "G"
    with pytest.raises(ValueError):
        build_graph(bad)


def test_pert_mean_formula():
    params = pert_parameters(PERT).set_index("task")
    assert params.loc["A","pert_mean"] == pytest.approx((3+4*4+6)/6)


def test_beta_pert_reproducible():
    a = beta_pert_sample(3,4,6,100,np.random.default_rng(2026))
    b = beta_pert_sample(3,4,6,100,np.random.default_rng(2026))
    assert np.allclose(a,b)


def test_monte_carlo_reproducible_and_plausible():
    r1, f1 = monte_carlo_project(TASKS, PERT, n=500, seed=2026)
    r2, f2 = monte_carlo_project(TASKS, PERT, n=500, seed=2026)
    assert np.allclose(r1["project_duration"], r2["project_duration"])
    assert 16 < r1["project_duration"].mean() < 20
    assert f1.iloc[0]["critical_path"] == "A -> C -> E -> G"


def test_deadline_probability_range():
    results, _ = monte_carlo_project(TASKS, PERT, n=800, seed=2026)
    p = deadline_probability(results, 19)
    assert 0 <= p <= 1
    assert 0.65 < p < 0.9
