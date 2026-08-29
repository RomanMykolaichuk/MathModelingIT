# Instructor notes — T2.L7

## Роль заняття

Це підсумкове заняття дисципліни. Його завдання — змінити одиницю мислення з «функція/solver/notebook» на **відтворюваний computational research workflow**.

## Головна методична теза

Ад’юнкт має навчитися розрізняти:

1. **model result** — що обчислила модель;
2. **verification result** — чи коректно реалізовано записану модель;
3. **uncertainty result** — наскільки нестійкий прогноз через дані/параметри;
4. **validation claim** — наскільки модель описує реальний об’єкт;
5. **scientific claim** — що допустимо стверджувати у статті або дисертації.

## Рекомендована послідовність

1. Показати research question і hypothesis до коду.
2. Показати noisy observations.
3. Запитати: «Чи можемо ми просто взяти q=12, k=0.1?» — ні, у дослідженні їх треба оцінити.
4. Провести calibration.
5. Побудувати fit.
6. Показати residual/RMSE.
7. Провести independent verification через solve_ivp.
8. Запустити q-sensitivity.
9. Запустити bootstrap.
10. Сформулювати point estimate + interval.
11. Обговорити limitations.
12. Перенести workflow на дисертаційну тему ад’юнкта.

## Контрольні значення

За `synthetic_observations.csv`:

- q_hat ≈ 11.916;
- k_hat ≈ 0.09859;
- RMSE ≈ 1.48;
- threshold time ≈ 9.165;
- S(20) ≈ 106.82;
- bootstrap 95% interval для threshold time ≈ [8.94; 9.53];
- analytical vs solve_ivp error ≈ 1e-9.

## Що обов’язково проговорити

### Calibration ≠ validation

Параметри можуть добре підганяти синтетичні або реальні дані, але це не доводить правильність механізму моделі.

### Verification ≠ validation

Якщо analytical solution і solve_ivp збігаються, це означає, що дві реалізації тієї самої математичної моделі узгоджені.

### Confidence/uncertainty interval ≠ «діапазон істини»

Bootstrap interval залежить від:
- обраної моделі;
- residual resampling scheme;
- обсягу й структури даних;
- fixed assumptions.

### Synthetic data

У занятті дані синтетичні навмисно. Це дозволяє тренувати весь research workflow без підміни навчального результату claims про реальні системи.

## Типові помилки

1. Починати з графіка, не сформулювавши research question.
2. Називати fitted parameters «істинними».
3. Інтерпретувати вузький bootstrap interval як доказ адекватності моделі.
4. Не фіксувати seed/config.
5. Редагувати CSV outputs вручну.
6. Переносити числовий результат у дисертацію без experiment ID.
7. Формулювати висновок ширше, ніж дозволяє модель.

## Питання для дискусії

- Що зміниться, якщо дані мають систематичне, а не випадкове відхилення?
- Чи достатньо одного набору observations для ідентифікації q та k?
- Які параметри вашої дисертаційної моделі можна калібрувати?
- Які джерела uncertainty у вашому дослідженні є найважливішими?
- Який independent verification можливий для вашої моделі?

## Definition of Done

Заняття завершене, коли ад’юнкт може пояснити ланцюг:

**question → hypothesis → data → model → calibration → experiment → verification → uncertainty → sensitivity → evidence → limitations → scientific claim → reproducibility**.
