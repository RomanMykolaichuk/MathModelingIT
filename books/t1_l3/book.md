# MathModelingIT MiniBook T1.L3

## Організація математичного моделювання

### Як перетворити код на відтворюваний дослідницький процес

> **Головна ідея книги:** математична модель у науковому дослідженні — це не лише формула й не лише notebook. Це простежуваний workflow, де research question, data, configuration, code, seed, outputs, metadata і Git state дозволяють іншому досліднику відтворити саме той результат, на який ви посилаєтесь у статті чи дисертації.

---

## 0. Паспорт книги

**Код заняття:** T1.L3  
**Тема:** організація математичного моделювання  
**Рівень:** середній  
**Орієнтовний час читання:** 70–85 хвилин  
**Попередні знання:** базова Python-модель, CSV/JSON, поняття random seed, Git на рівні commit.

Після цієї книги ви повинні вміти:

- розділяти research question, data, model, config, code і outputs;
- пояснювати, чому notebook не повинен бути єдиним джерелом логіки;
- виносити parameters experiment у config;
- використовувати seed як частину experiment identity;
- формувати raw results і summary окремо;
- розуміти роль metadata;
- пояснювати config hash;
- відрізняти reproducibility від adequacy;
- пов’язувати result → experiment ID → config/data → Git commit;
- проектувати мінімальний reproducible computational experiment для власного дослідження.

---

## 1. Сцена: «А який саме запуск дав цей рисунок?»

Уявімо звичайну ситуацію під час підготовки дисертації.

У текст вставлено figure.

На ньому п’ять scenarios.

Через пів року керівник запитує:

> «Які parameters використовувалися саме тут?»

Відкривається notebook.

У ньому десятки cells.

Деякі виконані в іншому порядку.

Частина parameters змінювалась вручну.

CSV уже оновлений.

Seed не зафіксовано.

Файл figure називається:

~~~text
plot_final_v2_really_final.png
~~~

І головне питання стає несподівано складним:

> **чи можемо ми точно відтворити той computational result, на який посилається dissertation text?**

Саме це питання є центральним у T1.L3.

<figure>
  <img src="figures/fig_01_reproducibility_chain.svg" alt="Ланцюг від research question до Git">
  <figcaption><strong>Рис. 1.</strong> Відтворюваність виникає з повного ланцюга: question → data → config → model/code → experiment → outputs → metadata → Git state.</figcaption>
</figure>

---

## 2. Reproducibility — властивість workflow

Поширена помилка:

> «У мене є notebook, отже experiment reproducible».

Не обов’язково.

Notebook може містити:

- hidden state;
- cells executed out of order;
- manually changed variables;
- local files;
- undocumented package versions;
- random draws without seed.

Тому reproducibility — це не format.

Це property whole workflow.

---

## 3. Центральна логіка

У lesson зафіксовано:

\[
Research\ question
\rightarrow
Data
\rightarrow
Config
\rightarrow
Model
\rightarrow
Code
\rightarrow
Experiment
\rightarrow
Verification
\rightarrow
Outputs
\rightarrow
Metadata
\rightarrow
Interpretation
\rightarrow
Git.
\]

Кожен елемент має окрему роль.

Якщо все змішано в одному notebook, простежуваність слабшає.

---

## 4. Research question — початок identity

Baseline question:

> Як змінюється очікувана результативність системи при зміні ресурсу або навантаження, і як організувати цей experiment так, щоб його можна було точно повторити?

Це навмисно simple mathematics.

Бо lesson досліджує не складність formula.

Він досліджує **organization of evidence**.

---

## 5. Математична модель

Deterministic part:

\[
Y=
\max(0,\ b+\alpha R-\beta L).
\]

Де:

- \(Y\) — modeled performance;
- \(R\) — resource;
- \(L\) — load;
- \(b\) — baseline level;
- \(\alpha\) — resource gain;
- \(\beta\) — load penalty.

Baseline:

\[
b=20,
\]

\[
\alpha=1.8,
\]

\[
\beta=1.2.
\]

---

## 6. Manual control case

При:

\[
R=40,
\]

\[
L=50
\]

отримуємо:

\[
Y=
20+1.8\cdot40-1.2\cdot50.
\]

\[
Y=20+72-60=32.
\]

Отже:

\[
Y=32.
\]

Це базовий verification case.

Якщо Python не повертає 32, проблема в implementation.

---

## 7. Clipping at zero

Model uses:

\[
Y=\max(0,\cdots).
\]

Тому modeled performance не negative.

Наприклад:

\[
R=0,\quad L=100.
\]

Raw expression:

\[
20-120=-100.
\]

Після clipping:

\[
Y=0.
\]

Це modeling assumption.

Не універсальний mathematical law.

---

## 8. Stochastic observation

Observed result:

\[
Y^{obs}=
\max(0,Y+\varepsilon),
\]

де:

\[
\varepsilon\sim N(0,\sigma^2).
\]

Baseline:

\[
\sigma=4.
\]

Deterministic model defines expected structural response.

Noise models run-to-run variation.

---

## 9. Model vs experiment

Це ключове distinction.

### Model

Form:

\[
Y=\max(0,b+\alpha R-\beta L).
\]

### Experiment

Includes:

- which scenarios;
- how many replications;
- seed;
- noise_sd;
- outputs;
- summary.

Змінити replications:

\[
200\rightarrow1000
\]

— це зміна experiment.

Змінити:

\[
Y=b+\alpha R-\beta L
\]

на nonlinear formula — зміна model.

---

## 10. Config як explicit contract

Baseline experiment_config.json:

~~~json
{
  "seed": 2026,
  "replications": 200,
  "model": {
    "baseline": 20.0,
    "resource_gain": 1.8,
    "load_penalty": 1.2,
    "noise_sd": 4.0
  }
}
~~~

Config робить parameters visible.

<figure>
  <img src="figures/fig_02_config_separation.svg" alt="Розділення model code і config">
  <figcaption><strong>Рис. 2.</strong> Model code визначає mathematical relation, а config — конкретні параметри experiment. Це дозволяє змінювати scenario design без редагування core function.</figcaption>
</figure>

---

## 11. Чому magic numbers небезпечні

Погано:

~~~python
for _ in range(200):
    y = 20 + 1.8*r - 1.2*l
    obs = rng.normal(y, 4)
~~~

Numbers hidden inside code.

Через місяць незрозуміло:

- що 200;
- чому 4;
- чи 1.8 baseline;
- чи цей file used for final result.

Краще:

> parameters live in config.

---

## 12. Scenarios як data

Scenario table:

| scenario | resource | load |
|---|---:|---:|
| baseline | 40 | 50 |
| resource_low | 30 | 50 |
| resource_high | 50 | 50 |
| load_low | 40 | 35 |
| load_high | 40 | 65 |

Scenario definitions зберігаються в CSV.

Це data layer.

---

## 13. Чому scenarios не треба hard-code

Hard-coded:

~~~python
scenarios = [
    ("baseline", 40, 50),
    ...
]
~~~

може працювати.

Але CSV:

- easier audit;
- easier compare;
- easier replace;
- easier version-control diff;
- separates experiment design from algorithm.

---

## 14. Baseline deterministic scenario values

### baseline

\[
R=40,L=50
\]

\[
Y=32.
\]

### resource_low

\[
R=30,L=50
\]

\[
Y=14.
\]

### resource_high

\[
R=50,L=50
\]

\[
Y=50.
\]

### load_low

\[
R=40,L=35
\]

\[
Y=50.
\]

### load_high

\[
R=40,L=65
\]

\[
Y=14.
\]

---

## 15. Однаковий output — різний mechanism

Зверніть увагу:

\[
resource\_high=50,
\]

і:

\[
load\_low=50.
\]

Same deterministic response.

Але first mechanism:

> resource increased.

Second:

> load decreased.

<figure>
  <img src="figures/fig_03_same_output_different_mechanism.svg" alt="Однаковий результат різних сценаріїв">
  <figcaption><strong>Рис. 3.</strong> Однакове числове \(Y=50\) не означає однаковий mechanism. Scenario identity і input values потрібно зберігати разом із result.</figcaption>
</figure>

Це важливий reason not to save only final metric.

---

## 16. Replications

Для кожного scenario:

\[
n=200
\]

stochastic observations.

Якщо scenarios=5:

\[
5\cdot200=1000
\]

raw rows.

Row count — simple sanity check.

---

## 17. Seed як experiment parameter

Baseline:

\[
seed=2026.
\]

run_experiment() creates:

~~~python
rng = np.random.default_rng(2026)
~~~

Same config + same scenarios + same code → same raw results.

Це перевіряється test.

---

## 18. Reproducibility and randomness

Це не contradiction.

Stochastic experiment може бути reproducible, якщо pseudo-random sequence controlled.

Тоді:

> randomness exists inside model, but computational realization is repeatable.

Це fundamental idea scientific computing.

---

## 19. Raw results vs summary

Raw results містять one row per replication.

Наприклад:

- scenario_id;
- resource;
- load;
- replication;
- deterministic_response;
- observed_response.

Summary агрегує.

Це два різні artifacts.

---

## 20. Summary metrics

summarize_results() computes:

- deterministic_response;
- mean_observed;
- std_observed;
- p10;
- p90.

Це scenario-level summary.

<figure>
  <img src="figures/fig_04_raw_to_summary.svg" alt="Від raw results до summary">
  <figcaption><strong>Рис. 4.</strong> Raw data зберігає кожну stochastic replication, summary стискає її до показників. Для відтворюваності бажано мати обидва рівні.</figcaption>
</figure>

---

## 21. Baseline observed means

README gives control values near:

| Scenario | Deterministic | Mean observed |
|---|---:|---:|
| baseline | 32.0 | ≈32.29 |
| resource_low | 14.0 | ≈14.07 |
| resource_high | 50.0 | ≈50.11 |
| load_low | 50.0 | ≈50.16 |
| load_high | 14.0 | ≈13.78 |

Observed means not exactly deterministic values because finite random sample.

But close.

---

## 22. Why p10 and p90

Mean alone hides spread.

p10:

> 10% observations below approximately this value.

p90:

> 90% observations below this value.

Interval:

\[
[p10,p90]
\]

is not a formal confidence interval by default.

It is empirical quantile range.

---

## 23. Metadata

metadata.json includes:

- experiment_id;
- config_hash;
- seed;
- replications;
- scenario_count;
- model parameters;
- workflow note.

Metadata answers:

> what exactly generated these outputs?

---

## 24. Canonical JSON

Hashing must be stable.

If JSON keys are reordered, experiment config meaning unchanged.

Function canonical_json:

- sort_keys=True;
- stable separators.

Then SHA-256.

This supports deterministic identity.

---

## 25. Config hash

\[
h=
SHA256(canonical\ config).
\]

Short form first 12 hex chars.

Baseline:

~~~text
0c5d08ed47eb
~~~

experiment ID:

~~~text
t1_l3_0c5d08ed47eb
~~~

<figure>
  <img src="figures/fig_05_experiment_identity.svg" alt="Experiment ID через config hash">
  <figcaption><strong>Рис. 5.</strong> Config hash створює deterministic identity конфігурації. Але повна reproducibility потребує також code, data і software environment.</figcaption>
</figure>

---

## 26. Що config hash доводить

Він доводить:

> canonical config content same.

Він не доводить:

- code same;
- scenarios CSV same;
- NumPy same;
- model.py same;
- OS/environment same.

Отже, config hash — useful, but partial identity.

---

## 27. Git commit

Git commit identifies code state.

Рекомендований chain:

\[
Result
\rightarrow
ExperimentID
\rightarrow
Config/Data
\rightarrow
GitCommit.
\]

Якщо figure у dissertation has this trace, it can be rebuilt.

---

## 28. Software environment

Навіть same code може behave differently with changed dependencies.

Тому reproducibility package має include:

- Python version;
- requirements;
- package versions.

Current repo pins dependencies.

Це strong foundation.

---

## 29. Verification hierarchy

### Hand calculation

\[
Y(40,50)=32.
\]

### Bounds

\[
Y\ge0.
\]

### Seed reproducibility

Same RNG seed → same observation sequence.

### Row count

\[
n_{rows}=n_{scenarios}\times n_{replications}.
\]

### Config hash stability

Key order does not matter.

### Full run reproducibility

Same inputs produce identical results DataFrame.

---

## 30. Tests are part of research infrastructure

Unit tests not only software engineering.

They capture invariant knowledge.

For T1.L3 tests document:

- baseline equation;
- clipping;
- input validity;
- RNG reproducibility;
- workflow size;
- config identity;
- metadata semantics.

This makes tests executable documentation.

---

## 31. Reproducible wrong model

Important sentence:

> **Відтворюваність неправильного припущення не робить модель адекватною.**

A perfectly reproducible experiment can consistently reproduce wrong assumptions.

Therefore two axes:

- reproducibility;
- validity/adequacy.

---

## 32. Reproducibility vs repeatability vs replicability

Terminology varies across disciplines.

For this course practical meaning:

> another researcher can recreate the same computational result from preserved artifacts.

Do not get lost in terminology.

Focus on traceability.

---

## 33. Notebook role

Notebook is useful for:

- exploration;
- narrative;
- visualization;
- interactive analysis.

But core model logic should live in src/.

Why?

- importable;
- testable;
- reusable;
- easier CI;
- less hidden state.

---

## 34. Hidden state problem

In notebook:

cell 10 may depend on variable changed in cell 3 after cell 7 already ran.

File appears correct.

Kernel state is not.

Strong workflow:

> Restart kernel → Run all → same output.

Even stronger:

> main experiment runs from command line independent of notebook.

---

## 35. Outputs should be generated, not edited

results.csv and summary.csv are derivatives.

Do not manually correct them.

If result wrong:

- fix model/config/data;
- rerun.

Manual editing breaks provenance.

---

## 36. Naming outputs

Avoid:

~~~text
final.csv
final2.csv
really_final.csv
~~~

Better:

- fixed paths inside experiment directory;
- experiment ID directory;
- metadata alongside outputs.

For large research project, experiment_id can name run folder.

---

## 37. Scenario provenance

If scenarios.csv changes, config hash alone does not detect it.

This reveals current limitation.

Possible improvement:

- data file hash;
- combined experiment hash;
- Git commit captures file state.

This is excellent “break the model/workflow” case.

---

## 38. Зламай workflow: same config, changed CSV

Keep:

~~~text
experiment_config.json
~~~

unchanged.

Change resource_high from 50 to 55.

Config hash unchanged.

But experiment changed.

Therefore:

> config_hash ≠ complete experiment hash.

Modernization:

- hash config + input files;
- or rely on Git state + explicit file hashes.

---

## 39. Зламай workflow: same config, changed model.py

Change:

\[
\alpha=1.8
\]

default in code while config still supplies 1.8? No effect.

But change formula itself:

\[
Y=b+\alpha\log(1+R)-\beta L.
\]

Config hash unchanged.

Experiment identity string unchanged.

Result different.

Hence code version must be recorded.

---

## 40. Зламай workflow: unpinned dependencies

Suppose future NumPy behavior changes.

Same code/config may produce different output or warning.

Therefore dependency snapshot matters.

---

## 41. Зламай workflow: seed removed

Without fixed seed:

- raw results change;
- debugging harder;
- figure not exactly reproducible.

Statistical summary may be similar, but exact artifact identity lost.

---

## 42. Зламай workflow: manual figure edits

If figure exported, then manually adjusted data points in image editor, code can no longer reproduce figure.

Allowed manual changes:

- layout;
- labels;
- typography.

Not allowed:

- change values without source update.

---

## 43. Config change vs model change

Change:

\[
noise\_sd=4\rightarrow6.
\]

Experiment config change.

Change:

\[
Y=\max(0,b+\alpha R-\beta L)
\]

to nonlinear relation.

Model change.

These should be reviewed differently.

---

## 44. Sensitivity via scenarios

Scenarios alter inputs:

- resource;
- load.

Config alters global model/experiment parameters:

- replications;
- seed;
- noise_sd.

This separation gives structured design.

---

## 45. Noise_sd experiment

If:

\[
\sigma=4\rightarrow8,
\]

deterministic response unchanged.

Mean observed likely remains around deterministic value in symmetric, non-clipped regions.

Spread increases.

At low deterministic values clipping may affect mean.

This connects T1.L3 with T1.L2 uncertainty concepts.

---

## 46. Replications experiment

Increase:

\[
n=200\rightarrow2000.
\]

Raw summary means often stabilize.

But more runs do not fix wrong model.

Same lesson as Monte Carlo.

---

## 47. Git traceability

A strong report block:

~~~text
experiment_id: t1_l3_0c5d08ed47eb
config_hash: 0c5d08ed47eb
seed: 2026
Git commit: <sha>
input data: data/scenarios.csv
output files:
  - results.csv
  - summary.csv
  - metadata.json
~~~

This is small but powerful.

---

## 48. Figure provenance

<figure>
  <img src="figures/fig_06_figure_provenance.svg" alt="Простежуваність рисунка">
  <figcaption><strong>Рис. 6.</strong> Figure у publication повинна мати шлях назад до output data, experiment ID, config/data та code version.</figcaption>
</figure>

Ideal chain:

\[
Figure
\rightarrow
Summary/RawData
\rightarrow
ExperimentID
\rightarrow
Config
\rightarrow
InputData
\rightarrow
Commit.
\]

---

## 49. Metadata as scientific evidence

Metadata is not decoration.

It allows questions:

- what seed?
- what config?
- how many scenarios?
- which parameters?
- what experiment identity?

Without metadata output file is orphaned.

---

## 50. Reproducibility checklist

Before citing result:

### Research question

Known?

### Data

Stored and documented?

### Model

Formula and assumptions explicit?

### Config

Parameters externalized?

### Execution

One command?

### Verification

Control case?

### Metadata

Experiment ID/hash?

### Git

Code version known?

### Interpretation

No overclaim?

---

## 51. Predict before Run

Before changing config, write:

### If replications ↑

What changes?

### If noise_sd ↑

What changes?

### If seed changes only

What changes?

Expected:

- raw observations change;
- deterministic response unchanged;
- distribution shape similar in aggregate.

---

## 52. Python без страху: deterministic response

~~~python
y = deterministic_response(
    resource=40,
    load=50,
)
assert y == 32
~~~

This is direct verification.

---

## 53. Python без страху: run experiment

~~~python
results = run_experiment(
    config,
    scenarios,
)
~~~

Expected row count:

\[
5\times200=1000.
\]

---

## 54. Python без страху: summary

~~~python
summary = summarize_results(results)
~~~

Output includes:

- deterministic;
- mean;
- std;
- p10;
- p90.

---

## 55. Python без страху: config hash

~~~python
experiment_id = (
    "t1_l3_" + config_hash(config)
)
~~~

Baseline:

~~~text
t1_l3_0c5d08ed47eb
~~~

---

## 56. Why hash key order stable

Config:

~~~json
{"seed":2026,"replications":200}
~~~

and:

~~~json
{"replications":200,"seed":2026}
~~~

same semantic mapping.

canonical_json sorts keys.

Thus same hash.

This is unit-tested.

---

## 57. Synthetic military context

Suppose \(Y\) is synthetic performance indicator of training-support process.

\(R\) — conditional resource.

\(L\) — conditional workload.

No real unit, no actual operational performance.

The case demonstrates workflow, not real decision recommendation.

---

## 58. Research Transfer

Question:

> Як організувати computational experiment для одного fragment власної dissertation?

Template:

~~~text
Research question:

Input data:

Data provenance:

Mathematical model:

Config parameters:

Scenario file:

Random seed:

Replications:

Verification case:

Raw outputs:

Summary outputs:

Metadata:

Experiment ID:

Git commit:

Software environment:

Limitations:

Allowed conclusion:
~~~

---

## 59. Example transfer: model calibration workflow

Imagine dissertation model estimates parameter from synthetic data.

Reproducible workflow:

1. raw data file;
2. preprocessing script;
3. calibration config;
4. seed;
5. fitted parameters;
6. diagnostic plots;
7. metadata;
8. commit;
9. result table.

T1.L3 structure transfers directly.

---

## 60. Versioning data

Git works well for small text CSV.

Large or sensitive data may need:

- data registry;
- object storage;
- checksum;
- access-controlled repository.

Important principle remains:

> result must reference exact data version.

---

## 61. Sensitive/closed data

In military research, data may not be publishable.

Reproducibility still possible inside controlled environment.

Preserve:

- data version ID;
- hash;
- schema;
- access conditions;
- code/config.

Public artifact can use synthetic equivalent while documenting difference.

---

## 62. Environment snapshot

Requirements file gives dependency versions.

For stronger reproducibility also record:

- Python version;
- OS/container image;
- hardware if relevant;
- CUDA/GPU for stochastic/numerical workloads where results depend on backend.

Not every experiment needs all details.

Record what can materially change results.

---

## 63. Deterministic outputs are not automatically reproducible

Even deterministic formula can fail reproducibility if:

- data changed;
- code changed;
- config unknown;
- preprocessing hidden.

Randomness is not the only threat.

---

## 64. Reproducibility levels

### Level 0

Screenshot only.

### Level 1

Notebook + data.

### Level 2

src + config + data + seed.

### Level 3

tests + metadata + Git commit.

### Level 4

environment + automated pipeline/CI.

Course aims toward Level 3–4.

<figure>
  <img src="figures/fig_07_reproducibility_levels.svg" alt="Рівні відтворюваності">
  <figcaption><strong>Рис. 7.</strong> Reproducibility посилюється шарами: artifact → code/data → config/seed → tests/metadata/Git → automated environment.</figcaption>
</figure>

---

## 65. CI as reproducibility assistant

Course CI executes tests and notebooks.

It cannot prove research validity.

But it can detect:

- broken imports;
- changed control values;
- missing files;
- non-executable notebook.

Automation reduces accidental drift.

---

## 66. Зламай систему: result without identity

Suppose summary.csv says:

~~~text
baseline mean_observed=32.29
~~~

but no config/hash/commit.

Can we use number?

We can read it.

Can we defend its provenance?

Weakly.

Thus result without identity is scientifically fragile.

---

## 67. Typical thinking errors

### «Якщо код є, результат reproducible»

Not enough.

### «Same config hash = same experiment»

Not if data/code differ.

### «Git replaces metadata»

No.

Git identifies repository state, metadata identifies run.

### «Seed makes stochastic conclusion true»

No.

Seed makes run repeatable.

### «Reproducible = valid»

No.

Wrong model can reproduce perfectly.

---

## 68. Model audit vs workflow audit

### Model audit

- formula;
- assumptions;
- parameters;
- adequacy.

### Workflow audit

- files;
- config;
- execution;
- metadata;
- versioning.

Strong dissertation computational work needs both.

---

## 69. One-command principle

A good experiment should have a clear command:

~~~bash
python -m lessons.t1_l3.src.experiment
~~~

This reduces hidden manual steps.

If full rebuild requires 17 undocumented clicks, reproducibility suffers.

---

## 70. Immutable raw inputs

Ideally raw input is not overwritten by experiment.

Derived data goes to outputs.

This preserves source.

For transformations, save script and intermediate if scientifically relevant.

---

## 71. Output overwrite issue

Current lesson writes fixed outputs directory.

For teaching this is simple.

For research scale, overwriting old experiment may be undesirable.

Modernization:

~~~text
outputs/<experiment_id>/
~~~

or timestamp + hash.

Then runs coexist.

---

## 72. Experiment registry

A small CSV/JSON index can contain:

- experiment_id;
- date;
- commit;
- config;
- note;
- status.

This helps large dissertation projects.

Not required baseline, but natural extension.

---

## 73. Allowed conclusion

Strong:

> For config hash 0c5d08ed47eb, seed 2026 and five scenarios with 200 replications each, baseline deterministic response is 32 and mean observed is approximately 32.29. The result is reproducible for the same code, config, scenario data and software environment.

Also state:

> This does not validate linear resource/load assumptions.

---

## 74. Від MiniBook до practice

Before practical:

1. run baseline;
2. record experiment_id;
3. verify Y=32;
4. rerun and compare results;
5. change only seed;
6. change config;
7. add scenarios;
8. record Git commit.

---

## 75. Research artifact passport

Create for each important result:

~~~text
Result:
Research question:
Experiment ID:
Config hash:
Input data:
Model version:
Seed:
Replications:
Git commit:
Environment:
Verification:
Limitations:
Publication use:
~~~

This is practical dissertation discipline.

---

## 76. Workflow architecture

<figure>
  <img src="figures/fig_08_project_architecture.svg" alt="Архітектура reproducible project">
  <figcaption><strong>Рис. 8.</strong> Хороша структура розділяє source code, inputs, config, notebooks і generated outputs. Кожен шар має власну responsibility.</figcaption>
</figure>

Recommended:

~~~text
data/
config
src/
tests/
notebooks/
outputs/
metadata
README
Git
~~~

---

## Поглиблення: reproducibility має кілька рівнів identity

У baseline experiment_id залежить від config.

Але повний computational result depends on broader state.

Корисно мислити шарами.

### Config identity

\[
ID_{config}=Hash(config).
\]

### Data identity

\[
ID_{data}=Hash(input\ files).
\]

### Code identity

Git commit:

\[
ID_{code}=commit\ SHA.
\]

### Environment identity

Dependency lock / container digest.

### Run identity

Може комбінувати:

\[
ID_{run}
=
f(
ID_{config},
ID_{data},
ID_{code},
ID_{env}
).
\]

Course implementation intentionally simpler.

Але ця hierarchy показує шлях розвитку dissertation infrastructure.

---

## Поглиблення: why Git commit alone is not enough

Git commit tells exact repository state only if:

- all relevant files tracked;
- no uncommitted changes;
- external data version known;
- environment known.

If local script modified but not committed, commit SHA points to another state.

Therefore a publication run should ideally start from a clean working tree.

If not, this is a reproducibility limitation.

---

## Поглиблення: dirty working tree

Imagine:

- commit = abc123;
- model.py edited locally;
- experiment run;
- change not committed.

Metadata records abc123.

Later checkout abc123 gives old model.

Result cannot be reproduced exactly.

Possible improvement:

- refuse publication run when repo dirty;
- record diff;
- auto-capture patch.

For course, awareness is enough.

---

## Поглиблення: input data hashing

Config hash protects config.

Add:

\[
h_{data}=SHA256(file\ bytes).
\]

Then metadata can include a scenario-data checksum.

Now scenario change detectable even if filename same.

This directly fixes one break-the-workflow case.

---

## Поглиблення: code version in metadata

Current metadata note says reproducible for same code/config/data/environment.

A stronger implementation could automatically query the Git commit and store it.

If Git unavailable, metadata should state:

~~~text
git_commit: unavailable
~~~

rather than invent certainty.

---

## Поглиблення: dependency snapshot

Pinned requirements in repository help.

But installed environment can still differ if user ignores them.

A run can record:

~~~text
python --version
pip freeze
~~~

or selected critical versions.

For scientific work useful fields include:

- Python;
- NumPy;
- pandas;
- SciPy;
- SymPy;
- Matplotlib.

For GPU workflows also backend versions.

---

## Поглиблення: environment reproducibility vs portability

Exact environment replication is strong but can become brittle over years.

Alternative goal:

> portable reproducibility.

That means code works under a documented version range, with tests verifying outputs/tolerances.

There is a trade-off between freezing everything exactly and maintaining a portable tested package.

Course chooses pinned stack for educational stability.

---

## Поглиблення: raw data should be immutable

A strong rule:

> raw input is never overwritten by experiment.

Why?

If the same file is modified in-place, historical result loses source.

Prefer:

~~~text
data/raw/
data/processed/
outputs/
~~~

Transformation script creates processed data from raw.

Then provenance is explicit.

---

## Поглиблення: preprocessing is part of model pipeline

Researchers sometimes think:

> preprocessing is just preparation.

But filtering, imputation, normalization and aggregation can change results.

Therefore preprocessing code belongs in reproducibility chain.

If a CSV is manually cleaned in a spreadsheet and overwritten, provenance weakens.

---

## Поглиблення: experiment config schema

JSON config is useful, but can contain invalid types.

For larger project define schema:

- required keys;
- type constraints;
- allowed ranges;
- defaults.

Current validate_config checks:

- seed;
- replications;
- model;
- positive replications;
- nonnegative noise_sd.

This is first step toward schema validation.

---

## Поглиблення: why explicit validation matters

Without validation a negative replication count or negative noise value could fail strangely later.

Validation creates early, meaningful error.

This is part of scientific quality.

Bad inputs should be rejected before expensive computation.

---

## Поглиблення: output determinism

For same config/data/code/seed baseline raw DataFrame should be identical.

Test:

~~~python
pd.testing.assert_frame_equal(a, b)
~~~

This is stronger than saying that means are close.

It checks exact computational repeatability.

For some parallel/GPU workflows bitwise identity may not be realistic.

Then reproducibility criterion must use tolerances.

---

## Поглиблення: exact vs statistical reproducibility

### Exact

Same raw numbers.

Appropriate for this CPU pseudo-random workflow.

### Numerical

Differences within tolerance.

Common for floating-point solvers.

### Statistical

Different draws but same distribution-level conclusions.

Common for stochastic HPC.

Before claiming reproducibility define which level intended.

---

## Поглиблення: experiment registry design

When dissertation has many runs, one metadata file per output directory is not enough for overview.

Create registry:

| experiment_id | commit | config | data | purpose | status |
|---|---|---|---|---|---|
| exp001 | abc | cfg1 | d1 | baseline | accepted |
| exp002 | def | cfg2 | d1 | sensitivity | exploratory |

This prevents “which run was final?” confusion.

---

## Поглиблення: exploratory vs confirmatory runs

During exploration researcher tries many configs.

Later select analysis plan.

It is useful to mark:

- exploratory;
- validation;
- final/publication.

Otherwise result selection can be opaque.

Metadata can include purpose tag.

---

## Поглиблення: publication artifact mapping

Suppose dissertation contains:

- Table 3.2;
- Figure 3.4;
- metric in paragraph.

Create mapping:

~~~text
Figure 3.4 -> experiment_id X -> script Y -> output Z
Table 3.2  -> experiment_id Q -> summary.csv
~~~

Then revision becomes manageable.

---

## Поглиблення: one source of truth for figures

Do not copy values manually from terminal into Excel, then chart.

Better:

\[
data
\rightarrow
script
\rightarrow
figure.
\]

If style adjustment needed, script controls it.

This keeps numbers linked to computation.

---

## Поглиблення: checksums for publication artifacts

For final figure or table, optional checksum can prove file identity.

For example:

\[
SHA256(figure.png).
\]

This may be overkill for classroom use.

But useful in audited pipelines.

---

## Поглиблення: reproducibility under closed-data constraints

Military and defence research may have data that cannot leave secure environment.

Reproducibility can still be designed.

Inside secure network preserve:

- exact raw data;
- version/hash;
- scripts;
- config;
- environment;
- outputs;
- access rules.

Outside secure network publish:

- synthetic dataset;
- schema;
- method;
- limitations.

Do not confuse public reproducibility with internal reproducibility.

---

## Поглиблення: synthetic twin dataset

A useful pattern:

1. confidential real dataset used in secure analysis;
2. synthetic dataset preserves structure, not sensitive values;
3. public repo demonstrates workflow;
4. secure metadata links internal result to real data version.

This supports teaching and method transparency without disclosing sensitive content.

---

## Поглиблення: provenance graph

Conceptually provenance forms graph:

\[
Data
\rightarrow
Experiment
\rightarrow
Output
\rightarrow
Publication.
\]

And:

\[
Code+Config
\rightarrow
Experiment.
\]

Metadata stores the edges.

This graph is a useful mental model for dissertation computational work.

---

## Поглиблення: why notebook outputs should not be trusted blindly

Notebook cell can display result from old kernel state even if code cell later edited.

Therefore final notebook should be:

1. restart kernel;
2. run all;
3. verify no error;
4. compare key outputs;
5. save executed version.

Course smoke execution supports this discipline.

---

## Поглиблення: CI is not a substitute for local provenance

CI says repository version passes checks.

But if publication result was produced locally with uncommitted changes, CI cannot know.

Thus CI and metadata complement each other.

---

## Поглиблення: failure recovery

Reproducible workflow also helps when experiment fails.

If run produces unexpected result, compare:

- config diff;
- data diff;
- commit diff;
- dependency diff.

Without provenance troubleshooting becomes guessing.

---

## Поглиблення: experiment comparison

Two experiments should be compared by explicit differences.

Example:

~~~text
A: seed=2026, noise_sd=4, reps=200
B: seed=2026, noise_sd=8, reps=200
~~~

Then causal interpretation is clearer because only one factor changed.

If many parameters change simultaneously, attribution weakens.

This is computational experimental design.

---

## Поглиблення: controlled change principle

One-factor change is not always scientifically sufficient, but pedagogically useful.

It allows:

\[
\Delta output
\]

to be associated with one parameter change.

For complex interactions use factorial or scenario designs.

The key is explicit design.

---

## Поглиблення: metadata should describe purpose, not only mechanics

Technical metadata:

- seed;
- hash;
- versions.

Scientific metadata:

- research question;
- scenario meaning;
- expected effect;
- acceptance criterion.

Both matter.

A perfectly identified run with unknown purpose is still hard to interpret.

---

## Поглиблення: reproducibility debt

Just as software has technical debt, research can accumulate reproducibility debt.

Examples:

- unnamed files;
- manual changes;
- missing seeds;
- undocumented configs;
- screenshots without source;
- notebooks with hidden state.

Debt grows with time.

T1.L3 aims to prevent it early in PhD workflow.

---

## Поглиблення: minimum viable reproducibility package

If time limited, preserve at least:

1. README command;
2. code;
3. input data;
4. config;
5. seed;
6. tests;
7. metadata;
8. commit SHA;
9. dependency file.

This small package gives large benefit.

---

## 77. Одна сторінка підсумку

### П’ять головних ідей

1. Reproducibility is workflow property.
2. Model and experiment configuration are different.
3. Seed, data, config and code version all matter.
4. Metadata gives run identity.
5. Reproducibility does not prove adequacy.

### Три правила

Manual baseline:

\[
Y=20+1.8R-1.2L.
\]

Observed:

\[
Y^{obs}=\max(0,Y+\varepsilon).
\]

Experiment identity:

\[
ID=f(Hash(config)).
\]

### Дві помилки

- config hash alone = full experiment identity;
- notebook exists = reproducible.

### Одне питання

> Чи можу я через шість місяців перебудувати конкретний figure із dissertation без ручного guessing?

### Наступний крок

Run baseline twice, change only seed, then document experiment ID and commit.

---

## 78. Фінальна думка

Складна математика не рятує слабко організований experiment.

І навпаки — навіть проста model може стати сильним research artifact, якщо:

- inputs explicit;
- config external;
- randomness controlled;
- verification present;
- outputs generated;
- metadata saved;
- code version known.

Тому T1.L3 навчає не «як написати ще один Python script».

Він навчає:

> **як зробити так, щоб computational result мав історію походження, яку можна перевірити, повторити й захистити.**
