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
- розуміти Monte Carlo як метод невизначеність propagation;
- розпізнавати мережа структура;
- розуміти MCDA як formalized multi-criteria comparison;
- вибирати інструмент Python після вибір методу;
- формулювати перевірка для кожного класу методу;
- проектувати method-selection chain для dissertation fragment.

---

## 1. Сцена: «Я знаю SciPy — отже, розв’яжу все SciPy»

Дослідник добре знає одну library і починає будь-яку задачу з думки:

> «Як це зробити через SciPy?»

Але problem може вимагати точний символьний вираз, graph структура, ранжування альтернативи, невизначеність розподіл або constrained оптимум.

Тому ключова дисципліна:

> **Структура задачі → метод → інструмент Python → перевірка → інтерпретація.**

<figure>
 <img src="figures/fig_01_method_selection.svg" alt="Ланцюг вибору методу">
 <figcaption><strong>Рис. 1.</strong> інструмент Python є четвертим кроком, а не першим. Спочатку потрібно зрозуміти Структура задачі та очікуваний результат.</figcaption>
</figure>

---

## 2. Шість питання перед вибором методу

Перед coding запитайте:

1. Який результат потрібен?
2. Чи є невизначеність?
3. Чи є цільова функція та обмеження?
4. Чи важлива мережа структура?
5. Чи є множинний критерії?
6. Чи існує аналітичний/символьний benchmark?

### вибір методу матриця

| Структура задачі | метод | інструмент Python | результат |
|---|---|---|---|
| корінь рівняння | чисельний пошук кореня | SciPy | number |
| точний вираз | символьна алгебра | SymPy | формула |
| найкращий допустимий розподіл | лінійна оптимізація | SciPy linprog | оптимум |
| ризик за випадковості | Monte Carlo | NumPy RNG | ймовірність/розподіл |
| вузьке місце залежностей | graph/мережа | NetworkX | шлях/структура |
| багатокритеріальний вибір | MCDA | pandas/NumPy | оцінка/ранжування |

---

# приклад — чисельний пошук кореня

## 3. Problem

знайти додатний time \(t\) коли:

\[
f(t)=120-6t-0.2t^2
\]

досягає нуля:

\[
f(t)=0.
\]

очікуваний результат: один чисельний значення. це підказує чисельний пошук кореня.

інтервал:

\[
t\in[0,30].
\]

оскільки:

\[
f(0)=120>0,
\]

\[
f(30)=-240<0,
\]

 неперервний функція має корінь inside.

---

## 4. чисельний результат

SciPy root_scalar з Brent метод gives:

\[
t^*\approx13.7228132327.
\]

перевірка:

\[
|f(t^*)|<10^{-8}.
\]

розв’язувач статус сам по собі є weaker than нев’язка перевірка.

<figure>
 <img src="figures/fig_02_root_numeric_symbolic.svg" alt="чисельний і символьний корінь">
 <figcaption><strong>Рис. 2.</strong> чисельний корінь gives floating-point значення; символьний метод gives точний вираз. Agreement provides cross-method перевірка.</figcaption>
</figure>

---

# приклад B — символьний аналіз

## 5. той самий рівняння, інший питання

Now ask:

> що є точний аналітичний вираз для корені?

SymPy returns:

\[
t=-15\pm5\sqrt{33}.
\]

додатний корінь:

\[
-15+5\sqrt{33}
\approx13.7228132327.
\]

той самий об’єкт, інший desired результат, тому інший метод.

---

## 6. чисельний порівняно з символьний

### чисельний

корисний коли:

- функція є складний;
- точний форма unavailable;
- лише numeric корінь є потрібний.

### символьний

корисний коли:

- точний dependence має значення;
- формула supports подальший аналіз;
- derivatives або межі є потрібний.

Neither є universally superior.

Cross-method agreement є strong перевірка.

---

## 7. чому точний не always середнє корисний

 точний вираз може бути huge, важким для інтерпретації або чисельно незручним.

якщо лише один скалярний результат є required, robust чисельний метод може бути better.

метод якість є judged against дослідження need.

---

# приклад C — лінійна оптимізація

## 8. Problem

максимізувати:

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

ми шукаємо найкращий допустимий decision, не корінь або формула.

---

## 9. Baseline оптимум

SciPy linprog returns:

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
 <img src="figures/fig_03_lp_geometry.svg" alt="Геометрія лінійна оптимізація">
 <figcaption><strong>Рис. 3.</strong> пошук кореня шукає нуля, оптимізація шукає найкращий точка область допустимих розв’язків. У baseline оптимум лежить на intersection двох активні обмеження.</figcaption>
</figure>

---

## 10. чому пошук кореня не може replace оптимізація

Немає одного рівняння \(f(t)=0\). натомість ми мають:

- цільова функція;
- область допустимих розв’язків;
- inequalities.

 клас методу має preserve цю семантику.

перевірка перевірки:

- non-negativity;
- ресурс;
- бюджет;
- незалежний recomputation цільова функція.

---

## 11. повний перебір versus оптимізація

 сітка може enumerate багато кандидатні точки.

але сітка resolution introduces approximation і scales poorly.

лінійне програмування exploits математичну структуру directly.

Той факт, що повний перебір може розв’язати малий навчальний приклад не make це preferred клас методу.

---

# приклад D — MONTE CARLO ризик

## 12. Problem

Single-step витрата:

\[
C_k\sim N(6,1.5^2)
\]

з від’ємні значення замінюються нулем.

для 20 steps:

\[
C_{tot}=\sum_{k=1}^{20}C_k.
\]

питання:

> що є ймовірність це загальний витрата exceeds 120?

Це ймовірність/розподіл питання.

---

## 13. Baseline моделювання

для:

\[
N=10000,
\]

\[
seed=2026,
\]

 курс реалізація оцінки:

\[
\hat p\approx0.5021.
\]

Nominal середнє загальний є:

\[
20\cdot6=120,
\]

тому результат біля one-half є правдоподібний.

<figure>
 <img src="figures/fig_04_monte_carlo_risk.svg" alt="Monte Carlo ризик розподіл">
 <figcaption><strong>Рис. 4.</strong> Monte Carlo answers distribution-level питання. спроможність поріг splits змодельованих сум into event і non-event результати.</figcaption>
</figure>

---

## 14. інтерпретація

коректний:

> за заданої моделі з незалежними однаково розподіленими обрізаними нормальними величинами, приблизно 50.21% змодельованих сум exceed 120.

Incorrect:

> реальний процес має точно 50.21% ризик.

моделювання оцінки наслідки припущень.

---

## 15. чому оптимізація є помилковий here

 поточний питання має немає decision змінна і немає цільова функція до максимізувати.

Adding оптимізація would answer another питання.

для приклад:

> що спроможність minimizes вартість subject до ризик нижче 5%?

це would legitimately combine моделювання і оптимізація.

---

# приклад E — мережа метод

## 16. Work graph

Edges:

- початок→, вага 3;
- початок→B, 4;
- →C, 5;
- B→C, 2;
- C→завершення, 4.

питання:

> який залежність шлях determines загальний тривалість?

Це graph-structure питання.

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
 <img src="figures/fig_05_network_path.svg" alt="критичний шлях mini-case">
 <figcaption><strong>Рис. 5.</strong> мережа метод uses залежність структура directly. Longest weighted DAG шлях є початок→→C→завершення, length 12.</figcaption>
</figure>

---

## 18. чому graph representation має значення

 тривалість table сам по собі може hide topology.

мережа representation preserves:

- node identity;
- edge напрям;
- залежність;
- шлях.

коли topology є питання, graph метод є natural.

---

# приклад F — MULTI-CRITERIA DECISION аналіз

## 19. альтернативи

| Alt | вартість | Time | надійність |
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

вартість/time є вартість критерії, надійність є виграш.

---

## 20. Ratio нормалізація

для вартість:

\[
r_{cost,i}=
\frac{\min(cost)}{cost_i}.
\]

для time:

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

## 21. Baseline ранжування

Approximate scores:

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
 <img src="figures/fig_06_mcda_ranking.svg" alt="MCDA ранжування mini-case">
 <figcaption><strong>Рис. 6.</strong> MCDA produces умовний ранжування за явний ваги і критерій directions. ранжування є не цільова функція property незалежний метод.</figcaption>
</figure>

---

## 22. MCDA versus оптимізація

LP chooses неперервний decision змінні за hard обмеження.

MCDA compares дискретний альтернативи за множинний критерії.

вони може coexist у larger decision workflow, але вони є не synonymous.

---

# вибір методу як дослідження REASONING

## 23. результат type є перший classifier

### Number

корінь, integral, параметр оцінка.

### формула

символьний вираз.

### оптимум

оптимізація.

### розподіл/ймовірність

Monte Carlo або statistical метод.

### шлях/структура

Graph/мережа метод.

### ранжування

MCDA.

 requested answer shape часто narrows метод choice immediately.

---

## 24. невизначеність є другий classifier

Ask:

> є вхідні дані або спостереження випадковий або uncertain?

якщо yes, probabilistic шар може бути required.

але Monte Carlo слід не бути added лише оскільки невизначеність “sounds науковий”.

Define випадковий змінні, distributions і припущення записані явноly.

---

## 25. обмеження є third classifier

якщо problem має цільова функція:

\[
F(x)\rightarrow\max
\]

subject до:

\[
g_i(x)\le0,
\]

оптимізація є natural class.

без decision цільова функція, оптимізація може бути category похибка.

---

## 26. мережа структура є fourth classifier

якщо relationships між entities determine результат, preserve them як graph структура.

Examples:

- проєкт залежності;
- communication topology;
- потік мережа;
- залежність graph.

---

## 27. множинний критерії є fifth classifier

коли альтернативи є judged за several non-equivalent критерії, один скалярний metric може require явний preference припущення.

MCDA makes them visible through:

- критерій directions;
- нормалізація;
- ваги;
- aggregation.

---

## 28. аналітичний benchmark є перевірка opportunity

Even коли final метод чисельний, ask:

> є там simpler точний приклад?

Examples:

- чисельний корінь checked за символьний корінь;
- чисельний ODE checked за замкнений форма;
- Monte Carlo checked against rough expectation;
- оптимізація checked за ручний corner точки.

Це reusable дослідження discipline.

---

## 29. метод, алгоритм, реалізація

Distinguish три levels.

### клас методу

чисельний пошук кореня.

### алгоритм

Brent метод.

### реалізація

SciPy root_scalar.

або:

### клас методу

лінійне програмування.

### алгоритм/backend

HiGHS.

### реалізація

SciPy linprog.

це distinction improves dissertation methodology language.

---

## 30. перевірка має match метод

| метод | перевірка |
|---|---|
| корінь | нев’язка |
| символьний | substitution/simplification |
| оптимізація | допустимість + цільова функція |
| Monte Carlo | початкове значення генератора + збіжність/range |
| мережа | ручний шлях validity/length |
| MCDA | directions + ваги + оцінка recomputation |

<figure>
 <img src="figures/fig_07_verification_matrix.svg" alt="перевірка матриця за метод">
 <figcaption><strong>Рис. 7.</strong> вибір методу includes перевірка selection. результат без method-specific перевірка є incomplete.</figcaption>
</figure>

---

## 31. Зламай вибір методу: hammer problem

якщо researcher knows один tool well, every problem може look like це tool.

 ймовірність питання forced into оптимізація є немає longer той самий дослідницьке питання.

 graph problem flattened into table може lose topology.

 ранжування питання reduced до один arbitrary оцінка може hide preferences.

 відмова є conceptual, не syntactic.

---

## 32. Зламай вибір методу: unnecessary complexity

 simple точний формула exists.

Researcher launches 100,000 Monte Carlo реалізації до оцінка той самий скалярний.

 результат може бути close, але adds:

- sampling noise;
- computational вартість;
- більше параметри.

Complexity слід earn its place.

---

## 33. Зламай вибір методу: exactness fetish

 символьний вираз може бути точний але uselessly великий.

якщо decision requires лише robust скалярний з допуск, чисельний метод може communicate better.

науковий rigor є не measured за вираз length.

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

кожний stage answers інший питання.

клас методуification є не приблизно choosing один метод forever.

це є приблизно choosing кожний метод deliberately.

---

## 35. Sequential метод escalation

 sensible strategy:

1. simplest baseline;
2. перевірити;
3. identify missing структура;
4. add метод шар;
5. перевірити again.

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

метод choice also depends на масштаб.

символьний solving може explode у complexity.

пошук на сітці може бутиcome impossible у високий dimension.

Monte Carlo може require багато реалізації.

Graph algorithms може масштаб well на sparse structures.

Computational допустимість belongs до метод justification.

---

## 37. Interpretability

інший методи expose інший свідчення.

символьний формула reveals dependence.

Monte Carlo reveals розподіл.

оптимізація reveals активні обмеження.

мережа метод reveals topology.

MCDA reveals trade-offs.

Choose метод according до що needs до бути explained, не лише computed.

---

## 38. прогнозувати до tool

до running кожний приклад, record expectation.

- корінь між 0 і 30.
- LP likely uses усі ресурс і бюджет.
- Monte Carlo ризик біля 0.5 оскільки середнє загальний≈спроможність.
- branch appears longer than B.
- C може lead MCDA due до time/надійність.

прогноз turns метод use into експеримент.

---

## 39. Python без fear: корінь

~~~python
root = numerical_root()
value = 120 - 6*root - 0.2*root**2
assert abs(value) < 1e-8
~~~

---

## 40. Python без fear: LP

~~~python
result = linear_optimization()
assert result["resource_used"] <= 100
assert result["budget_used"] <= 240
~~~

контрольний:

\[
F^*=680.
\]

---

## 41. Python без fear: Monte Carlo

~~~python
risk = monte_carlo_risk(
    n_runs=10000,
    seed=2026,
)
~~~

контрольний:

\[
risk\approx0.5021.
\]

---

## 42. Python без fear: мережа

~~~python
path, length = critical_path()
~~~

контрольний:

\[
Start\rightarrow A\rightarrow C\rightarrow Finish,
\]

\[
length=12.
\]

---

## 43. Python без fear: MCDA

~~~python
ranking = weighted_sum_decision()
~~~

контрольний:

\[
C>A>B.
\]

---

## 44. відтворюваність через клас методуes

кожний приклад слід record:

- вхідні дані;
- метод;
- параметри;
- Python реалізація;
- початкове значення генератора where relevant;
- перевірка;
- результат.

 точний метадані differs, але походження principle remains.

---

## 45. вибір методу table для dissertation

для кожний дослідження робота fill:

| питання | структура | результат | метод | альтернатива | перевірка |
|---|---|---|---|---|---|

це prevents methodology chapter від becoming list libraries.

---

## 46. альтернатива метод аналіз

Good дослідження explains не лише що було selected, але правдоподібний альтернативи.

приклад корінь:

- Brent: robust bracketed скалярний корінь;
- Newton: faster біля розв’язок але requires початок/похідна поведінка;
- SymPy: точний коли tractable.

Selection є argument.

---

## 47. коли методи disagree

припустімо символьний і чисельний корінь differ significantly.

не average them.

Investigate:

- помилковий рівняння;
- помилковий branch;
- допуск;
- область;
- coding похибка.

Disagreement є diagnostic свідчення.

---

## 48. коли методи agree

Agreement strengthens довірчий у реалізація.

але якщо обидва encode той самий помилковий припущення, область модель може усе ще бути помилковий.

це distinction repeats throughout курс.

---

## 49. синтетичний військовий context

 six приклади може represent abstract tasks such як поріг timing, training ресурс розподіл, uncertain синтетичний витрата, проєкт залежності і альтернатива selection.

немає реальний операційний дані є потрібний.

 transferable об’єкт є математичну структуру.

---

## 50. дослідження Transfer

для один dissertation fragment fill:

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

> оцінка параметри від зашумленими спостереженнями.

результат:

> параметр оцінки plus невизначеність.

кандидатний метод:

> нелінійний метод найменших квадратів plus бутстреп.

NetworkX would бути inappropriate unless graph структура actually exists.

метод justification має reference problem.

---

## 52. свідчення hierarchy

 strong результат includes:

1. valid вхідні дані;
2. justified метод;
3. verified обчислення;
4. чутливість/невизначеність коли потрібний;
5. bounded інтерпретація.

метод choice є лише один link у свідчення chain.

---

## 53. “найкращий метод” є contextual

Немає universal winner.

 метод є suitable relative до:

- питання;
- припущення;
- дані;
- результат;
- computational обмеження;
- перевірка opportunities.

Це чому класифікація є практичний methodology, не taxonomy trivia.

---

## 54. One-page підсумок

### Five ideas

1. Структура задачі selects метод.
2. результат type є перший classifier.
3. Python library є реалізація, не methodology.
4. перевірка має match клас методу.
5. Hybrid workflows є normal коли питання зміна.

### три rules

корінь:

\[
f(t^*)=0.
\]

оптимізація:

\[
F(x)\rightarrow\max
\quad\text{subject to constraints}.
\]

Monte Carlo:

\[
\hat p=\frac{events}{runs}.
\]

### два похибки

- familiar tool → forced метод;
- successful код → justified methodology.

### один питання

> що property my дослідження problem forces me до choose це метод?

### Next крок

Build:

\[
Question\rightarrow Method\rightarrow Tool\rightarrow Verification.
\]

<figure>
 <img src="figures/fig_08_research_transfer.svg" alt="дослідження transfer метод chain">
 <figcaption><strong>Рис. 8.</strong> вибір методу стає dissertation-ready коли chain від питання до перевірка є явний і reproducible.</figcaption>
</figure>

---

## 55. Фінальна думка

методи є не menu від який ми pick most sophisticated name.

вони є математичний answers до структурний питання.

 корінь метод finds нуля.

оптимізація finds найкращий допустимий decision.

Monte Carlo propagates невизначеність.

мережа метод exposes залежність структура.

MCDA formalizes multi-criteria preference.

символьна алгебра reveals точний структура.

 core competence є being able до say:

> **“My problem має це структура, тому це метод є appropriate, Це як I буде перевірити це, і ці є межі висновок.”**
