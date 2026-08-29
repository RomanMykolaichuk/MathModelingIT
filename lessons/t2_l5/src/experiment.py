"""Reproducible experiment for T2.L5."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from model import weighted_sum, topsis, one_factor_sensitivity, robustness_analysis


BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
OUT = BASE / "outputs"


def load_inputs():
    alternatives = pd.read_csv(DATA / "alternatives.csv").set_index("alternative")
    criteria = pd.read_csv(DATA / "criteria.csv")
    weights = criteria.set_index("criterion")["weight"].astype(float)
    types = criteria.set_index("criterion")["type"].to_dict()
    return alternatives, weights, types


def main():
    OUT.mkdir(exist_ok=True)
    matrix, weights, types = load_inputs()

    wsm = weighted_sum(matrix, weights, types)
    top = topsis(matrix, weights, types)

    ranking = pd.DataFrame({
        "alternative": matrix.index,
        "wsm_score": wsm.scores.reindex(matrix.index).values,
        "wsm_rank": wsm.scores.rank(ascending=False, method="min").astype(int).reindex(matrix.index).values,
        "topsis_score": top.scores.reindex(matrix.index).values,
        "topsis_rank": top.scores.rank(ascending=False, method="min").astype(int).reindex(matrix.index).values,
    })
    ranking.to_csv(OUT / "baseline_ranking.csv", index=False)

    sensitivity = one_factor_sensitivity(
        matrix, weights, types,
        focus="reliability",
        values=[0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45],
    )
    sensitivity.to_csv(OUT / "sensitivity_reliability.csv", index=False)

    robustness = robustness_analysis(
        matrix, weights, types,
        n_runs=3000, concentration=80.0, seed=2026,
    )
    robustness.to_csv(OUT / "robustness.csv", index=False)

    pivot = ranking.set_index("alternative")[["wsm_score", "topsis_score"]]
    ax = pivot.plot(kind="bar")
    ax.set_title("Порівняння WSM і TOPSIS")
    ax.set_xlabel("Альтернатива")
    ax.set_ylabel("Нормований бал")
    plt.tight_layout()
    plt.savefig(OUT / "baseline_scores.png", dpi=160)
    plt.close()

    print("WSM ranking:", wsm.ranking)
    print("TOPSIS ranking:", top.ranking)
    print(robustness.pivot(index="alternative", columns="method", values="top_choice_share"))


if __name__ == "__main__":
    main()
