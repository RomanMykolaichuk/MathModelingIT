# MathModelingIT · Мінікнига T1.L3

## Організація математичного моделювання

### Як перетворити код на відтворюваний дослідницький процес

> **Головна ідея книги:** математична модель у науковому дослідженні — це не лише формула й не лише ноутбук. Це простежуваний робочий процес, де Дослідницьке питання, дані, конфігурація, code, зерно генератора, результати, метадані і Git state дозволяють іншому досліднику відтворити саме той результат, на який ви посилаєтесь у статті чи дисертації.

---

## 0. Паспорт книги

**Код заняття:** T1.L3 
**Тема:** організація математичного моделювання 
**Рівень:** середній 
**Орієнтовний час читання:** 70–85 хвилин 
**Попередні знання:** базова Python-модель, CSV/JSON, поняття random зерно генератора, Git на рівні коміт.

Після цієї книги ви повинні вміти:

- розділяти Дослідницьке питання, дані, model, конфігурація, code і результати;
- пояснювати, чому ноутбук не повинен бути єдиним джерелом логіки;
- виносити параметри experiment у конфігурація;
- використовувати зерно генератора як частину ідентичність експерименту;
- формувати Первинні результати і підсумок окремо;
- розуміти роль метадані;
- пояснювати конфігурація хеш;
- відрізняти ВІДТВОРЮВАНІСТЬ від адекватність;
- пов’язувати result → experiment ID → конфігурація/дані → коміт Git;
- проектувати мінімальний відтворюваний Обчислювальний експеримент для власного дослідження.

---

## 1. Сцена: «А який саме запуск дав цей рисунок?»

Уявімо звичайну ситуацію під час підготовки дисертації.

У текст вставлено figure.

На ньому п’ять сценарії.

Через пів року керівник запитує:

> «Які параметри використовувалися саме тут?»

Відкривається ноутбук.

У ньому десятки комірки.

Деякі виконані в іншому порядку.

Частина параметри змінювалась вручну.

CSV уже оновлений.

зерно генератора не зафіксовано.

Файл figure називається:

~~~text
plot_final_v2_really_final.png
~~~

І головне питання стає несподівано складним:

> **чи можемо ми точно відтворити той computational result, на який посилається дисертація text?**

Саме це питання є центральним у T1.L3.

<figure>
 <img src="figures/fig_01_reproducibility_chain.svg" alt="Ланцюг від research question до Git">
 <figcaption><strong>Рис. 1.</strong> Відтворюваність виникає з повного ланцюга: питання → дані → конфігурація → model/code → experiment → результати → метадані → Git state.</figcaption>
</figure>

---

## 2. ВІДТВОРЮВАНІСТЬ — властивість робочий процес

Поширена помилка:

> «У мене є ноутбук, отже experiment відтворюваний».

Не обов’язково.

ноутбук може містити:

- прихований state;
- комірки виконані out порядок;
- manually змінений змінні;
- локальний файли;
- незадокументовані версії пакетів;
- випадкові вибірки без зерно генератора.

Тому ВІДТВОРЮВАНІСТЬ — це не format.

Це property весь робочий процес.

---

## 3. Центральна логіка

У lesson зафіксовано:

\[
Research\ question
\rightarrow
Data
\rightarrow
Config
\rightarrow
Model
\rightarrow
Code
\rightarrow
Experiment
\rightarrow
Verification
\rightarrow
Outputs
\rightarrow
Metadata
\rightarrow
Interpretation
\rightarrow
Git.
\]

Кожен елемент має окрему роль.

Якщо все змішано в одному ноутбук, простежуваність слабшає.

---

## 4. Дослідницьке питання — початок ідентичність

базовий питання:

> Як змінюється очікувана результативність системи при зміні ресурсу або навантаження, і як організувати цей experiment так, щоб його можна було точно повторити?

Це навмисно простий mathematics.

Бо lesson досліджує не складність формула.

Він досліджує **organization докази**.

---

## 5. Математична модель

детермінований part:

\[
Y=
\max(0,\ b+\alpha R-\beta L).
\]

Де:

- \(Y\) — modeled результативність;
- \(R\) — ресурс;
- \(L\) — навантаження;
- \(b\) — базовий рівень;
- \(\alpha\) — ресурс виграш;
- \(\beta\) — навантаження штраф.

базовий:

\[
b=20,
\]

\[
\alpha=1.8,
\]

\[
\beta=1.2.
\]

---

## 6. ручний контрольний приклад

При:

\[
R=40,
\]

\[
L=50
\]

отримуємо:

\[
Y=
20+1.8\cdot40-1.2\cdot50.
\]

\[
Y=20+72-60=32.
\]

Отже:

\[
Y=32.
\]

Це базовий ПЕРЕВІРКА випадок.

Якщо Python не повертає 32, проблема в реалізація.

---

## 7. обмеження знизу нулем

Model використовує:

\[
Y=\max(0,\cdots).
\]

Тому modeled результативність не від’ємний.

Наприклад:

\[
R=0,\quad L=100.
\]

первинний вираз:

\[
20-120=-100.
\]

Після clipping:

\[
Y=0.
\]

Це modeling припущення.

Не універсальний mathematical law.

---

## 8. стохастичний спостереження

спостережуваний result:

\[
Y^{obs}=
\max(0,Y+\varepsilon),
\]

де:

\[
\varepsilon\sim N(0,\sigma^2).
\]

базовий:

\[
\sigma=4.
\]

детермінована модель defines очікуваний structural відгук.

шум models між запусками варіативність.

---

## 9. Model vs experiment

Це ключове відмінність.

### Model

форма:

\[
Y=\max(0,b+\alpha R-\beta L).
\]

### Experiment

містить:

- який сценарії;
- як багато повторення;
- зерно генератора;
- noise_sd;
- результати;
- підсумок.

Змінити повторення:

\[
200\rightarrow1000
\]

— це зміна experiment.

Змінити:

\[
Y=b+\alpha R-\beta L
\]

на нелінійний формула — зміна model.

---

## 10. конфігурація як явний контракт

базовий experiment_config.json:

~~~json
{
  "seed": 2026,
  "replications": 200,
  "model": {
    "baseline": 20.0,
    "resource_gain": 1.8,
    "load_penalty": 1.2,
    "noise_sd": 4.0
  }
}
~~~

конфігурація робить параметри видимою.

<figure>
 <img src="figures/fig_02_config_separation.svg" alt="Розділення model code і config">
 <figcaption><strong>Рис. 2.</strong> Model code визначає mathematical співвідношення, а конфігурація — конкретні параметри experiment. Це дозволяє змінювати сценарій план без редагування основний функція.</figcaption>
</figure>

---

## 11. Чому приховані константи небезпечні

Погано:

~~~python
for _ in range(200):
    y = 20 + 1.8*r - 1.2*l
    obs = rng.normal(y, 4)
~~~

Numbers прихований всередині code.

Через місяць незрозуміло:

- що 200;
- чому 4;
- чи 1.8 базовий;
- чи цей файл використано для кінцевий result.

Краще:

> параметри зберігатися у конфігурація.

---

## 12. сценарії як дані

таблиця сценаріїв:

| сценарій | ресурс | навантаження |
|---|---:|---:|
| базовий | 40 | 50 |
| resource_low | 30 | 50 |
| resource_high | 50 | 50 |
| load_low | 40 | 35 |
| load_high | 40 | 65 |

сценарій definitions зберігаються в CSV.

Це дані layer.

---

## 13. Чому сценарії не треба hard-code

Hard-coded:

~~~python
scenarios = [
    ("baseline", 40, 50),
    ...
]
~~~

може працювати.

Але CSV:

- easier аудит;
- easier порівнювати;
- easier замінює;
- easier контроль версій diff;
- separates план експерименту з алгоритм.

---

## 14. базовий детермінований сценарій значення

### базовий

\[
R=40,L=50
\]

\[
Y=32.
\]

### resource_low

\[
R=30,L=50
\]

\[
Y=14.
\]

### resource_high

\[
R=50,L=50
\]

\[
Y=50.
\]

### load_low

\[
R=40,L=35
\]

\[
Y=50.
\]

### load_high

\[
R=40,L=65
\]

\[
Y=14.
\]

---

## 15. Однаковий результат — різний механізм

Зверніть увагу:

\[
resource\_high=50,
\]

і:

\[
load\_low=50.
\]

той самий детермінований відгук.

Але спочатку механізм:

> ресурс increased.

Second:

> навантаження decreased.

<figure>
 <img src="figures/fig_03_same_output_different_mechanism.svg" alt="Однаковий результат різних сценаріїв">
 <figcaption><strong>Рис. 3.</strong> Однакове числове \(Y=50\) не означає однаковий механізм. сценарій ідентичність і вхідні дані значення потрібно зберігати разом із result.</figcaption>
</figure>

Це важливий reason не до зберігати лише кінцевий показник.

---

## 16. повторення

Для кожного сценарій:

\[
n=200
\]

стохастичний спостереження.

Якщо сценарії=5:

\[
5\cdot200=1000
\]

первинний рядки.

рядок count — простий перевірка здорового глузду.

---

## 17. зерно генератора як experiment параметр

базовий:

\[
seed=2026.
\]

run_experiment() creates:

~~~python
rng = np.random.default_rng(2026)
~~~

той самий конфігурація + той самий сценарії + той самий code → той самий Первинні результати.

Це перевіряється тест.

---

## 18. ВІДТВОРЮВАНІСТЬ і випадковість

Це не contradiction.

стохастичний experiment може бути відтворюваний, якщо pseudo-випадкова послідовність контрольоване.

Тоді:

> випадковість exists всередині model, але computational реалізація є повторюваний.

Це fundamental idea наукові обчислення.

---

## 19. Первинні результати vs підсумок

Первинні результати містять один рядок на повторення.

Наприклад:

- scenario_id;
- ресурс;
- навантаження;
- повторення;
- deterministic_response;
- observed_response.

підсумок агрегує.

Це два різні артефакти.

---

## 20. Підсумкові показники

summarize_results() обчислює:

- deterministic_response;
- mean_observed;
- std_observed;
- p10;
- p90.

Це scenario-level підсумок.

<figure>
 <img src="figures/fig_04_raw_to_summary.svg" alt="Від raw results до summary">
 <figcaption><strong>Рис. 4.</strong> первинний дані зберігає кожну стохастичний повторення, підсумок стискає її до показників. Для відтворюваності бажано мати обидва рівні.</figcaption>
</figure>

---

## 21. базовий спостережуваний означає

README дає контрольні значення поблизу:

| сценарій | детермінований | середнє спостережуваний |
|---|---:|---:|
| базовий | 32.0 | ≈32.29 |
| resource_low | 14.0 | ≈14.07 |
| resource_high | 50.0 | ≈50.11 |
| load_low | 50.0 | ≈50.16 |
| load_high | 14.0 | ≈13.78 |

спостережуваний означає не точно детермінований значення тому що скінченний random вибірка.

але close.

---

## 22. чому p10 і p90

середнє самостійно hides spread.

p10:

> 10% спостереження нижче приблизно це значення.

p90:

> 90% спостереження нижче це значення.

інтервал:

\[
[p10,p90]
\]

є не формальний довірчий інтервал за допомогою default.

It є empirical квантиль діапазон.

---

## 23. метадані

metadata.json містить:

- experiment_id;
- config_hash;
- зерно генератора;
- повторення;
- scenario_count;
- model параметри;
- робочий процес note.

метадані answers:

> що точно згенерований ці результати?

---

## 24. канонічний JSON

хешування необхідно be стійкий.

якщо JSON ключі є перевпорядковані, experiment конфігурація зміст unchanged.

функція canonical_json:

- sort_keys=істинний;
- стійкий separators.

тоді SHA-256.

це підтримує детермінований ідентичність.

---

## 25. конфігурація хеш

\[
h=
SHA256(canonical\ config).
\]

Short форма спочатку 12 hex chars.

базовий:

~~~text
0c5d08ed47eb
~~~

experiment ID:

~~~text
t1_l3_0c5d08ed47eb
~~~

<figure>
 <img src="figures/fig_05_experiment_identity.svg" alt="Experiment ID через config hash">
 <figcaption><strong>Рис. 5.</strong> конфігурація хеш створює детермінований ідентичність конфігурації. Але повна ВІДТВОРЮВАНІСТЬ потребує також code, дані і програмне середовище.</figcaption>
</figure>

---

## 26. Що конфігурація хеш доводить

Він доводить:

> canonical конфігурація content той самий.

Він не доводить:

- code той самий;
- сценарії CSV той самий;
- NumPy той самий;
- model.py той самий;
- OS/середовище той самий.

Отже, конфігурація хеш — корисний, але partial ідентичність.

---

## 27. коміт Git

коміт Git ідентифікує code state.

Рекомендований chain:

\[
Result
\rightarrow
ExperimentID
\rightarrow
Config/Data
\rightarrow
GitCommit.
\]

Якщо figure у дисертація має це trace, it може be rebuilt.

---

## 28. програмне середовище

Навіть той самий code може поводитися differently з змінений залежності.

Тому ВІДТВОРЮВАНІСТЬ пакет має включати:

- Python версія;
- requirements;
- версії пакетів.

поточний repo pins залежності.

Це сильний foundation.

---

## 29. ПЕРЕВІРКА hierarchy

### Hand обчислення

\[
Y(40,50)=32.
\]

### межі

\[
Y\ge0.
\]

### зерно генератора ВІДТВОРЮВАНІСТЬ

той самий RNG зерно генератора → той самий спостереження послідовність.

### рядок count

\[
n_{rows}=n_{scenarios}\times n_{replications}.
\]

### конфігурація хеш стійкість

Key порядок робить не matter.

### Full запуск ВІДТВОРЮВАНІСТЬ

той самий вхідні дані produce identical results DataFrame.

---

## 30. тести є part дослідження інфраструктура

одиниця тести не лише програмний engineering.

They охоплювати інваріантний knowledge.

для T1.L3 тести document:

- базовий рівняння;
- clipping;
- вхідні дані validity;
- RNG ВІДТВОРЮВАНІСТЬ;
- робочий процес size;
- конфігурація ідентичність;
- метадані semantics.

це робить тести виконувана документація.

---

## 31. відтворюваний неправильний model

важливий sentence:

> **Відтворюваність неправильного припущення не робить модель адекватною.**

 ідеально відтворюваний experiment може послідовно reproduce неправильний припущення.

тому two axes:

- ВІДТВОРЮВАНІСТЬ;
- validity/адекватність.

---

## 32. ВІДТВОРЮВАНІСТЬ vs repeatability vs replicability

термінологія змінюється через дисципліни.

для це course практичний зміст:

> інший дослідник може відтворити той самий computational result з збережені артефакти.

робити не get втрачено у термінологія.

фокус на traceability.

---

## 33. ноутбук role

ноутбук є корисний для:

- exploration;
- narrative;
- visualization;
- interactive аналіз.

але основний model logic слід зберігатися у src/.

чому?

- importable;
- testable;
- reusable;
- easier CI;
- менше прихований state.

---

## 34. прихований state задача

у ноутбук:

cell 10 може depend на змінна змінений у cell 3 після cell 7 вже ran.

файл appears правильний.

Kernel state є не.

сильний робочий процес:

> Restart kernel → запуск усі → однаковий результат.

Even сильнішого:

> main experiment запуски з команда line незалежний ноутбук.

---

## 35. результати слід be згенерований, не відредаговані

results.csv і summary.csv є похідні.

робити не manually правильний them.

якщо result неправильний:

- fix model/конфігурація/дані;
- rerun.

ручний editing breaks походження даних і результату.

---

## 36. Naming результати

Avoid:

~~~text
final.csv
final2.csv
really_final.csv
~~~

кращий:

- фіксований шляхи всередині experiment каталог;
- experiment ID каталог;
- метадані alongside результати.

для великий дослідження проєкт, experiment_id може name запуск каталог.

---

## 37. сценарій походження даних і результату

якщо scenarios.csv зміни, конфігурація хеш самостійно робить не detect it.

це reveals поточний limitation.

Possible improvement:

- дані файл хеш;
- combined хеш експерименту;
- коміт Git captures файл state.

це є excellent “Зламай модель/робочий процес” випадок.

---

## 38. Зламай робочий процес: той самий конфігурація, змінений CSV

Keep:

~~~text
experiment_config.json
~~~

unchanged.

зміна resource_high з 50 до 55.

конфігурація хеш unchanged.

але experiment змінений.

тому:

> config_hash ≠ complete хеш експерименту.

Modernization:

- хеш конфігурація + вхідні дані файли;
- або rely на Git state + явний файл hashes.

---

## 39. Зламай робочий процес: той самий конфігурація, змінений model.py

зміна:

\[
\alpha=1.8
\]

default у code поки конфігурація усе ще supplies 1.8? No ефект.

але зміна формула itself:

\[
Y=b+\alpha\log(1+R)-\beta L.
\]

конфігурація хеш unchanged.

ідентичність експерименту string unchanged.

Result різний.

Hence code версія необхідно be зафіксований.

---

## 40. Зламай робочий процес: unpinned залежності

припустімо future NumPy поведінку зміни.

той самий code/конфігурація може produce різний результат або warning.

тому залежність snapshot має значення.

---

## 41. Зламай робочий процес: зерно генератора removed

без фіксований зерно генератора:

- Первинні результати зміна;
- debugging складніших;
- figure не точно відтворюваний.

статистичну підсумок може be подібний, але точний артефакт ідентичність втрачено.

---

## 42. Зламай робочий процес: ручний figure edits

якщо figure експортований, тоді manually скориговані дані точки у зображення редактор, code може no longer reproduce figure.

Allowed ручний зміни:

- layout;
- labels;
- typography.

не allowed:

- зміна значення без джерело update.

---

## 43. конфігурація зміна vs model зміна

зміна:

\[
noise\_sd=4\rightarrow6.
\]

Experiment конфігурація зміна.

зміна:

\[
Y=\max(0,b+\alpha R-\beta L)
\]

до нелінійний співвідношення.

Model зміна.

ці слід be переглядатися differently.

---

## 44. чутливість via сценарії

сценарії alter вхідні дані:

- ресурс;
- навантаження.

конфігурація alters глобальний model/experiment параметри:

- повторення;
- зерно генератора;
- noise_sd.

це розділення дає структурований план.

---

## 45. Noise_sd experiment

якщо:

\[
\sigma=4\rightarrow8,
\]

детермінований відгук unchanged.

середнє спостережуваний ймовірно залишається близько детермінований значення у симетричний, non-clipped regions.

Spread збільшує.

у низький детермінований значення clipping може affect середнє.

це пов’язує T1.L3 з T1.L2 невизначеність concepts.

---

## 46. повторення experiment

збільшення:

\[
n=200\rightarrow2000.
\]

первинний підсумок означає часто stabilize.

але більше запуски робити не fix неправильний model.

той самий lesson як Монте-Карло.

---

## 47. Git traceability

 сильний report block:

~~~text
experiment_id: t1_l3_0c5d08ed47eb
config_hash: 0c5d08ed47eb
seed: 2026
Git commit: <sha>
input data: data/scenarios.csv
output files:
  - results.csv
  - summary.csv
  - metadata.json
~~~

це є малий але сильний.

---

## 48. Figure походження даних і результату

<figure>
 <img src="figures/fig_06_figure_provenance.svg" alt="Простежуваність рисунка">
 <figcaption><strong>Рис. 6.</strong> Figure у публікація повинна мати шлях назад до результат дані, experiment ID, конфігурація/дані та code версія.</figcaption>
</figure>

ідеальний chain:

\[
Figure
\rightarrow
Summary/RawData
\rightarrow
ExperimentID
\rightarrow
Config
\rightarrow
InputData
\rightarrow
Commit.
\]

---

## 49. метадані як науковий докази

метадані є не decoration.

It дозволяє питання:

- що зерно генератора?
- що конфігурація?
- як багато сценарії?
- який параметри?
- що ідентичність експерименту?

без метадані результат файл є orphaned.

---

## 50. ВІДТВОРЮВАНІСТЬ checklist

до citing result:

### Дослідницьке питання

відомий?

### дані

Stored і documented?

### Model

формула і припущення явний?

### конфігурація

параметри externalized?

### Execution

один команда?

### ПЕРЕВІРКА

контрольний приклад?

### метадані

Experiment ID/хеш?

### Git

Code версія відомий?

### інтерпретація

No overclaim?

---

## 51. Predict до запуск

до зміною конфігурація, write:

### якщо повторення ↑

що зміни?

### якщо noise_sd ↑

що зміни?

### якщо зерно генератора зміни лише

що зміни?

очікуваний:

- первинний спостереження зміна;
- детермінований відгук unchanged;
- розподіл shape подібний у aggregate.

---

## 52. Python без страху: детермінований відгук

~~~python
y = deterministic_response(
    resource=40,
    load=50,
)
assert y == 32
~~~

це є direct ПЕРЕВІРКА.

---

## 53. Python без страху: запуск experiment

~~~python
results = run_experiment(
    config,
    scenarios,
)
~~~

очікуваний рядок count:

\[
5\times200=1000.
\]

---

## 54. Python без страху: підсумок

~~~python
summary = summarize_results(results)
~~~

результат містить:

- детермінований;
- середнє;
- std;
- p10;
- p90.

---

## 55. Python без страху: конфігурація хеш

~~~python
experiment_id = (
    "t1_l3_" + config_hash(config)
)
~~~

базовий:

~~~text
t1_l3_0c5d08ed47eb
~~~

---

## 56. чому хеш key порядок стійкий

конфігурація:

~~~json
{"seed":2026,"replications":200}
~~~

і:

~~~json
{"replications":200,"seed":2026}
~~~

той самий semantic mapping.

canonical_json sorts ключі.

отже той самий хеш.

це є перевірено тестами.

---

## 57. синтетичний military context

припустімо \(Y\) є синтетичний результативність indicator training-support process.

\(R\) — умовний ресурс.

\(L\) — умовний workload.

No реальний одиниця, no фактичний operational результативність.

 випадок demonstrates робочий процес, не реальний рішення recommendation.

---

## 58. Перенесення в дослідження

питання:

> Як організувати Обчислювальний експеримент для одного fragment власної дисертація?

Template:

~~~text
Research question:

Input data:

Data provenance:

Mathematical model:

Config parameters:

Scenario file:

Random seed:

Replications:

Verification case:

Raw outputs:

Summary outputs:

Metadata:

Experiment ID:

Git commit:

Software environment:

Limitations:

Allowed conclusion:
~~~

---

## 59. приклад transfer: model калібрування робочий процес

Imagine дисертація model оцінки параметр з Синтетичні дані.

відтворюваний робочий процес:

1. первинний дані файл;
2. preprocessing скрипт;
3. калібрування конфігурація;
4. зерно генератора;
5. підігнаний параметри;
6. diagnostic plots;
7. метадані;
8. коміт;
9. result table.

T1.L3 структура переноситься безпосередньо.

---

## 60. Versioning дані

Git працює well для малий text CSV.

великий або чутливий дані може need:

- дані registry;
- object storage;
- checksum;
- access-controlled репозиторій.

важливий principle залишається:

> result необхідно reference точний дані версія.

---

## 61. чутливий/closed дані

у military дослідження, дані може не be publishable.

ВІДТВОРЮВАНІСТЬ усе ще possible всередині контрольоване середовище.

Preserve:

- дані версія ID;
- хеш;
- schema;
- access conditions;
- code/конфігурація.

Public артефакт може використовувати синтетичний equivalent поки documenting різниця.

---

## 62. середовище snapshot

Requirements файл дає залежність версії.

для сильнішого ВІДТВОРЮВАНІСТЬ також record:

- Python версія;
- OS/container зображення;
- hardware якщо суттєвий;
- CUDA/GPU для стохастичний/чисельний workloads де results depend на backend.

не кожен experiment needs усі details.

Record що може суттєво зміна results.

---

## 63. детермінований результати є не автоматично відтворюваний

Even детермінований формула може fail ВІДТВОРЮВАНІСТЬ якщо:

- дані змінений;
- code змінений;
- конфігурація unknown;
- preprocessing прихований.

випадковість є не лише threat.

---

## 64. ВІДТВОРЮВАНІСТЬ levels

### рівень 0

Screenshot лише.

### рівень 1

ноутбук + дані.

### рівень 2

src + конфігурація + дані + зерно генератора.

### рівень 3

тести + метадані + коміт Git.

### рівень 4

середовище + automated pipeline/CI.

Course aims до рівень 3–4.

<figure>
 <img src="figures/fig_07_reproducibility_levels.svg" alt="Рівні відтворюваності">
 <figcaption><strong>Рис. 7.</strong> ВІДТВОРЮВАНІСТЬ посилюється шарами: артефакт → code/дані → конфігурація/зерно генератора → тести/метадані/Git → automated середовище.</figcaption>
</figure>

---

## 65. CI як ВІДТВОРЮВАНІСТЬ assistant

Course CI executes тести і notebooks.

It cannot довести дослідження validity.

але it може detect:

- broken imports;
- змінений контрольні значення;
- missing файли;
- non-executable ноутбук.

Automation зменшує accidental drift.

---

## 66. Зламай систему: result без ідентичність

припустімо summary.csv says:

~~~text
baseline mean_observed=32.29
~~~

але no конфігурація/хеш/коміт.

може we використовувати кількість?

We може read it.

може we defend its походження даних і результату?

Weakly.

отже result без ідентичність є scientifically fragile.

---

## 67. типову thinking похибки

### «Якщо код є, результат відтворюваний»

не достатньо.

### «той самий конфігурація хеш = той самий experiment»

не якщо дані/code differ.

### «Git replaces метадані»

No.

Git ідентифікує репозиторій state, метадані ідентифікує запуск.

### «зерно генератора робить стохастичний висновок істинний»

No.

зерно генератора робить запуск повторюваний.

### «відтворюваний = valid»

No.

неправильний model може reproduce ідеально.

---

## 68. Model аудит vs робочий процес аудит

### Model аудит

- формула;
- припущення;
- параметри;
- адекватність.

### робочий процес аудит

- файли;
- конфігурація;
- execution;
- метадані;
- versioning.

сильний дисертація computational працювати needs обидва.

---

## 69. One-command principle

 good experiment слід мають clear команда:

~~~bash
python -m lessons.t1_l3.src.experiment
~~~

це зменшує прихований ручний кроки.

якщо full rebuild потребує 17 незадокументовані clicks, ВІДТВОРЮВАНІСТЬ suffers.

---

## 70. Immutable первинний вхідні дані

Ideally первинний вхідні дані є не overwritten за допомогою experiment.

похідні дані goes до результати.

це preserves джерело.

для transformations, зберігати скрипт і intermediate якщо scientifically суттєвий.

---

## 71. результат overwrite issue

поточний lesson writes фіксований результати каталог.

для навчальний це є простий.

для дослідження масштаб, overwriting старий experiment може be undesirable.

Modernization:

~~~text
outputs/<experiment_id>/
~~~

або позначка часу + хеш.

тоді запуски coexist.

---

## 72. Experiment registry

 малий CSV/JSON index може contain:

- experiment_id;
- date;
- коміт;
- конфігурація;
- note;
- status.

це helps великий дисертація projects.

не required базовий, але natural extension.

---

## 73. Допустимий висновок

сильний:

> для конфігурація хеш 0c5d08ed47eb, зерно генератора 2026 і five сценарії з 200 повторення кожен, базовий детермінований відгук є 32 і середнє спостережуваний є приблизно 32.29. result є відтворюваний для той самий code, конфігурація, сценарій дані і програмне середовище.

також state:

> це робить не validate лінійний ресурс/навантаження припущення.

---

## 74. Від MiniBook до practice

до практичний:

1. запуск базовий;
2. record experiment_id;
3. перевірити Y=32;
4. rerun і порівнювати results;
5. зміна лише зерно генератора;
6. зміна конфігурація;
7. add сценарії;
8. record коміт Git.

---

## 75. дослідження артефакт passport

Create для кожен важливий result:

~~~text
Result:
Research question:
Experiment ID:
Config hash:
Input data:
Model version:
Seed:
Replications:
Git commit:
Environment:
Verification:
Limitations:
Publication use:
~~~

це є практичний дисертація discipline.

---

## 76. робочий процес architecture

<figure>
 <img src="figures/fig_08_project_architecture.svg" alt="Архітектура reproducible project">
 <figcaption><strong>Рис. 8.</strong> Хороша структура розділяє джерело code, вхідні дані, конфігурація, notebooks і згенерований результати. Кожен шар має власну responsibility.</figcaption>
</figure>

Recommended:

~~~text
data/
config
src/
tests/
notebooks/
outputs/
metadata
README
Git
~~~

---

## Поглиблення: ВІДТВОРЮВАНІСТЬ має кілька рівнів ідентичність

У базовий experiment_id залежить від конфігурація.

Але повний computational result залежить на broader state.

Корисно мислити шарами.

### конфігурація ідентичність

\[
ID_{config}=Hash(config).
\]

### дані ідентичність

\[
ID_{data}=Hash(input\ files).
\]

### Code ідентичність

коміт Git:

\[
ID_{code}=commit\ SHA.
\]

### середовище ідентичність

залежність lock / container digest.

### запуск ідентичність

Може комбінувати:

\[
ID_{run}
=
f(
ID_{config},
ID_{data},
ID_{code},
ID_{env}
).
\]

Course реалізація intentionally simpler.

Але ця hierarchy показує шлях розвитку дисертація інфраструктура.

---

## Поглиблення: чому коміт Git самостійно є не достатньо

коміт Git tells точний репозиторій state лише якщо:

- усі суттєвий файли tracked;
- no uncommitted зміни;
- external дані версія відомий;
- середовище відомий.

якщо локальний скрипт modified але не committed, коміт SHA точки до інший state.

тому публікація запуск слід ideally початок з clean робочий tree.

якщо не, це є ВІДТВОРЮВАНІСТЬ limitation.

---

## Поглиблення: незбережені зміни робочого дерева

Imagine:

- коміт = abc123;
- model.py відредаговані locally;
- experiment запуск;
- зміна не committed.

метадані фіксує abc123.

пізніше checkout abc123 дає старий model.

Result cannot be reproduced точно.

Possible improvement:

- refuse публікація запуск коли repo dirty;
- record diff;
- auto-capture patch.

для course, awareness є достатньо.

---

## Поглиблення: вхідні дані дані хешування

конфігурація хеш захищає конфігурація.

Add:

\[
h_{data}=SHA256(file\ bytes).
\]

тоді метадані може включати scenario-data checksum.

Now сценарій зміна detectable even якщо filename той самий.

це безпосередньо fixes один break-the-workflow випадок.

---

## Поглиблення: code версія у метадані

поточний метадані note says відтворюваний для той самий code/конфігурація/дані/середовище.

 сильнішого реалізація could автоматично query коміт Git і store it.

якщо Git недоступний, метадані слід state:

~~~text
git_commit: unavailable
~~~

rather ніж invent certainty.

---

## Поглиблення: залежність snapshot

Pinned requirements у репозиторій допомагають.

але installed середовище може усе ще differ якщо user ignores them.

 запуск може record:

~~~text
python --version
pip freeze
~~~

або selected критичний версії.

для науковий працювати корисний fields включати:

- Python;
- NumPy;
- pandas;
- SciPy;
- SymPy;
- Matplotlib.

для GPU workflows також backend версії.

---

## Поглиблення: середовище ВІДТВОРЮВАНІСТЬ vs portability

точний середовище повторення є сильний але може become brittle над years.

альтернатива goal:

> portable ВІДТВОРЮВАНІСТЬ.

що означає code працює за documented версія діапазон, з тести verifying результати/tolerances.

там є trade-off між freezing everything точно і maintaining portable tested пакет.

Course chooses pinned stack для educational стійкість.

---

## Поглиблення: первинний дані слід be immutable

 сильний rule:

> первинний вхідні дані є ніколи overwritten за допомогою experiment.

чому?

якщо той самий файл є modified in-place, historical result loses джерело.

Prefer:

~~~text
data/raw/
data/processed/
outputs/
~~~

Transformation скрипт creates processed дані з первинний.

тоді походження даних і результату є явний.

---

## Поглиблення: preprocessing є part model pipeline

Researchers інколи think:

> preprocessing є just preparation.

але filtering, imputation, нормалізація і агрегування може зміна results.

тому preprocessing code belongs у ВІДТВОРЮВАНІСТЬ chain.

якщо CSV є manually cleaned у spreadsheet і overwritten, походження даних і результату weakens.

---

## Поглиблення: experiment конфігурація schema

JSON конфігурація є корисний, але може contain invalid типи.

для larger проєкт визначити schema:

- required ключі;
- тип обмеження;
- allowed ranges;
- defaults.

поточний validate_config перевірки:

- зерно генератора;
- повторення;
- model;
- додатний повторення;
- невід’ємні noise_sd.

це є спочатку крок до schema валідація.

---

## Поглиблення: чому явний валідація має значення

без валідація від’ємний повторення count або від’ємний шум значення could fail strangely пізніше.

валідація creates early, meaningful похибка.

це є part науковий якість.

Bad вхідні дані слід be rejected до expensive computation.

---

## Поглиблення: результат determinism

для той самий конфігурація/дані/code/зерно генератора базовий первинний DataFrame слід be identical.

тест:

~~~python
pd.testing.assert_frame_equal(a, b)
~~~

це є сильнішого ніж saying що означає є close.

It перевірки точний computational repeatability.

для деяких parallel/GPU workflows bitwise ідентичність може не be realistic.

тоді ВІДТВОРЮВАНІСТЬ критерій необхідно використовувати tolerances.

---

## Поглиблення: точний vs статистичну ВІДТВОРЮВАНІСТЬ

### точний

той самий первинний numbers.

Appropriate для це CPU псевдовипадковий робочий процес.

### чисельний

Differences у межах допуск.

Common для floating-point solvers.

### статистичну

різний draws але той самий distribution-level висновки.

Common для стохастичний HPC.

до claiming ВІДТВОРЮВАНІСТЬ визначити який рівень intended.

---

## Поглиблення: experiment registry план

коли дисертація має багато запуски, один метадані файл на результат каталог є не достатньо для overview.

Create registry:

| experiment_id | коміт | конфігурація | дані | purpose | status |
|---|---|---|---|---|---|
| exp001 | abc | cfg1 | d1 | базовий | accepted |
| exp002 | def | cfg2 | d1 | чутливість | exploratory |

це prevents “який запуск було кінцевий?” confusion.

---

## Поглиблення: exploratory vs confirmatory запуски

During exploration дослідник tries багато configs.

пізніше select аналіз plan.

It є корисний до mark:

- exploratory;
- валідація;
- кінцевий/публікація.

Otherwise result selection може be opaque.

метадані може включати purpose tag.

---

## Поглиблення: публікаційний артефакт mapping

припустімо дисертація містить:

- Table 3.2;
- Figure 3.4;
- показник у paragraph.

Create mapping:

~~~text
Figure 3.4 -> experiment_id X -> script Y -> output Z
Table 3.2  -> experiment_id Q -> summary.csv
~~~

тоді revision стає manageable.

---

## Поглиблення: один еталонна реалізація для figures

робити не copy значення manually з terminal у Excel, тоді chart.

кращий:

\[
data
\rightarrow
script
\rightarrow
figure.
\]

якщо style adjustment потрібні, скрипт controls it.

це зберігає numbers linked до computation.

---

## Поглиблення: checksums для публікація артефакти

для кінцевий figure або table, optional checksum може довести файл ідентичність.

для приклад:

\[
SHA256(figure.png).
\]

це може be overkill для classroom використовувати.

але корисний у audited pipelines.

---

## Поглиблення: ВІДТВОРЮВАНІСТЬ за closed-data обмеження

Military і defence дослідження може мають дані що cannot leave secure середовище.

ВІДТВОРЮВАНІСТЬ може усе ще be designed.

всередині secure мережевий preserve:

- точний первинний дані;
- версія/хеш;
- scripts;
- конфігурація;
- середовище;
- результати;
- access rules.

поза secure мережевий publish:

- синтетичний dataset;
- schema;
- метод;
- обмеження.

робити не confuse public ВІДТВОРЮВАНІСТЬ з internal ВІДТВОРЮВАНІСТЬ.

---

## Поглиблення: синтетичний twin dataset

 корисний шаблон:

1. confidential реальний dataset використано у secure аналіз;
2. синтетичний dataset preserves структура, не чутливий значення;
3. public repo demonstrates робочий процес;
4. secure метадані links internal result до реальні дані версія.

це підтримує навчальний і метод transparency без disclosing чутливий content.

---

## Поглиблення: походження даних і результату граф

концептуально походження даних і результату форми граф:

\[
Data
\rightarrow
Experiment
\rightarrow
Output
\rightarrow
Publication.
\]

і:

\[
Code+Config
\rightarrow
Experiment.
\]

метадані stores edges.

це граф є корисний mental model для дисертація computational працювати.

---

## Поглиблення: чому ноутбук результати слід не be trusted blindly

ноутбук cell може display result з старий kernel state even якщо code cell пізніше відредаговані.

тому кінцевий ноутбук слід be:

1. restart kernel;
2. запуск усі;
3. перевірити no похибка;
4. порівнювати key результати;
5. зберігати виконані версія.

Course smoke execution підтримує це discipline.

---

## Поглиблення: CI є не substitute для локальний походження даних і результату

CI says репозиторій версія passes перевірки.

але якщо публікація result було produced locally з uncommitted зміни, CI cannot know.

отже CI і метадані complement кожен інший.

---

## Поглиблення: відмова recovery

відтворюваний робочий процес також helps коли experiment fails.

якщо запуск produces unexpected result, порівнювати:

- конфігурація diff;
- дані diff;
- коміт diff;
- залежність diff.

без походження даних і результату troubleshooting стає guessing.

---

## Поглиблення: experiment comparison

Two experiments слід be compared за допомогою явний differences.

приклад:

~~~text
A: seed=2026, noise_sd=4, reps=200
B: seed=2026, noise_sd=8, reps=200
~~~

тоді causal інтерпретація є зрозуміліше тому що лише один фактор змінений.

якщо багато параметри зміна simultaneously, attribution weakens.

це є computational experimental план.

---

## Поглиблення: контрольоване зміна principle

One-factor зміна є не завжди scientifically sufficient, але pedagogically корисний.

It дозволяє:

\[
\Delta output
\]

до be associated з один параметр зміна.

для complex interactions використовувати factorial або сценарій designs.

 key є явний план.

---

## Поглиблення: метадані слід describe purpose, не лише mechanics

Technical метадані:

- зерно генератора;
- хеш;
- версії.

науковий метадані:

- Дослідницьке питання;
- сценарій зміст;
- очікуваний ефект;
- acceptance критерій.

обидва matter.

 ідеально identified запуск з unknown purpose є усе ще hard до interpret.

---

## Поглиблення: ВІДТВОРЮВАНІСТЬ debt

Just як програмний має technical debt, дослідження може accumulate ВІДТВОРЮВАНІСТЬ debt.

Examples:

- unnamed файли;
- ручний зміни;
- missing seeds;
- незадокументовані configs;
- screenshots без джерело;
- notebooks з прихований state.

Debt зростає з час.

T1.L3 aims до prevent it early у PhD робочий процес.

---

## Поглиблення: мінімум viable ВІДТВОРЮВАНІСТЬ пакет

якщо час limited, preserve у least:

1. README команда;
2. code;
3. вхідні дані дані;
4. конфігурація;
5. зерно генератора;
6. тести;
7. метадані;
8. коміт SHA;
9. залежність файл.

це малий пакет дає великий benefit.

---

## Поглиблення: publication-grade experiment

 classroom experiment є відтворюваний коли файли rerun.

 publication-grade experiment слід additionally відповідати:

- який result entered який table/figure?
- хто/що згенерований it?
- за який code state?
- було репозиторій clean?
- були залежності зафіксований?
- були джерело дані immutable?
- може артефакт be regenerated автоматично?

це adds traceability з computation до публікація.

---

## Поглиблення: маніфест артефактів

Create manifest:

~~~text
artifact_id:
experiment_id:
source_output:
generation_script:
git_commit:
created_at:
checksum:
publication_target:
~~~

тоді figure/table стає first-class дослідження артефакт.

---

## Поглиблення: pipeline idempotence

запуск pipeline twice з той самий вхідні дані.

очікуваний:

- той самий Первинні результати;
- той самий підсумок;
- той самий метадані;
- той самий figures, modulo non-semantic метадані.

це property є called idempotent/повторюваний поведінку у практичний terms.

якщо rerun accumulates duplicate рядки або зміни result, робочий процес needs correction.

---

## Поглиблення: побічні ефекти

небезпечний experiment скрипт може:

- overwrite первинний дані;
- modify конфігурація;
- depend на поточний робочий каталог;
- append до старий результат.

Good runner слід minimize побічні ефекти.

результати слід go до designated location лише.

---

## Поглиблення: відносні шляхи

використання шляхи відносний до скрипт/проєкт покращує portability.

Hard-coded:

~~~text
C:\Users\Name\Desktop\data.csv
~~~

breaks на інший machine.

Project-relative шлях підтримує cloning.

---

## Поглиблення: позначка часу є не ідентичність

позначка часу tells коли запуск happened.

It робить не tell що параметри були використано.

So:

~~~text
run_2026_09_27
~~~

є weaker ніж конфігурація/дані/code хеш ідентичність.

позначка часу може supplement, не замінює походження даних і результату.

---

## Поглиблення: зрозумілий людині label + хеш

найкращий обидва:

~~~text
baseline_noise4_0c5d08ed47eb
~~~

Human understands purpose.

хеш ensures точний конфігурація ідентичність.

---

## Поглиблення: automated report generation

Future improvement:

experiment runner creates:

- results;
- підсумок;
- метадані;
- figures;
- short Markdown report.

тоді публікація draft references згенерований артефакти.

це зменшує ручний transcription похибки.

---

## Поглиблення: походження даних і результату як граф database idea

для великий дослідження program походження даних і результату could be represented як граф:

- дані node;
- model node;
- experiment node;
- артефакт node;
- публікація node.

Edges:

- використовує;
- згенерований;
- derived_from;
- cited_in.

You робити не need Neo4j для T1.L3.

але thinking у граф terms clarifies traceability.

---

## Поглиблення: ВІДТВОРЮВАНІСТЬ review до submission

до submitting article/дисертація chapter:

1. clone репозиторій fresh;
2. create середовище з requirements;
3. запуск тести;
4. запуск experiment;
5. regenerate результати;
6. порівнювати key metrics/артефакти;
7. перевірити citations точка до правильний запуск.

це є практичний pre-publication QA.

---

## Поглиблення: archival longevity

GitHub репозиторій може зміна.

для кінцевий дослідження archive consider:

- tagged release;
- DOI archive;
- institutional репозиторій;
- checksum bundle.

Course репозиторій teaches робочий процес; дисертація preservation може потребувати longer-term archive.

---

## Поглиблення: ВІДТВОРЮВАНІСТЬ і зрозумілий людині документація

Machine метадані самостійно недостатньою.

README слід explain:

- purpose;
- команда;
- вхідні дані;
- результати;
- обмеження.

Future дослідник може understand JSON хеш але не чому experiment exists.

науковий ВІДТВОРЮВАНІСТЬ потребує technical і conceptual документація.

---

## 77. Одна сторінка підсумку

### П’ять головних ідей

1. ВІДТВОРЮВАНІСТЬ є робочий процес property.
2. Model і experiment конфігурація є різний.
3. зерно генератора, дані, конфігурація і code версія усі matter.
4. метадані дає запуск ідентичність.
5. ВІДТВОРЮВАНІСТЬ робить не довести адекватність.

### Три правила

ручний базовий:

\[
Y=20+1.8R-1.2L.
\]

спостережуваний:

\[
Y^{obs}=\max(0,Y+\varepsilon).
\]

ідентичність експерименту:

\[
ID=f(Hash(config)).
\]

### Дві помилки

- конфігурація хеш самостійно = full ідентичність експерименту;
- ноутбук exists = відтворюваний.

### Одне питання

> Чи можу я через шість місяців перебудувати конкретний figure із дисертація без ручного guessing?

### Наступний крок

запуск базовий twice, зміна лише зерно генератора, тоді document experiment ID і коміт.

---

## 78. Фінальна думка

Складна математика не рятує слабко організований experiment.

І навпаки — навіть проста model може стати сильним дослідження артефакт, якщо:

- вхідні дані явний;
- конфігурація external;
- випадковість контрольоване;
- ПЕРЕВІРКА present;
- результати згенерований;
- метадані saved;
- code версія відомий.

Тому T1.L3 навчає не «як написати ще один Python скрипт».

Він навчає:

> **як зробити так, щоб computational result мав історію походження, яку можна перевірити, повторити й захистити.**
