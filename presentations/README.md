# Presentation phase

Цей каталог фіксує окремий презентаційний контур дисципліни **MathModelingIT**.

Презентації створюються тільки після стабілізації навчально-обчислювального контуру:

`lesson package -> verified code -> demo notebook -> practice notebook -> presentation brief -> slide plan -> narrative -> PPTX -> visual QA`

## Поточний стан

- 11/11 занять мають `content_stable`.
- Capstone має `content_stable`.
- Course CI зелений: 11 lesson structures, capstone, 98 Python tests, 12 demo notebooks.
- Створено початковий пакет із 11 PPTX-презентацій у єдиному академічному стилі.

## Принципи презентацій

1. Презентація не замінює notebook і не дублює код повністю.
2. Кожна презентація пояснює: **навіщо модель потрібна, як вона формалізується, як реалізується в Python, як перевіряється і як інтерпретується**.
3. Числові результати беруться з перевірених lesson packages.
4. Кожна презентація завершується research-transfer блоком для ад’юнктів.
5. PPTX-файли можуть генеруватися як артефакти релізу або додаватися окремо після затвердження стилю.

## Структура одного deck

Типовий deck має 8 слайдів:

1. Title
2. Lesson logic
3. Mathematical model
4. Python implementation
5. Computational experiment
6. Verification and reproducibility
7. Practice and research transfer
8. Summary

## Наступний етап

Після перегляду початкового PPTX-пакета необхідно:

- уточнити стиль, якщо потрібно;
- додати заняттєві графіки безпосередньо з `outputs/` lesson packages;
- за потреби створити повні narrative scripts для усного супроводу;
- зробити visual QA кожної презентації окремо.
