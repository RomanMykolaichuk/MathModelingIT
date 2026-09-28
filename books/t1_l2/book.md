# MathModelingIT — мінікнига T1.L2

## Класифікація математичних моделей

### Один об’єкт — чотири способи побачити невизначеність

> **Головна ідея книги:** класифікація математичних моделей потрібна не для запам’ятовування термінів. Вона допомагає зрозуміти, що саме модель вважає відомим, що вважає випадковим, як описує зміну стану, який тип результату повертає і які висновки після цього дозволено робити.

---

## 0. Паспорт книги

**Код заняття:** T1.L2  
**Тема:** класифікація математичних моделей  
**Рівень:** вступний → середній  
**Орієнтовний час читання:** 65–80 хвилин  
**Попередні знання:** базова алгебра, графік функції, середнє та стандартне відхилення.

Після цієї книги ви повинні вміти:

- класифікувати модель за кількома ознаками одночасно;
- пояснювати різницю між детермінованою і стохастичною моделями;
- відрізняти траєкторію від розподілу;
- пояснювати роль рівняння стану;
- відрізняти неперервний і дискретний у часі опис;
- розуміти метод Монте-Карло як експеримент над моделлю, а не «прогноз майбутнього»;
- використовувати початкове зерно генератора для відтворюваності;
- розрізняти вплив середнього значення та вплив мінливості;
- пояснювати, чому один об’єкт може мати кілька математичних моделей;
- формулювати допустимий висновок відповідно до класу моделі.

---

## 1. Сцена: «Скільки часу вистачить ресурсу?»

Уявімо умовний навчальний підрозділ, який має запас певного ресурсу.

Початковий запас:

\[
S_0=120.
\]

Середнє споживання:

\[
\bar v=6
\]

одиниць за один крок часу.

На перший погляд задача проста:

> «120 поділити на 6 — отже, ресурсу вистачить на 20 кроків».

Математично:

\[
t^*=\frac{120}{6}=20.
\]

Але далі виникають питання.

Чи справді кожний крок споживання дорівнює рівно 6?

Що, якщо в одному кроці 4.5, в іншому 7.2, у третьому 5.8?

Що означає «вистачить на 20», якщо реальний процес випадковий?

Чи потрібна нам одна прогнозована лінія?

Чи одна змодельована траєкторія?

Чи розподіл можливих моментів вичерпання?

Усі ці питання стосуються одного об’єкта — запасу ресурсу.

Але відповіді вимагають різних **класів моделей**.

<figure>
  <img src="figures/fig_01_one_object_many_models.svg" alt="Один об’єкт у кількох класах моделей">
  <figcaption><strong>Рис. 1.</strong> Один і той самий ресурс можна описати детерміновано, стохастично, як дискретний процес стану або як експеримент Монте-Карло. Клас моделі визначає тип відповіді.</figcaption>
</figure>

---

## 2. Класифікація — не ярлик, а набір припущень

Коли ми називаємо модель:

> детермінована,

ми фактично стверджуємо:

> за однакових вхідних даних модель повертає той самий результат.

Коли називаємо:

> стохастична,

додаємо:

> хоча вхідні параметри однакові, реалізація може змінюватися через випадкову складову.

Коли говоримо:

> динамічна,

стверджуємо:

> стан системи змінюється у часі.

Коли:

> дискретна,

час або оновлення стану відбувається кроками.

Отже, класифікація — це короткий спосіб описати **структуру припущень**.

---

## 3. Основні осі класифікації

Одна модель може належати одразу до кількох класів.

Наприклад:

> стохастична, dynamic, discrete, імітаційна модель.

Ключові осі класифікації:

### Детерміновані / стохастичні

Чи є випадковість?

### Статичні / динамічні

Чи змінюється стан?

### Неперервні / дискретні

Час і зміна стану описуються неперервно чи кроками?

### Лінійні / нелінійні

Зв’язки між змінними лінійні чи нелінійні?

### Аналітичні / імітаційні

Чи можна отримати аналітичний результат у замкненій формі, чи потрібне обчислювальне моделювання?

### Описові / оптимізаційні

Модель описує систему чи шукає найкраще рішення?

Ці осі не взаємовиключні.

---

## 4. Детермінована модель запасу

Найпростіша:

\[
S(t)=\max(0,S_0-vt).
\]

Де:

- \(S(t)\) — залишок;
- \(S_0\) — початковий запас;
- \(v\) — стала інтенсивність споживання;
- \(t\) — час.

Для:

\[
S_0=120,\qquad v=6
\]

маємо:

\[
S(t)=\max(0,120-6t).
\]

При:

\[
t=5
\]

залишок:

\[
S(5)=90.
\]

При:

\[
t=20
\]

маємо:

\[
S(20)=0.
\]

Результат — **одна траєкторія**.

---

## 5. Час вичерпання

Якщо:

\[
v>0,
\]

то:

\[
t^*=\frac{S_0}{v}.
\]

Базовий сценарій:

\[
t^*=20.
\]

Якщо:

\[
v=0,
\]

модель повертає:

\[
t^*=\infty.
\]

Це корисний граничний випадок.

Він змушує запитати:

> чи має нескінченний час предметний сенс, чи це лише математичне позначення «за таких припущень ресурс не витрачається»?

---

## 6. Неперервна модель

Формула:

\[
S(t)=S_0-vt
\]

визначена для будь-якого real \(t\ge0\).

Наприклад:

\[
t=3.7.
\]

Це неперервний у часі description.

Але реальний процес може вимірюватися лише раз на добу, зміну, цикл або iteration.

Тоді зручніше discrete model.

<figure>
  <img src="figures/fig_02_continuous_vs_discrete.svg" alt="Continuous і discrete representation">
  <figcaption><strong>Рис. 2.</strong> Continuous model описує state у будь-який момент часу; discrete model оновлює state кроками. Вони можуть описувати той самий process на різних рівнях деталізації.</figcaption>
</figure>

---

## 7. Discrete динамічна модель

Запис:

\[
S_{k+1}=\max(0,S_k-C_k).
\]

Де:

- \(S_k\) — stock на кроці \(k\);
- \(C_k\) — consumption на цьому кроці.

Manual control case:

\[
S_0=20.
\]

Consumptions:

\[
[5,7,10].
\]

Отримуємо:

\[
S_1=15,
\]

\[
S_2=8,
\]

\[
S_3=0.
\]

Trajectory:

\[
[20,15,8,0].
\]

Це control case у tests.

---

## 8. Чому dynamic state важливий

У динамічна модель наступний result залежить від попереднього:

\[
S_{k+1}=f(S_k,C_k).
\]

System має memory через state.

Якщо на ранньому кроці consumption було великим, усі наступні states стартують із меншого stock.

Це відрізняє dynamic process від static formula, де output обчислюється без accumulation history.

---

## 9. Стохастичне споживання

Тепер припустимо:

\[
C_k\sim\mathcal N(\mu,\sigma^2).
\]

Базовий сценарій:

\[
\mu=6,
\]

\[
\sigma=1.5.
\]

Оскільки negative consumption предметно беззмістовне, lesson model робить:

\[
C_k=\max(0,C_k).
\]

Це вже стохастична модель.

Однакові parameters не гарантують однакову sequence.

---

## 10. Що означає \(\mu\)

\[
\mu=6
\]

не означає:

> кожне consumption = 6.

Це center розподіл.

Окремі draws можуть бути:

- 4.7;
- 6.3;
- 7.5;
- 5.1.

У long sample average tends toward model mean.

---

## 11. Що означає \(\sigma\)

Standard deviation:

\[
\sigma
\]

контролює spread.

При:

\[
\sigma=0.5
\]

values tightly cluster around 6.

При:

\[
\sigma=3.0
\]

spread much wider.

Mean може залишатися 6.

Отже:

> зміна mean і зміна мінливість — різні model interventions.

<figure>
  <img src="figures/fig_03_mean_vs_variance.svg" alt="Вплив mean і standard deviation">
  <figcaption><strong>Рис. 3.</strong> Зміна \(\mu\) пересуває центр розподіл, а зміна \(\sigma\) змінює ширину. Ці два ефекти не треба змішувати.</figcaption>
</figure>

---

## 12. Одна stochastic траєкторія

Для одного зерно генератора генерується конкретна sequence:

\[
C_1,C_2,\ldots,C_{21}.
\]

Після цього отримуємо one stock path.

Інший зерно генератора → інша sequence → інша path.

Але це не означає, що одна path «правильна», а інша «помилкова».

Обидві — realizations тієї самої стохастична модель.

---

## 13. Seed і відтворюваність

Pseudo-random generator deterministic відносно зерно генератора.

Тому:

~~~python
a = stochastic_consumption(..., seed=123)
b = stochastic_consumption(..., seed=123)
~~~

дають однаковий result.

Це перевіряється unit test.

Seed потрібний, щоб:

- повторити experiment;
- debug code;
- порівняти сценарійs;
- відтворити figure.

Seed не робить стохастична модель більш «реалістичною».

---

## 14. Дві траєкторії — два можливі світи

У experiment використовуються:

- зерно генератора=7;
- зерно генератора=21.

Дві stochastic paths відрізняються.

Deterministic path — одна straight-like базовий сценарій траєкторія.

<figure>
  <img src="figures/fig_04_paths.svg" alt="Детермінована і дві стохастичні траєкторії">
  <figcaption><strong>Рис. 4.</strong> Deterministic model дає одну траєкторію. Stochastic model при різних зерно генератораs дає різні realizations, хоча \(\mu,\sigma,S_0\) однакові.</figcaption>
</figure>

Найважливіше питання:

> чи достатньо однієї random realization, щоб оцінити risk?

Ні.

---

## 15. Від stochastic path до Монте-Карло

Монте-Карло повторює стохастична модель багато разів.

Для run \(r\):

\[
T^{(r)}
\]

— exhaustion step.

Виконуємо:

\[
r=1,\ldots,N.
\]

Базовий сценарій:

\[
N=3000.
\]

У кожному run:

1. генерується нова random consumption sequence;
2. будується state path;
3. фіксується first zero;
4. якщо zero не досягнутий до horizon — записується missing/NaN.

---

## 16. Монте-Карло не змінює model assumptions

Важливий principle.

Якщо consumption розподіл неправильно обрана, 3000 runs не виправлять її.

Якщо independence assumption неправильна, 1 000 000 runs не зроблять result адекватним.

Монте-Карло лише точніше досліджує **наслідки заданої стохастична модель**.

> **More simulations ≠ better model.**

---

## 17. Probability exhausted

Після simulations:

\[
\hat p=
\frac{\text{runs exhausted within horizon}}
{N}.
\]

Для базовий сценарій з:

- horizon=21;
- N=3000;
- зерно генератора=2026

lesson дає приблизно:

\[
\hat p\approx0.80.
\]

Коректне формулювання:

> за заданої stochastic consumption model приблизно 80% simulated realizations вичерпують stock до кінця 21-го кроку.

Некоректне:

> ресурс «з імовірністю 80% точно закінчиться».

---

## 18. Conditional mean exhaustion step

Function summarize_exhaustion() бере лише finite exhaustion times.

Тобто mean:

\[
\bar T_{finite}
\]

є conditional mean:

> середній exhaustion step **серед тих runs, де exhaustion відбулося в horizon**.

Baseline близько:

\[
20.1.
\]

Це не unconditional expected lifetime.

Це важливе distinction.

---

## 19. Censoring intuition

Runs без exhaustion до horizon записані NaN.

Вони містять інформацію:

> \(T>21\).

Якщо просто викинути їх і дивитися лише mean finite times, можна недооцінити невизначеність.

Тому probability_exhausted і conditional timing потрібно показувати разом.

У складніших задачах це пов’язано з censoring / survival analysis.

---

## 20. Histogram

Histogram exhaustion steps показує розподіл finite outcomes.

<figure>
  <img src="figures/fig_05_monte_carlo_histogram.svg" alt="Monte Carlo distribution exhaustion step">
  <figcaption><strong>Рис. 5.</strong> Монте-Карло замінює одну прогнозовану точку розподіл можливих outcomes. Histogram треба читати разом із часткою runs без exhaustion у horizon.</figcaption>
</figure>

Вісь X:

> exhaustion step.

Вісь Y:

> number of simulated runs.

Histogram не є probability law real system.

Він є empirical розподіл generated by model.

---

## 21. Класифікація чотирьох representations

### Model 1

\[
S(t)=S_0-vt.
\]

- deterministic;
- dynamic;
- continuous;
- linear until clipping;
- analytical.

### Model 2

\[
C_k\sim N(\mu,\sigma^2).
\]

- stochastic;
- discrete draws;
- probabilistic component.

### Model 3

\[
S_{k+1}=\max(0,S_k-C_k).
\]

- dynamic;
- discrete;
- nonlinear because of clipping;
- stochastic if \(C_k\) stochastic.

### Model 4

3000 repeated runs.

- simulation / Монте-Карло;
- stochastic;
- produces розподіл-level summary.

---

## 22. Один об’єкт — різні дослідницьке питанняs

Deterministic question:

> коли resource reaches zero за constant rate?

Stochastic single-run question:

> як може виглядати одна realization?

Монте-Карло question:

> який розподіл exhaustion outcomes under assumed невизначеність?

Dynamic question:

> як state evolves step by step?

Клас model повинен відповідати question.

Не навпаки.

---

## 23. Static vs dynamic

Static model може описувати relation:

\[
Y=f(X)
\]

без explicit time evolution.

Dynamic model:

\[
S_{k+1}=f(S_k,\ldots).
\]

У нашому lesson central object naturally dynamic.

Але classification axis still useful: не кожне дослідницьке питання потребує траєкторія.

---

## 24. Analytical vs simulation

Deterministic exhaustion:

\[
t^*=\frac{S_0}{v}
\]

отримуємо analytically.

Монте-Карло probability closed-form тут не використовується.

Ми estimate через repeated simulation.

Це не означає, що simulation «гірша».

Вона відповідає на інший class question.

---

## 25. Linear vs nonlinear detail

До clipping:

\[
S(t)=S_0-vt
\]

linear in time.

Але:

\[
\max(0,S_0-vt)
\]

piecewise linear.

Discrete:

\[
S_{k+1}=\max(0,S_k-C_k)
\]

також має nonlinear clipping.

Classification іноді залежить від того, яку частину model structure аналізуємо.

---

## 26. Descriptive vs optimization

T1.L2 models описують process.

Вони не шукають:

\[
\max F(x)
\]

або:

\[
\min C(x).
\]

Отже, це descriptive/імітаційна модельs.

Якщо додати decision:

> який запас \(S_0\) мінімізує cost при risk constraint,

model перетворюється на optimization.

---

## 27. Scenario: low variance

Залишимо:

\[
\mu=6,
\]

але:

\[
\sigma=0.5.
\]

Expected direction:

- paths closer together;
- exhaustion розподіл narrower;
- deterministic траєкторія becomes stronger central reference.

Не обов’язково every simulation exhausts exactly at 20.

---

## 28. Scenario: high variance

\[
\sigma=3.
\]

Expected:

- wider траєкторія spread;
- more early and late exhaustion outcomes;
- greater невизначеність.

Mean consumption assumption remains same.

Це experiment on **мінливість**, not mean.

<figure>
  <img src="figures/fig_06_variance_scenarios.svg" alt="Сценарії low і high variance">
  <figcaption><strong>Рис. 6.</strong> За однакового mean higher \(\sigma\) розширює family можливих trajectories та outcomes. Зміна невизначеність не тотожна зміні expected level.</figcaption>
</figure>

---

## 29. Scenario: higher mean

\[
\mu=7.
\]

Deterministic analogue:

\[
t^*=\frac{120}{7}\approx17.14.
\]

Тобто center process shifts toward earlier depletion.

Це інший effect, ніж:

\[
\sigma\uparrow.
\]

---

## 30. Mean effect vs variance effect

Це одне з головних conceptual distinctions lesson.

### Mean increases

Distribution generally shifts.

### Variance increases

Distribution generally spreads.

У nonlinear/clipped process ці effects можуть взаємодіяти.

Тому не варто робити висновок лише за \(\mu\) і \(\sigma\) inputs — потрібен computational experiment.

---

## 31. Effect clipping at zero consumption

Normal розподіл theoretically permits negative draws.

Model applies:

\[
C_k=\max(0,C_k).
\]

Це changes розподіл.

При базовий сценарій:

\[
\mu=6,\sigma=1.5
\]

negative probability small.

При large \(\sigma\) clipping matters more.

Отже, стохастична модель is not exactly normal consumption after transformation.

Це хороший “break” point.

---

## 32. Зламай модель: very high variance

Припустимо:

\[
\sigma=10.
\]

Тоді raw normal draws often negative.

Clipping creates pile-up at zero.

Distribution becomes strongly distorted.

Question:

> чи нормальний розподіл із clipping still plausible domain model?

Можливо, краще:

- lognormal;
- gamma;
- truncated normal.

---

## 33. Зламай модель: independence

Current draws independent.

Але real consumption може мати autocorrelation.

High consumption today → high tomorrow.

Тоді:

\[
Corr(C_k,C_{k+1})>0.
\]

Independent model може underestimate clusters of heavy use.

Modernization:

- autoregressive process;
- regime-switching;
- block sampling.

---

## 34. Зламай модель: constant parameters

Baseline assumes:

\[
\mu,\sigma
\]

constant over horizon.

Але process may change by phase.

Наприклад:

\[
\mu_k=
\begin{cases}
5,&k<10\\
8,&k\ge10.
\end{cases}
\]

Тоді stationary стохастична модель inadequate.

---

## 35. Зламай модель: no replenishment

Current рівняння стану:

\[
S_{k+1}=\max(0,S_k-C_k).
\]

Якщо є replenishment \(Q_k\):

\[
S_{k+1}=
\max(0,S_k+Q_k-C_k).
\]

Це вже інша динамічна модель.

---

## 36. Зламай модель: horizon too short

Якщо horizon=10, більшість runs не exhausted.

Probability exhausted low.

Finite mean may describe only rare early cases.

Тоді conditional summary easily misread.

Horizon is part of experiment design.

---

## 37. Verification: deterministic control

Test:

\[
S(0)=120,
\]

\[
S(5)=90,
\]

\[
S(20)=0.
\]

Такі simple controls protect mathematical implementation.

---

## 38. Verification: manual discrete path

Input:

\[
20;\quad [5,7,10].
\]

Expected:

\[
[20,15,8,0].
\]

Якщо code returns other path, problem is not stochastic complexity.

Problem is core оновлення стану.

---

## 39. Verification: відтворюваність

Same зерно генератора must produce same draws.

Test uses:

\[
seed=123.
\]

This is regression evidence for RNG процес.

---

## 40. Verification: range

Stock:

\[
S_k\ge0.
\]

Probability:

\[
0\le\hat p\le1.
\]

These are invariant checks.

---

## 41. Python без страху: deterministic

~~~python
t = np.arange(0, 22)
stock = deterministic_stock(
    t,
    initial_stock=120,
    rate=6,
)
~~~

Код прямо відповідає:

\[
S(t)=\max(0,120-6t).
\]

---

## 42. Python без страху: stochastic path

~~~python
params = ResourceModelParams(
    initial_stock=120,
    mean_consumption=6,
    std_consumption=1.5,
    horizon=21,
)

stock, consumption = stochastic_stock_path(
    params,
    seed=7,
)
~~~

Змінюючи зерно генератора, ми змінюємо realization, не model parameters.

---

## 43. Python без страху: Монте-Карло

~~~python
times = monte_carlo_exhaustion_times(
    params,
    n_runs=3000,
    seed=2026,
)

summary = summarize_exhaustion(times)
~~~

Summary:

- probability_exhausted;
- mean finite exhaustion step;
- median finite exhaustion step.

---

## 44. Predict before Run

Перед experiment запишіть.

### Prediction A

Що буде при:

\[
\sigma=0.5?
\]

### Prediction B

Що буде при:

\[
\sigma=3?
\]

### Prediction C

Що буде при:

\[
\mu=7?
\]

Не потрібно вгадувати exact numbers.

Потрібно прогнозувати:

- shift;
- spread;
- probability direction.

---

## 45. Research interpretation

Strong conclusion:

> За deterministic assumptions \(S_0=120,v=6\) depletion time equals 20. Under stochastic independent clipped-normal consumption with \(\mu=6,\sigma=1.5\), horizon 21, 3000 runs and зерно генератора 2026, model estimates depletion within horizon at about 0.80. This is a property of the specified simulation assumptions, not a direct empirical probability of a real process.

Це conclusion with scope.

---

## 46. Типові помилки мислення

### «Deterministic model неправильна, бо reality random»

Не обов’язково.

Вона може бути useful базовий сценарій.

### «Монте-Карло більш реалістична автоматично»

Ні.

Realism depends on assumptions.

### «Одна random траєкторія — forecast»

Ні.

Це realization.

### «Mean exhaustion ≈20.1 означає, що ресурс закінчиться на 20.1»

Ні.

Це summary conditional finite runs.

### «Seed 2026 додає достовірність»

Ні.

Він додає відтворюваність.

---

## 47. Від моделі до лабораторія

Для цього заняття повний browser лабораторія ще не реалізований.

Тому мінікнига формує теоретичну основу перед Python experiment.

До практики потрібно спрогнозувати:

1. low variance;
2. high variance;
3. higher mean;
4. short horizon.

Потім перевірити predictions у notebook/Python.

---

## 48. Від мінікнига до Python

Python package реалізує:

- deterministic_stock();
- deterministic_exhaustion_time();
- stochastic_consumption();
- discrete_stock_path();
- stochastic_stock_path();
- exhaustion_step();
- monte_carlo_exhaustion_times();
- summarize_exhaustion().

Тобто мінікнига пояснює structure, а package дозволяє reproduce calculations.

---

## 49. Research Transfer

Поставте питання:

> Який один об’єкт мого дисертаційного дослідження можна описати двома різними класами моделей?

Шаблон:

~~~text
Research question:

Object:

State variable:

Deterministic model:

Source of randomness:

Stochastic model:

Dynamic state equation:

Simulation output:

Seed / reproducibility:

Verification case:

Uncertainty:

Limitations:

Allowed conclusion:
~~~

---

## 50. Приклад Research Transfer

Припустимо досліджується processing time information requests.

Deterministic version:

\[
T=n\bar t.
\]

Stochastic version:

\[
T=\sum_i T_i.
\]

Монте-Карло:

> розподіл total processing time.

Це лише structural example.

Parameters мають походити з actual/synthetic justified data.

---

## 51. Model selection map

<figure>
  <img src="figures/fig_07_model_selection_map.svg" alt="Карта вибору класу моделі">
  <figcaption><strong>Рис. 7.</strong> Вибір класу починається з дослідницьке питання: чи важлива мінливість, state evolution, optimization або розподіл outcomes.</figcaption>
</figure>

Questions:

- Need only базовий сценарій? → deterministic.
- Need path over steps? → dynamic.
- Randomness important? → stochastic.
- Need risk розподіл? → simulation/Монте-Карло.
- Need best decision? → optimization extension.

---

## 52. Класифікація як мова методології

Коли у дисертації написано:

> «побудовано стохастичну дискретну динамічну імітаційну model»,

читач повинен зрозуміти:

- state changes stepwise;
- transition contains randomness;
- results obtained computationally;
- conclusion likely розподіл-level.

Classification must explain method.

Не decorate text.

---

## 53. Reproducibility package T1.L2

Збережіть:

- model code;
- parameter values;
- horizon;
- зерно генератора;
- n_runs;
- сценарій table;
- generated paths;
- Монте-Карло output;
- summary;
- software versions;
- commit.

Тоді probability estimate has identity.

---

## 54. What Монте-Карло proves

Монте-Карло can show:

> consequences of assumptions.

It does not prove:

- chosen розподіл is correct;
- parameters represent real system;
- future will match simulated frequency;
- independent draws are adequate.

This boundary must be explicit.

---

## 55. Синтетичний військовий контекст

Наш «ресурс» не є real ammunition, fuel, coordinates or classified stock.

Це synthetic stock for training.

Такий design дозволяє вивчити:

- depletion;
- невизначеність;
- state;
- risk

без sensitive data.

Transfer to real work requires separate data governance and domain валідація.

---

## Поглиблення: однаковий mean не означає однаковий risk

Розглянемо дві hypothetical consumption models.

### Model A

\[
C_k\sim N(6,0.5^2).
\]

### Model B

\[
C_k\sim N(6,3^2).
\]

В обох:

\[
E[C_k]=6.
\]

Якщо дивитися лише на mean, вони здаються однаковими.

Але розподіл of cumulative consumption:

\[
\sum_{k=1}^{n}C_k
\]

відрізняється.

У Model B значно вища мінливість.

Отже, risk early exhaustion може змінюватися навіть при незмінному expected consumption.

Це фундаментальна причина, чому deterministic mean-based model не може автоматично замінити stochastic analysis.

---

## Поглиблення: law of large numbers не робить один run representative

Можна почути:

> «Якщо mean = 6, то за 21 step average consumption буде майже 6».

У середньому across many experiments — так.

Але один finite realization може відхилитися.

Law of large numbers говорить про convergence sample average при великому n.

Вона не гарантує:

> кожна коротка realization близька до mean.

Для horizon=21 мінливість все ще може суттєво впливати на depletion.

---

## Поглиблення: невизначеність accumulates

State:

\[
S_n=
\max\left(
0,
S_0-\sum_{k=1}^{n}C_k
\right).
\]

Навіть якщо each \(C_k\) має modest мінливість, sum мінливість accumulates.

Для independent variables without clipping approximately:

\[
Var\left(\sum C_k\right)
=
n\sigma^2.
\]

Standard deviation sum:

\[
\sigma_{sum}=\sqrt n\,\sigma.
\]

Тобто невизначеність grows with horizon.

Це пояснює, чому stochastic paths diverge from deterministic базовий сценарій as time proceeds.

---

## Поглиблення: correlation changes accumulated невизначеність

If consumptions correlated:

\[
Var\left(\sum C_k\right)
=
\sum Var(C_k)
+
2\sum_{i<j}Cov(C_i,C_j).
\]

Positive covariance increases cumulative variance.

Thus iid assumption matters.

Two models can have same:

- \(\mu\);
- \(\sigma\);

but different autocorrelation and therefore different depletion risk.

This is a powerful example of hidden structural assumption.

---

## Поглиблення: normal розподіл and domain

Why normal?

It is mathematically convenient.

But consumption is non-negative.

Normal has support:

\[
(-\infty,\infty).
\]

Clipping repairs impossible negative draws operationally, but changes розподіл.

Alternative positive розподілs:

- lognormal;
- gamma;
- truncated normal.

Which one is appropriate depends on data and mechanism.

No розподіл should be chosen only because NumPy makes it easy.

---

## Поглиблення: probability as model-conditional frequency

When we report:

\[
\hat p\approx0.80,
\]

the full statement should mentally include:

> conditional on \(S_0=120\), clipped-normal iid consumption with \(\mu=6,\sigma=1.5\), horizon 21, and this implementation.

This long condition often disappears in prose.

мінікнига trains habit of keeping it visible.

---

## Поглиблення: Монте-Карло sampling error

Even if стохастична модель fixed, estimated probability varies with finite N.

If true model probability is \(p\), approximate standard error:

\[
SE(\hat p)
\approx
\sqrt{\frac{p(1-p)}{N}}.
\]

For:

\[
p\approx0.8,
\quad
N=3000,
\]

roughly:

\[
SE\approx
\sqrt{\frac{0.8\cdot0.2}{3000}}
\approx0.0073.
\]

This does not measure model невизначеність.

It measures simulation sampling невизначеність.

Very important distinction:

- parameter/model невизначеність;
- Монте-Карло error.

---

## Поглиблення: increasing N

If N increases fourfold:

\[
N\rightarrow4N,
\]

Монте-Карло standard error halves approximately because:

\[
SE\propto\frac{1}{\sqrt N}.
\]

So precision improves slowly.

To reduce SE by factor 10, need about 100× runs.

This is why number of simulations should be justified, not chosen mystically.

---

## Поглиблення: convergence diagnostic

A useful computational experiment:

1. run N=100;
2. N=300;
3. N=1000;
4. N=3000;
5. N=10000.

Plot:

\[
\hat p_N
\]

versus N.

If estimate stabilizes, simulation numerical precision improving.

But again:

> convergence of \(\hat p_N\) does not validate the stochastic assumptions.

---

## Поглиблення: horizon and censoring

Suppose true depletion time exceeds 21 in some runs.

We observe only:

\[
T>21.
\]

That is right-censoring conceptually.

If horizon extended to 30:

- more runs become finite;
- probability_exhausted increases or stays same;
- conditional mean finite times changes.

Therefore summary depends on horizon.

Horizon is not merely a plotting choice.

It is part of дослідницьке питання.

---

## Поглиблення: compare probability across horizons

Define:

\[
p(H)=P(T\le H).
\]

Then:

\[
p(H)
\]

is cumulative розподіл function of depletion time under model.

Instead of one horizon 21, evaluate:

\[
H=18,19,20,21,22,24.
\]

This gives richer risk curve.

A single 0.80 becomes a function.

---

## Поглиблення: quantile of exhaustion time

If enough runs exhausted, one may estimate:

\[
Q_{0.5},
Q_{0.9}
\]

for finite or full time-to-event representation.

But handling non-exhausted runs needs care.

Simply dropping them changes interpretation.

This is why advanced analysis may use survival methods.

---

## Поглиблення: детермінована модель as expected-value proxy

It is tempting to say:

\[
S_{det}(t)=E[S_{stoch}(t)].
\]

With clipping and nonlinear state boundary this is not generally exact.

Because:

\[
E[\max(0,X)]\ne \max(0,E[X]).
\]

This is a key nonlinear expectation issue.

Thus deterministic path using середнє споживання is not automatically mean stochastic stock path.

---

## Поглиблення: Jensen-style intuition

Nonlinear transformations mean:

\[
E[f(X)]\ne f(E[X]).
\]

Clipping:

\[
f(x)=\max(0,x)
\]

is nonlinear.

Therefore deterministic substitution of mean parameters can differ from ensemble mean.

This is one reason simulation adds information.

---

## Поглиблення: сценарій table for клас моделіes

| Research need | Suitable базовий сценарій class | Main output |
|---|---|---|
| nominal depletion | deterministic continuous | one time |
| state by step | discrete dynamic | one траєкторія |
| one possible uncertain path | stochastic dynamic | realization |
| risk by horizon | Монте-Карло | probability |
| розподіл of timing | Монте-Карло | розподіл |
| choose best reserve | optimization extension | decision |

This table is not universal.

It is a decision aid.

---

## Поглиблення: model hierarchy instead of model competition

Do not replace детермінована модель with stochastic and throw first away.

Use hierarchy:

1. deterministic базовий сценарій;
2. stochastic extension;
3. dynamic simulation;
4. невизначеність analysis.

Each layer answers new questions.

The simpler model remains useful for перевірка здорового глуздуs.

---

## Поглиблення: calibration question

Where do:

\[
\mu=6,\sigma=1.5
\]

come from?

In course — synthetic.

In research they might be estimated from historical data.

Then невизначеність in estimates matters.

If sample small, \(\mu,\sigma\) themselves uncertain.

Монте-Карло with fixed estimated parameters underrepresents total невизначеність.

---

## Поглиблення: posterior/predictive idea

Advanced extension:

Instead of fixed:

\[
\mu,\sigma,
\]

sample parameters from невизначеність розподіл, then sample consumption.

This creates predictive невизначеність including parameter невизначеність.

Not required in T1.L2.

But conceptually important:

> stochastic observations and uncertain parameters are different layers.

---

## Поглиблення: break-the-model map

<figure>
  <img src="figures/fig_08_limits.svg" alt="Межі baseline stochastic model">
  <figcaption><strong>Рис. 8.</strong> Baseline iid clipped-normal model can fail when consumption is autocorrelated, parameters change over time, replenishment exists, or horizon creates strong censoring.</figcaption>
</figure>

A mature model description should state which failure modes are plausible.

---

## Поглиблення: верифікація vs валідація

Verification asks:

> did we implement equations correctly?

Examples:

- manual path;
- same зерно генератора;
- nonnegative stock.

Validation asks:

> do assumptions represent target process sufficiently?

Examples:

- розподіл fit;
- autocorrelation;
- parameter stability;
- replenishment dynamics.

Монте-Карло can be perfectly verified and poorly validated.

---

## Поглиблення: відтворюваність of stochastic results

To reproduce probability estimate preserve:

- code;
- зерно генератора;
- N;
- parameters;
- horizon;
- RNG library/version if exact identity matters.

If only statistical відтворюваність needed, exact same raw draws may be less important.

But course emphasizes exact computational traceability.

---

## Поглиблення: safe military interpretation

In real military research, stochastic resource modeling may involve sensitive data.

This мінікнига deliberately avoids:

- actual stock levels;
- real consumption rates;
- location;
- mission timelines.

Transfer should preserve mathematical pattern while using authorized or synthetic data.

The mathematical lesson survives without operational detail.

---

## Поглиблення: вибір класу моделі як наукове рішення

Клас моделі не слід обирати за принципом:

> «Монте-Карло сучасніше, тому використаємо Монте-Карло».

Правильніший порядок:

1. дослідницьке питання;
2. type of невизначеність;
3. time representation;
4. available data;
5. required output;
6. верифікація strategy.

Наприклад, якщо question:

> яка nominal траєкторія при fixed rate?

Монте-Карло зайва.

If question:

> яка ймовірність depletion before horizon?

Deterministic model alone insufficient.

Method complexity повинна відповідати information need.

---

## Поглиблення: epistemic і aleatory невизначеність

Корисно розрізняти два conceptual types.

### Aleatory

Variability modeled as inherent randomness.

Example:

\[
C_k\sim distribution.
\]

### Epistemic

Uncertainty because we do not know parameters/model structure well.

Example:

\[
\mu\in[5.5,6.5].
\]

Монте-Карло over \(C_k\) captures aleatory layer.

It does not automatically capture невизначеність about \(\mu\), \(\sigma\) or розподіл family.

This distinction becomes important in dissertation conclusions.

---

## Поглиблення: deterministic сценарій can represent epistemic alternatives

Suppose uncertain mean:

\[
\mu\in\{5,6,7\}.
\]

Instead of one стохастична модель, run three parameter сценарійs.

Then within each сценарій optionally perform Монте-Карло.

This creates nested structure:

\[
Parameter\ scenario
\rightarrow
Stochastic\ realizations.
\]

This is clearer than mixing all невизначеність into one undifferentiated розподіл.

---

## Поглиблення: ensemble mean траєкторія

With many Монте-Карло paths compute:

\[
\bar S_k=
\frac{1}{N}
\sum_{r=1}^{N}S_k^{(r)}.
\]

Also quantiles:

\[
Q_{0.1}(S_k),
\quad
Q_{0.9}(S_k).
\]

Then plot band over time.

This answers:

> how does невизначеність of state evolve?

It is richer than only exhaustion histogram.

---

## Поглиблення: невизначеність band is not confidence interval by default

A 10–90% simulation quantile band describes model-generated outcome розподіл.

It is not automatically:

> 80% confidence interval for true state.

Confidence terminology relates to inferential невизначеність of estimated quantities.

Use precise language.

---

## Поглиблення: event definition matters

Event:

\[
T\le21
\]

differs from:

\[
S_{21}<10.
\]

Both can be risk metrics.

Before simulation define event precisely.

Otherwise same model can produce multiple “probabilities” that answer different questions.

---

## Поглиблення: базовий сценарій as reference, not truth

Deterministic T=20 is useful because:

- easy to compute;
- easy to verify;
- provides scale.

But stochastic analysis may show wide розподіл.

Do not use базовий сценарій as truth and stochastic values as “errors”.

They are outputs of different клас моделіes.

---

## Поглиблення: сценарій comparison design

Good table:

| Scenario | \(\mu\) | \(\sigma\) | Horizon | Question |
|---|---:|---:|---:|---|
| базовий сценарій | 6 | 1.5 | 21 | control |
| stable | 6 | 0.5 | 21 | мінливість ↓ |
| high_var | 6 | 3 | 21 | мінливість ↑ |
| high_mean | 7 | 1.5 | 21 | level shift |
| long_horizon | 6 | 1.5 | 30 | censoring effect |

This makes each run interpretable.

---

## Поглиблення: comparing розподілs

Beyond mean/median, compare:

- probability by horizon;
- quantiles;
- spread;
- tail frequency.

Two сценарійs can have same mean exhaustion but different tails.

Risk analysis often cares about tails.

---

## Поглиблення: tail risk

Suppose two models have mean depletion step 20.

Model A tightly clustered around 20.

Model B sometimes depletes at 15 and sometimes at 25.

Same mean, different early-failure risk.

Therefore mean alone can hide operationally relevant невизначеність.

---

## Поглиблення: стохастична модель верифікація

Verification can include:

- same зерно генератора same draws;
- different зерно генератораs usually differ;
- sample length correct;
- nonnegative draws after clipping;
- state monotone non-increasing when no replenishment;
- exhaustion step first zero;
- NaN only if no exhaustion.

These are invariants.

---

## Поглиблення: валідація with data

If real authorized data available, inspect:

- histogram;
- autocorrelation;
- time trend;
- seasonal/regime effects;
- fit of candidate розподілs.

Then choose stochastic structure.

Simulation should come after data understanding.

---

## Поглиблення: model comparison as dissertation evidence

One useful research design:

1. deterministic базовий сценарій;
2. iid стохастична модель;
3. autocorrelated стохастична модель;
4. compare predictive/diagnostic performance.

Then classification itself becomes substantive research tool.

---

## Поглиблення: military-safe synthetic сценарій

Suppose resource is “computational capacity units” for a training exercise.

Consumption varies by simulation load.

This preserves:

- depletion logic;
- невизначеність;
- state transition;
- Монте-Карло risk,

without revealing real operational stocks.

This is appropriate for an open teaching repository.

---

## 56. Одна сторінка підсумку

### П’ять головних ідей

1. Classification captures model assumptions.
2. Deterministic траєкторія and stochastic розподіл answer different questions.
3. Dynamic model has state memory.
4. Монте-Карло explores невизначеність defined by the model.
5. Seed supports відтворюваність, not realism.

### Три правила

Deterministic:

\[
S(t)=\max(0,S_0-vt).
\]

Dynamic:

\[
S_{k+1}=\max(0,S_k-C_k).
\]

Монте-Карло estimate:

\[
\hat p=\frac{n_{event}}{N}.
\]

### Дві помилки

- one stochastic realization = forecast;
- more simulations = more adequate model.

### Одне питання

> Який class model відповідає моєму дослідницьке питання, а не просто моєму улюбленому Python tool?

### Наступний крок

Запустіть базовий сценарій, повторіть same зерно генератора, змініть \(\mu\) і \(\sigma\) окремо та поясніть різницю.

---

## 57. Фінальна думка

Один і той самий process може мати кілька математичних моделей.

Це не contradiction.

Це нормальна властивість modeling.

Детермінована model дає базовий сценарій.

Stochastic model вводить невизначеність.

Dynamic model показує evolution state.

Монте-Карло формує розподіл outcomes.

Сильний дослідник не питає:

> «яка модель правильна взагалі?»

Він питає:

> **яка model structure потрібна, щоб коректно відповісти саме на моє дослідницьке питання — і які висновки вона після цього дозволяє зробити?**
