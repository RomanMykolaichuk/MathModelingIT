# MathModelingIT · Мінікнига T1.L3

## Організація математичного моделювання

### Як перетворити код на відтворюваний дослідницький процес

> **Головна ідея книги:** математична модель у науковому дослідженні — це не лише формула й не лише ноутбук. Це простежуваний workflow, де дослідницьке питання, дані, конфігурація, код, початкове значення генератора, результати, метадані і Git стан дозволяють іншому досліднику відтворити саме той результат, на який ви посилаєтесь у статті чи дисертації.

---

## 0. Паспорт книги

**Код заняття:** T1.L3 
**Тема:** організація математичного моделювання 
**Рівень:** середній 
**Орієнтовний час читання:** 70–85 хвилин 
**Попередні знання:** базова Python-модель, CSV/JSON, поняття випадковий початкове значення генератора, Git на рівні коміт.

Після цієї книги ви повинні вміти:

- розділяти дослідницьке питання, дані, модель, конфігурація, код і результати;
- пояснювати, чому ноутбук не повинен бути єдиним джерелом логіки;
- виносити параметри експеримент у конфігурація;
- використовувати початкове значення генератора як частину експеримент identity;
- формувати необроблений результати і підсумок окремо;
- розуміти роль метадані;
- пояснювати конфігурація хеш;
- відрізняти відтворюваність від адекватність;
- пов’язувати результат → експеримент ID → конфігурація/дані → Git коміт;
- проектувати мінімальний reproducible computational експеримент для власного дослідження.

---

## 1. Сцена: «А який саме запуск дав цей рисунок?»

Уявімо звичайну ситуацію під час підготовки дисертації.

У текст вставлено рисунок.

На ньому п’ять scenarios.

Через пів року керівник запитує:

> «Які параметри використовувалися саме тут?»

Відкривається ноутбук.

У ньому десятки cells.

Деякі виконані в іншому порядку.

Частина параметри змінювалась вручну.

CSV уже оновлений.

початкове значення генератора не зафіксовано.

Файл рисунок називається:

~~~text
plot_final_v2_really_final.png
~~~

І головне питання стає несподівано складним:

> **чи можемо ми точно відтворити той computational результат, на який посилається dissertation text?**

Саме це питання є центральним у T1.L3.

<figure>
 <img src="figures/fig_01_reproducibility_chain.svg" alt="Ланцюг від дослідницьке питання до Git">
 <figcaption><strong>Рис. 1.</strong> Відтворюваність виникає з повного ланцюга: питання → дані → конфігурація → модель/код → експеримент → результати → метадані → Git стан.</figcaption>
</figure>

---

## 2. відтворюваність — властивість workflow

Поширена помилка:

> «У мене є ноутбук, отже експеримент reproducible».

Не обов’язково.

ноутбук може містити:

- прихований стан;
- комірки виконані не за порядком;
- manually changed змінні;
- локальний files;
- незадокументовані версії пакетів;
- випадкові вибірки без фіксованого початкового значення генератора.

Тому відтворюваність — це не format.

Це property whole workflow.

---

## 3. Центральна логіка

У заняття зафіксовано:

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

## 4. дослідницьке питання — початок identity

Baseline питання:

> Як змінюється очікувана результативність системи при зміні ресурсу або навантаження, і як організувати цей експеримент так, щоб його можна було точно повторити?

Це навмисно simple mathematics.

Бо заняття досліджує не складність формула.

Він досліджує **organization свідчення**.

---

## 5. Математична модель

детермінований part:

\[
Y=
\max(0,\ b+\alpha R-\beta L).
\]

Де:

- \(Y\) — modeled ефективність;
- \(R\) — ресурс;
- \(L\) — load;
- \(b\) — baseline рівень;
- \(\alpha\) — ресурс gain;
- \(\beta\) — load penalty.

Baseline:

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

Це базовий перевірка приклад.

Якщо Python не повертає 32, проблема в реалізація.

---

## 7. обрізання at нуля

модель uses:

\[
Y=\max(0,\cdots).
\]

Тому modeled ефективність не від’ємний.

Наприклад:

\[
R=0,\quad L=100.
\]

необроблений вираз:

\[
20-120=-100.
\]

Після обрізання:

\[
Y=0.
\]

Це modeling припущення.

Не універсальний математичний law.

---

## 8. стохастичний спостереження

спостережуваний результат:

\[
Y^{obs}=
\max(0,Y+\varepsilon),
\]

де:

\[
\varepsilon\sim N(0,\sigma^2).
\]

Baseline:

\[
\sigma=4.
\]

детермінований модель defines очікуваний структурний відгук.

Noise моделі варіацію між окремими запусками.

---

## 9. модель порівняно з експеримент

Це ключове distinction.

### модель

форма:

\[
Y=\max(0,b+\alpha R-\beta L).
\]

### експеримент

Includes:

- який scenarios;
- як багато повтори;
- початкове значення генератора;
- noise_sd;
- результати;
- підсумок.

Змінити повтори:

\[
200\rightarrow1000
\]

— це зміна експеримент.

Змінити:

\[
Y=b+\alpha R-\beta L
\]

на нелінійний формула — зміна модель.

---

## 10. конфігурація як явний contract

Baseline experiment_config.json:

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

конфігурація робить параметри visible.

<figure>
 <img src="figures/fig_02_config_separation.svg" alt="Розділення модель код і конфігурація">
 <figcaption><strong>Рис. 2.</strong> модель код визначає математичний relation, а конфігурація — конкретні параметри експеримент. Це дозволяє змінювати сценарій дизайн без редагування core функція.</figcaption>
</figure>

---

## 11. Чому magic числа небезпечні

Погано:

~~~python
for _ in range(200):
    y = 20 + 1.8*r - 1.2*l
    obs = rng.normal(y, 4)
~~~

Числа приховані всередині коду.

Через місяць незрозуміло:

- що 200;
- чому 4;
- чи 1.8 baseline;
- чи цей файл використаний для final результат.

Краще:

> параметри live у конфігурація.

---

## 12. Scenarios як дані

сценарій table:

| сценарій | ресурс | load |
|---|---:|---:|
| baseline | 40 | 50 |
| resource_low | 30 | 50 |
| resource_high | 50 | 50 |
| load_low | 40 | 35 |
| load_high | 40 | 65 |

сценарій definitions зберігаються в CSV.

Це дані шар.

---

## 13. Чому scenarios не треба hard-code

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
- easier порівняти;
- easier replace;
- easier порівняння змін у системі контролю версій;
- separates дизайн експерименту від алгоритм.

---

## 14. Baseline детермінований сценарій значення

### baseline

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

## 15. Однаковий результат — різний mechanism

Зверніть увагу:

\[
resource\_high=50,
\]

і:

\[
load\_low=50.
\]

той самий детермінований відгук.

Але перший mechanism:

> ресурс increased.

другий:

> load decreased.

<figure>
 <img src="figures/fig_03_same_output_different_mechanism.svg" alt="Однаковий результат різних сценаріїв">
 <figcaption><strong>Рис. 3.</strong> Однакове числове \(Y=50\) не означає однаковий mechanism. сценарій identity і вхідні дані значення потрібно зберігати разом із результат.</figcaption>
</figure>

Це важливий reason не до save лише підсумкову метрику.

---

## 16. повтори

Для кожного сценарій:

\[
n=200
\]

стохастичний спостереження.

Якщо scenarios=5:

\[
5\cdot200=1000
\]

необроблений rows.

Кількість рядків — simple перевірка здорового глузду.

---

## 17. початкове значення генератора як експеримент параметр

Baseline:

\[
seed=2026.
\]

run_experiment() creates:

~~~python
rng = np.random.default_rng(2026)
~~~

той самий конфігурація + той самий scenarios + той самий код → той самий необроблений результати.

Це перевіряється перевірка.

---

## 18. відтворюваність і randomness

Це не contradiction.

стохастичний експеримент може бути reproducible, якщо pseudo-random sequence controlled.

Тоді:

> randomness exists inside модель, але computational реалізація є repeatable.

Це fundamental idea наукових обчислень.

---

## 19. необроблений результати порівняно з підсумок

необроблений результати містять один рядок на одну реалізацію.

Наприклад:

- scenario_id;
- ресурс;
- load;
- replication;
- deterministic_response;
- observed_response.

підсумок агрегує.

Це два різні artifacts.

---

## 20. підсумок metrics

summarize_results() computes:

- deterministic_response;
- mean_observed;
- std_observed;
- p10;
- p90.

Це scenario-level підсумок.

<figure>
 <img src="figures/fig_04_raw_to_summary.svg" alt="Від необроблений результати до підсумок">
 <figcaption><strong>Рис. 4.</strong> необроблений дані зберігає кожну стохастичний replication, підсумок стискає її до показників. Для відтворюваності бажано мати обидва рівні.</figcaption>
</figure>

---

## 21. Baseline спостережуваний means

README gives контрольний значення біля:

| сценарій | детермінований | середнє спостережуваний |
|---|---:|---:|
| baseline | 32.0 | ≈32.29 |
| resource_low | 14.0 | ≈14.07 |
| resource_high | 50.0 | ≈50.11 |
| load_low | 50.0 | ≈50.16 |
| load_high | 14.0 | ≈13.78 |

спостережуваний means не точно детермінований значення оскільки скінченний випадковий вибірка.

але close.

---

## 22. чому p10 і p90

середнє сам по собі hides spread.

p10:

> 10% спостереження нижче approximately це значення.

p90:

> 90% спостереження нижче це значення.

інтервал:

\[
[p10,p90]
\]

є не формальний довірчий інтервал за default.

це є емпіричний квантильний діапазон.

---

## 23. метадані

metadata.json includes:

- experiment_id;
- config_hash;
- початкове значення генератора;
- повтори;
- scenario_count;
- модель параметри;
- workflow note.

метадані answers:

> що точно згенерований ці результати?

---

## 24. Canonical JSON

Hashing має бути стійкий.

якщо JSON keys є reordered, експеримент конфігурація зміст unchanged.

функція canonical_json:

- sort_keys=істинний;
- стійкий separators.

тоді SHA-256.

це supports детермінований identity.

---

## 25. конфігурація хеш

\[
h=
SHA256(canonical\ config).
\]

Short форма перший 12 hex chars.

Baseline:

~~~text
0c5d08ed47eb
~~~

експеримент ID:

~~~text
t1_l3_0c5d08ed47eb
~~~

<figure>
 <img src="figures/fig_05_experiment_identity.svg" alt="експеримент ID через конфігурація хеш">
 <figcaption><strong>Рис. 5.</strong> конфігурація хеш створює детермінований identity конфігурації. Але повна відтворюваність потребує також код, дані і програмний середовище.</figcaption>
</figure>

---

## 26. Що конфігурація хеш доводить

Він доводить:

> canonical конфігурація content той самий.

Він не доводить:

- код той самий;
- scenarios CSV той самий;
- NumPy той самий;
- model.py той самий;
- OS/середовище той самий.

Отже, конфігурація хеш — корисний, але partial identity.

---

## 27. Git коміт

Git коміт identifies код стан.

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

Якщо рисунок у dissertation має це trace, це може бути rebuilt.

---

## 28. програмний середовище

Навіть той самий код може behave differently з changed залежності.

Тому відтворюваність пакет має include:

- Python версія;
- requirements;
- пакет версії.

поточний repo pins залежності.

Це strong foundation.

---

## 29. перевірка hierarchy

### Hand calculation

\[
Y(40,50)=32.
\]

### Bounds

\[
Y\ge0.
\]

### початкове значення генератора відтворюваність

той самий RNG початкове значення генератора → той самий спостереження sequence.

### Кількість рядків

\[
n_{rows}=n_{scenarios}\times n_{replications}.
\]

### конфігурація хеш стійкість

Key order не matter.

### Full запуск відтворюваність

той самий вхідні дані produce identical результати DataFrame.

---

## 30. тести є part дослідження infrastructure

одиниця тести не лише програмний engineering.

вони capture invariant knowledge.

для T1.L3 тести document:

- baseline рівняння;
- обрізання;
- вхідні дані validity;
- RNG відтворюваність;
- workflow size;
- конфігурація identity;
- метадані semantics.

це makes тести executable documentation.

---

## 31. Reproducible помилковий модель

важливий sentence:

> **Відтворюваність неправильного припущення не робить модель адекватною.**

 perfectly reproducible експеримент може consistently reproduce помилковий припущення.

тому два axes:

- відтворюваність;
- validity/адекватність.

---

## 32. відтворюваність порівняно з repeatability порівняно з replicability

Terminology varies через disciplines.

для це курс практичний зміст:

> another researcher може recreate той самий computational результат від preserved artifacts.

не get lost у terminology.

Focus на traceability.

---

## 33. ноутбук role

ноутбук є корисний для:

- exploration;
- narrative;
- visualization;
- interactive аналіз.

але core модель logic слід live у src/.

чому?

- importable;
- testable;
- reusable;
- easier CI;
- менше прихований стан.

---

## 34. прихований стан problem

у ноутбук:

cell 10 може depend на змінна changed у cell 3 після cell 7 already ran.

файл appears коректний.

Kernel стан є не.

Strong workflow:

> Restart kernel → запуск усі → той самий результат.

Even сильніший:

> main експеримент реалізації від command line незалежний ноутбук.

---

## 35. результати має бути згенерований, не edited

results.csv і summary.csv є derivatives.

не manually коректний them.

якщо результат помилковий:

- fix модель/конфігурація/дані;
- rerun.

ручний editing breaks походження.

---

## 36. Naming результати

Avoid:

~~~text
final.csv
final2.csv
really_final.csv
~~~

Better:

- фіксований шляхи inside експеримент directory;
- експеримент ID directory;
- метадані alongside результати.

для великий дослідження проєкт, experiment_id може name запуск folder.

---

## 37. сценарій походження

якщо scenarios.csv зміни, конфігурація хеш сам по собі не detect це.

це reveals поточний limitation.

Possible improvement:

- дані файл хеш;
- combined експеримент хеш;
- Git коміт captures файл стан.

Це excellent “злам модель/workflow” приклад.

---

## 38. Зламай workflow: той самий конфігурація, changed CSV

Keep:

~~~text
experiment_config.json
~~~

unchanged.

зміна resource_high від 50 до 55.

конфігурація хеш unchanged.

але експеримент changed.

тому:

> config_hash ≠ complete експеримент хеш.

Modernization:

- хеш конфігурація + вхідні дані files;
- або rely на Git стан + явний файл hashes.

---

## 39. Зламай workflow: той самий конфігурація, changed model.py

зміна:

\[
\alpha=1.8
\]

default у код while конфігурація усе ще supplies 1.8? немає вплив.

але зміна формула itself:

\[
Y=b+\alpha\log(1+R)-\beta L.
\]

конфігурація хеш unchanged.

експеримент identity string unchanged.

результат інший.

Hence код версія має бути recorded.

---

## 40. Зламай workflow: unpinned залежності

припустімо future NumPy поведінка зміни.

той самий код/конфігурація може produce інший результат або warning.

тому залежність snapshot має значення.

---

## 41. Зламай workflow: початкове значення генератора removed

без фіксований початкове значення генератора:

- необроблений результати зміна;
- debugging harder;
- рисунок не точно reproducible.

Statistical підсумок може бути similar, але точний артефакт identity lost.

---

## 42. Зламай workflow: ручний рисунок edits

якщо рисунок exported, тоді manually adjusted дані точки у image editor, код може немає longer reproduce рисунок.

Allowed ручний зміни:

- layout;
- labels;
- typography.

не allowed:

- зміна значення без джерело update.

---

## 43. конфігурація зміна порівняно з модель зміна

зміна:

\[
noise\_sd=4\rightarrow6.
\]

експеримент конфігурація зміна.

зміна:

\[
Y=\max(0,b+\alpha R-\beta L)
\]

до нелінійний relation.

модель зміна.

ці має бути reviewed differently.

---

## 44. чутливість via scenarios

Scenarios alter вхідні дані:

- ресурс;
- load.

конфігурація alters глобальний модель/експеримент параметри:

- повтори;
- початкове значення генератора;
- noise_sd.

це separation gives structured дизайн.

---

## 45. Noise_sd експеримент

якщо:

\[
\sigma=4\rightarrow8,
\]

детермінований відгук unchanged.

середнє спостережуваний likely remains навколо детермінований значення у symmetric, non-clipped regions.

Spread зростає.

At низький детермінований значення обрізання може affect середнє.

це connects T1.L3 з T1.L2 невизначеність concepts.

---

## 46. повтори експеримент

Increase:

\[
n=200\rightarrow2000.
\]

необроблений підсумок means часто stabilize.

але більше реалізації не fix помилковий модель.

той самий заняття як Monte Carlo.

---

## 47. Git traceability

 strong report block:

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

Це малий але powerful.

---

## 48. рисунок походження

<figure>
 <img src="figures/fig_06_figure_provenance.svg" alt="Простежуваність рисунка">
 <figcaption><strong>Рис. 6.</strong> рисунок у публікація повинна мати шлях назад до результат дані, експеримент ID, конфігурація/дані та код версія.</figcaption>
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

## 49. метадані як науковий свідчення

метадані є не decoration.

це allows питання:

- що початкове значення генератора?
- що конфігурація?
- як багато scenarios?
- який параметри?
- що експеримент identity?

без метадані результат файл є orphaned.

---

## 50. відтворюваність checklist

до citing результат:

### дослідницьке питання

відомий?

### дані

Stored і documented?

### модель

формула і припущення записані явно?

### конфігурація

параметри externalized?

### Execution

один command?

### перевірка

контрольний приклад?

### метадані

експеримент ID/хеш?

### Git

код версія відомий?

### інтерпретація

немає overclaim?

---

## 51. прогнозувати до запуск

до changing конфігурація, write:

### якщо повтори ↑

що зміни?

### якщо noise_sd ↑

що зміни?

### якщо початкове значення генератора зміни лише

що зміни?

очікуваний:

- необроблений спостереження зміна;
- детермінований відгук unchanged;
- розподіл shape similar у aggregate.

---

## 52. Python без страху: детермінований відгук

~~~python
y = deterministic_response(
    resource=40,
    load=50,
)
assert y == 32
~~~

Це direct перевірка.

---

## 53. Python без страху: запуск експеримент

~~~python
results = run_experiment(
    config,
    scenarios,
)
~~~

очікуваний Кількість рядків:

\[
5\times200=1000.
\]

---

## 54. Python без страху: підсумок

~~~python
summary = summarize_results(results)
~~~

результат includes:

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

Baseline:

~~~text
t1_l3_0c5d08ed47eb
~~~

---

## 56. чому хеш key order стійкий

конфігурація:

~~~json
{"seed":2026,"replications":200}
~~~

і:

~~~json
{"replications":200,"seed":2026}
~~~

той самий semantic mapping.

canonical_json sorts keys.

отже той самий хеш.

Це unit-tested.

---

## 57. синтетичний військовий context

припустімо \(Y\) є синтетичний ефективність indicator training-support процес.

\(R\) — умовний ресурс.

\(L\) — умовний workload.

немає реальний одиниця, немає actual операційний ефективність.

 приклад demonstrates workflow, не реальний decision recommendation.

---

## 58. дослідження Transfer

питання:

> Як організувати computational експеримент для одного fragment власної dissertation?

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

## 59. приклад transfer: модель калібрування workflow

Imagine dissertation модель оцінки параметр від синтетичні дані.

Reproducible workflow:

1. необроблений дані файл;
2. preprocessing script;
3. калібрування конфігурація;
4. початкове значення генератора;
5. підігнаний параметри;
6. diagnostic plots;
7. метадані;
8. коміт;
9. результат table.

T1.L3 структура transfers directly.

---

## 60. Versioning дані

Git works well для малий text CSV.

великий або sensitive дані може need:

- дані registry;
- об’єкт storage;
- checksum;
- access-controlled repository.

важливий principle remains:

> результат має reference точний дані версія.

---

## 61. Sensitive/замкнений дані

у військовий дослідження, дані може не бути publishable.

відтворюваність усе ще possible inside controlled середовище.

Preserve:

- дані версія ID;
- хеш;
- schema;
- access conditions;
- код/конфігурація.

Public артефакт може use синтетичний equivalent while documenting difference.

---

## 62. середовище snapshot

Requirements файл gives залежність версії.

для сильніший відтворюваність also record:

- Python версія;
- OS/container image;
- hardware якщо relevant;
- CUDA/GPU для стохастичний/чисельний workloads where результати depend на backend.

не every експеримент needs усі details.

Record що може materially зміна результати.

---

## 63. детермінований результати є не automatically reproducible

Even детермінований формула може fail відтворюваність якщо:

- дані changed;
- код changed;
- конфігурація unknown;
- preprocessing hidden.

Randomness є не лише threat.

---

## 64. відтворюваність levels

### рівень 0

Screenshot лише.

### рівень 1

ноутбук + дані.

### рівень 2

src + конфігурація + дані + початкове значення генератора.

### рівень 3

тести + метадані + Git коміт.

### рівень 4

середовище + automated pipeline/CI.

курс aims toward рівень 3–4.

<figure>
 <img src="figures/fig_07_reproducibility_levels.svg" alt="Рівні відтворюваності">
 <figcaption><strong>Рис. 7.</strong> відтворюваність посилюється шарами: артефакт → код/дані → конфігурація/початкове значення генератора → тести/метадані/Git → automated середовище.</figcaption>
</figure>

---

## 65. CI як відтворюваність assistant

курс CI executes тести і notebooks.

це не може prove дослідження validity.

але це може detect:

- broken imports;
- changed контрольний значення;
- missing files;
- non-executable ноутбук.

Automation reduces accidental drift.

---

## 66. Зламай систему: результат без identity

припустімо summary.csv says:

~~~text
baseline mean_observed=32.29
~~~

але немає конфігурація/хеш/коміт.

може ми use number?

ми може read це.

може ми defend its походження?

Weakly.

отже результат без identity є scientifically fragile.

---

## 67. Typical thinking похибки

### «Якщо код є, результат reproducible»

не enough.

### «той самий конфігурація хеш = той самий експеримент»

не якщо дані/код differ.

### «Git replaces метадані»

немає.

Git identifies repository стан, метадані identifies запуск.

### «початкове значення генератора makes стохастичний висновок істинний»

немає.

початкове значення генератора makes запуск repeatable.

### «Reproducible = valid»

немає.

помилковий модель може reproduce perfectly.

---

## 68. модель аудит порівняно з workflow аудит

### модель аудит

- формула;
- припущення;
- параметри;
- адекватність.

### Workflow аудит

- files;
- конфігурація;
- execution;
- метадані;
- versioning.

Strong dissertation computational work needs обидва.

---

## 69. One-command principle

 good експеримент слід мають clear command:

~~~bash
python -m lessons.t1_l3.src.experiment
~~~

це reduces hidden ручний steps.

якщо full rebuild requires 17 undocumented clicks, відтворюваність suffers.

---

## 70. Immutable необроблений вхідні дані

Ideally необроблений вхідні дані є не overwritten за експеримент.

Derived дані goes до результати.

це preserves джерело.

для transformations, save script і intermediate якщо scientifically relevant.

---

## 71. результат overwrite issue

поточний заняття writes фіксований результати directory.

для навчальний Це simple.

для дослідження масштаб, overwriting old експеримент може бути undesirable.

Modernization:

~~~text
outputs/<experiment_id>/
~~~

або timestamp + хеш.

тоді реалізації coexist.

---

## 72. експеримент registry

 малий CSV/JSON index може contain:

- experiment_id;
- date;
- коміт;
- конфігурація;
- note;
- статус.

це helps великий dissertation проєкти.

не required baseline, але natural розширення.

---

## 73. Allowed висновок

Strong:

> для конфігурація хеш 0c5d08ed47eb, початкове значення генератора 2026 і five scenarios з 200 повтори кожний, baseline детермінований відгук є 32 і середнє спостережуваний є approximately 32.29. результат є reproducible для той самий код, конфігурація, сценарій дані і програмний середовище.

Also стан:

> Це не validate лінійний ресурс/load припущення.

---

## 74. Від мінікнига до practice

до практичний:

1. запуск baseline;
2. record experiment_id;
3. перевірити Y=32;
4. rerun і порівняти результати;
5. зміна лише початкове значення генератора;
6. зміна конфігурація;
7. add scenarios;
8. record Git коміт.

---

## 75. дослідження артефакт passport

Create для кожний важливий результат:

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

Це практичний dissertation discipline.

---

## 76. Workflow architecture

<figure>
 <img src="figures/fig_08_project_architecture.svg" alt="Архітектура reproducible проєкт">
 <figcaption><strong>Рис. 8.</strong> Хороша структура розділяє джерело код, вхідні дані, конфігурація, notebooks і згенерований результати. Кожен шар має власну responsibility.</figcaption>
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

## Поглиблення: відтворюваність має кілька рівнів identity

У baseline experiment_id залежить від конфігурація.

Але повний computational результат depends на broader стан.

Корисно мислити шарами.

### конфігурація identity

\[
ID_{config}=Hash(config).
\]

### дані identity

\[
ID_{data}=Hash(input\ files).
\]

### код identity

Git коміт:

\[
ID_{code}=commit\ SHA.
\]

### середовище identity

залежність lock / container digest.

### запуск identity

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

курс реалізація intentionally simpler.

Але ця hierarchy показує шлях розвитку dissertation infrastructure.

---

## Поглиблення: чому Git коміт сам по собі є не enough

Git коміт tells точний repository стан лише якщо:

- усі relevant files tracked;
- немає uncommitted зміни;
- external дані версія відомий;
- середовище відомий.

якщо локальний script modified але не committed, коміт SHA точки до another стан.

тому публікація запуск слід ideally початок від clean working tree.

якщо не, Це відтворюваність limitation.

---

## Поглиблення: dirty working tree

Imagine:

- коміт = abc123;
- model.py edited locally;
- експеримент запуск;
- зміна не committed.

метадані records abc123.

Later checkout abc123 gives old модель.

результат не може бути reproduced точно.

Possible improvement:

- refuse публікація запуск коли repo dirty;
- record diff;
- auto-capture patch.

для курс, awareness є enough.

---

## Поглиблення: вхідні дані дані hashing

конфігурація хеш protects конфігурація.

Add:

\[
h_{data}=SHA256(file\ bytes).
\]

тоді метадані може include scenario-data checksum.

Now сценарій зміна detectable even якщо filename той самий.

це directly fixes один break-the-workflow приклад.

---

## Поглиблення: код версія у метадані

поточний метадані note says reproducible для той самий код/конфігурація/дані/середовище.

 сильніший реалізація може automatically query Git коміт і store це.

якщо Git unavailable, метадані слід стан:

~~~text
git_commit: unavailable
~~~

rather than invent certainty.

---

## Поглиблення: залежність snapshot

Pinned requirements у repository help.

але installed середовище може усе ще differ якщо user ignores them.

 запуск може record:

~~~text
python --version
pip freeze
~~~

або selected критичний версії.

для науковий work корисний fields include:

- Python;
- NumPy;
- pandas;
- SciPy;
- SymPy;
- Matplotlib.

для GPU workflows also backend версії.

---

## Поглиблення: середовище відтворюваність порівняно з portability

точний середовище replication є strong але може бутиcome brittle над years.

альтернатива goal:

> portable відтворюваність.

це means код works за documented версія range, з тести verifying результати/tolerances.

там є trade-off між freezing everything точно і maintaining portable tested пакет.

курс chooses pinned stack для educational стійкість.

---

## Поглиблення: необроблений дані має бути immutable

 strong rule:

> необроблений вхідні дані є never overwritten за експеримент.

чому?

якщо той самий файл є modified in-place, historical результат loses джерело.

Prefer:

~~~text
data/raw/
data/processed/
outputs/
~~~

Transformation script creates processed дані від необроблений.

тоді походження є явний.

---

## Поглиблення: preprocessing є part модель pipeline

Researchers sometimes think:

> preprocessing є just preparation.

але filtering, imputation, нормалізація і aggregation може зміна результати.

тому preprocessing код belongs у відтворюваність chain.

якщо CSV є manually cleaned у spreadsheet і overwritten, походження weakens.

---

## Поглиблення: експеримент конфігурація schema

JSON конфігурація є корисний, але може contain invalid типи.

для larger проєкт define schema:

- required keys;
- type обмеження;
- allowed ranges;
- defaults.

поточний validate_config перевірки:

- початкове значення генератора;
- повтори;
- модель;
- додатний повтори;
- nonnegative noise_sd.

Це перший крок toward schema валідація.

---

## Поглиблення: чому явний валідація має значення

без валідація від’ємний replication count або від’ємний noise значення може fail strangely later.

валідація creates early, meaningful похибка.

Це part науковий якість.

Bad вхідні дані має бути rejected до expensive обчислення.

---

## Поглиблення: результат determinism

для той самий конфігурація/дані/код/початкове значення генератора baseline необроблений DataFrame має бути identical.

перевірка:

~~~python
pd.testing.assert_frame_equal(a, b)
~~~

Це сильніший than saying це means є close.

це перевірки точний computational repeatability.

для some parallel/GPU workflows bitwise identity може не бути realistic.

тоді відтворюваність критерій має use tolerances.

---

## Поглиблення: точний порівняно з statistical відтворюваність

### точний

той самий необроблений числа.

Appropriate для це CPU pseudo-random workflow.

### чисельний

Differences within допуск.

Common для floating-point solvers.

### Statistical

інший вибірки але той самий distribution-level висновки.

Common для стохастичний HPC.

до claiming відтворюваність define який рівень intended.

---

## Поглиблення: експеримент registry дизайн

коли dissertation має багато реалізації, один метадані файл per результат directory є не enough для overview.

Create registry:

| experiment_id | коміт | конфігурація | дані | purpose | статус |
|---|---|---|---|---|---|
| exp001 | abc | cfg1 | d1 | baseline | accepted |
| exp002 | def | cfg2 | d1 | чутливість | exploratory |

це prevents “який запуск було final?” confusion.

---

## Поглиблення: exploratory порівняно з confirmatory реалізації

During exploration researcher tries багато configs.

Later select аналіз план.

це є корисний до mark:

- exploratory;
- валідація;
- final/публікація.

Otherwise результат selection може бути opaque.

метадані може include purpose tag.

---

## Поглиблення: публікація артефакт mapping

припустімо dissertation contains:

- Table 3.2;
- рисунок 3.4;
- metric у paragraph.

Create mapping:

~~~text
Figure 3.4 -> experiment_id X -> script Y -> output Z
Table 3.2  -> experiment_id Q -> summary.csv
~~~

тоді revision стає manageable.

---

## Поглиблення: один джерело truth для figures

не copy значення manually від terminal into Excel, тоді chart.

Better:

\[
data
\rightarrow
script
\rightarrow
figure.
\]

якщо style adjustment потрібний, script controls це.

це keeps числа linked до обчислення.

---

## Поглиблення: checksums для публікація artifacts

для final рисунок або table, optional checksum може prove файл identity.

для приклад:

\[
SHA256(figure.png).
\]

це може бути overkill для classroom use.

але корисний у audited pipelines.

---

## Поглиблення: відтворюваність за closed-data обмеження

військовий і defence дослідження може мають дані це не може leave secure середовище.

відтворюваність може усе ще бути designed.

Inside secure мережа preserve:

- точний необроблений дані;
- версія/хеш;
- scripts;
- конфігурація;
- середовище;
- результати;
- access rules.

Outside secure мережа publish:

- синтетичні данінабір;
- schema;
- метод;
- limitations.

не confuse public відтворюваність з internal відтворюваність.

---

## Поглиблення: синтетичний twin dataset

 корисний pattern:

1. confidential реальних данихнабір використаний у secure аналіз;
2. синтетичні данінабір preserves структура, не sensitive значення;
3. public repo demonstrates workflow;
4. secure метадані links internal результат до реальних даних версія.

це supports навчальний і метод transparency без disclosing sensitive content.

---

## Поглиблення: походження graph

Conceptually походження forms graph:

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

це graph є корисний mental модель для dissertation computational work.

---

## Поглиблення: чому ноутбук результати слід не бути trusted blindly

ноутбук cell може display результат від old kernel стан even якщо код cell later edited.

тому final ноутбук має бути:

1. restart kernel;
2. запуск усі;
3. перевірити немає похибка;
4. порівняти key результати;
5. save executed версія.

курс smoke execution supports це discipline.

---

## Поглиблення: CI є не substitute для локальний походження

CI says repository версія passes перевірки.

але якщо публікація результат було produced locally з uncommitted зміни, CI не може know.

отже CI і метадані complement кожний other.

---

## Поглиблення: відмова recovery

Reproducible workflow also helps коли експеримент fails.

якщо запуск produces unexpected результат, порівняти:

- конфігурація diff;
- дані diff;
- коміт diff;
- залежність diff.

без походження troubleshooting стає guessing.

---

## Поглиблення: експеримент comparison

два experiments має бути compared за явний differences.

приклад:

~~~text
A: seed=2026, noise_sd=4, reps=200
B: seed=2026, noise_sd=8, reps=200
~~~

тоді causal інтерпретація є clearer оскільки лише один factor changed.

якщо багато параметри зміна simultaneously, attribution weakens.

Це computational experimental дизайн.

---

## Поглиблення: controlled зміна principle

One-factor зміна є не always scientifically sufficient, але pedagogically корисний.

це allows:

\[
\Delta output
\]

до бути associated з один параметр зміна.

для complex interactions use factorial або сценарій designs.

 key є явний дизайн.

---

## Поглиблення: метадані слід describe purpose, не лише mechanics

Technical метадані:

- початкове значення генератора;
- хеш;
- версії.

науковий метадані:

- дослідницьке питання;
- сценарій зміст;
- очікуваний вплив;
- acceptance критерій.

обидва matter.

 perfectly identified запуск з unknown purpose є усе ще важким для інтерпретації.

---

## Поглиблення: відтворюваність debt

Just як програмний має technical debt, дослідження може accumulate відтворюваність debt.

Examples:

- unnamed files;
- ручний зміни;
- missing seeds;
- undocumented configs;
- screenshots без джерело;
- notebooks з прихований стан.

Debt grows з time.

T1.L3 aims до prevent це early у PhD workflow.

---

## Поглиблення: minimum viable відтворюваність пакет

якщо time limited, preserve at least:

1. README command;
2. код;
3. вхідні дані дані;
4. конфігурація;
5. початкове значення генератора;
6. тести;
7. метадані;
8. коміт SHA;
9. залежність файл.

це малий пакет gives великий виграш.

---

## Поглиблення: publication-grade експеримент

 classroom експеримент є reproducible коли files rerun.

 publication-grade експеримент слід additionally answer:

- який результат entered який table/рисунок?
- who/що згенерований це?
- за який код стан?
- було repository clean?
- були залежності recorded?
- були джерело дані immutable?
- може артефакт бути regenerated automatically?

це adds traceability від обчислення до публікація.

---

## Поглиблення: артефакт manifest

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

тоді рисунок/table стає first-class дослідження артефакт.

---

## Поглиблення: pipeline idempotence

запуск pipeline twice з той самий вхідні дані.

очікуваний:

- той самий необроблений результати;
- той самий підсумок;
- той самий метадані;
- той самий figures, modulo non-semantic метадані.

це property є called idempotent/repeatable поведінка у практичний terms.

якщо rerun accumulates duplicate rows або зміни результат, workflow needs correction.

---

## Поглиблення: side effects

Dangerous експеримент script може:

- overwrite необроблений дані;
- modify конфігурація;
- depend на поточний working directory;
- append до old результат.

Good runner слід minimize side effects.

результати слід go до designated location лише.

---

## Поглиблення: relative шляхи

Using шляхи relative до script/проєкт improves portability.

Hard-coded:

~~~text
C:\Users\Name\Desktop\data.csv
~~~

breaks на another machine.

Project-relative шлях supports cloning.

---

## Поглиблення: timestamp є не identity

Timestamp tells коли запуск happened.

це не tell що параметри були використаний.

тому:

~~~text
run_2026_09_27
~~~

є weaker than конфігурація/дані/код хеш identity.

Timestamp може supplement, не replace походження.

---

## Поглиблення: human-readable label + хеш

найкращий обидва:

~~~text
baseline_noise4_0c5d08ed47eb
~~~

Human understands purpose.

хеш ensures точний конфігурація identity.

---

## Поглиблення: automated report generation

Future improvement:

експеримент runner creates:

- результати;
- підсумок;
- метадані;
- figures;
- short Markdown report.

тоді публікація draft references згенерований artifacts.

це reduces ручний transcription похибки.

---

## Поглиблення: походження як graph database idea

для великий дослідження program походження може бути represented як graph:

- дані node;
- модель node;
- експеримент node;
- артефакт node;
- публікація node.

Edges:

- uses;
- згенерований;
- derived_from;
- cited_in.

You не need Neo4j для T1.L3.

але thinking у graph terms clarifies traceability.

---

## Поглиблення: відтворюваність review до submission

до submitting article/dissertation chapter:

1. clone repository fresh;
2. create середовище від requirements;
3. запуск тести;
4. запуск експеримент;
5. regenerate результати;
6. порівняти key metrics/artifacts;
7. перевірити citations точка до коректний запуск.

Це практичний pre-publication QA.

---

## Поглиблення: archival longevity

GitHub repository може зміна.

для final дослідження archive consider:

- tagged release;
- DOI archive;
- institutional repository;
- checksum bundle.

курс repository teaches workflow; dissertation preservation може require longer-term archive.

---

## Поглиблення: відтворюваність і human-readable documentation

Machine метадані сам по собі insufficient.

README слід explain:

- purpose;
- command;
- вхідні дані;
- результати;
- limitations.

Future researcher може understand JSON хеш але не чому експеримент exists.

науковий відтворюваність requires technical і conceptual documentation.

---

## 77. Одна сторінка підсумку

### П’ять головних ідей

1. відтворюваність є workflow property.
2. модель і експеримент конфігурація є інший.
3. початкове значення генератора, дані, конфігурація і код версія усі matter.
4. метадані gives запуск identity.
5. відтворюваність не prove адекватність.

### Три правила

ручний baseline:

\[
Y=20+1.8R-1.2L.
\]

спостережуваний:

\[
Y^{obs}=\max(0,Y+\varepsilon).
\]

експеримент identity:

\[
ID=f(Hash(config)).
\]

### Дві помилки

- конфігурація хеш сам по собі = full експеримент identity;
- ноутбук exists = reproducible.

### Одне питання

> Чи можу я через шість місяців перебудувати конкретний рисунок із dissertation без ручного guessing?

### Наступний крок

запуск baseline twice, зміна лише початкове значення генератора, тоді document експеримент ID і коміт.

---

## 78. Фінальна думка

Складна математика не рятує слабко організований експеримент.

І навпаки — навіть проста модель може стати сильним дослідження артефакт, якщо:

- вхідні дані явний;
- конфігурація external;
- randomness controlled;
- перевірка present;
- результати згенерований;
- метадані saved;
- код версія відомий.

Тому T1.L3 навчає не «як написати ще один Python script».

Він навчає:

> **як зробити так, щоб computational результат мав історію походження, яку можна перевірити, повторити й захистити.**
