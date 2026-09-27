# MathModelingIT MiniBook T2.L6

## Системи комп'ютерної математики та їх можливості для математичного моделювання

### Від формули SymPy до незалежної чисельної перевірки

> **Головна ідея книги:** система комп’ютерної математики цінна не тим, що «вміє рахувати формули», а тим, що дозволяє пройти повний цикл: записати модель символічно, вивести структуру розв’язку, перевірити його алгебраїчно, перетворити на чисельну функцію, незалежно перевірити SciPy та провести параметричний експеримент.

---

## 0. Паспорт книги

**Код заняття:** T2.L6  
**Тема:** системи комп’ютерної математики та їх можливості  
**Рівень:** середній  
**Орієнтовний час читання:** 70–85 хвилин  
**Попередні знання:** похідна, інтеграл, просте ODE, Python functions, NumPy.

Після книги ви повинні вміти:

- задавати symbolic variables/functions у SymPy;
- формулювати differential equation;
- виводити equilibrium;
- читати closed-form solution;
- виконувати symbolic residual verification;
- інтегрувати symbolic expression;
- обчислювати symbolic sensitivity;
- використовувати lambdify;
- незалежно перевіряти trajectory через solve_ivp;
- оцінювати numerical error;
- знаходити threshold time;
- проводити parameter sensitivity;
- пояснювати, коли symbolic solution є перевагою, а коли numerical method необхідний.

---

## 1. Сцена: «Формула є. Але чому ми їй довіряємо?»

Уявімо synthetic dynamic system.

Є state \(S(t)\).

У систему постійно надходить resource with rate \(q\).

Втрати proportional to current state:

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

Хтось запускає SymPy й отримує formula.

І каже:

> «Готово. Комп’ютер дав розв’язок».

Але сильніший researcher запитає:

- чи formula satisfies ODE?
- чи initial condition виконується?
- що означає equilibrium?
- як parameter \(k\) впливає на state?
- чи numerical integrator дає ту саму trajectory?
- що буде, якщо symbolic solution unavailable?

Саме ці questions перетворюють CAS із «калькулятора» на research tool.

<figure>
  <img src="figures/fig_01_symbolic_numeric_pipeline.svg" alt="Symbolic-to-numeric pipeline">
  <figcaption><strong>Рис. 1.</strong> Сильний workflow: formulation → symbolic solution → symbolic verification → lambdify → independent numerical solve → sensitivity → interpretation.</figcaption>
</figure>

---

## 2. Центральна модель

\[
\frac{dS}{dt}=q-kS,
\qquad
S(0)=S_0.
\]

Де:

- \(S(t)\) — state;
- \(q\) — constant inflow;
- \(k>0\) — proportional loss coefficient;
- \(S_0\) — initial state.

Model is linear first-order ODE.

---

## 3. Інтуїція balance law

Right side:

\[
q-kS.
\]

Це:

> inflow − loss.

Якщо:

\[
q>kS,
\]

state grows.

Якщо:

\[
q<kS,
\]

state decreases.

If equal:

\[
q=kS,
\]

state stops changing.

That gives equilibrium.

---

## 4. Equilibrium

At equilibrium:

\[
\frac{dS}{dt}=0.
\]

Thus:

\[
q-kS^*=0.
\]

Therefore:

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

So:

\[
S^*=\frac{12}{0.1}=120.
\]

---

## 5. Why equilibrium matters

Equilibrium is not just an algebraic intermediate.

It answers:

> to what level does the system tend if parameters remain constant?

If:

\[
S_0<S^*,
\]

state rises.

If:

\[
S_0>S^*,
\]

state falls.

Baseline:

\[
S_0=20<120.
\]

Hence trajectory rises toward 120.

<figure>
  <img src="figures/fig_02_equilibrium_direction.svg" alt="Direction toward equilibrium">
  <figcaption><strong>Рис. 2.</strong> Знак \(q-kS\) визначає напрям руху state: нижче equilibrium trajectory зростає, вище — спадає.</figcaption>
</figure>

---

## 6. Closed-form solution

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

— equilibrium.

Друга:

\[
\left(S_0-S^*\right)e^{-kt}
\]

— transient deviation.

---

## 7. What exponential term means

\[
e^{-kt}
\]

decays toward zero.

Thus:

\[
S(t)\rightarrow S^*.
\]

Parameter \(k\) controls decay speed.

Large \(k\):

- stronger proportional loss;
- faster convergence;
- lower equilibrium \(q/k\).

So \(k\) affects both level and speed.

---

## 8. Initial condition check

At:

\[
t=0,
\]

\[
e^0=1.
\]

Therefore:

\[
S(0)=
\frac{q}{k}
+
\left(S_0-\frac{q}{k}\right)=S_0.
\]

This is simple manual verification.

---

## 9. Baseline trajectory

Parameters:

\[
q=12,\quad
k=0.10,\quad
S_0=20.
\]

Solution:

\[
S(t)=120-100e^{-0.1t}.
\]

At:

\[
t=10
\]

we get:

\[
S(10)\approx83.2121.
\]

This is a source-of-truth test value.

<figure>
  <img src="figures/fig_03_baseline_trajectory.svg" alt="Baseline trajectory toward equilibrium">
  <figcaption><strong>Рис. 3.</strong> Baseline state starts at 20 and monotonically approaches equilibrium 120. At \(t=10\), \(S\approx83.2121\).</figcaption>
</figure>

---

## 10. SymPy model

Symbolic setup:

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

This code mirrors notation.

---

## 11. Why symbolic assumptions matter

We declare:

\[
k>0.
\]

Why?

Because:

- equilibrium requires division by \(k\);
- model meaning says proportional loss positive;
- simplification can use positivity.

Symbolic systems reason better when assumptions explicit.

---

## 12. Symbolic equilibrium

SymPy solves:

\[
q-kS_{eq}=0.
\]

Result:

\[
S_{eq}=\frac{q}{k}.
\]

This is not difficult manually.

The point is not convenience.

The point is creating a symbolic object usable later.

---

## 13. Symbolic verification

Take candidate solution \(S_c(t)\).

Compute residual:

\[
R(t)=
\frac{dS_c}{dt}
-
(q-kS_c).
\]

If candidate is exact:

\[
R(t)=0.
\]

In code:

~~~python
residual = sp.simplify(
    sp.diff(solution, t)
    - (q - k*solution)
)
assert residual == 0
~~~

<figure>
  <img src="figures/fig_04_residual_verification.svg" alt="Symbolic residual verification">
  <figcaption><strong>Рис. 4.</strong> Residual check verifies the equation structurally for symbolic parameters, not only at several numerical points.</figcaption>
</figure>

---

## 14. Why residual check stronger than spot checks

Suppose we test:

\[
t=0,5,10.
\]

Candidate matches three points.

Could still be wrong elsewhere.

Symbolic residual:

\[
R(t)\equiv0
\]

checks identity under stated symbolic assumptions.

This is stronger evidence for algebraic correctness.

---

## 15. But symbolic residual does not validate the real model

Residual zero proves:

> formula solves equation.

It does not prove:

- equation describes real process;
- q constant;
- k constant;
- proportional-loss assumption true.

Again:

> verification ≠ validation.

---

## 16. Symbolic differentiation

Equilibrium:

\[
S^*=\frac{q}{k}.
\]

Sensitivity to \(q\):

\[
\frac{\partial S^*}{\partial q}
=
\frac{1}{k}.
\]

Sensitivity to \(k\):

\[
\frac{\partial S^*}{\partial k}
=
-\frac{q}{k^2}.
\]

These formulas show structure before any numbers.

---

## 17. Interpreting \(\partial S^*/\partial q\)

\[
\frac{1}{k}>0.
\]

Equilibrium grows when inflow grows.

At:

\[
k=0.1,
\]

\[
\frac{\partial S^*}{\partial q}=10.
\]

Locally, +1 in q changes equilibrium by +10.

---

## 18. Interpreting \(\partial S^*/\partial k\)

\[
-\frac{q}{k^2}<0.
\]

Increasing loss coefficient lowers equilibrium.

Baseline:

\[
-\frac{12}{0.1^2}=-1200.
\]

This large derivative reflects units and scale.

Do not interpret magnitude without units.

---

## 19. Relative sensitivity

Absolute derivative may look huge.

A dimensionless elasticity is often useful:

\[
E_k=
\frac{\partial S^*}{\partial k}
\frac{k}{S^*}.
\]

For:

\[
S^*=\frac{q}{k},
\]

we get:

\[
E_k=-1.
\]

So 1% increase in \(k\) gives approximately 1% decrease in equilibrium.

This is often more interpretable.

---

## 20. Symbolic integration

Sometimes question is not state at a moment.

We need cumulative exposure:

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

## 21. What cumulative state means

Depends on domain.

Could represent:

- accumulated availability;
- cumulative load;
- total exposure;
- area under state curve.

In synthetic lesson no operational interpretation is imposed.

The important idea:

> symbolic solution enables derived quantities.

---

## 22. Threshold time

Question:

> when does \(S(t)\) first reach target \(H\)?

Solve:

\[
H=
S^*+
(S_0-S^*)e^{-kt}.
\]

Then:

\[
e^{-kt}
=
\frac{H-S^*}{S_0-S^*}.
\]

Therefore:

\[
t=
-\frac{1}{k}
\ln
\left(
\frac{H-S^*}{S_0-S^*}
\right).
\]

For:

\[
H=80
\]

baseline:

\[
t\approx9.1629.
\]

---

## 23. Threshold validity

Target must lie between:

\[
S_0
\]

and:

\[
S^*.
\]

If target 150:

\[
150>120,
\]

baseline trajectory never reaches it.

Model raises ValueError.

This is semantic validation.

---

## 24. Equilibrium threshold

If target exactly:

\[
H=S^*,
\]

trajectory approaches asymptotically.

It does not reach in finite time.

Thus:

\[
t=\infty.
\]

This is a beautiful example where mathematical nuance matters.

---

## 25. Lambdify bridge

Symbolic expression useful for reasoning.

But to plot arrays, use:

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

This bridges symbolic and numerical worlds.

---

## 26. Why not rewrite formula manually

We could manually code:

~~~python
seq = q/k
return seq + (s0-seq)*np.exp(-k*t)
~~~

Current package has analytical_solution() exactly like that.

But lambdify adds verification:

> symbolic expression and direct numerical implementation agree.

Test checks it.

---

## 27. Independent numerical solution

Use solve_ivp on:

\[
\frac{dS}{dt}=q-kS.
\]

Numerical integrator does not use closed-form solution.

Therefore it is partially independent computational pathway.

If trajectories agree, confidence increases.

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

Strict tolerances support high agreement.

---

## 29. Error metric

Compare:

\[
e_i=
|S_{analytical}(t_i)-S_{numerical}(t_i)|.
\]

Maximum:

\[
e_{max}=\max_i e_i.
\]

Test requires:

\[
e_{max}<10^{-6}.
\]

<figure>
  <img src="figures/fig_05_three_trajectories.svg" alt="Analytical, lambdified and solve_ivp trajectories">
  <figcaption><strong>Рис. 5.</strong> Analytical NumPy, lambdified SymPy and independent solve_ivp trajectories should overlap within numerical tolerance.</figcaption>
</figure>

---

## 30. Agreement is evidence, not proof of adequacy

Three implementations agree.

This supports:

- derivation;
- coding;
- numerical integration.

Does not prove:

- model structure correct for real system.

This distinction repeats across course.

---

## 31. Parameter experiment in k

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

Results:

| k | S* | S(10) |
|---:|---:|---:|
| 0.05 | 240 | 106.56 |
| 0.08 | 150 | 91.59 |
| 0.10 | 120 | 83.21 |
| 0.12 | 100 | 75.90 |
| 0.15 | 80 | 66.61 |

---

## 32. Why equilibrium decreases

Formula:

\[
S^*=\frac{q}{k}.
\]

Increasing denominator reduces ratio.

Derivative confirms:

\[
\frac{\partial S^*}{\partial k}<0.
\]

Thus numerical table, formula and derivative tell same story.

<figure>
  <img src="figures/fig_06_k_sensitivity.svg" alt="Sensitivity to loss coefficient k">
  <figcaption><strong>Рис. 6.</strong> Increasing \(k\) lowers both equilibrium and \(S(10)\). Symbolic sensitivity explains the direction before numerical experiment.</figcaption>
</figure>

---

## 33. Why S(10) is not simply equilibrium

At finite time:

\[
S(10)\ne S^*
\]

unless system already at equilibrium or enough time passed.

Transient term still matters.

Therefore:

- equilibrium sensitivity;
- finite-horizon sensitivity

are related but distinct.

---

## 34. Time scale

Exponential decay characteristic time:

\[
\tau=\frac{1}{k}.
\]

Baseline:

\[
\tau=10.
\]

This gives intuition.

After several \(\tau\), transient becomes small.

Higher \(k\):

- smaller \(\tau\);
- faster convergence.

---

## 35. Half-life of deviation

Deviation:

\[
D(t)=S(t)-S^*.
\]

Then:

\[
D(t)=D(0)e^{-kt}.
\]

Time for deviation halve:

\[
t_{1/2}=
\frac{\ln2}{k}.
\]

Baseline:

\[
t_{1/2}\approx6.93.
\]

This is another derived symbolic insight.

---

## 36. CAS as structure explorer

SymPy helps ask:

- equilibrium?
- derivative?
- integral?
- threshold equation?
- asymptotic behavior?
- simplification?

This is more valuable than only numerical substitution.

---

## 37. Symbolic expression growth

Not every model yields elegant closed form.

For nonlinear or coupled systems SymPy may:

- return implicit form;
- return special functions;
- fail to solve;
- generate huge expression.

This is not failure of modeling.

It signals need for numerical methods.

---

## 38. Numerical methods are not second-class

If symbolic solution unavailable, solve_ivp may still be correct tool.

The goal is not:

> always find closed form.

The goal:

> choose representation suitable for question and verify it.

---

## 39. Symbolic vs numerical comparison

### Symbolic strengths

- exact structure;
- derivatives;
- integrals;
- simplification;
- parameter dependence.

### Numerical strengths

- complex models;
- nonlinear systems;
- time-varying coefficients;
- large systems;
- direct simulation.

Best workflow often combines both.

---

## 40. Зламай модель: k=0

Model assumes:

\[
k>0.
\]

If:

\[
k=0,
\]

equilibrium formula:

\[
q/k
\]

undefined.

But ODE becomes:

\[
\frac{dS}{dt}=q.
\]

Solution:

\[
S=S_0+qt.
\]

So k=0 is not impossible process.

It is outside current formula branch.

---

## 41. Зламай модель: q changes with time

Suppose:

\[
q=q(t).
\]

Then:

\[
\frac{dS}{dt}=q(t)-kS.
\]

Closed form may still exist for simple q(t), but baseline formula no longer valid.

Need re-derive.

---

## 42. Зламай модель: nonlinear loss

Suppose:

\[
\frac{dS}{dt}=q-kS^2.
\]

Equilibrium:

\[
S^*=\sqrt{q/k}.
\]

Dynamics nonlinear.

Different sensitivity and trajectory.

This is genuine model-class change.

---

## 43. Зламай модель: delay

Suppose loss depends on past:

\[
\frac{dS}{dt}
=
q-kS(t-\tau).
\]

Now delay differential equation.

Baseline ODE tools insufficient.

---

## 44. Зламай model: threshold process

Loss may activate only when:

\[
S>S_c.
\]

Then piecewise model.

Symbolic and numerical approach changes.

---

## 45. Validation hierarchy

<figure>
  <img src="figures/fig_07_verification_hierarchy.svg" alt="Verification hierarchy">
  <figcaption><strong>Рис. 7.</strong> Mathematical derivation, residual check, lambdify agreement and solve_ivp agreement verify computation at different levels; domain adequacy remains a separate question.</figcaption>
</figure>

Levels:

1. formulate ODE;
2. derive solution;
3. residual=0;
4. initial condition;
5. lambdify agreement;
6. solve_ivp agreement;
7. parameter experiment plausibility;
8. domain validation.

---

## 46. Python без страху: equilibrium

~~~python
value = equilibrium(
    q=12,
    k=0.1,
)
assert value == 120
~~~

Control test.

---

## 47. Python без страху: state t=10

~~~python
s10 = analytical_solution(
    10,
    q=12,
    k=0.1,
    s0=20,
)
~~~

Expected:

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

Expected:

\[
567.8794411714.
\]

---

## 49. Python без страху: threshold

~~~python
t80 = threshold_time(
    80,
    q=12,
    k=0.1,
    s0=20,
)
~~~

Expected:

\[
9.1629073187.
\]

---

## 50. Python без страху: verification error

~~~python
err = max_symbolic_numeric_error(
    times,
    q=12,
    k=0.1,
    s0=20,
)
assert err < 1e-6
~~~

This is explicit numerical criterion.

---

## 51. Predict before Run

Before sensitivity table, predict.

If \(k\) increases:

1. equilibrium?
2. convergence speed?
3. S(10)?
4. threshold time to 80?

Think before computation.

---

## 52. k affects two mechanisms

Increasing \(k\):

- lowers \(S^*=q/k\);
- makes exponent \(e^{-kt}\) decay faster.

These effects can pull finite-horizon state in nontrivial ways across different initial conditions.

Baseline both support lower S(10).

---

## 53. Scenario: S0 above equilibrium

Suppose:

\[
S_0=180>S^*=120.
\]

Then trajectory decreases toward 120.

Same formula.

This illustrates how initial state changes direction but not equilibrium.

---

## 54. Scenario: S0 exactly equilibrium

\[
S_0=S^*.
\]

Then transient coefficient zero:

\[
S_0-S^*=0.
\]

Hence:

\[
S(t)=S^*
\]

for all t.

This is valuable control case.

---

## 55. Scenario: q increase

If:

\[
q\uparrow,
\]

equilibrium increases linearly:

\[
S^*=\frac{q}{k}.
\]

Derivative constant for fixed k:

\[
1/k.
\]

This is simpler sensitivity than k.

---

## 56. Parameter identifiability intuition

Suppose only equilibrium observed:

\[
S^*=120.
\]

Many pairs satisfy:

\[
q/k=120.
\]

For example:

\[
q=12,k=0.1
\]

and:

\[
q=24,k=0.2.
\]

Equilibrium alone cannot identify both.

Trajectory speed helps identify k.

This is a deep research insight from symbolic structure.

---

## 57. Why time-series data matters

Transient term:

\[
e^{-kt}
\]

contains k directly.

Thus observations over time can distinguish parameter pairs with same equilibrium.

Symbolic model helps design data collection.

---

## 58. From solving to experimental design

This is why CAS matters in research.

It can reveal:

- which quantities depend on parameters;
- which observations identify them;
- which derivative is zero/nonzero;
- which measurement horizon informative.

Symbolic analysis informs experiment design.

---

## 59. Reproducibility

A complete T2.L6 experiment should save:

- symbolic form;
- baseline parameters;
- time grid;
- solve_ivp tolerances;
- comparison table;
- sensitivity table;
- summary;
- code commit.

Then agreement can be rebuilt.

---

## 60. Numerical tolerance

solve_ivp uses:

\[
rtol=10^{-10},
\]

\[
atol=10^{-12}.
\]

These are algorithm settings.

They influence numerical error and runtime.

Therefore they are part of reproducibility.

---

## 61. Error threshold vs exact equality

Do not assert:

\[
S_{analytical}=S_{numerical}
\]

bit-for-bit.

Numerical integration approximates.

Use tolerance:

\[
e_{max}<10^{-6}.
\]

This is correct computational reasoning.

---

## 62. Floating point

Even analytical NumPy evaluation uses floating point.

Symbolic expression exact in algebraic form.

Numerical substitution approximate.

This difference matters.

---

## 63. Symbolic simplification hazards

Equivalent expressions may look different.

Example:

\[
S^*+(S_0-S^*)e^{-kt}
\]

and expanded form.

String comparison is weak.

Use:

\[
sp.simplify(expr_1-expr_2)==0.
\]

This checks equivalence structurally.

---

## 64. Model audit

### Symbolic audit

- assumptions explicit?
- residual zero?
- initial condition?

### Numerical audit

- time grid valid?
- solver success?
- tolerance adequate?
- max error?

### Sensitivity audit

- parameter range meaningful?
- trend explained by formulas?

### Scientific audit

- q/k meanings justified?
- constant coefficients plausible?
- linear loss adequate?

---

## 65. Synthetic military context

Imagine \(S(t)\) as abstract readiness-support state in a training simulation.

\(q\) — synthetic replenishment intensity.

\(kS\) — synthetic proportional loss.

No actual readiness metric, logistics stock or operational coefficient is implied.

The purpose is mathematical structure only.

---

## 66. Research Transfer

Question:

> Яку частину мого dissertation model варто спочатку formalize symbolically, а яку verify numerically?

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

## 67. Example Research Transfer

Suppose process:

\[
\frac{dY}{dt}=a-bY.
\]

Symbolically derive:

- equilibrium;
- transient;
- derivative wrt parameters.

Numerically:

- solve_ivp;
- compare;
- sensitivity.

Then calibrate a,b from data in later work.

---

## 68. When symbolic method is especially useful

- small ODE;
- algebraic equilibrium;
- exact derivatives;
- parameter relations;
- transformations;
- asymptotic analysis.

---

## 69. When numerical method is especially useful

- nonlinear coupled systems;
- time-varying coefficients;
- discontinuities;
- no closed form;
- large state dimension;
- data-driven simulation.

---

## 70. Hybrid workflow

<figure>
  <img src="figures/fig_08_hybrid_method_map.svg" alt="Hybrid symbolic-numeric method map">
  <figcaption><strong>Рис. 8.</strong> Symbolic and numerical methods are complementary: symbolic reasoning exposes structure, numerical computation explores cases where closed form is unavailable or inconvenient.</figcaption>
</figure>

Best practice:

\[
Symbolic
\leftrightarrow
Numerical
\]

not competition.

---

## 71. Typical thinking errors

### «SymPy gave formula → model correct»

No.

Formula may solve wrong equation.

### «Residual zero → real system validated»

No.

Only equation verification.

### «solve_ivp matches → two independent truths»

They share same model assumptions.

### «More digits → more scientific»

No.

Reporting precision must reflect data/model quality.

### «Numerical method worse because approximate»

No.

Often it is the only practical method.

---

## 72. Allowed conclusion

Strong:

> For synthetic ODE \(dS/dt=q-kS\) with \(q=12,k=0.1,S_0=20\), symbolic solution gives equilibrium 120, \(S(10)\approx83.2121\), cumulative state over [0,10] ≈567.8794 and threshold time to 80 ≈9.1629. Symbolic residual is exactly zero, and independent solve_ivp trajectory agrees with the analytical solution within \(10^{-6}\) on the tested grid.

Then limitation:

> These checks verify the mathematical/computational implementation, not the adequacy of constant inflow and proportional-loss assumptions for a real system.

---

## 73. Від MiniBook до practice

Practical sequence:

1. define symbols;
2. write ODE;
3. derive solution;
4. residual check;
5. equilibrium;
6. sensitivity derivatives;
7. integral;
8. lambdify;
9. solve_ivp;
10. error;
11. k scenarios;
12. interpretation.

---

## 74. One-page summary

### П’ять головних ідей

1. CAS exposes mathematical structure.
2. Residual zero verifies symbolic solution.
3. Lambdify bridges symbolic and numerical representations.
4. solve_ivp provides independent numerical verification.
5. Verification of equation is not validation of real-world assumptions.

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

- «SymPy solved it = research complete»;
- «numerical match = real model adequate».

### Одне питання

> Яку structural information моя symbolic model can reveal before I launch a numerical experiment?

### Наступний крок

Reproduce baseline, verify residual, compare solve_ivp and run k-sensitivity.

---

## 75. Фінальна думка

Computer algebra and numerical methods are strongest together.

Symbolic layer answers:

> what does the model imply structurally?

Numerical layer answers:

> what happens for these parameters and scenarios?

Verification layer asks:

> do independent representations agree?

Research layer asks:

> are assumptions meaningful for the object?

A mature computational model moves through all four layers.

That is the real capability T2.L6 is designed to build.
