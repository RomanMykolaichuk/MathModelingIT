from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "instructions"
OUT.mkdir(parents=True, exist_ok=True)


def _font_path(*candidates: str) -> str:
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return str(path)
    raise FileNotFoundError("A Unicode font required for Ukrainian PDF generation was not found.")


REGULAR_FONT = _font_path(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
)
BOLD_FONT = _font_path(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
)

pdfmetrics.registerFont(TTFont("LabSans", REGULAR_FONT))
pdfmetrics.registerFont(TTFont("LabSans-Bold", BOLD_FONT))

ACCENT = colors.HexColor("#D4A72C")
NAVY = colors.HexColor("#102033")
MUTED = colors.HexColor("#566678")
LIGHT = colors.HexColor("#EEF2F6")
BORDER = colors.HexColor("#CDD6E0")

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleUA",
        parent=styles["Title"],
        fontName="LabSans-Bold",
        fontSize=18,
        leading=22,
        textColor=NAVY,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="SubUA",
        parent=styles["Normal"],
        fontName="LabSans",
        fontSize=9,
        leading=13,
        textColor=MUTED,
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="H1UA",
        parent=styles["Heading1"],
        fontName="LabSans-Bold",
        fontSize=13,
        leading=16,
        textColor=NAVY,
        spaceBefore=8,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyUA",
        parent=styles["BodyText"],
        fontName="LabSans",
        fontSize=9.3,
        leading=14,
        textColor=colors.HexColor("#1D2A36"),
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="BulletUA",
        parent=styles["BodyText"],
        fontName="LabSans",
        fontSize=9.2,
        leading=13.5,
        leftIndent=12,
        firstLineIndent=-7,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CalloutUA",
        parent=styles["BodyText"],
        fontName="LabSans-Bold",
        fontSize=9.4,
        leading=14,
        textColor=NAVY,
        backColor=colors.HexColor("#FFF7D8"),
        borderColor=ACCENT,
        borderWidth=0.7,
        borderPadding=8,
        spaceBefore=5,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="SmallUA",
        parent=styles["BodyText"],
        fontName="LabSans",
        fontSize=8,
        leading=11,
        textColor=MUTED,
    )
)


def _header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 12 * mm, width, 12 * mm, fill=1, stroke=0)
    canvas.setFont("LabSans-Bold", 7.5)
    canvas.setFillColor(colors.white)
    canvas.drawString(16 * mm, height - 7.6 * mm, "MathModelingIT Lab")
    canvas.setFont("LabSans", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(16 * mm, 9 * mm, "Інструкція до інтерактивної лабораторної роботи")
    canvas.drawRightString(width - 16 * mm, 9 * mm, f"Сторінка {doc.page}")
    canvas.restoreState()


def _bullet(text: str) -> Paragraph:
    return Paragraph("• " + text, styles["BulletUA"])


def _build(
    filename: str,
    code: str,
    title: str,
    purpose: str,
    baseline_rows: list[tuple[str, str]],
    workflow_steps: list[tuple[str, str]],
    break_text: str,
    transfer_text: str,
    python_extension: str,
    completion: list[str],
    source_note: str,
) -> Path:
    path = OUT / filename
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=20 * mm,
        bottomMargin=16 * mm,
        title=f"{code} - Інструкція до лабораторної роботи",
        author="MathModelingIT",
    )

    story = [
        Paragraph(f"{code} - {title}", styles["TitleUA"]),
        Paragraph(
            "Інструкція до інтерактивної лабораторної роботи у MathModelingIT Lab",
            styles["SubUA"],
        ),
        Paragraph("Мета", styles["H1UA"]),
        Paragraph(purpose, styles["BodyUA"]),
        Paragraph("Перед початком", styles["H1UA"]),
        _bullet(
            "Натисніть кнопку «Теоретичний матеріал» на сторінці лабораторії "
            "та відкрийте матеріал у новій вкладці."
        ),
        _bullet(
            "Поверніться до MathModelingIT Lab і виконуйте роботу за циклом "
            "Predict -> Run -> Explain -> Break -> Transfer."
        ),
        _bullet(
            "Не змінюйте одразу кілька параметрів, якщо завдання прямо цього не "
            "вимагає: спочатку встановіть причинний зв’язок для одного фактора."
        ),
        Paragraph("Контрольний baseline", styles["H1UA"]),
    ]

    data = [
        [
            Paragraph("<b>Параметр / результат</b>", styles["BodyUA"]),
            Paragraph("<b>Контрольне значення</b>", styles["BodyUA"]),
        ]
    ]
    for left, right in baseline_rows:
        data.append(
            [Paragraph(left, styles["BodyUA"]), Paragraph(right, styles["BodyUA"])]
        )

    table = Table(data, colWidths=[75 * mm, 88 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
                ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([table, Spacer(1, 6), Paragraph("Послідовність виконання", styles["H1UA"])])

    for index, (step, explanation) in enumerate(workflow_steps, 1):
        story.append(
            KeepTogether(
                [
                    Paragraph(f"<b>{index}. {step}</b>", styles["BodyUA"]),
                    Paragraph(explanation, styles["BodyUA"]),
                ]
            )
        )

    story.extend(
        [
            Paragraph("Break - знайдіть межу моделі", styles["H1UA"]),
            Paragraph(break_text, styles["CalloutUA"]),
            Paragraph("Transfer - перенесення у дослідження", styles["H1UA"]),
            Paragraph(transfer_text, styles["BodyUA"]),
            Paragraph("Перехід до Python-пакета", styles["H1UA"]),
            Paragraph(python_extension, styles["BodyUA"]),
            Paragraph("Результат, що вважається завершенням", styles["H1UA"]),
        ]
    )

    for item in completion:
        story.append(_bullet(item))

    story.extend(
        [
            Paragraph("Ключова вимога", styles["H1UA"]),
            Paragraph(
                "Правильний числовий результат без пояснення механізму, припущень "
                "і меж застосовності не є повним результатом лабораторної роботи.",
                styles["CalloutUA"],
            ),
            Spacer(1, 8),
            Paragraph(source_note, styles["SmallUA"]),
        ]
    )

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    return path


def generate_all() -> list[Path]:
    generated = []

    generated.append(
        _build(
            "t1_l1_lab_instruction.pdf",
            "T1.L1",
            "Форма і принципи представлення математичних моделей",
            "Перетворити прикладну постановку на формалізовану модель, дослідити "
            "вплив параметра інтенсивності витрачання та навчитися відрізняти "
            "математично можливий результат від змістовно допустимого.",
            [
                ("Початковий запас S0", "120"),
                ("Базова швидкість v1", "8"),
                ("Час вичерпання baseline", "15"),
                ("Сценарій v2", "5"),
                ("Час вичерпання scenario", "24"),
                ("Перевірка", "S(0)=S0"),
            ],
            [
                ("Predict", "До зміни параметрів запишіть, як зміна v вплине на час до вичерпання та чому."),
                ("Run", "Запустіть baseline S0=120, v1=8, horizon=20. Потім порівняйте зі сценарієм v2=5."),
                ("Explain", "Поясніть зміну через структуру S(t)=S0-vt і t*=S0/v. Не обмежуйтеся описом графіка."),
                ("Break", "Вимкніть обмеження «не допускати від’ємний ресурс» і збільшуйте горизонт або швидкість так, щоб S(t)<0."),
                ("Transfer", "Запишіть аналог об’єкта, незалежної змінної, результативної змінної, параметрів і основного припущення для власного дослідження."),
            ],
            "Продемонструйте ситуацію, коли формула продовжує обчислювати значення, "
            "але фізична інтерпретація стає неприйнятною. Поясніть, яке припущення "
            "або обмеження потрібно змінити.",
            "Сформулюйте просту модель для дисертаційної теми: об’єкт, змінні, "
            "параметри, припущення, обмеження, planned computational experiment, "
            "verification та expected interpretation.",
            "Після браузерної лабораторії відкрийте lessons/t1_l1/notebooks/practice.ipynb. "
            "Повна практична робота включає аналіз чутливості щонайменше для п’яти "
            "значень rate, графік, sanity check S(0)=S0 і короткий дослідницький висновок.",
            [
                "Заповнені поля Predict / Explain / Break / Transfer у веблабораторії.",
                "Позначка завершення лабораторії.",
                "Експортований JSON експерименту.",
                "Оновлений блок Model Passport.",
            ],
            "Джерело вимог: lessons/t1_l1/README.md та lessons/t1_l1/assignment.md.",
        )
    )

    generated.append(
        _build(
            "t2_l4_lab_instruction.pdf",
            "T2.L4",
            "Математичне моделювання із застосуванням методів мережевого планування",
            "Дослідити мережеву модель проєкту, критичний шлях, резерви часу та "
            "причинний механізм, через який локальна затримка може або не може "
            "змінити загальний строк.",
            [
                ("Baseline duration", "17"),
                ("Baseline critical path", "A -> C -> E -> G"),
                ("Slack B", "6"),
                ("Slack D", "4"),
                ("Slack F", "4"),
                ("C +3", "duration = 20"),
                ("D +3", "duration = 17"),
            ],
            [
                ("Predict", "Оберіть роботу і затримку та до запуску запишіть, чи зміниться загальна тривалість проєкту."),
                ("Run", "Спочатку перевірте baseline. Потім виконайте D+3 і C+3. Порівняйте duration, critical path і slack."),
                ("Explain", "Для кожного сценарію поясніть результат через місце роботи в мережі та доступний резерв часу."),
                ("Break", "Знайдіть таку затримку некритичної роботи, за якої резерв перестає її поглинати, або сформулюйте припущення про залежності, яке робить CPM-модель неправильною."),
                ("Transfer", "Опишіть 5–10 етапів власного дослідницького процесу, залежності між ними, тривалості та можливий bottleneck."),
            ],
            "Покажіть, що твердження «некритична робота не впливає на строк» не є "
            "універсальним: достатньо вичерпати її slack або змінити структуру "
            "залежностей. Поясніть, чому slack=4 не є гарантією за будь-яких "
            "одночасних змін мережі.",
            "Побудуйте мережеву постановку для власного дослідження: роботи/етапи, "
            "dependencies, duration estimates, дослідницький показник (строк, резерв, "
            "bottleneck або deadline probability), джерело даних і два обмеження адекватності.",
            "Веблабораторія фокусується на CPM і delay scenarios. Повний Python-пакет "
            "T2.L4 продовжує роботу через PERT і Monte Carlo: P50/P80/P90, probability "
            "finish by deadline=19 та frequency of critical paths.",
            [
                "Заповнені Predict / Explain / Break / Transfer.",
                "Перевірені baseline, D+3 і C+3.",
                "Експортований JSON зі schedule та critical path.",
                "Research-transfer запис у Model Passport.",
            ],
            "Джерело вимог: lessons/t2_l4/README.md та lessons/t2_l4/assignment.md.",
        )
    )

    generated.append(
        _build(
            "t2_l5_lab_instruction.pdf",
            "T2.L5",
            "Засоби розв’язування задач множинного вибору",
            "Дослідити, як ranking альтернатив залежить від типів критеріїв, ваг та "
            "методу агрегування; навчитися формулювати умовний, а не абсолютний "
            "висновок про лідера.",
            [
                ("WSM baseline", "C > D > B > A"),
                ("WSM score C", "~ 0.6167"),
                ("TOPSIS baseline", "C > A > D > B"),
                ("TOPSIS score C", "~ 0.5869"),
                ("При reliability = 0.10", "WSM: B; TOPSIS: C"),
            ],
            [
                ("Predict", "До руху слайдера reliability запишіть, коли очікуєте зміну лідера і чи однаково відреагують WSM та TOPSIS."),
                ("Run", "Перевірте baseline reliability=0.25. Потім зменшуйте вагу до 0.10 і спостерігайте ranking обох методів."),
                ("Explain", "Поясніть, чому WSM і TOPSIS можуть по-різному ранжувати ті самі альтернативи за однакових даних і ваг."),
                ("Break", "Знайдіть діапазон ваг, де висновок про перше місце змінюється, або сформулюйте помилку типу «cost як benefit», що змінює сенс моделі."),
                ("Transfer", "Сформуйте власну decision matrix з 3–7 альтернативами та 4–8 критеріями, визначте benefit/cost і спосіб перевірки стійкості."),
            ],
            "Не приймайте baseline ranking за об’єктивну істину. Знайдіть зміну ваг "
            "або класифікації критерію, що змінює висновок, і сформулюйте, які умови "
            "обов’язково мають супроводжувати науковий висновок.",
            "Опишіть альтернативи, критерії, benefit/cost classification, ваги, метод, "
            "sensitivity та limitations для власної задачі. Формулювання висновку має "
            "прямо залежати від цих умов.",
            "Веблабораторія демонструє baseline і one-factor sensitivity. Повний "
            "Python-пакет T2.L5 додає robustness analysis для невизначених ваг і "
            "щонайменше дві змістовні візуалізації.",
            [
                "Заповнені Predict / Explain / Break / Transfer.",
                "Перевірені WSM і TOPSIS baseline та сценарій reliability=0.10.",
                "Експортований JSON ranking/weights.",
                "У Model Passport зафіксовані критерії, припущення і limitations.",
            ],
            "Джерело вимог: lessons/t2_l5/README.md та lessons/t2_l5/assignment.md.",
        )
    )

    return generated


if __name__ == "__main__":
    for pdf in generate_all():
        print(pdf.relative_to(ROOT))
