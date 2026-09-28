# MathModelingIT Lab — architecture and expansion contract

## Призначення

The web layer reduces environment/setup friction and gives the learner an immediate experiment in the browser. It does **not** replace the Python пакет заняття, блокнот Jupyter, tests or дослідження-grade experiment.

The contract is:

> **browser intuition → explicit explanation → Python reproduction → дослідження Перенесення**

## Правило еталонного джерела

For every mathematical idea implemented twice:

1. Python заняття code remains the computational еталонне джерело.
2. Browser JavaScript may implement only a transparent teaching subset.
3. A shared контрольний приклад must be stored in `web/control-cases.json`.
4. CI must verify the case independently with Node and Python.
5. A browser результат must not claim more precision or scope than the Python модель supports.

## Рушій лабораторій

`web/lab-engine.js` contains pure functions with no DOM dependency. This is deliberate:

- the browser UI can call them;
- Node can test them without a browser;
- UI refactoring cannot silently change the mathematics;
- future labs can add small testable functions instead of embedding equations in event handlers.

`web/app.js` is responsible only for:

- reading UI параметри;
- rendering результати;
- saving local progress/reflections;
- exporting JSON;
- Слухач / Викладач mode.

## Єдиний навчальний цикл

Every full browser laboratory must implement:

1. **Прогноз** — learner commits to an expectation before seeing the результат.
2. **Запуск** — learner changes at least one meaningful модель parameter.
3. **Пояснення** — learner Поясненняs the observed mechanism.
4. **Перевірка меж** — learner finds a counterexample, invalid assumption or boundary.
5. **Перенесення** — learner maps the метод to a дослідження задача.

A slider plus a chart is therefore **not** sufficient to count as a completed interactive lab.

## Обов’язкові матеріали перед лабораторною

Every full interactive laboratory must begin with a visible **pre-lab resource bar** placed before the Прогноз → Запуск → Пояснення → Перевірка меж → Перенесення cycle.

The resource vocabulary is fixed:

1. **Конспект** — a button that opens the заняття `README.md` in a **new browser tab**. README is the concise technical/thematic note, not the deep theory.
2. **Теорія** — a button that opens the заняття **MathModelingIT MiniBook** web edition in a **new browser tab**. A link may be shown only when that MiniBook exists; it must never point to README.
3. **Lab instruction (PDF)** — a button that opens a versioned PDF instruction in a **new browser tab**. PDF files live under `web/instructions/`.

During the MiniBook rollout, existing interactive labs without a completed MiniBook expose **Конспект + PDF**. Once a MiniBook is published, the lab exposes **Конспект + Теорія + PDF**. The target state for all 11 заняття is the three-resource pattern.

PDF instructions must:
- be derived from the заняття `README.md` and `assignment.md`;
- describe the browser процес and its контрольні приклади;
- explicitly separate the browser teaching subset from the full Python assignment when the scopes differ;
- include completion criteria and дослідження-Перенесення expectations;
- be visually QA-checked before commit.

Course CI must verify that every PDF referenced by the current interactive labs exists and is non-empty.

## Критерії додавання нової інтерактивної лабораторії

A заняття may move from `python` to `interactive` in `web/course-catalog.js` only when all of the following exist:

- a базовий сценарій контрольний приклад with known output;
- at least one meaningful parameter to manipulate;
- an explicit “Перевірка меж the модель” scenario;
- a дослідження-Перенесення prompt;
- a pure function in the Рушій лабораторій or an explicitly precomputed scenario;
- Node перевірка;
- Python перевірка;
- an Викладач checkpoint;
- a notes/Конспект link to заняття README;
- a versioned PDF lab instruction under `web/instructions/`;
- when a MiniBook is published, a Theory link to its generated web edition.

## Запропонована черговість розширення

### Хвиля 1 — high visual payoff

- **T2.L1 optimization:** feasible region, active обмеження, цільова функція movement.
- **T2.L2 transport:** route matrix/flow diagram and forbidden-route experiment.
- **T2.L3 nonlinear optimization:** contour surface, start point and optimizer path.

### Хвиля 2 — відтворюваність and невизначеність

- **T1.L2 модель classification:** deterministic trajectory vs stochastic ensemble.
- **T1.L3 modeling organization:** seed/config/metadata відтворюваність experiment.
- **T2.L6 computer mathematics:** symbolic vs numerical solution comparison.

### Хвиля 3 — meta-modeling

- **T1.L4 метод selection:** задача features → метод selection with counterexamples.
- **T2.L7 дослідження процес:** calibration, residuals, невизначеність and alternative-модель challenge.

This order intentionally prioritizes labs where browser interaction adds information that is difficult to see in a блокнот Jupyter listing alone.

## дані and security

The first version:

- uses no accounts;
- sends no learner дані to a backend;
- stores progress and reflections in `localStorage`;
- exports learner-owned JSON files;
- uses synthetic/non-sensitive teaching дані.

If server-side functions are added later, they should be treated as a separate architecture decision rather than hidden inside the GitHub Pages layer.

## Критерії готовності for the web layer

A release candidate requires:

- all web files pass syntax checks;
- shared Node/Python контрольні приклади pass;
- existing full course smoke check passes;
- three current interactive labs reproduce their базовий сценарій Python результати;
- Слухач and Викладач modes remain progressive enhancement, not separate codebases;
- the site remains functional as a static GitHub Pages deployment;
- every interactive lab exposes its Конспект and PDF instruction before the interactive cycle;
- every published MiniBook is linked as Теорія and never masquerades README as deep theory.
