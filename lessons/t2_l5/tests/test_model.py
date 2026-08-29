import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))
from model import (
    minmax_normalize, weighted_sum, topsis, reweight_focus,
    one_factor_sensitivity, robustness_analysis
)

M = pd.DataFrame({
    "cost":[82,70,92,76],
    "time":[18,22,15,20],
    "reliability":[0.92,0.88,0.96,0.90],
    "capacity":[75,90,80,85],
    "risk":[0.18,0.25,0.12,0.20],
}, index=["A","B","C","D"])
W = pd.Series({"cost":0.25,"time":0.20,"reliability":0.25,"capacity":0.20,"risk":0.10})
T = {"cost":"cost","time":"cost","reliability":"benefit","capacity":"benefit","risk":"cost"}


def test_minmax_higher_is_always_better():
    n = minmax_normalize(M, T)
    assert n.loc["B","cost"] == pytest.approx(1.0)
    assert n.loc["C","cost"] == pytest.approx(0.0)
    assert n.loc["C","reliability"] == pytest.approx(1.0)


def test_wsm_baseline_ranking():
    r = weighted_sum(M, W, T)
    assert r.ranking == ["C","D","B","A"]
    assert r.scores["C"] == pytest.approx(0.6166666667)


def test_topsis_baseline_ranking():
    r = topsis(M, W, T)
    assert r.ranking == ["C","A","D","B"]
    assert r.scores["C"] == pytest.approx(0.5868840374)


def test_reweight_focus_preserves_sum():
    w = reweight_focus(W, "reliability", 0.40)
    assert w["reliability"] == pytest.approx(0.40)
    assert w.sum() == pytest.approx(1.0)


def test_sensitivity_detects_wsm_rank_change():
    s = one_factor_sensitivity(M, W, T, "reliability", [0.10,0.25])
    assert s.iloc[0]["wsm_top"] == "B"
    assert s.iloc[1]["wsm_top"] == "C"
    assert s.iloc[0]["topsis_top"] == "C"


def test_robustness_reproducible():
    a = robustness_analysis(M, W, T, n_runs=500, concentration=80, seed=2026)
    b = robustness_analysis(M, W, T, n_runs=500, concentration=80, seed=2026)
    pd.testing.assert_frame_equal(a, b)


def test_robustness_baseline_favors_c():
    r = robustness_analysis(M, W, T, n_runs=3000, concentration=80, seed=2026)
    p = r.pivot(index="alternative", columns="method", values="top_choice_share")
    assert p.loc["C","wsm"] > 0.90
    assert p.loc["C","topsis"] > 0.80


def test_invalid_weights_rejected():
    with pytest.raises(ValueError):
        weighted_sum(M, W * 0.9, T)


def test_cost_benefit_classification_matters():
    wrong = dict(T)
    wrong["cost"] = "benefit"
    right = weighted_sum(M, W, T)
    wrong_result = weighted_sum(M, W, wrong)
    assert not np.allclose(right.scores.values, wrong_result.scores.values)
    assert right.ranking != wrong_result.ranking
