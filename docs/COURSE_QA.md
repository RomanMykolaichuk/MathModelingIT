# Course-level QA and reproducibility gate

Цей документ описує фінальну технічну перевірку дисципліни перед створенням презентацій.

## Єдине правило

Презентаційний контур не вважається готовим до масштабної генерації, доки course-level CI не підтвердив, що source-of-truth — `lessons/` та `capstone/` — відтворюється без помилок.

## Що перевіряє `tools/course_smoke.py`

1. Наявність усіх 11 офіційних lesson packages.
2. Наявність у кожному пакеті ключових файлів: README, assignment, instructor notes, model, experiment, demo/practice notebooks, tests.
3. Рівно 11 статусів `content_stable` у `course_manifest.yaml`.
4. Повноту `capstone/`.
5. `pytest` для кожного lesson окремо та для capstone.
6. Виконання всіх 11 `demo.ipynb` і `capstone_demo.ipynb` через `nbclient` у headless режимі.
7. Формування машинозчитуваного `course_smoke_report.json`.

## Локальний запуск

```bash
pip install -r requirements.txt
python tools/course_smoke.py
```

Тільки structural check:

```bash
python tools/course_smoke.py --skip-tests --skip-notebooks
```

Тести без notebooks:

```bash
python tools/course_smoke.py --skip-notebooks
```

## CI

Workflow `.github/workflows/course-ci.yml` запускає перевірку на `push` і `pull_request`.

## Gate для presentation phase

Перехід до створення `.pptx` дозволяється, якщо:

- structure = PASS;
- усі lesson tests = PASS;
- capstone tests = PASS;
- усі demo notebooks = PASS;
- немає невідтворюваних figures/tables, які плануються до слайдів.

Якщо після створення презентації source code або model змінено, презентація переходить у `NEEDS REVIEW`.
