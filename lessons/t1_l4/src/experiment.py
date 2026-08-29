from pathlib import Path
import pandas as pd

from methods import (
    numerical_root,
    symbolic_roots,
    linear_optimization,
    monte_carlo_risk,
    critical_path,
    weighted_sum_decision,
)


def run_all(output_dir: str | Path = "../outputs"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    num_root = numerical_root()
    sym_roots = [float(r.evalf()) for r in symbolic_roots()]
    lp = linear_optimization()
    risk = monte_carlo_risk()
    path, length = critical_path()
    ranking = weighted_sum_decision()

    summary = pd.DataFrame([
        {"case": "A", "method": "numerical root", "tool": "SciPy", "result": num_root},
        {"case": "B", "method": "symbolic", "tool": "SymPy", "result": str(sym_roots)},
        {"case": "C", "method": "linear optimization", "tool": "SciPy linprog", "result": lp["objective"]},
        {"case": "D", "method": "Monte Carlo", "tool": "NumPy", "result": risk},
        {"case": "E", "method": "network", "tool": "NetworkX", "result": f"{path}; length={length}"},
        {"case": "F", "method": "MCDA weighted sum", "tool": "pandas/NumPy", "result": ranking.iloc[0]["alternative"]},
    ])
    summary.to_csv(output_dir / "method_comparison.csv", index=False)
    ranking.to_csv(output_dir / "mcda_ranking.csv", index=False)
    return summary, ranking


if __name__ == "__main__":
    summary, ranking = run_all()
    print(summary.to_string(index=False))
    print("\nMCDA ranking:\n", ranking.to_string(index=False))
