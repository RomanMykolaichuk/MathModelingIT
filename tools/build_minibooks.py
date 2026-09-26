from __future__ import annotations

from pathlib import Path
import shutil

import markdown


ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "books"
WEB = ROOT / "web"

PUBLISHED = {
    "t1_l1": {
        "title": "T1.L1 — Форма і принципи представлення математичних моделей",
        "lab": "../../index.html#resource",
        "notes": "https://github.com/RomanMykolaichuk/MathModelingIT/blob/main/lessons/t1_l1/README.md",
    }
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
    body = md.convert(source.read_text(encoding="utf-8"))
    toc = md.toc

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
      <a href="{config['lab']}">До лабораторії</a>
    </nav>
  </header>
  <div class="book-layout">
    <aside class="book-toc">
      <p class="book-label">MINIBOOK · {book_id.upper()}</p>
      {toc}
    </aside>
    <main class="book-content">
      {body}
      <section class="book-next">
        <p>Теорію пройдено. Наступний крок — перевірити інтуїцію експериментом.</p>
        <a class="book-cta" href="{config['lab']}">Відкрити Lab T1.L1 →</a>
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
