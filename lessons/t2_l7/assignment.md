# Практичне завдання T2.L7

## Мета

Виконати завершений відтворюваний mini-research experiment за шаблоном заняття.

## Частина A. Research question та hypothesis

1. Сформулюйте дослідницьке питання.
2. Сформулюйте одну перевірювану гіпотезу.
3. Вкажіть, який саме модельний результат може підтримати або послабити цю гіпотезу.

## Частина B. Data and model

1. Завантажте `synthetic_observations.csv`.
2. Опишіть змінні та параметри моделі.
3. Поясніть припущення моделі `dS/dt = q - kS`.
4. Вкажіть, які аспекти реальної системи модель ігнорує.

## Частина C. Calibration

1. Оцініть `q` та `k`.
2. Побудуйте fitted trajectory.
3. Обчисліть RMSE.
4. Поясніть, чому «малий RMSE» не є доказом істинності моделі.

## Частина D. Verification

Порівняйте аналітичну траєкторію з `solve_ivp` та наведіть максимальну абсолютну похибку.

## Частина E. Scenario experiment

Змініть `q` у межах 80–120% від baseline.

Для кожного сценарію обчисліть:
- equilibrium;
- `S(horizon)`;
- time to threshold.

Побудуйте щонайменше один графік.

## Частина F. Uncertainty

Виконайте bootstrap не менше ніж для 300 повторів.

Для `time_to_threshold` наведіть:
- mean;
- median;
- 2.5 percentile;
- 97.5 percentile.

## Частина G. Research conclusion

Підготуйте висновок 250–350 слів, у якому окремо зазначте:
- що показала модель;
- що показав sensitivity analysis;
- що показав bootstrap;
- які твердження допустимі;
- які твердження були б надмірними;
- що потрібно для валідації на реальних даних.

## Частина H. Research transfer

Складіть аналогічний workflow для власної дисертаційної задачі.

## Deliverables

1. Заповнений `practice.ipynb`.
2. Не менше 2 графіків.
3. Таблиця сценаріїв.
4. Bootstrap summary.
5. Research conclusion.
6. Research transfer block.

## Оцінювання

- research question + hypothesis — 15%;
- model/data formalization — 15%;
- calibration — 15%;
- verification — 10%;
- scenario/sensitivity experiment — 15%;
- uncertainty analysis — 15%;
- scientific interpretation and limitations — 10%;
- reproducibility/research transfer — 5%.

**Принцип:** результат без опису assumptions, uncertainty і verification не вважається повним науковим результатом.
