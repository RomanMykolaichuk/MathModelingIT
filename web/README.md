# MathModelingIT Lab

Статичний інтерактивний пілот для GitHub Pages.

## Мета

Скоротити шлях від відкриття матеріалу до першого осмисленого експерименту. Браузерний шар не замінює Python-код: він дає швидке інтуїтивне дослідження, після якого слухач переходить до notebook і відтворюваного computational experiment.

## Пілотні лабораторії

- T1.L1 — ресурсна модель;
- T2.L4 — CPM / critical path / delay experiment;
- T2.L5 — WSM / TOPSIS / sensitivity.

Додатково є локальний «паспорт моделі», що зберігається через localStorage та експортується у JSON.

## Локальний запуск

Можна відкрити index.html безпосередньо або використати будь-який статичний HTTP server.

## GitHub Pages

Workflow .github/workflows/pages.yml публікує лише каталог web/. У Settings → Pages для репозиторію потрібно обрати GitHub Actions як source, якщо це ще не зроблено.

## Принцип узгодження з Python

JavaScript-реалізації у пілоті відтворюють контрольні сценарії чинних lesson packages. Для подальшого масштабування потрібні shared control cases між Python і JavaScript.
