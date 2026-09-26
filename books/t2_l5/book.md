# MathModelingIT MiniBook T2.L5

## Засоби розв’язування задач множинного вибору

### Як обирати між альтернативами, не перетворюючи ваги на магію

> **Головна ідея книги:** багатокритеріальний вибір не відповідає на питання «що найкраще взагалі». Він формалізує умови, за яких певна альтернатива стає кращою за інші: за заданих критеріїв, типів benefit/cost, ваг, методу нормалізації та способу агрегування. Тому хороший результат MCDA — не лише ranking, а пояснення його стійкості й меж застосовності.

---

## 0. Паспорт книги

**Код заняття:** T2.L5  
**Тема:** засоби розв’язування задач множинного вибору  
**Рівень:** середній  
**Орієнтовний час читання:** 65–80 хвилин  
**Попередні знання:** базова алгебра, таблиці, відсотки, поняття середнього; програмування не обов’язкове.

Після цієї книги ви повинні вміти:

- формулювати задачу вибору через alternatives, criteria, weights;
- розрізняти benefit і cost критерії;
- пояснювати, навіщо потрібна нормалізація;
- обчислювати і тлумачити WSM;
- пояснювати інтуїцію TOPSIS;
- розуміти, чому два методи можуть дати різний ranking;
- проводити one-factor sensitivity;
- пояснювати robustness analysis для невизначених ваг;
- не робити висновок «об’єктивно найкраща альтернатива»;
- знаходити помилки типу «cost як benefit»;
- переносити MCDA на власну дослідницьку задачу.

**Після книги:** відкрийте Lab T2.L5, змініть вагу reliability, порівняйте WSM/TOPSIS і сформулюйте умовний висновок.

---

## 1. Сцена: «Який варіант кращий?»

Уявімо синтетичний навчальний сценарій.

Група планування має обрати один із чотирьох технічних варіантів — A, B, C або D — для підтримки навчального процесу. Ми навмисно не прив’язуємо приклад до реальних систем чи бойових спроможностей.

Кожен варіант має переваги й недоліки.

Один дешевший.

Інший швидше розгортається.

Третій надійніший.

Четвертий має більшу умовну capacity.

Ще є risk.

На нараді хтось запитує:

> «То який варіант найкращий?»

Це звучить природно, але математично питання неповне.

Найкращий **за яким критерієм**?

Що важливіше: cost чи reliability?

Наскільки важливіше?

Чи вважаємо time витратним критерієм, де менше краще?

Що буде, якщо ваги трохи зміняться?

Чи дасть інший MCDA method той самий ranking?

Тому коректне дослідницьке питання:

> **Як змінюється ranking альтернатив залежно від структури критеріїв, їхніх типів, ваг і методу агрегування, та наскільки стійким є висновок про перше місце?**

Саме з цього починається багатокритеріальне моделювання.

<figure>
  <img src="figures/fig_01_decision_problem.svg" alt="Від суб’єктивного вибору до формальної MCDA моделі">
  <figcaption><strong>Рис. 1.</strong> MCDA перетворює нечітке «що краще?» на явну систему: alternatives → criteria → criterion types → weights → method → ranking → sensitivity → conditional conclusion.</figcaption>
</figure>

---

## 2. Чому одного критерію недостатньо

Якби нас цікавила лише ціна, задача була б простою:

> обрати найменший cost.

Якби тільки reliability:

> обрати найбільшу reliability.

Але реальні рішення майже завжди багатокритеріальні.

У нашій synthetic decision matrix:

| Alternative | cost | time | reliability | capacity | risk |
|---|---:|---:|---:|---:|---:|
| A | 82 | 18 | 0.92 | 75 | 0.18 |
| B | 70 | 22 | 0.88 | 90 | 0.25 |
| C | 92 | 15 | 0.96 | 80 | 0.12 |
| D | 76 | 20 | 0.90 | 85 | 0.20 |

Жодна альтернатива не домінує очевидно за всім.

B найдешевша й має найвищу capacity, але гірша за reliability, time та risk.

C найдорожча, зате має найкращий time, reliability і risk.

D — компроміс.

A — теж має власний профіль.

Отже, рішення потребує **правила компромісу**.

---

## 3. Формальна постановка

Нехай:

- \(A_i\) — альтернативи;
- \(C_j\) — критерії;
- \(x_{ij}\) — оцінка альтернативи \(i\) за критерієм \(j\);
- \(w_j\) — вага критерію.

Ваги задовольняють:

\[
w_j\ge0,
\]

\[
\sum_j w_j=1.
\]

У baseline:

\[
w_{cost}=0.25,
\]

\[
w_{time}=0.20,
\]

\[
w_{reliability}=0.25,
\]

\[
w_{capacity}=0.20,
\]

\[
w_{risk}=0.10.
\]

Сама сума 1 не робить ваги «правильними».

Вона лише робить їх нормованими.

Правильність або обґрунтованість ваг — предметне питання.

---

## 4. Benefit і cost: напрям має значення

Критерії бувають різного типу.

### Benefit

Більше = краще.

У baseline:

- reliability;
- capacity.

### Cost

Менше = краще.

У baseline:

- cost;
- time;
- risk.

Це принципово.

Якщо cost помилково трактувати як benefit, модель почне винагороджувати дорожчі альтернативи.

Математично все може обчислитися без помилки.

Предметно результат буде абсурдним.

> **Тип критерію — це частина моделі, а не косметична мітка.**

---

## 5. Чому не можна просто скласти сирі значення

У таблиці критерії мають різні шкали.

Наприклад:

- cost: десятки;
- time: десятки;
- reliability: близько 1;
- capacity: десятки;
- risk: дробові значення.

Якщо написати:

\[
82+18+0.92+75+0.18,
\]

ми змішаємо величини різної природи.

Більші числові шкали почнуть домінувати лише через одиниці вимірювання.

Тому перед агрегуванням потрібна **нормалізація**.

---

## 6. Min-max normalization для WSM

Для benefit-критерію:

\[
r_{ij}=
\frac{x_{ij}-\min_i x_{ij}}
{\max_i x_{ij}-\min_i x_{ij}}.
\]

Для cost-критерію:

\[
r_{ij}=
\frac{\max_i x_{ij}-x_{ij}}
{\max_i x_{ij}-\min_i x_{ij}}.
\]

Після цього:

\[
0\le r_{ij}\le1,
\]

і в усіх критеріях:

> більше = краще.

Це дуже зручно.

<figure>
  <img src="figures/fig_02_normalization.svg" alt="Benefit і cost нормалізація">
  <figcaption><strong>Рис. 2.</strong> Нормалізація переводить різні шкали у спільну [0,1]. Для benefit більші raw values стають кращими; для cost напрям інвертується.</figcaption>
</figure>

---

## 7. Приклад: cost

Raw cost:

- A = 82;
- B = 70;
- C = 92;
- D = 76.

Мінімум:

\[
70.
\]

Максимум:

\[
92.
\]

Оскільки cost — cost criterion:

\[
r_{A,cost}=
\frac{92-82}{92-70}
=
\frac{10}{22}
\approx0.455.
\]

Для B:

\[
r_{B,cost}=1.
\]

Для C:

\[
r_{C,cost}=0.
\]

Тобто найдешевша альтернатива отримала 1, найдорожча — 0.

Це відповідає логіці критерію.

---

## 8. Приклад: reliability

Raw reliability:

- A = 0.92;
- B = 0.88;
- C = 0.96;
- D = 0.90.

Оскільки reliability — benefit:

\[
r_{A,reliability}
=
\frac{0.92-0.88}{0.96-0.88}
=
0.5.
\]

Для C:

\[
r_{C,reliability}=1.
\]

Для B:

\[
r_{B,reliability}=0.
\]

Знову отримуємо шкалу, де 1 означає краще відносне положення серед розглянутих альтернатив.

---

## 9. Нормалізована baseline matrix

Для нашого набору:

| Alt | cost | time | reliability | capacity | risk |
|---|---:|---:|---:|---:|---:|
| A | 0.455 | 0.571 | 0.500 | 0.000 | 0.538 |
| B | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| C | 0.000 | 1.000 | 1.000 | 0.333 | 1.000 |
| D | 0.727 | 0.286 | 0.250 | 0.667 | 0.385 |

Тепер критерії можна агрегувати.

Але навіть після нормалізації постає нове питання:

> яким способом?

---

## 10. Weighted Sum Model

WSM — найпростіший спосіб.

Для альтернативи \(i\):

\[
S_i=\sum_j w_j r_{ij}.
\]

Інтуїтивно:

1. нормалізуємо;
2. множимо кожен критерій на його вагу;
3. складаємо;
4. більше \(S_i\) → вище ranking.

Це **лінійна компенсаторна модель**.

Сильний результат за одним критерієм може компенсувати слабкий за іншим.

---

## 11. WSM baseline для C

Для C:

\[
r_C=
(0,\ 1,\ 1,\ 0.333,\ 1).
\]

Ваги:

\[
w=
(0.25,\ 0.20,\ 0.25,\ 0.20,\ 0.10).
\]

Отже:

\[
S_C=
0\cdot0.25+
1\cdot0.20+
1\cdot0.25+
0.333\cdot0.20+
1\cdot0.10.
\]

\[
S_C\approx0.6167.
\]

Baseline ranking WSM:

\[
C>D>B>A.
\]

Точні scores:

- C ≈ 0.6167;
- D ≈ 0.4733;
- B = 0.4500;
- A ≈ 0.4068.

<figure>
  <img src="figures/fig_03_wsm_contributions.svg" alt="Внески критеріїв у WSM score">
  <figcaption><strong>Рис. 3.</strong> WSM score є сумою зважених нормалізованих внесків. Один високий criterion value може компенсувати інший низький.</figcaption>
</figure>

---

## 12. Що означає «компенсаторна модель»

Припустимо, альтернатива має високу reliability, але поганий cost.

WSM дозволяє високій reliability частково компенсувати cost.

Це не помилка.

Це **вбудована логіка методу**.

Але іноді предметна задача не дозволяє таку компенсацію.

Наприклад, може існувати hard constraint:

> risk не повинен перевищувати певного порога незалежно від інших переваг.

Тоді простий WSM без constraint може бути непридатним.

Отже, перед вибором методу потрібно спитати:

> чи дозволяє предметна область компенсувати слабкість за одним критерієм силою за іншим?

---

## 13. TOPSIS: інша ідея «кращості»

TOPSIS працює інакше.

Він шукає альтернативу, яка:

- близька до ideal best;
- далека від ideal worst.

Назва:

> Technique for Order Preference by Similarity to Ideal Solution.

Ідея геометрична.

Після нормалізації та зважування кожна альтернатива стає точкою в багатовимірному просторі критеріїв.

Створюємо дві умовні точки:

- ideal best;
- ideal worst.

Потім вимірюємо відстані.

---

## 14. Векторна нормалізація TOPSIS

TOPSIS у нашому Python package використовує vector normalization.

Для критерію \(j\):

\[
z_{ij}=
\frac{x_{ij}}
{\sqrt{\sum_i x_{ij}^2}}.
\]

Потім:

\[
v_{ij}=w_j z_{ij}.
\]

Тобто спочатку scale adjustment, потім weighting.

Далі формуються ideal points.

---

## 15. Ideal best і ideal worst

Для benefit criterion ideal best — максимум weighted value.

Для cost criterion ideal best — мінімум.

Відповідно ideal worst навпаки.

Для альтернативи \(i\):

\[
D_i^+
\]

— відстань до ideal best.

\[
D_i^-
\]

— відстань до ideal worst.

Closeness coefficient:

\[
C_i=
\frac{D_i^-}
{D_i^+ + D_i^-}.
\]

Чим більше \(C_i\), тим альтернатива:

- ближча до ideal best;
- далі від ideal worst.

---

## 16. TOPSIS baseline

Для baseline:

- C: \(C_i\approx0.5869\);
- A: ≈ 0.4830;
- D: ≈ 0.4719;
- B: ≈ 0.4307.

Ranking:

\[
C>A>D>B.
\]

Це відрізняється від WSM:

\[
C>D>B>A.
\]

Обидва методи ставлять C першою.

Але порядок інших альтернатив різний.

<figure>
  <img src="figures/fig_04_topsis_geometry.svg" alt="Інтуїція TOPSIS">
  <figcaption><strong>Рис. 4.</strong> TOPSIS оцінює альтернативу через одночасну близькість до ideal best і віддаленість від ideal worst. Це інша логіка, ніж лінійна сума WSM.</figcaption>
</figure>

---

## 17. Чому WSM і TOPSIS можуть не погоджуватися

Це не «баг».

Методи мають різні математичні визначення якості.

WSM питає:

> який weighted sum normalized performance найбільший?

TOPSIS питає:

> яка точка найкраще розташована відносно ideal best і ideal worst?

Тому одна і та сама decision matrix може давати різний ranking.

Це дуже важливий науковий сигнал.

> **Якщо висновок сильно залежить від методу, його треба формулювати обережніше.**

---

## 18. Ranking — функція не лише даних

Корисно записати:

\[
Ranking=
f(
Data,\ Types,\ Weights,\ Normalization,\ Method
).
\]

Тобто ranking залежить від:

- decision matrix;
- benefit/cost classification;
- weights;
- normalization;
- aggregation method.

Зміна будь-якого елемента може змінити висновок.

Це руйнує небезпечну ілюзію:

> «таблиця містить об’єктивний переможець».

Ні.

Таблиця містить дані.

Переможець виникає після додавання **моделі рішення**.

---

## 19. Ваги: числа з великим впливом

Baseline:

\[
w_{reliability}=0.25.
\]

Що це означає?

Не:

> reliability «об’єктивно становить 25% якості».

Коректніше:

> у цій MCDA model reliability отримує 25% сумарної ваги.

Вага — це частина decision model.

Її походження повинно бути обґрунтоване.

Можливі джерела:

- expert elicitation;
- policy priorities;
- AHP або інші процедури;
- нормативні вимоги;
- data-driven estimation;
- сценарний аналіз.

Найгірший варіант:

> «поставили 0.25, бо виглядало нормально».

---

## 20. Sensitivity analysis: якщо вага трохи інша

Змінюємо вагу reliability від:

\[
0.10
\]

до:

\[
0.45.
\]

Інші ваги пропорційно перенормовуємо так, щоб:

\[
\sum_j w_j=1.
\]

Це one-factor weight sensitivity.

Мета:

> з’ясувати, чи стабільне перше місце до зміни одного важливого припущення.

---

## 21. Що відбувається при reliability = 0.10

При:

\[
w_{reliability}=0.10
\]

WSM обирає:

\[
B.
\]

TOPSIS продовжує обирати:

\[
C.
\]

Це дуже інформативний результат.

Він говорить:

- WSM leader чутливий до зниження reliability weight;
- TOPSIS у цьому сценарії стійкіший до тієї самої зміни;
- висновок про «переможця» залежить від method.

<figure>
  <img src="figures/fig_05_sensitivity.svg" alt="Sensitivity ranking до ваги reliability">
  <figcaption><strong>Рис. 5.</strong> При малих значеннях ваги reliability WSM може перейти від C до B, тоді як TOPSIS зберігає C. Це приклад method-dependent stability.</figcaption>
</figure>

---

## 22. Чому інші ваги потрібно перенормовувати

Якщо просто змінити reliability з 0.25 до 0.10 і залишити все інше без змін:

\[
\sum_j w_j<1.
\]

Тоді змінилася не лише відносна важливість reliability.

Змінився scale total weight.

У функції reweight_focus решта ваг пропорційно масштабуються:

\[
w'_k=
w_k
\frac{1-w'_{focus}}
{\sum_{j\ne focus}w_j}.
\]

Це зберігає:

\[
\sum_j w'_j=1.
\]

---

## 23. Sensitivity — не «покрутіть слайдер»

Сильний sensitivity analysis має питання.

Наприклад:

> при якому діапазоні reliability weight leader WSM змінюється?

Або:

> чи погоджуються WSM і TOPSIS у всьому діапазоні?

Або:

> який критерій найбільш критичний для першого місця?

Тоді sensitivity — дослідницький експеримент.

Без питання slider може стати просто інтерфейсною іграшкою.

---

## 24. Robustness: ваги невідомі точно

One-factor sensitivity змінює одну вагу.

Але реальні ваги можуть бути невизначеними всі разом.

У Python package використовується Dirichlet distribution навколо baseline.

Ідея:

- expected weight vector = baseline;
- кожний run дає трохи інший набір weights;
- сума автоматично дорівнює 1;
- concentration визначає, наскільки сильно weights коливаються.

Для baseline:

- n = 3000;
- concentration = 80;
- seed = 2026.

---

## 25. Що означає concentration

У спрощеній інтуїції:

- великий concentration → sampled weights близькі до baseline;
- малий concentration → більший розкид.

Це не «рівень достовірності».

Це параметр stochastic model weights.

Його також потрібно обґрунтовувати або аналізувати sensitivity.

---

## 26. Robustness baseline results

Для 3000 runs:

### WSM

C перша приблизно у:

\[
94.2\%
\]

симуляцій.

B — приблизно у:

\[
5.8\%.
\]

### TOPSIS

C перша приблизно у:

\[
85.1\%.
\]

D — приблизно у:

\[
9.7\%.
\]

B — приблизно у:

\[
5.2\%.
\]

<figure>
  <img src="figures/fig_06_robustness.svg" alt="Robustness frequency first place">
  <figcaption><strong>Рис. 6.</strong> C є частим лідером, але не абсолютним. TOPSIS демонструє більшу мінливість першого місця, ніж WSM, за тієї самої моделі uncertainty weights.</figcaption>
</figure>

---

## 27. Як правильно читати 94%

Неправильно:

> C має 94% імовірність бути реально найкращою.

Правильно:

> за baseline decision matrix, Dirichlet perturbation weights з concentration=80 і WSM C посідає перше місце приблизно у 94% simulated weight vectors.

Чому це важливо?

Бо stochastic robustness model описує **невизначеність ваг**, а не всю реальну невизначеність рішення.

Вона не включає автоматично:

- error in scores;
- uncertainty criterion types;
- missing criteria;
- correlations;
- model choice;
- future conditions.

---

## 28. Seed і reproducibility

У robustness analysis:

\[
seed=2026.
\]

Навіщо?

Щоб repeated experiment генерував той самий pseudo-random sample.

Це дозволяє:

- перевіряти результати;
- порівнювати код;
- тестувати regression;
- відтворювати figure.

Seed не робить симуляцію «правильнішою».

Він робить її **відтворюваною**.

---

## 29. Найнебезпечніша помилка: переплутати cost і benefit

Припустимо, cost помилково позначено як benefit.

Тоді модель починає вважати:

> дорожче = краще.

З математичного погляду алгоритм може бути стабільним.

Нормалізація виконається.

WSM дасть scores.

Ranking виглядатиме акуратно.

Але сенс моделі зламаний.

<figure>
  <img src="figures/fig_07_break_cost_benefit.svg" alt="Помилка cost як benefit">
  <figcaption><strong>Рис. 7.</strong> Неправильний criterion type не обов’язково викликає software error. Він може тихо змінити напрям переваги й породити переконливий, але предметно хибний ranking.</figcaption>
</figure>

Це хороший приклад:

> **correct code ≠ correct model.**

---

## 30. Зламай модель: zero-range criterion

Що буде, якщо всі alternatives мають однакове значення за критерієм?

Тоді:

\[
\max x_j-\min x_j=0.
\]

Звичайна min-max formula мала б ділення на нуль.

У Python package такий criterion отримує normalized value 1 для всіх alternatives.

Інтуїтивно:

> критерій не розрізняє alternatives.

Отже, він не впливає на ranking між ними.

Але методологічно можна спитати:

> навіщо criterion із нульовою discrimination capacity взагалі включений у модель?

---

## 31. Зламай модель: одна альтернатива домінує лише через scale

Якщо пропустити normalization, criterion із великими raw numbers може домінувати.

Наприклад capacity 75–90 чисельно набагато більша за reliability 0.88–0.96.

Сума raw weighted values тоді змішує:

- одиниці;
- відсотки;
- умовні бали;
- час.

Це не просто технічна неточність.

Це беззмістовна арифметика.

---

## 32. Зламай модель: жорсткий поріг

Припустимо, risk > 0.20 є неприйнятним незалежно від інших критеріїв.

Тоді MCDA, де risk просто має weight 0.10, може дозволити іншими перевагами компенсувати неприйнятний risk.

Потрібно додати constraint:

\[
risk_i\le0.20.
\]

Тільки після filtering допустимих alternatives виконувати ranking.

Це приклад межі компенсаторної MCDA.

---

## 33. Зламай модель: взаємозалежні критерії

Припустимо reliability і risk фактично описують майже один і той самий аспект.

Якщо дати їм окремі ваги:

\[
0.25+0.10,
\]

можна двічі врахувати одну властивість.

Це називають double counting.

Перед MCDA потрібно спитати:

- criteria conceptually distinct?
- чи не дублюють один одного?
- чи не є один функцією іншого?

---

## 34. Зламай модель: weights як політичне число

Якщо weight було визначено неаналітично, але представлено з трьома знаками після коми, може виникнути ілюзія точності.

Наприклад:

\[
w=0.237.
\]

Чи справді stakeholder preference відомий із точністю до тисячної?

Можливо, чесніше:

\[
w\in[0.20,0.30].
\]

Тоді потрібен sensitivity або robustness.

---

## 35. Python без страху: WSM

Концептуально:

~~~python
result = weighted_sum(matrix, weights, types)

print(result.ranking)
print(result.scores)
~~~

Контроль:

~~~text
C > D > B > A
score(C) ≈ 0.6167
~~~

Якщо результат не збігається, перевіряємо:

- criterion types;
- weights;
- normalization;
- index alignment.

---

## 36. Python без страху: TOPSIS

~~~python
result = topsis(matrix, weights, types)

print(result.ranking)
print(result.scores)
~~~

Контроль:

~~~text
C > A > D > B
score(C) ≈ 0.5869
~~~

Не потрібно очікувати, що ranking обов’язково збігатиметься з WSM.

---

## 37. Python без страху: sensitivity

~~~python
s = one_factor_sensitivity(
    matrix,
    weights,
    types,
    focus="reliability",
    values=[0.10, 0.25, 0.40],
)
~~~

Контрольний факт:

~~~text
reliability = 0.10
WSM top = B
TOPSIS top = C
~~~

Це корисний regression case.

---

## 38. Python без страху: robustness

~~~python
r = robustness_analysis(
    matrix,
    weights,
    types,
    n_runs=3000,
    concentration=80,
    seed=2026,
)
~~~

Після цього аналізуємо:

- top-choice counts;
- top-choice shares;
- difference WSM vs TOPSIS.

Важливо не просто вивести таблицю, а пояснити її.

---

## 39. Verification checklist

### Inputs

Decision matrix не порожня.

Усі values finite.

Weights finite.

Weights:

\[
w_j\ge0.
\]

І:

\[
\sum_jw_j=1.
\]

Criterion types лише:

- benefit;
- cost.

### Baseline WSM

\[
C>D>B>A.
\]

\[
S_C\approx0.6167.
\]

### Baseline TOPSIS

\[
C>A>D>B.
\]

\[
C_C\approx0.5869.
\]

### Sensitivity

При:

\[
w_{reliability}=0.10
\]

WSM leader:

\[
B.
\]

TOPSIS leader:

\[
C.
\]

### Robustness

Однаковий seed → однакові results.

---

## 40. Чому finite inputs важливі

NaN або infinity можуть тихо проникнути в матрицю.

Тоді:

- normalization може дати NaN;
- sorting може поводитися несподівано;
- ranking може виглядати валідним, хоча дані зіпсовані.

Тому current Python model явно відхиляє non-finite:

\[
NaN,\quad +\infty,\quad -\infty.
\]

Це частина mathematical hygiene.

---

## Поглиблення: повна baseline-матриця після нормалізації

Нормалізацію корисно бачити не лише у формулі, а як повну таблицю.

Для baseline:

| Alternative | cost | time | reliability | capacity | risk |
|---|---:|---:|---:|---:|---:|
| A | 0.455 | 0.571 | 0.500 | 0.000 | 0.538 |
| B | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| C | 0.000 | 1.000 | 1.000 | 0.333 | 1.000 |
| D | 0.727 | 0.286 | 0.250 | 0.667 | 0.385 |

Ця таблиця вже містить важливу інтерпретацію.

### B

B сильна за:

- cost;
- capacity.

Але слабка за:

- time;
- reliability;
- risk.

### C

C сильна за:

- time;
- reliability;
- risk.

Але найгірша за cost.

### D

D ніде не є абсолютним максимумом, але має помірно сильний профіль.

Саме тому D у WSM посідає друге місце.

MCDA часто винагороджує не «найкращий окремий показник», а **збалансований профіль**.

---

## Поглиблення: WSM як сума criterion contributions

Для кожної alternative можна розкласти score:

\[
S_i=
w_1r_{i1}+
w_2r_{i2}+
\cdots+
w_mr_{im}.
\]

Для C:

\[
S_C=
0.25\cdot0+
0.20\cdot1+
0.25\cdot1+
0.20\cdot0.333+
0.10\cdot1.
\]

Окремі contributions:

- cost: 0;
- time: 0.20;
- reliability: 0.25;
- capacity: ≈0.0667;
- risk: 0.10.

Разом:

\[
S_C\approx0.6167.
\]

Це корисніше за одне число 0.6167.

Ми бачимо **звідки взявся score**.

Такий decomposition особливо важливий для explainability.

Якщо stakeholder не погоджується з ranking, можна показати:

- який criterion дав найбільший внесок;
- який criterion «покарав» alternative;
- які weights сформували результат.

---

## Поглиблення: WSM і компенсація

Розглянемо extreme thought experiment.

Альтернатива X має:

- дуже низьку reliability;
- дуже низький risk;
- дуже низький cost.

WSM може дати їй високий total score, якщо cost/risk weights достатньо великі.

Тобто:

> poor performance за одним criterion може бути компенсована good performance за іншими.

Це не завжди прийнятно.

Якщо reliability має hard minimum:

\[
reliability_i\ge0.90,
\]

спочатку потрібно filtering.

Тоді MCDA працює вже серед admissible alternatives.

Отже, корисна структура:

\[
Constraints\rightarrow MCDA.
\]

Не завжди:

\[
MCDA\rightarrow winner.
\]

---

## Поглиблення: звідки беруться weights

Weights — найвпливовіша і водночас найчастіше недооцінена частина MCDA.

Можна виділити кілька джерел.

### Direct assignment

Експерт одразу задає:

\[
w=(0.25,0.20,0.25,0.20,0.10).
\]

Просто, але потребує пояснення.

### Pairwise comparison

Експерти порівнюють criteria парами.

Це може бути реалізовано через AHP або інші процедури.

### Rank-based methods

Спочатку criteria упорядковуються за importance, потім ranking перетворюється на weights.

### Data-driven methods

Іноді використовують entropy або інші statistical approaches.

Але такі weights відображають властивості data, а не обов’язково stakeholder values.

### Policy-defined weights

Weights можуть бути задані нормативно або управлінським рішенням.

У будь-якому випадку книга й дослідження повинні відповісти:

> **що означають weights і звідки вони взялися?**

---

## Поглиблення: weight normalization не створює обґрунтованість

Нехай експерт дав:

\[
(5,4,5,4,2).
\]

Можна нормувати:

\[
w_j=
\frac{a_j}
{\sum_k a_k}.
\]

Отримаємо:

\[
(0.25,0.20,0.25,0.20,0.10).
\]

Математично все добре.

Але якщо числа 5,4,5,4,2 взяті довільно, normalization не робить їх науково обґрунтованими.

Це загальний принцип:

> **математична обробка не виправляє слабке походження input assumptions.**

---

## Поглиблення: TOPSIS distances як окрема таблиця

Для baseline:

| Alternative | \(D^+\) | \(D^-\) | \(C_i\) |
|---|---:|---:|---:|
| C | 0.0363 | 0.0515 | 0.5869 |
| A | 0.0346 | 0.0323 | 0.4830 |
| D | 0.0363 | 0.0324 | 0.4719 |
| B | 0.0512 | 0.0387 | 0.4307 |

Зверніть увагу на A і D.

Їхні \(C_i\) близькі.

Невелика зміна:

- weights;
- score;
- normalization assumptions

може змінити їх relative order.

Це ще одна причина не писати ranking як абсолютну істину.

---

## Поглиблення: що означає ideal solution

Ideal best у TOPSIS часто не є реальною alternative.

Це synthetic point.

Вона складається з найкращих criterion values:

- найкращий cost;
- найкращий time;
- найкраща reliability;
- найкраща capacity;
- найкращий risk.

Можливо, жодна реальна alternative не має такого набору.

Тому ideal point — **reference**, а не «секретний п’ятий варіант».

Це важливо для інтерпретації.

---

## Поглиблення: sensitivity threshold

У нашому one-factor experiment змінюється reliability weight.

Baseline:

\[
w_{rel}=0.25.
\]

При:

\[
w_{rel}=0.10
\]

WSM leader — B.

При трохи більшому значенні baseline dataset уже повертає C на перше місце.

Це означає:

> WSM ranking має boundary region поблизу low reliability weight.

Такий threshold — сильніша інформація, ніж один screenshot.

У звіті корисно писати:

> leader змінюється при переході через певний діапазон weight.

А не лише:

> при 0.10 B, при 0.25 C.

---

## Поглиблення: sensitivity map замість одного slider

One-factor analysis — лише перший крок.

У складнішому дослідженні можна змінювати два weights одночасно.

Наприклад:

\[
w_{cost},
\quad
w_{reliability}.
\]

Тоді простір можна поділити на області:

- тут leader A;
- тут B;
- тут C;
- тут D.

Це вже **decision stability map**.

Вона відповідає:

> які preference configurations підтримують кожну alternative?

Таке представлення часто інформативніше за одну baseline ranking.

---

## Поглиблення: uncertainty не лише у weights

Current robustness model perturb weights.

Але uncertainty може бути і в raw scores.

Наприклад:

\[
reliability_C=0.96
\]

може бути estimate.

Реально:

\[
reliability_C\in[0.93,0.97].
\]

Тоді stochastic model може perturb:

- weights;
- criterion values;
- або обидва.

Це вже значно ширша robustness analysis.

Але її не слід додавати автоматично.

Спершу треба визначити:

> де саме в decision model знаходиться реальна uncertainty?

---

## Поглиблення: correlations між criteria

Criteria можуть бути статистично або концептуально пов’язані.

Наприклад:

- cost і capacity;
- reliability і risk;
- time і cost.

Якщо два criteria майже дублюють одне одного, model може double-count one dimension.

Перед MCDA корисно провести:

- conceptual review;
- correlation analysis, якщо є sufficient data;
- stakeholder review of criterion definitions.

MCDA не повинна починатися з weights.

Вона повинна починатися з **якісного набору criteria**.

---

## Поглиблення: dominated alternative

Альтернатива \(A\) домінується \(B\), якщо B не гірша за всіма criteria й краща хоча б за одним.

Якщо alternative dominated, її присутність у ranking може бути малоінформативною.

Але в нашій baseline matrix немає очевидної alternative, яка повністю домінує іншу за всіма criterion directions.

Це добре для навчання:

> alternatives мають реальні trade-offs.

Перед запуском MCDA корисно зробити dominance check.

---

## Поглиблення: rank reversal як нагадування про залежність від model set

У деяких MCDA methods ranking може змінитися після:

- додавання нової alternative;
- видалення alternative;
- зміни normalization context.

Причина в тому, що normalization або ideal points залежать від set of alternatives.

Це означає:

> ranking іноді є властивістю не лише alternative, а всього comparison set.

Тому якщо decision set змінюється, analysis потрібно повторювати.

Не слід вважати старі scores «вічними характеристиками» alternatives.

---

## Поглиблення: verification, validation і decision validity

### Verification

Чи правильно реалізовані formulas?

- min-max;
- WSM;
- TOPSIS;
- reweighting;
- Dirichlet sampling.

### Input validation

Чи:

- weights finite;
- values finite;
- criterion types valid;
- columns aligned?

### Model validity

Чи:

- criteria справді релевантні;
- weights обґрунтовані;
- compensation допустима;
- method відповідає decision logic?

### Decision usefulness

Чи допомагає model реально пояснити trade-offs?

Можна мати mathematically perfect MCDA, яка не відповідає реальному decision question.

---

## Поглиблення: scenario design для T2.L5

Корисний planned experiment:

| Run | Зміна | Очікування | Що перевіряємо |
|---|---|---|---|
| Baseline | none | C top | контроль |
| Low reliability | \(w_r=0.10\) | WSM may switch | sensitivity |
| High reliability | \(w_r=0.40\) | C stronger | stability |
| Wrong type | cost→benefit | ranking changes | semantic failure |
| Robustness | Dirichlet | C often top | uncertain weights |
| Constraint | risk≤0.20 | B excluded | non-compensation |

Це значно сильніше за один ranking.

---

## Поглиблення: conditional conclusion як структура

Сильний висновок можна будувати за шаблоном:

> За [data], [criterion types], [weights] та [method] alternative X має [result]. Sensitivity показує [stability/change]. Robustness under [uncertainty model] показує [share/range]. Висновок обмежений [limitations].

Наприклад:

> За baseline matrix, benefit/cost classification та weights C є першою за WSM і TOPSIS. При reliability weight 0.10 WSM leader змінюється на B, тоді як TOPSIS залишає C. У Dirichlet robustness з concentration=80 C посідає перше місце приблизно у 94% WSM і 85% TOPSIS runs. Це свідчить про високу, але не абсолютну stability у межах заданої uncertainty model.

Такий conclusion значно науковіший, ніж:

> C — найкраща.

---

## Поглиблення: MCDA і людське рішення

MCDA не повинна замінювати decision-maker.

Вона:

- структурує data;
- робить weights явними;
- показує trade-offs;
- виявляє sensitivity;
- документує reasoning.

Але остаточне рішення може враховувати:

- constraints поза model;
- нову information;
- qualitative considerations;
- policy requirements.

Тому модель — **decision support**, а не автоматичний носій істини.

Це особливо важливо у військовій організації, де decision accountability залишається за людиною.

---

## Поглиблення: reproducibility package MCDA

Для наукового результату збережіть:

- decision matrix;
- criterion definitions;
- benefit/cost types;
- weights;
- weight rationale;
- normalization method;
- WSM/TOPSIS implementation;
- sensitivity grid;
- robustness seed;
- concentration;
- n_runs;
- result tables;
- figures;
- commit/version metadata.

Тоді інший дослідник може відтворити не лише winner, а **весь шлях до conclusion**.

---

## Поглиблення: interpretation of robustness shares

Для WSM:

\[
P_{sim}(C\ top)\approx0.942.
\]

Для TOPSIS:

\[
P_{sim}(C\ top)\approx0.851.
\]

Позначення \(P_{sim}\) корисне саме педагогічно.

Воно нагадує:

> це probability/share у simulated model space.

Не:

\[
P(C\ objectively\ best).
\]

Ця різниця принципова.

---

<figure>
  <img src="figures/fig_08_conditional_conclusion.svg" alt="Структура умовного MCDA висновку">
  <figcaption><strong>Рис. 8.</strong> Сильний висновок MCDA пов’язує data, criterion types, weights і method із sensitivity/robustness та завершується allowed conclusion, а не абсолютним ярликом «best».</figcaption>
</figure>

## 41. Типові помилки мислення

### Помилка 1. «C — об’єктивно найкраща»

Ні.

Коректно:

> за заданою model configuration C є baseline leader.

### Помилка 2. «Weights — просто налаштування»

Ні.

Вони визначають value structure рішення.

### Помилка 3. «Два methods повинні дати однаковий ranking»

Ні.

Розбіжність може бути змістовною інформацією.

### Помилка 4. «Sensitivity достатньо зробити для одного випадкового criterion»

Ні.

Focus criterion має бути обґрунтований.

### Помилка 5. «94% robustness = 94% probability C справді найкраща»

Ні.

Це share under simulated weight uncertainty model.

### Помилка 6. «Більше decimal places = більше об’єктивності»

Ні.

Numerical precision не замінює якість assumptions.

---

## 42. Як формулювати коректний висновок

Погано:

> C є найкращою альтернативою.

Краще:

> За baseline criteria, criterion types, weights і WSM C має найвищий score 0.6167.

Ще сильніше:

> За baseline criteria, types і weights C посідає перше місце як у WSM, так і TOPSIS; однак порядок інших alternatives залежить від method, а one-factor sensitivity показує, що при reliability weight 0.10 WSM leader змінюється на B.

Ще повніше:

> У stochastic weight robustness analysis з Dirichlet concentration=80 і seed=2026 C залишається top choice приблизно у 94% WSM та 85% TOPSIS runs. Отже, baseline leadership C є високою, але не абсолютною стійкістю в межах саме цієї uncertainty model.

Останнє формулювання чітко відділяє:

- факт;
- method;
- uncertainty model;
- limitation.

---

## 43. Predict: перед Lab

Перед слайдером reliability запишіть прогноз.

1. Якщо reliability weight зменшити, хто може виграти?
2. Чи однаково відреагують WSM і TOPSIS?
3. Чому B може піднятися?
4. Чи означає зміна leader, що baseline був «неправильним»?
5. Який висновок можна назвати стійким?

Прогноз потрібен, щоб не пояснювати лише те, що вже побачили на екрані.

---

## 44. Від MiniBook до Lab

У browser Lab T2.L5:

- змінюється reliability weight;
- інші weights пропорційно перенормовуються;
- показуються WSM і TOPSIS rankings;
- відстежується stability у діапазоні.

Пройдіть:

### Predict

Запишіть, чи зміниться leader.

### Run

Зменшіть reliability до 0.10.

### Explain

Поясніть, чому WSM перейшов до B, а TOPSIS — ні.

### Break

Знайдіть умову або modeling mistake, що змінює conclusion.

### Transfer

Побудуйте власну decision matrix.

[**Відкрити інтерактивну Lab T2.L5 →**](../../index.html#mcda)

---

## 45. Від Lab до Python

Browser Lab демонструє:

- baseline ranking;
- weight sensitivity.

Python package додає:

- full validation;
- min-max normalization;
- WSM;
- TOPSIS;
- arbitrary sensitivity grid;
- Dirichlet robustness;
- reproducible seed;
- unit tests.

Тобто:

> **Lab показує механізм, Python дозволяє систематично дослідити його.**

---

## 46. Research Transfer

Візьміть власну задачу вибору.

Не обов’язково військово-технічну.

Це може бути:

- вибір research method;
- software architecture;
- data source;
- model configuration;
- experimental design;
- infrastructure option.

Шаблон:

~~~text
Decision question:

Alternatives:

Criteria:

Criterion types:

Raw data:

Weights:

Weight source / justification:

Normalization:

Method 1:

Method 2:

Baseline ranking:

Sensitivity focus:

Robustness model:

Verification:

Limitations:

Allowed conclusion:
~~~

### Мінімальна постановка

- 3–7 alternatives;
- 4–8 criteria;
- benefit/cost classification;
- weights;
- WSM;
- TOPSIS;
- sensitivity;
- robustness;
- interpretation.

---

## 47. Як не перетворити Research Transfer на декоративну таблицю

Слабка постановка:

> Є три alternatives, поставимо weights і виберемо winner.

Сильніша:

> Потрібно обрати альтернативу для конкретної decision purpose. Criteria відповідають визначеним dimensions. Criterion types перевірені. Weights походять із описаної procedure. Baseline ranking порівнюється двома methods. Sensitivity виявляє critical weights. Robustness оцінює stability. Conclusion explicitly conditional.

Різниця — не у кількості формул.

Різниця — у **дослідницькій дисципліні**.

---

## 48. Мінісловник T2.L5

### Alternative

Один із варіантів вибору.

### Criterion

Ознака, за якою порівнюються alternatives.

### Benefit criterion

Більше = краще.

### Cost criterion

Менше = краще.

### Weight

Модельована відносна важливість criterion.

### Normalization

Перетворення різних scales у сумісну форму.

### WSM

Weighted Sum Model — зважена сума normalized values.

### TOPSIS

Метод, що оцінює proximity to ideal best та distance from ideal worst.

### Ranking

Порядок alternatives за score певного method.

### Sensitivity

Зміна conclusion при зміні параметра.

### Robustness

Стійкість conclusion у множині plausible model configurations.

### Dirichlet distribution

Розподіл для випадкових positive weights, сума яких дорівнює 1.

### Conditional conclusion

Висновок, де явно вказані умови model.

---

## 49. Мініексперимент для самоперевірки

### Сценарій 1

Що станеться, якщо cost помилково зробити benefit?

Вищий cost почне збільшувати attractiveness.

Це предметна помилка.

### Сценарій 2

Якщо всі alternatives мають однакову capacity?

Capacity перестає розрізняти alternatives.

### Сценарій 3

Якщо C top у baseline WSM і TOPSIS, чи достатньо цього для strong conclusion?

Ні.

Потрібно перевірити sensitivity і assumptions.

### Сценарій 4

Якщо C top у 94% WSM runs, чи є це real-world probability?

Ні.

Це robustness under specified uncertainty model.

---

## 50. Одна сторінка підсумку

### П’ять головних ідей

1. MCDA ranking виникає не лише з data, а з усієї model configuration.
2. Benefit/cost direction — фундаментальна частина моделі.
3. WSM і TOPSIS можуть давати різні rankings без software error.
4. Sensitivity показує, наскільки conclusion залежить від weights.
5. Robustness frequency не є автоматично real-world probability.

### Три формули

WSM:

\[
S_i=\sum_j w_j r_{ij}.
\]

TOPSIS closeness:

\[
C_i=
\frac{D_i^-}
{D_i^+ + D_i^-}.
\]

Weight constraint:

\[
\sum_jw_j=1.
\]

### Дві типові помилки

- «winner = objectively best»;
- «robustness share = probability of truth».

### Одне питання

> Який елемент моєї MCDA model найбільше впливає на conclusion: data, types, weights чи method?

### Наступний крок

У Lab змініть reliability 0.25 → 0.10, порівняйте WSM/TOPSIS і сформулюйте conclusion так, щоб у ньому були method та assumptions.

---

## 51. Фінальна думка

Багатокритеріальна модель не повинна приховувати ціннісні припущення за математичними score.

Навпаки.

Її сила в тому, що вона робить їх явними:

- які criteria враховані;
- у якому напрямі вони працюють;
- яку importance отримали;
- який method агрегує;
- наскільки ranking stable.

Тому найкраще питання після MCDA не:

> «Хто переміг?»

А:

> **«За яких умов ця альтернатива перша, наскільки цей висновок стійкий і що має змінитися, щоб ranking став іншим?»**

Саме це перетворює таблицю з балами на дослідницьку модель.
