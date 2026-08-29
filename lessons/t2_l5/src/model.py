"""MCDA models for T2.L5.

Implements:
- min-max normalization for benefit/cost criteria;
- Weighted Sum Model (WSM);
- TOPSIS;
- one-factor weight sensitivity;
- stochastic robustness analysis for uncertain weights.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class MCDAResult:
    scores: pd.Series
    ranking: list[str]


def validate_inputs(
    decision_matrix: pd.DataFrame,
    weights: pd.Series,
    criterion_types: Mapping[str, str],
) -> None:
    if decision_matrix.empty:
        raise ValueError("Decision matrix must not be empty.")
    if decision_matrix.isna().any().any():
        raise ValueError("Decision matrix contains missing values.")
    if set(decision_matrix.columns) != set(weights.index):
        raise ValueError("Weights must match decision-matrix criteria.")
    if set(decision_matrix.columns) != set(criterion_types.keys()):
        raise ValueError("Criterion types must match decision-matrix criteria.")
    if (weights < 0).any():
        raise ValueError("Weights must be non-negative.")
    if not np.isclose(float(weights.sum()), 1.0, atol=1e-9):
        raise ValueError("Weights must sum to 1.")
    invalid = {v for v in criterion_types.values() if v not in {"benefit", "cost"}}
    if invalid:
        raise ValueError(f"Unknown criterion types: {sorted(invalid)}")


def minmax_normalize(
    decision_matrix: pd.DataFrame,
    criterion_types: Mapping[str, str],
) -> pd.DataFrame:
    """Normalize all criteria to [0,1], where higher is always better."""
    out = pd.DataFrame(index=decision_matrix.index, dtype=float)
    for col in decision_matrix.columns:
        values = decision_matrix[col].astype(float)
        lo, hi = float(values.min()), float(values.max())
        if np.isclose(hi, lo):
            out[col] = 1.0
        elif criterion_types[col] == "benefit":
            out[col] = (values - lo) / (hi - lo)
        else:
            out[col] = (hi - values) / (hi - lo)
    return out


def weighted_sum(
    decision_matrix: pd.DataFrame,
    weights: pd.Series,
    criterion_types: Mapping[str, str],
) -> MCDAResult:
    validate_inputs(decision_matrix, weights, criterion_types)
    norm = minmax_normalize(decision_matrix, criterion_types)
    scores = (norm * weights[decision_matrix.columns]).sum(axis=1)
    ranking = scores.sort_values(ascending=False).index.tolist()
    return MCDAResult(scores=scores, ranking=ranking)


def topsis(
    decision_matrix: pd.DataFrame,
    weights: pd.Series,
    criterion_types: Mapping[str, str],
) -> MCDAResult:
    """Classic TOPSIS with vector normalization."""
    validate_inputs(decision_matrix, weights, criterion_types)
    matrix = decision_matrix.astype(float)
    denom = np.sqrt((matrix ** 2).sum(axis=0))
    if np.isclose(denom, 0).any():
        raise ValueError("TOPSIS vector normalization encountered a zero column norm.")
    normalized = matrix / denom
    weighted = normalized * weights[matrix.columns]

    ideal_best = {}
    ideal_worst = {}
    for col in matrix.columns:
        if criterion_types[col] == "benefit":
            ideal_best[col] = float(weighted[col].max())
            ideal_worst[col] = float(weighted[col].min())
        else:
            ideal_best[col] = float(weighted[col].min())
            ideal_worst[col] = float(weighted[col].max())

    best = pd.Series(ideal_best)
    worst = pd.Series(ideal_worst)
    d_best = np.sqrt(((weighted - best) ** 2).sum(axis=1))
    d_worst = np.sqrt(((weighted - worst) ** 2).sum(axis=1))
    denom_dist = d_best + d_worst
    scores = pd.Series(
        np.where(np.isclose(denom_dist, 0), 0.5, d_worst / denom_dist),
        index=matrix.index,
        dtype=float,
    )
    ranking = scores.sort_values(ascending=False).index.tolist()
    return MCDAResult(scores=scores, ranking=ranking)


def reweight_focus(weights: pd.Series, focus: str, new_weight: float) -> pd.Series:
    """Change one criterion weight and proportionally rescale all others."""
    if focus not in weights.index:
        raise KeyError(focus)
    if not 0 <= new_weight <= 1:
        raise ValueError("new_weight must be in [0,1].")
    other = weights.drop(focus)
    if len(other) == 0:
        return pd.Series({focus: 1.0})
    if np.isclose(float(other.sum()), 0):
        raise ValueError("Cannot rescale zero-weight remainder.")
    result = weights.astype(float).copy()
    result[focus] = float(new_weight)
    result.loc[other.index] = other / other.sum() * (1.0 - new_weight)
    return result


def one_factor_sensitivity(
    decision_matrix: pd.DataFrame,
    weights: pd.Series,
    criterion_types: Mapping[str, str],
    focus: str,
    values: Sequence[float],
) -> pd.DataFrame:
    """Compare WSM and TOPSIS when one criterion weight changes."""
    rows = []
    for value in values:
        w = reweight_focus(weights, focus, float(value))
        wsm = weighted_sum(decision_matrix, w, criterion_types)
        top = topsis(decision_matrix, w, criterion_types)
        rows.append({
            "focus": focus,
            "focus_weight": float(value),
            "wsm_top": wsm.ranking[0],
            "wsm_top_score": float(wsm.scores[wsm.ranking[0]]),
            "topsis_top": top.ranking[0],
            "topsis_top_score": float(top.scores[top.ranking[0]]),
        })
    return pd.DataFrame(rows)


def robustness_analysis(
    decision_matrix: pd.DataFrame,
    weights: pd.Series,
    criterion_types: Mapping[str, str],
    n_runs: int = 3000,
    concentration: float = 80.0,
    seed: int = 2026,
) -> pd.DataFrame:
    """Perturb criterion weights using a Dirichlet distribution.

    The expected sampled weight vector equals the baseline weights.
    Higher concentration => smaller perturbations.
    """
    validate_inputs(decision_matrix, weights, criterion_types)
    if n_runs <= 0:
        raise ValueError("n_runs must be positive.")
    if concentration <= 0:
        raise ValueError("concentration must be positive.")
    if (weights <= 0).any():
        raise ValueError("Dirichlet robustness analysis requires strictly positive weights.")

    rng = np.random.default_rng(seed)
    samples = rng.dirichlet(weights.values * concentration, size=n_runs)
    alternatives = decision_matrix.index.tolist()
    counts = {
        "wsm": {a: 0 for a in alternatives},
        "topsis": {a: 0 for a in alternatives},
    }
    for row in samples:
        w = pd.Series(row, index=weights.index)
        wsm_top = weighted_sum(decision_matrix, w, criterion_types).ranking[0]
        top_top = topsis(decision_matrix, w, criterion_types).ranking[0]
        counts["wsm"][wsm_top] += 1
        counts["topsis"][top_top] += 1

    rows = []
    for method in ["wsm", "topsis"]:
        for alt in alternatives:
            rows.append({
                "method": method,
                "alternative": alt,
                "top_choice_count": counts[method][alt],
                "top_choice_share": counts[method][alt] / n_runs,
            })
    return pd.DataFrame(rows)
