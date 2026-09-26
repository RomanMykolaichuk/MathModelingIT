# MathModelingIT

Навчальний репозиторій дисципліни з математичного моделювання для **ад’юнктів**.

## Поточний статус

- **11/11 офіційних занять:** `content_stable`;
- **capstone:** сформований і локально перевірений;
- **course-level QA:** автоматизований через GitHub Actions;
- **presentation phase:** manifest фіксує згенерований початковий пакет; PPTX/ZIP не зберігаються у поточному дереві репозиторію;
- **interactive lab pilot:** розробляється окремий статичний інтерфейс у `web/` для GitHub Pages.

## Концепція

Дисципліна не перетворюється на окремий курс програмування Python. Python використовується як наскрізний інструмент реалізації та дослідження математичних моделей:

> **прикладна задача → математична постановка → формалізація → Python-модель → обчислювальний експеримент → візуалізація → інтерпретація → науковий висновок**

Офіційні назви тем і занять зберігаються. Змінюється внутрішня методика: від теоретичного розгляду моделей — до відтворюваного computational modeling workflow.

## Цільова аудиторія

Ад’юнкти, для яких математичне моделювання має бути не лише навчальною дисципліною, а інструментом власного наукового дослідження.

## Основний результат навчання

Здатність формалізувати прикладну або наукову задачу у вигляді математичної моделі, обґрунтовано обрати метод її дослідження, реалізувати модель засобами Python, провести відтворюваний обчислювальний експеримент, проаналізувати й візуалізувати результати та сформулювати обґрунтований висновок.

## Технологічний стек

- Python
- NumPy
- pandas
- SciPy
- Matplotlib
- SymPy
- NetworkX
- PuLP / OR-Tools
- Jupyter
- VS Code
- Git / GitHub

## Структура розроблення

Репозиторій розвивається у двох пов’язаних, але окремих потоках:

1. **Навчально-обчислювальний контур** — зміст занять, Python-код, notebooks, дані, завдання, результати та мініпроєкти.
2. **Презентаційний контур** — окремі презентації до кожного заняття, які створюються тільки після стабілізації змісту та практики відповідного заняття.

Окремо сформований **capstone**, який інтегрує калібрування, оптимізацію, independent verification, sensitivity, uncertainty та reproducibility metadata в одному mini-research project.

Докладніше:

- [`docs/COURSE_TASK.md`](docs/COURSE_TASK.md) — зафіксоване завдання на розроблення дисципліни;
- [`docs/DEVELOPMENT_PLAN.md`](docs/DEVELOPMENT_PLAN.md) — поетапний план реалізації;
- [`docs/LESSON_STANDARD.md`](docs/LESSON_STANDARD.md) — єдиний стандарт одного заняття;
- [`docs/PRESENTATION_WORKFLOW.md`](docs/PRESENTATION_WORKFLOW.md) — окремий процес створення презентацій;
- [`docs/COURSE_QA.md`](docs/COURSE_QA.md) — course-level QA та reproducibility gate;
- [`course_manifest.yaml`](course_manifest.yaml) — перелік усіх 11 занять, capstone і поточний статус;
- [`capstone/`](capstone/) — підсумковий інтеграційний mini-research project;
- [`tools/course_smoke.py`](tools/course_smoke.py) — повна структурна, тестова та notebook-перевірка курсу.

## Принцип розроблення

Для кожного заняття спочатку формується методична й обчислювальна основа:

`lesson brief → model → notebook/code → experiment → expected outputs → verification → instructor notes`

і лише після цього:

`lesson content → slide narrative → presentation → visual QA`.

Це дозволяє підтримувати відповідність між математичною моделлю, кодом, практичним завданням і презентаційним матеріалом.

## Course-level QA

Повна перевірка запускається командою:

```bash
python tools/course_smoke.py
```

GitHub Actions workflow `.github/workflows/course-ci.yml` перевіряє:

- структуру всіх 11 lesson packages;
- усі lesson tests;
- виконання всіх `demo.ipynb`;
- capstone tests і notebook;
- відповідність manifest статусам `content_stable`.

До презентацій переходять тільки після проходження цього gate.


## MathModelingIT Lab — interactive course layer

Каталог `web/` тепер є єдиним браузерним шаром для всіх 11 занять. Три лабораторії — **T1.L1, T2.L4, T2.L5** — мають повний інтерактивний цикл **Predict → Run → Explain → Break → Transfer**; решта занять представлені в course map і ведуть до Python lesson packages.

Платформа має режими **Student / Instructor**, локальне збереження прогресу та рефлексій, export JSON і накопичуваний model passport. Математичні функції винесені у `web/lab-engine.js`.

Ключовий принцип: Python/notebooks залишаються source of truth. Файл `web/control-cases.json` задає спільні контрольні сценарії, які Course CI перевіряє і через Node, і через Python (`tools/verify_web_control_cases.py`).

Докладніше: [`web/README.md`](web/README.md).
