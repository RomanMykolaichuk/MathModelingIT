# MathModelingIT MiniBook T2.L3

## Математичні моделі задач нелінійного програмування

### Коли пряма лінія перестає працювати: diminishing returns, локальні максимуми і перевірка оптимуму

> **Головна ідея книги:** у нелінійній оптимізації недостатньо отримати повідомлення **success=True**. Нелінійна форма objective може створювати saturation, interaction, curved feasible regions і кілька локальних максимумів. Тому сильний computational result повинен поєднувати формалізацію, feasibility checks, sensitivity, multi-start, незалежну перевірку і візуальну інтерпретацію landscape.

---

## 0. Паспорт книги

**Код заняття:** T2.L3  
**Тема:** математичні моделі задач нелінійного програмування  
**Рівень:** середній  
**Орієнтовний час читання:** 70–85 хвилин  
**Попередні знання:** поняття функції, constraint, derivative на інтуїтивному рівні, базова лінійна оптимізація.

Після цієї книги ви повинні вміти:

- пояснювати, що робить optimization problem нелінійною;
- відрізняти diminishing returns від linear returns;
- читати saturation curve;
- формулювати nonlinear objective і constraints;
- інтерпретувати applied optimum T2.L3;
- розуміти роль стартової точки;
- розрізняти local і global optimum;
- пояснювати, чому local solver може успішно завершитися в різних точках;
- використовувати multi-start як практичну перевірку;
- використовувати grid search як independent sanity check у двох вимірах;
- читати contour plot;
- проводити sensitivity до total resource;
- формулювати allowed conclusion без перебільшення;
- знаходити аналог nonlinear effect у власній research problem.

---

## 1. Сцена: більше ресурсу — але не пропорційно більше ефекту

Уявімо синтетичну навчальну задачу.

Є два напрями використання обмеженого ресурсу:

- \(x\);
- \(y\).

Загальний ресурс:

\[
R=100.
\]

На першому етапі додаткові units ресурсу дають значний effect.

Але далі напрям насичується.

Перші 10 units можуть бути дуже корисними.

Наступні 10 — трохи менше.

Після певного рівня ще одна unit майже не змінює result.

Крім того, два напрями можуть слабко підсилювати один одного.

У такій ситуації linear objective на кшталт:

\[
8x+6y
\]

вже не описує бажану поведінку.

Потрібна нелінійна model.

Дослідницьке питання:

> **Як розподілити обмежений ресурс між двома напрямами, якщо їхня віддача насичується, а результат містить слабку interaction, і як перевірити, що чисельний optimizer не ввів нас в оману?**

<figure>
  <img src="figures/fig_01_linear_vs_nonlinear.svg" alt="Лінійна і нелінійна віддача">
  <figcaption><strong>Рис. 1.</strong> У linear model marginal return сталий. У diminishing-returns model кожна наступна unit дає менший приріст, тому оптимальний розподіл уже не визначається простим порівнянням коефіцієнтів.</figcaption>
</figure>

---

## 2. Що означає нелінійність

Функція нелінійна, якщо relationship між variables і result не можна подати лише як:

\[
a_1x_1+a_2x_2+\dots+a_nx_n+b.
\]

Нелінійність може виникати через:

- exponent;
- logarithm;
- square root;
- product variables;
- powers;
- trigonometric functions;
- thresholds;
- piecewise effects;
- ratios.

У нашому applied case присутні одразу кілька nonlinear forms.

---

## 3. Applied objective T2.L3

Функція:

\[
F(x,y)=
40(1-e^{-0.05x})
+
35(1-e^{-0.04y})
+
0.15\sqrt{xy}.
\]

Потрібно:

\[
F(x,y)\rightarrow\max.
\]

Constraints:

\[
x+y\le R,
\]

\[
x\ge0,
\]

\[
y\ge0.
\]

Для baseline:

\[
R=100.
\]

Ця formula навмисно синтетична.

Вона потрібна для розуміння nonlinear behavior, а не для опису конкретної реальної військової системи.

---

## 4. Перший доданок: diminishing returns для x

Розглянемо:

\[
F_x(x)=40(1-e^{-0.05x}).
\]

Коли:

\[
x=0,
\]

маємо:

\[
F_x(0)=0.
\]

Коли \(x\) зростає:

\[
e^{-0.05x}\rightarrow0.
\]

Отже:

\[
F_x(x)\rightarrow40.
\]

Тобто effect має upper saturation level близько 40.

Це принципово інша поведінка, ніж:

\[
8x,
\]

яка росте безмежно.

<figure>
  <img src="figures/fig_02_diminishing_returns.svg" alt="Криві diminishing returns">
  <figcaption><strong>Рис. 2.</strong> Експоненційні компоненти швидко ростуть на початку, але поступово виходять на saturation. Marginal gain зменшується зі збільшенням allocation.</figcaption>
</figure>

---

## 5. Marginal return як похідна

Для:

\[
F_x(x)=40(1-e^{-0.05x}),
\]

derivative:

\[
\frac{dF_x}{dx}=2e^{-0.05x}.
\]

На старті:

\[
\frac{dF_x}{dx}\Big|_{x=0}=2.
\]

При \(x=20\):

\[
2e^{-1}\approx0.736.
\]

При \(x=60\):

\[
2e^{-3}\approx0.100.
\]

Тобто додаткова unit x стає менш корисною.

Це і є **diminishing marginal returns**.

---

## 6. Другий напрям y

Для:

\[
F_y(y)=35(1-e^{-0.04y}),
\]

derivative:

\[
\frac{dF_y}{dy}=1.4e^{-0.04y}.
\]

Він теж diminishing.

Але має інший saturation level та іншу швидкість saturation.

Отже, optimum повинен балансувати два nonlinear response profiles.

---

## 7. Interaction term

Третій term:

\[
0.15\sqrt{xy}.
\]

Він залежить від обох variables одночасно.

Якщо:

\[
x=0
\]

або:

\[
y=0,
\]

interaction term = 0.

Коли обидва positive, з’являється додаткова utility.

Це weak synergy.

У linear additive model:

\[
F(x,y)=F_x(x)+F_y(y)
\]

такої interaction немає.

Тут:

\[
F(x,y)\ne F_x(x)+F_y(y).
\]

---

## 8. Чому synergy впливає на balance

Без interaction optimizer міг би більше схилятися до напряму з кращим standalone marginal profile.

Term:

\[
\sqrt{xy}
\]

винагороджує ситуацію, де positive allocations є в обох directions.

Це не означає автоматично 50/50.

Але робить extreme allocation менш attractive.

У baseline optimum:

\[
x^*\approx48.659,
\]

\[
y^*\approx51.341.
\]

Результат близький до balance, але не exactly equal.

---

## 9. Constraint ресурс

Маємо:

\[
x+y\le100.
\]

У optimum:

\[
x^*+y^*\approx100.
\]

Resource practically fully used.

Чому?

Бо в baseline domain utility still increasing in both variables.

Якщо залишити resource unused, можна трохи збільшити x або y й покращити objective.

Отже, constraint active:

\[
x+y=100.
\]

---

## 10. Baseline optimum

Source-of-truth tests фіксують:

\[
x^*\approx48.6593,
\]

\[
y^*\approx51.3407.
\]

Objective:

\[
F^*\approx74.49685.
\]

Resource used:

\[
100.
\]

<figure>
  <img src="figures/fig_03_applied_surface.svg" alt="Поверхня applied objective">
  <figcaption><strong>Рис. 3.</strong> Applied objective є гладкою nonlinear surface. Feasible region обмежена трикутником \(x\ge0\), \(y\ge0\), \(x+y\le100\); optimum лежить поблизу resource boundary.</figcaption>
</figure>

---

## 11. Чому optimum не 50/50

Рівний allocation:

\[
(50,50)
\]

дуже близький до optimum.

Але coefficients двох saturation components різні:

- 40 та 0.05 для x;
- 35 та 0.04 для y.

Тому marginal returns трохи різні.

Solver знаходить balance, де small local reallocation уже не дає improvement у межах constraint.

---

## 12. One-dimensional intuition

Якщо resource constraint active:

\[
y=R-x.
\]

Тоді objective можна розглядати як:

\[
H(x)=F(x,R-x).
\]

Optimum приблизно там, де:

\[
\frac{dH}{dx}=0.
\]

Інтуїтивно:

> marginal benefit перенести одну малу unit з y у x стає нульовим.

Тобто system balance досягнуто не через symmetry, а через equality relevant marginal trade-off.

---

## 13. Feasibility checks

Після solver окремо перевіряємо:

\[
x\ge0,
\]

\[
y\ge0,
\]

\[
x+y\le R,
\]

і:

\[
F(x,y)
\]

finite.

У source code verify_applied_solution() робить це незалежно.

**success=True** і feasibility — різні твердження.

---

## 14. Чому SLSQP

Applied problem розв’язується через SLSQP.

Цей method підтримує:

- bounds;
- inequality constraints;
- smooth nonlinear objectives.

Ми мінімізуємо:

\[
-F(x,y),
\]

бо scipy.optimize.minimize — minimizer.

Тобто:

\[
\max F
\]

перетворюється на:

\[
\min(-F).
\]

---

## 15. Стартова точка

Numerical nonlinear solver потребує initial guess:

\[
(x_0,y_0).
\]

Наприклад:

\[
(50,50).
\]

Для applied model assignment пропонує:

- (10,10);
- (80,10);
- (10,80);
- (50,50).

У nonlinear optimization path algorithm може залежати від start.

---

## 16. Applied model і start dependence

Для smooth applied function у baseline різні reasonable starts сходяться близько до того самого optimum.

Це корисний empirical evidence.

Але це не universal property nonlinear problems.

Саме тому course має другий case — deliberately non-convex landscape.

---

## 17. Sensitivity to total resource

Досліджуємо:

\[
R\in\{60,80,100,120\}.
\]

Контрольні результати:

| R | x* | y* | F* |
|---:|---:|---:|---:|
| 60 | ≈30.56 | ≈29.44 | ≈60.04 |
| 80 | ≈39.58 | ≈40.42 | ≈68.52 |
| 100 | ≈48.66 | ≈51.34 | ≈74.50 |
| 120 | ≈57.83 | ≈62.17 | ≈78.86 |

Objective зростає.

Але increments зменшуються.

---

## 18. Diminishing value additional resource

Приріст від 60 до 80:

\[
68.52-60.04\approx8.48.
\]

Від 80 до 100:

\[
74.50-68.52\approx5.98.
\]

Від 100 до 120:

\[
78.86-74.50\approx4.36.
\]

Однакове:

\[
\Delta R=20.
\]

Але \(\Delta F\) зменшується.

<figure>
  <img src="figures/fig_04_resource_sensitivity.svg" alt="Sensitivity до total resource">
  <figcaption><strong>Рис. 4.</strong> Additional resource покращує optimum, але marginal gain зменшується. Це прямий прояв diminishing returns на рівні optimal value function.</figcaption>
</figure>

---

## 19. Value function

Визначимо:

\[
V(R)=
\max_{x+y\le R}F(x,y).
\]

Sensitivity table — samples function \(V(R)\).

У nonlinear case вона curved.

Ключове question:

> як змінюється best achievable result при relaxation resource constraint?

Це часто значно важливіше, ніж один baseline optimum.

---

## 20. Non-convex case: навіщо друга модель

Applied function поводиться досить дружньо.

Щоб навчитися local optima, потрібна surface із кількома peaks.

Course використовує:

\[
G(x,y)=
\sin(1.7x)\cos(1.3y)
+
0.15x
-
0.03(x^2+y^2).
\]

Bounds:

\[
-4\le x\le4,
\]

\[
-4\le y\le4.
\]

Ця function — навчальний landscape.

Вона не претендує на direct real-world military interpretation.

---

## 21. Чому landscape non-convex

Trigonometric terms:

\[
\sin(1.7x),\qquad
\cos(1.3y)
\]

створюють oscillations.

Quadratic term:

\[
-0.03(x^2+y^2)
\]

формує broad downward trend.

Linear:

\[
0.15x
\]

нахиляє surface.

У результаті:

- кілька peaks;
- кілька valleys;
- local maxima.

<figure>
  <img src="figures/fig_05_nonconvex_contours.svg" alt="Contour non-convex landscape">
  <figcaption><strong>Рис. 5.</strong> Non-convex landscape має кілька локальних максимумів. Різні start points можуть привести local solver у різні basins of attraction.</figcaption>
</figure>

---

## 22. Local optimum

Point \(z^*\) є local maximum, якщо в невеликому neighborhood немає кращого point.

Але десь далеко може існувати:

\[
G(\tilde z)>G(z^*).
\]

Тоді local optimum не global.

Це центральна проблема non-convex optimization.

---

## 23. Global optimum

Global maximum задовольняє:

\[
G(z^*)\ge G(z)
\]

для всіх feasible \(z\).

У bounded 2D teaching landscape можна наближено перевірити global region через dense grid search.

У високій dimension це швидко стає expensive.

---

## 24. Що реально означає success=True

Для local solver **success=True** означає, що algorithm задовольнив власний stopping condition.

Не означає:

> знайдений найвищий peak на всій surface.

Це фундаментальне правило:

> **Convergence is not globality.**

---

## 25. Start point як частина experiment

Запустимо:

\[
(0,0)
\]

і:

\[
(2,2).
\]

Source-of-truth test вимагає, щоб отримані objectives відрізнялися більше ніж на 0.05.

Отже, різні starts можуть привести до різних local solutions.

---

## 26. Basin of attraction

Інтуїтивно surface схожа на гористу місцевість.

Local optimizer — мандрівник, який іде вгору, але бачить лише local slope.

Якщо стартує біля одного peak, підніметься на нього.

Якщо біля іншого — на інший.

Область start points, що приводить до певного local optimum, називають basin of attraction.

<figure>
  <img src="figures/fig_06_multistart.svg" alt="Multi-start optimization">
  <figcaption><strong>Рис. 6.</strong> Multi-start запускає local optimizer з різних точок. Якщо solutions різняться, start dependence є empirically demonstrated, а не лише теоретично згаданою.</figcaption>
</figure>

---

## 27. Multi-start

Course запускає starts:

\[
(-3,-3),\ (-3,2),\ (0,0),\ (2,2),\ (3,-2),\ (4,4).
\]

Для кожного:

1. solve local;
2. записати final x,y;
3. objective;
4. success.

Потім sort by objective.

Best known region:

\[
x\approx0.956,
\]

\[
y\approx0,
\]

\[
G\approx1.1145.
\]

---

## 28. Multi-start не є formal proof

Навіть якщо 100 starts дали один best result, це ще не formal proof global optimality.

Можливо:

- вузький peak не потрапив у sampled basins;
- solver skipped region;
- boundaries insufficiently explored.

Multi-start — strong practical check.

Не universal proof.

---

## 29. Independent grid search

У 2D можна зробити coarse grid.

Наприклад:

\[
step=0.05.
\]

Перебираємо всі grid combinations у bounds.

Для кожного point обчислюємо G.

Беремо best.

Source-of-truth test вимагає:

\[
|G_{multistart}-G_{grid}|<0.01.
\]

Це independent sanity check.

---

## 30. Чому grid search корисний

Переваги:

- простий;
- не залежить від gradient;
- оглядає всю bounded area;
- легко visualise;
- має інший failure mode, ніж local optimizer.

У 2D це сильний teaching verification.

---

## 31. Чому grid search погано масштабується

Якщо на одну variable маємо 161 grid points, у 2D:

\[
161^2\approx25921.
\]

У 5D:

\[
161^5
\]

вже величезне число.

Це curse of dimensionality.

Grid search — не general global optimization solution.

---

## 32. Grid resolution і accuracy

Step:

\[
0.05
\]

означає, що grid не бачить точки між nodes.

Зменшимо step:

- accuracy higher;
- computations much more.

Тобто independent verifier теж має parameter і limitation.

---

## 33. Contour plot як evidence

Contour plot показує lines equal objective.

На ньому можна побачити:

- peaks;
- valleys;
- basins;
- start points;
- solver endpoints.

Це інформативніше за таблицю success values.

<figure>
  <img src="figures/fig_07_grid_vs_multistart.svg" alt="Grid search і multistart">
  <figcaption><strong>Рис. 7.</strong> Multi-start і coarse grid використовують різні computational mechanisms. Їхня згода поблизу \(x\approx0.956, y\approx0\) підсилює confidence у знайденому best region.</figcaption>
</figure>

---

## 34. Visualization не доводить optimum

Красивий contour plot не є formal proof.

Resolution limited.

Color scale може приховувати differences.

Plot useful для:

- intuition;
- anomaly detection;
- communication.

Але не замінює numeric verification.

---

## 35. Constraints і bounds — різні механізми

Applied model:

\[
x+y\le R
\]

— general inequality constraint.

Також:

\[
x\ge0,y\ge0
\]

можна задавати bounds.

Nonconvex:

\[
-4\le x,y\le4
\]

— box bounds.

Solver algorithms можуть обробляти їх по-різному.

Для modeler головне — mathematical meaning має бути explicit.

---

## 36. Feasible vs local optimum

Point може бути local maximum unconstrained, але infeasible.

Optimization шукає optimum лише всередині feasible region.

Boundary itself може містити optimum.

Тому після numeric solve завжди перевіряємо constraints.

---

## 37. KKT intuition

У constrained smooth optimization formal theory використовує Karush–Kuhn–Tucker conditions.

На introductory level важлива idea:

- якщо constraint inactive, optimum locally behaves like unconstrained stationary point;
- якщо constraint active, optimum може лежати на boundary;
- gradient objective взаємодіє з gradients constraints.

У baseline applied problem resource constraint active.

---

## 38. Lagrange multiplier intuition

Для:

\[
x+y\le R
\]

multiplier можна інтерпретувати як local value additional resource.

Це nonlinear analogue shadow-price intuition.

Якщо \(V(R)\) saturates, marginal value:

\[
\frac{dV}{dR}
\]

decreases.

Sensitivity table already показує це без складної dual theory.

---

## 39. Convexity і concavity intuition

У maximization є важлива властивість.

Якщо:

- feasible set convex;
- objective concave,

то local maximum є global maximum.

Це дуже сильна гарантія.

У deliberately non-convex landscape такої гарантії немає.

Саме тому один local solve недостатній.

---

## 40. Hessian intuition

Для двічі differentiable function curvature описує Hessian matrix.

Не потрібно вручну обчислювати Hessian для кожної Lab.

Але варто пам’ятати:

- curvature determines shape;
- negative curvature around point може підтримувати local maximum interpretation;
- mixed curvature може створювати saddles.

Optimization algorithm взаємодіє з geometry, а не просто «перебирає числа».

---

## 41. Saddle point

Point може мати zero gradient, але не бути optimum.

Наприклад:

\[
H(x,y)=x^2-y^2.
\]

У:

\[
(0,0)
\]

gradient zero.

Але вздовж x function зростає, вздовж y — зменшується.

Це saddle.

Отже:

> stationary point ≠ automatically optimum.

---

## 42. Model adequacy applied case

Applied function synthetic.

У real research потрібно обґрунтувати:

- why exponential saturation;
- why these coefficients;
- why square-root synergy;
- whether interaction positive;
- whether resource continuous;
- whether one period sufficient.

Без цього formula має teaching meaning only.

---

## 43. Calibration nonlinear model

Якщо є observed pairs:

\[
(x_k,y_k,F_k),
\]

можна оцінювати coefficients:

\[
40,\ 0.05,\ 35,\ 0.04,\ 0.15.
\]

Наприклад nonlinear least squares.

Тоді optimization model пов’язується з data.

Але з’являється uncertainty parameters.

---

## 44. Uncertainty optimum

Якщо coefficients uncertain, optimum:

\[
x^*,y^*
\]

теж uncertain.

Можна:

1. sample coefficients;
2. solve optimization кожен run;
3. analyse distribution optimal decisions.

Але тут є важлива методологічна розвилка.

### Reoptimization

Кожна sampled world отримує власний optimum.

Питання:

> яким був би optimum, якби parameters були саме такими?

### Fixed-decision robustness

Обираємо один decision \(x^*\) і оцінюємо його performance under uncertain parameters.

Питання:

> наскільки baseline decision robust, якщо real parameters інші?

Ці experiments не можна змішувати.

---

## 45. Diminishing returns vs threshold effect

Diminishing returns — smooth decrease marginal gain.

Threshold — sharp change біля певного value.

Наприклад:

\[
F(x)=
\begin{cases}
ax,&x<T,\\
ax+b,&x\ge T.
\end{cases}
\]

Такий model nonlinear/non-smooth.

Не всі nonlinearities однакові.

Method selection залежить від structure.

---

## 46. Non-smooth objective

Якщо objective має:

- absolute values;
- min/max;
- discontinuities;

gradient-based solver може мати difficulties.

Потрібно обирати method відповідно до mathematical properties.

Питання «який solver?» завжди йде **після** питання «яка структура model?».

---

## 47. Чому property важливіша за brand solver

Перед вибором algorithm запитайте:

- objective smooth?
- convex/concave?
- bounds?
- constraints?
- derivatives available?
- dimension?
- discrete variables?
- non-convex?
- stochastic?

Після цього method.

Назва library — останній рівень, а не перший.

---

## 48. Python без страху: applied objective

~~~python
def applied_utility(x, y):
    return (
        40 * (1 - exp(-0.05*x))
        + 35 * (1 - exp(-0.04*y))
        + 0.15 * sqrt(x*y)
    )
~~~

Code mirrors formula.

Це desirable для audit.

---

## 49. Python без страху: applied solve

~~~python
sol = solve_applied(
    total_resource=100,
    start=(50, 50),
)
~~~

Контроль:

~~~text
x ≈ 48.659
y ≈ 51.341
F ≈ 74.497
~~~

---

## 50. Python без страху: verification

~~~python
checks = verify_applied_solution(
    sol,
    total_resource=100,
)

assert checks["all_passed"]
~~~

Не вважайте success достатньою verification.

---

## 51. Python без страху: sensitivity

~~~python
rows = applied_sensitivity(
    [60, 80, 100, 120]
)
~~~

Перевірка:

\[
F^*(R)
\]

має non-decreasing trend для цього model.

Source test перевіряє саме це.

---

## 52. Python без страху: nonconvex

~~~python
a = solve_nonconvex((0,0))
b = solve_nonconvex((2,2))
~~~

Якщо objective values різні:

> local solver start dependence demonstrated.

---

## 53. Python без страху: multi-start

~~~python
rows = multistart_nonconvex([
    (-3,-3),
    (-3,2),
    (0,0),
    (2,2),
    (3,-2),
    (4,4),
])
~~~

Sort by objective.

Best region near:

\[
(0.956,0).
\]

---

## 54. Python без страху: grid check

~~~python
grid = grid_search_nonconvex(
    step=0.05
)
~~~

Порівняйте:

\[
G_{grid}
\]

і:

\[
G_{best\ multistart}.
\]

Різниця < 0.01 у control test.

---

## 55. Verification layers

### Input validation

- R positive;
- start length = 2;
- start non-negative applied case;
- grid step positive.

### Feasibility

- x,y within constraints.

### Solver convergence

- success status.

### Cross-method check

- multi-start;
- grid search.

### Model adequacy

- structure justified by domain/data.

<figure>
  <img src="figures/fig_08_verification_layers.svg" alt="Рівні перевірки nonlinear optimization">
  <figcaption><strong>Рис. 8.</strong> Надійний nonlinear result будується шарами: valid inputs → feasible solution → numerical convergence → multi-start / independent check → domain adequacy.</figcaption>
</figure>

---

## 56. Зламай модель: one start only

Запустили з:

\[
(0,0)
\]

і отримали success.

Зупинилися.

У non-convex landscape це insufficient.

Break condition:

> інший start дає кращий objective.

Модернізація:

> multi-start.

---

## 57. Зламай модель: coarse grid too coarse

Step:

\[
1.0
\]

може пропустити narrow peak.

Grid says best A.

Finer grid — best B.

Отже, grid resolution itself parameter.

Need sensitivity to verification method.

---

## 58. Зламай модель: invalid start

Applied start:

\[
(80,80)
\]

sum > R.

Current function rescales start to feasible resource total.

Це convenient behavior.

Але researcher повинен знати, що algorithm changed initial point.

Transparent logging важливе.

---

## 59. Зламай модель: square root near zero

Term:

\[
\sqrt{xy}
\]

має derivatives із higher sensitivity near zero.

Якщо model допускає exact zero, mathematical smoothness changes.

У current setup solver handles baseline.

Але form objective впливає на numerical behavior.

---

## 60. Зламай модель: wrong domain

Якщо x або y negative, applied_utility returns negative infinity.

Це semantic guard.

У real model domain restrictions повинні бути explicit constraints.

---

## 61. Зламай модель: coefficients без data

Якщо coefficients 40, 35, 0.05, 0.04, 0.15 не мають empirical basis, optimum має teaching meaning only.

Це нормально для course.

Але dissertation result потребує parameter provenance.

---

## Поглиблення: зведення constrained problem до однієї змінної

У baseline resource constraint active:

\[
x+y=R.
\]

Тому:

\[
y=R-x.
\]

Підставимо в objective:

\[
H_R(x)=F(x,R-x).
\]

Feasible interval:

\[
0\le x\le R.
\]

Це дуже корисний conceptual step.

Двовимірна constrained optimization problem стає one-dimensional problem.

Ми можемо:

- побудувати graph \(H_R(x)\);
- побачити максимум;
- порівняти numerical solution;
- перевірити shape.

Для \(R=100\) maximum \(H_{100}(x)\) лежить поблизу:

\[
x\approx48.66.
\]

Тоді:

\[
y\approx51.34.
\]

Це independent interpretation of solver result.

Важливо:

> reduction works because we know active equality-like structure in optimum.

Не кожну constrained problem можна так просто reduce.

---

## Поглиблення: gradient як локальний компас

Для smooth function gradient:

\[
\nabla F(x,y)
=
\left(
\frac{\partial F}{\partial x},
\frac{\partial F}{\partial y}
\right)
\]

показує direction найшвидшого local increase.

У unconstrained maximization stationary candidate задовольняє:

\[
\nabla F=0.
\]

Але в constrained problem optimum може лежати на boundary, де gradient не zero.

Baseline саме такий випадок.

Resource boundary:

\[
x+y=R.
\]

Тому важливо не застосовувати правило:

> «optimum там, де derivative = 0»

без урахування constraints.

---

## Поглиблення: marginal balance на boundary

Якщо:

\[
y=R-x,
\]

то small increase \(dx\) автоматично означає:

\[
dy=-dx.
\]

У optimum local gain from x має балансувати local loss from y з урахуванням interaction.

Тобто:

\[
\frac{dH_R}{dx}=0.
\]

Інтуїтивно:

> якщо перенести дуже малу unit ресурсу з y у x, objective майже не зміниться.

Це глибша причина того, чому allocation близький до balance.

Не «solver любить 50/50», а:

> marginal trade-off balanced.

---

## Поглиблення: curvature пояснює saturation

Перша derivative показує marginal gain.

Друга derivative:

\[
\frac{d^2F}{dx^2}
\]

описує curvature.

Для exponential saturation component:

\[
F_x(x)=40(1-e^{-0.05x}),
\]

маємо:

\[
\frac{d^2F_x}{dx^2}
=
-0.1e^{-0.05x}<0.
\]

Negative second derivative означає concavity цього component.

Тобто slope зменшується.

Це математичний signature diminishing returns.

---

## Поглиблення: concavity не треба плутати з «кривою вниз на картинці»

Graphical intuition корисна.

Але formal property важливіша.

Concave objective over convex feasible set для maximization дає сильну гарантію:

> будь-який local optimum є global.

Саме тому classification problem geometry має практичне значення.

У non-convex case такої гарантії немає.

---

## Поглиблення: scaling variables

Numerical optimization може поводитися гірше, якщо variables мають дуже різні scales.

Наприклад:

\[
x\in[0,1],
\]

\[
y\in[0,10^6].
\]

Тоді gradient components можуть мати radically different magnitudes.

Корисно масштабувати:

\[
\tilde x=\frac{x-x_{min}}{x_{max}-x_{min}}.
\]

У нашому teaching case x і y одного порядку, тому issue мінімальна.

Але для Research Transfer scaling потрібно перевіряти.

---

## Поглиблення: scaling objective

Так само objective components можуть мати різні magnitudes.

Якщо one component ~0.01, а інший ~100000, small component numerical solver майже «не бачить».

Це не обов’язково означає, що він предметно неважливий.

Потрібно distinguish:

- numerical scale;
- conceptual importance.

Особливо це важливо в weighted nonlinear objectives.

---

## Поглиблення: stopping tolerance

Solver зупиняється не тоді, коли досягнуто mathematically exact optimum.

Він використовує tolerances.

Наприклад:

- gradient norm small;
- step small;
- objective change small;
- maximum iterations.

Тому два runs можуть дати:

\[
74.49684
\]

і:

\[
74.49685.
\]

Це не meaningful scientific difference.

Потрібно reporting precision узгоджувати з numerical tolerance та data quality.

---

## Поглиблення: false precision nonlinear result

Якщо parameters synthetic:

\[
0.05,\ 0.04,\ 0.15,
\]

то reporting:

\[
x^*=48.659312487
\]

створює false precision.

У teaching interpretation достатньо:

\[
x^*\approx48.66,
\]

\[
y^*\approx51.34.
\]

Точніші digits потрібні для tests, але не обов’язково для scientific narrative.

Це важливе розділення:

- computational precision;
- reporting precision.

---

## Поглиблення: design of multi-start experiment

Multi-start не повинен бути випадковим списком start points.

Корисно включити:

### Center

\[
(0,0)
\]

або center domain.

### Corners

\[
(-4,-4),\ (-4,4),\ (4,-4),\ (4,4).
\]

### Interior points

кілька locations.

### Random sample

за потреби.

Мета:

> покрити різні basins.

У course використовується невеликий deterministic set, щоб experiment був reproducible.

---

## Поглиблення: deterministic starts vs random starts

Deterministic starts:

- reproducible;
- easy to compare;
- можуть miss region systematically.

Random starts:

- broader exploration;
- require seed;
- results vary with sample.

Комбінований design:

1. fixed canonical starts;
2. random starts with seed.

Це часто practical compromise.

---

## Поглиблення: best-of-multistart as lower bound on global optimum

У maximization якщо знайдено best value:

\[
G_{best}=1.1145,
\]

то ми знаємо:

\[
G_{global}\ge1.1145.
\]

Бо global optimum не може бути гіршим за знайдений feasible solution.

Але не знаємо:

\[
G_{global}=1.1145
\]

без stronger proof.

Тобто best found value дає **lower bound on global maximum value**.

Це коректна логічна позиція.

---

## Поглиблення: grid search як upper-proof не працює

Coarse grid знаходить best among grid points.

Це не upper bound на continuous maximum.

Між grid nodes може бути вищий point.

Отже:

\[
G_{grid}
\]

— ще один feasible lower bound.

Якщо:

\[
G_{grid}\approx G_{multistart},
\]

confidence grows.

Але formal gap unknown.

---

## Поглиблення: branch-and-bound / global methods як наступний рівень

Для деяких non-convex problems існують global optimization methods:

- branch-and-bound;
- interval methods;
- deterministic global solvers;
- evolutionary algorithms;
- basin hopping;
- differential evolution.

Але їх застосування залежить від:

- dimension;
- smoothness;
- bounds;
- derivative availability;
- computational budget.

На T2.L3 головне не перелік algorithms.

Головне:

> local method потребує explicit verification strategy.

---

## Поглиблення: boundary optimum

Nonconvex best region у course близький до:

\[
y\approx0.
\]

Тобто best solution лежить біля boundary.

Це важливий reminder.

Optimum не обов’язково «в центрі красивого peak».

Bounds самі формують feasible landscape.

Тому visualization повинна показувати не лише objective, а й feasible domain.

---

## Поглиблення: active bounds і interpretation

Якщо optimum має:

\[
y=0,
\]

це active lower bound.

Предметна interpretation:

> у цій synthetic landscape model allocation y не дає достатньої marginal benefit near best region.

Але це не означає:

> real direction y «не потрібний».

Toy landscape не має direct domain semantics.

Це teaching example of local/global behavior.

---

## Поглиблення: parameter sensitivity нелінійної форми

Можна змінити coefficient interaction:

\[
0.15\rightarrow0.05,\ 0.30.
\]

Question:

> як stronger/weaker synergy змінює allocation?

Або saturation rate:

\[
0.05\rightarrow0.03.
\]

Question:

> як slower saturation x змінює optimum?

Такі experiments допомагають визначити:

> які nonlinear assumptions найбільше формують decision.

---

## Поглиблення: structural uncertainty

Parameter uncertainty:

> coefficient 0.05 неточний.

Structural uncertainty:

> можливо exponential saturation взагалі неправильна function family.

Це глибша проблема.

Можливі alternatives:

- logarithmic;
- Michaelis–Menten;
- logistic;
- piecewise linear.

У research model варто порівнювати plausible structures, якщо data не підтримує одну однозначно.

---

## Поглиблення: calibration before optimization

Небезпечний workflow:

1. invent nonlinear formula;
2. optimize;
3. report optimum.

Сильніший:

1. formulate mechanism hypothesis;
2. collect/prepare data;
3. estimate parameters;
4. validate response function;
5. quantify uncertainty;
6. only then optimize;
7. evaluate robustness decision.

Optimization should sit **after** model calibration, not replace it.

---

## Поглиблення: fixed-decision robustness

Припустимо baseline optimum:

\[
d_0=(48.66,51.34).
\]

Parameters uncertainty.

Є два experiments.

### Reoptimize each draw

Для кожного parameter sample знаходимо new optimum.

Отримуємо distribution:

\[
d^*(\theta).
\]

### Keep \(d_0\) fixed

Для кожного parameter sample оцінюємо:

\[
F(d_0;\theta).
\]

Це показує robustness actual chosen decision.

Для decision support другий experiment часто не менш важливий.

---

## Поглиблення: regret

Можна визначити regret:

\[
Regret(\theta)
=
F(d^*(\theta);\theta)
-
F(d_0;\theta).
\]

Він відповідає:

> скільки performance ми втрачаємо, якщо використовуємо baseline decision замість scenario-specific optimum?

Це сильний bridge до robust decision making.

---

## Поглиблення: model audit T2.L3

### Mathematical audit

- domain correct?
- objective finite?
- constraints explicit?
- smoothness understood?

### Numerical audit

- starts logged?
- tolerance known?
- scaling acceptable?
- convergence checked?

### Globality audit

- convexity/concavity known?
- multi-start performed?
- independent check available?

### Scientific audit

- formula justified?
- parameters calibrated?
- uncertainty acknowledged?
- allowed conclusion conditional?

---

## Поглиблення: reproducibility package

Для nonlinear experiment збережіть:

- function definition;
- parameter values;
- bounds;
- constraints;
- solver/method;
- initial points;
- tolerances;
- random seed, якщо є;
- all local solutions;
- best objective;
- grid resolution;
- sensitivity results;
- figures;
- code version;
- package versions.

Особливо важливо зберігати starts.

Без них colleague може не відтворити local solution.

---

## Поглиблення: напівхудожнє повернення до сцени

Керівник бачить:

\[
x=48.66,\quad y=51.34
\]

і питає:

> «Чому не 50 на 50?»

Аналітик відповідає:

> «Бо два напрями мають різні saturation rates, а interaction винагороджує спільне використання. На boundary \(x+y=100\) optimum виникає там, де marginal trade-off balance. Якщо ресурс збільшувати, objective росте, але все повільніше».

Потім керівник дивиться на non-convex case:

> «А тут solver теж написав success. Чому ви запускаєте його шість разів?»

Аналітик:

> «Бо success означає local convergence. Різні starts приводять до різних peaks. Ми використовуємо multi-start і independent grid, щоб не переплутати локальний максимум із найкращим знайденим region».

Саме ця друга відповідь і є сутністю T2.L3.

---

## 62. Scenario design nonlinear

Корисний plan:

| Run | Change | Purpose |
|---|---|---|
| Baseline | R=100 | control |
| Low R | 60 | diminishing returns |
| Mid R | 80 | value function |
| High R | 120 | saturation |
| Starts | 4 starts | start sensitivity |
| Nonconvex | 6 starts | local optima |
| Grid | step=.05 | independent check |

Перед запуском бажано записати prediction.

---

## 63. Allowed conclusion applied case

Слабкий:

> оптимально x=48.659, y=51.341.

Кращий:

> Для synthetic nonlinear utility T2.L3 за R=100 SLSQP знаходить feasible solution \(x\approx48.659\), \(y\approx51.341\) з \(F\approx74.497\), використовуючи practically весь resource.

Ще сильніше:

> Sensitivity R=60–120 показує nonlinear increase optimal objective з diminishing marginal gains; отже additional resource має decreasing modeled value у цьому saturation structure.

---

## 64. Allowed conclusion nonconvex case

Слабкий:

> global optimum = 1.1145.

Обережніше:

> У bounded toy landscape multi-start із заданого набору starts знаходить best solution поблизу \(x\approx0.956,y\approx0\) з objective >1.11; independent grid search step=.05 дає objective within .01, що підсилює confidence у цьому best region, але не є formal proof global optimality.

Це саме той level precision, який підтримує evidence.

---

## 65. Research Transfer

Поставте питання:

> де у моєму research object очікується nonlinear response?

Можливі patterns:

- diminishing returns;
- saturation;
- threshold;
- synergy;
- conflict;
- quadratic penalty;
- probability response;
- exponential decay;
- logistic growth.

Шаблон:

~~~text
Research question:

Decision variables:

Parameters:

Nonlinear mechanism:

Objective:

Constraints:

Bounds:

Data source:

Starting points:

Solver:

Feasibility verification:

Multi-start plan:

Independent check:

Sensitivity parameter:

Uncertainty:

Limitations:

Allowed conclusion:
~~~

---

## 66. Не вставляйте nonlinear formula лише «щоб було складніше»

Nonlinearity повинна мати reason.

Наприклад:

- saturation observed in data;
- physics;
- known interaction;
- theoretical mechanism.

Formula без предметного пояснення не робить research stronger.

Вона лише робить computation harder.

---

## Поглиблення: що саме означає «надійний nonlinear optimum»

Для nonlinear optimization слово «надійний» повинно мати конкретний зміст.

### Numerical reliability

Solver converged repeatedly.

### Feasibility reliability

Constraints independently verified.

### Start reliability

Several starts lead to same or comparable best region.

### Cross-method reliability

Independent grid or another method supports the same region.

### Model reliability

Functional form and parameters have domain/data justification.

Ці levels утворюють evidence hierarchy.

Якщо є лише перший рівень:

> solver success,

висновок слабкий.

Якщо є всі п’ять, computational claim значно сильніший.

---

## Поглиблення: synthetic military interpretation без operational claims

Applied case можна уявити як allocation умовного навчального ресурсу між двома напрямами підготовки.

Кожен напрям має saturation:

> після певного рівня додаткове вкладення дає дедалі менший ефект.

Interaction term означає:

> певна частина корисності виникає лише коли обидва напрями підтримуються разом.

Це не реальна оцінка combat effectiveness.

Це pedagogical mechanism для пояснення:

- diminishing returns;
- synergy;
- constrained nonlinear allocation.

Nonconvex case взагалі не має domain semantics.

Він навмисно є **mathematical stress test** для optimizer.

Це теж важлива академічна дисципліна:

> не кожен teaching example потрібно маскувати під «реалістичний military case».

---

## Поглиблення: checklist перед claim про global optimum

Перед словами:

> «знайдено глобальний optimum»

перевірте:

1. Чи problem convex/concave у relevant sense?
2. Чи theorem гарантує local=global?
3. Якщо ні — які globality checks виконані?
4. Скільки starts?
5. Як вони обрані?
6. Чи перевірені boundaries?
7. Чи є independent method?
8. Який unresolved optimality gap?

Якщо formal guarantee немає, коректніше писати:

> best solution found under specified search and verification procedure.

Це не слабкість.

Це точність.

---

## 67. Мінісловник T2.L3

### Nonlinear function

Function, що не є affine combination variables.

### Diminishing returns

Decreasing marginal gain при зростанні input.

### Saturation

Approach to upper response limit.

### Interaction

Effect одного variable залежить від іншого.

### Local optimum

Best point only in neighborhood.

### Global optimum

Best point over entire feasible region.

### Start point

Initial guess numerical solver.

### Basin of attraction

Region starts converging to same local optimum.

### Multi-start

Repeated local optimization from several starts.

### Grid search

Explicit evaluation on discrete grid.

### Contour plot

Lines of equal objective value.

### Convergence

Algorithm stopping under numerical criterion.

### Convexity / concavity

Properties that determine whether local optimum can imply global optimum.

---

## 68. Мініексперимент

### Question 1

Чому \(F^*(R)\) зростає не лінійно?

Через saturation/diminishing returns.

### Question 2

Чому different successful starts можуть мати різні objective?

Non-convex landscape has multiple local maxima.

### Question 3

Навіщо grid search?

Independent coarse verification.

### Question 4

Чи grid step .05 proves global optimum?

Ні.

---

## 69. Одна сторінка підсумку

### П’ять ідей

1. Nonlinearity змінює geometry objective і optimization behavior.
2. Diminishing returns означає decreasing marginal effect.
3. success=True означає convergence, не globality.
4. Multi-start і independent grid check підсилюють evidence.
5. Model form повинна мати предметне або data-based обґрунтування.

### Три формули

Applied:

\[
F(x,y)=40(1-e^{-0.05x})+35(1-e^{-0.04y})+0.15\sqrt{xy}.
\]

Resource:

\[
x+y\le R.
\]

Nonconvex:

\[
G(x,y)=\sin(1.7x)\cos(1.3y)+0.15x-0.03(x^2+y^2).
\]

### Дві помилки

- «solver success = global optimum»;
- «складніша formula = краща model».

### Одне питання

> Який nonlinear mechanism у моєму research object можна обґрунтувати даними або theory?

### Наступний крок

Порівняйте applied sensitivity, запустіть nonconvex з кількох starts і перевірте best region grid search.

---

## 70. Фінальна думка

Нелінійна optimization model наближає нас до систем, де effect рідко зростає вічно й пропорційно.

Але разом із realism приходить нова відповідальність:

- algorithm може залежати від start;
- local optimum може маскуватися під «рішення»;
- visualization може створювати false confidence;
- verification потребує кількох незалежних підходів.

Тому головний lesson T2.L3 не «як викликати SciPy optimizer».

Головний lesson:

> **чим складніша geometry model, тим сильнішим має бути ланцюг доказів, що обчислювальний результат справді означає те, що ми про нього стверджуємо.**
