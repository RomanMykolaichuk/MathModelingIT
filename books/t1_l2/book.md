# MathModelingIT MiniBook T1.L2

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
- пояснювати різницю між deterministic і stochastic model;
- відрізняти trajectory від distribution;
- пояснювати роль state equation;
- відрізняти continuous-time і discrete-time description;
- розуміти Monte Carlo як експеримент над моделлю, а не «прогноз майбутнього»;
- використовувати seed для reproducibility;
- розрізняти mean effect і variability effect;
- пояснювати, чому один об’єкт може мати кілька математичних моделей;
- формулювати allowed conclusion відповідно до класу моделі.

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

units за один крок часу.

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

Чи одна simulated trajectory?

Чи distribution можливих моментів вичерпання?

Усі ці питання стосуються одного об’єкта — запасу ресурсу.

Але відповіді вимагають різних **класів моделей**.

<figure>
  <img src="figures/fig_01_one_object_many_models.svg" alt="Один об’єкт у кількох класах моделей">
  <figcaption><strong>Рис. 1.</strong> Один і той самий ресурс можна описати детерміновано, стохастично, як discrete state process або як Monte Carlo experiment. Клас моделі визначає тип відповіді.</figcaption>
</figure>

---

## 2. Класифікація — не ярлик, а набір припущень

Коли ми називаємо модель:

> deterministic,

ми фактично стверджуємо:

> за однакових inputs model повертає той самий output.

Коли називаємо:

> stochastic,

додаємо:

> хоча inputs parameters однакові, realization може змінюватися через random component.

Коли говоримо:

> dynamic,

стверджуємо:

> стан системи змінюється у часі.

Коли:

> discrete,

час або state update відбувається кроками.

Отже, classification — це короткий спосіб описати **структуру assumptions**.

---

## 3. Основні осі класифікації

Одна модель може належати одразу до кількох класів.

Наприклад:

> stochastic, dynamic, discrete, simulation model.

Ключові axes:

### Deterministic / stochastic

Чи є randomness?

### Static / dynamic

Чи змінюється state?

### Continuous / discrete

Час і state evolution описуються неперервно чи кроками?

### Linear / nonlinear

Relations між variables linear чи nonlinear?

### Analytical / simulation

Можна отримати closed-form result чи потрібне computational imitation?

### Descriptive / optimization

Модель описує system чи шукає best decision?

Ці axes не взаємовиключні.

---

## 4. Детермінована модель запасу

Найпростіша:

\[
S(t)=\max(0,S_0-vt).
\]

Де:

- \(S(t)\) — залишок;
- \(S_0\) — initial stock;
- \(v\) — constant consumption rate;
- \(t\) — time.

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

Результат — **одна trajectory**.

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

Baseline:

\[
t^*=20.
\]

Якщо:

\[
v=0,
\]

model повертає:

\[
t^*=\infty.
\]

Це корисний boundary case.

Він змушує запитати:

> чи має нескінченний час предметний сенс, чи це лише математичне позначення «за таких assumptions ресурс не витрачається»?

---

## 6. Continuous model

Формула:

\[
S(t)=S_0-vt
\]

визначена для будь-якого real \(t\ge0\).

Наприклад:

\[
t=3.7.
\]

Це continuous-time description.

Але реальний процес може вимірюватися лише раз на добу, зміну, цикл або iteration.

Тоді зручніше discrete model.

<figure>
  <img src="figures/fig_02_continuous_vs_discrete.svg" alt="Continuous і discrete representation">
  <figcaption><strong>Рис. 2.</strong> Continuous model описує state у будь-який момент часу; discrete model оновлює state кроками. Вони можуть описувати той самий process на різних рівнях деталізації.</figcaption>
</figure>

---

## 7. Discrete dynamic model

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

У dynamic model наступний result залежить від попереднього:

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

Baseline:

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

Це вже stochastic model.

Однакові parameters не гарантують однакову sequence.

---

## 10. Що означає \(\mu\)

\[
\mu=6
\]

не означає:

> кожне consumption = 6.

Це center distribution.

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

> зміна mean і зміна variability — різні model interventions.

<figure>
  <img src="figures/fig_03_mean_vs_variance.svg" alt="Вплив mean і standard deviation">
  <figcaption><strong>Рис. 3.</strong> Зміна \(\mu\) пересуває центр distribution, а зміна \(\sigma\) змінює ширину. Ці два ефекти не треба змішувати.</figcaption>
</figure>

---

## 12. Одна stochastic trajectory

Для одного seed генерується конкретна sequence:

\[
C_1,C_2,\ldots,C_{21}.
\]

Після цього отримуємо one stock path.

Інший seed → інша sequence → інша path.

Але це не означає, що одна path «правильна», а інша «помилкова».

Обидві — realizations тієї самої stochastic model.

---

## 13. Seed і reproducibility

Pseudo-random generator deterministic відносно seed.

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
- порівняти scenarios;
- відтворити figure.

Seed не робить stochastic model більш «реалістичною».

---

## 14. Дві траєкторії — два можливі світи

У experiment використовуються:

- seed=7;
- seed=21.

Дві stochastic paths відрізняються.

Deterministic path — одна straight-like baseline trajectory.

<figure>
  <img src="figures/fig_04_paths.svg" alt="Детермінована і дві стохастичні траєкторії">
  <figcaption><strong>Рис. 4.</strong> Deterministic model дає одну траєкторію. Stochastic model при різних seeds дає різні realizations, хоча \(\mu,\sigma,S_0\) однакові.</figcaption>
</figure>

Найважливіше питання:

> чи достатньо однієї random realization, щоб оцінити risk?

Ні.

---

## 15. Від stochastic path до Monte Carlo

Monte Carlo повторює stochastic model багато разів.

Для run \(r\):

\[
T^{(r)}
\]

— exhaustion step.

Виконуємо:

\[
r=1,\ldots,N.
\]

Baseline:

\[
N=3000.
\]

У кожному run:

1. генерується нова random consumption sequence;
2. будується state path;
3. фіксується first zero;
4. якщо zero не досягнутий до horizon — записується missing/NaN.

---

## 16. Monte Carlo не змінює model assumptions

Важливий principle.

Якщо consumption distribution неправильно обрана, 3000 runs не виправлять її.

Якщо independence assumption неправильна, 1 000 000 runs не зроблять result адекватним.

Monte Carlo лише точніше досліджує **наслідки заданої stochastic model**.

> **More simulations ≠ better model.**

---

## 17. Probability exhausted

Після simulations:

\[
\hat p=
\frac{\text{runs exhausted within horizon}}
{N}.
\]

Для baseline з:

- horizon=21;
- N=3000;
- seed=2026

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

Якщо просто викинути їх і дивитися лише mean finite times, можна недооцінити uncertainty.

Тому probability_exhausted і conditional timing потрібно показувати разом.

У складніших задачах це пов’язано з censoring / survival analysis.

---

## 20. Histogram

Histogram exhaustion steps показує distribution finite outcomes.

<figure>
  <img src="figures/fig_05_monte_carlo_histogram.svg" alt="Monte Carlo distribution exhaustion step">
  <figcaption><strong>Рис. 5.</strong> Monte Carlo замінює одну прогнозовану точку distribution можливих outcomes. Histogram треба читати разом із часткою runs без exhaustion у horizon.</figcaption>
</figure>

Вісь X:

> exhaustion step.

Вісь Y:

> number of simulated runs.

Histogram не є probability law real system.

Він є empirical distribution generated by model.

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

- simulation / Monte Carlo;
- stochastic;
- produces distribution-level summary.

---

## 22. Один об’єкт — різні research questions

Deterministic question:

> коли resource reaches zero за constant rate?

Stochastic single-run question:

> як може виглядати одна realization?

Monte Carlo question:

> який distribution exhaustion outcomes under assumed uncertainty?

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

Але classification axis still useful: не кожне research question потребує trajectory.

---

## 24. Analytical vs simulation

Deterministic exhaustion:

\[
t^*=\frac{S_0}{v}
\]

отримуємо analytically.

Monte Carlo probability closed-form тут не використовується.

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

Отже, це descriptive/simulation models.

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
- exhaustion distribution narrower;
- deterministic trajectory becomes stronger central reference.

Не обов’язково every simulation exhausts exactly at 20.

---

## 28. Scenario: high variance

\[
\sigma=3.
\]

Expected:

- wider trajectory spread;
- more early and late exhaustion outcomes;
- greater uncertainty.

Mean consumption assumption remains same.

Це experiment on **variability**, not mean.

<figure>
  <img src="figures/fig_06_variance_scenarios.svg" alt="Сценарії low і high variance">
  <figcaption><strong>Рис. 6.</strong> За однакового mean higher \(\sigma\) розширює family можливих trajectories та outcomes. Зміна uncertainty не тотожна зміні expected level.</figcaption>
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

Normal distribution theoretically permits negative draws.

Model applies:

\[
C_k=\max(0,C_k).
\]

Це changes distribution.

При baseline:

\[
\mu=6,\sigma=1.5
\]

negative probability small.

При large \(\sigma\) clipping matters more.

Отже, stochastic model is not exactly normal consumption after transformation.

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

> чи нормальний distribution із clipping still plausible domain model?

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

Тоді stationary stochastic model inadequate.

---

## 35. Зламай модель: no replenishment

Current state equation:

\[
S_{k+1}=\max(0,S_k-C_k).
\]

Якщо є replenishment \(Q_k\):

\[
S_{k+1}=
\max(0,S_k+Q_k-C_k).
\]

Це вже інша dynamic model.

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

Problem is core state update.

---

## 39. Verification: reproducibility

Same seed must produce same draws.

Test uses:

\[
seed=123.
\]

This is regression evidence for RNG workflow.

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

Змінюючи seed, ми змінюємо realization, не model parameters.

---

## 43. Python без страху: Monte Carlo

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

> За deterministic assumptions \(S_0=120,v=6\) depletion time equals 20. Under stochastic independent clipped-normal consumption with \(\mu=6,\sigma=1.5\), horizon 21, 3000 runs and seed 2026, model estimates depletion within horizon at about 0.80. This is a property of the specified simulation assumptions, not a direct empirical probability of a real process.

Це conclusion with scope.

---

## 46. Типові помилки мислення

### «Deterministic model неправильна, бо reality random»

Не обов’язково.

Вона може бути useful baseline.

### «Monte Carlo більш реалістична автоматично»

Ні.

Realism depends on assumptions.

### «Одна random trajectory — forecast»

Ні.

Це realization.

### «Mean exhaustion ≈20.1 означає, що ресурс закінчиться на 20.1»

Ні.

Це summary conditional finite runs.

### «Seed 2026 додає достовірність»

Ні.

Він додає reproducibility.

---

## 47. Від моделі до Lab

Для цього заняття повний browser Lab ще не реалізований.

Тому MiniBook формує теоретичну основу перед Python experiment.

До практики потрібно спрогнозувати:

1. low variance;
2. high variance;
3. higher mean;
4. short horizon.

Потім перевірити predictions у notebook/Python.

---

## 48. Від MiniBook до Python

Python package реалізує:

- deterministic_stock();
- deterministic_exhaustion_time();
- stochastic_consumption();
- discrete_stock_path();
- stochastic_stock_path();
- exhaustion_step();
- monte_carlo_exhaustion_times();
- summarize_exhaustion().

Тобто MiniBook пояснює structure, а package дозволяє reproduce calculations.

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

Monte Carlo:

> distribution total processing time.

Це лише structural example.

Parameters мають походити з actual/synthetic justified data.

---

## 51. Model selection map

<figure>
  <img src="figures/fig_07_model_selection_map.svg" alt="Карта вибору класу моделі">
  <figcaption><strong>Рис. 7.</strong> Вибір класу починається з research question: чи важлива variability, state evolution, optimization або distribution outcomes.</figcaption>
</figure>

Questions:

- Need only baseline? → deterministic.
- Need path over steps? → dynamic.
- Randomness important? → stochastic.
- Need risk distribution? → simulation/Monte Carlo.
- Need best decision? → optimization extension.

---

## 52. Класифікація як мова методології

Коли у дисертації написано:

> «побудовано стохастичну дискретну динамічну імітаційну model»,

читач повинен зрозуміти:

- state changes stepwise;
- transition contains randomness;
- results obtained computationally;
- conclusion likely distribution-level.

Classification must explain method.

Не decorate text.

---

## 53. Reproducibility package T1.L2

Збережіть:

- model code;
- parameter values;
- horizon;
- seed;
- n_runs;
- scenario table;
- generated paths;
- Monte Carlo output;
- summary;
- software versions;
- commit.

Тоді probability estimate has identity.

---

## 54. What Monte Carlo proves

Monte Carlo can show:

> consequences of assumptions.

It does not prove:

- chosen distribution is correct;
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
- uncertainty;
- state;
- risk

без sensitive data.

Transfer to real work requires separate data governance and domain validation.

---

## 56. Одна сторінка підсумку

### П’ять головних ідей

1. Classification captures model assumptions.
2. Deterministic trajectory and stochastic distribution answer different questions.
3. Dynamic model has state memory.
4. Monte Carlo explores uncertainty defined by the model.
5. Seed supports reproducibility, not realism.

### Три правила

Deterministic:

\[
S(t)=\max(0,S_0-vt).
\]

Dynamic:

\[
S_{k+1}=\max(0,S_k-C_k).
\]

Monte Carlo estimate:

\[
\hat p=\frac{n_{event}}{N}.
\]

### Дві помилки

- one stochastic realization = forecast;
- more simulations = more adequate model.

### Одне питання

> Який class model відповідає моєму research question, а не просто моєму улюбленому Python tool?

### Наступний крок

Запустіть baseline, повторіть same seed, змініть \(\mu\) і \(\sigma\) окремо та поясніть різницю.

---

## 57. Фінальна думка

Один і той самий process може мати кілька математичних моделей.

Це не contradiction.

Це нормальна властивість modeling.

Детермінована model дає baseline.

Stochastic model вводить uncertainty.

Dynamic model показує evolution state.

Monte Carlo формує distribution outcomes.

Сильний дослідник не питає:

> «яка модель правильна взагалі?»

Він питає:

> **яка model structure потрібна, щоб коректно відповісти саме на моє research question — і які висновки вона після цього дозволяє зробити?**
