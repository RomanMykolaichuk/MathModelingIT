# MathModelingIT · Мінікнига T1.L4

## Класифікація методів математичного моделювання

### Метод обирає задача, а не бібліотека

> **Головна ідея книги:** сильний дослідник починає не з питання «яку бібліотеку Python використати?», а з питання «яку структуру має моя задача і який тип результату мені потрібен?». Метод — це відповідь на структуру проблеми. Бібліотека — лише інструмент реалізації.

---

## 0. Паспорт книги

**Код заняття:** T1.L4 
**Тема:** класифікація методів математичного моделювання 
**Рівень:** середній 
**Орієнтовний час читання:** 75–90 хвилин.

Після книги ви повинні вміти:

- визначати тип результат: число, формула, оптимум, ймовірність, шлях, ранжування;
- відрізняти чисельний і символьний методи;
- пояснювати, коли потрібна оптимізація;
- розуміти Монте-Карло як метод невизначеність propagation;
- розпізнавати мережева структура;
- розуміти MCDA як formalized multi-criteria comparison;
- вибирати інструмент Python після Вибір методу;
- формулювати ПЕРЕВІРКА для кожного класу методу;
- проектувати method-selection chain для дисертація fragment.

---

## 1. Сцена: «Я знаю SciPy — отже, розв’яжу все SciPy»

Дослідник добре знає одну library і починає будь-яку задачу з думки:

> «Як це зробити через SciPy?»

Але задача може вимагати точний символьний вираз, граф структура, ранжування альтернативи, невизначеність розподіл або з обмеженнями оптимум.

Тому ключова дисципліна:

> **задача структура → метод → інструмент Python → ПЕРЕВІРКА → інтерпретація.**

<figure>
 <img src="figures/fig_01_method_selection.svg" alt="Ланцюг вибору методу">
 <figcaption><strong>Рис. 1.</strong> інструмент Python є четвертим кроком, а не першим. Спочатку потрібно зрозуміти задача структура та очікуваний результат.</figcaption>
</figure>

---

## 2. Шість питання перед вибором методу

Перед coding запитайте:

1. Який result потрібен?
2. Чи є невизначеність?
3. Чи є цільова функція та обмеження?
4. Чи важлива мережева структура?
5. Чи є кілька критерії?
6. Чи існує analytical/символьний benchmark?

### Вибір методу матриця

| задача структура | метод | інструмент Python | Result |
|---|---|---|---|
| root рівняння | чисельний пошук кореня | SciPy | кількість |
| точний вираз | символьний algebra | SymPy | формула |
| найкращий допустимий розподіл | лінійна оптимізація | SciPy linprog | оптимум |
| ризик за випадковість | Монте-Карло | NumPy RNG | ймовірність/розподіл |
| залежність вузьке місце | граф/мережевий | NetworkX | шлях/структура |
| multi-criteria вибір | MCDA | pandas/NumPy | оцінка/ранжування |

---

# ВИПАДОК — ЧИСЕЛЬНИЙ ПОШУК КОРЕНЯ

## 3. задача

Find додатний час \(t\) коли:

\[
f(t)=120-6t-0.2t^2
\]

досягає нуль:

\[
f(t)=0.
\]

очікуваний результат: один числове значення. це suggests чисельний пошук кореня.

Bracket:

\[
t\in[0,30].
\]

тому що:

\[
f(0)=120>0,
\]

\[
f(30)=-240<0,
\]

 неперервний функція має root всередині.

---

## 4. чисельний result

SciPy root_scalar з Brent метод дає:

\[
t^*\approx13.7228132327.
\]

ПЕРЕВІРКА:

\[
|f(t^*)|<10^{-8}.
\]

розв’язувач status самостійно є weaker ніж residual перевірка.

<figure>
 <img src="figures/fig_02_root_numeric_symbolic.svg" alt="Numerical and symbolic root">
 <figcaption><strong>Рис. 2.</strong> чисельний root дає floating-point значення; символьний метод дає точний вираз. збіг provides cross-method ПЕРЕВІРКА.</figcaption>
</figure>

---

# ВИПАДОК B — СИМВОЛЬНИЙ АНАЛІЗ

## 5. той самий рівняння, різний питання

Now ask:

> що є точний analytical вираз для roots?

SymPy повертає:

\[
t=-15\pm5\sqrt{33}.
\]

додатний root:

\[
-15+5\sqrt{33}
\approx13.7228132327.
\]

той самий object, різний desired результат, тому різний метод.

---

## 6. чисельний vs символьний

### чисельний

корисний коли:

- функція є complicated;
- точний форма недоступний;
- лише numeric root є потрібні.

### символьний

корисний коли:

- точний dependence має значення;
- формула підтримує further аналіз;
- похідні або limits є потрібні.

Neither є universally superior.

Cross-method збіг є сильний ПЕРЕВІРКА.

---

## 7. чому точний робить не завжди середнє корисний

 точний вираз може be huge, hard до interpret або чисельно inconvenient.

якщо лише один scalar result є required, robust чисельний метод може be кращий.

метод якість є judged against потреба дослідження.

---

# ВИПАДОК C — ЛІНІЙНА ОПТИМІЗАЦІЯ

## 8. задача

Maximize:

\[
F=8x_1+6x_2
\]

subject до:

\[
x_1+x_2\le100,
\]

\[
3x_1+2x_2\le240,
\]

\[
x_1,x_2\ge0.
\]

We seek найкращий допустимий рішення, не root або формула.

---

## 9. базовий оптимум

SciPy linprog повертає:

\[
x_1=40,\qquad x_2=60.
\]

цільова функція:

\[
F^*=8\cdot40+6\cdot60=680.
\]

обидва глобальний обмеження є активний:

\[
40+60=100,
\]

\[
3\cdot40+2\cdot60=240.
\]

<figure>
 <img src="figures/fig_03_lp_geometry.svg" alt="Геометрія linear optimization">
 <figcaption><strong>Рис. 3.</strong> пошук кореня шукає нуль, оптимізація шукає найкращий точка допустима область. У базовий оптимум лежить на intersection двох активні обмеження.</figcaption>
</figure>

---

## 10. чому пошук кореня cannot замінює оптимізація

там є no single рівняння \(f(t)=0\). Instead we мають:

- цільова функція;
- допустима область;
- inequalities.

 клас методу необхідно preserve ці semantics.

ПЕРЕВІРКА перевірки:

- non-negativity;
- ресурс;
- бюджет;
- незалежний recomputation цільова функція.

---

## 11. повний перебір versus оптимізація

 сітка could enumerate багато candidate точки.

але сітка resolution introduces approximation і scales погано.

лінійний програмування exploits mathematical структура безпосередньо.

 fact що повний перебір може solve tiny навчальний випадок робить не робити it preferred клас методу.

---

# ВИПАДОК D — РИЗИК ЗА МЕТОДОМ МОНТЕ-КАРЛО

## 12. задача

Single-step споживання:

\[
C_k\sim N(6,1.5^2)
\]

with negative values clipped to zero.

для 20 кроки:

\[
C_{tot}=\sum_{k=1}^{20}C_k.
\]

питання:

> що є ймовірність що total споживання exceeds 120?

це є ймовірність/розподіл питання.

---

## 13. базове моделювання

для:

\[
N=10000,
\]

\[
seed=2026,
\]

 course реалізація оцінки:

\[
\hat p\approx0.5021.
\]

Nominal середнє total є:

\[
20\cdot6=120,
\]

so result поблизу one-half є правдоподібну.

<figure>
 <img src="figures/fig_04_monte_carlo_risk.svg" alt="Monte Carlo risk distribution">
 <figcaption><strong>Рис. 4.</strong> Монте-Карло answers distribution-level питання. пропускна спроможність поріг splits змодельовані підсумки у подія і non-event результати.</figcaption>
</figure>

---

## 14. інтерпретація

правильний:

> за specified iid clipped-normal model, про 50.21% змодельовані підсумки exceed 120.

Incorrect:

> реальний процес має точно 50.21% ризик.

моделювання оцінки consequences припущення.

---

## 15. чому оптимізація є неправильний тут

 поточний питання має no змінна рішення і no цільова функція до maximize.

Adding оптимізація would відповідати інший питання.

для приклад:

> що пропускна спроможність мінімізує вартість subject до ризик нижче 5%?

що would legitimately combine моделювання і оптимізація.

---

# ВИПАДОК E — МЕРЕЖЕВИЙ МЕТОД

## 16. працювати граф

Edges:

- початок→, вага 3;
- початок→B, 4;
- →C, 5;
- B→C, 2;
- C→Finish, 4.

питання:

> який залежність шлях determines total тривалість?

це є graph-structure питання.

---

## 17. критичний шлях

Via:

\[
3+5+4=12.
\]

Via B:

\[
4+2+4=10.
\]

тому:

\[
Start\rightarrow A\rightarrow C\rightarrow Finish
\]

має length:

\[
12.
\]

<figure>
 <img src="figures/fig_05_network_path.svg" alt="Critical path mini-case">
 <figcaption><strong>Рис. 5.</strong> мережевий метод використовує структура залежностей безпосередньо. Longest зважений DAG шлях є початок→→C→Finish, length 12.</figcaption>
</figure>

---

## 18. чому граф представлення має значення

 тривалість table самостійно може hide топологія.

мережевий представлення preserves:

- node ідентичність;
- edge напрям;
- залежність;
- шлях.

коли топологія є питання, граф метод є natural.

---

# ВИПАДОК F — БАГАТОКРИТЕРІАЛЬНИЙ АНАЛІЗ РІШЕНЬ

## 19. альтернативи

| Alt | вартість | час | надійність |
|---|---:|---:|---:|
| | 80 | 7 |.90 |
| B | 65 | 9 |.82 |
| C | 95 | 5 |.96 |

ваги:

\[
w_{cost}=0.30,\quad
w_{time}=0.25,\quad
w_{rel}=0.45.
\]

вартість/час є вартість критерії, надійність є benefit.

---

## 20. Ratio нормалізація

для вартість:

\[
r_{cost,i}=
\frac{\min(cost)}{cost_i}.
\]

для час:

\[
r_{time,i}=
\frac{\min(time)}{time_i}.
\]

для надійність:

\[
r_{rel,i}=
\frac{rel_i}{\max(rel)}.
\]

оцінка:

\[
S_i=
0.30r_{cost,i}
+0.25r_{time,i}
+0.45r_{rel,i}.
\]

---

## 21. базове ранжування

наближений оцінки:

\[
S_C\approx0.9053,
\]

\[
S_A\approx0.8442,
\]

\[
S_B\approx0.8233.
\]

ранжування:

\[
C>A>B.
\]

<figure>
 <img src="figures/fig_06_mcda_ranking.svg" alt="MCDA ranking mini-case">
 <figcaption><strong>Рис. 6.</strong> MCDA produces умовний ранжування за явний ваги і критерій directions. ранжування є не цільова функція property незалежний метод.</figcaption>
</figure>

---

## 22. MCDA versus оптимізація

LP chooses неперервний рішення змінні за hard обмеження.

MCDA compares дискретний альтернативи за кілька критерії.

They може coexist у larger рішення робочий процес, але they є не synonymous.

---

# ВИБІР МЕТОДУ ЯК ДОСЛІДНИЦЬКЕ МІРКУВАННЯ

## 23. результат тип є спочатку класифікатор

### кількість

Root, integral, параметр оцінка.

### формула

символьний вираз.

### оптимум

оптимізація.

### розподіл/ймовірність

Монте-Карло або статистичну метод.

### шлях/структура

граф/мережевий метод.

### ранжування

MCDA.

 запитаний відповідати shape часто narrows метод вибір immediately.

---

## 24. невизначеність є second класифікатор

Ask:

> є вхідні дані або спостереження random або невизначені?

якщо yes, probabilistic layer може be required.

але Монте-Карло слід не be added лише тому що невизначеність “sounds науковий”.

визначити random змінні, distributions і припущення explicitly.

---

## 25. обмеження є third класифікатор

якщо задача має цільова функція:

\[
F(x)\rightarrow\max
\]

subject до:

\[
g_i(x)\le0,
\]

оптимізація є natural class.

без рішення цільова функція, оптимізація може be category похибка.

---

## 26. мережева структура є fourth класифікатор

якщо relationships між entities determine результат, preserve them як граф структура.

Examples:

- проєкт залежності;
- communication топологія;
- потік мережевий;
- залежність граф.

---

## 27. кілька критерії є fifth класифікатор

коли альтернативи є judged за допомогою кілька non-equivalent критерії, один scalar показник може потребувати явний перевага припущення.

MCDA робить them видимою через:

- критерій directions;
- нормалізація;
- ваги;
- агрегування.

---

## 28. аналітичний еталон є ПЕРЕВІРКА opportunity

Even коли кінцевий метод чисельний, ask:

> є там simpler точний випадок?

Examples:

- чисельний root checked за допомогою символьний root;
- чисельний ODE checked за допомогою closed форма;
- Монте-Карло checked against rough expectation;
- оптимізація checked за допомогою ручний corner точки.

це є reusable дослідження discipline.

---

## 29. метод, алгоритм, реалізація

Distinguish three levels.

### клас методу

чисельний пошук кореня.

### алгоритм

Brent метод.

### реалізація

SciPy root_scalar.

або:

### клас методу

лінійний програмування.

### алгоритм/backend

HiGHS.

### реалізація

SciPy linprog.

це відмінність покращує дисертація методологія мовою.

---

## 30. ПЕРЕВІРКА необхідно match метод

| метод | ПЕРЕВІРКА |
|---|---|
| root | residual |
| символьний | підстановка/спрощення |
| оптимізація | допустимість + цільова функція |
| Монте-Карло | зерно генератора + збіжність/діапазон |
| мережевий | ручний шлях validity/length |
| MCDA | directions + ваги + оцінка recomputation |

<figure>
 <img src="figures/fig_07_verification_matrix.svg" alt="Verification matrix by method">
 <figcaption><strong>Рис. 7.</strong> Вибір методу містить ПЕРЕВІРКА selection. result без method-specific перевірка є incomplete.</figcaption>
</figure>

---

## 31. Зламай Вибір методу: hammer задача

якщо дослідник knows один інструмент well, кожен задача може look like що інструмент.

 ймовірність питання forced у оптимізація є no longer той самий Дослідницьке питання.

 граф задача flattened у table може lose топологія.

 ранжування питання reduced до один arbitrary оцінка може hide preferences.

 відмова є conceptual, не syntactic.

---

## 32. Зламай Вибір методу: unnecessary складність

 простий точний формула exists.

дослідник launches 100,000 Монте-Карло запуски до оцінка той самий scalar.

 result може be close, але adds:

- sampling шум;
- computational вартість;
- більше параметри.

складність слід earn its place.

---

## 33. Зламай Вибір методу: exactness fetish

 символьний вираз може be точний але uselessly великий.

якщо рішення потребує лише robust scalar з допуск, чисельний метод може communicate кращий.

науковий rigor є не measured за допомогою вираз length.

---

## 34. Hybrid методи

реальний дослідження часто combines:

\[
Data
\rightarrow
Calibration
\rightarrow
Simulation
\rightarrow
Optimization
\rightarrow
Sensitivity.
\]

кожен stage answers різний питання.

метод класифікація є не про choosing один метод forever.

It є про choosing кожен метод навмисно.

---

## 35. Sequential метод escalation

 sensible strategy:

1. simplest базовий;
2. перевірити;
3. ідентифікувати missing структура;
4. add метод layer;
5. перевірити знову.

для невизначеність:

\[
Deterministic
\rightarrow
Stochastic
\rightarrow
Monte\ Carlo.
\]

для decisions:

\[
Descriptive
\rightarrow
Optimization
\rightarrow
Robustness.
\]

---

## 36. Computational вартість

метод вибір також залежить на масштаб.

символьний solving може explode у складність.

пошук по сітці може become impossible у високий dimension.

Монте-Карло може потребувати багато запуски.

граф algorithms може масштаб well на sparse structures.

Computational допустимість belongs до метод justification.

---

## 37. Interpretability

різний методи expose різний докази.

символьний формула reveals dependence.

Монте-Карло reveals розподіл.

оптимізація reveals активні обмеження.

мережевий метод reveals топологія.

MCDA reveals компроміси.

Choose метод according до що needs до be explained, не лише computed.

---

## 38. Predict до інструмент

до running кожен випадок, record expectation.

- Root між 0 і 30.
- LP ймовірно використовує усі ресурс і бюджет.
- Монте-Карло ризик поблизу 0.5 тому що середнє total≈пропускна спроможність.
- branch appears longer ніж B.
- C може lead MCDA через до час/надійність.

ПРОГНОЗ turns метод використовувати у experiment.

---

## 39. PYTHON БЕЗ СТРАХУ: root

~~~python
root = numerical_root()
value = 120 - 6*root - 0.2*root**2
assert abs(value) < 1e-8
~~~

---

## 40. PYTHON БЕЗ СТРАХУ: LP

~~~python
result = linear_optimization()
assert result["resource_used"] <= 100
assert result["budget_used"] <= 240
~~~

Control:

\[
F^*=680.
\]

---

## 41. PYTHON БЕЗ СТРАХУ: Монте-Карло

~~~python
risk = monte_carlo_risk(
    n_runs=10000,
    seed=2026,
)
~~~

Control:

\[
risk\approx0.5021.
\]

---

## 42. PYTHON БЕЗ СТРАХУ: мережевий

~~~python
path, length = critical_path()
~~~

Control:

\[
Start\rightarrow A\rightarrow C\rightarrow Finish,
\]

\[
length=12.
\]

---

## 43. PYTHON БЕЗ СТРАХУ: MCDA

~~~python
ranking = weighted_sum_decision()
~~~

Control:

\[
C>A>B.
\]

---

## 44. ВІДТВОРЮВАНІСТЬ через метод classes

кожен випадок слід record:

- вхідні дані;
- метод;
- параметри;
- Python реалізація;
- зерно генератора де суттєвий;
- ПЕРЕВІРКА;
- результат.

 точний метадані differs, але походження даних і результату principle залишається.

---

## 45. Вибір методу table для дисертація

для кожен дослідження робота fill:

| питання | структура | результат | метод | альтернатива | ПЕРЕВІРКА |
|---|---|---|---|---|---|

це prevents методологія chapter з becoming list libraries.

---

## 46. альтернатива метод аналіз

Good дослідження explains не лише що було selected, але правдоподібну альтернативи.

приклад root:

- Brent: robust bracketed scalar root;
- Newton: faster поблизу розв’язок але потребує початок/похідна поведінку;
- SymPy: точний коли tractable.

Selection є argument.

---

## 47. коли методи disagree

припустімо символьний і чисельний root differ significantly.

робити не середнє them.

Investigate:

- неправильний рівняння;
- неправильний branch;
- допуск;
- предметна область;
- coding похибка.

Disagreement є diagnostic докази.

---

## 48. коли методи узгоджуються

збіг strengthens довірчий у реалізація.

але якщо обидва encode той самий неправильний припущення, предметна область model може усе ще be неправильний.

це відмінність repeats throughout course.

---

## 49. синтетичний military context

 six cases може represent abstract роботи такий як поріг timing, training розподіл ресурсів, невизначені синтетичний споживання, проєкт залежності і альтернатива selection.

No реальний operational дані є потрібні.

 transferable object є mathematical структура.

---

## 50. Перенесення в дослідження

для один дисертація fragment fill:

~~~text
Research question:

Expected output type:

Deterministic / uncertain:

Decision variables:

Constraints:

Network structure:

Multiple criteria:

Candidate method:

Alternative method:

Why chosen method fits:

Python tool:

Verification:

Sensitivity / uncertainty:

Limitations:

Allowed conclusion:
~~~

---

## 51. приклад transfer

питання:

> оцінка параметри з шумний спостереження.

результат:

> параметр оцінки plus невизначеність.

Candidate метод:

> нелінійний метод найменших квадратів plus бутстреп.

NetworkX would be inappropriate unless граф структура фактично exists.

метод justification необхідно reference задача.

---

## 52. докази hierarchy

 сильний result містить:

1. valid вхідні дані;
2. justified метод;
3. перевірена computation;
4. чутливість/невизначеність коли потрібні;
5. обмежений інтерпретація.

метод вибір є лише один link у докази chain.

---

## 53. “найкращий метод” є contextual

там є no universal переможець.

 метод є придатний відносний до:

- питання;
- припущення;
- дані;
- результат;
- computational обмеження;
- ПЕРЕВІРКА opportunities.

це є чому класифікація є практичний методологія, не taxonomy trivia.

---

## 54. One-page підсумок

### П’ять головних ідей

1. задача структура selects метод.
2. результат тип є спочатку класифікатор.
3. Python library є реалізація, не методологія.
4. ПЕРЕВІРКА необхідно match клас методу.
5. Hybrid workflows є нормальний коли питання зміна.

### Три правила

Root:

\[
f(t^*)=0.
\]

оптимізація:

\[
F(x)\rightarrow\max
\quad\text{subject to constraints}.
\]

Монте-Карло:

\[
\hat p=\frac{events}{runs}.
\]

### Дві типові помилки

- familiar інструмент → forced метод;
- successful code → justified методологія.

### Одне питання

> що property my дослідження задача forces me до choose це метод?

### Наступний крок

Build:

\[
Question\rightarrow Method\rightarrow Tool\rightarrow Verification.
\]

<figure>
 <img src="figures/fig_08_research_transfer.svg" alt="Research transfer method chain">
 <figcaption><strong>Рис. 8.</strong> Вибір методу стає dissertation-ready коли chain з питання до ПЕРЕВІРКА є явний і відтворюваний.</figcaption>
</figure>

---

## 55. Фінальна думка

методи є не menu з який we pick most sophisticated name.

They є mathematical answers до structural питання.

 root метод finds нуль.

оптимізація finds найкращий допустимий рішення.

Монте-Карло propagates невизначеність.

мережевий метод exposes структура залежностей.

MCDA formalizes multi-criteria перевага.

символьний algebra reveals точний структура.

 основний competence є being able до say:

> **“My задача має це структура, тому це метод є appropriate, це є як I will перевірити it, і ці є limits висновок.”**
