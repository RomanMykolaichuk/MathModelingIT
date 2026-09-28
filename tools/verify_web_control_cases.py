from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "web" / "control-cases.json").read_text(encoding="utf-8"))


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


resource = load_module("web_parity_t1_l1", ROOT / "lessons" / "t1_l1" / "src" / "model.py")
network = load_module("web_parity_t2_l4", ROOT / "lessons" / "t2_l4" / "src" / "model.py")
mcda = load_module("web_parity_t2_l5", ROOT / "lessons" / "t2_l5" / "src" / "model.py")


def assert_close(actual: float, expected: float, tol: float = 1e-8) -> None:
    if abs(float(actual) - float(expected)) > tol:
        raise AssertionError(f"очікувалося {expected}, отримано {actual}")


for key in ("baseline", "scenario"):
    c = CASES["resource"][key]
    assert_close(resource.resource(c["time"], c["s0"], c["rate"], c["clamp_zero"]), c["expected_value"])
    assert_close(resource.depletion_time(c["s0"], c["rate"]), c["expected_depletion_time"])


tasks = pd.DataFrame(
    [
        {"task": "A", "duration": 4, "predecessors": ""},
        {"task": "B", "duration": 3, "predecessors": ""},
        {"task": "C", "duration": 5, "predecessors": "A"},
        {"task": "D", "duration": 4, "predecessors": "A"},
        {"task": "E", "duration": 6, "predecessors": "B;C"},
        {"task": "F", "duration": 3, "predecessors": "D"},
        {"task": "G", "duration": 2, "predecessors": "E;F"},
    ]
)

duration, _, path = network.cpm_schedule(tasks)
assert_close(duration, CASES["network"]["baseline"]["expected_duration"])
assert path == CASES["network"]["baseline"]["expected_path"]

for key in ("delay_c3", "delay_d3"):
    c = CASES["network"][key]
    duration, _, path = network.cpm_schedule(network.apply_delay(tasks, c["task"], c["delay"]))
    assert_close(duration, c["expected_duration"])
    if "expected_path" in c:
        assert path == c["expected_path"]


matrix = pd.DataFrame(
    {
        "cost": [82, 70, 92, 76],
        "time": [18, 22, 15, 20],
        "reliability": [0.92, 0.88, 0.96, 0.90],
        "capacity": [75, 90, 80, 85],
        "risk": [0.18, 0.25, 0.12, 0.20],
    },
    index=["A", "B", "C", "D"],
)
base_weights = pd.Series({"cost": 0.25, "time": 0.20, "reliability": 0.25, "capacity": 0.20, "risk": 0.10})
types = {"cost": "cost", "time": "cost", "reliability": "benefit", "capacity": "benefit", "risk": "cost"}

for key in ("baseline", "low_reliability"):
    c = CASES["mcda"][key]
    weights = mcda.reweight_focus(base_weights, "reliability", c["reliability_weight"])
    wsm = mcda.weighted_sum(matrix, weights, types)
    top = mcda.topsis(matrix, weights, types)
    if "expected_wsm_ranking" in c:
        assert wsm.ranking == c["expected_wsm_ranking"]
    if "expected_topsis_ranking" in c:
        assert top.ranking == c["expected_topsis_ranking"]
    if "expected_wsm_top" in c:
        assert wsm.ranking[0] == c["expected_wsm_top"]
    if "expected_topsis_top" in c:
        assert top.ranking[0] == c["expected_topsis_top"]
    if "expected_wsm_c" in c:
        assert_close(wsm.scores["C"], c["expected_wsm_c"], 1e-9)
    if "expected_topsis_c" in c:
        assert_close(top.scores["C"], c["expected_topsis_c"], 1e-9)

print("Python control cases: PASS")
