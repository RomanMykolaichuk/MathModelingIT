# MathModelingIT · Мінікнига T2.L6

## Системи комп'ютерної математики та їх можливості для математичного моделювання

### Від формули SymPy до незалежної чисельної перевірки

> **Головна ідея книги:** система комп’ютерної математики цінна не тим, що «вміє рахувати формули», а тим, що дозволяє пройти повний цикл: записати модель символічно, вивести структуру розв’язку, перевірити його алгебраїчно, перетворити на чисельну функцію, незалежно перевірити SciPy та провести параметричний експеримент.

---

## 0. Паспорт книги

**Код заняття:** T2.L6 
**Тема:** системи комп’ютерної математики та їх можливості 
**Рівень:** середній 
**Орієнтовний час читання:** 70–85 хвилин 
**Попередні знання:** похідна, інтеграл, просте ODE, Python функції, NumPy.

Після книги ви повинні вміти:

- задавати символьний змінні/функції у SymPy;
- формулювати differential рівняння;
- виводити рівновага;
- читати у замкненій формі розв’язок;
- виконувати символьний нев’язка перевірка;
- інтегрувати символьний вираз;
- обчислювати символьний чутливість;
- використовувати lambdify;
- незалежно перевіряти траєкторія через solve_ivp;
- оцінювати чисельний похибка;
- знаходити час досягнення порогу;
- проводити параметр чутливість;
- пояснювати, коли символьний розв’язок є перевагою, а коли чисельний метод необхідний.

---

## 1. Сцена: «Формула є. Але чому ми їй довіряємо?»

Уявімо синтетичний динамічний система.

Є стан \(S(t)\).

У систему постійно надходить ресурс з rate \(q\).

Втрати proportional до поточний стан:

\[
kS.
\]

Модель:

\[
\frac{dS}{dt}=q-kS.
\]

Початковий стан:

\[
S(0)=S_0.
\]

Хтось запускає SymPy й отримує формула.

І каже:

> «Готово. Комп’ютер дав розв’язок».

Але сильніший researcher запитає:

- чи формула satisfies ODE?
- чи початковий умова виконується?
- що означає рівновага?
- як параметр \(k\) впливає на стан?
- чи чисельний integrator дає ту саму траєкторія?
- що буде, якщо символьний розв’язок unavailable?

Саме ці питання перетворюють CAS із «калькулятора» на дослідження tool.

<figure>
 <img src="figures/fig_01_symbolic_numeric_pipeline.svg" alt="Symbolic-to-numeric pipeline">
 <figcaption><strong>Рис. 1.</strong> Сильний workflow: formulation → символьний розв’язок → символьний перевірка → lambdify → незалежний чисельний розв’язати → чутливість → інтерпретація.</figcaption>
</figure>

---

## 2. Центральна модель

\[
\frac{dS}{dt}=q-kS,
\qquad
S(0)=S_0.
\]

Де:

- \(S(t)\) — стан;
- \(q\) — сталий надходження;
- \(k>0\) — proportional втрата коефіцієнт;
- \(S_0\) — початковий стан.

модель є лінійний first-order ODE.

---

## 3. Інтуїція баланс law

Права частина:

\[
q-kS.
\]

Це:

> надходження − втрата.

Якщо:

\[
q>kS,
\]

стан зростає.

Якщо:

\[
q<kS,
\]

стан зменшується.

якщо equal:

\[
q=kS,
\]

стан перестає змінюватися.

Звідси отримуємо рівновага.

---

## 4. рівновага

У стані рівноваги:

\[
\frac{dS}{dt}=0.
\]

отже:

\[
q-kS^*=0.
\]

тому:

\[
S^*=\frac{q}{k}.
\]

Baseline:

\[
q=12,
\]

\[
k=0.10.
\]

тому:

\[
S^*=\frac{12}{0.1}=120.
\]

---

## 5. чому рівновага має значення

рівновага є не just algebraic intermediate.

це answers:

> до що рівень робить система tend якщо параметри remain сталий?

якщо:

\[
S_0<S^*,
\]

стан rises.

якщо:

\[
S_0>S^*,
\]

стан falls.

Baseline:

\[
S_0=20<120.
\]

Hence траєкторія rises toward 120.

<figure>
 <img src="figures/fig_02_equilibrium_direction.svg" alt="напрям toward рівновага">
 <figcaption><strong>Рис. 2.</strong> Знак \(q-kS\) визначає напрям руху стан: нижче рівновага траєкторія зростає, вище — спадає.</figcaption>
</figure>

---

## 6. у замкненій формі розв’язок

Аналітичний розв’язок:

\[
S(t)=
\frac{q}{k}
+
\left(
S_0-\frac{q}{k}
\right)e^{-kt}.
\]

Його структура дуже інформативна.

Перша частина:

\[
\frac{q}{k}=S^*
\]

— рівновага.

Друга:

\[
\left(S_0-S^*\right)e^{-kt}
\]

— перехідний deviation.

---

## 7. що exponential term means

\[
e^{-kt}
\]

decays toward нуля.

отже:

\[
S(t)\rightarrow S^*.
\]

параметр \(k\) controls швидкість згасання.

великий \(k\):

- сильніший proportional втрата;
- faster збіжність;
- lower рівновага \(q/k\).

тому \(k\) впливає і на рівень, і на швидкість.

---

## 8. початковий умова перевірка

At:

\[
t=0,
\]

\[
e^0=1.
\]

тому:

\[
S(0)=
\frac{q}{k}
+
\left(S_0-\frac{q}{k}\right)=S_0.
\]

Це simple ручний перевірка.

---

## 9. Baseline траєкторія

параметри:

\[
q=12,\quad
k=0.10,\quad
S_0=20.
\]

розв’язок:

\[
S(t)=120-100e^{-0.1t}.
\]

At:

\[
t=10
\]

ми get:

\[
S(10)\approx83.2121.
\]

Це source-of-truth перевірка значення.

<figure>
 <img src="figures/fig_03_baseline_trajectory.svg" alt="Baseline траєкторія toward рівновага">
 <figcaption><strong>Рис. 3.</strong> Baseline стан починається з 20 і монотонно наближається до рівновага 120. At \(t=10\), \(S\approx83.2121\).</figcaption>
</figure>

---

## 10. SymPy модель

символьний setup:

~~~python
t = sp.symbols("t", nonnegative=True)
q, k = sp.symbols("q k", positive=True)
S0 = sp.symbols("S0", nonnegative=True)
S = sp.Function("S")
~~~

ODE:

~~~python
ode = sp.Eq(
    sp.diff(S(t), t),
    q - k*S(t),
)
~~~

це код відтворює математичні позначення.

---

## 11. чому символьний припущення matter

ми declare:

\[
k>0.
\]

чому?

оскільки:

- рівновага потребує ділення на \(k\);
- модель зміст says proportional втрата додатний;
- simplification може use positivity.

символьні системи дають змогу краще міркувати коли припущення записані явно.

---

## 12. символьний рівновага

SymPy solves:

\[
q-kS_{eq}=0.
\]

результат:

\[
S_{eq}=\frac{q}{k}.
\]

Це не difficult manually.

 точка є не convenience.

 точка є creating символьний об’єкт, який можна використовувати далі.

---

## 13. символьний перевірка

Take кандидатний розв’язок \(S_c(t)\).

Compute нев’язка:

\[
R(t)=
\frac{dS_c}{dt}
-
(q-kS_c).
\]

якщо кандидатний є точний:

\[
R(t)=0.
\]

у код:

~~~python
residual = sp.simplify(
    sp.diff(solution, t)
    - (q - k*solution)
)
assert residual == 0
~~~

<figure>
 <img src="figures/fig_04_residual_verification.svg" alt="символьний нев’язка перевірка">
 <figcaption><strong>Рис. 4.</strong> нев’язка перевірка verifies рівняння structurally для символьний параметри, не лише at кількох числових точках.</figcaption>
</figure>

---

## 14. чому нев’язка перевірка сильніший than точкові перевірки

Припустімо, ми перевіряємо:

\[
t=0,5,10.
\]

Кандидатний розв’язок збігається у три точки.

Проте в інших точках він усе ще може бути неправильним.

символьний нев’язка:

\[
R(t)\equiv0
\]

перевірки identity за stated символьний припущення.

Це сильніший свідчення для алгебраїчної коректності.

---

## 15. але символьний нев’язка не validate реальний модель

нев’язка нуля proves:

> формула solves рівняння.

це не prove:

- рівняння describes реальний процес;
- q сталий;
- k сталий;
- proportional-loss припущення істинний.

Again:

> перевірка ≠ валідація.

---

## 16. символьний differentiation

рівновага:

\[
S^*=\frac{q}{k}.
\]

чутливість до \(q\):

\[
\frac{\partial S^*}{\partial q}
=
\frac{1}{k}.
\]

чутливість до \(k\):

\[
\frac{\partial S^*}{\partial k}
=
-\frac{q}{k^2}.
\]

ці formulas show структура до any числа.

---

## 17. Interpreting \(\partial S^*/\partial q\)

\[
\frac{1}{k}>0.
\]

рівновага grows коли надходження grows.

At:

\[
k=0.1,
\]

\[
\frac{\partial S^*}{\partial q}=10.
\]

Locally, +1 у q зміни рівновага за +10.

---

## 18. Interpreting \(\partial S^*/\partial k\)

\[
-\frac{q}{k^2}<0.
\]

Increasing втрата коефіцієнт lowers рівновага.

Baseline:

\[
-\frac{12}{0.1^2}=-1200.
\]

це великий похідна reflects units і масштаб.

не інтерпретувати magnitude без units.

---

## 19. Relative чутливість

Absolute похідна може look huge.

 dimensionless elasticity є часто корисний:

\[
E_k=
\frac{\partial S^*}{\partial k}
\frac{k}{S^*}.
\]

для:

\[
S^*=\frac{q}{k},
\]

ми get:

\[
E_k=-1.
\]

тому 1% increase у \(k\) gives approximately 1% decrease у рівновага.

Це часто більше interpretable.

---

## 20. символьний integration

Sometimes питання є не стан at moment.

ми need cumulative exposure:

\[
A(T)=\int_0^T S(t)\,dt.
\]

Analytically:

\[
A(T)=
\frac{q}{k}T
+
\left(
S_0-\frac{q}{k}
\right)
\frac{1-e^{-kT}}{k}.
\]

Baseline:

\[
A(10)\approx567.8794.
\]

---

## 21. що cumulative стан means

Depends на область.

може represent:

- accumulated availability;
- cumulative load;
- загальний exposure;
- area за стан curve.

у синтетичний заняття немає операційний інтерпретація є imposed.

 важливий idea:

> символьний розв’язок enables derived quantities.

---

## 22. час досягнення порогу

питання:

> коли робить \(S(t)\) перший reach target \(H\)?

розв’язати:

\[
H=
S^*+
(S_0-S^*)e^{-kt}.
\]

тоді:

\[
e^{-kt}
=
\frac{H-S^*}{S_0-S^*}.
\]

тому:

\[
t=
-\frac{1}{k}
\ln
\left(
\frac{H-S^*}{S_0-S^*}
\right).
\]

для:

\[
H=80
\]

baseline:

\[
t\approx9.1629.
\]

---

## 23. поріг validity

Target має lie між:

\[
S_0
\]

і:

\[
S^*.
\]

якщо target 150:

\[
150>120,
\]

baseline траєкторія never досягає це.

модель raises ValueError.

Це semantic валідація.

---

## 24. рівновага поріг

якщо target точно:

\[
H=S^*,
\]

траєкторія approaches asymptotically.

це не reach у скінченний time.

отже:

\[
t=\infty.
\]

Це beautiful приклад where математичний nuance має значення.

---

## 25. Lambdify bridge

символьний вираз корисний для reasoning.

але до plot arrays, use:

~~~python
fn = sp.lambdify(
    (t,q,k,S0),
    solution,
    modules="numpy",
)
~~~

Now:

~~~python
values = fn(times, 12, 0.1, 20)
~~~

це bridges символьний і чисельний worlds.

---

## 26. чому не rewrite формула manually

ми може manually код:

~~~python
seq = q/k
return seq + (s0-seq)*np.exp(-k*t)
~~~

поточний пакет має analytical_solution() точно like це.

але lambdify adds перевірка:

> символьний вираз і direct чисельний реалізація agree.

перевірка перевірки це.

---

## 27. незалежний чисельний розв’язок

Use solve_ivp на:

\[
\frac{dS}{dt}=q-kS.
\]

чисельний integrator не use у замкненій формі розв’язок.

тому це є partially незалежний computational pathway.

якщо trajectories agree, довірчий зростає.

---

## 28. solve_ivp setup

~~~python
def rhs(t, y):
    return [q - k*y[0]]

result = solve_ivp(
    rhs,
    (t0, t1),
    [s0],
    t_eval=times,
    rtol=1e-10,
    atol=1e-12,
)
~~~

Strict tolerances support високий agreement.

---

## 29. похибка metric

порівняти:

\[
e_i=
|S_{analytical}(t_i)-S_{numerical}(t_i)|.
\]

максимум:

\[
e_{max}=\max_i e_i.
\]

перевірка requires:

\[
e_{max}<10^{-6}.
\]

<figure>
 <img src="figures/fig_05_three_trajectories.svg" alt="аналітичний, lambdified і solve_ivp trajectories">
 <figcaption><strong>Рис. 5.</strong> аналітичний NumPy, lambdified SymPy і незалежний solve_ivp trajectories слід overlap within чисельний допуск.</figcaption>
</figure>

---

## 30. Agreement є свідчення, не proof адекватність

три implementations agree.

це supports:

- derivation;
- coding;
- чисельний integration.

не prove:

- модель структура коректний для реальний система.

це distinction repeats через курс.

---

## 31. параметр експеримент у k

Fix:

\[
q=12,
\]

\[
S_0=20.
\]

Vary:

\[
k\in
\{0.05,0.08,0.10,0.12,0.15\}.
\]

результати:

| k | S* | S(10) |
|---:|---:|---:|
| 0.05 | 240 | 106.56 |
| 0.08 | 150 | 91.59 |
| 0.10 | 120 | 83.21 |
| 0.12 | 100 | 75.90 |
| 0.15 | 80 | 66.61 |

---

## 32. чому рівновага decreases

формула:

\[
S^*=\frac{q}{k}.
\]

Increasing denominator reduces ratio.

похідна confirms:

\[
\frac{\partial S^*}{\partial k}<0.
\]

отже чисельний table, формула і похідна tell той самий story.

<figure>
 <img src="figures/fig_06_k_sensitivity.svg" alt="чутливість до втрата коефіцієнт k">
 <figcaption><strong>Рис. 6.</strong> Increasing \(k\) lowers обидва рівновага і \(S(10)\). символьний чутливість explains напрям до чисельний експеримент.</figcaption>
</figure>

---

## 33. чому S(10) є не simply рівновага

At скінченний time:

\[
S(10)\ne S^*
\]

unless система already У стані рівноваги або enough time passed.

перехідний term усе ще має значення.

тому:

- рівновага чутливість;
- finite-horizon чутливість

є related але distinct.

---

## 34. Time масштаб

Exponential decay characteristic time:

\[
\tau=\frac{1}{k}.
\]

Baseline:

\[
\tau=10.
\]

це gives інтуїція.

після several \(\tau\), перехідний стає малий.

Higher \(k\):

- smaller \(\tau\);
- faster збіжність.

---

## 35. Half-life deviation

Deviation:

\[
D(t)=S(t)-S^*.
\]

тоді:

\[
D(t)=D(0)e^{-kt}.
\]

Time для deviation halve:

\[
t_{1/2}=
\frac{\ln2}{k}.
\]

Baseline:

\[
t_{1/2}\approx6.93.
\]

Це another derived символьний insight.

---

## 36. CAS як структура explorer

SymPy helps ask:

- рівновага?
- похідна?
- integral?
- поріг рівняння?
- asymptotic поведінка?
- simplification?

Це більше valuable than лише чисельний substitution.

---

## 37. символьний вираз growth

не every модель yields elegant замкнений форма.

для нелінійний або coupled systems SymPy може:

- return implicit форма;
- return special функції;
- fail до розв’язати;
- generate huge вираз.

Це не відмова modeling.

це signals need для чисельний методи.

---

## 38. чисельний методи є не second-class

якщо символьний розв’язок unavailable, solve_ivp може усе ще бути коректний tool.

 goal є не:

> always знайти замкнений форма.

 goal:

> choose representation suitable для питання і перевірити це.

---

## 39. символьний порівняно з чисельний comparison

### символьний strengths

- точний структура;
- derivatives;
- integrals;
- simplification;
- параметр dependence.

### чисельний strengths

- complex моделі;
- нелінійний systems;
- time-varying коефіцієнти;
- великий systems;
- direct моделювання.

найкращий workflow часто combines обидва.

---

## 40. Зламай модель: k=0

модель assumes:

\[
k>0.
\]

якщо:

\[
k=0,
\]

рівновага формула:

\[
q/k
\]

undefined.

але ODE стає:

\[
\frac{dS}{dt}=q.
\]

розв’язок:

\[
S=S_0+qt.
\]

тому k=0 є не impossible процес.

це є outside поточний формула branch.

---

## 41. Зламай модель: q зміни з time

припустімо:

\[
q=q(t).
\]

тоді:

\[
\frac{dS}{dt}=q(t)-kS.
\]

замкнений форма може усе ще exist для simple q(t), але baseline формула немає longer valid.

Need re-derive.

---

## 42. Зламай модель: нелінійний втрата

припустімо:

\[
\frac{dS}{dt}=q-kS^2.
\]

рівновага:

\[
S^*=\sqrt{q/k}.
\]

Dynamics нелінійний.

інший чутливість і траєкторія.

Це genuine model-class зміна.

---

## 43. Зламай модель: затримка

припустімо втрата depends на past:

\[
\frac{dS}{dt}
=
q-kS(t-\tau).
\]

Now затримка differential рівняння.

Baseline ODE tools insufficient.

---

## 44. Зламай модель: поріг процес

втрата може activate лише коли:

\[
S>S_c.
\]

тоді piecewise модель.

символьний і чисельний approach зміни.

---

## 45. валідація hierarchy

<figure>
 <img src="figures/fig_07_verification_hierarchy.svg" alt="перевірка hierarchy">
 <figcaption><strong>Рис. 7.</strong> математичний derivation, нев’язка перевірка, lambdify agreement і solve_ivp agreement перевірити обчислення at інший levels; область адекватність remains separate питання.</figcaption>
</figure>

Levels:

1. formulate ODE;
2. derive розв’язок;
3. нев’язка=0;
4. початковий умова;
5. lambdify agreement;
6. solve_ivp agreement;
7. параметр експеримент plausibility;
8. область валідація.

---

## 46. Python без страху: рівновага

~~~python
value = equilibrium(
    q=12,
    k=0.1,
)
assert value == 120
~~~

контрольний перевірка.

---

## 47. Python без страху: стан t=10

~~~python
s10 = analytical_solution(
    10,
    q=12,
    k=0.1,
    s0=20,
)
~~~

очікуваний:

\[
83.2120558829.
\]

---

## 48. Python без страху: cumulative

~~~python
area = cumulative_state(
    10,
    q=12,
    k=0.1,
    s0=20,
)
~~~

очікуваний:

\[
567.8794411714.
\]

---

## 49. Python без страху: поріг

~~~python
t80 = threshold_time(
    80,
    q=12,
    k=0.1,
    s0=20,
)
~~~

очікуваний:

\[
9.1629073187.
\]

---

## 50. Python без страху: перевірка похибка

~~~python
err = max_symbolic_numeric_error(
    times,
    q=12,
    k=0.1,
    s0=20,
)
assert err < 1e-6
~~~

Це явний чисельний критерій.

---

## 51. прогнозувати до запуск

до чутливість table, прогнозувати.

якщо \(k\) зростає:

1. рівновага?
2. збіжність speed?
3. S(10)?
4. час досягнення порогу до 80?

Think до обчислення.

---

## 52. k affects два mechanisms

Increasing \(k\):

- lowers \(S^*=q/k\);
- makes експонента \(e^{-kt}\) decay faster.

ці effects може pull скінченний-стан на заданому горизонті у nontrivial ways через інший початковий conditions.

Baseline обидва support lower S(10).

---

## 53. сценарій: S0 вище рівновага

припустімо:

\[
S_0=180>S^*=120.
\]

тоді траєкторія decreases toward 120.

той самий формула.

це illustrates як початковий стан зміни напрям але не рівновага.

---

## 54. сценарій: S0 точно рівновага

\[
S_0=S^*.
\]

тоді перехідний коефіцієнт нуля:

\[
S_0-S^*=0.
\]

Hence:

\[
S(t)=S^*
\]

для усі t.

Це valuable контрольний приклад.

---

## 55. сценарій: q increase

якщо:

\[
q\uparrow,
\]

рівновага зростає linearly:

\[
S^*=\frac{q}{k}.
\]

похідна сталий для фіксований k:

\[
1/k.
\]

Це simpler чутливість than k.

---

## 56. параметр identifiability інтуїція

припустімо лише рівновага спостережуваний:

\[
S^*=120.
\]

багато pairs satisfy:

\[
q/k=120.
\]

для приклад:

\[
q=12,k=0.1
\]

і:

\[
q=24,k=0.2.
\]

рівновага сам по собі не може identify обидва.

траєкторія speed helps identify k.

Це deep дослідження insight від символьний структура.

---

## 57. чому time-series дані має значення

перехідний term:

\[
e^{-kt}
\]

contains k directly.

отже спостереження над time може distinguish параметр pairs з той самий рівновага.

символьний модель helps дизайн дані collection.

---

## 58. від solving до experimental дизайн

Це чому CAS має значення у дослідження.

це може reveal:

- який quantities depend на параметри;
- який спостереження identify them;
- який похідна є нуля/nonzero;
- який measurement горизонт informative.

символьний аналіз informs дизайн експерименту.

---

## 59. відтворюваність

 complete T2.L6 експеримент слід save:

- символьний форма;
- baseline параметри;
- time сітка;
- solve_ivp tolerances;
- comparison table;
- чутливість table;
- підсумок;
- код коміт.

тоді agreement може бути rebuilt.

---

## 60. чисельний допуск

solve_ivp uses:

\[
rtol=10^{-10},
\]

\[
atol=10^{-12}.
\]

ці є алгоритм settings.

вони influence чисельний похибка і runtime.

тому вони є part відтворюваність.

---

## 61. похибка поріг порівняно з точний equality

не assert:

\[
S_{analytical}=S_{numerical}
\]

bit-for-bit.

чисельний integration approximates.

Use допуск:

\[
e_{max}<10^{-6}.
\]

Це коректний computational reasoning.

---

## 62. Floating точка

Even аналітичний NumPy evaluation uses floating точка.

символьний вираз точний у algebraic форма.

чисельний substitution approximate.

це difference має значення.

---

## 63. символьний simplification hazards

Equivalent expressions може look інший.

приклад:

\[
S^*+(S_0-S^*)e^{-kt}
\]

і expanded форма.

String comparison є weak.

Use:

\[
sp.simplify(expr_1-expr_2)==0.
\]

це перевірки equivalence structurally.

---

## 64. модель аудит

### символьний аудит

- припущення записані явно?
- нев’язка нуля?
- початковий умова?

### чисельний аудит

- time сітка valid?
- розв’язувач успіх?
- допуск adequate?
- max похибка?

### чутливість аудит

- параметр range meaningful?
- trend explained за formulas?

### науковий аудит

- q/k meanings justified?
- сталий коефіцієнти правдоподібний?
- лінійний втрата adequate?

---

## 65. синтетичний військовий context

Imagine \(S(t)\) як abstract readiness-support стан у training моделювання.

\(q\) — синтетичний replenishment intensity.

\(kS\) — синтетичний proportional втрата.

немає actual readiness metric, logistics запас або операційний коефіцієнт є implied.

 purpose є математичну структуру лише.

---

## 66. дослідження Transfer

питання:

> Яку частину мого dissertation модель варто спочатку formalize symbolically, а яку перевірити numerically?

Template:

~~~text
Research question:

State variable:

Parameters:

Differential / algebraic relation:

Initial / boundary conditions:

Symbolic operations:

Expected equilibrium:

Sensitivity derivative:

Derived integral / threshold:

Numerical method:

Independent verification metric:

Parameter scenarios:

Data needed:

Limitations:

Allowed conclusion:
~~~

---

## 67. приклад дослідження Transfer

припустімо процес:

\[
\frac{dY}{dt}=a-bY.
\]

Symbolically derive:

- рівновага;
- перехідний;
- похідна wrt параметри.

Numerically:

- solve_ivp;
- порівняти;
- чутливість.

тоді calibrate,b від дані у later work.

---

## 68. коли символьний метод є especially корисний

- малий ODE;
- algebraic рівновага;
- точний derivatives;
- параметр relations;
- transformations;
- asymptotic аналіз.

---

## 69. коли чисельний метод є especially корисний

- нелінійний coupled systems;
- time-varying коефіцієнти;
- discontinuities;
- немає замкнений форма;
- великий стан dimension;
- data-driven моделювання.

---

## 70. Hybrid workflow

<figure>
 <img src="figures/fig_08_hybrid_method_map.svg" alt="Hybrid symbolic-numeric метод map">
 <figcaption><strong>Рис. 8.</strong> символьний і чисельний методи є complementary: символьний reasoning exposes структура, чисельний обчислення explores приклади where замкнений форма є unavailable або inconvenient.</figcaption>
</figure>

найкращий practice:

\[
Symbolic
\leftrightarrow
Numerical
\]

не competition.

---

## 71. Typical thinking похибки

### «SymPy gave формула → модель коректний»

немає.

формула може розв’язати помилковий рівняння.

### «нев’язка нуля → реальний система validated»

немає.

лише рівняння перевірка.

### «solve_ivp matches → два незалежний truths»

вони share той самий модель припущення.

### «більше digits → більше науковий»

немає.

Reporting точність має reflect дані/модель якість.

### «чисельний метод worse оскільки approximate»

немає.

часто це є лише практичний метод.

---

## 72. Allowed висновок

Strong:

> для синтетичний ODE \(dS/dt=q-kS\) з \(q=12,k=0.1,S_0=20\), символьний розв’язок gives рівновага 120, \(S(10)\approx83.2121\), cumulative стан над [0,10] ≈567.8794 і час досягнення порогу до 80 ≈9.1629. символьний нев’язка є точно нуля, і незалежний solve_ivp траєкторія agrees з аналітичний розв’язок within \(10^{-6}\) на tested сітка.

тоді limitation:

> ці перевірки перевірити математичний/computational реалізація, не адекватність сталий надходження і proportional-loss припущення для реальний система.

---

## 73. Від мінікнига до practice

практичний sequence:

1. define symbols;
2. write ODE;
3. derive розв’язок;
4. нев’язка перевірка;
5. рівновага;
6. чутливість derivatives;
7. integral;
8. lambdify;
9. solve_ivp;
10. похибка;
11. k scenarios;
12. інтерпретація.

---

## Поглиблення: dimensional аналіз до символьний manipulation

Перед тим як натискати \`solve\`, корисно перевірити units.

ODE:

\[
\frac{dS}{dt}=q-kS.
\]

якщо \(S\) measured у стан units і \(t\) у time, тоді:

\[
[q]=\frac{S}{t},
\]

і оскільки:

\[
[kS]=\frac{S}{t},
\]

ми need:

\[
[k]=\frac{1}{t}.
\]

тому:

\[
\frac{q}{k}
\]

має units \(S\), як required для рівновага.

це simple перевірка catches багато formulation похибки до any CAS work.

---

## Поглиблення: nondimensionalization

Define:

\[
s=\frac{S}{S^*},
\qquad
\tau=kt.
\]

оскільки:

\[
S^*=\frac{q}{k},
\]

 ODE стає:

\[
\frac{ds}{d\tau}=1-s.
\]

Now параметр \(q\) і \(k\) disappear від dimensionless dynamics.

розв’язок:

\[
s(\tau)=1+(s_0-1)e^{-\tau}.
\]

це reveals universal структура.

інший \(q,k\) приклади є scaled версії той самий normalized процес.

символьний tools help expose such simplifications.

---

## Поглиблення: чому nondimensionalization має значення

це може show:

- який параметр combinations truly matter;
- natural time масштаб;
- natural стан масштаб;
- як багато незалежний dimensionless groups remain.

у baseline:

\[
\tau=kt
\]

shows \(1/k\) є time масштаб.

\[
S^*=q/k
\]

є стан масштаб.

Це deeper than just computing числа.

---

## Поглиблення: стійкість рівновага

Let:

\[
u(t)=S(t)-S^*.
\]

тоді:

\[
\frac{du}{dt}=-ku.
\]

розв’язок:

\[
u(t)=u(0)e^{-kt}.
\]

Since \(k>0\):

\[
u(t)\rightarrow0.
\]

тому рівновага є asymptotically стійкий.

це висновок follows directly від transformed рівняння.

CAS може support algebra, але стійкість інтерпретація remains researcher’s робота.

---

## Поглиблення: якщо k < 0

поточний модель rejects \(k\le0\).

чому?

якщо \(k<0\), рівняння стає:

\[
\frac{dS}{dt}=q+|k|S.
\]

стан зростає exponentially.

 supposed “втрата коефіцієнт” стає gain.

тому вхідні дані валідація encodes область зміст.

Це good приклад semantic валідація, не лише numeric hygiene.

---

## Поглиблення: identifiability від рівновага лише

якщо лише long-run рівновага спостережуваний:

\[
S^*=120,
\]

тоді any pair satisfying:

\[
q=120k
\]

fits рівновага.

Examples:

\[
(12,0.1),
\]

\[
(24,0.2),
\]

\[
(6,0.05).
\]

тому рівновага дані сам по собі не може identify обидва параметри.

Це **структурний identifiability інтуїція**.

---

## Поглиблення: перехідний дані identify k

Normalized deviation:

\[
\frac{S(t)-S^*}{S_0-S^*}
=
e^{-kt}.
\]

Take log:

\[
\ln
\left|
\frac{S(t)-S^*}{S_0-S^*}
\right|
=
-kt.
\]

отже перехідний slope може reveal \(k\) коли рівновага відомий.

тоді:

\[
q=kS^*.
\]

це connects символьний derivation до experimental дизайн.

---

## Поглиблення: choosing спостереження times

якщо усі спостереження є taken very late:

\[
t\gg1/k,
\]

тоді:

\[
e^{-kt}\approx0.
\]

дані mostly show рівновага.

Information приблизно \(k\) від перехідний shape є weak.

якщо усі спостереження є too early, рівновага poorly constrained.

тому символьний структура підказує collecting дані через множинний time scales.

---

## Поглиблення: час досягнення порогу чутливість

поріг формула:

\[
t_H=
-\frac1k
\ln
\left(
\frac{H-S^*}{S_0-S^*}
\right).
\]

це depends на \(k\) обидва:

- directly through \(1/k\);
- indirectly through \(S^*=q/k\).

тому поріг чутливість може бути більше complex than рівновага чутливість.

чисельний параметр sweep може complement символьний differentiation.

---

## Поглиблення: cumulative стан як цільова функція або обмеження

\[
A(T)=\int_0^T S(t)\,dt.
\]

у future оптимізація problem, \((T)\) може become:

- цільова функція;
- обмеження;
- exposure metric.

отже символьний integration є не isolated exercise.

це може generate derived quantity використаний downstream.

---

## Поглиблення: аналітичний розв’язок як benchmark

коли замкнений форма exists, це provides excellent benchmark для чисельний розв’язувач.

Це rare privilege.

Use це до перевірка:

- допуск;
- крок choices;
- interpolation;
- реалізація.

тоді later, для модель з немає замкнений форма, you already trust чисельний pipeline більше.

---

## Поглиблення: чисельний похибка бюджет

Agreement критерій:

\[
e_{max}<10^{-6}.
\]

але загальний computational discrepancy може мають components:

- truncation похибка;
- розв’язувач допуск;
- interpolation;
- floating точка;
- time сітка.

 single допуск не explain усі похибка.

для baseline smooth ODE, solve_ivp з strict tolerances makes ці tiny.

---

## Поглиблення: збіжність study

 сильніший чисельний перевірка:

1. розв’язати з допуск набір;
2. розв’язати з tighter набір B;
3. порівняти trajectories;
4. перевірка стійкість key результати.

якщо результати stop changing materially, довірчий зростає.

Це чисельний збіжність свідчення.

---

## Поглиблення: time-grid independence

solve_ivp internally chooses adaptive steps.

\`t_eval\` лише requests результат точки.

якщо user зміни результат сітка від 121 до 61 точки, underlying integration може усе ще remain accurate.

але max похибка evaluated на сітка може зміна slightly.

отже перевірка metric itself depends на evaluation дизайн.

---

## Поглиблення: символьний вираз complexity

для larger systems, CAS може produce вираз тому великий це це є:

- hard до read;
- slow до evaluate;
- numerically unstable.

 замкнений форма є не automatically найкращий computational representation.

Sometimes чисельний розв’язок є більше корисний і reliable.

---

## Поглиблення: catastrophic cancellation

два algebraically equivalent expressions може бутимають differently numerically.

для very малий \(kt\), вираз:

\[
1-e^{-kt}
\]

може lose точність.

Special чисельний функції like \`expm1\` може бути better.

Це advanced reminder:

> символьний equivalence не guarantee identical floating-point стійкість.

---

## Поглиблення: символьний перевірка з припущення

Simplification може depend на припущення such як:

\[
k>0.
\]

без припущення, SymPy може keep умовний expressions або fail до reduce.

тому символьний модель слід declare відомий область restrictions.

це makes mathematics явний.

---

## Поглиблення: точний порівняно з floating-point constants

SymPy distinguishes:

\[
\frac{1}{10}
\]

від floating:

\[
0.1.
\]

точний rationals preserve algebraic exactness longer.

для символьний derivation, use точний objects where possible.

для чисельний evaluation, convert intentionally.

---

## Поглиблення: solving ODE з dsolve

один може ask SymPy:

~~~python
sp.dsolve(ode)
~~~

але курс модель constructs відомий замкнений форма directly після finding рівновага.

чому?

оскільки pedagogical goal є до understand структура:

\[
equilibrium + transient.
\]

Automatic dsolve може hide це reasoning.

CAS слід support thinking, не replace це.

---

## Поглиблення: нев’язка як reusable pattern

нев’язка перевірка generalizes.

для algebraic рівняння:

\[
f(x)=0,
\]

перевірка:

\[
f(x^*)\approx0.
\]

для PDE/ODE кандидатний:

\[
R=\mathcal L(u)-f.
\]

для оптимізація обмеження:

\[
g(x)\le0.
\]

нев’язка thinking є universal перевірка habit.

---

## Поглиблення: comparing незалежний representations

T2.L6 intentionally uses три representations:

1. символьний вираз;
2. hand-coded аналітичний NumPy;
3. solve_ivp чисельний integration.

якщо усі agree, common coding похибки менше likely.

Yet вони усе ще share той самий математичний припущення.

Це **реалізація triangulation**, не empirical валідація.

---

## Поглиблення: модель валідація would require дані

до validate ODE для реальний процес, ми would need спостереження:

\[
(t_i,S_i).
\]

тоді порівняти:

- predicted траєкторія;
- residuals;
- параметр оцінки;
- out-of-sample ефективність.

це moves beyond T2.L6 into калібрування і дослідження workflow.

---

## Поглиблення: модель калібрування link до T2.L7

припустімо \(q,k\) unknown.

Given дані, оцінка:

\[
\hat q,\hat k.
\]

тоді:

1. calibrate;
2. assess residuals;
3. quantify невизначеність;
4. перевірити чисельний розв’язок;
5. прогнозувати thresholds/integrals.

Це точно як символьний структура стає part науковий modeling.

---

## Поглиблення: чутливість beyond один параметр

поточний експеримент varies \(k\) з фіксований \(q\).

може build сітка:

\[
q\in\{8,12,16\},
\quad
k\in\{0.05,0.1,0.15\}.
\]

тоді study відгук surface:

\[
S(10;q,k).
\]

це exposes interactions у finite-time результат even though ODE лінійний у S.

---

## Поглиблення: contour map

 contour:

\[
S(10;q,k)
\]

shows combinations yielding той самий скінченний-стан на заданому горизонті.

це може reveal параметр trade-offs.

це also helps explain identifiability: один спостереження може correspond до багато параметр pairs.

---

## Поглиблення: невизначеність propagation

якщо:

\[
q\sim distribution,
\quad
k\sim distribution,
\]

тоді even точний формула produces uncertain:

\[
S(t),S^*,t_H.
\]

символьний розв’язок makes repeated evaluation cheap.

отже символьний work може accelerate Monte Carlo невизначеність propagation.

---

## Поглиблення: символьний чутливість і Monte Carlo complement кожний other

похідна gives локальний вплив:

\[
\frac{\partial S^*}{\partial k}.
\]

Monte Carlo параметр невизначеність gives глобальний розподіл.

Use похідна для локальний understanding.

Use моделювання для broader невизначеність.

Neither universally replaces other.

---

## Поглиблення: break-the-model checklist

Ask:

1. є q сталий?
2. є k сталий?
3. є losses proportional до S?
4. є там затримка?
5. є там thresholds?
6. є система one-dimensional?
7. є спостереження noisy?
8. є параметри відомий?
9. є стан неперервний?

кожний “немає” підказує модель розширення.

---

## Поглиблення: research-safe військовий приклад

один може describe \(S(t)\) як синтетичний training-support indicator.

не map q, k, S0 до actual операційний capacities без authorized дані і область justification.

 transferable заняття є:

\[
balance\ law
\rightarrow
equilibrium
\rightarrow
transient
\rightarrow
verification
\rightarrow
sensitivity.
\]

---

## Поглиблення: reporting точність

тести store:

\[
83.2120558829.
\]

Text reports:

\[
83.2121.
\]

Це intentional.

Regression тести need tight значення.

Human інтерпретація не need ten decimal places.

точність слід match purpose.

---

## Поглиблення: compact свідчення table

| твердження | свідчення |
|---|---|
| формула solves ODE | символьний нев’язка = 0 |
| початковий умова коректний | substitution \(t=0\) |
| рівновага 120 | \(q/k\) |
| чисельний реалізація коректний | lambdify/direct agreement |
| ODE integration коректний | solve_ivp похибка < \(10^{-6}\) |
| k trend understood | похідна + сценарій table |
| реальний система adequate | **не established за заняття** |

це table prevents overclaiming.

---

## Поглиблення: від символьний insight до дослідження дизайн

символьний аналіз може зміна не лише як ми розв’язати модель, але що експеримент ми дизайн.

для baseline:

\[
S^*=\frac{q}{k}.
\]

це tells us рівновага identifies ratio \(q/k\), не параметри separately.

перехідний:

\[
e^{-kt}
\]

tells us early-time дані contain information приблизно \(k\).

отже символьний структура підказує:

- collect equilibrium-like late дані;
- collect перехідний early дані.

Це приклад mathematics guiding measurement strategy.

---

## Поглиблення: чутливість як experimental priority

якщо:

\[
\left|\frac{\partial output}{\partial \theta}\right|
\]

є very малий через relevant range, precise estimation \(\theta\) може matter менше для це результат.

якщо похідна великий, параметр невизначеність strongly affects прогноз.

чутливість може guide where до invest measurement effort.

---

## Поглиблення: локальний порівняно з глобальний чутливість

символьний похідна є локальний.

для larger параметр зміни, нелінійний вплив може differ.

тому pair:

- символьний похідна;
- параметр sweep.

це combination appears repeatedly у good modeling practice.

---

## Поглиблення: параметр sweep матриця

для q і k:

| q | k | S* | S(10) |
|---:|---:|---:|---:|
| 8 |.08 | 100 |... |
| 12 |.08 | 150 |... |
| 16 |.08 | 200 |... |
| 8 |.12 | 66.7 |... |
| 12 |.12 | 100 |... |

це table shows обидва структурний формула і finite-time вплив.

---

## Поглиблення: символьний limit аналіз

ми може inspect межі.

як:

\[
t\rightarrow\infty,
\]

\[
S(t)\rightarrow q/k.
\]

як:

\[
k\rightarrow\infty
\]

для фіксований q і t>0, рівновага tends до нуля.

як:

\[
k\rightarrow0^+,
\]

поточний у замкненій формі вираз має terms це look singular, але limit corresponds до linear-growth ODE.

Limit аналіз може expose альтернатива branches.

---

## Поглиблення: checking limit k→0

Original ODE з k=0:

\[
S=S_0+qt.
\]

 символьний limit у замкненій формі вираз може recover це.

Це powerful consistency перевірка і good CAS exercise.

---

## Поглиблення: series expansion

для малий \(kt\):

\[
e^{-kt}
\approx
1-kt+\frac{(kt)^2}{2}-\cdots.
\]

Substitute into розв’язок до get short-time approximation.

Leading поведінка:

\[
S(t)\approx
S_0+(q-kS_0)t.
\]

це matches початковий похідна від ODE.

Another символьний consistency перевірка.

---

## Поглиблення: локальний linearization нелінійний моделі

у future нелінійний ODE:

\[
\dot x=f(x),
\]

рівновага \(x^*\) може бути studied using похідна/Jacobian:

\[
J=\frac{\partial f}{\partial x}\Big|_{x^*}.
\]

T2.L6 лінійний приклад prepares це idea.

---

## Поглиблення: Jacobian для поточний модель

\[
f(S)=q-kS.
\]

похідна:

\[
\frac{df}{dS}=-k.
\]

оскільки:

\[
-k<0,
\]

рівновага стійкий.

Це simplest possible Jacobian стійкість аналіз.

---

## Поглиблення: символьний матриця моделі

для vector стан:

\[
\dot{\mathbf x}=A\mathbf x+\mathbf b.
\]

CAS може help:

- eigenvalues;
- рівновага;
- матриця exponential;
- символьний Jacobian.

чисельний методи тоді handle larger systems.

T2.L6 скалярний приклад є foundation.

---

## Поглиблення: stiffness preview

Some ODE systems contain very інший time scales.

тоді явний чисельний integrators може struggle.

розв’язувач choice стає важливий.

поточний модель є не stiff.

але hybrid символьний/чисельний reasoning helps detect time scales.

---

## Поглиблення: event detection натомість у замкненій формі поріг

для complex ODE where поріг формула unavailable, solve_ivp може detect event:

\[
S(t)-H=0.
\]

отже threshold_time concept generalizes від analytic algebra до чисельний event функції.

---

## Поглиблення: comparing поріг методи

для baseline:

1. аналітичний поріг формула;
2. чисельний event detection.

якщо вони agree, event реалізація verified.

це може бутиcome future розширення.

---

## Поглиблення: cumulative integral numerically

Similarly порівняти:

- символьний cumulative_state();
- чисельний quadrature траєкторія.

це provides another незалежний перевірка channel.

---

## Поглиблення: triangulation дизайн

 rich валідація матриця:

| Quantity | символьний | Direct NumPy | SciPy |
|---|---|---|---|
| S(t) | замкнений форма | analytical_solution | solve_ivp |
| integral | integrate | cumulative_state | quadrature |
| поріг | розв’язати algebra | threshold_time | event detection |
| чутливість | diff | скінченний difference | сценарій sweep |

Agreement через rows strengthens реалізація свідчення.

---

## Поглиблення: finite-difference чутливість перевірка

символьний:

\[
dS^*/dk=-q/k^2.
\]

чисельний скінченний difference:

\[
\frac{S^*(k+h)-S^*(k-h)}{2h}.
\]

порівняти для малий h.

це перевірки символьний похідна і чисельний реалізація.

---

## Поглиблення: choosing h

Too великий:

- truncation похибка.

Too малий:

- floating-point cancellation.

Це classic чисельний аналіз trade-off.

CAS похідна avoids finite-difference approximation коли точний вираз доступний.

---

## Поглиблення: documentation припущення beside formulas

 формула слід не travel сам по собі.

для:

\[
S(t)=S^*+(S_0-S^*)e^{-kt}
\]

store припущення:

- q сталий;
- k сталий >0;
- one-dimensional стан;
- немає delays;
- початковий умова S0;
- детермінований dynamics.

це prevents later misuse.

---

## Поглиблення: символьний notebooks і джерело files

ноутбук є ідеальний для displaying SymPy derivation.

але reusable функції слід live у src/model.py.

той самий principle як T1.L3.

це enables тести і CI.

---

## Поглиблення: CAS versioning

SymPy simplification/printing може зміна через версії.

математичний equivalence може remain.

тому тести слід prefer структурний equivalence:

\[
simplify(expr_1-expr_2)=0
\]

rather than точний string formatting.

---

## Поглиблення: публікація формула перевірка

до placing формула у article:

1. derive symbolically;
2. simplify;
3. нев’язка перевірка;
4. render LaTeX;
5. порівняти notation з manuscript.

це reduces transcription похибки між код і paper.

---

## 74. One-page підсумок

### П’ять головних ідей

1. CAS exposes математичну структуру.
2. нев’язка нуля verifies символьний розв’язок.
3. Lambdify bridges символьний і чисельний representations.
4. solve_ivp provides незалежний чисельний перевірка.
5. перевірка рівняння є не валідація реальний припущення.

### Три формули

\[
S^*=\frac{q}{k}.
\]

\[
S(t)=S^*+(S_0-S^*)e^{-kt}.
\]

\[
\frac{\partial S^*}{\partial k}
=
-\frac{q}{k^2}.
\]

### Дві помилки

- «SymPy solved це = дослідження complete»;
- «чисельний match = реальний модель adequate».

### Одне питання

> Яку структурний information моя символьний модель може reveal до I launch чисельний експеримент?

### Наступний крок

Reproduce baseline, перевірити нев’язка, порівняти solve_ivp і запуск k-sensitivity.

---

## 75. Фінальна думка

Computer algebra і чисельний методи є strongest together.

символьний шар answers:

> що робить модель imply structurally?

чисельний шар answers:

> що happens для ці параметри і scenarios?

перевірка шар asks:

> робити незалежний representations agree?

дослідження шар asks:

> є припущення meaningful для об’єкт?

 mature computational модель moves through усі four layers.

це є реальний capability T2.L6 є designed до build.
