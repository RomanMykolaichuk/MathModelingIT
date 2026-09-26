# MathModelingIT Lab

Статична дослідницька платформа для GitHub Pages. Її завдання — скоротити шлях від відкриття курсу до першого осмисленого обчислювального експерименту, не підміняючи Python/notebooks.

## Навчальний цикл

Кожна інтерактивна лабораторія використовує один шаблон:

**Predict → Run → Explain → Break → Transfer**

- **Predict** — слухач фіксує очікування до запуску;
- **Run** — змінює параметри та спостерігає наслідок;
- **Explain** — пояснює механізм зміни;
- **Break** — знаходить межу застосовності або контрприклад;
- **Transfer** — переносить структуру методу на власне дослідження.

## Course map

Платформа показує всі 11 занять. Повний browser experiment зараз реалізований для:

- T1.L1 — ресурсна модель;
- T2.L4 — CPM / critical path / delay experiment;
- T2.L5 — WSM / TOPSIS / sensitivity.

Решта занять присутні в course map і ведуть до чинних Python lesson packages. Це дозволяє масштабувати інтерактивність поступово, не створюючи 11 незалежних мінісайтів.

## Режими

- **Student** — експеримент, пояснення, прогрес і model passport.
- **Instructor** — додаткові teaching checkpoints та research-transfer підказки.

Режим, прогрес і рефлексії зберігаються локально в браузері. Облікові записи та сервер не потрібні.

## Архітектура

- `index.html` — структура платформи;
- `styles.css` — responsive UI;
- `course-catalog.js` — карта 11 занять;
- `lab-engine.js` — чисті математичні функції, придатні і для браузера, і для Node;
- `app.js` — UI state, rendering, localStorage та export;
- `control-cases.json` — спільні контрольні сценарії Python↔JavaScript;
- `control-cases.test.js` — перевірка browser engine у Node.

Python-side parity перевіряє `tools/verify_web_control_cases.py`.

## Quality gate

Course CI виконує:

1. syntax check JavaScript;
2. Node control cases;
3. Python verification тих самих control cases;
4. повний `tools/course_smoke.py` для 11 lesson packages і capstone.

Таким чином browser layer не може непомітно розійтися з контрольними результатами Python.

## GitHub Pages

`.github/workflows/pages.yml` публікує лише каталог `web/`. У Settings → Pages джерелом має бути **GitHub Actions**.

## Наступне масштабування

Для кожного наступного заняття browser laboratory додається лише після визначення:

1. baseline control case;
2. параметра для інтерактивного експерименту;
3. counterexample / “break the model” case;
4. research-transfer question;
5. Python↔JavaScript parity check.
