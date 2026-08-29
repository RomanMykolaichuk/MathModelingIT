from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from model import cpm_schedule, apply_delay, pert_parameters, monte_carlo_project, deadline_probability

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
OUTPUTS.mkdir(exist_ok=True)

tasks = pd.read_csv(DATA / "tasks.csv")
pert = pd.read_csv(DATA / "pert.csv")

project_duration, schedule, critical_path = cpm_schedule(tasks)
schedule.to_csv(OUTPUTS / "cpm_schedule.csv", index=False)

delayed = apply_delay(tasks, "C", 3)
delay_duration, delay_schedule, delay_path = cpm_schedule(delayed)
delay_schedule.to_csv(OUTPUTS / "delay_scenario.csv", index=False)

pert_parameters(pert).to_csv(OUTPUTS / "pert_parameters.csv", index=False)

mc, critical_freq = monte_carlo_project(tasks, pert, n=3000, seed=2026)
mc.to_csv(OUTPUTS / "monte_carlo_results.csv", index=False)
critical_freq.to_csv(OUTPUTS / "critical_path_frequency.csv", index=False)

summary = pd.DataFrame([{
    "baseline_duration": project_duration,
    "baseline_critical_path": " -> ".join(critical_path),
    "delay_duration": delay_duration,
    "delay_critical_path": " -> ".join(delay_path),
    "mc_mean_duration": mc["project_duration"].mean(),
    "mc_p90_duration": mc["project_duration"].quantile(0.90),
    "probability_finish_by_19": deadline_probability(mc, 19.0),
}])
summary.to_csv(OUTPUTS / "summary.csv", index=False)

plt.figure(figsize=(8,5))
plt.hist(mc["project_duration"], bins=30)
plt.axvline(19, linestyle="--", label="Deadline = 19")
plt.xlabel("Project duration")
plt.ylabel("Simulation count")
plt.title("Monte Carlo distribution of project duration")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUTS / "project_duration_distribution.png", dpi=160)
plt.close()

print(summary.to_string(index=False))
