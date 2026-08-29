# T2.L7. Використання систем комп’ютерної математики в наукових дослідженнях

**Статус:** CONTENT STABLE  
**Аудиторія:** ад’юнкти  
**Тип заняття:** інтеграційне mini-research project

## Мета

Сформувати вміння використовувати системи комп’ютерної математики як середовище повного наукового дослідження: від дослідницького питання й гіпотези до калібрування моделі, обчислювального експерименту, оцінювання невизначеності, верифікації, візуалізації та відтворюваного наукового висновку.

## Навчальні питання

1. **Організація повного computational research workflow із використанням Python та систем комп’ютерної математики.**
2. **Калібрування, верифікація, аналіз чутливості та невизначеності математичної моделі у науковому дослідженні.**

## Дослідницьке питання

Наскільки надійно за шумними спостереженнями можна оцінити параметри динамічної системи та спрогнозувати час досягнення заданого порогу?

## Робоча гіпотеза

Калібрована модель відновить параметри з малою похибкою, а bootstrap покаже вузький, але ненульовий інтервал невизначеності прогнозу.

## Математична модель

Розглядається узагальнена динамічна модель стану обмеженого ресурсу:

\[
\frac{dS}{dt}=q-kS,
\]

де:
- \(S(t)\) — стан системи;
- \(q\) — інтенсивність поповнення;
- \(k\) — коефіцієнт втрати/витрачання;
- \(S(0)=S_0\).

Аналітичний розв’язок:

\[
S(t)=\frac{q}{k}+\left(S_0-\frac{q}{k}\right)e^{-kt}.
\]

## Research workflow

```text
research question
    ↓
hypothesis
    ↓
synthetic observations
    ↓
model specification
    ↓
parameter calibration
    ↓
analytical prediction
    ↓
independent numerical verification
    ↓
batch scenarios
    ↓
bootstrap uncertainty
    ↓
sensitivity analysis
    ↓
figures + tables + metadata
    ↓
research conclusion
```

## Дані

`data/synthetic_observations.csv` містить синтетичні спостереження стану системи на часових точках 0–20. Дані спеціально містять шум, тому параметри не можна просто «прочитати» з таблиці.

## Калібрування

Параметри \(q\) та \(k\) оцінюються методом нелінійних найменших квадратів (`scipy.optimize.least_squares`).

Контрольний baseline:

- \(\hat q \approx 11.916\);
- \(\hat k \approx 0.09859\);
- RMSE \(\approx 1.48\).

## Прогноз

Для порогу \(S=80\):

- point estimate часу досягнення порогу ≈ **9.165**;
- bootstrap 95% interval ≈ **[8.94; 9.53]**.

Для горизонту \(t=20\):

- прогнозований стан ≈ **106.82**.

## Verification

Аналітична траєкторія незалежно перевіряється через `scipy.integrate.solve_ivp`.

Очікувана максимальна абсолютна різниця — близько \(10^{-9}\).

> Збіг двох реалізацій підтверджує узгодженість обчислень, але не доводить адекватність моделі реальному об’єкту.

## Sensitivity analysis

Параметр \(q\) змінюється в діапазоні 80–120% від каліброваного значення. Аналізується:
- стан на горизонті;
- час досягнення порогу;
- нелінійність реакції системи.

## Uncertainty analysis

Bootstrap використовується для повторної калібрації на ресемпльованих залишках. Це дає розподіл:
- \(\hat q\);
- \(\hat k\);
- часу досягнення порогу;
- прогнозу \(S(20)\).

## Відтворюваність

`experiment_config.json` фіксує:
- дослідницьке питання;
- гіпотезу;
- стартовий стан;
- threshold;
- horizon;
- сценарії;
- кількість bootstrap replications;
- random seed.

`src/experiment.py` автоматично створює:
- `calibration_summary.csv`;
- `scenario_results.csv`;
- `bootstrap_predictions.csv`;
- `summary.csv`;
- `metadata.json`;
- `calibration_fit.png`;
- `sensitivity.png`;
- `bootstrap_threshold.png`.

Для однакових `data + config + model` формується deterministic `experiment_id`.

## Структура

```text
lessons/t2_l7/
├── README.md
├── experiment_config.json
├── data/
│   └── synthetic_observations.csv
├── notebooks/
│   ├── demo.ipynb
│   └── practice.ipynb
├── src/
│   ├── __init__.py
│   ├── model.py
│   └── experiment.py
├── tests/
│   └── test_model.py
├── outputs/
│   └── .gitkeep
├── assignment.md
└── instructor_notes.md
```

## Запуск

```bash
python lessons/t2_l7/src/experiment.py
pytest lessons/t2_l7/tests -q
```

## Критерій завершення заняття

Ад’юнкт має вміти відповісти не тільки на питання «який результат дала модель?», а й:

1. яке дослідницьке питання перевірялось;
2. які параметри оцінювались;
3. як перевірялась реалізація;
4. яка невизначеність прогнозу;
5. наскільки результат чутливий до параметрів;
6. які обмеження має модель;
7. як відтворити експеримент;
8. який обережний науковий висновок можна сформулювати.

## Research transfer

Фінальний блок заняття вимагає перенести workflow на власну дисертаційну тему:

**Research question → mathematical model → data → calibration/parameter choice → computational experiment → uncertainty/sensitivity → verification → reproducible evidence → scientific claim.**
