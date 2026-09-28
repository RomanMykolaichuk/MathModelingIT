from __future__ import annotations

from pathlib import Path
import shutil

import markdown


ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "books"
WEB = ROOT / "web"

MATH_DELIMITER_TOKENS = {
    r"\[": "MMITMATHDISPLAYOPEN9X",
    r"\]": "MMITMATHDISPLAYCLOSE9X",
    r"\(": "MMITMATHINLINEOPEN9X",
    r"\)": "MMITMATHINLINECLOSE9X",
}


def protect_math_delimiters(text: str) -> str:
    """Protect MathJax delimiters from Python-Markdown backslash escaping."""
    for delimiter, token in MATH_DELIMITER_TOKENS.items():
        text = text.replace(delimiter, token)
    return text


def restore_math_delimiters(text: str) -> str:
    """Restore MathJax delimiters after Markdown conversion."""
    for delimiter, token in MATH_DELIMITER_TOKENS.items():
        text = text.replace(token, delimiter)
    return text


PUBLISHED = {
    "t1_l1": {
        "code": "T1.L1",
        "title": "T1.L1 — Форма і принципи представлення математичних моделей",
        "lab": "../../index.html#resource",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t1_l1/README.md",
    },
    "t1_l2": {
        "code": "T1.L2",
        "title": "T1.L2 — Класифікація математичних моделей",
        "lab": "https://github.com/RomanMykolaichuk/MathModelingIT/tree/main/lessons/t1_l2",
        "lab_label": "До Python-заняття",
        "cta_label": "Відкрити Python-заняття →",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t1_l2/README.md",
    },
    "t1_l3": {
        "code": "T1.L3",
        "title": "T1.L3 — Організація математичного моделювання",
        "lab": "https://github.com/RomanMykolaichuk/MathModelingIT/tree/main/lessons/t1_l3",
        "lab_label": "До Python-заняття",
        "cta_label": "Відкрити Python-заняття →",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t1_l3/README.md",
    },
    "t1_l4": {
        "code": "T1.L4",
        "title": "T1.L4 — Класифікація методів математичного моделювання",
        "lab": "https://github.com/RomanMykolaichuk/MathModelingIT/tree/main/lessons/t1_l4",
        "lab_label": "До Python-заняття",
        "cta_label": "Відкрити Python-заняття →",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t1_l4/README.md",
    },
    "t2_l1": {
        "code": "T2.L1",
        "title": "T2.L1 — Задачі оптимізації в середовищі VS Code",
        "lab": "https://github.com/RomanMykolaichuk/MathModelingIT/tree/main/lessons/t2_l1",
        "lab_label": "До Python-заняття",
        "cta_label": "Відкрити Python-заняття →",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t2_l1/README.md",
    },
    "t2_l2": {
        "code": "T2.L2",
        "title": "T2.L2 — Математична модель транспортної задачі",
        "lab": "https://github.com/RomanMykolaichuk/MathModelingIT/tree/main/lessons/t2_l2",
        "lab_label": "До Python-заняття",
        "cta_label": "Відкрити Python-заняття →",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t2_l2/README.md",
    },
    "t2_l3": {
        "code": "T2.L3",
        "title": "T2.L3 — Математичні моделі задач нелінійного програмування",
        "lab": "https://github.com/RomanMykolaichuk/MathModelingIT/tree/main/lessons/t2_l3",
        "lab_label": "До Python-заняття",
        "cta_label": "Відкрити Python-заняття →",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t2_l3/README.md",
    },
    "t2_l4": {
        "code": "T2.L4",
        "title": "T2.L4 — Математичне моделювання із застосуванням методів мережевого планування",
        "lab": "../../index.html#network",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t2_l4/README.md",
    },
    "t2_l5": {
        "code": "T2.L5",
        "title": "T2.L5 — Засоби розв’язування задач множинного вибору",
        "lab": "../../index.html#mcda",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t2_l5/README.md",
    },
    "t2_l6": {
        "code": "T2.L6",
        "title": "T2.L6 — Системи комп'ютерної математики та їх можливості для математичного моделювання",
        "lab": "https://github.com/RomanMykolaichuk/MathModelingIT/tree/main/lessons/t2_l6",
        "lab_label": "До Python-заняття",
        "cta_label": "Відкрити Python-заняття →",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t2_l6/README.md",
    },
    "t2_l7": {
        "code": "T2.L7",
        "title": "T2.L7 — Використання систем комп’ютерної математики в наукових дослідженнях",
        "lab": "https://github.com/RomanMykolaichuk/MathModelingIT/tree/main/lessons/t2_l7",
        "lab_label": "До Python-заняття",
        "cta_label": "Відкрити Python-заняття →",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t2_l7/README.md",
    },
}


def build_book(book_id: str, config: dict[str, str]) -> Path:
    source_dir = BOOKS / book_id
    source = source_dir / "book.md"
    if not source.exists():
        raise FileNotFoundError(source)

    target_dir = WEB / "books" / book_id
    target_dir.mkdir(parents=True, exist_ok=True)

    figures = source_dir / "figures"
    target_figures = target_dir / "figures"
    if target_figures.exists():
        shutil.rmtree(target_figures)
    shutil.copytree(figures, target_figures)

    md = markdown.Markdown(
        extensions=["extra", "tables", "fenced_code", "toc"],
        extension_configs={"toc": {"permalink": True, "toc_depth": "1-3"}},
        output_format="html5",
    )
    source_text = protect_math_delimiters(source.read_text(encoding="utf-8"))
    body = restore_math_delimiters(md.convert(source_text))
    toc = restore_math_delimiters(md.toc)

    html = f"""<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="MathModelingIT MiniBook {book_id.upper()}">
  <title>MathModelingIT MiniBook · {config['title']}</title>
  <link rel="stylesheet" href="../minibook.css">
  <script>
    window.MathJax = {{
      tex: {{inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['\\\\[','\\\\]']]}},
      svg: {{fontCache: 'global'}}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
  <header class="book-topbar">
    <a href="../../index.html">← MathModelingIT Lab</a>
    <nav>
      <a href="{config['notes']}" target="_blank" rel="noopener noreferrer">Конспект ↗</a>
      <a href="{config['lab']}">{config.get('lab_label', 'До лабораторії')}</a>
    </nav>
  </header>
  <div class="book-layout">
    <aside class="book-toc">
      <p class="book-label">МІНІКНИГА · {book_id.upper()}</p>
      {toc}
    </aside>
    <main class="book-content">
      {body}
      <section class="book-next">
        <p>Теорію пройдено. Наступний крок — перевірити інтуїцію експериментом.</p>
        <a class="book-cta" href="{config['lab']}">{config.get('cta_label', f"Відкрити лабораторію {config['code']} →")}</a>
      </section>
    </main>
  </div>
</body>
</html>
"""
    output = target_dir / "index.html"
    output.write_text(html, encoding="utf-8")
    return output


def main() -> None:
    for book_id, config in PUBLISHED.items():
        output = build_book(book_id, config)
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
