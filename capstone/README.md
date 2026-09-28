# підсумковий проєкт — від дослідницького питання до відтворюваного обчислювального висновку

**Статус:** `content_stable`

підсумковий проєкт інтегрує ключові підходи дисципліни в одному мініпроєкт дослідження. Це не дванадцяте заняття, а підсумкова дослідницька робота, у якій ад’юнкт має продемонструвати, що здатний самостійно організувати повний процес обчислювального моделювання.

## Дослідницька логіка

**дослідницьке питання → hypothesis → synthetic observations → mathematical модель → parameter calibration → intervention optimization → незалежна перевірка → чутливість → невизначеність → figures/tables → metadata → scientific conclusion**

## Дослідницьке питання

Як калібрована динамічна модель і оптимізація керованих інтервенцій змінюють прогнозований стан системи за обмеженого бюджету?

## Модель

Використовується абстрактна динамічна модель стану ресурсу/спроможності:

\[
\frac{dS}{dt}=q-kS, \qquad S(0)=S_0,
\]

де `q` — темп поповнення/формування, `k` — інтенсивність втрати/розсіювання, `S(t)` — стан системи.

Після калібрування параметрів вводяться дві керовані інтервенції `u` і `v`:

\[
q_{eff}=q(1+g_q u), \qquad k_{eff}=k(1-g_k v),
\]

за бюджетного обмеження

\[
c_u u + c_v v \le B, \qquad 0\le u,v\le1.
\]

Оптимізаційна задача:

\[
S(T;u,v)\rightarrow\max.
\]

## Що інтегрується з курсу

- формалізація та припущення;
- динамічне математичне моделювання;
- калібрування параметрів через `scipy.optimize.least_squares`;
- нелінійна оптимізація через `SLSQP`;
- незалежна `grid search` перевірка;
- batch чутливість аналіз;
- bootstrap невизначеність;
- `pandas` для таблиць;
- `Matplotlib` для figures;
- deterministic experiment fingerprint;
- дослідження conclusion з чітким розділенням між результатом моделі та твердженням про реальну систему.

## Очікувані контрольні результати

Для наданих synthetic observations оцінки мають знаходитись приблизно в областях:

- `q_hat`: 11–13.5;
- `k_hat`: 0.085–0.12;
- RMSE < 2.5;
- оптимізований terminal state має бути вищим за базовий сценарій;
- SLSQP та grid search повинні давати близькі результати.

Точні числа є наслідком конкретного synthetic dataset і не повинні трактуватись як параметри реальної системи.

## Структура

```text
capstone/
├── README.md
├── CAPSTONE_TASK.md
├── RUBRIC.md
├── RESEARCH_PROTOCOL.md
├── experiment_config.json
├── data/
│   └── observations.csv
├── notebooks/
│   └── capstone_demo.ipynb
├── src/
│   ├── model.py
│   └── experiment.py
├── tests/
│   └── test_capstone.py
└── outputs/
```

## Запуск

```bash
python -m pytest capstone/tests -q
python capstone/src/experiment.py
```

Результати experiment Запускner створює у `capstone/outputs/`:

- `summary.json`;
- `budget_sensitivity.csv`;
- `bootstrap_results.csv`;
- `trajectory_comparison.png`;
- `budget_sensitivity.png`;
- `metadata.json`.

## Ключове правило інтерпретації

**Калібрування + оптимізація + bootstrap підсилюють обґрунтованість computational conclusion, але не перетворюють synthetic модель на емпірично валідовану модель реальної системи.**
