# MathModelingIT · Мінікнига T2.L7

## Використання систем комп’ютерної математики в наукових дослідженнях

### Від шумних спостережень до відтворюваного наукового висновку

> **Головна ідея книги:** науковий computational результат — це не підігнана крива і не одне число RMSE. Це ланцюг свідчення: дослідницьке питання → гіпотеза → дані → модель → калібрування → перевірка → прогноз → чутливість → невизначеність → відтворюваність → обережний наукове твердження.

---

## 0. Паспорт книги

**Код заняття:** T2.L7 
**Тип:** інтеграційний mini-research проєкт 
**Рівень:** підвищений 
**Орієнтовний час читання:** 80–95 хвилин.

Після книги ви повинні вміти:

- формулювати дослідницьке питання і перевірювана гіпотеза;
- відокремлювати спостереження від траєкторії моделі;
- калібрувати \(q,k\) методом нелінійний метод найменших квадратів;
- інтерпретувати RMSE без overclaim;
- будувати підігнана траєкторія;
- незалежно перевірити аналітичний розв’язок через solve_ivp;
- прогнозувати час досягнення порогу і стан на заданому горизонті;
- виконувати сценарій чутливість по \(q\);
- пояснювати нев’язка бутстреп;
- відрізняти невизначеність recalibration від стійкість фіксований decision;
- інтерпретувати скінченний/нескінченний поріг результати;
- формувати детермінований експеримент identity;
- писати науковий висновок, що не сильніший за свідчення.

---

## 1. Сцена: «Модель красиво підігнала дані. Чи можемо ми їй довіряти?»

Уявімо, що є синтетичний спостереження динамічний стан.

На графіку dots лежать близько до smooth curve.

Researcher запускає least_squares.

Отримує:

\[
RMSE\approx1.48.
\]

Виглядає переконливо.

І звучить фраза:

> «Модель підтверджена».

Але одразу виникають питання:

- які параметри estimated?
- чи параметр значення стійкий?
- чи підігнаний формула independently verified?
- яка невизначеність поріг прогноз?
- що станеться, якщо \(q\) зміниться?
- чи бутстреп інтервал умовний на chosen модель?
- чи можна точний експеримент reproduce?
- чи малий RMSE distinguishes альтернативна модель structures?

Саме цим T2.L7 відрізняється від простого curve fitting.

<figure>
 <img src="figures/fig_01_research_workflow.svg" alt="Повний дослідження workflow">
 <figcaption><strong>Рис. 1.</strong> T2.L7 з’єднує всі попередні теми в один дослідження workflow: питання, дані, калібрування, перевірка, чутливість, невизначеність, метадані та твердження.</figcaption>
</figure>

---

## 2. дослідницьке питання

заняття питання:

> **Наскільки надійно за шумними спостереженнями можна оцінити параметри динамічної системи та спрогнозувати час досягнення заданого порогу?**

Це питання має дві частини:

1. оцінювання параметрів;
2. надійність прогнозу.

калібрування без прогноз невизначеність відповідає лише на першу.

---

## 3. гіпотеза

робоча гіпотеза:

> калібрований модель відновить \(q,k\) із малою похибкою, а бутстреп покаже вузький, але ненульовий інтервал невизначеність поріг прогноз.

гіпотеза має бути linked до спостережуваними свідченнями:

- калібрований значення біля синтетичний generating параметри;
- RMSE малий;
- інтервал скінченний і не zero-width.

---

## 4. динамічний модель

\[
\frac{dS}{dt}=q-kS,
\]

\[
S(0)=S_0.
\]

аналітичний розв’язок:

\[
S(t)=
\frac{q}{k}
+
\left(
S_0-\frac{q}{k}
\right)e^{-kt}.
\]

Та сама математична основа, що й T2.L6.

Але дослідницька роль інша.

T2.L6: derive і перевірити.

T2.L7: оцінка параметри від noisy дані і quantify невизначеність.

---

## 5. синтетичні дані

спостережуваний pairs:

| t | спостережуваний S |
|---:|---:|
| 0 | 18.5724 |
| 2 | 38.5600 |
| 4 | 49.5546 |
| 6 | 67.6312 |
| 8 | 76.2160 |
| 10 | 82.6864 |
| 12 | 89.3191 |
| 14 | 95.8872 |
| 16 | 99.3286 |
| 18 | 103.0635 |
| 20 | 107.7626 |

дані intentionally contain noise.

отже параметри не може бути read directly від один точка.

---

## 6. чому синтетичні дані є корисний here

синтетичні дані allow контрольоване навчальне середовище:

- модель структура відомий;
- очікуваний параметри roughly відомий;
- немає sensitive дані;
- reproducible baseline;
- калібрування може бути checked.

але успішне відновлення на синтетичні дані не prove ефективність на реальних даних.

синтетичний перевірка є перевірка/етап навчання.

---

## 7. калібрування цільова функція

Let спостереження:

\[
y_i.
\]

модель прогноз:

\[
\hat y_i(q,k)=S(t_i;q,k).
\]

нев’язка:

\[
r_i(q,k)=\hat y_i-y_i.
\]

метод найменших квадратів minimizes:

\[
J(q,k)=
\sum_i r_i(q,k)^2.
\]

SciPy least_squares оцінки:

\[
\hat q,\hat k.
\]

---

## 8. чому нелінійний метод найменших квадратів

модель є нелінійний у \(k\) оскільки:

\[
e^{-kt}
\]

і:

\[
q/k.
\]

отже звичайна постановка лінійної регресії не directly match параметр структура.

Use нелінійний метод найменших квадратів.

---

## 9. калібрований baseline

точний поточний контрольний значення:

\[
\hat q
=
11.9159423611,
\]

\[
\hat k
=
0.0985939001.
\]

Estimated рівновага:

\[
\hat S^*
=
\frac{\hat q}{\hat k}
\approx120.8588193439.
\]

RMSE:

\[
RMSE\approx1.4821542085.
\]

ці добре узгоджуються з синтетичний параметрами генерації \(q\approx12,k\approx0.1\).

<figure>
 <img src="figures/fig_02_calibration_fit.svg" alt="калібрування підгонка">
 <figcaption><strong>Рис. 2.</strong> калібрування minimizes residuals між зашумленими спостереженнями і аналітичний траєкторія. візуально близьке наближення є свідчення приблизно якість підгонки, не доказ істинності моделі.</figcaption>
</figure>

---

## 10. RMSE

\[
RMSE=
\sqrt{
\frac1n
\sum_i
(y_i-\hat y_i)^2
}.
\]

це measures типовий модуль нев’язки у результат units.

Smaller є better **відносно контексту**.

RMSE не say:

- припущення коректний;
- параметри unique;
- predictions unbiased outside спостережуваного діапазону;
- немає альтернативна модель підходить так само добре.

---

## 11. Residuals

нев’язка:

\[
e_i=y_i-\hat y_i.
\]

Inspect:

- sign pattern;
- trend над time;
- changing variance;
- outliers;
- autocorrelation.

якщо residuals show структура, модель може бути не враховувати певний механізм.

 скалярний RMSE може hide це.

---

## 12. Identifiability connection

від T2.L6:

\[
S^*=q/k.
\]

рівновага сам по собі визначає лише відношення, не обидва параметри окремо.

перехідний траєкторія:

\[
e^{-kt}
\]

contains information приблизно \(k\).

тому time-series спостереження help identify обидва.

Це strong приклад символьний theory informing калібрування.

---

## 13. початковий guesses

least_squares починається від:

\[
q_0=10,
\qquad
k_0=0.08.
\]

для well-behaved baseline це converges до контрольний підгонка.

у нелінійний калібрування, starting точка може matter.

 сильніший дослідження workflow може перевірка множинний починається.

---

## 14. параметр bounds

реалізація constrains:

\[
q>0,
\]

\[
k>0.
\]

це encodes область зміст.

без bounds оптимізатор може explore physically meaningless regions.

---

## 15. підгонка є не валідація

 statement:

> RMSE <2.

supports:

> модель fits це синтетичні данінабір reasonably closely.

це не establish:

> реальний процес obeys \(dS/dt=q-kS\).

валідація requires незалежний реальний/authorized дані або область свідчення.

---

# прогноз

## 16. час досягнення порогу

поріг:

\[
S=80.
\]

Using калібрований параметри:

\[
t_{80}
\approx9.1648572165.
\]

Це точка оцінка.

це answers:

> за підігнаний модель, коли робить траєкторія reach 80?

---

## 17. стан на заданому горизонті

горизонт:

\[
t=20.
\]

прогноз:

\[
S(20)
\approx106.8197556402.
\]

Again, точка оцінка умовний на \(\hat q,\hat k\).

---

## 18. точка оцінка є не невизначеність

 single number:

\[
9.1649
\]

не tell:

- як sensitive це є до дані noise;
- як параметри co-vary;
- як часто поріг might бути unreachable за resampled fits.

Need невизначеність аналіз.

---

# перевірка

## 19. аналітичний траєкторія

калібрування uses аналітичний формула.

до перевірити реалізація, use незалежний чисельний ODE розв’язувач.

---

## 20. коректний initial-condition origin

важливий hardened rule:

\[
S_0
\]

є defined at:

\[
t=0.
\]

якщо requested результат сітка починається з \(t=5\), чисельний розв’язувач має усе ще integrate від нуля до requested times.

Earlier помилковий реалізація може reinterpret \(S_0\) як стан at перший requested time.

це було фіксований.

---

## 21. Nonzero-start контрольний приклад

для:

\[
t=[5,6,7],
\]

\[
S_0=20,
\]

\[
q=10,
\]

\[
k=0.1,
\]

аналітичний/чисельний перший requested стан є приблизно:

\[
S(5)\approx51.4775.
\]

не 20.

це перевірка protects математичний зміст початковий умова.

---

## 22. аналітичний порівняно з solve_ivp

Compute:

\[
e_{max}
=
\max_t
|S_{analytical}(t)-S_{numerical}(t)|.
\]

тести require:

\[
e_{max}<10^{-6}.
\]

експеримент usually obtains похибка навколо \(10^{-9}\).

<figure>
 <img src="figures/fig_03_verification.svg" alt="аналітичний versus чисельний перевірка">
 <figcaption><strong>Рис. 3.</strong> незалежний solve_ivp verifies чисельний consistency калібрований аналітичний траєкторія. Agreement supports реалізація, не empirical адекватність.</figcaption>
</figure>

---

## 23. що перевірка proves

це supports:

- аналітичний формула implemented correctly;
- чисельний розв’язувач initialized at коректний time;
- trajectories consistent.

це не prove:

- модель структура істинний;
- синтетичні дані representative;
- параметр оцінки unbiased.

---

# сценарій / чутливість

## 24. Vary q

конфігурація uses multipliers:

\[
0.8,\ 0.9,\ 1.0,\ 1.1,\ 1.2.
\]

для кожний:

\[
q'=m\hat q.
\]

Hold калібрований \(k\) фіксований.

Calculate:

- рівновага;
- \(S(20)\);
- time до поріг 80.

---

## 25. очікуваний напрям

як \(q\) зростає:

\[
S^*=\frac qk
\]

зростає.

стан на заданому горизонті зростає.

поріг 80 є reached sooner.

тести перевірити:

- \(S(20)\) monotonic increasing;
- час досягнення порогу monotonic decreasing.

---

## 26. чутливість є умовний

це експеримент зміни q лише.

це assumes k фіксований.

висновок:

> відгук до q за фіксований калібрований k.

не:

> complete невизначеність система.

<figure>
 <img src="figures/fig_04_sensitivity.svg" alt="чутливість до q">
 <figcaption><strong>Рис. 4.</strong> q-sensitivity asks controlled “що якщо?” питання: increasing replenishment raises стан на заданому горизонті і generally reduces time до поріг.</figcaption>
</figure>

---

## 27. One-factor limitation

якщо q і k uncertain together, однофакторний аналіз чутливості може miss взаємодія/correlation.

Possible розширення:

- 2D сітка;
- joint бутстреп;
- відгук surface.

T2.L7 baseline keeps one-factor сценарій для interpretability.

---

# бутстреп невизначеність

## 28. чому бутстреп

ми мають один noisy dataset.

Want до know:

> як much might підігнаний параметри і predictions vary оскільки спостереження contain noise?

нев’язка бутстреп approximates це невизначеність.

---

## 29. нев’язка бутстреп steps

1. підгонка модель до original спостереження.
2. Compute підігнаний значення.
3. Compute residuals:
   \[
   e_i=y_i-\hat y_i.
   \]
4. вибірка residuals з replacement.
5. Create синтетичний бутстреп dataset:
   \[
   y_i^{(b)}=\hat y_i+e_i^*.
   \]
6. Recalibrate q,k.
7. Recompute поріг і горизонт прогноз.
8. Repeat.

Baseline:

\[
B=500,
\]

\[
seed=2026.
\]

---

## 30. Recalibration є crucial

кожний бутстреп replication оцінки new:

\[
\hat q^{(b)},
\hat k^{(b)}.
\]

тому бутстреп розподіл represents:

> **невизначеність re-estimated параметри/predictions за residual-resampling припущення.**

це є не ефективність розподіл один фіксований параметр pair.

---

## 31. Це не fixed-decision стійкість

припустімо ми freeze:

\[
\hat q,\hat k
\]

і perturb середовище.

це asks another питання.

поточний бутстреп asks:

> якщо ми спостережуваний another noise реалізація і recalibrated, як would оцінки/predictions vary?

Keep ці concepts separate.

---

## 32. бутстреп поріг розподіл

для поточний 500-replication baseline:

\[
P_{2.5}
\approx8.9421,
\]

медіана:

\[
\approx9.1944,
\]

\[
P_{97.5}
\approx9.5252.
\]

середнє:

\[
\approx9.2020.
\]

точка оцінка:

\[
9.1649.
\]

 точка lies inside бутстреп інтервал.

<figure>
 <img src="figures/fig_05_bootstrap.svg" alt="бутстреп поріг розподіл">
 <figcaption><strong>Рис. 5.</strong> нев’язка бутстреп generates розподіл recalibrated поріг predictions. інтервал є умовний на residual-resampling і модель припущення.</figcaption>
</figure>

---

## 33. горизонт бутстреп

для \(S(20)\), поточний бутстреп approximately gives:

\[
P_{2.5}\approx104.8995,
\]

медіана:

\[
106.7010,
\]

\[
P_{97.5}\approx108.4714.
\]

середнє:

\[
106.7153.
\]

це quantifies калібрування/data-noise невизначеність у горизонт прогноз.

---

## 34. бутстреп інтервал є не universal truth

це є умовний на:

- chosen модель структура;
- нев’язка бутстреп procedure;
- спостережуваний дані;
- number повтори;
- початкове значення генератора для точний запуск.

якщо нев’язка припущення помилковий, інтервал може misrepresent невизначеність.

---

## 35. нев’язка бутстреп припущення

Implicitly residuals treated як exchangeable enough до resample.

якщо нев’язка variance зміни з time або residuals correlated, simple нев’язка бутстреп може бути inadequate.

Possible extensions:

- wild бутстреп;
- block бутстреп;
- parametric бутстреп.

---

# UNREACHED THRESHOLDS

## 36. поріг може бути unreachable

для some параметр combinations рівновага може lie нижче target.

тоді:

\[
t_{threshold}=\infty.
\]

Це meaningful.

це means за це траєкторії моделі never досягає поріг.

---

## 37. чому silently dropping infinity є dangerous

припустімо бутстреп times:

\[
[10,20,\infty,\infty,\infty].
\]

скінченний середнє:

\[
15.
\]

якщо report лише 15, you hide це 60% реалізації never reach поріг.

це було red-team finding і є now explicitly handled.

---

## 38. Hardened підсумок

quantile_summary reports:

- Умовне середнє;
- умовний медіана;
- finite_share;
- nonfinite_share;
- positive_infinity_share;
- n_total;
- n_finite.

для приклад:

\[
finite\_share=0.4,
\]

\[
nonfinite\_share=0.6.
\]

це makes conditioning visible.

<figure>
 <img src="figures/fig_06_finite_nonfinite.svg" alt="скінченний і нескінченний поріг результати">
 <figcaption><strong>Рис. 6.</strong> скінченний Умовне середнє має бути reported together з share simulations це actually reach поріг.</figcaption>
</figure>

---

## 39. Baseline скінченний share

для поточний 500 бутстреп повтори навколо підігнаний дані:

\[
finite\_share=1.0.
\]

усі бутстреп fits reach поріг 80.

Це baseline property.

у other scenarios це може не hold.

---

# відтворюваність

## 40. конфігурація records науковий intent

experiment_config stores:

- дослідницьке питання;
- гіпотеза;
- s0;
- поріг;
- горизонт;
- q multipliers;
- бутстреп повтори;
- початкове значення генератора.

Це сильніший than параметри scattered у ноутбук.

---

## 41. експеримент хеш includes дані

Unlike T1.L3 config-only хеш, T2.L7 експеримент хеш payload includes:

- конфігурація;
- rounded спостереження;
- модель identity string.

отже дані зміни alter експеримент ID.

це closes earlier походження gap.

---

## 42. Baseline експеримент identity

поточний canonical експеримент:

~~~text
t2_l7_92787dfc5ccd
~~~

Це детермінований для той самий payload.

це не replace Git коміт або залежність info, але це identifies модель+конфігурація+дані payload.

---

## 43. метадані

experiment.py stores:

- експеримент ID;
- модель;
- конфігурація;
- калібрований параметри;
- поріг невизначеність;
- горизонт невизначеність;
- перевірка похибка;
- Python/platform середовище.

результати include:

- calibration_summary.csv;
- scenario_results.csv;
- bootstrap_predictions.csv;
- summary.csv;
- metadata.json;
- figures.

---

## 44. чому метадані є part свідчення

 chart без метадані says:

> here є розподіл.

метадані lets us answer:

- який дані?
- який початкове значення генератора?
- як багато bootstraps?
- який поріг?
- який підгонка?
- який модель?

Це дослідження traceability.

---

# науковий інтерпретація

## 45. що модель shows

Supported:

> chosen динамічний модель може бути калібрований до синтетичний спостереження з RMSE навколо 1.48 і параметри біля параметрами генерації.

Supported:

> аналітичний і чисельний implementations agree within strict чисельний допуск.

Supported:

> поріг прогноз за калібрований модель є навколо 9.165 і нев’язка бутстреп gives nonzero невизначеність навколо це.

---

## 46. що модель не show

не established:

- істинний реальний система follows це ODE;
- похибки є iid/exchangeable;
- q,k remain сталий;
- поріг definition operationally valid;
- бутстреп інтервал covers усі невизначеність;
- калібрування unique за усі starting точки/модель structures.

ці є limitations.

---

## 47. малий RMSE може hide помилковий структура

два інший модель forms може підгонка спостережуваний window similarly.

приклад:

- exponential approach;
- flexible polynomial;
- logistic curve.

 низький RMSE лише measures підгонка у спостережуваний дані.

модель comparison і out-of-sample валідація потрібний для сильніший структурний твердження.

---

## 48. калібрування невизначеність порівняно з model-form невизначеність

бутстреп varies дані noise within фіксований модель форма.

це не vary рівняння itself.

отже інтервал omits структурний невизначеність.

це distinction слід appear у dissertation methodology.

---

## 49. чутливість порівняно з невизначеність

чутливість:

> deliberately зміна q і observe відгук.

невизначеність:

> quantify правдоподібний variation у оцінки/predictions due до noisy дані.

інший питання.

обидва потрібний.

---

## 50. перевірка порівняно з валідація

перевірка:

> рівняння/код agree.

валідація:

> модель adequate для target реальний процес.

T2.L7 provides strong перевірка.

Real-data валідація remains future робота.

---

## 51. дослідження висновок template

 strong висновок:

> Using синтетичний спостереження і модель \(dS/dt=q-kS\), нелінійний метод найменших квадратів estimated \(q=11.9159\) і \(k=0.098594\) з RMSE 1.482. підігнаний модель predicts поріг \(S=80\) at \(t=9.1649\) і \(S(20)=106.8198\). аналітичний і solve_ivp trajectories agree within чисельний допуск. 500-replication нев’язка бутстреп gives 95% empirical інтервал для час досягнення порогу approximately [8.942; 9.525]. ці результати quantify калібрування і residual-resampling невизначеність за selected модель; вони не validate модель для реальний система.

це є evidence-bounded language.

---

# злам модель

## 52. злам: зміна time origin

якщо чисельний integration починається з перший requested time натомість нуля, \(S_0\) gets reinterpreted.

це може produce internally smooth але помилковий траєкторія.

заняття перевірка protects against це.

---

## 53. злам: поріг вище рівновага

якщо:

\[
threshold>S^*,
\]

і \(S_0<S^*\), поріг unreachable.

Return:

\[
\infty.
\]

не force number.

---

## 54. злам: poor starting параметри

нелінійний метод найменших квадратів може бути sensitive до initialization у harder problems.

перевірка множинний починається якщо поверхня uncertain.

---

## 55. злам: heteroskedastic residuals

якщо noise grows з S, нев’язка resampling assumes помилковий структура.

Need weighted метод найменших квадратів або інший бутстреп.

---

## 56. злам: correlated residuals

Time-series нев’язка correlation violates naive exchangeability.

Block/бутстреп або явний похибка модель може бути потрібний.

---

## 57. злам: параметр drift

якщо q або k зміни над time:

\[
q=q(t),
\quad
k=k(t),
\]

constant-parameter ODE може підгонка average поведінка але miss mechanism.

---

## 58. злам: alternate модель

Try нелінійний втрата:

\[
\frac{dS}{dt}=q-kS^\gamma.
\]

якщо \(\gamma\ne1\) materially improves validated підгонка, baseline структура може бути insufficient.

модель comparison стає дослідницьке питання.

---

# PYTHON без FEAR

## 59. калібрування

~~~python
fit = calibrate_parameters(
    times,
    observations,
    s0=20,
)
~~~

перевірка:

\[
q\approx11.916,
\quad
k\approx0.09859.
\]

---

## 60. прогноз

~~~python
t80 = time_to_threshold(
    s0=20,
    q=fit["q"],
    k=fit["k"],
    threshold=80,
)
~~~

контрольний:

\[
9.164857.
\]

---

## 61. сценарій batch

~~~python
scenarios = scenario_batch(
    q_values,
    s0=20,
    k=fit["k"],
    horizon=20,
    threshold=80,
)
~~~

перевірити directions:

- s_horizon increasing;
- time_to_threshold decreasing.

---

## 62. бутстреп

~~~python
boot = bootstrap_calibration(
    times,
    observations,
    s0=20,
    threshold=80,
    horizon=20,
    n_boot=500,
    seed=2026,
)
~~~

точний repeatability з той самий початкове значення генератора є unit-tested.

---

## 63. Quantile підсумок

~~~python
summary = quantile_summary(
    boot,
    "time_to_threshold",
)
~~~

Always inspect:

- p2_5;
- медіана;
- p97_5;
- finite_share;
- nonfinite_share.

---

# дослідження TRANSFER

## 64. Transfer до dissertation

Use template:

~~~text
Research question:

Hypothesis:

Data:

Data provenance:

Mathematical model:

Parameters to estimate:

Calibration method:

Fit metric:

Independent verification:

Prediction target:

Scenario/sensitivity factors:

Uncertainty method:

Finite/nonfinite outcome rule:

Reproducibility ID:

Model limitations:

Validation data needed:

Allowed scientific claim:
~~~

---

## 65. приклад transfer

припустімо dissertation studies відгук time information-processing subsystem.

Possible workflow:

1. define динамічний/statistical модель;
2. collect authorized спостереження;
3. calibrate;
4. перевірити код на відомий приклади;
5. perform scenarios;
6. бутстреп параметр/прогноз невизначеність;
7. validate на held-out дані;
8. record експеримент ID і коміт.

 метод transfers без copying military-sensitive значення.

---

## 66. дослідження свідчення pyramid

<figure>
 <img src="figures/fig_07_evidence_pyramid.svg" alt="дослідження свідчення pyramid">
 <figcaption><strong>Рис. 7.</strong> підігнана крива є лише bottom шар. сильніший свідчення adds перевірка, чутливість, невизначеність, відтворюваність і external/область валідація.</figcaption>
</figure>

Layers:

1. підгонка;
2. перевірка;
3. чутливість;
4. невизначеність;
5. відтворюваність;
6. валідація.

---

## 67. Research-grade checklist

до публікація ask:

- питання явний?
- гіпотеза testable?
- дані походження відомий?
- модель припущення записані явно?
- калібрування reproducible?
- residuals inspected?
- чисельний реалізація verified?
- сценарій logic justified?
- бутстреп припущення stated?
- unreachable результати visible?
- експеримент ID recorded?
- Git/середовище recorded?
- висновок умовний?

---

## 68. Relationship до previous мінікниги

T2.L7 integrates:

- T1.L2 невизначеність;
- T1.L3 відтворюваність;
- T1.L4 вибір методу;
- T2.L3 nonлінійна оптимізація ideas;
- T2.L6 символьний/numeric перевірка.

це є курс’s дослідження synthesis.

---

## 69. One-page підсумок

### Five ideas

1. калібрування є лише один stage дослідження свідчення.
2. малий RMSE не validate модель структура.
3. незалежний solve_ivp перевірки computational consistency.
4. бутстреп quantifies recalibration невизначеність за явний припущення.
5. науковий висновок має preserve conditions, невизначеність і limitations.

### три formulas

модель:

\[
\frac{dS}{dt}=q-kS.
\]

Least-squares цільова функція:

\[
J(q,k)=\sum_i(\hat y_i-y_i)^2.
\]

поріг підсумок має pair умовний quantiles з:

\[
finite\_share=
\frac{n_{finite}}{n_{total}}.
\]

### два похибки

- narrow бутстреп інтервал = модель truth;
- малий RMSE = валідація.

### один питання

> що свідчення would усе ще бути потрібний до I use це калібрований модель до make реальний наукове твердження?

### Next крок

Reproduce експеримент ID, калібрування, перевірка, q-sensitivity і бутстреп до changing any припущення.

<figure>
 <img src="figures/fig_08_claim_boundary.svg" alt="межа наукове твердження">
 <figcaption><strong>Рис. 8.</strong> allowed твердження є bounded за дані, модель форма, калібрування, перевірка і невизначеність припущення. Beyond це межа begins speculation.</figcaption>
</figure>

---

## 70. Фінальна думка

 most dangerous computational результат є не один з visible похибка.

це є один це looks precise, fits nicely, і quietly carries припущення nobody wrote down.

T2.L7 builds opposite habit.

 дослідження результат слід say:

- що питання було asked;
- що модель було assumed;
- що дані були використаний;
- що було estimated;
- як реалізація було verified;
- як невизначеність було quantified;
- як sensitive прогноз є;
- як експеримент може бути reproduced;
- і що результат **не** prove.

це є difference між calculation і defensible computational дослідження твердження.
